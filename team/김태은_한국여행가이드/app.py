import os
import json
import time
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import anthropic
from apscheduler.schedulers.background import BackgroundScheduler

from core.location import auto_expand_radius, haversine, walk_minutes
from core.session import (
    create_session,
    get_session,
    get_or_create_session,
    add_message,
    get_history,
    cleanup_expired,
    active_session_count,
)

# ─── 설정 ───────────────────────────────────────────────────────────────────
HAIKU_MODEL = os.getenv("HAIKU_MODEL", "claude-haiku-4-5-20251001")
SONNET_MODEL = os.getenv("SONNET_MODEL", "claude-sonnet-4-5")
MAX_TOKENS_HAIKU = 512
MAX_TOKENS_SONNET = 1024

BASE_DIR = Path(__file__).parent
RESTAURANTS_FILE = BASE_DIR / "data" / "restaurants.json"

# ─── 앱 초기화 ────────────────────────────────────────────────────────────
app = FastAPI(title="Korea Local Guide — Restaurant Recommender")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

with open(RESTAURANTS_FILE, "r", encoding="utf-8") as f:
    RESTAURANTS: list[dict] = json.load(f)

# ─── APScheduler: 만료 세션 정리 ─────────────────────────────────────────
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_expired, "interval", hours=1)
scheduler.start()


# ─── Pydantic Models ─────────────────────────────────────────────────────

class RecommendRequest(BaseModel):
    food_preference: str = ""
    location: str = "Seoul"
    lat: Optional[float] = None
    lng: Optional[float] = None
    session_id: Optional[str] = None


class Restaurant(BaseModel):
    id: int
    name: str
    korean_name: str
    category: str
    location: str
    address: str
    rating: float
    price_range: str
    english_menu: bool
    description: str
    hours: str
    tags: list[str] = []
    reason: str = ""
    distance_km: Optional[float] = None
    walk_minutes: Optional[int] = None
    google_maps_url: str = ""


class RecommendResponse(BaseModel):
    recommendations: list[Restaurant]
    ai_message: str
    session_id: str
    search_radius_km: Optional[float] = None


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


class ChatResponse(BaseModel):
    reply: str
    recommendations: Optional[list[Restaurant]] = None
    session_id: str


class RestaurantDetail(BaseModel):
    id: int
    name: str
    korean_name: str
    category: str
    tags: list[str] = []
    location: str
    address: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    rating: float
    price_range: str
    english_menu: bool
    description: str
    hours: str
    signature_dishes: list[str] = []
    atmosphere_tags: list[str] = []
    pros_cons: dict = {"pros": [], "cons": []}
    google_maps_url: str = ""


# ─── 헬퍼 함수 ───────────────────────────────────────────────────────────

def make_google_maps_url(r: dict) -> str:
    """식당 좌표 또는 주소로 Google Maps URL 생성."""
    lat = r.get("lat")
    lng = r.get("lng")
    if lat and lng:
        return f"https://www.google.com/maps/search/?api=1&query={lat},{lng}"
    return f"https://www.google.com/maps/search/?api=1&query={quote(r.get('address', r.get('name', '')))}"


def build_restaurant_text(restaurants: list[dict]) -> str:
    """식당 목록을 Claude 프롬프트용 텍스트로 변환."""
    lines = []
    for r in restaurants:
        dist_info = ""
        if r.get("distance_km") is not None:
            dist_info = f" | Distance: {r['distance_km']}km ({r.get('walk_minutes', '?')} min walk)"
        lines.append(
            f"[ID:{r['id']}] {r['name']} ({r['korean_name']}) | "
            f"Category: {r['category']} | Tags: {', '.join(r.get('tags', []))} | "
            f"Location: {r['location']} | Rating: {r['rating']} | "
            f"Price: {r['price_range']} | English menu: {r['english_menu']} | "
            f"Hours: {r['hours']}{dist_info}"
        )
    return "\n".join(lines)


def parse_ai_recommendations(
    raw: str,
    source_restaurants: list[dict],
    user_lat: Optional[float],
    user_lng: Optional[float],
) -> tuple[list[Restaurant], str]:
    """
    Claude 응답 JSON 파싱 후 Restaurant 모델 리스트 반환.
    파싱 실패 시 ValueError 발생.
    """
    data = json.loads(raw)
    picks = data.get("picks", [])
    reasons = data.get("reasons", [])
    ai_message = data.get("message", "")

    if len(picks) != 3:
        raise ValueError(f"Expected 3 picks, got {len(picks)}")

    # source_restaurants를 id로 인덱싱
    by_id = {r["id"]: r for r in source_restaurants}

    recommendations = []
    for pick_id, reason in zip(picks, reasons):
        r = by_id.get(pick_id)
        if r is None:
            # fallback: RESTAURANTS 전체에서 찾기
            all_by_id = {x["id"]: x for x in RESTAURANTS}
            r = all_by_id.get(pick_id)
        if r is None:
            raise ValueError(f"Invalid restaurant id: {pick_id}")

        # 거리 계산
        dist_km = r.get("distance_km")
        wm = r.get("walk_minutes")
        if dist_km is None and user_lat is not None and user_lng is not None:
            r_lat = r.get("lat")
            r_lng = r.get("lng")
            if r_lat and r_lng:
                dist_km = round(haversine(user_lat, user_lng, r_lat, r_lng), 2)
                wm = walk_minutes(dist_km)

        recommendations.append(
            Restaurant(
                id=r["id"],
                name=r["name"],
                korean_name=r["korean_name"],
                category=r["category"],
                location=r["location"],
                address=r["address"],
                rating=r["rating"],
                price_range=r["price_range"],
                english_menu=r["english_menu"],
                description=r["description"],
                hours=r["hours"],
                tags=r.get("tags", []),
                reason=reason,
                distance_km=dist_km,
                walk_minutes=wm,
                google_maps_url=make_google_maps_url(r),
            )
        )

    return recommendations, ai_message


# ─── API 엔드포인트 ──────────────────────────────────────────────────────

@app.post("/recommend", response_model=RecommendResponse)
async def recommend_restaurants(req: RecommendRequest):
    start_time = time.time()

    # 세션 처리
    session_id, _ = get_or_create_session(req.session_id)

    # GPS 기반 필터링 vs 텍스트 기반
    search_radius_km = None
    if req.lat is not None and req.lng is not None:
        candidate_restaurants, search_radius_km = auto_expand_radius(
            RESTAURANTS, req.lat, req.lng
        )
    else:
        # 기존 location 텍스트 기반 (하위 호환)
        location_lower = req.location.lower()
        if location_lower == "seoul" or not location_lower:
            candidate_restaurants = RESTAURANTS
        else:
            candidate_restaurants = [
                r for r in RESTAURANTS
                if location_lower in r.get("location", "").lower()
                or location_lower in r.get("address", "").lower()
            ]
            if not candidate_restaurants:
                candidate_restaurants = RESTAURANTS

    restaurant_list_text = build_restaurant_text(candidate_restaurants)
    food_pref = req.food_preference or "any good local restaurant"

    gps_context = ""
    if req.lat is not None and search_radius_km is not None:
        if search_radius_km <= 5.0:
            gps_context = f"\nThe tourist is currently at GPS coordinates ({req.lat:.4f}, {req.lng:.4f}). Restaurants are sorted by walking distance."
        else:
            gps_context = "\nNo restaurants found within 5km. Showing closest available options."

    prompt = f"""You are a friendly Korean local guide helping a foreign tourist find great restaurants in Seoul.{gps_context}

The tourist says: "{food_pref}"

Available restaurants (indexed by ID):
{restaurant_list_text}

Select the 3 BEST matching restaurants for this tourist based on their preference.
Respond ONLY with valid JSON in this exact format (no markdown, no explanation outside JSON):
{{
  "picks": [0, 5, 12],
  "reasons": [
    "Reason why this restaurant matches",
    "Reason why this restaurant matches",
    "Reason why this restaurant matches"
  ],
  "message": "A warm, friendly 1-2 sentence message to the tourist about your picks"
}}

Rules:
- picks must be exactly 3 IDs from the list above (use the ID number in [ID:X])
- reasons must be specific and helpful
- message should be encouraging and mention what to expect"""

    # Claude Haiku 호출 (1회 재시도)
    raw = None
    for attempt in range(2):
        try:
            response = client.messages.create(
                model=HAIKU_MODEL,
                max_tokens=MAX_TOKENS_HAIKU,
                messages=[{"role": "user", "content": prompt}],
                timeout=8.0,
            )
            raw = response.content[0].text.strip()
            recommendations, ai_message = parse_ai_recommendations(
                raw, candidate_restaurants, req.lat, req.lng
            )
            break
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            if attempt == 1:
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": {
                            "code": "AI_PARSE_ERROR",
                            "message": f"AI returned invalid response after 2 attempts: {str(e)}",
                            "fallback": "Please try again with a different preference.",
                        }
                    },
                )

    # 세션에 저장
    add_message(session_id, "assistant", f"Recommended: {[r.id for r in recommendations]}")

    elapsed = round(time.time() - start_time, 3)

    return RecommendResponse(
        recommendations=recommendations,
        ai_message=ai_message,
        session_id=session_id,
        search_radius_km=search_radius_km,
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    # 세션 처리
    session_id, is_new = get_or_create_session(req.session_id)

    # 기존 히스토리 조회 (최근 10턴만 Claude에 전달)
    history = get_history(session_id)
    recent_history = history[-10:] if len(history) > 10 else history

    # 사용자 메시지 저장
    add_message(session_id, "user", req.message)

    # 식당 컨텍스트 준비 (간략 버전)
    restaurant_context = "\n".join(
        f"[ID:{r['id']}] {r['name']} | {r['category']} | {r['location']} | "
        f"Rating: {r['rating']} | Price: {r['price_range']} | Tags: {', '.join(r.get('tags', []))}"
        for r in RESTAURANTS
    )

    gps_info = ""
    if req.lat is not None and req.lng is not None:
        gps_info = f"\nTourist's current GPS: ({req.lat:.4f}, {req.lng:.4f})"

    system_prompt = f"""You are a friendly Korean local guide helping foreign tourists find great restaurants and experiences in Seoul.
Keep responses concise, helpful, and warm. Speak in English.{gps_info}

Available restaurants for recommendation:
{restaurant_context}

If the tourist asks for restaurant recommendations, respond with a JSON block in this format embedded in your text:
<recommendations>
{{"ids": [0, 5, 12], "reasons": ["reason1", "reason2", "reason3"]}}
</recommendations>

If it's a general question or conversation, just answer normally without the JSON block.
Guidelines:
- Be enthusiastic about Korean food culture
- Mention practical tips (cash, reservations, etc.) when relevant
- If recommending restaurants, pick the 3 best matches from the list above"""

    # Claude Sonnet 호출
    messages_for_api = []
    for msg in recent_history:
        role = msg["role"]
        content = msg["content"]
        # assistant 메시지 중 시스템 내부 기록은 스킵
        if role == "assistant" and content.startswith("Recommended:"):
            continue
        messages_for_api.append({"role": role, "content": content})

    # 현재 사용자 메시지 추가
    messages_for_api.append({"role": "user", "content": req.message})

    try:
        response = client.messages.create(
            model=SONNET_MODEL,
            max_tokens=MAX_TOKENS_SONNET,
            system=system_prompt,
            messages=messages_for_api,
            timeout=8.0,
        )
        reply_text = response.content[0].text.strip()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": {
                    "code": "AI_ERROR",
                    "message": "Failed to get response from AI.",
                    "fallback": "Please try again.",
                }
            },
        )

    # 추천 JSON 파싱 (있는 경우)
    inline_recommendations = None
    if "<recommendations>" in reply_text and "</recommendations>" in reply_text:
        try:
            start = reply_text.index("<recommendations>") + len("<recommendations>")
            end = reply_text.index("</recommendations>")
            rec_json = json.loads(reply_text[start:end].strip())
            ids = rec_json.get("ids", [])
            reasons = rec_json.get("reasons", [])
            by_id = {r["id"]: r for r in RESTAURANTS}

            inline_recommendations = []
            for rid, reason in zip(ids, reasons):
                r = by_id.get(rid)
                if not r:
                    continue
                dist_km = None
                wm = None
                if req.lat is not None and req.lng is not None:
                    r_lat = r.get("lat")
                    r_lng = r.get("lng")
                    if r_lat and r_lng:
                        dist_km = round(haversine(req.lat, req.lng, r_lat, r_lng), 2)
                        wm = walk_minutes(dist_km)
                inline_recommendations.append(
                    Restaurant(
                        id=r["id"],
                        name=r["name"],
                        korean_name=r["korean_name"],
                        category=r["category"],
                        location=r["location"],
                        address=r["address"],
                        rating=r["rating"],
                        price_range=r["price_range"],
                        english_menu=r["english_menu"],
                        description=r["description"],
                        hours=r["hours"],
                        tags=r.get("tags", []),
                        reason=reason,
                        distance_km=dist_km,
                        walk_minutes=wm,
                        google_maps_url=make_google_maps_url(r),
                    )
                )

            # reply_text에서 JSON 블록 제거
            reply_text = (
                reply_text[: reply_text.index("<recommendations>")]
                + reply_text[reply_text.index("</recommendations>") + len("</recommendations>"):]
            ).strip()
        except (json.JSONDecodeError, ValueError):
            inline_recommendations = None

    # AI 응답 저장
    add_message(session_id, "assistant", reply_text)

    return ChatResponse(
        reply=reply_text,
        recommendations=inline_recommendations,
        session_id=session_id,
    )


@app.get("/restaurant/{restaurant_id}", response_model=RestaurantDetail)
async def get_restaurant(restaurant_id: int):
    # id 필드 기반 검색 (인덱스 기반 접근은 id와 배열 순서가 다를 때 잘못된 데이터 반환)
    r = next((x for x in RESTAURANTS if x.get("id") == restaurant_id), None)
    if r is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "NOT_FOUND",
                    "message": f"Restaurant with id {restaurant_id} not found.",
                    "fallback": "Check the id from the /recommend response.",
                }
            },
        )
    maps_url = make_google_maps_url(r)

    return RestaurantDetail(
        id=r["id"],
        name=r["name"],
        korean_name=r["korean_name"],
        category=r["category"],
        tags=r.get("tags", []),
        location=r["location"],
        address=r["address"],
        lat=r.get("lat"),
        lng=r.get("lng"),
        rating=r["rating"],
        price_range=r["price_range"],
        english_menu=r["english_menu"],
        description=r["description"],
        hours=r["hours"],
        signature_dishes=r.get("signature_dishes", []),
        atmosphere_tags=r.get("atmosphere_tags", []),
        pros_cons=r.get("pros_cons", {"pros": "", "cons": ""}),
        google_maps_url=maps_url,
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "restaurants_loaded": len(RESTAURANTS),
        "active_sessions": active_session_count(),
    }


# 정적 파일 서빙 — 마지막에 마운트 (API 라우트보다 뒤에 와야 함)
app.mount("/", StaticFiles(directory=str(BASE_DIR / "static"), html=True), name="static")
