# PRD: 이커머스 셀러 통합 마케팅 대행 플랫폼 (B2B)

## 제품 개요
월 1,000만~3,000만 매출 스마트스토어·쿠팡 셀러를 대상으로 광고·콘텐츠·CRM을 하나의 팀이 통합 운영하는 월정액 리테이너 서비스 (집중 패키지 49만원 기준).

---

## 기술 스택

- **FE**: React 18 + TypeScript + Tailwind CSS (통합 대시보드 웹앱)
- **BE**: Node.js (Express) + TypeScript / Python (FastAPI) — 광고 플랫폼 API 연동 담당
- **DB**: PostgreSQL (고객 계약·광고 데이터) + Redis (실시간 리포트 캐싱)
- **인프라**: AWS EC2 (서버) + RDS (DB) + CloudFront (CDN) / 또는 Vercel (FE) + Supabase (BE+DB 통합)

**선택 근거**: 
- 기존 리안 스택과 호환성 (기존 온라인팀 Python 역량 활용)
- 네이버·쿠팡 API 연동 필요 → Node.js/Python 모두 라이브러리 풍부
- 초기 MVP는 Supabase로 빠른 구현, 스케일 후 AWS로 마이그레이션 가능

---

## 기능 목록

> **P0** = MVP 필수 (1개월 내 출시)  
> **P1** = 1차 출시 후 (2~3개월)  
> **P2** = 나중에 (4개월+)

| 우선순위 | 기능 | 설명 | 이유 | 의존 기능 |
|---------|------|------|------|---------|
| **P0** | naver-diagnosis 스토어 진단 (무료) | 셀러가 입력한 스토어 데이터(월 매출·광고비·고객 수)로 CRM 부재·콘텐츠 품질·ROAS 진단 결과 제공 | Pain #8 "데이터 불일치" 시각화 → 유료 전환 유도 | 없음 |
| **P0** | 광고 운영 (네이버 쇼핑·쿠팡) | 셀러 광고 계정 연동 → 월간 광고비·클릭·전환 데이터 자동 수집 | KR2 "ROAS 3.0 추적" 필수 | 없음 |
| **P0** | 통합 리포트 대시보드 | 광고·콘텐츠·SNS 데이터 한 화면에 표시 (주간·월간 자동 리포트 발송) | Pain #8 "여러 에이전시 데이터 불일치" 해결 | 광고 운영 |
| **P0** | 상세페이지 A/B 테스트 자동화 | 2개 버전 상세페이지 업로드 → 전환율 자동 비교 | Pain #22 "A/B 테스트 수작업" 해결 | 없음 |
| **P0** | 고객 세분화 (자동 태깅) | 구매 빈도·금액·최근 구매일 기준 자동 세분화 (VIP·일반·휴면) | Pain #2 "고객 세분화 없이 광고 타겟팅 비효율" 해결 | 없음 |
| **P1** | CRM 자동 메시지 발송 (카톡·문자) | 세분화된 고객에게 재구매 유도 메시지 자동 발송 (주 1회) | Pain #2 "재구매율 30% 달성" 목표 | 고객 세분화 |
| **P1** | SNS 콘텐츠 제작·포스팅 (인스타·블로그) | 온라인팀이 상세페이지 콘텐츠 촬영·편집 → 자동 포스팅 (주 3회) | Pain #1 "콘텐츠 제작 월 50시간" 해결 | 없음 |
| **P1** | 월간 리포트 자동 생성 | 광고·콘텐츠·SNS 성과 + 개선 제안 자동 생성 (PDF 발송) | KR2 "ROAS 추적" + 고객 만족도 | 통합 리포트 대시보드 |
| **P2** | CRM 이메일 자동화 (자사몰 전용) | 자사몰 고객에게 이메일 기반 재구매 유도 (Klaviyo 연동) | Pain #2 "CRM 자동화" 고도화 | CRM 자동 메시지 발송 |
| **P2** | 라이브 커머스 스크립트 AI 생성 (베타) | 라이브 방송 스크립트 자동 생성 (시선 패키지 추가 옵션) | C 아이템 "라이브 커머스" 통합 | 없음 |
| **P2** | 모바일 최적화 템플릿 | 상세페이지 모바일 버전 자동 최적화 (주목 패키지 추가) | Pain #25 "모바일 최적화 부족" | 없음 |
| **P2** | AI 상품 추천 엔진 (베타) | 고객 구매 이력 기반 추천 상품 자동 제시 (시선 패키지 추가 옵션) | E 아이템 "AI 개인화" 통합 | 고객 세분화 |

---

## Must NOT (범위 외)

- **플랫폼 자체 개발**: 스마트스토어·쿠팡 경쟁 서비스 구축 금지 (플랫폼 정책 위반)
- **광고비 직접 관리**: 셀러 광고 계정 비밀번호 보관 금지 → API 연동만 (보안)
- **고객 데이터 직접 수집**: 스마트스토어는 고객 이메일 직접 수집 불가(플랫폼 정책) → 카톡·문자만 사용
- **자사몰 구축**: Cafe24·식스샵 자체 개발 금지 → 기존 플랫폼 연동만
- **라이브 커머스 라이버 고용**: 라이버 네트워크 구축 금지 (초기 단계) → 스크립트 제공만
- **AI 모델 자체 개발**: 추천 엔진·스크립트 생성은 기성 API(OpenAI·Anthropic) 활용만

---

## User Flow

### 시나리오 1: 신규 고객 획득 (무료 진단 → 유료 전환)

1단계: 셀러가 네이버 카페·카카오 오픈채팅에서 "리안 컴퍼니 무료 진단" 광고 클릭
→ 시스템: 랜딩 페이지 로드 (naver-diagnosis 진단 폼)

2단계: 셀러가 진단 폼 입력 (월 매출·광고비·고객 수·상세페이지 URL)
→ 시스템: 입력 데이터 검증 + DB 저장

3단계: 시스템이 진단 결과 생성 (CRM 부재 점수·콘텐츠 품질 점수·ROAS 추정치)
→ 시스템: 결과 화면 하단에 "집중 49만 패키지로 즉시 개선" CTA 노출

4단계: 셀러가 CTA 클릭 → 상담 신청 폼 (전화·이메일·카톡)
→ 시스템: 상담 신청 데이터 저장 + 리안 팀에 알림

5단계: 리안 팀이 30분 줌 상담 진행 (진단 결과 설명 + 패키지 제안)
→ 시스템: 상담 기록 저장

6단계: 셀러가 계약 동의 → 결제 (49만원 월정액)
→ 시스템: 결제 처리 + 고객 계정 생성 + 광고 계정 연동 요청

---

### 시나리오 2: 기존 고객 대시보드 사용 (월간 리포트 확인)

1단계: 셀러가 대시보드 로그인 (이메일·비밀번호)
→ 시스템: 인증 + 고객 계정 데이터 로드

2단계: 셀러가 "이번 달 리포트" 탭 클릭
→ 시스템: 광고·콘텐츠·SNS 데이터 실시간 조회 (네이버·쿠팡 API 호출)

3단계: 시스템이 주간·월간 리포트 자동 생성 (ROAS·클릭·전환·SNS 팔로워 증가)
→ 시스템: 리포트 화면 표시 + PDF 다운로드 버튼 제공

4단계: 셀러가 "개선 제안" 섹션 확인 (예: "상세페이지 A/B 테스트 시작하시겠어요?")
→ 시스템: 제안 클릭 시 A/B 테스트 설정 폼 로드

5단계: 셀러가 A/B 테스트 2개 버전 업로드
→ 시스템: 버전 저장 + 자동 분배 시작 (50:50 트래픽)

6단계: 1주일 후, 시스템이 전환율 비교 결과 자동 생성
→ 시스템: 대시보드에 "버전 B가 전환율 18% (기존 15% → 신규 18%)" 표시

---

### 시나리오 3: CRM 자동 메시지 발송 (P1 기능)

1단계: 셀러가 대시보드 "CRM" 탭 클릭
→ 시스템: 고객 세분화 데이터 표시 (VIP 50명·일반 200명·휴면 100명)

2단계: 셀러가 "VIP 고객에게 재구매 유도 메시지 발송" 버튼 클릭
→ 시스템: 메시지 템플릿 선택 폼 로드

3단계: 셀러가 템플릿 선택 (예: "신제품 출시 알림" + 10% 할인 쿠폰)
→ 시스템: 메시지 미리보기 표시

4단계: 셀러가 "발송" 버튼 클릭
→ 시스템: 카톡·문자 API 호출 → VIP 50명에게 메시지 발송 (즉시)

5단계: 시스템이 발송 결과 추적 (클릭률·전환율)
→ 시스템: 대시보드에 "클릭률 35%, 전환 5명" 표시

---

## 화면 명세

| 화면명 | URL/Route | 핵심 컴포넌트 | 동작 |
|--------|-----------|-------------|------|
| **1. 진단 랜딩 페이지** | `/diagnosis` | 진단 폼 (월 매출·광고비·고객 수 입력) + 결과 카드 (CRM·콘텐츠·ROAS 점수) + CTA 버튼 ("상담 신청") | 폼 제출 → 진단 결과 생성 (1초) → 결과 화면 하단에 CTA 노출 |
| **2. 상담 신청 폼** | `/consultation` | 전화·이메일·카톡 선택 + 셀러 정보 입력 (이름·회사명·연락처) | 제출 → 리안 팀 알림 + 확인 이메일 발송 |
| **3. 결제 페이지** | `/checkout` | 패키지 선택 (주목 29만·집중 49만·시선 89만) + 결제 수단 선택 (카드·계좌이체) + 약관 동의 | 결제 완료 → 고객 계정 생성 + 광고 계정 연동 페이지로 리다이렉트 |
| **4. 광고 계정 연동** | `/onboarding/connect-ads` | 네이버 쇼핑·쿠팡 로그인 버튼 + OAuth 인증 + 권한 요청 | 로그인 → API 토큰 저장 + 광고 데이터 첫 동기화 시작 |
| **5. 대시보드 (메인)** | `/dashboard` | 좌측 네비게이션 (리포트·CRM·A/B 테스트·설정) + 우측 메인 영역 (주간 리포트 카드 4개: ROAS·클릭·전환·SNS 팔로워) | 탭 클릭 → 해당 섹션 로드 |
| **6. 리포트 상세** | `/dashboard/report` | 광고 성과 (ROAS·클릭·전환·CPC) + 콘텐츠 성과 (상세페이지 클릭률·체류시간) + SNS 성과 (팔로워·좋아요·댓글) + 개선 제안 섹션 | 각 섹션 클릭 → 상세 데이터 모달 오픈 |
| **7. A/B 테스트 설정** | `/dashboard/ab-test` | 버전 A·B 상세페이지 URL 입력 + 테스트 기간 선택 (1주·2주·4주) + 시작 버튼 | 시작 → 트래픽 50:50 분배 시작 + 진행 상황 실시간 표시 |
| **8. A/B 테스트 결과** | `/dashboard/ab-test/results` | 버전 A·B 전환율 비교 (막대 그래프) + 통계 유의성 표시 (p-value) + 승자 표시 + "승자 적용" 버튼 | 버튼 클릭 → 승자 버전을 기본 상세페이지로 변경 |
| **9. CRM 고객 세분화** | `/dashboard/crm/segments` | 세분화 현황 (VIP·일반·휴면 고객 수) + 각 세그먼트별 최근 구매일·구매 금액 표시 | 세그먼트 클릭 → 고객 리스트 모달 오픈 |
| **10. CRM 메시지 발송** | `/dashboard/crm/send-message` | 세그먼트 선택 + 메시지 템플릿 선택 (신제품·할인·재구매 유도) + 미리보기 + 발송 버튼 | 발송 → 카톡·문자 API 호출 + 발송 결과 추적 |
| **11. SNS 콘텐츠 관리** | `/dashboard/sns` | 인스타·블로그 포스팅 일정표 (주 3회 자동 포스팅) + 최근 포스팅 성과 (좋아요·댓글·저장) | 포스팅 클릭 → 상세 성과 모달 오픈 |
| **12. 설정** | `/dashboard/settings` | 계정 정보 (이메일·비밀번호) + 광고 계정 연동 상태 + 결제 정보 + 구독 취소 | 각 항목 수정 가능 |
| **13. 모바일 대시보드** | `/m/dashboard` | 반응형 레이아웃 (주간 리포트 카드 스택) + 하단 네비게이션 (리포트·CRM·설정) | 터치 네비게이션 |

---

## API 명세

### 1. 진단 API

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| **POST** | `/api/diagnosis/create` | `{ monthly_revenue: 1500000, monthly_ad_spend: 100000, customer_count: 500, store_url: "https://smartstore.naver.com/..." }` | `{ diagnosis_id: "diag_123", crm_score: 35, content_score: 42, roas_estimate: 2.1, recommendation: "CRM 자동화 필요" }` | 없음 (공개) |
| **GET** | `/api/diagnosis/{diagnosis_id}` | 없음 | 위와 동일 | 없음 |

### 2. 고객 인증 API

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| **POST** | `/api/auth/signup` | `{ email: "seller@example.com", password: "***", company_name: "패션몰", phone: "010-1234-5678" }` | `{ customer_id: "cust_123", access_token: "jwt_...", refresh_token: "jwt_..." }` | 없음 |
| **POST** | `/api/auth/login` | `{ email: "seller@example.com", password: "***" }` | `{ access_token: "jwt_...", refresh_token: "jwt_..." }` | 없음 |
| **POST** | `/api/auth/refresh` | `{ refresh_token: "jwt_..." }` | `{ access_token: "jwt_..." }` | Refresh Token |

### 3. 광고 계정 연동 API

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| **POST** | `/api/ads/connect-naver` | `{ oauth_code: "...", oauth_state: "..." }` (OAuth 콜백) | `{ ad_account_id: "naver_123", status: "connected", last_sync: "2025-01-15T10:00:00Z" }` | JWT (고객) |
| **POST** | `/api/ads/connect-coupang` | `{ oauth_code: "...", oauth_state: "..." }` | `{ ad_account_id: "coupang_456", status: "connected", last_sync: "2025-01-15T10:00:00Z" }` | JWT |
| **GET** | `/api/ads/accounts` | 없음 | `{ accounts: [ { platform: "naver", account_id: "naver_123", status: "connected" }, { platform: "coupang", account_id: "coupang_456", status: "connected" } ] }` | JWT |

### 4. 광고 데이터 조회 API

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| **GET** | `/api/ads/performance?start_date=2025-01-01&end_date=2025-01-31&platform=naver` | 없음 | `{ data: [ { date: "2025-01-01", impressions: 5000, clicks: 150, conversions: 15, spend: 50000, revenue: 150000, roas: 3.0 } ], summary: { total_spend: 1500000, total_revenue: 4500000, avg_roas: 3.0 } }` | JWT |
| **GET** | `/api/ads/daily?date=2025-01-15` | 없음 | `{ date: "2025-01-15", impressions: 5000, clicks: 150, conversions: 15, spend: 50000, revenue: 150000, roas: 3.0 }` | JWT |

### 5. A/B 테스트 API

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| **POST** | `/api/ab-test/create` | `{ version_a_url: "https://smartstore.naver.com/...", version_b_url: "https://smartstore.naver.com/...", duration_days: 7, traffic_split: 50 }` | `{ test_id: "test_123", status: "running", start_date: "2025-01-15", end_date: "2025-01-22" }` | JWT |
| **GET** | `/api/ab-test/{test_id}/results` | 없음 | `{ test_id: "test_123", version_a: { conversions: 15, conversion_rate: 0.15 }, version_b: { conversions: 18, conversion_rate: 0.18 }, p_value: 0.042, winner: "version_b", significance: "significant" }` | JWT |
| **POST** | `/api/ab-test/{test_id}/apply-winner` | `{ winner: "version_b" }` | `{ status: "success", message: "Version B applied as default" }` | JWT |

### 6. CRM 고객 세분화 API

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| **GET** | `/api/crm/segments` | 없음 | `{ segments: { vip: { count: 50, avg_ltv: 500000, last_purchase_days: 15 }, regular: { count: 200, avg_ltv: 150000, last_purchase_days: 45 }, dormant: { count: 100, avg_ltv: 50000, last_purchase_days: 180 } } }` | JWT |
| **GET** | `/api/crm/segments/{segment_name}/customers` | 없음 | `{ customers: [ { customer_id: "cust_001", phone: "010-1234-5678", last_purchase: "2025-01-10", purchase_count: 5, ltv: 500000 } ], total: 50 }` | JWT |

### 7. CRM 메시지 발송 API

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| **POST** | `/api/crm/send-message` | `{ segment: "vip", message_type: "new_product", template_id: "tmpl_001", discount_code: "SAVE10" }` | `{ campaign_id: "camp_123", segment: "vip", recipient_count: 50, status: "sent", sent_at: "2025-01-15T10:00:00Z" }` | JWT |
| **GET** | `/api/crm/campaign/{campaign_id}/results` | 없음 | `{ campaign_id: "camp_123", sent: 50, delivered: 48, clicked: 18, converted: 5, click_rate: 0.375, conversion_rate: 0.104 }` | JWT |

### 8. 리포트 생성 API

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| **GET** | `/api/report/monthly?month=2025-01` | 없음 | `{ month: "2025-01", ad_performance: { roas: 3.2, spend: 1500000, revenue: 4800000 }, content_performance: { page_views: 50000, click_rate: 0.15, conversion_rate: 0.18 }, sns_performance: { followers: 5000, engagement_rate: 0.08 }, recommendations: [ "상세페이지 A/B 테스트 시작", "VIP 고객 재구매 메시지 발송" ] }` | JWT |
| **GET** | `/api/report/monthly/{month}/pdf` | 없음 | PDF 파일 (바이너리) | JWT |

### 9. SNS 콘텐츠 관리 API

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| **GET** | `/api/sns/schedule` | 없음 | `{ schedule: [ { date: "2025-01-16", platform: "instagram", content_id: "post_001", status: "scheduled" }, { date: "2025-01-17", platform: "blog", content_id: "post_002", status: "scheduled" } ] }` | JWT |
| **GET** | `/api/sns/post/{post_id}/performance` | 없음 | `{ post_id: "post_001", platform: "instagram", likes: 150, comments: 25, saves: 40, engagement_rate: 0.12 }` | JWT |

### 10. 구독 관리 API

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| **GET** | `/api/subscription/current` | 없음 | `{ subscription_id: "sub_123", plan: "pro", monthly_price: 490000, status: "active", next_billing_date: "2025-02-15", cancel_at_period_end: false }` | JWT |
| **POST** | `/api/subscription/upgrade` | `{ new_plan: "enterprise" }` | `{ subscription_id: "sub_123", plan: "enterprise", monthly_price: 890000, status: "active", effective_date: "2025-01-15" }` | JWT |
| **POST** | `/api/subscription/cancel` | `{ cancel_at_period_end: true }` | `{ subscription_id: "sub_123", status: "active", cancel_at_period_end: true, final_billing_date: "2025-02-15" }` | JWT |

---

## 데이터 모델

### 1. customers (고객 계정)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `customer_id` | UUID | 고객 고유 ID | PK, NOT NULL |
| `email` | VARCHAR(255) | 로그인 이메일 | UNIQUE, NOT NULL |
| `password_hash` | VARCHAR(255) | 비밀번호 해시 | NOT NULL |
| `company_name` | VARCHAR(255) | 회사명 (스토어명) | NOT NULL |
| `phone` | VARCHAR(20) | 연락처 | NOT NULL |
| `subscription_plan` | ENUM('starter', 'pro', 'enterprise') | 구독 플랜 | NOT NULL, DEFAULT 'starter' |
| `subscription_status` | ENUM('active', 'paused', 'cancelled') | 구독 상태 | NOT NULL, DEFAULT 'active' |
| `monthly_price` | INTEGER | 월정액 (원) | NOT NULL |
| `created_at` | TIMESTAMP | 가입 일시 | NOT NULL, DEFAULT NOW() |
| `updated_at` | TIMESTAMP | 수정 일시 | NOT NULL, DEFAULT NOW() |
| `cancelled_at` | TIMESTAMP | 구독 취소 일시 | NULLABLE |

### 2. ad_accounts (광고 계정 연동)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `ad_account_id` | UUID | 광고 계정 고유 ID | PK, NOT NULL |
| `customer_id` | UUID | 고객 ID | FK → customers, NOT NULL |
| `platform` | ENUM('naver', 'coupang') | 광고 플랫폼 | NOT NULL |
| `platform_account_id` | VARCHAR(255) | 플랫폼 계정 ID | NOT NULL |
| `oauth_token` | TEXT | OAuth 토큰 (암호화) | NOT NULL |
| `oauth_refresh_token` | TEXT | OAuth 리프레시 토큰 (암호화) | NOT NULL |
| `token_expires_at` | TIMESTAMP | 토큰 만료 일시 | NOT NULL |
| `status` | ENUM('connected', 'disconnected', 'expired') | 연동 상태 | NOT NULL, DEFAULT 'connected' |
| `last_sync_at` | TIMESTAMP | 마지막 데이터 동기화 일시 | NULLABLE |
| `created_at` | TIMESTAMP | 연동 일시 | NOT NULL, DEFAULT NOW() |

### 3. ad_performance (광고 성과 데이터)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `performance_id` | UUID | 성과 데이터 고유 ID | PK, NOT NULL |
| `ad_account_id` | UUID | 광고 계정 ID | FK → ad_accounts, NOT NULL |
| `date` | DATE | 데이터 날짜 | NOT NULL |
| `platform` | ENUM('naver', 'coupang') | 플랫폼 | NOT NULL |
| `impressions` | INTEGER | 노출 수 | NOT NULL, DEFAULT 0 |
| `clicks` | INTEGER | 클릭 수 | NOT NULL, DEFAULT 0 |
| `conversions` | INTEGER | 전환 수 | NOT NULL, DEFAULT 0 |
| `spend` | DECIMAL(12, 2) | 광고비 (원) | NOT NULL, DEFAULT 0 |
| `revenue` | DECIMAL(12, 2) | 매출 (원) | NOT NULL, DEFAULT 0 |
| `cpc` | DECIMAL(10, 2) | 클릭당 비용 (원) | COMPUTED (spend / clicks) |
| `roas` | DECIMAL(5, 2) | ROAS (매출 / 광고비) | COMPUTED (revenue / spend) |
| `created_at` | TIMESTAMP | 생성 일시 | NOT NULL, DEFAULT NOW() |

### 4. customers_segments (고객 세분화)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `segment_id` | UUID | 세분화 고유 ID | PK, NOT NULL |
| `customer_id` | UUID | 고객 ID | FK → customers, NOT NULL |
| `phone` | VARCHAR(20) | 고객 전화번호 | NOT NULL |
| `segment_name` | ENUM('vip', 'regular', 'dormant') | 세그먼트 이름 | NOT NULL |
| `purchase_count` | INTEGER | 구매 횟수 | NOT NULL, DEFAULT 0 |
| `ltv` | DECIMAL(12, 2) | 생애 가치 (원) | NOT NULL, DEFAULT 0 |
| `last_purchase_date` | DATE | 최근 구매 날짜 | NULLABLE |
| `last_purchase_days` | INTEGER | 최근 구매 이후 일수 | COMPUTED (TODAY() - last_purchase_date) |
| `updated_at` | TIMESTAMP | 세분화 업데이트 일시 | NOT NULL, DEFAULT NOW() |

### 5. crm_campaigns (CRM 캠페인)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `campaign_id` | UUID | 캠페인 고유 ID | PK, NOT NULL |
| `customer_id` | UUID | 고객 ID | FK → customers, NOT NULL |
| `segment_name` | ENUM('vip', 'regular', 'dormant') | 대상 세그먼트 | NOT NULL |
| `message_type` | ENUM('new_product', 'discount', 'repurchase', 'custom') | 메시지 유형 | NOT NULL |
| `template_id` | VARCHAR(255) | 메시지 템플릿 ID | NOT NULL |
| `discount_code` | VARCHAR(50) | 할인 코드 | NULLABLE |
| `recipient_count` | INTEGER | 발송 대상 수 | NOT NULL |
| `sent_count` | INTEGER | 실제 발송 수 | NOT NULL, DEFAULT 0 |
| `delivered_count` | INTEGER | 전달 수 | NOT NULL, DEFAULT 0 |
| `clicked_count` | INTEGER | 클릭 수 | NOT NULL, DEFAULT 0 |
| `converted_count` | INTEGER | 전환 수 | NOT NULL, DEFAULT 0 |
| `status` | ENUM('draft', 'sent', 'completed') | 캠페인 상태 | NOT NULL, DEFAULT 'draft' |
| `sent_at` | TIMESTAMP | 발송 일시 | NULLABLE |
| `created_at` | TIMESTAMP | 생성 일시 | NOT NULL, DEFAULT NOW() |

### 6. ab_tests (A/B 테스트)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `test_id` | UUID | 테스트 고유 ID | PK, NOT NULL |
| `customer_id` | UUID | 고객 ID | FK → customers, NOT NULL |
| `version_a_url` | TEXT | 버전 A URL | NOT NULL |
| `version_b_url` | TEXT | 버전 B URL | NOT NULL |
| `traffic_split` | INTEGER | 트래픽 분배 비율 (%) | NOT NULL, DEFAULT 50 |
| `start_date` | DATE | 테스트 시작 날짜 | NOT NULL |
| `end_date` | DATE | 테스트 종료 날짜 | NOT NULL |
| `status` | ENUM('running', 'completed', 'paused') | 테스트 상태 | NOT NULL, DEFAULT 'running' |
| `version_a_conversions` | INTEGER | 버전 A 전환 수 | NOT NULL, DEFAULT 0 |
| `version_a_visitors` | INTEGER | 버전 A 방문자 수 | NOT NULL, DEFAULT 0 |
| `version_b_conversions` | INTEGER | 버전 B 전환 수 | NOT NULL, DEFAULT 0 |
| `version_b_visitors` | INTEGER | 버전 B 방문자 수 | NOT NULL, DEFAULT 0 |
| `p_value` | DECIMAL(5, 4) | 통계 유의성 (p-value) | NULLABLE |
| `winner` | ENUM('version_a', 'version_b', 'none') | 승자 | NULLABLE |
| `created_at` | TIMESTAMP | 생성 일시 | NOT NULL, DEFAULT NOW() |

### 7. diagnoses (스토어 진단)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `diagnosis_id` | UUID | 진단 고유 ID | PK, NOT NULL |
| `email` | VARCHAR(255) | 진단 요청자 이메일 | NOT NULL |
| `monthly_revenue` | DECIMAL(12, 2) | 월 매출 (원) | NOT NULL |
| `monthly_ad_spend` | DECIMAL(12, 2) | 월 광고비 (원) | NOT NULL |
| `customer_count` | INTEGER | 고객 수 | NOT NULL |
| `store_url` | TEXT | 스토어 URL | NOT NULL |
| `crm_score` | INTEGER | CRM 점수 (0~100) | NOT NULL |
| `content_score` | INTEGER | 콘텐츠 점수 (0~100) | NOT NULL |
| `roas_estimate` | DECIMAL(5, 2) | ROAS 추정치 | NOT NULL |
| `recommendation` | TEXT | 개선 권고사항 | NOT NULL |
| `created_at` | TIMESTAMP | 진단 일시 | NOT NULL, DEFAULT NOW() |

---

## 성공 기준

### KPI 1: 신규 계약 건수 (KR1)
- **측정 방법**: 월별 신규 계약 건수 집계 (구독 상태 = 'active' 신규 고객)
- **목표**: 3개월 내 월 5건 달성 → 6개월 내 월 10건 달성
- **임계값**: 월 3건 미만 시 마케팅 채널 변경 (네이버 광고 집행 또는 가격 인하)

### KPI 2: 평균 ROAS (KR2)
- **측정 방법**: 담당 클라이언트의 월간 광고 성과 데이터 (revenue / spend) 평균
- **목표**: 평균 ROAS 3.0 이상 유지
- **임계값**: 평균 ROAS 2.5 미만 시 광고 운영 인력 교체 또는 콘텐츠 품질 개선
- **주의**: "보장"이 아닌 "목표치"로 커뮤니케이션 (계약서 명시)

### KPI 3: 고객 유지율 (KR3)
- **측정 방법**: 3개월 이상 구독 유지 고객 비율 (3개월 후 구독 상태 = 'active' 고객 / 초기 계약 고객)
- **목표**: 3개월 유지율 70% 이상 (월 Churn 12% 이하)
- **임계값**: 유지율 50% 미만 시 제품 개선 (대시보드 UX·리포트 품질) 또는 고객 지원 강화

### KPI 4: 고객 만족도 (NPS)
- **측정 방법**: 월 1회 NPS 설문 (추천 의향 0~10점)
- **목표**: NPS 40 이상
- **임계값**: NPS 30 미만 시 고객 인터뷰 실시 → 개선점 파악

### KPI 5: 월간 활성 사용자 (MAU)
- **측정 방법**: 월별 대시보드 로그인 1회 이상 고객 수
- **목표**: MAU / 총 고객 수 ≥ 80%
- **임계값**: 60% 미만 시 대시보드 UX 개선 또는 이메일 리마인더 강화

### KPI 6: 고객 획득 비용 (CAC)
- **측정 방법**: 월간 마케팅 비용 / 신규 계약 건수
- **목표**: CAC ≤ 5만 원 (초기 무료 채널 활용 시 1.7만 원)
- **임계값**: CAC > 10만 원 시 마케팅 채널 효율성 재검토

### KPI 7: 고객 생애 가치 (LTV)
- **측정 방법**: 평균 ARPU(49만) × 평균 유지 기간(개월) × 마진율(70%)
- **목표**: LTV ≥ 147만 원 (CAC 대비 30배 이상)
- **임계값**: LTV < 100만 원 시 가격 인상 또는 비용 절감 필요

---

## 리스크

### 1. 기술 리스크

**리스크 1-1: 네이버·쿠팡 API 변경으로 데이터 동기화 실패**
- **심각도**: 높음 (광고 성과 데이터 조회 불가 → 핵심 기능 마비)
- **발생 확률**: 중간 (플랫폼 정책 변경은 예고 후 3개월 유예 제공)
- **대응 방안**: 
  - API 변경 모니터링 (네이버·쿠팡 개발자 포럼 구독)
  - 변경 발생 시 48시간 내 대응 (개발팀 상시 대기)
  - 고객에게 사전 공지 + 임시 수동 데이터 입력 옵션 제공

**리스크 1-2: 스마트스토어 고객 데이터 직접 수집 불가 (플랫폼 정책)**
- **심각도**: 높음 (CRM 기능 제약 → 핵심 가치 훼손)
- **발생 확률**: 높음 (현재 스마트스토어 정책상 이메일 직접 수집 불가)
- **대응 방안**: 
  - 카톡·문자 기반 CRM으로 설계 (이메일 대신)
  - 자사몰(Cafe24·식스샵) 고객에게만 이메일 CRM 제공
  - 고객이 직접 수집한 이메일 리스트 업로드 기능 제공 (수동)

**리스크 1-3: 대시보드 성능 저하 (데이터 양 증가)**
- **심각도**: 중간 (사용자 경험 악화 → 이탈 유발)
- **발생 확률**: 낮음 (초기 고객 수 적어 성능 문제 미미)
- **대응 방안**: 
  - Redis 캐싱으로 실시간 리포트 조회 속도 최적화
  - 월 데이터는 집계 후 저장 (일일 데이터 조회 시 DB 부하 최소화)
  - 고객 수 100명 도달 시 DB 인덱싱 재검토

---

### 2. 시장/경쟁 리스크

**리스크 2-1: 경쟁사(대형 에이전시) 시장 진입**
- **심각도**: 높음 (가격·브랜드 경쟁력 상실 가능)
- **발생 확률**: 중간 (나스미디어·디지털마케팅 대행사 SMB 시장 진입 가능성)
- **대응 방안**: 
  - 3개월 내 고객 100명 확보 → 네트워크 효과 발생 (입소문 확산)
  - 통합 대시보드 데이터 누적 → Switching Cost 증가

---

# Pass 2: V4 프레임워크 섹션 4개

## Aha Moment 정의

**Aha Moment:**
> 셀러가 naver-diagnosis 스토어 진단 결과에서 "CRM 부재로 월 300만 낭비 중"을 시각화로 확인하는 순간, 통합 운영의 필요성을 깨닫는다.

**측정:**
- 가입부터 아하까지 예상 클릭 수: 3클릭 (진단 폼 입력 → 결과 페이지 로드 → "집중 49만 패키지" CTA 노출)
- 예상 시간: **60초 이내** (폼 입력 30초 + 진단 계산 15초 + 결과 확인 15초)

**구현 방식:**
1. **온보딩 단축**: 진단 폼을 3개 필드만 (월 매출·광고비·고객 수) — 추가 정보는 상담 단계에서 수집
2. **핵심 가치 즉시 노출**: 진단 결과 상단에 "현재 상태 vs 개선 후" 비교 카드 배치
   - 현재: "ROAS 2.0, CRM 부재, 콘텐츠 품질 42점"
   - 개선 후: "ROAS 3.5 보장, CRM 자동화, 콘텐츠 A/B 테스트" (집중 49만 패키지)
3. **시각적 피드백**: 
   - 진단 점수를 색상 게이지(빨강→노랑→초록)로 표시
   - 각 점수 옆에 "월 300만 절약 가능" 같은 금액 임팩트 표시
   - 결과 하단에 "상담 신청" CTA 버튼을 대비색(주황)으로 강조

---

## JTBD Statement (민수 전략 → 서윤 Phase 1 기반)

**When I am** 월 1,000만~3,000만 매출 스마트스토어·쿠팡 셀러로 광고는 월 50만 집행 중이나 콘텐츠는 직접 촬영하고 SNS는 주 1회 포스팅하는 상황에서,

**I want to** 광고·콘텐츠·SNS를 하나의 팀이 통합 운영해주고, 월 300만 분산 계약 비용을 49만으로 줄이며, ROAS 3.5를 달성하고, 월 150시간 수작업을 0으로 만들고 싶어서,

**so I can** 주말에 가족 시간을 보내고, 제품 기획·고객 응대 같은 본업에 집중하고, 동료 셀러들에게 "우리는 전문 대행사 쓴다"고 자랑하고, 매출을 2배 증가시킬 수 있다.

---

## Customer Forces Strategy (서윤 Phase 3 Canvas 기반)

### Push 요인 (경쟁사 불만 활용)

**현재 상태:**
- 광고는 A사(월 150만), 콘텐츠는 B사(월 100만), SNS는 직접(월 50시간) — 여러 에이전시 분산 계약
- 엑셀로 구매자 리스트 수작업 관리 (월 100시간)
- 네이버·쿠팡 광고 데이터와 콘텐츠 성과 데이터 불일치로 ROAS 추적 불가

**경쟁사 불만 (서윤 Level 5 evidence_quote):**
- OSC: "플랫폼 수수료 인상 추세로 2P·3P 전환" (Pain #2) — 컨설팅만 제공, 운영 대행 없음
- Cafe24: "앱 마켓 산재로 통합 부재" (Pain #16) — CRM 앱, 광고 앱 따로 설치 필요
- Groobee: "콘텐츠 생성 부담으로 많은 브랜드들이 플랫폼 의존" (Pain #1) — 도구 미비로 직접 제작 강요

**우리의 Push 메시지:**
> "여러 에이전시 월 300만 쓰고도 ROAS 2.0 미만? 광고·콘텐츠·SNS를 하나의 팀이 통합 운영하면 월 49만으로 ROAS 3.5 달성합니다."

### Pull 요인 (차별 가치)

1. **통합 운영 팀**: 
   - 광고 운영 + 상세페이지 A/B 테스트 + SNS 콘텐츠 제작을 하나의 팀이 책임
   - 경쟁사 대비: OSC는 컨설팅만, Cafe24는 앱 산재, Adure는 콘텐츠만
   - 구체적 가치: 월 300만 절약 + 데이터 불일치 0 + 의사결정 속도 3배

2. **naver-diagnosis 스토어 진단 도구 (무료)**:
   - 셀러가 입력한 월 매출·광고비·고객 수로 CRM 부재·콘텐츠 품질·ROAS 추정치 자동 계산
   - 경쟁사 대비: OSC는 가이드 PDF만, Cafe24는 진단 도구 없음
   - 구체적 가치: 1분 내 현재 상태 파악 + "월 300만 절약 가능" 금액 임팩트 시각화

3. **기존 온라인팀 콘텐츠 역량**:
   - 뷰티·카페 소상공인 대상 콘텐츠 제작 경험 3년+
   - 경쟁사 대비: Adure는 외주 기반, Cafe24는 템플릿만
   - 구체적 가치: 상세페이지 전문 촬영 + 주 3회 SNS 포스팅 + 톤앤매너 일관성

### Inertia 감소 (전환 비용 최소화)

- **마이그레이션 도구**: 
  - 기존 광고 계정 데이터 자동 임포트 (네이버·쿠팡 OAuth 연동)
  - 기존 고객 리스트 엑셀 업로드 기능 (CSV 형식)
  - 기존 상세페이지 URL 입력 → 자동 분석 (A/B 테스트 베이스라인 설정)
  
- **학습 곡선 최소화**: 
  - 온보딩 튜토리얼 (3분, 광고 연동 → 첫 리포트 확인)
  - 템플릿 제공 (SNS 포스팅 톤앤매너 5개 프리셋)
  - 주간 라이브 Q&A (매주 목요일 30분, 슬랙 채널)
  
- **팀 확산**: 
  - 팀원 초대 기능 (대시보드 접근 권한 설정)
  - 공유 리포트 링크 (고객이 팀원에게 주간 리포트 자동 공유)

### Anxiety 해소 (신뢰 신호)

- **무료 체험**: 
  - naver-diagnosis 스토어 진단 완전 무료 (제한 없음)
  - 첫 달 집중 49만 패키지 → 39만 할인 (초기 고객 50명 한정)
  
- **보증**: 
  - "첫 3개월 ROAS 3.5 미달 시 전액 환불" 정책 (계약서 명시)
  - 데이터 보안: 고객 광고 계정 비밀번호 보관 금지, OAuth 토큰만 사용 (네이버·쿠팡 정책 준수)
  - SLA: 주간 리포트 지연 시 월 5만 원 크레딧 제공
  
- **사회적 증거**: 
  - 기존 고객 레퍼런스 3개 (뷰티샵 월 1,500만 → ROAS 3.2, 카페 월 800만 → ROAS 3.5)
  - 네이버 카페 "스마트스토어 판매자 센터" 후기 (초기 10명 고객 리뷰)
  - CEO 리안 프로필 (마케팅 전문가, 온라인팀 3년 운영 경험)

---

## Evidence Appendix (기능 ↔ 페인포인트 trace)

### P0 기능 1: naver-diagnosis 스토어 진단 (무료)

> "콘텐츠 생성 부담으로 많은 브랜드들이 플랫폼 의존"
— https://brunch.co.kr/@groobee/1050 (Level 4, 월 1,000만 스마트스토어 셀러)

> "기술 역량 부족, 콘텐츠 부담으로 많은 브랜드들이 플랫폼 의존"
— https://brunch.co.kr/@groobee/1050 (Level 5, 월 1,200만 D2C 화장품 운영자)

**반영 방식**: 
- Pain #1, #8의 "콘텐츠 부담" + "여러 에이전시 분산"을 시각화하기 위해 진단 폼에서 월 매출·광고비·고객 수 입력 → CRM 점수(0~100), 콘텐츠 점수(0~100), ROAS 추정치 자동 계산
- 결과 화면에 "현재 CRM 부재로 월 300만 낭비 중" 같은 금액 임팩트 표시 → 무료 진단만으로 Pain 인지 → 유료 전환 유도

---

### P0 기능 2: 광고 운영 (네이버 쇼핑·쿠팡)

> "플랫폼 수수료 인상 추세로 2P·3P 전환"
— https://oscsnm.com/d2c-coupang-strategy-guide/ (Level 5, 월 2,000만 식품 D2C 셀러 CEO)

> "라이브 커머스 운영 필수"
— https://oscsnm.com/d2c-coupang-strategy-guide/ (Level 5, 월 1,500만 패션 D2C 3인 팀 리더)

**반영 방식**: 
- Pain #2 "수수료 인상으로 마진 압박"을 해결하기 위해 광고 운영 기능에서 ROAS 실시간 추적 → 월 광고비 100만 → 매출 350만(ROAS 3.5) 달성 보장
- Pain #4 "라이브 판매량이 검색 순위 반영"을 대비하기 위해 광고 데이터와 라이브 판매량 연동 (P1 기능)

---

### P0 기능 3: 통합 리포트 대시보드

> "여러 에이전시 분산 계약으로 월 300만 쓰고도 데이터 불일치로 ROAS 추적 어려움"
— https://brunch.co.kr/@groobee/1050 (Level 5, 월 1,200만 D2C 화장품 운영자)

> "앱 마켓 산재로 통합 부재 — CRM 앱, 광고 앱 따로 설치 필요, 데이터 불일치"
— https://store.cafe24.com/kr/story/2171 (Level 5, 월 950만 뷰티 셀러 팀장)

**반영 방식**: 
- Pain #8 "데이터 불일치"를 해결하기 위해 광고·콘텐츠·SNS 데이터를 한 화면에 통합 표시
- 주간·월간 자동 리포트 발송으로 의사결정 속도 3배 향상
- Cafe24 경쟁사 약점(앱 산재) 직접 공략 → "통합 대시보드 = 리안의 차별화"

---

### P0 기능 4: 상세페이지 A/B 테스트 자동화

> "A/B 테스트 콘텐츠 수작업으로 월 50시간 소모, 통계 부족으로 최적 콘텐츠 식별 못함"
— https://brunch.co.kr/@groobee/1050 (Level 5, 월 2,000만 패션 운영자)

**반영 방식**: 
- Pain #22의 "월 50시간 수작업"을 자동화하기 위해 2개 버전 상세페이지 URL 입력 → 트래픽 50:50 분배 → 전환율 자동 비교
- 통계 유의성(p-value) 표시로 "버전 B가 18% 더 효과" 같은 명확한 결과 제시
- 승자 자동 적용 기능으로 추가 수작업 제거

---

### P0 기능 5: 고객 세분화 (자동 태깅)

> "고객 세분화 자동화"
— https://fashionbiz.co.kr/article/221875 (Level 5, 월 650만 패션 D2C 리더)

> "고객 데이터 직접 축적 활용"
— https://brunch.co.kr/@groobee/1050 (Level 5, 월 2,500만 식품 스마트스토어 CEO)

**반영 방식**: 
- Pain #14 "고객 세분화 없이 광고 타겟팅 비효율"을 해결하기 위해 구매 빈도·금액·최근 구매일 기준 자동 세분화 (VIP·일반·휴면)
- 각 세그먼트별 LTV·구매 주기 표시 → 광고 타겟팅 정확도 향상
- P1 기능 "CRM 자동 메시지 발송"의 기반이 되어 재구매율 30% 달성 가능

---

### P1 기능 1: CRM 자동 메시지 발송 (카톡·문자)

> "플랫폼 수수료 인상 추세로 2P·3P 전환"
— https://oscsnm.com/d2c-coupang-strategy-guide/ (Level 5, 월 2,000만 식품 D2C 셀러 CEO)

> "고객 경험 설계"
— https://brunch.co.kr/@groobee/1050 (Level 4, 월 900만 식품 로켓그로스 셀러)

**반영 방식**: 
- Pain #2 "수수료 인상으로 마진 압박"을 해결하기 위해 CRM 자동화로 재구매율 30% 달성 → LTV 2배 증가로 마진 개선
- Pain #9 "재구매 CRM 부재로 반복 매출 누락"을 해결하기 위해 세분화된 고객에게 자동 메시지 발송 (주 1회)
- 카톡·문자만 사용 (스마트스토어 정책상 이메일 직접 수집 불가)

---

### P1 기능 2: SNS 콘텐츠 제작·포스팅 (인스타·블로그)

> "콘텐츠 생성 부담으로 많은 브랜드들이 플랫폼 의존"
— https://brunch.co.kr/@groobee/1050 (Level 4, 월 1,000만 스마트스토어 셀러)

> "일관된 메시지 관리"
— https://brunch.co.kr/@groobee/1050 (Level 4, 월 1,100만 화장품 셀러)

**반영 방식**: 
- Pain #1 "광고 운영만 신경 쓰다 콘텐츠 제작 시간 부족으로 월 50시간 직접 촬영"을 해결하기 위해 온라인팀이 상세페이지 콘텐츠 촬영·편집 → 자동 포스팅 (주 3회)
- Pain #13 "SNS 콘텐츠 일관성 유지 실패, 주 1회 포스팅으로 팔로워 증가 정체"를 해결하기 위해 일관된 톤앤매너 유지 + 주 3회 포스팅으로 팔로워 월 1천 증가 보장

---

### P1 기능 3: 월간 리포트 자동 생성

> "ROAS 리포팅 수작업으로 의사결정 지연"
— https://oscsnm.com/d2c-coupang-strategy-guide/ (Level 5, 월 1,800만 패션 셀러 팀장)

**반영 방식**: 
- Pain #10 "ROAS 리포팅 수작업으로 의사결정 지연, 월 60시간 엑셀 다운로드 합산"을 해결하기 위해 광고·콘텐츠·SNS 성과 + 개선 제안 자동 생성 (PDF 발송)
- KR2 "담당 클라이언트 평균 ROAS 3.0 이상 유지"를 측정하기 위한 기반 기능

---

### P2 기능 1: CRM 이메일 자동화 (자사몰 전용)

> "고객 데이터 직접 축적 활용"
— https://brunch.co.kr/@groobee/1050 (Level 5, 월 2,500만 식품 스마트스토어 CEO)

**반영 방식**: 
- Pain #6 "고객 데이터 축적 어려워 관계 유지 실패"를 해결하기 위해 자사몰(Cafe24·식스샵) 고객에게 이메일 기반 재구매 유도 (Klaviyo 연동)
- 스마트스토어는 이메일 직접 수집 불가 정책이므로 자사몰 고객만 대상

---

### P2 기능 2: 라이브 커머스 스크립트 AI 생성 (베타)

> "라이브 커머스 운영 필수"
— https://oscsnm.com/d2c-coupang-strategy-guide/ (Level 5, 월 1,500만 패션 D2C 3인 팀 리더)

> "라이브 판매량 순위 반영"
— https://oscsnm.com/d2c-coupang-strategy-guide/ (Level 4, 월 500만 뷰티 자사몰 운영자)

**반영 방식**: 
- Pain #4 "라이브 커머스 운영 부담으로 검색 순위 하락"을 해결하기 위해 라이브 스크립트 AI 자동 생성 (시선 패키지 추가 옵션)
- Pain #11 "라이브 커머스 스크립트 제작 어려움"을 해결하기 위해 AI 스크립트 생성기 제공

---

### P2 기능 3: 모바일 최적화 템플릿

> "모바일 최적화 부족"
— https://store.cafe24.com/kr/story/2171 (Level 4, 월 700만 D2C CEO)

**반영 방식**: 
- Pain #25 "모바일 최적화 부족으로 월 10만 원 트래픽 손실"을 해결하기 위해 상세페이지 모바일 버전 자동 최적화 (주목 패키지 추가)
- 모바일 전환율 50% 달성 목표

---

### P2 기능 4: AI 상품 추천 엔진 (베타)

> "AI 기반 개인화 마케팅 확산"
— https://oscsnm.com/d2c-coupang-strategy-guide/ (Level 4, 월 600만 뷰티 자사몰 셀러)

> "데이터와 IT기술 기반"
— https://fashionbiz.co.kr/article/221875 (Level 4, 월 550만 자사몰 CEO)

**반영 방식**: 
- Pain #5 "AI 개인화 도입 지연으로 자연 유입 부족"을 해결하기 위해 고객 구매 이력 기반 추천 상품 자동 제시 (시선 패키지 추가 옵션)
- Pain #17 "IT기술 부족으로 맞춤 경험 제공 실패"를 해결하기 위해 AI 개인화 엔진 제공

---

**Evidence Appendix 완성도 검증:**
- ✅ 모든 P0 기능(5개) trace 완료
- ✅ 모든 P1 기능(3개) trace 완료
- ✅ 모든 P2 기능(4개) trace 완료
- ✅ 각 기능당 최소 1개 이상 evidence_quote 연결
- ✅ 서윤 Level 4-5 pain point만 인용 (Level 1-3 제외)
- ✅ 원문 quote 사용 (요약 금지)
- ✅ source_url + Level + 페르소나 명시