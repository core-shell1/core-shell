# PRD: 거래망 추천 시스템 (Trustrade)

## 제품 개요
**신용도 기반 거래망 추천으로 인테리어 시공업체의 거래 리스크를 줄이고 수주율을 높이는 B2B SaaS**

---

## 기술 스택

| 계층 | 선택 | 근거 |
|------|------|------|
| **FE** | React 18 + TypeScript + TailwindCSS | 빠른 반복 개발, 인테리어 업체 대상 모바일-우선 UI 필수 |
| **BE** | Node.js (Express) + TypeScript | 초기 팀 규모 고려, 빠른 프로토타이핑, 기존 리안 스택과 호환 |
| **DB** | PostgreSQL (관계형) + Redis (캐시) | 거래망 신용도 데이터 정규화 필수, 추천 알고리즘 캐싱 |
| **인프라** | AWS EC2 + RDS + S3 | 확장성, 기존 리안 인프라 통합 가능 |
| **외부 API** | 나이스평가정보 / KCB (신용조회) — Phase 2 | MVP는 수동 DB로 대체 |
| **배포** | GitHub Actions + Docker | CI/CD 자동화, 빠른 반복 |

---

## 기능 목록

> **Wave 전략**: P0(MVP 3주) → P1(1차 출시 후 4주) → P2(장기 로드맵)

| 우선순위 | 기능 | 설명 | 이유 | 의존 기능 | 예상 개발 기간 |
|---------|------|------|------|---------|-------------|
| **P0** | 회원가입 / 로그인 (B2B) | 이메일 + 휴대폰 인증 | 기본 기능 | 없음 | 3일 |
| **P0** | 거래망 추천 엔진 (수동 DB 기반) | 신용도 점수 기반 TOP 5 업체 추천 | **핵심 가치 전달** — 준혁 조건: 신용도 DB 수동 큐레이션 50개 선행 필수 | 회원가입 | 5일 |
| **P0** | 추천 업체 상세 정보 조회 | 업체명, 신용도 점수, 거래 이력, 연락처 | 사용자가 추천 결과를 신뢰하고 행동 | 거래망 추천 엔진 | 2일 |
| **P0** | 추천 이력 저장 (Favorites) | 관심 업체 저장 / 삭제 | 사용자 재방문 유도 | 추천 업체 상세 정보 | 2일 |
| **P0** | 결제 / 구독 관리 (Starter 플랜) | 월 20만 원, 월 50건 추천 | 수익화 | 회원가입 | 4일 |
| **P1** | 신용도 점수 상세 분석 | 신용도 산정 근거 (거래 이력, 연체 여부, 평판) 시각화 | 투명성 → 신뢰도 ↑ | 거래망 추천 엔진 | 5일 |
| **P1** | 거래 후기 / 평점 시스템 | 사용자가 추천받은 업체와 거래 후 평가 입력 | 신용도 DB 자동 업데이트 → 선순환 | 추천 업체 상세 정보 | 5일 |
| **P1** | 나이스평가정보 / KCB API 연동 | 실시간 신용도 조회 (수동 DB 대체) | 신용도 정확성 ↑, 수동 관리 부담 ↓ | 거래망 추천 엔진 | 7일 |
| **P1** | Pro 플랜 (월 35만 원) | Starter + 법률 리스크 체크 (체크리스트 기반) | 업셀 경로 | 거래망 추천 엔진 | 5일 |
| **P2** | 법률 리스크 자동 체크 | 계약서 자동 분석 (PDF 업로드) | 차별화 기능 (블루오션) | Pro 플랜 | 14일 |
| **P2** | 공기 산출 자동화 | 시공 면적 + 공종 입력 → 표준공기 자동 계산 | 차별화 기능 (블루오션) | 거래망 추천 엔진 | 14일 |
| **P2** | 사업성 평가서 자동 생성 | 거래망 신용도 + 공기 + 법률 리스크 통합 리포트 | 원스톱 의사결정 도구 | 법률 리스크 + 공기 산출 | 10일 |

### Must NOT (범위 외)

| 제외 기능 | 이유 |
|---------|------|
| 자재 가격 비교 | 시장 데이터 수집 난이도 높음, MVP 핵심 가치와 무관 |
| 시공 일정 관리 | 프로젝트 관리 도구 경쟁사 다수, 차별화 불가 |
| 클라이언트 관리 (CRM) | 범위 확대 → 개발 지연 위험, P2 이후 검토 |
| 자동 인보이싱 | 세무/회계 복잡성, MVP 단계에서 불필요 |
| 모바일 앱 (네이티브) | 초기 웹 기반으로 충분, 사용자 검증 후 고려 |

---

## User Flow

### **Flow 1: 신규 가입 → 첫 추천받기 (Aha Moment)**

```
1단계: 랜딩 페이지 방문
   → "신용도 기반으로 안전한 거래망을 추천받고 거래 리스크를 줄이세요 (월 20만 원)"
   → [지금 시작하기] 버튼 클릭

2단계: 회원가입 (이메일 + 휴대폰)
   → 인증 코드 입력
   → 회사명, 직급, 업종(인테리어 시공) 입력
   → 가입 완료

3단계: 온보딩 (30초)
   → "어떤 거래처를 찾으세요?" 팝업
   → 선택지: [자재 공급업체] / [하청 시공팀] / [설계사]
   → 선택 후 [추천받기] 클릭

4단계: 첫 추천 결과 노출 (Aha Moment 발생 지점)
   ✓ TOP 5 업체 카드 노출
   ✓ 각 카드: 업체명 + 신용도 점수(0~100) + 거래 이력 수 + "연락처 보기" 버튼
   ✓ 사용자가 "이 업체 신용도 높네" 인지 → 신뢰 형성
   
   **Aha Moment 정의**: 
   "신용도 점수를 보고 '아, 이 업체는 안전하겠네'라고 판단하는 순간"
   
   **측정치**: 가입 → 첫 추천 결과 노출까지 **45초 이내**
   **목표**: 60초 이내 달성

5단계: 액션 선택
   → [연락처 보기] 클릭 (유료 기능 트리거)
     또는
   → [저장하기] 클릭 (Favorites 추가)
     또는
   → [다른 업체 추천받기] 클릭 (재추천)

6단계: 결제 유도
   → 연락처 보기 시도 시 "Starter 플랜 구독 필요" 모달
   → [월 20만 원 구독하기] 또는 [3개월 선결제 50% 할인]
   → 결제 완료 → 연락처 노출
```

### **Flow 2: 기존 사용자 → 거래 후 평가 입력**

```
1단계: 로그인 후 대시보드
   → 저장된 업체 목록 노출
   → "최근 거래한 업체가 있나요?" 배너

2단계: 거래 후기 입력
   → 업체 선택 → [거래 후기 작성] 클릭
   → 평점(1~5) + 텍스트 입력
   → 제출

3단계: 신용도 DB 업데이트 (백그라운드)
   → 후기 데이터 수집 → 신용도 점수 재계산
   → 다른 사용자의 추천 결과에 반영
```

---

## 화면 명세

| 화면명 | Route | 핵심 컴포넌트 | 동작 |
|--------|-------|-------------|------|
| **랜딩 페이지** | `/` | Hero 섹션 + 가치 제안 + CTA 버튼 | [지금 시작하기] → `/signup` 이동 |
| **회원가입** | `/signup` | 이메일 입력 + 휴대폰 인증 + 회사정보 폼 | 입력 → 인증 → 가입 완료 → `/onboarding` |
| **온보딩** | `/onboarding` | 업종 선택 팝업 + [추천받기] 버튼 | 선택 → `/recommendations` |
| **추천 결과** | `/recommendations` | 업체 카드 리스트 (TOP 5) + 신용도 점수 시각화 | 카드 클릭 → `/company/:id` / [저장] → Favorites 추가 / [연락처 보기] → 결제 모달 |
| **업체 상세** | `/company/:id` | 업체명 + 신용도 상세 분석 + 거래 이력 + 평점 + 연락처 | [연락처 복사] / [저장] / [후기 작성] |
| **결제 모달** | (overlay) | 플랜 선택 (Starter/Pro) + 결제 수단 선택 | 결제 완료 → 연락처 노출 |
| **대시보드** | `/dashboard` | 저장된 업체 목록 + 최근 추천 이력 + 구독 상태 | 업체 클릭 → `/company/:id` / [거래 후기 작성] |
| **거래 후기** | `/company/:id/review` | 평점(1~5) + 텍스트 입력 폼 | 제출 → 신용도 DB 업데이트 |
| **로그인** | `/login` | 이메일 + 비밀번호 입력 | 로그인 → `/dashboard` |

---

## API 명세

### **1. 회원가입 / 인증**

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/auth/signup` | `{ email, password, phone, company_name, job_title, industry }` | `{ user_id, email, token }` | 없음 |
| POST | `/api/auth/verify-phone` | `{ phone, code }` | `{ verified: true }` | 없음 |
| POST | `/api/auth/login` | `{ email, password }` | `{ user_id, token, subscription_status }` | 없음 |
| POST | `/api/auth/logout` | `{}` | `{ success: true }` | Bearer Token |

### **2. 거래망 추천**

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/recommendations/generate` | `{ industry, category: "material_supplier" \| "subcontractor" \| "designer", limit: 5 }` | `{ recommendations: [{ company_id, name, credit_score, trade_count, contact_hidden: true }], recommendation_id }` | Bearer Token |
| GET | `/api/recommendations/history` | (Query: `limit=10, offset=0`) | `{ recommendations: [...], total_count }` | Bearer Token |

### **3. 업체 상세 정보**

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/companies/:company_id` | (Query: `show_contact=false`) | `{ company_id, name, credit_score, credit_breakdown: { trade_history: 80, payment_record: 90, reputation: 70 }, trade_count, reviews: [...], contact: { phone, address } (조건부) }` | Bearer Token |
| GET | `/api/companies/:company_id/reviews` | (Query: `limit=10`) | `{ reviews: [{ user_id, rating, text, created_at }], avg_rating }` | Bearer Token |

### **4. 저장 / Favorites**

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/favorites` | `{ company_id }` | `{ favorite_id, company_id, created_at }` | Bearer Token |
| DELETE | `/api/favorites/:favorite_id` | `{}` | `{ success: true }` | Bearer Token |
| GET | `/api/favorites` | (Query: `limit=20`) | `{ favorites: [{ favorite_id, company_id, company_name, credit_score }], total_count }` | Bearer Token |

### **5. 거래 후기 / 평점**

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/reviews` | `{ company_id, rating: 1-5, text }` | `{ review_id, company_id, created_at }` | Bearer Token |
| PUT | `/api/reviews/:review_id` | `{ rating, text }` | `{ review_id, updated_at }` | Bearer Token |
| DELETE | `/api/reviews/:review_id` | `{}` | `{ success: true }` | Bearer Token |

### **6. 결제 / 구독**

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/subscriptions/checkout` | `{ plan: "starter" \| "pro", payment_method: "card" \| "bank_transfer", billing_cycle: "monthly" \| "quarterly" }` | `{ checkout_url, session_id }` (Stripe 리다이렉트) | Bearer Token |
| GET | `/api/subscriptions/status` | `{}` | `{ plan, status: "active" \| "expired", remaining_recommendations: 45, expires_at }` | Bearer Token |
| POST | `/api/subscriptions/cancel` | `{}` | `{ success: true, refund_status }` | Bearer Token |

### **7. 연락처 노출 (유료 기능)**

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/companies/:company_id/contact` | `{}` | `{ phone, address, email }` (구독 확인 후) 또는 `{ error: "subscription_required" }` | Bearer Token |

### **8. 관리자 API (수동 DB 관리)**

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/admin/companies` | `{ name, phone, address, credit_score: 0-100, category, trade_history: [...] }` | `{ company_id }` | Admin Token |
| PUT | `/api/admin/companies/:company_id` | `{ credit_score, trade_history }` | `{ success: true }` | Admin Token |
| GET | `/api/admin/companies` | (Query: `limit=50`) | `{ companies: [...], total_count }` | Admin Token |

---

## 데이터 모델

### **1. users (사용자)**

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| user_id | UUID | 사용자 고유 ID | PK |
| email | VARCHAR(255) | 이메일 | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | 해시된 비밀번호 | NOT NULL |
| phone | VARCHAR(20) | 휴대폰 번호 | UNIQUE, NOT NULL |
| company_name | VARCHAR(255) | 회사명 | NOT NULL |
| job_title | VARCHAR(100) | 직급 | NOT NULL |
| industry | ENUM('interior', 'construction', 'design') | 업종 | NOT NULL |
| created_at | TIMESTAMP | 가입 일시 | DEFAULT NOW() |
| updated_at | TIMESTAMP | 수정 일시 | DEFAULT NOW() |

### **2. companies (거래망 DB)**

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| company_id | UUID | 업체 고유 ID | PK |
| name | VARCHAR(255) | 업체명 | NOT NULL |
| phone | VARCHAR(20) | 연락처 | NOT NULL |
| address | VARCHAR(500) | 주소 | NOT NULL |
| category | ENUM('material_supplier', 'subcontractor', 'designer') | 업체 분류 | NOT NULL |
| credit_score | INT (0-100) | 신용도 점수 | DEFAULT 50 |
| trade_count | INT | 거래 이력 수 | DEFAULT 0 |
| avg_rating | DECIMAL(2,1) | 평균 평점 | DEFAULT 0.0 |
| data_source | ENUM('manual', 'nice_api', 'kcb_api', 'user_review') | 데이터 출처 | DEFAULT 'manual' |
| last_updated | TIMESTAMP | 마지막 업데이트 | DEFAULT NOW() |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

### **3. recommendations (추천 이력)**

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| recommendation_id | UUID | 추천 고유 ID | PK |
| user_id | UUID | 사용자 ID | FK(users) |
| company_ids | UUID[] | 추천받은 업체 ID 배열 (TOP 5) | NOT NULL |
| category | ENUM('material_supplier', 'subcontractor', 'designer') | 추천 카테고리 | NOT NULL |
| created_at | TIMESTAMP | 추천 일시 | DEFAULT NOW() |

### **4. favorites (저장된 업체)**

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| favorite_id | UUID | 저장 고유 ID | PK |
| user_id | UUID | 사용자 ID | FK(users) |
| company_id | UUID | 업체 ID | FK(companies) |
| created_at | TIMESTAMP | 저장 일시 | DEFAULT NOW() |
| UNIQUE(user_id, company_id) | | 중복 저장 방지 | |

### **5. reviews (거래 후기)**

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| review_id | UUID | 후기 고유 ID | PK |
| user_id | UUID | 작성자 ID | FK(users) |
| company_id | UUID | 업체 ID | FK(companies) |
| rating | INT (1-5) | 평점 | NOT NULL |
| text | TEXT | 후기 내용 | NOT NULL |
| created_at | TIMESTAMP | 작성 일시 | DEFAULT NOW() |
| updated_at | TIMESTAMP | 수정 일시 | DEFAULT NOW() |

### **6. subscriptions (구독)**

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| subscription_id | UUID | 구독 고유 ID | PK |
| user_id | UUID | 사용자 ID | FK(users) |
| plan | ENUM('starter', 'pro', 'enterprise') | 플랜 | NOT NULL |
| status | ENUM('active', 'expired', 'cancelled') | 구독 상태 | DEFAULT 'active' |
| monthly_quota | INT | 월 추천 건수 한도 | (starter: 50, pro: 100) |
| remaining_quota | INT | 남은 추천 건수 | DEFAULT = monthly_quota |
| started_at | TIMESTAMP | 구독 시작 일시 | NOT NULL |
| expires_at | TIMESTAMP | 구독 만료 일시 | NOT NULL |
| stripe_subscription_id | VARCHAR(255) | Stripe 구독 ID | UNIQUE |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

### **7. contact_views (연락처 조회 로그)**

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| view_id | UUID | 조회 고유 ID | PK |
| user_id | UUID | 사용자 ID | FK(users) |
| company_id | UUID | 업체 ID | FK(companies) |
| viewed_at | TIMESTAMP | 조회 일시 | DEFAULT NOW() |

---

## 성공 기준

### **Phase 1 (MVP 출시 후 4주) — 기본 검증**

| KPI | 목표치 | 측정 방법 | 임계값 |
|-----|--------|---------|--------|
| **Aha Moment 달성율** | 60% 이상 | 가입 후 45초 이내 첫 추천 결과 노출 사용자 / 전체 가입자 | <40% = 온보딩 재설계 |
| **첫 주 재방문율 (DAU/WAU)** | 30% 이상 | 가입 후 7일 내 재로그인 사용자 수 | <20% = 가치 제안 재검토 |
| **유료 전환율** | 10% 이상 | 연락처 보기 시도 → 결제 완료 / 전체 추천 조회 | <5% = 가격/신뢰도 문제 |
| **초기 고객 확보** | 50명 이상 | 유료 구독자 수 | <30명 = 마케팅 채널 재검토 |
| **월 매출** | 1,000만 원 이상 | Starter 50명 × 20만 원 | <500만 원 = 피벗 신호 |
| **신용도 DB 정확성** | 80% 이상 | 사용자 후기 기반 신용도 점수 검증 (실제 거래 경험과 일치도) | <70% = 수동 DB 재검증 |

### **Phase 2 (1~3개월) — 성장 검증**

| KPI | 목표치 | 측정 방법 | 임계값 |
|-----|--------|---------|--------|
| **월 활성 사용자 (MAU)** | 300명 이상 | 월 1회 이상 로그인 사용자 | <200명 = 채널 확대 |
| **평균 추천 조회 수 (per user/month)** | 8회 이상 | 월 총 추천 조회 / MAU | <5회 = 가치 제안 약함 |
| **구독 유지율 (MRR Churn)** | 5% 이하 | (이전월 MRR - 해지 MRR) / 이전월 MRR | >10% = 고객 만족도 문제 |
| **LTV/CAC 비율** | 3 이상 | LTV(50만 원) / CAC(실제 측정) | <2 = 단위경제 재검토 |
| **거래 후기 입력율** | 20% 이상 | 연락처 조회 → 후기 입력 / 전체 연락처 조회 | <10% = 후기 입력 UX 개선 |

### **Phase 3 (3~6개월) — 스케일 검증**

| KPI | 목표치 | 측정 방법 | 임계값 |
|-----|--------|---------|--------|
| **월 매출 (MRR)** | 5,000만 원 이상 | Starter 200명 + Pro 50명 | <3,000만 원 = 성장 정체 |
| **Pro 플랜 업셀율** | 15% 이상 | Pro 구독자 / 전체 구독자 | <10% = Pro 가치 제안 약함 |
| **신용도 DB 규모** | 500개 이상 | 수동 + API 연동 업체 수 | <300개 = DB 구축 지연 |
| **NPS (Net Promoter Score)** | 40 이상 | "이 서비스를 동료에게 추천하겠는가?" (0~10) | <30 = 제품 만족도 문제 |

---

## Aha Moment 정의

**정의**: 사용자가 추천받은 업체의 신용도 점수를 보고 "아, 이 업체는 신뢰할 수 있겠네"라고 판단하는 순간

**측정치**: 
- 가입 완료 → 첫 추천 결과 노출까지 **45초 이내**
- 목표: 60초 이내 달성

**구현 방식**:
1. 온보딩 단계 최소화 (업종 선택만 → 2초)
2. 추천 엔진 응답 시간 <3초 (캐시 활용)
3. 신용도 점수 시각화 (숫자 + 게이지 바 + 색상 코딩)
4. 첫 추천 결과 화면에서 "왜 이 업체를 추천했는가?" 한 줄 설명 추가

---

## JTBD Statement (민수 전략 → 서윤 Phase 1 기반)

**When I am** 새로운 자재 공급업체나 하청 시공팀을 찾아야 할 때,

**I want to** 신용도가 높고 거래 이력이 확실한 업체를 빠르게 추천받고

**so I can** 거래 리스크(연체, 부실 시공, 신용 부도)를 줄이고 수주율을 높일 수 있다.

---

## Customer Forces Strategy (서윤 Phase 3 Canvas 기반)

### **Push 요인 (경쟁사 불만 활용)**
- 현재: 거래망을 손으로 관리 (엑셀, 카톡 메모) → 신용도 파악 어려움
- 경쟁사 불만: 거래처 추천 서비스 없음 (블루오션 플래그 확인)
- **우리의 Push**: "신용도 기반 거래망 추천이 없어서 손해 본 경험, 이제 끝내세요"

### **Pull 요인 (차별 가치)**
1. **신용도 기반 매칭**: 거래 이력 + 평판 + 신용도 점수로 안전한 업체