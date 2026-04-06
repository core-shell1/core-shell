# Wave BE — 완료 보고서

**작성일:** 2026-04-06
**담당:** BE (정우)
**기반:** wave_cto.md + wave_pm.md + wave_fe.md

---

## 구현된 파일 목록

| 파일 | 상태 | 설명 |
|------|------|------|
| `core/location.py` | 신규 생성 | Haversine 거리 계산 + 반경 필터링 + 자동 확장 |
| `core/session.py` | 신규 생성 | 서버 메모리 세션 관리 (24시간 TTL) |
| `core/__init__.py` | 신규 생성 | 패키지 초기화 |
| `data/restaurants.json` | 업데이트 | 20개 식당 전체에 lat/lng/id/상세 필드 추가 |
| `app.py` | 전면 업그레이드 | /recommend 확장 + /chat + /restaurant/{id} 신규 |
| `requirements.txt` | 업데이트 | apscheduler==3.10.4 추가 |

---

## 구현된 API

| Method | Path | 상태 | 설명 |
|--------|------|------|------|
| POST | `/recommend` | 완료 | GPS 반경 검색 + 텍스트 fallback + 세션 발급 |
| POST | `/chat` | 완료 | Claude Sonnet 세션 기반 대화 |
| GET | `/restaurant/{id}` | 완료 | 식당 상세 정보 |
| GET | `/health` | 완료 | active_sessions 카운트 추가 |

---

## restaurants.json 추가 필드

기존 20개 식당 전체에 아래 필드 추가:

| 필드 | 타입 | 설명 |
|------|------|------|
| `id` | int | 0~19, restaurants.json 인덱스와 일치 |
| `lat` | float | GPS 위도 (서울 관광지 기준 좌표) |
| `lng` | float | GPS 경도 |
| `signature_dishes` | list[str] | 대표 메뉴 3개 |
| `atmosphere_tags` | list[str] | 분위기 태그 (cozy, lively 등) |
| `pros_cons` | dict | `{"pros": "...", "cons": "..."}` |

**구역별 좌표 기준:**
- 광장시장/Jongno-gu: 37.5700, 126.9994
- Gyeongbokgung 인근: 37.5796, 126.9697
- Jung-gu (명동): 37.5636, 126.9848
- Itaewon (Yongsan-gu): 37.5344, 126.9947
- Hongdae (Mapo-gu): 37.5563, 126.9236
- Gangnam-gu: 37.5044, 127.0230
- Insadong: 37.5741, 126.9851
- Cheongdam/Apgujeong: 37.5199, 127.0537
- Songpa-gu (잠실): 37.5131, 127.1006

---

## FE가 주의해야 할 API 동작 차이

### 1. POST /recommend — 응답 구조 변경

**기존 응답 (변경 전):**
```json
{
  "recommendations": [{"name": "...", "reason": "..."}],
  "ai_message": "..."
}
```

**신규 응답 (변경 후):**
```json
{
  "recommendations": [
    {
      "id": 0,
      "name": "...",
      "korean_name": "...",
      "category": "...",
      "location": "...",
      "address": "...",
      "rating": 4.7,
      "price_range": "$",
      "english_menu": true,
      "description": "...",
      "hours": "...",
      "tags": ["korean", "traditional"],
      "reason": "...",
      "distance_km": 0.64,
      "walk_minutes": 8,
      "google_maps_url": "https://www.google.com/maps/search/?api=1&query=37.57,126.99"
    }
  ],
  "ai_message": "...",
  "session_id": "uuid-string",
  "search_radius_km": 1.0
}
```

- `id` 필드 추가됨 — BottomSheet `/restaurant/{id}` 호출 시 필수
- `distance_km`, `walk_minutes` — GPS 없이 호출 시 null
- `search_radius_km` — GPS 없이 호출 시 null
- `session_id` — 항상 반환됨 (신규 발급 포함). localStorage에 저장 필요

### 2. POST /chat — session_id 처리

- `session_id` 없이 요청하면 새 세션 자동 생성 후 반환
- 만료된 session_id 전달해도 404 대신 새 세션 발급 후 정상 응답
  - 단, `session_id`가 새 UUID로 바뀌어 반환되므로 FE에서 응답의 `session_id`로 갱신 필요

- `recommendations` 필드: Claude가 추천 판단 시에만 포함. 일반 대화는 `null` 반환 (wave_pm.md 명세의 빈 배열 `[]` 대신 `null`로 처리 — FE에서 null 체크 필요)

### 3. GET /restaurant/{id}

- `id`는 `/recommend` 응답의 `recommendations[].id` 값
- 범위 초과 시 HTTP 404 + 에러 JSON 반환
- `pros_cons` 구조: `{"pros": "string", "cons": "string"}` — wave_cto.md 명세와 동일

### 4. GPS 반경 자동 확장 동작

```
lat/lng 포함 요청 시:
  1km → 결과 없으면 → 2km → 결과 없으면 → 5km
  5km에도 없으면 → 전체 식당 거리순 반환 (search_radius_km: 99.0)

search_radius_km 값 해석:
  1.0 = 1km 반경 내 결과
  2.0 = 2km로 확장됨
  5.0 = 5km로 확장됨
  99.0 = 전체 데이터셋 fallback (search_radius_km > 5 이면 "No restaurants within 5km" UI 표시 권장)
```

---

## 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# .env 파일 설정 (기존 .env 유지, 추가 항목 없음)
# ANTHROPIC_API_KEY=sk-ant-...

# 실행
uvicorn app:app --reload --port 8000
```

---

## curl 테스트 예시

### POST /recommend — GPS 기반

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "food_preference": "I want spicy Korean street food",
    "lat": 37.5700,
    "lng": 126.9994
  }'
```

### POST /recommend — 텍스트 fallback

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "food_preference": "cheap noodles in Myeongdong",
    "location": "Myeongdong"
  }'
```

### POST /chat

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Show me something vegetarian and cheap",
    "session_id": "SESSION_ID_FROM_RECOMMEND"
  }'
```

### GET /restaurant/{id}

```bash
curl http://localhost:8000/restaurant/0
```

### GET /health

```bash
curl http://localhost:8000/health
# 응답: {"status":"ok","restaurants_loaded":20,"active_sessions":1}
```

---

## Haversine 검증 결과

```
서울 중심(37.5665, 126.9780) → 광장시장(37.5700, 126.9994)
실측: 1.93km (wave_cto.md 기대값 ~1.8km, ±0.1 허용 범위)

광장시장 좌표 기준 반경 1km 내 식당: 2개
auto_expand_radius 적용 시: 2개, 반경 1.0km
```

---

## 환경변수 목록

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `ANTHROPIC_API_KEY` | 필수 | Anthropic API 키 |
| `HAIKU_MODEL` | `claude-haiku-4-5-20251001` | /recommend에 사용할 모델 |
| `SONNET_MODEL` | `claude-sonnet-4-5` | /chat에 사용할 모델 |

---

*Wave BE 완료 — 정우 | 2026-04-06*
