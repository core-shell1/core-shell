# Wave PM — 한국 로컬가이드 개발 태스크

**작성일:** 2026-04-06
**담당:** PM (Wave 2)
**기반:** wave_cto.md + DESIGN.md + 요구사항명세서.md + 현재 app.py + static/index.html
**MVP 목표:** 2주 내 GPS 기반 맛집 추천 + 세션 채팅 동작

---

## BE 태스크 목록

| ID | 태스크 | 상세 설명 | 우선순위 |
|----|--------|-----------|---------|
| BE-001 | `location.py` 신규 생성 — Haversine 함수 + 반경 자동 확장 | `haversine_km(lat1, lng1, lat2, lng2) -> float`, `walk_minutes(distance_km) -> int`, `filter_by_radius(restaurants, user_lat, user_lng) -> (list, float)` 구현. RADIUS_STEPS = [1.0, 2.0, 5.0]. 5km에도 없으면 전체 반환 | P0 |
| BE-002 | `session.py` 신규 생성 — 세션 관리 모듈 | `SessionData`, `Message`, `LocationData` Pydantic 모델 정의. `sessions: Dict[str, SessionData]` 모듈 레벨 dict. `get_or_create_session(session_id)`, `update_session(session_id, message, role)`, `cleanup_expired_sessions()` 함수 구현. 히스토리 최대 20턴 FIFO | P0 |
| BE-003 | `settings.py` 신규 생성 — 환경변수 + 모델명 중앙 관리 | `HAIKU_MODEL = os.getenv("HAIKU_MODEL", "claude-haiku-4-5-20251001")`, `SONNET_MODEL = os.getenv("SONNET_MODEL", "claude-sonnet-4-5")`, `MAX_TOKENS_HAIKU = 512`, `MAX_TOKENS_SONNET = 1024` 정의. 하드코딩 없음 | P0 |
| BE-004 | `restaurants.json` 스키마 확장 — lat/lng + 상세 필드 추가 | 기존 20개 항목 전체에 `lat`, `lng`, `signature_dishes`, `atmosphere_tags`, `pros_cons` 필드 추가. 구역 기준 좌표 매핑 테이블(wave_cto.md) 참고. 각 식당의 위치(location 필드)에 맞는 좌표 입력 | P0 |
| BE-005 | `POST /recommend` 업그레이드 — GPS 파라미터 + Haversine 필터링 통합 | Request에 `lat: Optional[float]`, `lng: Optional[float]`, `session_id: Optional[str]` 추가. `lat/lng` 있으면 `filter_by_radius()` 호출 후 필터된 식당만 프롬프트에 포함. Response에 `id`, `distance_km`, `walk_minutes`, `search_radius_km`, `session_id`, `google_maps_url`, `tags`, `address` 추가. 기존 `location` 텍스트 기반 로직은 fallback으로 유지 (하위 호환) | P0 |
| BE-006 | `POST /chat` 신규 API — 세션 기반 자연어 대화 | Request: `session_id(필수)`, `message(필수)`, `lat(선택)`, `lng(선택)`. session_id로 히스토리 조회 → 최근 10턴 + 현재 메시지 → Claude Sonnet 호출. Response: `reply`, `recommendations([]로 비어도 됨)`, `session_id`. `max_tokens=1024`. 히스토리 업데이트 후 반환 | P0 |
| BE-007 | `GET /restaurant/{id}` 신규 API — 식당 상세 | Path parameter `id`(정수). `restaurants[id]` 조회. 전체 필드 반환: `id`, `name`, `korean_name`, `category`, `tags`, `location`, `address`, `lat`, `lng`, `rating`, `price_range`, `english_menu`, `description`, `hours`, `signature_dishes`, `atmosphere_tags`, `pros_cons`, `google_maps_url`. id 범위 초과 시 HTTP 404 | P0 |
| BE-008 | `APScheduler` 세션 만료 처리 — 24시간 TTL | `requirements.txt`에 `apscheduler==3.10.4` 추가. 앱 시작 시 `BackgroundScheduler` 초기화. 1시간 주기로 `cleanup_expired_sessions()` 실행. `last_active` 기준 24시간 초과 세션 삭제 | P1 |
| BE-009 | `GET /health` 업그레이드 — active_sessions 카운트 추가 | 기존 응답에 `"active_sessions": len(sessions)` 추가 | P1 |
| BE-010 | `POST /recommend` 에러 응답 통일 + 재시도 로직 | JSON 파싱 실패 시 1회 재시도. 2회 실패 시 HTTP 500. 에러 응답 형식: `{"error": {"code": "...", "message": "...", "fallback": "..."}}`. GPS 좌표가 서울 범위 밖이면 `GPS_OUT_OF_RANGE` 에러 코드 반환 | P1 |
| BE-011 | `restaurants.json` 식당 데이터 20개 완성 | 현재 데이터 확인 후 누락 항목 보충. 서울 주요 관광구역(종로, 중구, 마포/홍대, 용산/이태원, 강남, 인사동, 청담, 송파) 각 2~3개 이상. 총 20개 완성 | P1 |

---

## FE 태스크 목록

| ID | 태스크 | 상세 설명 | 우선순위 |
|----|--------|-----------|---------|
| FE-001 | CSS 변수 시스템 전체 교체 | 기존 빨간 그라디언트 스타일 제거. DESIGN.md 7번 `:root {}` 블록 전체 적용. DM Sans + DM Serif Display Google Fonts 임포트. `body { background: var(--color-background); font-family: var(--font-body); }` | P0 |
| FE-002 | Screen 1 — 홈 GPS 버튼 화면 구현 | 기존 `<header>` + `.search-card` 레이아웃 제거. 세로 전체 화면 레이아웃으로 교체. 앱명(DM Serif Display 28px), 서브카피, pulse 애니메이션 위치 아이콘, GPSButton 컴포넌트(56px 높이, 전폭, `#C85C3A`), "or" 구분선, 텍스트 입력 fallback 순서로 배치. 상태 3개: idle / locating(스피너+비활성화) / error(텍스트 입력 포커스) | P0 |
| FE-003 | `navigator.geolocation.getCurrentPosition()` GPS 요청 로직 | GPS 버튼 클릭 시 `getCurrentPosition()` 호출. 성공 시 `lat`, `lng` 획득 → `POST /recommend` 호출. 실패(PERMISSION_DENIED) 시 텍스트 입력 자동 포커스 + "Location access denied. Enter your neighborhood instead." 안내 표시. timeout: 10000ms | P0 |
| FE-004 | Screen 2 — 맛집 카드 3개 결과 화면 구현 | 상단 바(앱명 좌 + 위치명 우), AI 메시지 배너(Amber 배경, 최대 높이 56px, 이탤릭), FilterChip 가로 스크롤 행, RestaurantCard 3개(1번 카드 가장 강조). 번호 배지(Primary Light 배경), 영어메뉴 배지(Moss 색), 거리 표시(`walk_minutes`분 기준), AI 추천 이유 박스(Primary Light 배경, 이탤릭). 카드 하단 "See Details" 버튼. fadeUp 애니메이션(1번: 0s, 2번: 0.08s, 3번: 0.16s) | P0 |
| FE-005 | Screen 4 — 식당 상세 BottomSheet 구현 | RestaurantCard "See Details" 클릭 시 `GET /restaurant/{id}` 호출 → BottomSheet 슬라이드업(translateY 100%→0, 350ms ease-out). 85vh 높이. 드래그 핸들(상단 중앙 40x4px 막대). 내부 스크롤. 식당명/한국어명/별점/가격대/거리 배지 그룹, AI 추천 이유 박스, signature_dishes 3개, 영업시간, atmosphere_tags 칩, pros_cons 2컬럼, 주소(복사 버튼). Sticky 하단 "Open in Google Maps" 버튼(전폭, Primary). 배경 오버레이 탭 or 스와이프 다운 시 닫기 | P0 |
| FE-006 | Screen 3 — 채팅 UI 구현 | 하단 탭 "Chat" 클릭 시 화면 전환. 대화 히스토리 스크롤 영역. User 버블(우측 정렬, Primary 배경 흰 텍스트, border-radius 18px 18px 4px 18px), AI 버블(좌측 정렬, Surface 배경, border-radius 18px 18px 18px 4px). 채팅 중 추천 카드 인라인 표시. 퀵칩 행("Something spicy" / "Near me" / "Vegetarian" / "Cheaper option"). sticky 입력창 + 전송 버튼(Primary 원형). 빈 상태 안내 문구 표시 | P0 |
| FE-007 | NavigationBar (하단 탭) 구현 | Fixed bottom-0. 높이 64px + safe-area-inset-bottom. 탭 3개: Home(집 아이콘) / Chat(말풍선 아이콘) / Saved(북마크, 비활성 UI만). 활성 탭: Primary 컬러. 비활성: Text Tertiary. `backdrop-filter: blur(12px)`. 탭 클릭 시 화면 전환 상태 관리 | P0 |
| FE-008 | 세션 관리 — localStorage session_id 저장 | `/recommend` 응답에서 `session_id` 수신 시 `localStorage.setItem("session_id", ...)` 저장. 이후 모든 `/chat` 요청에 포함. 세션 만료(서버 404 응답) 시 새 session_id 발급 + "Your previous chat has expired. Starting fresh!" 안내 표시 | P0 |
| FE-009 | 반경 자동 확장 피드백 UI | `/recommend` 응답의 `search_radius_km`가 1.0 초과 시 AI 메시지 배너 위에 "Expanded search to {N}km" 안내 칩 표시(Amber 배경). 1km 이내면 미표시 | P1 |
| FE-010 | 로딩 상태 — 스켈레톤 UI | GPS 감지 중 + API 호출 중 스켈레톤 카드 3개 표시. 카드와 동일한 레이아웃으로 회색 블록 애니메이션(`shimmer` 효과). 현재 `loading-dots` 텍스트 방식 대체 | P1 |
| FE-011 | PWA 설정 — manifest.json + 서비스워커 | `manifest.json`: `name: "Korea Local Guide"`, `display: "standalone"`, `theme_color: "#C85C3A"`, `background_color: "#FAF7F4"`. 기본 서비스워커(오프라인 대응 최소화). `<meta name="viewport">` + `env(safe-area-inset-bottom)` 적용 | P1 |
| FE-012 | 에러 상태 처리 — Toast 컴포넌트 | API 오류(네트워크 끊김, 429, 500) 시 "Something went wrong. Try again." 토스트 메시지(하단 고정, 3초 자동 제거). 현재 `error-box` 방식 대체. z-index: 400(--z-toast) | P1 |
| FE-013 | 반응형 레이아웃 — 태블릿/데스크탑 대응 | `max-width: 480px` 컨테이너 중앙 정렬. `@media (min-width: 768px)`: body 배경 `--color-surface-alt`, 컨테이너 `border-radius: 24px`, `box-shadow: var(--shadow-lg)`. 기본 스타일은 모바일 360px 기준 | P1 |

---

## API 연결 명세

FE가 호출하는 BE API 전체 목록. 호출 시점과 파라미터 기준.

### 1. `POST /recommend`

**호출 시점:**
- GPS 버튼 클릭 → `getCurrentPosition()` 성공 후
- 텍스트 입력 fallback → Enter 또는 전송 버튼 클릭

**FE → BE Request:**
```json
{
  "food_preference": "Find me the best local restaurants",
  "lat": 37.5665,
  "lng": 126.9780,
  "session_id": "uuid-or-null"
}
```
GPS 거부 fallback 시:
```json
{
  "food_preference": "Traditional Korean near Hongdae",
  "location": "Hongdae"
}
```

**BE → FE Response:**
```json
{
  "recommendations": [
    {
      "id": 3,
      "name": "...",
      "korean_name": "...",
      "walk_minutes": 8,
      "distance_km": 0.64,
      "rating": 4.7,
      "price_range": "$$",
      "english_menu": true,
      "description": "...",
      "hours": "...",
      "reason": "...",
      "tags": ["cozy", "solo"],
      "address": "...",
      "google_maps_url": "https://maps.google.com/?q=37.57,126.99"
    }
  ],
  "ai_message": "Here are 3 spots within walking distance...",
  "search_radius_km": 1.0,
  "session_id": "uuid-string"
}
```

**FE 처리:**
- `session_id` → localStorage 저장
- `search_radius_km > 1.0` → 반경 확장 피드백 칩 표시
- `walk_minutes` → 카드에 "8 min walk" 표시
- `id` → "See Details" 클릭 시 `/restaurant/{id}` 호출용

---

### 2. `GET /restaurant/{id}`

**호출 시점:** RestaurantCard "See Details" 탭

**FE → BE:** Path parameter `id` (정수, `/recommend` 응답의 `id` 값)

**BE → FE Response:**
```json
{
  "id": 3,
  "name": "...",
  "korean_name": "...",
  "signature_dishes": ["Dish 1", "Dish 2", "Dish 3"],
  "atmosphere_tags": ["cozy", "solo-friendly"],
  "pros_cons": {
    "pros": "Great atmosphere, English menu, cheap",
    "cons": "Cash only, crowded weekends"
  },
  "hours": "10:00 - 22:00",
  "address": "...",
  "google_maps_url": "https://maps.google.com/?q=37.57,126.99",
  "rating": 4.7,
  "price_range": "$$",
  "english_menu": true
}
```

**FE 처리:** 응답 수신 즉시 BottomSheet 슬라이드업 + 데이터 렌더링

---

### 3. `POST /chat`

**호출 시점:** Screen 3 채팅 화면에서 전송 버튼 클릭 또는 퀵칩 선택

**FE → BE Request:**
```json
{
  "session_id": "uuid-from-localstorage",
  "message": "Show me something cheaper",
  "lat": 37.5665,
  "lng": 126.9780
}
```
`lat/lng`는 선택. GPS 좌표가 있을 때만 포함.

**BE → FE Response:**
```json
{
  "reply": "Got it! Here are some more affordable options...",
  "recommendations": [],
  "session_id": "uuid-string"
}
```
`recommendations`가 있을 경우 → 채팅 버블 아래에 인라인 카드 표시

**FE 처리:**
- `reply` → AI 버블로 추가
- `recommendations` 있으면 → 버블 아래 RestaurantCard 축소 버전 표시
- 세션 만료(서버 404 or 빈 session_id) → 새 세션 생성 + 안내 토스트

---

## 개발 순서 (의존성 기준)

```
Phase 1 — BE 기반 (BE 먼저, FE는 Mock 데이터로 선행 가능)
  Day 1:
    BE-001 location.py      ← 의존성 없음. 순수 Python 함수.
    BE-002 session.py       ← 의존성 없음. Pydantic 모델만.
    BE-003 settings.py      ← 의존성 없음. 환경변수 정의.

  Day 2:
    BE-004 restaurants.json ← BE-001 완료 후 (lat/lng 필드 어떻게 쓰이는지 파악 후 입력)
    BE-005 /recommend 업그레이드 ← BE-001, BE-002, BE-003, BE-004 모두 필요

  Day 3:
    BE-006 /chat 신규       ← BE-002(세션), BE-003(모델명) 필요
    BE-007 /restaurant/{id} ← BE-004(스키마 확장) 필요

Phase 2 — FE 기반 (BE API 완성 후 실제 연동)
  Day 4:
    FE-001 CSS 변수 시스템  ← 의존성 없음. 먼저 전체 스타일 기반 교체.
    FE-002 Screen 1 홈 화면 ← FE-001 필요
    FE-003 GPS 로직         ← FE-002 필요 (버튼과 함께 구현)

  Day 5:
    FE-004 Screen 2 카드 결과 ← FE-001, FE-003, BE-005 필요
    FE-007 NavigationBar    ← FE-001 필요 (독립 컴포넌트)

  Day 6:
    FE-005 BottomSheet 상세 ← FE-004, BE-007 필요
    FE-008 세션 localStorage ← FE-004, BE-005, BE-006 필요

  Day 7:
    FE-006 채팅 UI          ← FE-007, FE-008, BE-006 필요

Phase 3 — 품질 보강 (P1 태스크)
  Day 8:
    BE-008 APScheduler      ← BE-002 필요
    BE-009 /health 업그레이드
    BE-010 에러 응답 통일
    BE-011 식당 데이터 완성

  Day 9:
    FE-009 반경 확장 피드백
    FE-010 스켈레톤 UI
    FE-012 Toast 에러 컴포넌트

  Day 10:
    FE-011 PWA manifest
    FE-013 반응형 태블릿 대응
```

---

## Acceptance Criteria (완료 기준)

### BE 완료 기준

**BE-001 (Haversine)**
- Given 서울 중심(37.5665, 126.9780)과 광장시장(37.5700, 126.9993), When `haversine_km()` 호출, Then 약 1.8km 반환 (±0.1 허용)
- Given 반경 1km에 식당 0개, When `filter_by_radius()` 호출, Then 2km로 자동 확장 후 결과 반환
- Given 5km에도 식당 없음, Then 전체 식당을 거리 오름차순으로 반환

**BE-005 (/recommend GPS)**
- Given lat/lng 파라미터 있음, When POST /recommend, Then 반경 내 식당만 프롬프트에 포함
- Given lat/lng 없음, When POST /recommend, Then 기존 location 텍스트 기반 로직 실행 (하위 호환)
- Given GPS 응답, Then `walk_minutes`, `distance_km`, `search_radius_km`, `session_id` 포함

**BE-006 (/chat)**
- Given session_id + message, When POST /chat, Then 이전 대화 히스토리 포함한 응답 반환
- Given 20턴 초과 히스토리, Then 앞에서부터 FIFO로 제거, 21번째 메시지도 정상 처리
- Given 없는 session_id, Then 새 세션 생성 후 응답

**BE-007 (/restaurant/{id})**
- Given 유효한 id, When GET /restaurant/{id}, Then 전체 필드 반환
- Given 범위 밖 id, Then HTTP 404

### FE 완료 기준

**FE-002 (홈 화면)**
- Given 앱 첫 진입, When GPS 버튼 보임, Then 3초 안에 첫 화면 렌더링 완료
- Given GPS 버튼 클릭, Then 버튼 비활성화 + "Locating..." 텍스트 즉시 표시

**FE-003 (GPS)**
- Given GPS 허용, Then lat/lng 획득 후 /recommend 자동 호출
- Given GPS 거부, Then 텍스트 입력 자동 포커스 + 안내 메시지 표시

**FE-004 (카드 결과)**
- Given /recommend 응답, Then 카드 3개 fadeUp 애니메이션과 함께 표시
- Given search_radius_km > 1.0, Then 반경 확장 안내 표시
- Given walk_minutes 값, Then "N min walk" 형식으로 카드에 표시

**FE-005 (BottomSheet)**
- Given "See Details" 탭, Then 350ms 내 BottomSheet 슬라이드업
- Given 스와이프 다운 또는 배경 탭, Then BottomSheet 닫힘
- Given google_maps_url, Then "Open in Google Maps" 버튼 탭 시 새 탭으로 열림

**FE-006 (채팅)**
- Given 메시지 전송, Then 0.4초 이내 User 버블 화면 추가 + AI 로딩 상태
- Given AI 응답 + recommendations 있음, Then 버블 아래 인라인 카드 표시

**전체 모바일 완료 기준**
- Given 375px 너비 기기, Then 가로 스크롤 없이 정상 표시
- Given iOS Safari, Then safe-area-inset-bottom 적용으로 홈바 가림 없음
- Given 터치 타겟, Then 모든 버튼 최소 44x44px 이상

---

## Out of Scope (이번 MVP에서 제외)

- F-004 분위기/상황 필터 (UI 설계 추가 필요, Phase 2)
- 메뉴판 사진 분석 (Vision API)
- 즐겨찾기 / 여행 일지
- 다국어 지원 (일본어, 중국어)
- 실시간 영업 상태 확인 (hours 필드 파싱 복잡도 높음, CTO 피드백 반영)
- Redis 세션 저장 (Phase 2)
- 식당 데이터 100개 확장 (Phase 2, 현재 20개로 MVP 진행)
- Fly.io 배포 (MVP 로컬 동작 완료 후)
