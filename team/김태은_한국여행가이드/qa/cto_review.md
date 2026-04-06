# CTO 코드 리뷰 — 한국 로컬가이드 (Korea Local Guide)

**작성일:** 2026-04-06
**리뷰어:** CTO (Wave 4)
**리뷰 대상:** app.py, core/location.py, core/session.py, static/index.html
**기준:** wave_cto.md (설계 명세)

---

## 1. 아키텍처 준수 여부

### 1-1. 설계 대비 구현 상태

| 설계 항목 | 준수 여부 | 비고 |
|---|---|---|
| POST /recommend (GPS + 텍스트 fallback) | PASS | 설계 그대로 구현. 하위 호환 유지. |
| POST /chat (Sonnet, 세션 히스토리) | PASS | recent_history [-10:] 슬라이싱 확인됨. |
| GET /restaurant/{id} | PASS | 404 처리 포함. |
| GET /health (세션 카운트 포함) | PASS | active_session_count() 연동. |
| location.py 분리 (Haversine) | PASS | core/location.py 독립 모듈로 분리됨. |
| session.py 분리 | PASS | core/session.py 독립 모듈. |
| APScheduler 1시간 주기 세션 정리 | PASS | cleanup_expired() 연결됨. |
| Haiku (/recommend) / Sonnet (/chat) 모델 분리 | PASS | 환경변수로 관리, 하드코딩 없음. |
| max_tokens Haiku 512 / Sonnet 1024 | PASS | 상수로 명시됨. |
| 에러 응답 형식 통일 (code/message/fallback) | PASS | 3개 엔드포인트 모두 통일됨. |
| StaticFiles 마지막 마운트 | PASS | API 라우트 이후 mount 확인됨. |

### 1-2. 설계 대비 미구현 또는 차이점

| 항목 | 설계 명세 | 실제 구현 | 영향 |
|---|---|---|---|
| X-Response-Time 헤더 | Rule 1 — 디버깅용 응답 헤더 추가 명시 | 미구현 (elapsed 변수는 있으나 헤더 미포함) | LOW — 운영 디버깅에만 영향 |
| Claude API timeout=8.0 | Rule 1 명시 | client.messages.create()에 timeout 파라미터 없음 | MEDIUM — 느린 응답 시 요청 hang 가능 |
| SessionData에 last_recommended, last_location 필드 | 설계 명세 데이터 구조 | 세션에 저장 안 됨. add_message()로 텍스트 기록만 | LOW — MVP 기능 영향 없음 |
| settings.py 분리 | 설계 명세 폴더 구조 | 환경변수 app.py 상단에서 직접 처리 | LOW — 현재는 문제 없음 |

---

## 2. 보안 리뷰

### 2-1. API Key 노출

**결과: PASS**

- `ANTHROPIC_API_KEY`는 `os.getenv()`로만 참조.
- FE(index.html)에서 직접 Anthropic API 호출 없음.
- 키가 응답 본문에 포함되는 경로 없음.

### 2-2. 입력값 검증 — lat/lng 범위 체크

**결과: FAIL (CRITICAL)**

`app.py`의 `/recommend`, `/chat` 엔드포인트 모두 `lat`, `lng` 파라미터를 수신하지만, 서울 좌표 범위 검증이 없다.

- 설계 Rule 6에 `GPS_OUT_OF_RANGE` 에러 코드가 명시되어 있으나 미구현.
- 현재 임의의 위도/경도 값(예: lat=0.0, lng=0.0)을 전달해도 Haversine 계산이 그대로 실행됨.
- Haversine 자체는 안전하나, 의도치 않은 좌표로 엉뚱한 결과가 반환될 수 있음.

서울 유효 범위: `lat 37.4 ~ 37.7`, `lng 126.8 ~ 127.2`

검증 코드 없음 — `/recommend` 약 222~226행, `/chat` 약 334~335행 모두 해당.

### 2-3. XSS 방지 (FE)

**결과: PASS (부분) + FAIL (2건 발견)**

`escHtml()` 함수가 구현되어 있으며 대부분의 출력에 적용됨:
- `r.name`, `r.korean_name`, `r.description`, `r.hours`, `r.reason`(sheet), `r.address`(sheet), 채팅 버블 등 → 모두 `escHtml()` 처리됨.

**미처리 항목 2건:**

1. `buildCardHTML()` 내 `card-address` (약 1926행):
   ```javascript
   // 현재 — XSS 취약
   ? `<span class="card-address">${r.address}</span>`
   ```
   `r.address`에 `escHtml()` 미적용. 카드 목록 렌더링 시 노출됨.

2. `buildCardHTML()` 내 `card-reason` (약 1930행):
   ```javascript
   // 현재 — XSS 취약
   ? `<div class="card-reason">${r.reason}</div>`
   ```
   `r.reason`은 Claude가 생성한 텍스트이나, AI 응답이 항상 안전하다고 보장할 수 없음.
   (sheet의 `sheet-reason-box`는 `escHtml()` 처리되어 있으나 카드의 reason만 누락됨)

**수정 방법:**
```javascript
? `<span class="card-address">${escHtml(r.address)}</span>`
? `<div class="card-reason">${escHtml(r.reason)}</div>`
```

---

## 3. 성능 리뷰

### 3-1. Claude API 호출 최적화

**결과: PASS**

- `/recommend`: 필터된 식당만 프롬프트에 포함 (`candidate_restaurants`). 전체 목록을 항상 넘기지 않음. 설계 의도대로.
- `/chat`: 전체 식당을 system prompt에 포함하나, 간략 버전(id/name/category/location/rating/price/tags)으로 압축. 상세 description 제외됨.
- Haiku 512 토큰, Sonnet 1024 토큰 — 적정 수준.
- 재시도 로직: `/recommend`는 최대 2회. 무한 루프 없음.

**주의 사항 (MEDIUM):**
`/chat`의 system prompt에 전체 식당 목록을 매 요청마다 포함한다. 식당 수가 20개에서 100개로 늘어날 경우 system prompt 토큰이 크게 증가한다. 현재는 허용 범위이나, 100개 이상으로 확장 시 카테고리 기반 사전 필터링 도입 검토 필요.

### 3-2. 메모리 세션 크기 제한

**결과: PASS**

- `MAX_HISTORY = 20`: 세션당 메시지 최대 20개, FIFO로 오래된 것 제거됨. (`session.py` 57~58행)
- `SESSION_TTL = 86400`: 24시간 만료.
- `cleanup_expired()`: APScheduler 1시간 주기 실행.
- `active_session_count()`: `/health`로 모니터링 가능.

세션 메모리 한도 계산:
- 메시지 1개 평균 약 200자 = 200 bytes
- 세션 1개 = 20 메시지 x 200 bytes = ~4KB
- 256MB / 4KB = 약 64,000 세션 동시 수용 가능

Fly.io 무료 티어(256MB) 기준 충분함.

**주의 사항 (LOW):**
`SESSIONS` dict 자체의 최대 세션 수 제한 코드 없음. 비정상적인 세션 폭증 시 메모리 한계를 초과할 수 있으나, TTL 정리 + 트래픽 규모 감안 시 MVP에서는 허용 가능.

---

## 4. 코드 품질

### 4-1. 에러 핸들링 일관성

**결과: PASS (부분 주의)**

에러 응답 형식은 세 엔드포인트 모두 `{"error": {"code": ..., "message": ..., "fallback": ...}}`로 통일됨. Rule 6 준수.

**주의 (MEDIUM):**
`/chat`의 Claude API 호출 에러 핸들링이 너무 포괄적:
```python
except Exception as e:
    raise HTTPException(status_code=500, ...)
```
`Exception`을 모두 잡으면 네트워크 오류, 인증 오류, 레이트 리밋 오류가 동일한 500으로 처리됨. Anthropic SDK는 `anthropic.RateLimitError`, `anthropic.AuthenticationError` 등 구체적인 예외를 제공한다. 최소한 레이트 리밋(429)과 인증 오류(401)는 별도 처리 권장.

`/recommend`는 `json.JSONDecodeError, ValueError, KeyError`를 명시적으로 잡음 — 더 나은 패턴.

### 4-2. 중복 코드

**결과: MEDIUM**

`/recommend`와 `/chat` 양쪽에서 거의 동일한 거리 계산 블록이 중복됨:

`app.py` 178~185행 (`/recommend`):
```python
if dist_km is None and user_lat is not None and user_lng is not None:
    r_lat = r.get("lat")
    r_lng = r.get("lng")
    if r_lat and r_lng:
        dist_km = round(haversine(user_lat, user_lng, r_lat, r_lng), 2)
        wm = walk_minutes(dist_km)
```

`app.py` 404~410행 (`/chat`):
```python
if req.lat is not None and req.lng is not None:
    r_lat = r.get("lat")
    r_lng = r.get("lng")
    if r_lat and r_lng:
        dist_km = round(haversine(req.lat, req.lng, r_lat, r_lng), 2)
        wm = walk_minutes(dist_km)
```

동일한 패턴. 헬퍼 함수로 추출 권장. 예: `calc_distance(r, user_lat, user_lng) -> tuple[Optional[float], Optional[int]]`

Restaurant 모델 생성 블록(`/recommend` 187~205행, `/chat` 412~430행)도 거의 동일. `build_restaurant_model()` 헬퍼로 추출 가능.

### 4-3. 타입 힌트 누락

**결과: PASS (대체로 양호)**

- `location.py`: 모든 함수에 타입 힌트 완비.
- `session.py`: 모든 함수에 타입 힌트 완비.
- `app.py` 헬퍼 함수들: `make_google_maps_url`, `build_restaurant_text`, `parse_ai_recommendations` 모두 힌트 있음.

**경미한 누락:**
- `app.py` 37행: `client = anthropic.Anthropic(...)` — 변수 타입 힌트 없으나 모듈 레벨 변수이므로 허용 가능.
- `app.py` 40행: `RESTAURANTS: list[dict] = json.load(f)` — `list[dict]`보다 `list[dict[str, Any]]`이 더 정확하나 큰 문제 없음.

### 4-4. GPS 좌표 서버 저장 금지 규칙 준수 여부

**결과: PASS**

- `/recommend`: `req.lat`, `req.lng`는 함수 스코프 내에서만 사용 후 폐기. 세션에 GPS 좌표 저장 없음.
- `/chat`: `req.lat`, `req.lng`는 system prompt 생성 및 거리 계산에만 사용. 세션 저장 없음.
- `session.py`: `SESSIONS` dict에 GPS 관련 필드 없음.
- 설계 명세의 `last_location` 필드는 미구현 — GPS 저장 금지 관점에서는 오히려 더 안전함.
- 로그에 GPS 출력 없음.

Rule 2 완전 준수.

---

## 5. 즉시 수정 필요한 것 (CRITICAL)

### CRITICAL-1: XSS 취약점 — card-address, card-reason 미이스케이프

**파일:** `static/index.html`, 약 1926행, 1930행

`buildCardHTML()` 함수에서 `r.address`와 `r.reason` 값이 `escHtml()` 처리 없이 innerHTML에 삽입됨.

현재 코드:
```javascript
const address = r.address
  ? `<span class="card-address">${r.address}</span>`
  : '';

const reason = r.reason
  ? `<div class="card-reason">${r.reason}</div>`
  : '';
```

수정 방법:
```javascript
const address = r.address
  ? `<span class="card-address">${escHtml(r.address)}</span>`
  : '';

const reason = r.reason
  ? `<div class="card-reason">${escHtml(r.reason)}</div>`
  : '';
```

sheet의 동일 필드(`sheet-address-text`, `sheet-reason-box`)는 이미 `escHtml()` 처리됨 — 카드 렌더링만 누락된 상태.

### CRITICAL-2: Claude API 타임아웃 미설정

**파일:** `app.py`, 278~281행 (`/recommend`), 368~373행 (`/chat`)

설계 Rule 1에 "Claude API 호출 타임아웃: timeout=8.0" 명시. 현재 `client.messages.create()` 호출에 타임아웃 없음.

Anthropic Python SDK에서 타임아웃은 다음과 같이 설정:
```python
response = client.messages.create(
    model=HAIKU_MODEL,
    max_tokens=MAX_TOKENS_HAIKU,
    messages=[...],
    timeout=8.0,  # 추가 필요
)
```

타임아웃 미설정 시 API 응답이 지연될 때 요청이 무한 대기하며 서버 스레드를 점유한다. 응답 3초 이내 보장 불가.

---

## 6. 권장 개선사항

### HIGH

**H-1: lat/lng 좌표 범위 검증 추가**

`/recommend`와 `/chat` 모두 lat/lng 수신 시 서울 범위 밖이면 즉시 400 반환.

```python
SEOUL_LAT_RANGE = (37.4, 37.7)
SEOUL_LNG_RANGE = (126.8, 127.2)

def validate_seoul_coords(lat: float, lng: float) -> bool:
    return (SEOUL_LAT_RANGE[0] <= lat <= SEOUL_LAT_RANGE[1] and
            SEOUL_LNG_RANGE[0] <= lng <= SEOUL_LNG_RANGE[1])
```

설계 Rule 6의 `GPS_OUT_OF_RANGE` 에러 코드가 이미 명시되어 있음 — 구현만 누락된 상태.

**H-2: /chat의 Exception 포괄 처리 세분화**

```python
except anthropic.RateLimitError:
    raise HTTPException(status_code=429, detail={"error": {"code": "RATE_LIMIT", ...}})
except anthropic.AuthenticationError:
    raise HTTPException(status_code=500, detail={"error": {"code": "AI_AUTH_ERROR", ...}})
except Exception as e:
    raise HTTPException(status_code=500, detail={"error": {"code": "AI_ERROR", ...}})
```

### MEDIUM

**M-1: 거리 계산 + Restaurant 모델 생성 중복 제거**

`/recommend`와 `/chat` 양쪽에 동일한 패턴 중복. 헬퍼 함수 2개 추출:
- `calc_distance(r: dict, user_lat: Optional[float], user_lng: Optional[float]) -> tuple[Optional[float], Optional[int]]`
- `build_restaurant_obj(r: dict, reason: str, user_lat, user_lng) -> Restaurant`

**M-2: /chat system prompt 식당 목록 크기 관리**

현재: 전체 식당을 매 요청마다 system prompt에 포함.
100개 확장 시 system prompt 토큰이 약 2~3배 증가.

개선 방향: `/chat` 요청에 GPS가 있을 경우 Haversine으로 5km 내 식당만 system prompt에 포함. GPS 없으면 전체 유지. 현재 구조에서 `auto_expand_radius()`를 재활용하면 됨.

**M-3: X-Response-Time 응답 헤더 추가**

설계 Rule 1에 명시됨. `elapsed` 변수가 이미 계산되어 있으나 헤더에 포함되지 않음.

```python
from fastapi import Response

@app.post("/recommend")
async def recommend_restaurants(req: RecommendRequest, response: Response):
    ...
    response.headers["X-Response-Time"] = str(elapsed)
```

### LOW

**L-1: /restaurant/{id} 조회 방식 개선**

현재 `RESTAURANTS[restaurant_id]`는 인덱스 기반 접근. `id` 필드 값과 배열 인덱스가 일치한다고 가정.

만약 restaurants.json에서 id 값이 배열 인덱스와 다를 경우 잘못된 식당 반환. 방어적 코드:
```python
r = next((x for x in RESTAURANTS if x["id"] == restaurant_id), None)
if r is None:
    raise HTTPException(status_code=404, ...)
```

단, 현재 데이터셋에서 id == 인덱스가 보장된다면 LOW 우선순위 유지.

**L-2: SESSIONS dict 최대 크기 제한**

비정상 트래픽 대비 안전장치:
```python
MAX_SESSIONS = 10000

def create_session() -> str:
    if len(SESSIONS) >= MAX_SESSIONS:
        # 가장 오래된 세션 제거
        oldest = min(SESSIONS, key=lambda k: SESSIONS[k]["last_active"])
        del SESSIONS[oldest]
    ...
```

**L-3: settings.py 분리 (선택)**

현재 `HAIKU_MODEL`, `SONNET_MODEL`, `MAX_TOKENS_*` 상수가 `app.py` 상단에 있음. 설계 명세에서는 `settings.py` 분리를 명시했으나 기능 영향 없음. 코드 규모 커지면 분리 고려.

---

## 7. 종합 판정

| 항목 | 결과 |
|---|---|
| 아키텍처 준수 | PASS (미구현 2건은 LOW 영향) |
| GPS 좌표 서버 저장 금지 | PASS |
| 응답 3초 이내 구조 | CONDITIONAL PASS (API 타임아웃 설정 필요) |
| API Key 보안 | PASS |
| XSS 방지 | FAIL (2건 미처리 — 수정 필요) |
| 입력값 검증 | FAIL (좌표 범위 체크 미구현) |
| 에러 핸들링 | PASS (부분 개선 권장) |
| 세션 메모리 관리 | PASS |
| 타입 힌트 | PASS |
| 코드 중복 | MEDIUM (리팩토링 권장) |

**최종 판정: CONDITIONAL PASS**

CRITICAL 2건 수정 후 배포 가능. HIGH 2건은 배포 직후 이어서 처리 권장.

동작하는 구조는 설계 의도를 잘 따르고 있음. GPS 저장 금지, 모델 분리, 세션 관리, 에러 형식 통일 등 핵심 설계 규칙은 모두 준수됨.
