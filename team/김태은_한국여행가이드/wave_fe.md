# Wave FE — 완료 보고서

**작성일:** 2026-04-06
**담당:** FE (민준)
**기반:** DESIGN.md v1.0 + wave_pm.md FE 태스크 목록

---

## 구현 화면 목록

| 화면 | ID | 구현 상태 | 비고 |
|------|----|-----------|------|
| Screen 1 — 홈 (GPS) | `#screen-home` | 완료 | idle / locating / error 3상태 |
| Screen 2 — 추천 결과 | `#screen-results` | 완료 | 스켈레톤 + fadeUp 카드 애니 |
| Screen 3 — 채팅 | `#screen-chat` | 완료 | 세션 기반 히스토리 |
| Screen 4 — 식당 상세 | `#bottom-sheet` | 완료 | BottomSheet 슬라이드업 |
| 하단 내비게이션 바 | `.bottom-nav` | 완료 | Home / Chat / Saved(UI only) |

---

## PM 태스크 완료 현황

| ID | 태스크 | 상태 |
|----|--------|------|
| FE-001 | CSS 변수 시스템 전체 교체 | 완료 |
| FE-002 | Screen 1 — 홈 GPS 버튼 화면 | 완료 |
| FE-003 | GPS `getCurrentPosition()` 로직 | 완료 |
| FE-004 | Screen 2 — 카드 결과 화면 | 완료 |
| FE-005 | Screen 4 — BottomSheet 상세 | 완료 |
| FE-006 | Screen 3 — 채팅 UI | 완료 |
| FE-007 | NavigationBar 하단 탭 | 완료 |
| FE-008 | 세션 localStorage 관리 | 완료 |
| FE-009 | 반경 확장 피드백 칩 | 완료 |
| FE-010 | 스켈레톤 UI | 완료 |
| FE-011 | PWA manifest.json | 완료 |
| FE-012 | Toast 에러 컴포넌트 | 완료 |
| FE-013 | 반응형 태블릿 대응 | 완료 |

---

## 주요 JS 함수 목록

### 화면 전환
| 함수 | 역할 |
|------|------|
| `showScreen(name)` | 화면 전환 — 'home' / 'results' / 'chat' |
| `navTo(name)` | 하단 탭 클릭 라우팅 |
| `updateNavBar(screen)` | 활성 탭 상태 업데이트 |

### GPS & 위치
| 함수 | 역할 |
|------|------|
| `handleGPSClick()` | GPS 버튼 클릭 핸들러 — 상태 전환 + geolocation 호출 |
| `handleGPSSuccess(pos)` | GPS 성공 콜백 — lat/lng 저장 + /recommend 호출 |
| `handleGPSError(err, customMsg)` | GPS 실패 처리 — 텍스트 입력 폴백 포커스 |
| `resetGPSBtn()` | GPS 버튼 원상 복구 |

### API
| 함수 | 역할 |
|------|------|
| `findNearby(lat, lng)` | POST /recommend (GPS 좌표 기반) |
| `callRecommendText(query)` | POST /recommend (텍스트 폴백) |
| `handleRecommendResponse(data, lat, lng)` | /recommend 응답 처리 — 세션/카드/칩 업데이트 |
| `openDetail(id)` | GET /restaurant/{id} → BottomSheet 오픈 |
| `sendChat(messageOverride)` | POST /chat — 메시지 전송 + 응답 렌더링 |

### 렌더링
| 함수 | 역할 |
|------|------|
| `renderCards(restaurants)` | Screen 2 카드 3개 렌더링 |
| `buildCardHTML(r, index)` | 단일 RestaurantCard HTML 생성 |
| `showSkeletonCards()` | 로딩 스켈레톤 카드 3개 표시 |
| `clearSkeletonCards()` | 스켈레톤 제거 |
| `renderSheet(r)` | BottomSheet 내용 렌더링 |
| `openSheet(data)` | BottomSheet 열기 (null이면 로딩 상태) |
| `closeSheet()` | BottomSheet 닫기 |

### 채팅
| 함수 | 역할 |
|------|------|
| `addBubble(role, text)` | 채팅 버블 추가 ('user' 또는 'ai') |
| `addTypingBubble()` | AI 타이핑 인디케이터 추가, id 반환 |
| `removeTypingBubble(id)` | 타이핑 인디케이터 제거 |
| `addInlineCards(restaurants)` | 채팅 내 인라인 추천 카드 추가 |
| `sendQuickChip(text)` | 퀵 칩 클릭 → sendChat 호출 |

### 유틸
| 함수 | 역할 |
|------|------|
| `showToast(msg)` | 하단 토스트 메시지 (3초 자동 제거) |
| `copyAddress(addr)` | 주소 클립보드 복사 |
| `filterChipClick(chip)` | 필터 칩 선택 상태 토글 |
| `escHtml(str)` | XSS 방지 HTML 이스케이프 |

---

## 파일 목록

| 파일 | 설명 |
|------|------|
| `static/index.html` | 단일 HTML — 모든 화면 + CSS + JS 포함 |
| `static/manifest.json` | PWA 매니페스트 |

---

## BE가 알아야 할 사항

### 1. API Response 필드 의존성

FE가 사용하는 필드 — 없어도 렌더링은 되지만 UI 품질 저하:

**POST /recommend 응답:**
- `recommendations[].id` — 필수. BottomSheet 호출에 사용
- `recommendations[].walk_minutes` — 카드에 "N min walk" 표시
- `recommendations[].reason` — AI 추천 이유 박스 (핵심 차별 포인트)
- `ai_message` — 상단 배너 텍스트
- `search_radius_km` — 1.0 초과 시 반경 확장 칩 표시
- `session_id` — localStorage 저장, 이후 /chat에 사용

**GET /restaurant/{id} 응답:**
- `signature_dishes` — 배열. "Must-try dishes" 섹션
- `atmosphere_tags` — 배열. "Vibe" 칩 섹션
- `pros_cons.pros` + `pros_cons.cons` — "Good to know" 2컬럼 박스
- `google_maps_url` — BottomSheet 하단 CTA 링크. 없으면 주소로 대체 생성

**POST /chat 응답:**
- `reply` — AI 텍스트 버블
- `recommendations` — 있으면 버블 아래 인라인 카드 표시
- `session_id` — 세션 갱신

### 2. 세션 만료 처리
- `/chat` 404 응답 시 → 세션 초기화 + "Your previous chat expired. Starting fresh!" 메시지 표시
- `/recommend` 응답에서 `session_id`를 항상 내려줘야 함 (신규 세션 발급 포함)

### 3. PWA 아이콘
- `manifest.json`에 `icon-192.png`, `icon-512.png` 경로 선언됨
- `static/` 폴더에 실제 아이콘 파일 추가 필요 (현재 미포함)
- 없어도 PWA 자체는 동작하지만 홈 화면 추가 시 기본 아이콘으로 표시됨

### 4. HTTPS 필요
- `navigator.geolocation`은 HTTPS 환경에서만 동작
- 로컬 개발: `localhost`는 허용됨 (HTTP도 동작)
- 배포 시 반드시 HTTPS 적용 필요

### 5. Content-Type
- FE는 모든 요청에 `Content-Type: application/json` 헤더 포함
- BE는 JSON 응답 시 `Content-Type: application/json` 헤더 반환 필요

---

*Wave FE 완료 — 민준 | 2026-04-06*
