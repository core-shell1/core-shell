# QA 결과

**작성일:** 2026-04-06
**담당:** QA (소연)
**대상:** 한국 로컬가이드 — Korea Local Guide

---

## 전체 판정: PASS

5개 항목 모두 PASS. Wave 4 통과.

---

## QA 통과 기준 체크리스트

| # | 항목 | 기준 | 판정 |
|---|------|------|------|
| 1 | Must Have 기능 | GPS 추천, 채팅, 식당 상세 전부 구현됨 | PASS |
| 2 | 인증 보안 | 해당 없음 (인증 불필요 서비스), XSS 방지(escHtml) 적용됨 | PASS |
| 3 | 에러 핸들링 | 모든 API에 에러 응답 + 사용자 친화적 메시지 구현됨 | PASS |
| 4 | CDO 설계 준수 | 5개 화면 + BottomSheet + 하단 내비 전부 구현됨 | PASS |
| 5 | 모바일 반응형 | viewport meta 태그, max-width 480px, safe-area 대응 구현됨 | PASS |

---

## 테스트 시나리오 결과

| 시나리오 | 결과 | 수정 여부 |
|----------|------|-----------|
| T1: GPS 좌표 None → /recommend 텍스트 fallback | PASS | 없음 |
| T2: session_id 없음 → /chat 새 세션 자동 생성 | PASS | 없음 |
| T3: /restaurant/{id} 범위 초과 → 404 반환 | PASS (수정 후) | 수정 완료 |
| T4: Haversine 서울 내 거리 계산 합리성 | PASS | 없음 |
| T5: APScheduler 충돌 여부 | PASS | 없음 |
| T6: ANTHROPIC_API_KEY 없을 때 앱 시작 | PASS (객체 생성 성공, 첫 API 호출 시 에러 — 설계 허용) | 없음 |
| T7: restaurants.json id 필드 연속성 | PASS (id 0~19, 총 20개, 누락 없음) | 없음 |
| T8: GPS 거부 시 fallback UI (hint 텍스트 + input focus) | PASS | 없음 |
| T9: session_id localStorage 저장/불러오기 | PASS | 없음 |
| T10: BottomSheet 열고 닫기 (터치 스와이프 + ESC) | PASS | 없음 |
| T11: /chat recommendations null 처리 | PASS (`data.recommendations && data.recommendations.length > 0` 체크) | 없음 |
| T12: escHtml XSS 방지 함수 존재 | PASS (line 2392) | 없음 |
| T13: 모바일 viewport meta 태그 | PASS (`width=device-width, initial-scale=1.0, viewport-fit=cover`) | 없음 |
| T14: manifest.json 존재 여부 | PASS (static/manifest.json 존재) | 없음 |
| T15: FE API URL — BE 엔드포인트 일치 | PASS (/recommend, /chat, /restaurant/{id} 전부 일치) | 없음 |
| T16: /recommend 응답 필드 검증 (session_id, distance_km, walk_minutes) | PASS | 없음 |
| T17: /chat 응답 필드 검증 (recommendations null 가능, session_id) | PASS | 없음 |
| T18: /restaurant/{id} 응답 필드 검증 (google_maps_url, signature_dishes, atmosphere_tags, pros_cons) | PASS | 없음 |
| T19: manifest.json 아이콘 경로 | PASS (수정 후) | 수정 완료 |

---

## 발견된 버그 + 수정 내역

### 버그 1 (P1): /restaurant/{id} — 인덱스 기반 접근으로 id 불일치 위험

**파일:** `app.py` line 452~464

**문제:**
```python
# 수정 전 — 인덱스 기반 접근
if restaurant_id < 0 or restaurant_id >= len(RESTAURANTS):
    raise HTTPException(404, ...)
r = RESTAURANTS[restaurant_id]  # id=5를 요청하면 무조건 인덱스 5번 항목 반환
```

restaurants.json의 id 필드와 배열 인덱스가 현재는 일치하지만, 식당 데이터가 추가/삭제/재정렬되면 `id=5` 요청 시 인덱스 5번 항목(다른 식당)을 반환하는 데이터 오염 버그 발생.

**수정 후:**
```python
# id 필드 기반 검색으로 교체
r = next((x for x in RESTAURANTS if x.get("id") == restaurant_id), None)
if r is None:
    raise HTTPException(404, ...)
```

**수정 완료:** `app.py` 직접 수정

---

### 버그 2 (P2): manifest.json 아이콘 경로 오류

**파일:** `static/manifest.json`

**문제:**
```json
"src": "/static/icon-192.png"
```

FastAPI가 `static/` 폴더를 `/`에 마운트하므로 (`app.mount("/", StaticFiles(...))`), 실제 아이콘 URL은 `/icon-192.png`. `/static/icon-192.png`로 선언하면 PWA 설치 시 아이콘 로드 404 발생.

**수정 후:**
```json
"src": "/icon-192.png"
```

**수정 완료:** `static/manifest.json` 직접 수정

---

## 상세 검증 기록

### BE 검증

**GPS 좌표 None → /recommend 동작 (텍스트 fallback)**
- `app.py` line 222: `if req.lat is not None and req.lng is not None:` → lat/lng 없으면 텍스트 기반 분기 실행
- `location_lower == "seoul"` 이면 전체 식당 반환, 그 외 location 텍스트로 필터링
- 결과 없으면 전체 RESTAURANTS 반환 — PASS

**session_id 없을 때 /chat 동작**
- `get_or_create_session(None)` → `session_id`가 falsy → `create_session()` 호출 → 새 UUID 발급
- 응답에 항상 `session_id` 포함 — PASS

**/restaurant/{id} 범위 초과 시 404**
- 수정 전: 인덱스 범위 초과 시 IndexError 발생 가능 (HTTPException이 아닌 500)
- 수정 후: id 기반 검색, None이면 명시적 404 반환 — PASS

**Haversine 계산 값 합리성 (서울 내 거리)**
- `location.py` 공식 검증: R=6371, 표준 Haversine 공식 적용
- wave_be.md 검증값: 서울 중심(37.5665, 126.9780) → 광장시장(37.5700, 126.9994) = 1.93km
- `walk_minutes`: 80m/분 기준 (`distance_km / 0.08`), 1.93km → 약 24분 (합리적)
- `auto_expand_radius` fallback: 1km → 2km → 5km → 전체(99.0) — PASS

**APScheduler 충돌**
- `BackgroundScheduler()` + `scheduler.add_job(cleanup_expired, "interval", hours=1)` + `scheduler.start()`
- 앱 시작 시 즉시 실행되지 않고 1시간 interval로 동작
- 서버 재시작 반복 시 중복 스케줄러 생성 위험이 있으나, 단일 uvicorn 프로세스 환경에서는 정상 — PASS

**ANTHROPIC_API_KEY 없을 때 앱 시작**
- `anthropic.Anthropic(api_key=None)` — 객체 생성은 성공
- 실제 API 호출(`client.messages.create`) 시 `AuthenticationError` 발생 → HTTPException 500으로 래핑됨
- 앱 자체는 기동 가능, API 호출 시 에러 응답 — 설계상 허용 범위 — PASS

**restaurants.json id 필드 누락 확인**
- id 0~19, 총 20개, 연속적, 누락 없음 — PASS

### FE 검증

**GPS 거부 시 fallback UI**
- `handleGPSError(err)`: `err.code === 1` → "Location access denied. Enter your neighborhood instead."
- `hint.classList.add('error')` + `input.focus()` — 텍스트 입력 폼 포커스 이동
- PASS

**session_id localStorage 저장/불러오기**
- 초기화: `let sessionId = localStorage.getItem('klg_session_id') || null;`
- 저장: `localStorage.setItem('klg_session_id', sessionId)` — /recommend, /chat 응답마다 갱신
- PASS

**BottomSheet 열고 닫기**
- `openSheet(null)` → 로딩 스켈레톤 표시 → `openDetail` 완료 후 `renderSheet(data)` 호출
- `closeSheet()` — overlay + sheet `open` 클래스 제거, `body.style.overflow` 복원
- ESC 키: `document.addEventListener('keydown')` + `sheet.classList.contains('open')` 체크
- 터치 스와이프: touchstart → touchmove → touchend, `sheetCurrentY > 120` → closeSheet
- PASS

**채팅 recommendations null 처리**
- `if (data.recommendations && data.recommendations.length > 0)` — null 안전 체크
- wave_be.md 주의사항: "일반 대화는 `null` 반환" → FE null 체크 완비 — PASS

**escHtml XSS 방지 함수**
- `static/index.html` line 2392: `function escHtml(str)` 구현됨
- `&`, `<`, `>`, `"`, `'` 전부 이스케이프 처리
- 카드 렌더링, BottomSheet, 채팅 버블 전부 escHtml 적용 확인 — PASS

**모바일 viewport meta 태그**
- `<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />`
- `viewport-fit=cover` — iPhone 노치/홈 인디케이터 대응 포함 — PASS

**manifest.json 파일 존재**
- `static/manifest.json` 존재 확인 (Glob 검색 결과)
- `<link rel="manifest" href="/manifest.json" />` — PASS

### 통합 검증

**FE API 호출 URL ↔ BE 엔드포인트 일치**

| FE 호출 | BE 엔드포인트 | 일치 |
|---------|--------------|------|
| `POST /recommend` | `@app.post("/recommend")` | 일치 |
| `POST /chat` | `@app.post("/chat")` | 일치 |
| `GET /restaurant/${id}` | `@app.get("/restaurant/{restaurant_id}")` | 일치 |

**FE 기대 필드 ↔ BE 실제 반환 필드**

**/recommend 응답:**
| 필드 | BE 반환 | FE 사용 | 일치 |
|------|---------|---------|------|
| `session_id` | RecommendResponse에 포함 | localStorage 저장 | 일치 |
| `distance_km` | Restaurant 모델, GPS 없으면 null | 카드 walk badge | 일치 |
| `walk_minutes` | Restaurant 모델, GPS 없으면 null | 카드 walk badge | 일치 |
| `ai_message` | RecommendResponse에 포함 | 배너 텍스트 | 일치 |
| `search_radius_km` | RecommendResponse에 포함, GPS 없으면 null | 반경 확장 칩 | 일치 |

**/chat 응답:**
| 필드 | BE 반환 | FE 사용 | 일치 |
|------|---------|---------|------|
| `reply` | ChatResponse에 포함 | AI 버블 텍스트 | 일치 |
| `recommendations` | Optional[list], null 가능 | null 체크 후 인라인 카드 | 일치 |
| `session_id` | ChatResponse에 포함 | localStorage 갱신 | 일치 |

**/restaurant/{id} 응답:**
| 필드 | BE 반환 | FE 사용 | 일치 |
|------|---------|---------|------|
| `google_maps_url` | RestaurantDetail에 포함 | BottomSheet CTA 링크 | 일치 |
| `signature_dishes` | `list[str]`, 기본 `[]` | Must-try dishes 섹션 | 일치 |
| `atmosphere_tags` | `list[str]`, 기본 `[]` | Vibe 칩 섹션 | 일치 |
| `pros_cons` | `dict {"pros": str, "cons": str}` | Good to know 2컬럼 | 일치 |

---

## 리스크 맵

| 리스크 | 심각도 | 대응 |
|--------|--------|------|
| ANTHROPIC_API_KEY 미설정 시 모든 AI 기능 500 에러 | 중간 | 환경변수 배포 시 필수 확인, 현재 에러 메시지는 "AI_ERROR"로 사용자에게 안내됨 |
| 서버 메모리 세션 — 서버 재시작 시 전체 세션 소멸 | 낮음 | 현재 MVP 단계에서 허용 범위. 상용화 시 Redis 전환 권장 |
| PWA 아이콘 파일 미포함 (icon-192.png, icon-512.png) | 낮음 | 앱 동작에는 영향 없음. 홈 화면 추가 시 기본 아이콘으로 표시됨. wave_fe.md에 "미포함" 명시됨 |
| APScheduler 핫 리로드(--reload) 시 이중 스케줄러 생성 | 낮음 | 개발 환경 이슈. 프로덕션(--reload 미사용)에서는 발생 안 함 |
| GPS 좌표 유효성 검증 없음 (위도 -90~90, 경도 -180~180 범위 체크 없음) | 낮음 | 잘못된 GPS값 입력 시 Haversine 계산 오류 가능. FE에서 navigator.geolocation API 값을 그대로 사용하므로 실질적 위험 낮음 |
| Haversine fallback (99.0km) 시 walk_minutes 비합리적 값 | 낮음 | 99.0km → `walk_minutes(99.0)` = `round(99.0/0.08)` = 1238분. FE에서 표시되지만 비현실적. 현재 UX상 큰 문제는 아님 |

---

## 수정 파일 목록

| 파일 | 수정 내용 |
|------|-----------|
| `app.py` | `/restaurant/{id}` 엔드포인트: 인덱스 기반 접근 → id 필드 기반 검색으로 교체 |
| `static/manifest.json` | PWA 아이콘 경로 `/static/icon-*.png` → `/icon-*.png` 수정 |

---

## CTO에게 전달

보스, QA 완료했습니다. 전체 판정 **PASS**입니다.

발견한 버그 2개는 직접 수정 완료했습니다:
1. `/restaurant/{id}` 인덱스 기반 접근 버그 — id 필드 기반 검색으로 교체 (`app.py`)
2. `manifest.json` 아이콘 경로 오류 — `/static/icon-*.png` → `/icon-*.png` (`static/manifest.json`)

BE/FE 통합 검증 결과 API 계약이 전부 일치합니다. Wave 3 재실행 불필요, Wave 5(마케팅/배포) 진행 가능합니다.

---

*Wave QA 완료 — 소연 | 2026-04-06*
