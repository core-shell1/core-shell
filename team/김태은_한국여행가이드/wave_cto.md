# CTO 분석 — 한국 로컬가이드 (Korea Local Guide)

**작성일:** 2026-04-06
**담당:** CTO (Wave 1)
**기반:** 기존 코드베이스 (app.py, requirements.txt, restaurants.json) + 요구사항명세서 v1.0

---

## 기술 스택 결정

| 항목 | 선택 | 이유 |
|------|------|------|
| 백엔드 프레임워크 | FastAPI (기존 유지) | 이미 동작 중. Pydantic 타입 검증, async 지원, OpenAPI 자동 생성. 변경 이유 없음. |
| AI 모델 | Claude Haiku (기본) + Sonnet (복잡 쿼리) | Haiku: 단순 GPS 추천 (빠름, 저비용). Sonnet: 세션 대화 맥락 처리. |
| 위치 처리 | Haversine 공식 (순수 Python) | 외부 서비스 의존 없음. GPS 좌표 수신 즉시 서버 메모리에서 계산 후 폐기. 지연 0ms. |
| 세션 관리 | 서버 메모리 (dict) | MVP 단계. 단일 인스턴스 배포이므로 Redis 불필요. 세션 24시간 TTL은 백그라운드 스케줄러로 처리. |
| 데이터 저장 | JSON 파일 (기존 유지, 스키마 확장) | 100개 이하 데이터셋은 JSON으로 충분. 배포 복잡도 최소화. DB 전환은 Phase 2. |
| 프론트엔드 | 정적 HTML + JavaScript PWA (기존 StaticFiles 유지) | 별도 빌드 파이프라인 없이 FastAPI StaticFiles로 서빙. Geolocation API는 브라우저 네이티브. |
| 배포 | Fly.io 또는 Render | 요구사항명세서 명시. 둘 다 무료 티어 존재, Python 지원. Fly.io 권장 (더 빠른 Cold Start). |
| 추가 의존성 | `apscheduler` (세션 만료) | 가벼운 스케줄러. 24시간 TTL 세션 정리용. |

---

## 아키텍처

```
[브라우저 PWA — static/index.html]
    |
    | 1. 진입 시 Geolocation API 호출 (브라우저 네이티브)
    | 2. GPS 허용 → lat/lng 획득 → POST /recommend
    |    GPS 거부 → 텍스트 입력 → POST /recommend (location_text 파라미터)
    |
    v
[FastAPI 서버 — app.py]
    |
    +-- POST /recommend  ←─ GPS 좌표 or 텍스트 위치 + 취향 입력
    |       |
    |       +-- [1] GPS 있을 때: Haversine 계산 → 반경 1km 필터링
    |       |         결과 0개 → 2km → 0개 → 5km (자동 확장)
    |       |   [2] 텍스트 있을 때: location 필드 기반 필터링 (기존 로직)
    |       |
    |       +-- 필터된 식당 목록 → Claude Haiku → 3개 선택 + 이유 + 거리(도보분)
    |       |
    |       +-- 응답 반환 (3초 이내 보장)
    |
    +-- POST /chat  ←─ session_id + message (세션 대화)
    |       |
    |       +-- session_id로 히스토리 조회 (메모리 dict)
    |       +-- 이전 대화 + 현재 메시지 → Claude Sonnet → 응답
    |       +-- 히스토리 업데이트 (최대 20턴 유지)
    |
    +-- GET /restaurant/{id}  ←─ 식당 상세 정보
    |       |
    |       +-- restaurants.json에서 id로 조회 → 상세 필드 반환
    |
    +-- GET /health
    |
    [메모리 세션 저장소]
    sessions: Dict[str, SessionData]
    - session_id (UUID)
    - created_at (datetime)
    - history: List[Message]  ← 최대 20턴
    - last_recommended: List[int]  ← 마지막 추천 식당 인덱스
    - last_location: Optional[LocationData]  ← 마지막 GPS 좌표

    [APScheduler 백그라운드]
    - 1시간마다 실행: 24시간 초과 세션 삭제

    [restaurants.json — 정적 파일]
    - 앱 시작 시 메모리 로드 (기존 유지)
    - lat/lng 필드 추가 (스키마 확장)
```

---

## API 설계

### POST /recommend

**기존 API 확장. GPS 파라미터 추가.**

Request:
```json
{
  "food_preference": "I want something cozy and spicy",
  "lat": 37.5665,
  "lng": 126.9780,
  "session_id": "uuid-string-optional",
  "radius_km": 1.0
}
```

- `food_preference`: 필수. 자연어 취향 입력.
- `lat`, `lng`: 선택. GPS 좌표. 둘 다 없으면 location_text 기반.
- `location`: 선택. 텍스트 위치 (GPS 거부 fallback). 기존 필드 유지.
- `session_id`: 선택. 있으면 세션 히스토리 컨텍스트 포함.
- `radius_km`: 선택. 기본값 1.0. 클라이언트에서 변경 불필요 (서버 자동 확장).

Response:
```json
{
  "recommendations": [
    {
      "id": 0,
      "name": "Gwangjang Market Bindaetteok",
      "korean_name": "광장시장 빈대떡",
      "category": "korean",
      "location": "Jongno-gu, Seoul",
      "address": "88 Changgyeonggung-ro, Jongno-gu, Seoul",
      "rating": 4.7,
      "price_range": "$",
      "english_menu": true,
      "description": "Famous traditional Korean mung bean pancakes...",
      "hours": "09:00 - 22:00",
      "distance_km": 0.8,
      "walk_minutes": 10,
      "reason": "Perfect for your spicy craving — bindaetteok is savory and bold.",
      "google_maps_url": "https://maps.google.com/?q=37.5700,126.9993",
      "tags": ["korean", "traditional", "street food"]
    }
  ],
  "ai_message": "Here are 3 spots within 10 minutes walk...",
  "search_radius_km": 1.0,
  "session_id": "uuid-string"
}
```

- `id`: 식당 인덱스. `/restaurant/{id}` 호출용.
- `distance_km`: Haversine으로 계산한 실제 직선 거리.
- `walk_minutes`: `distance_km / 0.08` (도보 속도 80m/분 기준, 반올림).
- `search_radius_km`: 실제 적용된 반경 (자동 확장 시 변경됨).
- `session_id`: 신규 생성 또는 기존 유지.
- `google_maps_url`: `https://maps.google.com/?q={lat},{lng}` 형식.

---

### POST /chat

**신규. 세션 기반 자연어 대화.**

Request:
```json
{
  "session_id": "uuid-string",
  "message": "Show me something cheaper and closer",
  "lat": 37.5665,
  "lng": 126.9780
}
```

- `session_id`: 필수. `/recommend` 응답에서 받은 값.
- `message`: 필수. 사용자 자연어 메시지.
- `lat`, `lng`: 선택. 현재 위치 갱신 시 포함.

Response:
```json
{
  "reply": "Got it! Here are some more affordable options nearby...",
  "recommendations": [...],
  "session_id": "uuid-string"
}
```

- `recommendations`: 없을 수도 있음 (단순 질문 응답 시 빈 배열).
- Claude Sonnet 사용 (맥락 유지 품질 중요).

---

### GET /restaurant/{id}

**신규. 식당 상세 정보.**

Request: Path parameter `id` (정수, restaurants.json 인덱스)

Response:
```json
{
  "id": 0,
  "name": "Gwangjang Market Bindaetteok",
  "korean_name": "광장시장 빈대떡",
  "category": "korean",
  "tags": ["korean", "traditional", "street food"],
  "location": "Jongno-gu, Seoul",
  "address": "88 Changgyeonggung-ro, Jongno-gu, Seoul",
  "lat": 37.5700,
  "lng": 126.9993,
  "rating": 4.7,
  "price_range": "$",
  "english_menu": true,
  "description": "Famous traditional Korean mung bean pancakes...",
  "hours": "09:00 - 22:00",
  "signature_dishes": ["Bindaetteok (Mung Bean Pancake)", "Mayak Gimbap", "Tteokbokki"],
  "atmosphere_tags": ["lively", "traditional", "good for solo"],
  "pros_cons": {
    "pros": "Authentic street food atmosphere, incredibly affordable, English menu available",
    "cons": "Can be crowded on weekends, cash only, limited seating"
  },
  "google_maps_url": "https://maps.google.com/?q=37.5700,126.9993"
}
```

- `signature_dishes`, `atmosphere_tags`, `pros_cons`: restaurants.json 스키마 확장으로 추가.
- id 범위 초과 시: HTTP 404

---

### GET /health

기존 유지. 세션 카운트 추가.

Response:
```json
{
  "status": "ok",
  "restaurants_loaded": 20,
  "active_sessions": 3
}
```

---

## 데이터 설계

### restaurants.json 스키마 확장

기존 필드 전부 유지. 아래 필드 추가:

```json
{
  "name": "Gwangjang Market Bindaetteok",
  "korean_name": "광장시장 빈대떡",
  "category": "korean",
  "tags": ["korean", "traditional", "street food", "pancake", "savory"],
  "location": "Jongno-gu, Seoul",
  "address": "88 Changgyeonggung-ro, Jongno-gu, Seoul",

  // --- 추가 필드 ---
  "lat": 37.5700,
  "lng": 126.9993,
  "signature_dishes": [
    "Bindaetteok (Mung Bean Pancake)",
    "Mayak Gimbap",
    "Nokdu Bindaetteok"
  ],
  "atmosphere_tags": ["lively", "traditional", "market", "good for solo"],
  "pros_cons": {
    "pros": "Authentic street food, very affordable, English menu available",
    "cons": "Crowded on weekends, mostly cash only"
  },
  // --- 기존 필드 ---
  "rating": 4.7,
  "price_range": "$",
  "english_menu": true,
  "description": "...",
  "hours": "09:00 - 22:00"
}
```

### 서울 주요 관광구역 좌표 매핑

GPS 좌표가 없는 식당의 기본 좌표. `lat/lng` 직접 입력 시 무시됨.

| 구역 (location 필드) | 기준 좌표 |
|---|---|
| Jongno-gu, Seoul | 37.5704, 126.9921 |
| Jung-gu, Seoul | 37.5641, 126.9979 |
| Mapo-gu, Seoul (Hongdae) | 37.5563, 126.9228 |
| Yongsan-gu, Seoul (Itaewon) | 37.5347, 126.9939 |
| Gangnam-gu, Seoul | 37.5172, 127.0473 |
| Insadong, Seoul | 37.5735, 126.9865 |
| Cheongdam-dong, Seoul | 37.5267, 127.0473 |
| Songpa-gu, Seoul | 37.5145, 127.1059 |
| Nationwide | 37.5665, 126.9780 (서울 중심) |

### 세션 데이터 구조

```python
# 서버 메모리 (모듈 레벨 dict)
sessions: Dict[str, SessionData] = {}

class Message(BaseModel):
    role: str           # "user" or "assistant"
    content: str

class LocationData(BaseModel):
    lat: float
    lng: float

class SessionData(BaseModel):
    session_id: str
    created_at: datetime
    last_active: datetime
    history: List[Message]          # 최대 20개 유지 (초과 시 앞에서 제거)
    last_recommended: List[int]     # 마지막 추천 식당 인덱스 목록
    last_location: Optional[LocationData]
```

---

## GPS 반경 검색 알고리즘

### Haversine 공식 구현

```python
import math

def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """두 GPS 좌표 간 거리를 킬로미터로 반환."""
    R = 6371.0  # 지구 반지름 (km)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))

def walk_minutes(distance_km: float) -> int:
    """거리를 도보 시간(분)으로 변환. 도보 속도 80m/분 기준."""
    return max(1, round(distance_km / 0.08))
```

### 반경 자동 확장 로직

```python
RADIUS_STEPS = [1.0, 2.0, 5.0]  # km

def filter_by_radius(
    restaurants: list,
    user_lat: float,
    user_lng: float,
) -> tuple[list, float]:
    """
    반경 내 식당 필터링. 결과 없으면 자동 확장.
    Returns: (필터된 식당 리스트 with distance, 실제 적용된 반경)
    """
    for radius in RADIUS_STEPS:
        nearby = []
        for r in restaurants:
            d = haversine_km(user_lat, user_lng, r["lat"], r["lng"])
            if d <= radius:
                nearby.append({**r, "distance_km": round(d, 2)})
        if nearby:
            # 거리 오름차순 정렬
            nearby.sort(key=lambda x: x["distance_km"])
            return nearby, radius

    # 5km에도 없으면 전체 반환 (서울 전체 커버)
    all_restaurants = [
        {**r, "distance_km": round(haversine_km(user_lat, user_lng, r["lat"], r["lng"]), 2)}
        for r in restaurants
    ]
    all_restaurants.sort(key=lambda x: x["distance_km"])
    return all_restaurants, 99.0
```

---

## Engineering Rules

이 프로젝트에서 반드시 지킬 규칙. FE/BE 모두 적용.

### Rule 1 — 응답 3초 이내 강제

- Claude API 호출 타임아웃: `timeout=8.0` (Haiku 기준 실제 응답 2초 이하)
- Haversine 계산은 동기 처리 (1ms 이하, async 불필요)
- `build_restaurant_list_text()`는 필터된 식당만 포함 (전체 아님)
  - GPS 없을 때: 전체 20개 → Haiku가 처리 가능한 범위
  - GPS 있을 때: 반경 내 식당만 → 프롬프트 크기 자동 축소
- `/recommend` 응답에 `X-Response-Time` 헤더 포함 (디버깅용)

### Rule 2 — GPS 좌표 서버 저장 금지

- `lat`, `lng` 파라미터는 함수 스코프 내에서만 사용
- 세션에는 마지막 위치를 `last_location`으로 저장 가능하나, 세션 만료 시 함께 삭제
- DB 도입 후에도 GPS 좌표 컬럼 생성 금지
- 로그에 GPS 좌표 출력 금지 (`print`, `logging` 모두)

### Rule 3 — 정적 파일 서빙은 FastAPI StaticFiles 유지

- `app.mount("/", StaticFiles(...))` 패턴 유지
- CDN 또는 별도 정적 서버 도입 금지 (배포 단순화)
- `static/` 폴더 내 파일만 수정. 빌드 도구 (Webpack, Vite 등) 도입 금지.

### Rule 4 — AI 모델 사용 기준

- `/recommend`: Claude Haiku 고정. 단순 선택 작업.
- `/chat`: Claude Sonnet 사용. 세션 히스토리 포함 복잡 쿼리.
- `max_tokens`: Haiku 512 (기존), Sonnet 1024
- 모델 이름 하드코딩 금지. `settings.py` 또는 환경변수로 관리.

### Rule 5 — 세션 히스토리 최대 20턴

- 20턴 초과 시 앞에서부터 제거 (FIFO)
- Claude API에 넘기는 히스토리: 최근 10턴만 (프롬프트 크기 관리)
- 24시간 TTL: `APScheduler`로 1시간마다 `last_active` 체크 후 만료 세션 삭제

### Rule 6 — 에러 응답 형식 통일

```json
{
  "error": {
    "code": "GPS_OUT_OF_RANGE",
    "message": "Coordinates appear to be outside Seoul area.",
    "fallback": "Try entering a neighborhood name instead."
  }
}
```

- HTTP 상태 코드: 400 (클라이언트 오류), 500 (서버/AI 오류)
- AI JSON 파싱 실패 시 → 재시도 1회 후 500 반환 (무한 루프 금지)

---

## 기술 리스크 & 대응

| 리스크 | 발생 조건 | 대응 방법 |
|---|---|---|
| GPS 권한 거부 | iOS/Android 브라우저에서 권한 거부 | `location` 텍스트 필드 fallback. UI에 "또는 동네 이름 입력" 안내. `/recommend`에서 `lat/lng` 없으면 기존 location 텍스트 로직 실행. |
| 반경 내 식당 0개 | 관광지 외 지역 진입 | `RADIUS_STEPS = [1.0, 2.0, 5.0]` 자동 확장. 5km에도 없으면 전체 데이터셋에서 가장 가까운 순으로 반환. |
| Claude API 레이트 리밋 초과 | 동시 요청 급증 | Anthropic Haiku 기준 TPM/RPM 제한 초과 시 HTTP 429 반환. 클라이언트에서 "서버가 바쁩니다, 잠시 후 재시도" 메시지 표시. MVP에서 별도 큐 미도입. |
| 세션 메모리 누수 | 서버 재시작 없이 장기 운영 | APScheduler 1시간 주기 만료 세션 정리. Fly.io 무료 티어 메모리 256MB 기준 세션 1개 약 2KB → 최대 10만 세션 저장 가능. |
| restaurants.json lat/lng 누락 | 데이터 입력 오류 | `lat`, `lng` 필드 없는 식당은 구역 기준 좌표로 대체 (위 매핑 테이블 사용). 로드 시 경고 로그 출력. |
| 서버 재시작 시 세션 소멸 | Fly.io 자동 재배포 | 세션 소멸 허용 (MVP 단계). 클라이언트는 session_id 로컬스토리지 저장 → 서버에 없으면 새 세션 생성. |
| Fly.io Cold Start | 트래픽 없는 기간 후 첫 요청 | `fly.toml`에 `min_machines_running = 1` 설정 (항상 1대 유지). 무료 티어 한도 내 운영 가능. |

---

## 의존성 추가

```
# requirements.txt 추가 항목
apscheduler==3.10.4   # 세션 만료 백그라운드 스케줄러
```

기존 4개 의존성 전부 유지. 최소 추가 원칙.

---

## 폴더 구조 (변경 후)

```
team/김태은_한국여행가이드/
├── app.py                  ← 기존 + /chat, /restaurant/{id} 추가
├── requirements.txt        ← apscheduler 추가
├── settings.py             ← 신규. 환경변수 + 모델명 관리
├── location.py             ← 신규. Haversine 함수 분리
├── session.py              ← 신규. 세션 관리 (dict + APScheduler)
├── data/
│   └── restaurants.json    ← lat/lng + 추가 필드 확장
└── static/
    └── index.html          ← 기존 + GPS 요청 JS 추가
```

`app.py`에 모든 것을 넣지 않는다. 위치 계산(`location.py`)과 세션 관리(`session.py`)는 분리.

---

## CDO에게 요청

1. **GPS 권한 요청 UX**: 브라우저 GPS 권한 팝업은 사용자가 직접 허용/거부한다. 허용 전 "왜 위치가 필요한지" 한 줄 안내 문구를 버튼 위에 표시해달라. (예: "Find restaurants near you — location used only for search")
2. **거리 표시 형식**: `distance_km`와 `walk_minutes` 중 UI에는 도보 분 단위만 표시 권장. (예: "10 min walk") km 수치는 보조 정보로.
3. **반경 자동 확장 피드백**: 1km → 2km로 확장됐을 때 "Expanded search to 2km" 같은 피드백을 UI에 표시해달라. 사용자가 왜 멀리 있는 식당이 나왔는지 혼란스럽지 않도록.
4. **세션 만료 UX**: 24시간 후 세션이 소멸했을 때 클라이언트 측 처리. "Your previous chat has expired. Starting fresh!" 정도의 안내.

---

## CPO에게 피드백

1. **데이터 20개 → 100개 확장 (MVP 포함)**: `lat/lng` 필드를 100개 식당에 수동 입력해야 한다. 구글 지도에서 좌표 확인 작업이 필요. 이 작업을 MVP 일정에 반드시 포함시켜야 한다. 예상 소요: 2~3시간.
2. **Claude Sonnet 비용**: `/chat` API는 Sonnet을 사용한다. Haiku 대비 약 10배 비용. 세션당 대화 3~5턴 기준 요청당 약 $0.01~0.02 수준. 500건 목표 기준 월 $5~10. MVP에서는 허용 가능하나 스케일 시 Haiku로 `/chat`도 전환하거나 캐싱 도입 필요.
3. **현재 영업 여부 필터 (F-001 요구사항)**: 요구사항에 "현재 영업 여부" 추천 기준이 포함되어 있다. 현재 `hours` 필드는 단순 문자열 (`"09:00 - 22:00"`)로 요일별 구분이 없다. Phase 1 MVP에서 실시간 영업 상태 판단은 불가. hours 파싱 로직 추가가 필요하면 일정 재검토 필요.

---

## 작성 메모

- GPS 처리: 브라우저 Geolocation API → 서버로 좌표 전달 → Haversine 계산 → 폐기. 서버 GPS 저장 없음.
- 세션: Redis 없이 서버 메모리로 충분. Fly.io 재시작 시 세션 소멸은 허용 (로그인 기반 서비스 아님).
- 기존 `/recommend` API는 하위 호환 유지. `lat/lng` 없으면 기존 `location` 텍스트 기반으로 동작.
- 목표: 기존 동작하는 코드를 최대한 유지하면서 GPS와 세션만 추가.
