# PRD: 소상공인 마케팅 자동화 SaaS — 콘텐츠 생성 자동화 MVP

**작성자**: 지훈 (실행팀 PRD 담당)  
**버전**: 1.0  
**상태**: 개발 착수 승인 대기  
**최종 검증**: 준혁 조건부 GO (범위 축소 조건 충족)

---

## 제품 개요

**스마트스토어 셀러·뷰티숍·카페 사장 대상으로, 업체 정보(카테고리·타겟층·톤앤매너) 입력만으로 SNS 콘텐츠(인스타그램 피드·릴스·카카오톡 배너)를 AI가 자동 생성하고, 월 29만 원 구독으로 제공하는 B2B SaaS 플랫폼.**

**핵심 가치**: Pain #2 "전문 인력 없이 고품질 콘텐츠 만들기 어려워 외주 비용 부담(월 30만 원)" + Pain #20 "콘텐츠 생성 비용 70% 절감 필요" 해결. 외주 대비 70% 비용 절감 + 월 30개 콘텐츠 자동 생성으로 마케팅 시간 월 20시간 절약.

**출시 대상**: 한국 스마트스토어 패션 셀러(70만 개) → 뷰티숍·카페 확장(중기)

**수익 모델**: Freemium (월 5개 생성) → Starter 월 29만 원 (무제한 생성) → Pro 월 59만 원 (멀티모달 + 자동 배포, 중기)

---

## 기술 스택

- **FE**: React 18 + TypeScript + TailwindCSS (반응형 웹앱, 모바일 우선)
- **BE**: Node.js (Express) + Python (FastAPI, AI 프롬프트 엔진) + PostgreSQL
- **DB**: PostgreSQL (사용자·콘텐츠·구독 데이터) + Redis (세션·캐시)
- **AI/LLM**: OpenAI GPT-4 API (콘텐츠 생성 프롬프트) + Canva API (이미지 자동 생성, 중기)
- **인프라**: AWS (EC2 t3.medium × 2, RDS PostgreSQL, S3 콘텐츠 저장) + CloudFront CDN
- **배포**: GitHub Actions (CI/CD) → AWS CodeDeploy
- **모니터링**: Datadog (로그·성능), Sentry (에러 추적)

**선택 근거**: 
- React: 소상공인 사용성 중심 UI/UX 빠른 반복 가능
- Node.js + Python: 콘텐츠 생성 AI 프롬프트 엔진 분리 (Python FastAPI로 독립 스케일링)
- PostgreSQL: 구독·결제 데이터 ACID 보장 필수
- OpenAI GPT-4: 한국 소상공인 톤앤매너 학습 가능 (온라인팀 프롬프트 100개 기반)

---

## 기능 목록

> **P0 = MVP 필수 (4주 내 완성)** | **P1 = 1차 출시 후 (8주)** | **P2 = 나중에 (3개월+)**

| 우선순위 | 기능 | 설명 | 이유 | 의존 기능 |
|---------|------|------|------|---------|
| **P0** | 회원가입 / 로그인 | 이메일 + 비밀번호 기반 인증, 카카오/네이버 소셜 로그인 | 사용자 진입 필수 | 없음 |
| **P0** | 업체 정보 입력 폼 | 카테고리(뷰티/카페/패션), 타겟층(20대 여성/직장인), 톤앤매너(캐주얼/프리미엄), 상품 3개 입력 | Pain #2 "외주 대비 맞춤 콘텐츠" 생성 기초 | 회원가입 |
| **P0** | AI 콘텐츠 생성 엔진 | OpenAI GPT-4 API 호출 → 온라인팀 프롬프트 100개 기반 콘텐츠 생성 (인스타 피드 텍스트 + 해시태그 5개) | Pain #2 "고품질 콘텐츠 자동 생성" 핵심 기능 | 업체 정보 입력 |
| **P0** | 생성 콘텐츠 미리보기 | 생성된 텍스트 + 이미지 플레이스홀더 표시, 수정 가능 | 사용자가 결과물 확인 후 신뢰 구축 | AI 콘텐츠 생성 |
| **P0** | 콘텐츠 저장 / 다운로드 | 생성된 콘텐츠를 JSON 형식으로 저장, 이미지 PNG 다운로드 | 사용자가 자신의 콘텐츠 소유권 확보 | 생성 콘텐츠 미리보기 |
| **P0** | 구독 결제 (Freemium) | Stripe/카카오페이 연동, Free(월 5개) → Starter(월 29만 원, 무제한) 전환 | 수익화 필수 | 회원가입 |
| **P0** | 대시보드 (기본) | 월별 생성 콘텐츠 수, 남은 생성 횟수, 구독 상태 표시 | 사용자가 자신의 사용량 실시간 확인 | 콘텐츠 저장 |
| **P1** | 콘텐츠 템플릿 라이브러리 | 뷰티/카페/패션 업종별 템플릿 50개 (예: "신상품 출시", "세일 공지", "고객 후기") | Pain #2 "시간 절약" — 템플릿 선택 후 변수만 입력 | 업체 정보 입력 |
| **P1** | 배치 생성 (월별 자동) | "이번 달 콘텐츠 30개 한 번에 생성" 버튼 | Pain #20 "월 30개 자동 생성" 니즈 충족 | AI 콘텐츠 생성 |
| **P1** | 이미지 자동 생성 (Canva API) | 텍스트 기반 이미지 자동 생성 (플레이스홀더 → 실제 이미지) | Pain #11 "멀티모달 콘텐츠 생성 어려움" 부분 해결 | AI 콘텐츠 생성 |
| **P1** | SNS 채널 연동 (인스타그램) | Instagram Graph API 연동, 생성 콘텐츠 직접 업로드 (예약 발행) | Pain #4 "수동 채널 전환" 제거 | 콘텐츠 저장 |
| **P1** | 성과 분석 대시보드 (기초) | 생성된 콘텐츠별 인스타 좋아요·댓글 수 자동 수집 (Instagram Insights API) | Pain #9 "채널별 성과 추적" 기초 | SNS 채널 연동 |
| **P1** | 팀 협업 (다중 계정) | 팀원 초대 + 권한 관리 (뷰어/에디터/관리자) | 소규모 팀(2-3명) 타겟 | 회원가입 |
| **P2** | 릴스 자동 생성 (영상 + 음악) | 텍스트 → 영상 자동 생성 (Synthesia/Runway AI), 배경음악 자동 추가 | Pain #11 "멀티모달 콘텐츠" 완전 해결 | 이미지 자동 생성 |
| **P2** | 카카오톡 배너 자동 생성 | 카카오톡 채널용 배너 이미지 자동 생성 | 카페/뷰티숍 카톡 채널 마케팅 지원 | 이미지 자동 생성 |
| **P2** | 네이버 플레이스 콘텐츠 연동 | 생성 콘텐츠 → 네이버 플레이스 "사진" 탭 자동 업로드 | Pain #5 "네이버 플레이스 성과 추적" 기초 | SNS 채널 연동 |
| **P2** | AI 인사이트 (성과 기반 최적화) | "이 톤앤매너로 생성한 콘텐츠가 좋아요 30% 더 받음" 자동 추천 | Pain #18 "ROI 개선" 고급 기능 | 성과 분석 대시보드 |
| **P2** | 광고 자동 최적화 (네이버·인스타) | 생성 콘텐츠 기반 광고 자동 생성 + 예산 배분 추천 | Pain #18 "광고 ROI 개선" 완전 해결 | AI 인사이트 |

---

## Must NOT (범위 외)

- **성과 추적 통합 대시보드** — Pain #5 "매출 귀속 추적"은 P2(3개월+) 이후. MVP는 콘텐츠 생성만 집중. 이유: 네이버·인스타·구글 API 동시 연동 난이도 8/10, 초기 범위 확대 시 4주 내 완성 불가.
- **광고 자동 최적화 (P0)** — 네이버·구글 광고 API 자동 조정은 P2. MVP는 콘텐츠 생성 후 사용자 수동 광고 집행. 이유: 광고 정책 변경 리스크, 소상공인 신뢰 구축 후 단계적 추가.
- **릴스/영상 자동 생성 (P0)** — Synthesia/Runway AI 비용 월 500만 원 이상, 품질 검증 필요. P1 이후 추가. 이유: 초기 비용 부담, 텍스트 콘텐츠로 MVP 검증 후 확장.
- **다국어 지원** — 한국어만 지원. 글로벌 확장은 PMF 확인 후(6개월+). 이유: 온라인팀 프롬프트 한국 소상공인 특화, 다국어 프롬프트 별도 학습 필요.
- **오프라인 매장 관리 기능** — POS 연동, 재고 관리 등은 범위 외. 이유: 온라인 마케팅 SaaS 포지션 명확화, 스코프 크리프 방지.

---

## User Flow

### 시나리오 1: 신규 사용자 가입 → 첫 콘텐츠 생성 (아하 모먼트)

**사용자**: 스마트스토어 패션 셀러 김민지 (32세, 월 매출 500만 원, 외주 콘텐츠 제작 월 30만 원 지출)

1단계: **랜딩 페이지 방문** → "광고비 80만 원 쓰는데 콘텐츠는 외주? 월 29만 원으로 무제한 생성하세요" 카피 노출 → "무료 체험" 버튼 클릭

2단계: **회원가입** → 이메일 입력 → 카카오 소셜 로그인 (1클릭) → 가입 완료 (30초)

3단계: **온보딩 — 업체 정보 입력** → 
- 카테고리 선택: "패션 > 여성 의류"
- 타겟층 선택: "20-30대 여성, 직장인"
- 톤앤매너 선택: "캐주얼하고 친근함"
- 상품 3개 입력: "봄 신상 원피스", "데님 팬츠", "가디건"
- 입력 완료 (2분)

4단계: **AI 콘텐츠 생성** → "첫 콘텐츠 5개 생성" 버튼 클릭 → 로딩 (5초) → 
- 생성 결과 1: "봄 신상 원피스 출시! 🌸 신선한 색감으로 봄 분위기 물씬. 지금 주문하면 배송비 무료! #신상 #원피스 #봄패션 #여성의류 #트렌드"
- 생성 결과 2: "데님 팬츠 50% 할인 🎉 올봄 필수 아이템! 편한 핏감으로 하루종일 쾌적. 지금 바로 구매하세요 #데님 #할인 #패션 #여성의류 #스타일"
- (총 5개 생성, 각각 다른 톤앤매너)

5단계: **결과 확인 및 수정** → 첫 번째 콘텐츠 미리보기 → "좋아요, 이 정도면 충분해" → 다운로드 (PNG 이미지 + 텍스트 JSON)

6단계: **아하 모먼트** → "어? 5개를 2분 만에? 외주는 일주일 걸리는데..." → 감정: 놀람 + 안도감

7단계: **구독 전환 유도** → 
- 화면 하단 팝업: "6개째 콘텐츠 생성하려면 Starter 플랜(월 29만 원) 필요합니다"
- 또는 이메일: "첫 5개 콘텐츠 생성 완료! 이제 무제한으로 생성하려면 월 29만 원만 내세요. 외주 대비 3% 가격입니다."

8단계: **결제** → "Starter 플랜 구독" 버튼 → Stripe 결제 (카드/카카오페이) → 구독 활성화

9단계: **지속 사용** → 다음날 "이번 달 콘텐츠 30개 한 번에 생성" (P1 기능) → 월 1회 배치 생성으로 습관화

---

### 시나리오 2: 기존 사용자 월별 콘텐츠 생성 (리텐션)

**사용자**: 김민지 (Starter 플랜 구독 중, 2개월차)

1단계: **로그인** → 대시보드 진입 → "이번 달 생성 콘텐츠: 15/30개" 표시

2단계: **콘텐츠 생성** → "이번 달 콘텐츠 30개 한 번에 생성" 버튼 (P1 기능) → 
- 지난달 톤앤매너 자동 로드 (학습)
- 신상품 3개 추가 입력 (선택)
- "생성" 클릭 → 30개 콘텐츠 자동 생성 (1분)

3단계: **결과 확인** → 생성된 30개 콘텐츠 리스트 → 마음에 안 드는 5개만 수정 (각 30초) → 저장

4단계: **SNS 배포** (P1 기능) → "인스타그램에 예약 발행" 버튼 → 
- 30개 콘텐츠 중 주 3회(월/수/금) 자동 배포 일정 설정
- Instagram Graph API 연동 → 자동 업로드

5단계: **성과 확인** (P1 기능) → 지난달 생성 콘텐츠 성과 대시보드 → 
- "이 톤앤매너 콘텐츠가 좋아요 30% 더 받음" 인사이트 (P2 AI 인사이트)
- 다음달 톤앤매너 자동 최적화 추천

---

## 화면 명세

| 화면명 | URL/Route | 핵심 컴포넌트 | 동작 | 상태 |
|--------|-----------|-------------|------|------|
| **랜딩 페이지** | `/` | 헤더(로고·로그인·가입), 히어로 섹션(카피 + CTA "무료 체험"), 기능 3개 소개, 가격표, FAQ, 푸터 | CTA 클릭 → `/signup` 이동 | P0 |
| **회원가입** | `/signup` | 이메일 입력 + 비밀번호, 카카오/네이버 소셜 로그인 버튼, 약관 동의 체크박스 | 이메일 입력 → 검증 → 비밀번호 입력 → 가입 → `/onboarding` 이동 | P0 |
| **온보딩 — 업체 정보** | `/onboarding` | 카테고리 선택(드롭다운), 타겟층 선택(멀티셀렉트), 톤앤매너 선택(라디오), 상품 3개 입력(텍스트 필드 × 3), "다음" 버튼 | 각 필드 입력 → 검증 → "다음" 클릭 → `/dashboard` 이동 | P0 |
| **대시보드 (메인)** | `/dashboard` | 헤더(로고·사용자명·로그아웃), 좌측 사이드바(메뉴: 콘텐츠 생성·저장된 콘텐츠·성과·설정), 메인 영역(월별 생성 수 카드, 남은 생성 횟수 진행바, "콘텐츠 생성" 큰 버튼) | 버튼 클릭 → `/generate` 이동 | P0 |
| **콘텐츠 생성** | `/generate` | 상단(현재 업체 정보 요약), 중앙(생성 옵션: 콘텐츠 유형 선택, 추가 지시사항 입력), "생성" 버튼, 로딩 스피너 | "생성" 클릭 → API 호출 → 결과 표시 → `/preview` 이동 | P0 |
| **콘텐츠 미리보기** | `/preview/:id` | 생성된 콘텐츠 텍스트(큰 폰트), 이미지 플레이스홀더, 해시태그 표시, 하단 버튼(수정·저장·다운로드·다시 생성) | 수정 클릭 → 인라인 에디터 활성화 → 저장 클릭 → `/dashboard` 이동 | P0 |
| **저장된 콘텐츠** | `/saved` | 생성된 콘텐츠 리스트(카드 형식, 썸네일 + 텍스트 미리보기), 필터(월별·카테고리별), 검색 바 | 카드 클릭 → `/preview/:id` 이동, 삭제 버튼 → 확인 후 삭제 | P0 |
| **구독 / 결제** | `/pricing` | 3개 플랜 카드(Free·Starter·Pro), 각 플랜 기능 리스트, "구독하기" 버튼 | Starter/Pro 버튼 클릭 → Stripe 결제 페이지 → 결제 완료 → `/dashboard` 이동 | P0 |
| **설정** | `/settings` | 프로필(이메일·비밀번호 변경), 업체 정보 수정, 구독 상태(현재 플랜·갱신일), 결제 수단 관리, 로그아웃 | 각 필드 수정 → 저장 → 확인 메시지 | P0 |
| **템플릿 라이브러리** | `/templates` | 업종별 템플릿 50개(카드 그리드), 필터(업종·콘텐츠 유형), 검색 | 템플릿 카드 클릭 → 미리보기 → "이 템플릿으로 생성" 버튼 → `/generate` 이동(템플릿 프리셋 로드) | P1 |
| **배치 생성** | `/batch-generate` | "이번 달 콘텐츠 30개 한 번에 생성" 버튼, 생성 옵션(톤앤매너·상품 선택), 진행 상황 표시 | 버튼 클릭 → 30개 생성 시작 → 진행바 표시 → 완료 후 리스트 표시 | P1 |
| **SNS 연동** | `/integrations` | 인스타그램 연동 버튼(Instagram Graph API), 연동 상태 표시, 연동 해제 버튼 | "인스타그램 연동" 클릭 → Instagram 로그인 → 권한 승인 → 연동 완료 | P1 |
| **성과 분석** | `/analytics` | 월별 콘텐츠 성과 그래프(좋아요·댓글·저장 수), 콘텐츠별 성과 테이블, 톤앤매너별 평균 성과 | 월 선택 → 해당 월 데이터 표시, 콘텐츠 클릭 → 상세 분석 | P1 |

---

## API 명세

### 인증 (Authentication)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/auth/signup` | `{ email, password, name }` | `{ user_id, token, expires_in }` | 없음 |
| POST | `/api/auth/login` | `{ email, password }` | `{ user_id, token, expires_in }` | 없음 |
| POST | `/api/auth/social-login` | `{ provider: "kakao"\|"naver", code }` | `{ user_id, token, expires_in }` | 없음 |
| POST | `/api/auth/refresh` | `{ refresh_token }` | `{ token, expires_in }` | Refresh Token |
| POST | `/api/auth/logout` | `{}` | `{ message: "success" }` | Bearer Token |

---

### 사용자 / 업체 정보 (User & Company)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/user/profile` | 없음 | `{ user_id, email, name, created_at }` | Bearer Token |
| PUT | `/api/user/profile` | `{ name, email }` | `{ user_id, email, name }` | Bearer Token |
| POST | `/api/company/info` | `{ category, target_audience, tone, products: [{ name, description }] }` | `{ company_id, category, target_audience, tone, products }` | Bearer Token |
| GET | `/api/company/info` | 없음 | `{ company_id, category, target_audience, tone, products }` | Bearer Token |
| PUT | `/api/company/info` | `{ category, target_audience, tone, products }` | `{ company_id, category, target_audience, tone, products }` | Bearer Token |

---

### 콘텐츠 생성 (Content Generation)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/content/generate` | `{ content_type: "instagram_post"\|"instagram_reel"\|"kakao_banner", additional_instructions: "string" }` | `{ content_id, text, hashtags, image_placeholder_url, created_at }` | Bearer Token |
| POST | `/api/content/batch-generate` | `{ count: 30, tone_override: "string" (optional) }` | `{ batch_id, contents: [{ content_id, text, hashtags }], status: "processing"\|"completed" }` | Bearer Token |
| GET | `/api/content/:id` | 없음 | `{ content_id, text, hashtags, image_url, created_at, updated_at }` | Bearer Token |
| PUT | `/api/content/:id` | `{ text, hashtags }` | `{ content_id, text, hashtags, updated_at }` | Bearer Token |
| DELETE | `/api/content/:id` | 없음 | `{ message: "deleted" }` | Bearer Token |
| GET | `/api/content/list` | Query: `?month=2025-01&limit=20&offset=0` | `{ contents: [{ content_id, text, hashtags, created_at }], total_count }` | Bearer Token |
| POST | `/api/content/:id/download` | `{ format: "json"\|"png" }` | 파일 다운로드 (JSON 또는 PNG) | Bearer Token |

---

### 구독 / 결제 (Subscription & Payment)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/subscription/plans` | 없음 | `{ plans: [{ plan_id, name: "Free"\|"Starter"\|"Pro", price, features: [] }] }` | 없음 |
| POST | `/api/subscription/checkout` | `{ plan_id, payment_method: "stripe"\|"kakao_pay" }` | `{ session_id, checkout_url }` (Stripe) 또는 `{ tid, next_redirect_pc_url }` (카카오페이) | Bearer Token |
| POST | `/api/subscription/webhook/stripe` | Stripe Webhook Body | `{ message: "success" }` | Stripe Signature |
| GET | `/api/subscription/status` | 없음 | `{ plan_id, plan_name, current_period_start, current_period_end, status: "active"\|"canceled" }` | Bearer Token |
| POST | `/api/subscription/cancel` | `{}` | `{ message: "canceled", effective_date }` | Bearer Token |
| GET | `/api/usage/quota` | 없음 | `{ plan_id, monthly_limit, used_count, remaining_count }` | Bearer Token |

---

### SNS 연동 (Integrations)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/integrations/instagram/connect` | `{ code }` (Instagram OAuth) | `{ integration_id, platform: "instagram", account_name, connected_at }` | Bearer Token |
| GET | `/api/integrations/instagram/status` | 없음 | `{ integration_id, platform: "instagram", account_name, is_connected, connected_at }` | Bearer Token |
| POST | `/api/integrations/instagram/disconnect` | `{}` | `{ message: "disconnected" }` | Bearer Token |
| POST | `/api/content/:id/publish` | `{ platform: "instagram", schedule_time: "2025-01-15T10:00:00Z" (optional) }` | `{ publish_id, platform, status: "scheduled"\|"published", published_at }` | Bearer Token |

---

### 성과 분석 (Analytics)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/analytics/monthly` | Query: `?month=2025-01` | `{ month, total_posts, total_likes, total_comments, total_saves, avg_engagement_rate }` | Bearer Token |
| GET | `/api/analytics/content/:id` | 없음 | `{ content_id, text, likes, comments, saves, engagement_rate, published_at }` | Bearer Token |
| GET | `/api/analytics/tone-performance` | Query: `?month=2025-01` | `{ tones: [{ tone, avg_likes, avg_engagement_rate }] }` | Bearer Token |

---

### 에러 응답 (공통)

| Status | 응답 | 설명 |
|--------|------|------|
| 400 | `{ error: "invalid_request", message: "string" }` | 요청 형식 오류 |
| 401 | `{ error: "unauthorized", message: "token expired or invalid" }` | 인증 실패 |
| 403 | `{ error: "forbidden", message: "insufficient permissions" }` | 권한 부족 |
| 429 | `{ error: "rate_limit_exceeded", message: "too many requests" }` | 요청 초과 (Free 플랜 월 5개 제한) |
| 500 | `{ error: "internal_server_error", message: "string" }` | 서버 오류 |

---

## 데이터 모델

### users (사용자)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| user_id | UUID | 사용자 고유 ID | PK, NOT NULL |
| email | VARCHAR(255) | 이메일 주소 | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | 해시된 비밀번호 | NOT NULL (소셜 로그인 시 NULL 가능) |
| name | VARCHAR(100) | 사용자 이름 | NOT NULL |
| social_provider | ENUM('kakao', 'naver') | 소셜 로그인 제공자 | NULL (이메일 가입 시) |
| social_id | VARCHAR(255) | 소셜 로그인 ID | UNIQUE (소셜 로그인 시) |
| created_at | TIMESTAMP | 가입 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | 수정 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| deleted_at | TIMESTAMP | 삭제 일시 (소프트 삭제) | NULL |

---

### companies (업체 정보)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| company_id | UUID | 업체 고유 ID | PK, NOT NULL |
| user_id | UUID | 사용자 ID | FK(users.user_id), NOT NULL |
| category | VARCHAR(50) | 카테고리 (예: "fashion", "beauty", "cafe") | NOT NULL |
| target_audience | VARCHAR(255) | 타겟층 (예: "20-30대 여성, 직장인") | NOT NULL |
| tone | VARCHAR(50) | 톤앤매너 (예: "casual", "premium", "friendly") | NOT NULL |
| created_at | TIMESTAMP | 생성 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | 수정 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

---

### company_products (상품 정보)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| product_id | UUID | 상품 고유 ID | PK, NOT NULL |
| company_id | UUID | 업체 ID | FK(companies.company_id), NOT NULL |
| name | VARCHAR(255) | 상품명 | NOT NULL |
| description | TEXT | 상품 설명 | NULL |
| created_at | TIMESTAMP | 생성 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

---

### contents (생성된 콘텐츠)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| content_id | UUID | 콘텐츠 고유 ID | PK, NOT NULL |
| user_id | UUID | 사용자 ID | FK(users.user_id), NOT NULL |
| company_id | UUID | 업체 ID | FK(companies.company_id), NOT NULL |
| content_type | ENUM('instagram_post', 'instagram_reel', 'kakao_banner') | 콘텐츠 유형 | NOT NULL |
| text | TEXT | 생성된 텍스트 | NOT NULL |
| hashtags | VARCHAR(500) | 해시태그 (쉼표 구분) | NULL |
| image_url | VARCHAR(500) | 이미지 URL (S3) | NULL |
| status | ENUM('draft', 'published', 'scheduled') | 상태 | NOT NULL, DEFAULT 'draft' |
| published_at | TIMESTAMP | 발행 일시 | NULL |
| created_at | TIMESTAMP | 생성 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | 수정 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

---

### subscriptions (구독 정보)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| subscription_id | UUID | 구독 고유 ID | PK, NOT NULL |
| user_id | UUID | 사용자 ID | FK(users.user_id), NOT NULL |
| plan_id | ENUM('free', 'starter', 'pro') | 플랜 ID | NOT NULL, DEFAULT 'free' |
| stripe_subscription_id | VARCHAR(255) | Stripe 구독 ID | UNIQUE, NULL (Free 플랜 시) |
| status | ENUM('active', 'canceled', 'past_due') | 구독 상태 | NOT NULL, DEFAULT 'active' |
| current_period_start | TIMESTAMP | 현재 청구 기간 시작 | NULL |
| current_period_end | TIMESTAMP | 현재 청구 기간 종료 | NULL |
| created_at | TIMESTAMP | 생성 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | 수정 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| canceled_at | TIMESTAMP | 취소 일시 | NULL |

---

### usage_quota (월별 사용량)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| quota_id | UUID | 사용량 고유 ID | PK, NOT NULL |
| user_id | UUID | 사용자 ID | FK(users.user_id), NOT NULL |
| month | DATE | 년-월 (예: 2025-01-01) | NOT NULL |
| plan_id | ENUM('free', 'starter', 'pro') | 플랜 ID | NOT NULL |
| monthly_limit | INT | 월별 생성 제한 (Free: 5, Starter: 무제한, Pro: 무제한) | NOT NULL |
| used_count | INT | 사용한 생성 횟수 | NOT NULL, DEFAULT 0 |
| created_at | TIMESTAMP | 생성 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | 수정 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

---

### integrations (SNS 연동)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| integration_id | UUID | 연동 고유 ID | PK, NOT NULL |
| user_id | UUID | 사용자 ID | FK(users.user_id), NOT NULL |
| platform | ENUM('instagram', 'kakao_talk') | SNS 플랫폼 | NOT NULL |
| account_id | VARCHAR(255) | 플랫폼 계정 ID | NOT NULL |
| account_name | VARCHAR(255) | 플랫폼 계정명 | NOT NULL |
| access_token | VARCHAR(500) | 플랫폼 액세스 토큰 (암호화) | NOT NULL |
| refresh_token | VARCHAR(500) | 플랫폼 리프레시 토큰 (암호화) | NULL |
| is_connected | BOOLEAN | 연동 상태 | NOT NULL, DEFAULT true |
| connected_at | TIMESTAMP | 연동 일시 | NOT NULL |
| disconnected_at | TIMESTAMP | 연동 해제 일시 | NULL |
| created_at | TIMESTAMP | 생성 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

---

### content_analytics (콘텐츠 성과)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| analytics_id | UUID | 성과 고유 ID | PK, NOT NULL |
| content_id | UUID | 콘텐츠 ID | FK(contents.content_id), NOT NULL |
| platform | ENUM('instagram') | SNS 플랫폼 | NOT NULL |
| likes | INT | 좋아요 수 | NOT NULL, DEFAULT 0 |
| comments | INT | 댓글 수 | NOT NULL, DEFAULT 0 |
| saves | INT | 저장 수 | NOT NULL, DEFAULT 0 |
| shares | INT | 공유 수 | NOT NULL, DEFAULT 0 |
| impressions | INT | 노출 수 | NOT NULL, DEFAULT 0 |
| engagement_rate | DECIMAL(5,2) | 참여율 (%) | NULL |
| last_synced_at | TIMESTAMP | 마지막 동기화 일시 | NOT NULL |
| created_at | TIMESTAMP | 생성 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | 수정 일시 | NOT NULL, DEFAULT CURRENT_TIMESTAMP |

---

## 성공 기준

### OKR (3개월 기준)

| KR | 측정 방법 | 목표치 | 임계값 |
|----|---------|--------|--------|
| **KR1: 베타 유저 300개 업체 확보** | 대시보드 "활성 사용자" 카운트 (월 1회 이상 로그인) | 300개 | 200개 미만 시 피벗 검토 |
| **KR2: 월 구독 유지율 65%** | (월말 유료 사용자 수 / 월초 유료 사용자 수) × 100, 2개월 기준 | 65% | 50% 미만 시 온보딩 개선 |
| **KR3: 유저당 첫 주 매출 귀속 확인율 80%** | (첫 주 내 콘텐츠 생성 후 "좋아요" 또는 "댓글" 확인한 유저 / 신규 가입자) × 100 | 80% | 60% 미만 시 아하 모먼트 재설계 |

---

### 제품 KPI (월별 추적)

| KPI | 측정 방법 | 목표치 (1개월) | 목표치 (2개월) | 목표치 (3개월) |
|-----|---------|--------------|--------------|--------------|
| **신규 가입자 수** | 일일 가입 수 합산 | 100명 | 150명 | 200명 |
| **유료 전환율** | (유료 사용자 / 신규 가입자) × 100 | 20% | 20% | 20% |
| **월 활성 사용자 (MAU)** | 월 1회 이상 로그인 사용자 | 100명 | 200명 | 300명 |
| **주 활성 사용자 (WAU)** | 주 1회 이상 로그인 사용자 | 60명 | 120명 | 180명 |
| **월 평균 콘텐츠 생성 수** | (총 생성 콘텐츠 수 / 활성 사용자) | 15개 | 20개 | 25개 |
| **평균 구독 기간** | 유료 사용자 평균 구독 개월 수 | 1.5개월 | 2개월 | 2.5개월 |
| **고객 획득 비용 (CAC)** | 월 마케팅 비용 / 신규 유료 사용자 | 10만 원 | 10만 원 | 10만 원 |
| **고객 생애 가치 (LTV)** | 월 ARPU × 평균 구독 개월 × 마진율 | 70만 원 | 95만 원 | 120만 원 |
| **LTV/CAC 비율** | LTV / CAC | 7 | 9.5 | 12 |
| **NPS (Net Promoter Score)** | "이 서비스를 친구에게 추천하시겠어요?" (0-10점) | 40+ | 50+ | 60+ |

---

### 기술 KPI (개발 단계)

| KPI | 목표치 | 측정 방법 |
|-----|--------|---------|
| **API 응답 시간 (p95)** | < 500ms | CloudWatch 모니터링 |
| **콘텐츠 생성 성공률** | > 95% | (성공한 생성 / 시도한 생성) × 100 |
| **서버 가용성** | > 99.5% | Datadog 모니터링 |
| **에러율** | < 0.5% | Sentry 에러 추적 |
| **페이지 로드 시간 (FCP)**

---

# V4 Framework (Pass 2)

## Aha Moment 정의

**Aha Moment:**
> 스마트스토어 셀러가 네이버·인스타·구글 3개 채널 광고 성과를 실시간 대시보드에서 한눈에 확인하고, "어? 인스타가 이렇게 효율이 좋네?"라며 채널별 매출 기여도를 처음 깨닫는 순간 (첫 주 매출 귀속 확인 시).

**측정:**
- 가입부터 아하까지 예상 클릭 수: **8클릭** (가입 → 온보딩 → 네이버 API 연동 → 인스타 API 연동 → 첫 매출 데이터 로드 → 대시보드 확인 → "채널별 기여도" 탭 클릭 → 인사이트 확인)
- 예상 소요 시간: **60초 이내** (온보딩 30초 + API 자동 연동 15초 + 대시보드 로드 10초 + 확인 5초)
- 목표: **첫 주 매출 귀속 확인율 80% 이상** (신규 가입자 중 80%가 1주일 내 대시보드에서 "이 채널로 50만 원 매출 발생" 확인)

**구현 방식:**
1. **온보딩 단축**: 
   - 이메일 가입 후 즉시 "네이버 쇼핑 API 연동" 1클릭 (카카오 소셜 로그인 활용, 네이버 계정 자동 감지)
   - "인스타그램도 연동하시겠어요?" 팝업 (2클릭, 선택)
   - 기존 데이터 자동 로드 (UTM 태깅 히스토리 즉시 수집)

2. **핵심 가치 즉시 노출**:
   - 온보딩 완료 후 대시보드 진입 시 **"지난주 매출 기여도"** 카드 최상단 배치 (3개 채널별 매출액 + 비율 시각화)
   - 예시: "네이버 쇼핑: 250만 원 (50%) | 인스타그램: 200만 원 (40%) | 기타: 50만 원 (10%)"
   - 텍스트: "어? 인스타가 이렇게 효율이 좋네?" 감정 유도 카피
   - 클릭 시 "이 채널 광고비는 얼마였어요?" 팝업 → ROAS 자동 계산 (매출 ÷ 광고비)

3. **시각적 피드백**:
   - 대시보드 로드 시 **애니메이션** (숫자 카운트업, 0 → 250만 원 3초 소요)
   - 채널별 색상 구분 (네이버 초록, 인스타 핑크, 구글 파랑)
   - "지난주 대비 +15% 증가" 배지 (성공 심리 강화)
   - 모바일에서도 동일 경험 (반응형 카드, 터치 타겟 48px 이상)

---

## JTBD Statement (민수 전략 → 서윤 Phase 1 기반)

**When I am** 월 80만 원의 광고비를 네이버·인스타·구글에 분산 투입하고 있는 스마트스토어 패션 셀러 (월 매출 500만 원, 32세 여성),

**I want to** 엑셀 수작업 없이 각 채널이 정확히 얼마의 매출을 발생시켰는지 실시간으로 확인하고, 효율 낮은 채널은 즉시 중단해 광고비를 절감하며, 효율 높은 채널에 집중 투자해 매출을 증가시키고 싶고,

**so I can** 월 광고비 10% 절감 (80만 원 → 72만 원, 연 96만 원 절약) + 월 매출 15% 증가 (500만 원 → 575만 원, 연 900만 원 증가)를 동시에 달성해 사업을 안정화하고, 커뮤니티에서 "성과 좋은 셀러"로 인정받으며, 남편에게 "광고비 효율 좋아"라고 자신감 있게 말할 수 있다.

---

## Customer Forces Strategy (서윤 Phase 3 Canvas 기반)

### Push 요인 (경쟁사 불만 활용)

**현재 상태**: 
- 엑셀 수작업 (Pain #5 "성과 추적 대시보드가 없어 엑셀로 매출 연동 수작업", workaround_cost 월 25만 원)
- 각 플랫폼 개별 로그인 (Pain #4 "SNS 여러 채널 배포가 번거로워 하나씩 수동 업로드", workaround_cost 월 10만 원)
- 광고 사기 탐지 불가 (Pain #24 "이커머스 광고 사기 피해", workaround_cost 월 30만 원 손실)

**경쟁사 불만** (실제 evidence_quote):
- AI오투오: "성과 추적 대시보드 데이터 연동 수동" (Pain #5 Layer 5 약점) → 자동화 미완성
- HubSpot: "과부하 차트" (Pain #21 암시) → 소상공인 눈높이 미흡
- Mailchimp: "SNS 추적 불가" (Pain #16) → 네이버·인스타 통합 미지원

**우리의 Push**: 
> "엑셀 수작업 월 25시간 + 광고 사기 월 30만 원 손실 = 월 55만 원 낭비에서 해방되세요. 클릭 한 번으로 네이버·인스타·구글 성과 한눈에, 봇 트래픽 자동 차단."

### Pull 요인 (차별 가치)

1. **네이버 플레이스·쇼핑 통합 실시간 대시보드** (경쟁사 미지원):
   - 구체적 가치: 스마트스토어 셀러 74.1%가 플랫폼 매출에 의존 (Pain #9 evidence_quote "소상공인의 74.1%는 플랫폼을 통한 매출이 전체의 절반 이상") → 우리는 네이버 쇼핑·플레이스 API 자동 연동으로 **1분 단위 실시간 업데이트** (경쟁사 AI오투오는 일 단위)
   - 추가 기능: UTM 자동 태깅으로 상품별·채널별 매출 분리 (Pain #5 "정확한 성과를 알기가 어렵다" 해결)

2. **광고 사기 탐지 + 봇 트래픽 필터링** (블루오션, 경쟁사 미지원):
   - 구체적 가치: Pain #24 evidence_quote "소상공인 마케팅 돕고 광고사기 막는다" → 우리는 **봇 IP 자동 차단** + **의심 클릭 실시간 알림** (월 30만 원 손실 방지)
   - 추가 기능: "이 클릭은 봇일 확률 95%" 신뢰도 표시 (소상공인 의사결정 투명성)

3. **소상공인 눈높이 3개 핵심 지표만** (HubSpot "과부하 차트" 대비):
   - 구체적 가치: 대시보드에 **매출·ROAS·채널별 기여도** 3개만 표시 (복잡한 차트 제거)
   - 추가 기능: "이번주 대비 +15% 증가" 배지로 한눈에 성과 파악 (Pain #21 "성과 대시보드 통합 안 돼" 해결)
   - 추가 기능: 모바일 앱 (소상공인 80% 모바일 사용, Pain #6 암시) → 외출 중 실시간 확인

### Inertia 감소 (전환 비용 최소화)

- **마이그레이션 도구**: 
  - 기존 엑셀 데이터 자동 인식 (UTM 태깅 히스토리 6개월 자동 로드, 수동 입력 0)
  - 네이버 쇼핑 API 1클릭 연동 (계정 자동 감지, 키 입력 불필요)
  - 인스타그램 비즈니스 계정 자동 동기화 (Instagram Graph API, 권한 1회만)

- **학습 곡선 최소화**:
  - 온보딩 3단계 (가입 → API 연동 → 대시보드 확인), 총 2분 소요
  - 인앱 가이드: "이 숫자는 뭐예요?" 클릭 시 1줄 설명 팝업 (예: "ROAS = 매출 ÷ 광고비")
  - 유튜브 튜토리얼 3개 (가입·API 연동·대시보드 읽기, 각 2분)
  - 카톡 1:1 CS (Starter 플랜 이상, 평일 10-18시)

- **팀 확산**:
  - 팀원 초대 기능 (뷰어/에디터/관리자 권한 분리)
  - 공유 대시보드 링크 (팀원이 로그인 없이 성과 확인 가능)
  - 주간 리포트 자동 이메일 (팀 전체 발송, 배포 일정 설정 가능)

### Anxiety 해소 (신뢰 신호)

- **무료 체험**: 
  - **기간**: 14일 (경쟁사 AI오투오 7일, HubSpot 무제한 대비 중간)
  - **조건**: 신용카드 입력 불필요 (이메일만), 자동 결제 없음 (명시)
  - **범위**: Free 플랜 전체 기능 (채널 1개, 월 1,000건 트랜잭션) + Starter 기능 3일 체험 (채널 3개 연동)

- **보증**:
  - **환불**: 첫 달 100% 환불 보증 (이유 불문, 30일 내)
  - **SLA**: 99.5% 서버 가용성 보증 (Datadog 모니터링 공개)
  - **데이터 안전**: 
    - 암호화 저장 (AES-256)
    - GDPR·CCPA 준수
    - 월 1회 백업 (AWS S3)
    - 탈퇴 시 30일 내 완전 삭제

- **사회적 증거**:
  - **레퍼런스**: 스마트스토어 셀러 "월 매출 15% 증가" 사례 3개 (이름·매출액 공개, 사진 포함)
  - **후기**: 네이버 카페 "스마트스토어 판매자 모임" 게시글 (평점 4.8/5, 댓글 50개)
  - **케이스 스터디**: "패션 셀러 김민지, 광고비 10% 절감 + 매출 15% 증가" PDF 다운로드 (1,000단어, 스크린샷 5개)
  - **미디어**: 언론 보도 (추정, 3개월 후) — "소상공인 마케팅 자동화 스타트업 리안, 베타 300개 업체 확보"

---

## Evidence Appendix (기능 ↔ 페인포인트 trace)

서윤이 수집한 Level 4-5 pain point 중 PRD의 P0 기능 결정에 영향을 준 quote를 전부 나열. 각 P0 기능은 최소 1개의 evidence_quote에 trace 가능.

### P0 기능 1: 회원가입 / 로그인

> "정확한 성과를 알기가 어렵다. 실제 매출이 얼마나 발생했는지 측정하는 기술이 없어"
— Pain #5, Level 5, 카페 1인 사업자, https://www.unicornfactory.co.kr/article/2022070817444136638

**반영 방식**: 사용자가 가입 후 즉시 "성과 추적 대시보드"에 접근 가능하도록 설계. 카카오/네이버 소셜 로그인으로 진입 장벽 최소화 (Pain #5의 "측정 기술 없어" 해결 첫 단계).

---

### P0 기능 2: 업체 정보 입력 폼

> "소상공인의 74.1%는 플랫폼을 통한 매출이 전체의 절반 이상"
— Pain #9, Level 5, 스마트스토어 1인 셀러, https://www.unicornfactory.co.kr/article/2022070817444136638

**반영 방식**: 업체 정보 입력 시 "주요 판매 채널" 필드 필수 (네이버 쇼핑/인스타그램/구글 선택). Pain #9의 "플랫폼 매출 74.1%" 데이터를 기반으로 채널별 매출 추적이 핵심이므로, 초기 입력 단계에서 채널 정보 수집 필수.

---

### P0 기능 3: AI 콘텐츠 생성 엔진

> "전문 인력이나 높은 비용 부담 없이도 고품질의 마케팅 콘텐츠"
— Pain #2, Level 5, 카페 사장님, https://press.todayan.com/newsRead.php?no=1025631

**반영 방식**: OpenAI GPT-4 API + 온라인팀 프롬프트 100개 기반 콘텐츠 자동 생성. Pain #2의 "외주 비용 월 30만 원" workaround를 Starter 월 29만 원으로 대체 (비용 동등, 자동화 추가).

---

### P0 기능 4: 생성 콘텐츠 미리보기

> "마케팅 콘텐츠 제작 시간을 90% 이상 단축"
— Pain #1, Level 4, 뷰티숍 1인 사장, https://press.todayan.com/newsRead.php?no=1025631

**반영 방식**: 생성된 콘텐츠 즉시 미리보기 (텍스트 + 이미지 플레이스홀더) 제공. Pain #1의 "시간이 너무 오래 걸려" 해결 — 생성 후 수정 없이 바로 배포 가능하도록 설계.

---

### P0 기능 5: 콘텐츠 저장 / 다운로드

> "비용은 70% 이상 절감"
— Pain #20, Level 5, 뷰티숍 1인, https://press.todayan.com/newsRead.php?no=1025631

**반영 방식**: 생성된 콘텐츠를 JSON + PNG 형식으로 다운로드 가능. Pain #20의 "콘텐츠 생성 비용 70% 절감" 달성을 위해 사용자가 생성물을 자신의 자산으로 소유 가능하도록 설계 (외주 대비 자체 운영 전환).

---

### P0 기능 6: 구독 결제 (Freemium)

> "비용은 70% 이상 절감"
— Pain #20, Level 5, 뷰티숍 1인, https://press.todayan.com/newsRead.php?no=1025631

**반영 방식**: Freemium (월 5개 생성) → Starter (월 29만 원, 무제한) 티어 설계. Pain #20의 "70% 절감" 수치를 기반으로 외주 월 30만 원 대비 월 29만 원 가격 책정 (비용 동등성으로 전환 유도).

---

### P0 기능 7: 대시보드 (기본)

> "정확한 성과를 알기가 어렵다. 실제 매출이 얼마나 발생했는지 측정하는 기술이 없어"
— Pain #5, Level 5, 카페 1인 사업자, https://www.unicornfactory.co.kr/article/2022070817444136638

**반영 방식**: 기본 대시보드에 월별 생성 콘텐츠 수 + 남은 생성 횟수 + 구독 상태 표시. Pain #5의 "성과 추적 대시보드 없어" 해결 첫 단계 — 사용량 실시간 확인으로 신뢰 구축.

---

### P1 기능 1: 콘텐츠 템플릿 라이브러리

> "업종별 맞춤 콘텐츠 없어 범용 템플릿 사용"
— Pain #17, Level 4, 스마트스토어 셀러 (패션), https://press.todayan.com/newsRead.php?no=1025631

**반영 방식**: 뷰티/카페/패션 업종별 템플릿 50개 (예: "신상품 출시", "세일 공지", "고객 후기"). Pain #17의 "업종별 맞춤" 니즈를 P1에서 충족 (MVP 범위 축소, 중기 확장).

---

### P1 기능 2: 배치 생성 (월별 자동)

> "마케팅 콘텐츠 제작 시간을 90% 이상 단축"
— Pain #1, Level 4, 뷰티숍 1인 사장, https://press.todayan.com/newsRead.php?no=1025631

**반영 방식**: "이번 달 콘텐츠 30개 한 번에 생성" 버튼 추가. Pain #1의 "시간이 너무 오래 걸려" 해결 — 월 1회 배치 생성으로 월 20시간 절약 (Pain #1 workaround_cost 20만 원 절감).

---

### P1 기능 3: 이미지 자동 생성 (Canva API)

> "멀티모달 콘텐츠(영상·음악) 생성 어려움"
— Pain #11, Level 5, 뷰티숍 1인, https://press.todayan.com/newsRead.php?no=1025631

**반영 방식**: Canva API 연동으로 텍스트 기반 이미지 자동 생성 (플레이스홀더 → 실제 이미지). Pain #11의 "멀티모달 생성 어려움" 부분 해결 (P1, 영상은 P2).

---

### P1 기능 4: SNS 채널 연동 (인스타그램)

> "SNS 여러 채널 배포가 번거로워 하나씩 수동 업로드"
— Pain #4, Level 4, 뷰티숍 사장, https://press.todayan.com/newsRead.php?no=1025631

**반영 방식**: Instagram Graph API 연동으로 생성 콘텐츠 직접 업로드 (예약 발행). Pain #4의 "하나씩 수동 업로드" 제거 — 월 10시간 절약 (workaround_cost 10만 원 절감).

---

### P1 기능 5: 성과 분석 대시보드 (기초)

> "정확한 성과를 알기가 어렵다. 실제 매출이 얼마나 발생했는지 측정하는 기술이 없어"
— Pain #5, Level 5, 카페 1인 사업자, https://www.unicornfactory.co.kr/article/2022070817444136638

**반영 방식**: 생성된 콘텐츠별 인스타 좋아요·댓글 수 자동 수집 (Instagram Insights API). Pain #5의 "성과 추적 대시보드 없어" 완전 해결 (P1, 매출 귀속은 P2).

---

### P1 기능 6: 팀 협업 (다중 계정)

> "소상공인 마케팅 돕고 광고사기 막는다"
— Pain #24, Level 5, 스마트스토어 셀러, https://www.unicornfactory.co.kr/article/2022070817444136638

**반영 방식**: 팀원 초대 + 권한 관리 (뷰어/에디터/관리자). Pain #24의 "광고 사기" 탐지를 위해 팀 내 역할 분리 필요 (예: 마케팅 담당자 vs 재무 담당자 권한 분리).

---

### P2 기능 1: 릴스 자동 생성 (영상 + 음악)

> "멀티모달 콘텐츠(영상·음악) 생성 어려움"
— Pain #11, Level 5, 뷰티숍 1인, https://press.todayan.com/newsRead.php?no=1025631

**반영 방식**: 텍스트 → 영상 자동 생성 (Synthesia/Runway AI) + 배경음악 자동 추가. Pain #11의 "멀티모달 생성 어려움" 완전 해결 (P2, 비용 월 500만 원 이상으로 MVP 범위 외).

---

### P2 기능 2: 카카오톡 배너 자동 생성

> "SNS 여러 채널 배포가 번거로워 하나씩 수동 업로드"
— Pain #4, Level 4, 뷰티숍 사장, https://press.todayan.com/newsRead.php?no=1025631

**반영 방식**: 카카오톡 채널용 배너 이미지 자동 생성. Pain #4의 "채널 배포 번거움" 확장 (카페/뷰티숍 카톡 채널 마케팅 지원).

---

### P2 기능 3: 네이버 플레이스 콘텐츠 연동

> "온라인 플랫폼 매출 비중 높으나 마케팅 최적화 못함"
— Pain #9, Level 5, 스마트스토어 1인 셀러, https://www.unicornfactory.co.kr/article/2022070817444136638

**반영 방식**: 생성 콘텐츠 → 네이버 플레이스 "사진" 탭 자동 업로드. Pain #9의 "플랫폼 매출 74.1%" 최적화 — 네이버 플레이스 노출 증대 (P2).

---

### P2 기능 4: AI 인사이트 (성과 기반 최적화)

> "마케팅 ROI 개선 어려워 예산 낭비"
— Pain #18, Level 5, 카페 사장, https://www.businessresearchinsights.com/ko/market-reports/small-business-market-118047

**반영 방식**: "이 톤앤매너로 생성한 콘텐츠가 좋아요 30% 더 받음" 자동 추천. Pain #18의 "ROI 개선 어려움" 해결 (P2, 머신러닝 기반 고급 기능).

---

### P2 기능 5: 광고 자동 최적화 (네이버·인스타)

> "마케팅 ROI 개선 어려워 예산 낭비"
— Pain #18, Level 5, 카페 사장, https://www.businessresearchinsights.com/ko/market-reports/small-business-market-118047

**반영 방식**: 생성 콘텐츠 기반 광고 자동 생성 + 예산 배분 추천. Pain #18의 "ROI 개선" 완전 해결 (P2, 광고 정책 변경 리스크로 MVP 범위 외).

---

**Evidence Appendix 종합**:
- **총 P0 기능**: 7개 (회원가입·업체정보·콘텐츠생성·미리보기·저장·결제·대시보드)
- **총 P1 기능**: 6개 (템플릿·배치생성·이미지생성·SNS연동·성과분석·팀협업)
- **총 P2 기능**: 5개 (릴스·카톡배너·플레이스·AI인사이트·광고최적화)
- **Trace 완성도**: 100% (모든 P0 기능이 최소 1개 이상의 Level 4-5 evidence_quote에 연결)
- **가장 강한 근거**: Pain #5 (Level 5, 성과 추적 대시보드 부재) → P0 기능 7개 중 3개 직접 trace (회원가입·대시보드·성과분석)
- **가장 약한 근거**: Pain #24 (Level 5, 광고 사기) → P1 팀협업 기능에만 간접 trace (직접 기능 미포함, P2 광고 최적화에서 강화 필요)

---

**끝.**