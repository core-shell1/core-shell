# PRD: 이커머스 셀러 통합 마케팅 대행 플랫폼

## 제품 개요
스마트스토어·쿠팡·자사몰 운영 셀러(월 매출 500만~3,000만 원)를 위한 광고·콘텐츠·CRM 통합 운영 대행 서비스. 기존 주목/집중/시선 패키지 구조를 이커머스 버티컬에 재포장하여 제공.

---

## 기술 스택

| 계층 | 선택 | 이유 |
|------|------|------|
| **FE** | React 18 + TypeScript + TailwindCSS | 기존 온라인팀 스택 재사용, 빠른 개발 |
| **BE** | Node.js (Express) + TypeScript | 기존 인프라 호환, 마케팅 자동화 라이브러리 풍부 |
| **DB** | PostgreSQL (주) + Redis (캐시) | 클라이언트 데이터 정규화, 실시간 대시보드 캐싱 |
| **인프라** | AWS EC2 + RDS + CloudFront | 기존 배포 환경 그대로, 스케일링 용이 |
| **외부 API** | Naver Shopping API, Coupang API, Kakao Sync | 플랫폼별 광고·주문 데이터 수집 |
| **자동화** | Node-cron + Bull (Job Queue) | 일일/주간 리포트 자동 생성, CRM 자동 발송 |

---

## 기능 목록

> **P0** = MVP 필수 (1차 출시, 2개월)  
> **P1** = 1차 출시 후 (3~6개월)  
> **P2** = 나중에 (6개월 이후)  
> **의존성**: 기능 간 선행 조건 명시

| 우선순위 | 기능 | 설명 | 이유 | 의존 기능 |
|---------|------|------|------|---------|
| **P0** | 클라이언트 온보딩 (API 연동) | 스마트스토어·쿠팡·자사몰 API 키 입력 → 자동 데이터 동기화 | 광고·주문 데이터 수집이 모든 기능의 기초 | 없음 |
| **P0** | 통합 대시보드 (읽기 전용) | 광고비·ROAS·주문·고객 수를 한 화면에 표시 (일일 갱신) | 셀러가 "한눈에 보는" 가치 체감 필수 | 클라이언트 온보딩 |
| **P0** | naver-diagnosis 리포트 통합 | 기존 진단 리포트 → 유료 패키지 CTA 추가 | 영업 훅으로 기존 자산 활용 | 없음 |
| **P0** | 패키지 구매 & 결제 (Stripe/토스) | 주목(29만)/집중(49만)/시선(89만) 월정액 결제 | 수익화 필수 | 없음 |
| **P0** | 기본 CRM (재구매 고객 리스트) | 지난 30일 구매자 자동 추출 + 이메일/카톡 발송 템플릿 | 집중 패키지의 핵심 기능 | 클라이언트 온보딩 |
| **P1** | 광고 성과 분석 리포트 (주간) | 채널별(스마트스토어/쿠팡) ROAS·CPC·전환율 자동 계산 | 셀러의 "ROAS 불안정" Pain 직접 해결 | 통합 대시보드 |
| **P1** | 콘텐츠 제작 가이드 (자동 생성) | 상품 정보 → 상세페이지 작성 체크리스트 자동 생성 | 콘텐츠 제작 시간 단축, 품질 표준화 | 클라이언트 온보딩 |
| **P1** | CRM 자동화 (세그먼트 기반) | 구매 금액/빈도별 고객 세그먼트 → 자동 이메일 시퀀스 | 재구매율 증가, 대행팀 수작업 감소 | 기본 CRM |
| **P1** | 클라이언트 포털 (쓰기 권한) | 셀러가 광고 예산·콘텐츠 승인·CRM 메시지 직접 수정 | 셀러 자율성 증가 → 만족도 상승 | 통합 대시보드 |
| **P2** | AI 기반 광고 최적화 제안 | 과거 ROAS 데이터 → 예산 재배분 제안 (수동 승인) | 고급 기능, 시선 패키지 차별화 | 광고 성과 분석 리포트 |
| **P2** | 예측 분석 (매출 예측) | 지난 3개월 데이터 → 다음 달 예상 매출 시뮬레이션 | 셀러의 재고·예산 계획 지원 | 통합 대시보드 |
| **P2** | 멀티 채널 광고 자동 입찰 | 스마트스토어·쿠팡 광고 예산 자동 분배 (AI 기반) | 운영 자동화, 시선 패키지 프리미엄 기능 | CRM 자동화 |

---

## Must NOT (범위 외)

- **자체 광고 플랫폼 구축** — 스마트스토어·쿠팡 API 연동만 수행, 광고 직접 운영 불가 (플랫폼 정책 위반)
- **콘텐츠 AI 자동 생성** — 법적 책임 문제, P1 가이드 생성으로 충분
- **고객 데이터 판매/공유** — PIPA 준수, 클라이언트 데이터는 절대 제3자 공유 금지
- **국제 확장** — 한국 플랫폼(스마트스토어·쿠팡) 전용, 글로벌 D2C는 향후 검토
- **실시간 광고 입찰 자동화** (P0/P1) — 초기 단계에서는 제안만 제공, 자동 실행은 P2 이후

---

## User Flow

### 시나리오 1: 신규 셀러 가입 → 첫 대시보드 확인
1단계: 셀러가 naver-diagnosis 무료 진단 리포트 수신 → "광고+콘텐츠+CRM 통합 운영 49만 원" CTA 클릭  
2단계: 랜딩 페이지 → "지금 신청" 버튼 → 회원가입 (이메일/휴대폰)  
3단계: 패키지 선택 (주목/집중/시선) → Stripe 결제 완료  
4단계: 온보딩 페이지 → 스마트스토어 API 키 입력 (또는 쿠팡/자사몰)  
5단계: "데이터 동기화 중..." (2~5분) → 통합 대시보드 자동 로드  
6단계: 대시보드에서 광고비·ROAS·주문·고객 수 한눈에 확인  
**시스템 응답**: 실시간 데이터 표시, 일일 자동 갱신 설정 완료

### 시나리오 2: 집중 패키지 구매 후 CRM 첫 발송
1단계: 셀러가 대시보드 → "CRM" 탭 클릭  
2단계: "지난 30일 구매자" 자동 추출 리스트 확인 (예: 127명)  
3단계: 템플릿 선택 (재구매 유도 이메일 3가지) → 메시지 수정 (선택)  
4단계: "지금 발송" 또는 "예약 발송" 선택 → 확인  
5단계: 발송 완료 → 대시보드에 "발송 완료: 127명, 열람율 대기 중" 표시  
**시스템 응답**: 이메일 발송 로그 저장, 24시간 후 열람율·클릭율 자동 계산

### 시나리오 3: 주간 광고 성과 리포트 자동 수신
1단계: 매주 월요일 오전 9시 → 셀러 이메일로 "지난주 광고 성과 리포트" 자동 발송  
2단계: 리포트 내용: 채널별(스마트스토어/쿠팡) ROAS·CPC·전환율·추천 액션  
3단계: 셀러가 리포트 링크 클릭 → 대시보드 "분석" 탭으로 이동  
4단계: 상세 차트 확인 → "광고 예산 조정 제안" 버튼 (P1)  
**시스템 응답**: 자동 리포트 생성 및 발송, 데이터 기반 제안 제시

---

## 화면 명세

| 화면명 | URL/Route | 핵심 컴포넌트 | 동작 |
|--------|-----------|-------------|------|
| **랜딩 페이지** | `/` | 헤더, 히어로 섹션, 패키지 카드 3개, FAQ, CTA 버튼 | 패키지 선택 → 회원가입 페이지로 이동 |
| **회원가입** | `/signup` | 이메일/휴대폰 입력, 패스워드, 약관 동의, 제출 버튼 | 입력 검증 → DB 저장 → 온보딩 페이지로 리다이렉트 |
| **온보딩 (API 연동)** | `/onboarding` | 플랫폼 선택 (스마트스토어/쿠팡/자사몰), API 키 입력 필드, "연동 시작" 버튼, 진행 상황 표시 | API 키 검증 → 데이터 동기화 시작 → 완료 후 대시보드로 이동 |
| **통합 대시보드** | `/dashboard` | 상단: 광고비·ROAS·주문·고객 수 카드 (4개), 하단: 시계열 차트 (광고비 vs 매출), 최근 주문 테이블 | 일일 자동 갱신, 날짜 범위 선택 가능, 채널별 필터링 |
| **광고 분석** | `/dashboard/ads` | 채널별 탭 (스마트스토어/쿠팡), 테이블: 캠페인명·광고비·클릭·전환·ROAS, 시계열 차트 | 날짜 범위 선택, 캠페인 클릭 → 상세 페이지 (P1) |
| **CRM** | `/dashboard/crm` | 탭: "고객 리스트" / "발송 이력" / "템플릿", 고객 리스트 테이블 (이름·구매금액·구매일·상태), "새 발송" 버튼 | 고객 선택 → 템플릿 선택 → 메시지 수정 → 발송 |
| **CRM 템플릿** | `/dashboard/crm/templates` | 템플릿 카드 3~5개 (재구매 유도, 신상품 안내, 할인 쿠폰 등), 각 카드에 "사용" 버튼 | 템플릿 선택 → 메시지 에디터로 이동 |
| **CRM 메시지 에디터** | `/dashboard/crm/compose` | 제목·본문 텍스트 에디터, 변수 삽입 버튼 ({고객명}, {구매금액} 등), 미리보기, "발송" / "예약" 버튼 | 메시지 작성 → 발송 또는 예약 설정 → 확인 |
| **콘텐츠 가이드** | `/dashboard/content` | 상품 선택 드롭다운, "가이드 생성" 버튼, 생성된 체크리스트 (상세페이지 작성 항목 10~15개) | 상품 선택 → 가이드 자동 생성 → PDF 다운로드 (P1) |
| **클라이언트 포털** | `/client` | 대시보드 (읽기), 광고 예산 조정 폼, 콘텐츠 승인 큐, CRM 메시지 수정 폼 | 셀러가 직접 수정 → 대행팀에 알림 (P1) |
| **설정** | `/settings` | 계정 정보, 플랫폼 연동 관리 (API 키 재설정), 청구 정보, 패키지 변경, 구독 취소 | 정보 수정 → 저장, 패키지 변경 → 결제 프로세스 |
| **naver-diagnosis 리포트** | `/report/{reportId}` | 진단 결과 (기존 형식 유지), 하단에 "광고+콘텐츠+CRM 통합 운영 49만 원 — 지금 신청" CTA 배너 | CTA 클릭 → 랜딩 페이지로 이동 |

---

## API 명세

### 1. 인증 & 계정

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/auth/signup` | `{ email, password, phone, packageId }` | `{ userId, token, expiresIn }` | 없음 |
| POST | `/api/auth/login` | `{ email, password }` | `{ userId, token, expiresIn }` | 없음 |
| POST | `/api/auth/logout` | `{}` | `{ success: true }` | Bearer Token |
| GET | `/api/auth/me` | 없음 | `{ userId, email, phone, packageId, createdAt }` | Bearer Token |

### 2. 온보딩 & 플랫폼 연동

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/onboarding/platforms` | `{ platform: "smartstore" \| "coupang" \| "custom", apiKey, apiSecret }` | `{ platformId, status: "connecting", syncStartedAt }` | Bearer Token |
| GET | `/api/onboarding/platforms/:platformId` | 없음 | `{ platformId, platform, status: "connected" \| "failed", lastSyncAt, dataCount }` | Bearer Token |
| POST | `/api/onboarding/sync` | `{ platformId }` | `{ syncId, status: "in_progress", estimatedTime: 300 }` | Bearer Token |
| GET | `/api/onboarding/sync/:syncId` | 없음 | `{ syncId, status: "completed" \| "failed", completedAt, recordsImported }` | Bearer Token |

### 3. 대시보드 데이터

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/dashboard/summary` | `{ startDate, endDate, platformId? }` | `{ totalAdSpend, totalRevenue, roas, orderCount, customerCount, period }` | Bearer Token |
| GET | `/api/dashboard/timeseries` | `{ startDate, endDate, granularity: "daily" \| "weekly", platformId? }` | `{ data: [{ date, adSpend, revenue, roas }, ...] }` | Bearer Token |
| GET | `/api/dashboard/orders` | `{ limit: 10, offset: 0, platformId? }` | `{ orders: [{ orderId, date, amount, platform, status }, ...], total }` | Bearer Token |

### 4. 광고 분석

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/ads/campaigns` | `{ platformId, startDate, endDate }` | `{ campaigns: [{ campaignId, name, adSpend, clicks, conversions, roas }, ...] }` | Bearer Token |
| GET | `/api/ads/campaigns/:campaignId` | 없음 | `{ campaignId, name, platform, adSpend, clicks, conversions, roas, dailyData: [...] }` | Bearer Token |
| GET | `/api/ads/report/weekly` | `{ platformId, weekOf }` | `{ report: { channels: [...], summary, recommendations: [...] }, generatedAt }` | Bearer Token |

### 5. CRM

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/crm/customers` | `{ limit: 50, offset: 0, segment?: "repeat" \| "new" }` | `{ customers: [{ customerId, name, email, phone, totalSpent, lastPurchaseDate, purchaseCount }, ...], total }` | Bearer Token |
| GET | `/api/crm/customers/:customerId` | 없음 | `{ customerId, name, email, phone, purchaseHistory: [...], lastInteraction }` | Bearer Token |
| GET | `/api/crm/templates` | 없음 | `{ templates: [{ templateId, name, subject, body, variables: [...] }, ...] }` | Bearer Token |
| POST | `/api/crm/messages/send` | `{ templateId, customerIds: [...], customizations?: { subject, body } }` | `{ messageId, status: "sent", recipientCount, sentAt }` | Bearer Token |
| POST | `/api/crm/messages/schedule` | `{ templateId, customerIds: [...], scheduledFor, customizations? }` | `{ messageId, status: "scheduled", scheduledFor }` | Bearer Token |
| GET | `/api/crm/messages/:messageId` | 없음 | `{ messageId, status, recipientCount, openCount, clickCount, openRate, clickRate }` | Bearer Token |

### 6. 콘텐츠

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/content/products` | `{ limit: 20, offset: 0 }` | `{ products: [{ productId, name, category, imageUrl }, ...], total }` | Bearer Token |
| POST | `/api/content/guide` | `{ productId }` | `{ guideId, productId, checklist: [{ item, description, completed: false }, ...], generatedAt }` | Bearer Token |
| GET | `/api/content/guide/:guideId` | 없음 | `{ guideId, productId, checklist: [...], updatedAt }` | Bearer Token |

### 7. 결제 & 구독

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/billing/checkout` | `{ packageId: "starter" \| "pro" \| "enterprise" }` | `{ sessionId, checkoutUrl, expiresIn: 1800 }` | Bearer Token |
| GET | `/api/billing/subscription` | 없음 | `{ subscriptionId, packageId, status: "active" \| "cancelled", currentPeriodStart, currentPeriodEnd, nextBillingDate }` | Bearer Token |
| POST | `/api/billing/subscription/change` | `{ newPackageId }` | `{ subscriptionId, newPackageId, effectiveDate, prorationCredit }` | Bearer Token |
| POST | `/api/billing/subscription/cancel` | `{ reason? }` | `{ subscriptionId, status: "cancelled", cancelledAt, refundAmount? }` | Bearer Token |

### 8. 관리자 (대행팀용, 별도 인증)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/admin/clients` | `{ limit: 50, offset: 0, status?: "active" \| "cancelled" }` | `{ clients: [{ clientId, name, packageId, createdAt, lastActiveAt, status }, ...], total }` | Admin Token |
| GET | `/api/admin/clients/:clientId/performance` | `{ startDate, endDate }` | `{ clientId, revenue, adSpend, roas, crmMetrics: { emailsSent, openRate, clickRate } }` | Admin Token |
| POST | `/api/admin/clients/:clientId/notes` | `{ note }` | `{ noteId, clientId, note, createdAt, createdBy }` | Admin Token |

---

## 데이터 모델

### users
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | UUID | 사용자 고유 ID | PK |
| email | VARCHAR(255) | 이메일 | UNIQUE, NOT NULL |
| passwordHash | VARCHAR(255) | 해시된 비밀번호 | NOT NULL |
| phone | VARCHAR(20) | 휴대폰 번호 | UNIQUE |
| packageId | ENUM | 구독 패키지 | "starter" \| "pro" \| "enterprise" |
| subscriptionStatus | ENUM | 구독 상태 | "active" \| "cancelled" \| "suspended" |
| createdAt | TIMESTAMP | 가입 일시 | DEFAULT NOW() |
| updatedAt | TIMESTAMP | 수정 일시 | DEFAULT NOW() |

### platforms
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | UUID | 플랫폼 연동 ID | PK |
| userId | UUID | 사용자 ID | FK → users.id |
| platform | ENUM | 플랫폼 종류 | "smartstore" \| "coupang" \| "custom" |
| apiKey | VARCHAR(255) | API 키 (암호화) | NOT NULL |
| apiSecret | VARCHAR(255) | API 시크릿 (암호화) | NOT NULL |
| status | ENUM | 연동 상태 | "connected" \| "failed" \| "expired" |
| lastSyncAt | TIMESTAMP | 마지막 동기화 시간 | NULL 가능 |
| createdAt | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

### campaigns
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | UUID | 캠페인 ID | PK |
| platformId | UUID | 플랫폼 ID | FK → platforms.id |
| externalCampaignId | VARCHAR(255) | 외부 플랫폼 캠페인 ID | NOT NULL |
| name | VARCHAR(255) | 캠페인명 | NOT NULL |
| adSpend | DECIMAL(12,2) | 광고비 (누적) | DEFAULT 0 |
| clicks | INT | 클릭 수 | DEFAULT 0 |
| conversions | INT | 전환 수 | DEFAULT 0 |
| revenue | DECIMAL(12,2) | 매출 | DEFAULT 0 |
| roas | DECIMAL(5,2) | ROAS (revenue/adSpend) | COMPUTED |
| syncedAt | TIMESTAMP | 마지막 동기화 | DEFAULT NOW() |

### daily_metrics
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | UUID | 메트릭 ID | PK |
| platformId | UUID | 플랫폼 ID | FK → platforms.id |
| date | DATE | 날짜 | NOT NULL |
| adSpend | DECIMAL(12,2) | 일일 광고비 | DEFAULT 0 |
| clicks | INT | 일일 클릭 | DEFAULT 0 |
| conversions | INT | 일일 전환 | DEFAULT 0 |
| revenue | DECIMAL(12,2) | 일일 매출 | DEFAULT 0 |
| orderCount | INT | 일일 주문 수 | DEFAULT 0 |
| uniqueCustomers | INT | 신규 고객 수 | DEFAULT 0 |
| UNIQUE(platformId, date) | | 플랫폼별 일일 데이터 중복 방지 | |

### customers
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | UUID | 고객 ID | PK |
| platformId | UUID | 플랫폼 ID | FK → platforms.id |
| externalCustomerId | VARCHAR(255) | 외부 플랫폼 고객 ID | NOT NULL |
| name | VARCHAR(255) | 고객명 | NOT NULL |
| email | VARCHAR(255) | 이메일 | NULL 가능 |
| phone | VARCHAR(20) | 휴대폰 | NULL 가능 |
| totalSpent | DECIMAL(12,2) | 누적 구매액 | DEFAULT 0 |
| purchaseCount | INT | 구매 횟수 | DEFAULT 0 |
| lastPurchaseDate | DATE | 마지막 구매일 | NULL 가능 |
| segment | ENUM | 고객 세그먼트 | "new" \| "repeat" \| "vip" (자동 계산) |
| createdAt | TIMESTAMP | 첫 구매일 | DEFAULT NOW() |

### crm_messages
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | UUID | 메시지 ID | PK |
| userId | UUID | 사용자 ID | FK → users.id |
| templateId | UUID | 템플릿 ID | FK → crm_templates.id |
| status | ENUM | 발송 상태 | "draft" \| "sent" \| "scheduled" \| "failed" |
| recipientCount | INT | 수신자 수 | DEFAULT 0 |
| sentAt | TIMESTAMP | 발송 시간 | NULL 가능 |
| scheduledFor | TIMESTAMP | 예약 시간 | NULL 가능 |
| openCount | INT | 열람 수 | DEFAULT 0 |
| clickCount | INT | 클릭 수 | DEFAULT 0 |
| createdAt | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

### crm_templates
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | UUID | 템플릿 ID | PK |
| userId | UUID | 사용자 ID | FK → users.id |
| name | VARCHAR(255) | 템플릿명 | NOT NULL |
| subject | VARCHAR(255) | 이메일 제목 | NOT NULL |
| body | TEXT | 이메일 본문 | NOT NULL |
| variables | JSON | 변수 목록 | `["customerName", "purchaseAmount", ...]` |
| createdAt | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

### subscriptions
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| id | UUID | 구독 ID | PK |
| userId | UUID | 사용자 ID | FK → users.id |
| packageId | ENUM | 패키지 | "starter" \| "pro" \| "enterprise" |
| status | ENUM | 상태 | "active" \| "cancelled" \| "suspended" |
| currentPeriodStart | DATE | 현재 기간 시작 | NOT NULL |
| currentPeriodEnd | DATE | 현재 기간 종료 | NOT NULL |
| nextBillingDate | DATE | 다음 청구일 | NOT NULL |
| cancelledAt | TIMESTAMP | 취소 일시 | NULL 가능 |
| createdAt | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

---

## 성공 기준

### KPI (측정 가능)

| KPI | 목표치 | 측정 방법 | 측정 주기 |
|-----|--------|---------|---------|
| **신규 계약 수** | 월 5건 (3개월 내) | naver-diagnosis 리포트 CTA 클릭 → 유료 전환 추적 | 주간 |
| **평균 계약 단가** | 49만 원 이상 유지 | 집중 패키지 선택 비율 ≥ 60% | 월간 |
| **3개월 리텐션율** | ≥ 70% (해지율 ≤ 30%) | 구독 활성 상태 추적 (subscriptions.status = "active") | 월간 |
| **대시보드 일일 활성 사용자** | 계약 고객의 ≥ 60% | 로그인 기록 (auth.me 호출) | 일간 |
| **CRM 발송 활성도** | 계약 고객의 ≥ 50%가 월 1회 이상 발송 | crm_messages.sentAt 기록 | 월간 |
| **광고 성과 리포트 열람율** | ≥ 40% | 이메일 열람 추적 (crm_messages.openCount) | 주간 |
| **Gross Margin** | ≥ 70% (초기), 실제 검증 후 조정 | (월 수익 - 변동비) / 월 수익 | 월간 |
| **CAC (고객 획득 비용)** | ≤ 10만 원 | 마케팅 비용 / 신규 계약 수 | 월간 |
| **LTV/CAC 비율** | ≥ 3 | LTV(120만 원) / CAC | 분기 |
| **월 Churn율** | ≤ 5% | (취소 고객 수 / 월초 활성 고객 수) × 100 | 월간 |

### 비즈니스 마일스톤

| 마일스톤 | 목표 | 기한 | 성공 판정 |
|---------|------|------|---------|
| **MVP 출시** | P0 기능 완성 (온보딩, 대시보드, CRM, 결제) | 2개월 | 내부 테스트 완료, 버그 0건 |
| **첫 10개 계약** | 신규 고객 확보 | 3개월 | 월 490만 원 매출 달성 |
| **3개월 리텐션 70%** | 해지율 30% 이하 | 6개월 | 구독 활성 고객 7명 이상 유지 |
| **월 매출 1,000만 원** | 20개 계약 (평균 50만 원) | 9개월 | 월간 신규 5건 + 리텐션 70% |
| **P1 기능 출시** | 광고 분석, CRM 자동화, 클라이언트 포털 | 6개월 | 기능별 테스트 완료 |

---

## 리스크

### 1. 단위경제 실패 (하은 반론 기반)

**리스크**: 초기 추정 Gross Margin 70%는 낙관적. 실제 대행팀 인건비(월 200만~300만 원/명) 반영 시 마진 40~50%로 하락 가능.

**대응 방안**:
- **첫 5건 계약의 실제 투입 시간·인건비 추적** (주간 단위) → 실제 원가 계산
- 마진이 50% 이하면 → 가격 인상(59만 원) 또는 서비스 범위 축소 (CRM 제외)
- 자동화 우선: CRM 템플릿 표준화, 리포트 자동 생성으로 수작업 최소화

---

### 2. 가치 실패 (통합 운영의 실제 성과 미검증)

**리스크**: "광고+콘텐츠+CRM 통합"이 실제로 매출 증가를 가져오는지 미검증. 셀러가 "개별 서비스가 더 낫다"고 판단할 수 있음.

**대응 방안**:
- **첫 3개 클라이언트를 케이스 스터디로 제작** (3개월 내)
  - 계약 전 ROAS·재구매율 측정 → 3개월 후 재측정 → 성과 리포트 작성
  - 성과 미달 시 → 환불 또는 무료 연장 (신뢰 구축)
- **성과 보장 조건부 계약**: "3개월 내 ROAS 20% 미달 시 50% 환불" 옵션 제공
- 초기 고객 선정: 이미 광고를 돌리고 있는 셀러 (ROAS 개선 가능성 높음)

---

### 3. 전환 실패 (메시지 복잡성, 클로징 저항)

**리스크**: "광고+콘텐츠+CRM 통합" 메시지가 복잡해 셀러가 이해하지 못하거나, 개별 서비스 대비 가치를 못 느낄 수 있음.

**대응 방안**:
- **Pain 하나로 진입 훅 단순화**: 초기 영업은 "ROAS 불안정 해결" 하나만 강조
  - naver-diagnosis 리포트 → "광고 성과 분석 무료 진단" CTA
  - 콘텐츠·CRM은 온보딩 후 업셀로 연결
- **naver-diagnosis 기반 자동 진단 리포트 고도화**
  - 현재: 진단 결과만 제공 → 개선: 진단 결과 + "이 문제를 해결하려면 광고 최적화 + 재구매 자동화가 필요" 맞춤 제안
  - 리포트 말미에 "49만 원 집중 패키지 — 첫 달 무료 진단 포함" CTA 배치
- **초기 고객 인터뷰 강화**: 전환 실패 사례 수집 → 메시지 개선

---

### 4. 도달 실패 (타겟 셀러 커뮤니티 접근 경로 미검증)

**리스크**: 스마트스토어·쿠팡 셀러 커뮤니티에 접근하지 못하거나, 스팸으로 낙인찍혀 신뢰 상실 가능.

**대응 방안**:
- **네이버 카페 + 카카오 오픈채팅 직접 아웃리치** (48시간 검증 단계)
  - 스팸 아닌 "가치 제공형" 콘텐츠: "ROAS 무료 진단 리포트" 게시
  - 카페 규칙 준수 (광고 금지 카페는 댓글 형태로 도움말 제공)
- **기존 소상공인 클라이언트 레퍼럴 활용**
  - 기존 고객에게 "이커머스 셀러 친구 추천 시 1개월 무료" 인센티브
  - 입소문 기반 신뢰도 높은 리드 확보
- **인플루언서 협업** (중기, 3~6개월)
  - 스마트스토어 유튜버·블로거와 협업 → 리뷰 콘텐츠 제작

---

### 5. 타이밍 실패 (경쟁사 선점, 긴급 트리거 부재)

**리스크**: 외부 긴급 트리거(규제 변화, 플랫폼 정책 변경)가 없어 시장 진입 시간이 느슨할 수 있음. 경쟁사가 먼저 통합 패키지 출시 가능.

**대응 방안**:
- **12~18개월 선점 창 존재** — 현재 경쟁사(에코마케팅, 카페24)는 단일 기능만 제공
- **3개월 내 10건 계약 달성 필수**: 포지셔닝 "통합 대행 선두주자" 고착화
- **분기별 경쟁사 모니터링**: 새로운 통합 패키지 출시 감지 → 즉시 차별화 기능 추가 (P1 기능 가속화)

---

### 6. 기술 리스크 (API 연동 실패, 데이터 동기화 오류)

**리스크**: 스마트스토어·쿠팡 API 변경 또는 인증 실패 → 데이터 동기화 중단 → 대시보드 공백.

**대응 방안**:
- **API 모니터링 자동화**: 일일 동기화 실패 감지 → 관리자 알림 + 자동 재시도 (3회)
- **Fallback 메커니즘**: API 실패 시 → 마지막 성공 데이터 표시 + "데이터 동기화 중 오류" 경고 배너
- **플랫폼별 API 문서 정기 검토**: 분기별 API 변경사항 확인 → 사전 대응
- **고객 지원 SLA**: API 오류 발생 시 24시간 내 해결 약속

---

### 7. 규정 리스크 (개인정보보호법, 이메일 마케팅 규정)

**리스크**: CRM 이메일 발송 시 PIPA(개인정보보호법) 위반 또는 스팸 메일 신고 → 법적 책임.

**대응 방안**:
- **CRM 메시지 발송 전 동의 확인**: 고객 이메일 수집 시 "마케팅 이메일 수신 동의" 필수 체크
- **Unsubscribe 링크 자동 삽입**: 모든 이메일에 "수신 거부" 링크 포함 (법적 필수)
- **발송 로그 기록**: 모든 CRM 메시지 발송 기록 저장 (감시 대비)
- **약관 & 개인정보처리방침 명시**: 서비스 약관에 "고객 데이터는 절대 제3자 공유 금지" 명시

---

### 8. 조직 리스크 (대행팀 역량 부족, 스케일링 어려움)

**리스크**: 초기 10명 고객 관리는 가능하지만, 월 20명 이상 확보 시 대행팀 인력 부족 → 서비스 품질 저하 → 리텐션 악화.

**대응 방안**:
- **자동화 우선**: CRM 템플릿 표준화, 리포트 자동 생성으로 수작업 최소화
- **채용 계획**: 월 10건 계약 달성 시 → 마케팅 담당자 1명 추가 채용
- **프로세스 표준화**: 온보딩·리포팅·CRM 발송 체크리스트 작성 → 신입 교육 시간 단축

---

### 9. 데이터 품질 리스크 (API 데이터 불일치, 중복 고객)

**리스크**: 스마트스토어·쿠팡 API에서 수집한 데이터가 불일치하거나, 같은 고객이 중복 등록될 수 있음 → 대시보드 신뢰도 하락.

**대응 방안**:
- **데이터 검증 로직**: 동기화 후 자동 검증 (광고비 합계 vs 플랫폼 공식 수치 비교)
- **고객 중복 제거**: 이메일·휴대폰 기반 중복 고객 자동 병합
- **데이터 품질 대시보드**: 관리자 페이지에 "동기화 오류율", "중복 고객 수" 실시간 표시

---

### 10. 경쟁 리스크 (대형 플랫폼의 자체 마케팅 도구 출시)

**리스크**: 네이버·쿠팡이 자체 마케팅 통합 도구 출시 → 우리 서비스 가치 하락.

**대응 방안**:
- **차별화 고착**: naver-diagnosis 기반 자동 진단 + AI 기반 최적화 제안 (P2)
- **고객 Lock-in**: 3개월 계약 → 6개월 계약으로 유도, 성과 기반 인센티브 제공
- **데이터 자산화**: 고객 성과 데이터 누적 → "이커머스 셀러 벤치마

---

# V4 Framework Sections (Pass 2)

## Aha Moment 정의

**Aha Moment:**
> 셀러가 통합 대시보드에서 광고비·ROAS·주문·고객 수를 한 화면에서 실시간으로 확인하고, "아, 이제 엑셀 안 봐도 되겠네"라고 깨닫는 순간.

**측정:**
- 가입부터 아하까지 예상 클릭 수: 5클릭 (회원가입 → 온보딩 → API 연동 → 데이터 동기화 → 대시보드 진입)
- 예상 소요 시간: 45초 이내
- 목표: 60초 이내 달성

**구현 방식:**
1. **온보딩 단축**: 회원가입 → API 키 입력 → "데이터 동기화 중..." 진행바 → 자동 대시보드 로드 (3단계, 2분 이내)
   - 스마트스토어/쿠팡 API 키 사전 검증 → 실패 시 즉시 피드백 (재입력 유도)
   - 템플릿 선택 (스마트스토어 vs 쿠팡) → 자동 필드 매핑 (수동 설정 제거)

2. **핵심 가치 즉시 노출**: 대시보드 상단에 4개 카드 배치
   - 광고비 (누적), ROAS (실시간), 주문 수 (일일), 고객 수 (신규)
   - 각 카드에 "지난주 대비 ↑ 15%" 같은 비교 지표 추가 (성과 감각 극대화)
   - 하단에 시계열 차트 (광고비 vs 매출) → 직관적 상관관계 파악

3. **시각적 피드백**:
   - 데이터 동기화 진행 중: 애니메이션 로딩바 + "스마트스토어에서 광고 데이터 가져오는 중..." 텍스트
   - 동기화 완료: 녹색 체크마크 + "완료! 대시보드 준비됨" → 자동 스크롤 다운
   - 첫 방문 사용자: 투어 팝업 (선택) — "이 카드는 어제 광고비입니다" 같은 1줄 설명

---

## JTBD Statement (민수 전략 → 서윤 Phase 1 기반)

**When I am** 월 1,000만 원대 스마트스토어·쿠팡 셀러로, 광고·콘텐츠·CRM을 따로따로 관리하느라 주 15시간을 쏟고 있고, ROAS가 1.5 이하로 떨어져 매출이 정체되어 있을 때,

**I want to** 광고·콘텐츠·CRM을 한 팀에 맡겨서 통합 운영받고, 실시간 ROAS 대시보드로 성과를 추적하며, 재구매 고객을 자동으로 세그먼트해서 맞춤 메시지를 발송받으면서,

**so I can** 마케팅 운영 시간을 월 50시간 절약하고, ROAS를 3.0 이상으로 안정화해서 매출을 20% 성장시키고, 그 시간에 상품 개발·고객 응대 같은 핵심 업무에 집중할 수 있다.

---

## Customer Forces Strategy (서윤 Phase 3 Canvas 기반)

### Push 요인 (경쟁사 불만 활용)

**현재 상태:**
- 스마트스토어·쿠팡 광고는 에코마케팅 같은 대행사에 맡김 (월 30~100만 원)
- 상세페이지·SNS 콘텐츠는 프리랜서 아웃소싱 (월 50~100만 원)
- CRM·재구매 유도는 엑셀 + 수동 SMS (직원 1명 전담, 월 200만 원)
- 결과: 월 280~400만 원 비용 + 통합 부족으로 ROAS 불안정, 재구매율 저조

**경쟁사 불만 (서윤 Level 5 quotes):**
1. > "광고만 맡기고 콘텐츠·재구매는 따로 해야 해서 피로" — 에코마케팅 사용자 (네이버 카페)
2. > "자사몰은 좋지만 플랫폼 광고 대행 없어 수작업" — 카페24 사용자 (G2 리뷰)
3. > "재구매 고객 데이터 엑셀로 관리하다 놓쳐서 손해" — Klaviyo 사용자 (패션비즈)
4. > "통합 대행사 찾고 있음, 유료 OK" — 스마트스토어 셀러 (adure.net)
5. > "쿠팡 광고만 대행 맡기고 나머지 직접" — 에코마케팅 사용자 (KRX 공시)

**우리의 Push 메시지:**
> "광고·콘텐츠·CRM을 한 팀이 통합 운영해서, 월 280만 원 비용 절감 + ROAS 20% 향상 + 재구매율 30% 달성"

### Pull 요인 (차별 가치)

1. **naver-diagnosis 기반 자동 진단 + 맞춤 제안**
   - 기존 자산(naver-diagnosis) 활용 → 셀러의 광고·콘텐츠·CRM 현황 무료 진단
   - 진단 결과 → "이 문제를 해결하려면 광고 최적화 + 재구매 자동화 필요" 맞춤 제안
   - 경쟁사(에코마케팅, 카페24): 진단 기능 없음 → 리안만의 차별점

2. **실시간 통합 대시보드 (광고+주문+고객 한 화면)**
   - 스마트스토어·쿠팡 API 자동 연동 → 광고비·ROAS·주문·고객 수 실시간 표시
   - 채널별 필터링 + 날짜 범위 선택 가능
   - 경쟁사: 단일 채널(에코마케팅은 광고만, 카페24는 자사몰만) → 리안은 멀티채널 통합

3. **CRM 자동화 (세그먼트 기반 자동 발송)**
   - 구매 금액·빈도별 고객 자동 세그먼트 → 맞춤 이메일/SMS 템플릿 자동 발송
   - 재구매 고객 30일 자동 추출 + 이탈 고객 복귀 캠페인 자동 실행
   - 경쟁사(Klaviyo): 한국 플랫폼 미지원, 수동 설정 필요 → 리안은 스마트스토어·쿠팡 네이티브

### Inertia 감소 (전환 비용 최소화)

- **마이그레이션 도구**: 
  - 기존 엑셀 고객 리스트 → CSV 업로드 기능 (1클릭 임포트)
  - 기존 광고 캠페인 데이터 → API 자동 동기화 (수동 입력 제거)
  - 기존 CRM 템플릿 → 리안 템플릿으로 자동 변환 (학습 곡선 최소화)

- **학습 곡선 최소화**:
  - 온보딩 투어 (선택) — 대시보드·CRM·분석 탭 3분 설명
  - 템플릿 라이브러리 (재구매 유도, 신상품 안내, 할인 쿠폰 등 5가지 사전 제공)
  - 주간 이메일 팁 — "이번주 ROAS 분석 결과 + 추천 액션" (자동 생성)

- **팀 확산**:
  - 초대 기능 — 셀러가 팀원(마케팅 담당자) 추가 가능 (권한 설정: 읽기/쓰기)
  - 공유 기능 — 대시보드·리포트 링크 공유 (외부 이해관계자도 열람 가능)
  - 역할 기반 접근 제어 (RBAC) — 관리자/마케터/뷰어 3단계

### Anxiety 해소 (신뢰 신호)

- **무료 체험**:
  - 첫 14일 무료 (집중 패키지 풀 기능)
  - 신용카드 등록 불필요 (이메일만으로 가입)
  - 14일 후 자동 결제 아님 (수동 구매 필수)

- **보증**:
  - 30일 환불 보증 — "3개월 내 ROAS 20% 미달 시 50% 환불"
  - SLA 99.5% 가용성 (대시보드 다운타임 최소화)
  - 데이터 안전 — 암호화 저장 + PIPA 준수 + 고객 데이터 절대 제3자 공유 금지

- **사회적 증거**:
  - 초기 고객 케이스 스터디 (3개월 내 제작)
    - "월 1,000만 스마트스토어 셀러, ROAS 1.5 → 3.2 달성 (3개월)"
    - "월 800만 자사몰 D2C, 재구매율 12% → 28% 달성"
  - 후기 배치 (랜딩 페이지 하단) — "리안 덕분에 광고 시간 80% 줄었어요" (초기 고객 인용)
  - 네이버 카페·카카오 오픈채팅 입소문 (초기 고객 추천)

---

## Evidence Appendix (기능 ↔ 페인포인트 trace)

### P0 기능 1: 클라이언트 온보딩 (API 연동)

> "광고비 날리고 ROAS 계산 엑셀로"
— https://cafe.naver.com/smartstore (Level 4, 월 1,000만 쿠팡 셀러)

> "재구매 리스트 엑셀로 버티다 오류"
— https://brunch.co.kr/@groobee/1050 (Level 4, 월 800만 자사몰 운영자)

> "통합 대행사 찾고 있음, 유료 OK"
— https://adure.net/contents/detail/... (Level 5, D2C 전환 희망 셀러)

**반영 방식**: 
- 엑셀 workaround의 근본 원인은 "데이터 수집 자동화 부재" → API 자동 연동으로 해결
- 온보딩 단계에서 스마트스토어·쿠팡·자사몰 API 키 입력 → 자동 데이터 동기화 시작
- 기존 엑셀 데이터 CSV 임포트 기능으로 마이그레이션 비용 최소화
- 결과: 셀러가 "데이터 수집"에 쓰던 월 80시간 절약 가능

---

### P0 기능 2: 통합 대시보드 (읽기 전용)

> "쿠팡 광고만 대행 맡기고 나머지 직접"
— https://kind.krx.co.kr/common/disclsviewer.do?method=search&acptno=20250814003419 (Level 4, 월 600만 멀티플랫폼 셀러)

> "플랫폼별(쿠팡·스마트) 광고 따로 관리 피로"
— https://cafe.naver.com/sellerhub (Level 4, 마케팅 담당 1명)

> "멀티채널(쿠팡+자사) 통합 리포트 없음"
— https://kind.krx.co.kr/... (Level 4, 월 1,200만 멀티 셀러)

**반영 방식**:
- 경쟁사(에코마케팅): 광고만 대행 → 콘텐츠·CRM은 셀러가 직접 관리 (분산 피로)
- 리안의 통합 대시보드: 광고비·ROAS·주문·고객 수를 한 화면에 표시
- 채널별 필터링(스마트스토어 vs 쿠팡) + 날짜 범위 선택 → 멀티채널 통합 리포트 자동 생성
- 결과: 셀러가 "여러 툴 병행"에 쓰던 월 150시간 절약, 통합 뷰로 의사결정 속도 2배

---

### P0 기능 3: naver-diagnosis 리포트 통합

> "광고만 맡기고 콘텐츠·재구매는 따로 해야 해서 피로"
— 에코마케팅 사용자 (네이버 카페) (Level 5, 1~5인 운영 브랜드)

> "콘텐츠 제작해도 판매 안 돼 사람 고용 중"
— https://cafe.naver.com/sellerhub (Level 5, 월 600만 셀러)

**반영 방식**:
- 기존 naver-diagnosis 무료 진단 리포트 → 하단에 "광고+콘텐츠+CRM 통합 운영 49만 원" CTA 추가
- 진단 결과 분석 → "이 문제를 해결하려면 광고 최적화 + 콘텐츠 개선 + 재구매 자동화 필요" 맞춤 제안
- 경쟁사(에코마케팅, 카페24): 진단 기능 없음 → 리안만의 영업 훅
- 결과: 기존 자산 활용으로 초기 고객 확보 비용 최소화, 전환율 높은 리드 생성

---

### P0 기능 4: 패키지 구매 & 결제

> "통합 대행사 찾고 있음, 유료 OK"
— https://adure.net/contents/detail/... (Level 5, D2C 전환 희망 셀러)

> "ROAS 추적 툴 연동 실패"
— https://www.g2.com (한국 리뷰) (Level 5, 광고 전문가 셀러)

**반영 방식**:
- 셀러가 "유료 OK" 신호 → 명확한 가격 티어(주목 29만/집중 49만/시선 89만) 제시
- 결제 프로세스 단순화: 패키지 선택 → Stripe/토스 결제 → 즉시 온보딩 시작
- 14일 무료 체험 + 30일 환불 보증으로 구매 불안 해소
- 결과: 높은 전환율 달성, 월 5건 신규 계약 목표 달성 가능

---

### P0 기능 5: 기본 CRM (재구매 고객 리스트)

> "재구매 고객 데이터 엑셀로 관리하다 놓쳐서 손해"
— https://fashionbiz.co.kr/article/221875 (Level 5, 자사몰 운영자)

> "재구매 리스트 엑셀로 버티다 오류"
— https://brunch.co.kr/@groobee/1050 (Level 4, 월 800만 자사몰 운영자)

> "AI CRM 없어 맞춤 메일 실패"
— https://fashionbiz.co.kr/article/221875 (Level 5, 자사몰 운영자)

**반영 방식**:
- 엑셀 workaround의 근본 원인: "고객 세그먼트 자동화 부재" + "발송 자동화 부재"
- 리안의 기본 CRM: 지난 30일 구매자 자동 추출 + 이메일/카톡 발송 템플릿 제공
- 집중 패키지의 핵심 기능 → 셀러가 "한 번의 클릭"으로 재구매 캠페인 실행
- 결과: 셀러가 "CRM 수작업"에 쓰던 월 50시간 절약, 재구매율 30% 달성 가능

---

### P1 기능 1: 광고 성과 분석 리포트 (주간)

> "광고비 날리고 ROAS 계산 엑셀로"
— https://cafe.naver.com/smartstore (Level 4, 월 1,000만 쿠팡 셀러)

> "데이터 분석 없이 직감 광고 운영"
— https://brunch.co.kr/@groobee/1050 (Level 4, 신규 스마트스토어 셀러)

> "광고 예산 초과 모니터링 없음"
— https://cafe.naver.com/smartstore (Level 5, 1인 셀러)

**반영 방식**:
- 경쟁사(에코마케팅): 광고 대행만 제공, 분석 리포트 자동화 부족
- 리안의 P1 기능: 매주 월요일 오전 9시 → 채널별(스마트스토어/쿠팡) ROAS·CPC·전환율 자동 계산 리포트 발송
- 리포트 내용: 지난주 성과 + 추천 액션 (예: "광고 예산 20% 증액 추천")
- 결과: 셀러가 "ROAS 불안정" pain 직접 해결, 데이터 기반 의사결정 가능

---

### P1 기능 2: 콘텐츠 제작 가이드 (자동 생성)

> "상세페이지 콘텐츠 매번 새로 제작하느라 시간 부족"
— https://store.cafe24.com/kr/story/2171 (Level 4, 월 800만 자사몰 D2C 브랜드)

> "콘텐츠 제작해도 판매 안 돼 사람 고용 중"
— https://cafe.naver.com/sellerhub (Level 5, 월 600만 셀러)

> "상세페이지 A/B 테스트 수작업"
— https://store.cafe24.com/kr/story/2171 (Level 4, 쿠팡 셀러 PM)

**반영 방식**:
- 경쟁사(카페24): 콘텐츠 제작 기능 있지만, 자동화 부족 (수동 작성 필요)
- 리안의 P1 기능: 상품 정보 입력 → 상세페이지 작성 체크리스트 자동 생성
  - 예: "제목(30자 이내)", "주요 이미지(1200x1200px)", "상품 설명(500자)", "고객 리뷰 섹션" 등
- 결과: 셀러가 "콘텐츠 제작 시간" 월 50시간 절약, 품질 표준화

---

### P1 기능 3: CRM 자동화 (세그먼트 기반)

> "고객 세그먼트 타겟팅 수동"
— https://fashionbiz.co.kr/article/221875 (Level 4, CRM 담당자)

> "재구매 고객 데이터 엑셀로 관리하다 놓쳐서 손해"
— https://fashionbiz.co.kr/article/221875 (Level 5, 자사몰 운영자)

> "AI CRM 없어 맞춤 메일 실패"
— https://fashionbiz.co.kr/article/221875 (Level 5, 자사몰 운영자)

**반영 방식**:
- 경쟁사(Klaviyo): AI CRM 강하지만, 한국 플랫폼(스마트스토어·쿠팡) 미지원
- 리안의 P1 기능: 구매 금액·빈도별 고객 자동 세그먼트 → 자동 이메일 시퀀스 실행
  - 예: "VIP 고객(월 50만 원 이상)" → "신상품 얼리액세스" 자동 발송
  - 예: "이탈 고객(30일 미구매)" → "복귀 캠페인" 자동 실행
- 결과: 셀러가 "CRM 수작업" 월 50시간 절약, 재구매율 30% 달성

---

### P1 기능 4: 클라이언트 포털 (쓰기 권한)

> "통합 대행사 찾고 있음, 유료 OK"
— https://adure.net/contents/detail/... (Level 5, D2C 전환 희망 셀러)

> "쿠팡 광고만 대행 맡기고 나머지 직접"
— https://kind.krx.co.kr/... (Level 4, 월 600만 멀티플랫폼 셀러)

**반영 방식**:
- 경쟁사(에코마케팅): 대행사 일방적 운영, 셀러 피드백 반영 느림
- 리안의 P1 기능: 셀러가 포털에서 광고 예산·콘텐츠 승인·CRM 메시지 직접 수정 가능
  - 예: "다음주 광고 예산 20만 원 → 30만 원으로 증액" 직접 변경
  - 예: "CRM 이메일 제목 수정" 직접 편집
- 결과: 셀러 자율성 증가 → 만족도 상승, 리텐션율 70% 달성 가능

---

### P2 기능 1: AI 기반 광고 최적화 제안

> "광고비 날리고 ROAS 계산 엑셀로"
— https://cafe.naver.com/smartstore (Level 4, 월 1,000만 쿠팡 셀러)

> "데이터 분석 없이 직감 광고 운영"
— https://brunch.co.kr/@groobee/1050 (Level 4, 신규 스마트스토어 셀러)

**반영 방식**:
- 경쟁사(Klaviyo): AI 기반 최적화 있지만, 한국 플랫폼 미지원
- 리안의 P2 기능: 과거 ROAS 데이터 → 예산 재배분 제안 (수동 승인)
  - 예: "스마트스토어 광고 ROAS 3.5, 쿠팡 광고 ROAS 1.8 → 쿠팡 예산 30% 감액 추천"
- 결과: 고급 기능으로 시선 패키지 차별화, 셀러의 ROAS 안정화 가속

---

### P2 기능 2: 예측 분석 (매출 예측)

> "자사몰 트래픽 유입 부족으로 플랫폼 의존"
— https://adure.net/contents/detail/... (Level 5, D2C 전환 희망 월 1,500만 셀러)

**반영 방식**:
- 경쟁사(삼성SDS): 데이터 기반 전략 제공하지만, SMB 접근성 낮음
- 리안의 P2 기능: 지난 3개월 데이터 → 다음 달 예상 매출 시뮬레이션
  - 예: "현재 추세 유지 시 다음달 예상 매출 1,200만 원, 광고 20% 증액 시 1,500만 원"
- 결과: 셀러의 재고·예산 계획 지원, 자사몰 전환 의사결정 가속

---

### P2 기능 3: 멀티 채널 광고 자동 입찰

> "플랫폼별(쿠팡·스마트) 광고 따로 관리 피로"
— https://cafe.naver.com/sellerhub (Level 4, 마케팅 담당 1명)

> "광고 예산 초과 모니터링 없음"
— https://cafe.naver.com/smartstore (Level 5, 1인 셀러)

**반영 방식**:
- 경쟁사: 자동 입찰 기능 없음 (수동 관리 필수)
- 리안의 P2 기능: 스마트스토어·쿠팡 광고 예산 자동 분배 (AI 기반)
  - 예: "일일 예산 100만 원 → ROAS 기반으로 스마트스토어 60만, 쿠팡 40만 자동 배분"
- 결과: 운영 자동화로 시선 패키지 프리미엄 기능, 셀러의 운영 시간 월 100시간 절약

---

**Evidence Appendix 완성**: 모든 P0/P1/P2 기능이 서윤 Phase 1 pain point (Level 4-5)의 실제 quote로 trace 가능. 경쟁사 불만(에코마케팅·카페24·Klaviyo·삼성SDS) 기반 gap 명확화. 리안의 차별점(naver-diagnosis 활용, 한국 플랫폼 네이티브, 통합 대행) 각 기능에 반영됨.