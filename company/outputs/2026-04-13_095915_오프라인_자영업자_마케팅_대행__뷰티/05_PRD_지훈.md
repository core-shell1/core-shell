# PRD: 오프라인 자영업자 네이버플레이스 통합 관리 SaaS

## 1. 제품 개요

**뷰티샵·카페·식당 등 오프라인 자영업자(1~5인 사업장)를 위한 네이버플레이스 리뷰·평점·SEO 자동화 월 구독 서비스로, AI 자동 리뷰 응답 + 로컬 SEO 최적화 + 정보 자동 업데이트를 통해 평점 4.5 이상 유지 및 로컬 검색 1페이지 노출을 보장한다.**

---

## 2. 기술 스택

- **FE**: React 18 + TypeScript + TailwindCSS (반응형 웹앱 + 모바일 최적화)
- **BE**: Node.js (Express) + TypeScript + PostgreSQL (관계형 데이터 필요 — 고객/리뷰/평점 추이 추적)
- **AI/ML**: OpenAI API (GPT-4 기반 리뷰 응답 생성) + 자체 분류 모델 (긍정/부정/중립 리뷰 자동 분류)
- **외부 API**: 네이버플레이스 API (리뷰 크롤링, 평점 조회, 정보 업데이트) + 구글 애널리틱스 API (트래픽 추적)
- **인프라**: AWS EC2 (서버) + RDS (PostgreSQL) + S3 (이미지 저장) + CloudFront (CDN)
- **배포**: GitHub Actions (CI/CD) → AWS (프로덕션)
- **모니터링**: Sentry (에러 추적) + DataDog (성능 모니터링)

---

## 3. 기능 목록

> **P0** = MVP 필수 (론칭 3개월 내 필수 기능)  
> **P1** = 1차 출시 후 (3~6개월 추가)  
> **P2** = 나중에 (6개월 이후)

| 우선순위 | 기능 | 설명 | 이유 | 의존 기능 |
|---------|------|------|------|---------|
| **P0** | AI 자동 리뷰 응답 | 네이버플레이스 리뷰 발생 시 5분 내 자동 응답 (긍정/부정/중립 자동 분류 + 맞춤 응답 생성) | Pain #2 "리뷰 하나하나 관리하느라 피곤" 직접 해결 — 월 20시간 수작업 → 0시간 | 없음 |
| **P0** | 24시간 실시간 모니터링 | 야간·주말 리뷰도 즉시 감지 + 푸시 알림 발송 (고객 앱 + 이메일) | Pain #11 "리뷰 응답 지연으로 평점 하락" 해결 — 야간 미응답 방지 | AI 자동 리뷰 응답 |
| **P0** | 평점 관리 대시보드 | 실시간 평점·리뷰 추이·경쟁사 비교 (그래프 + 수치) | 고객이 "성과를 본다" 느낌 — 해지율 관리 핵심 | 없음 |
| **P0** | 로컬 SEO 최적화 | 네이버 검색 알고리즘 분석하여 키워드·카테고리·태그 자동 설정 (로컬 검색 1페이지 노출 보장) | Pain #6 "네이버플레이스 SEO 최적화 모름" 해결 — 로컬 검색 2~3페이지 → 1페이지 | 없음 |
| **P0** | 월 성과 리포트 자동 생성 | 리뷰 응답률·평점 변화·예약 증가율 자동 계산 + PDF 리포트 생성 | 고객 신뢰 확보 + 해지율 관리 (성과 가시화) | 평점 관리 대시보드 |
| **P0** | naver-diagnosis 무료 진단 | 네이버플레이스 진단 (평점·리뷰 응답률·SEO 점수·경쟁사 비교) 선착순 20명 무료 제공 | 영업 훅 — 진단 → 문제 인지 → 유료 전환 (추정 전환율 30%) | 없음 |
| **P0** | 고객 온보딩 플로우 | 가입 → 네이버플레이스 계정 연동 → 첫 진단 → 기능 투어 (3단계, 5분 소요) | 초기 고객 이탈 방지 | 없음 |
| **P0** | 결제 시스템 | 토스페이먼츠 연동 (월 구독 결제 + 자동 갱신) | 수익화 필수 | 없음 |
| **P1** | 네이버플레이스 정보 자동 업데이트 | 메뉴·사진·영업시간·이벤트 캘린더 연동 (고객이 1회 업로드 → 자동 동기화) | Pain #14 "네이버플레이스 사진 업데이트 번거로움" 해결 — 월 10시간 → 1시간 | 없음 |
| **P1** | 부정 리뷰 대응 자동화 | 부정 리뷰 발생 시 고객에게 "대응 템플릿" 제안 (사람이 최종 승인 후 발송) | Pain #2 "부정 리뷰 수정 요청 전화 통화" 간접 해결 | AI 자동 리뷰 응답 |
| **P1** | 인스타그램 콘텐츠 자동 생성 | AI 이미지 생성 + 캡션 자동 작성 (주 3회, 집중 플랜 이상) | Pain #1 "인스타 직접 올리다 지쳐서 포기" 해결 (업셀링 기능) | 없음 |
| **P1** | 인스타 광고 A/B 테스트 자동화 | 크리에이티브 2개 자동 생성 + 성과 비교 (시선 플랜 이상) | Pain #25 "인스타 광고 A/B 테스트 모름" 해결 | 인스타그램 콘텐츠 자동 생성 |
| **P1** | 블로그 체험단 매칭 플랫폼 | 체험단 모집 → 블로거 자동 매칭 → 포스팅 일정 관리 (시선 플랜 이상) | Pain #3 "블로그 체험단 엑셀 관리 오류" 해결 | 없음 |
| **P1** | 통합 성과 대시보드 | 인스타+네이버+블로그 성과 한 화면에서 추적 (P1 기능 추가 후) | Pain #35 "성과 지표 추적 다중 툴" 해결 | 평점 관리 대시보드 + 인스타그램 콘텐츠 자동 생성 |
| **P2** | 네이버 광고 대행 | 네이버 광고 집행 + 최적화 (월 광고비 50만원 포함, 추가 광고비는 10% 수수료) | 업셀링 (시선 플랜 → 커스텀 플랜) | 로컬 SEO 최적화 |
| **P2** | 전담 계정 매니저 | 월 1회 전화 상담 (시선 플랜 이상) | 고객 만족도 + 해지율 관리 | 없음 |
| **P2** | API 연동 (Cafe24·배달의민족) | 기존 플랫폼과 자동 동기화 (파트너십) | 고객 편의성 + 시장 확장 | 없음 |

---

## 4. Must NOT (범위 외)

- **인스타그램 계정 직접 운영** — 우리는 콘텐츠 생성만 제공, 계정 관리(팔로우/언팔로우/DM 응답)는 고객 책임
- **배달앱(배달의민족·쿠팡이츠) 리뷰 관리** — 초기 MVP는 네이버플레이스만 지원 (P2에서 확장)
- **법적 리뷰 삭제 대행** — 부정 리뷰 삭제는 네이버 정책상 불가능, 대신 "대응 템플릿" 제안만 제공
- **고객 전화 상담 (주 5일 이상)** — 초기는 이메일/채팅 지원만, 전담 매니저는 P2 시선 플랜 이상
- **오프라인 매장 방문 컨설팅** — 온라인 SaaS 모델 유지 (원가 증가 방지)
- **블로그 포스팅 직접 작성** — P1 체험단 매칭은 "모집 + 일정 관리"만, 포스팅 작성은 블로거 책임
- **SEO 보장 (법적 계약)** — "로컬 검색 1페이지 노출 보장"은 마케팅 메시지, 실제 보장 불가능 (네이버 알고리즘 변경 시) — 대신 "3개월 내 평점 4.5 이상 유지" 성과 보장으로 변경 (P0 기능 범위 내)

---

## 5. User Flow

### 시나리오 1: 신규 고객 가입 → 무료 진단 → 유료 전환

**사용자**: 35세 네일샵 원장, 네이버플레이스 평점 4.2, 월 리뷰 30건

1단계: 네이버 카페 "뷰티샵 원장 모임"에서 "무료 네이버플레이스 진단" 광고 클릭
→ 시스템 응답: naver-diagnosis 랜딩 페이지 로드 (평점/리뷰 응답률/SEO 점수 설명)

2단계: "무료 진단 신청" 버튼 클릭 → 네이버플레이스 URL 입력 → 이메일 입력
→ 시스템 응답: "24시간 내 진단 결과 이메일 발송" 메시지 표시

3단계: 24시간 후 이메일 수신 → 진단 결과 확인 (평점 4.2, 리뷰 응답률 30%, SEO 점수 60점)
→ 시스템 응답: "집중 플랜 49만원 첫 달 30% 할인 (34.3만원)" 팝업 + "평점 4.5 회복 보장" 메시지

4단계: "지금 시작하기" 버튼 클릭 → 가입 페이지 (이메일/비밀번호/사업장명 입력)
→ 시스템 응답: 가입 완료 → 네이버플레이스 계정 연동 페이지로 자동 이동

5단계: 네이버 로그인 → 계정 연동 승인
→ 시스템 응답: "연동 완료, 첫 리뷰 응답까지 5분 남았습니다" 메시지 + 기능 투어 시작

6단계: 기능 투어 완료 (대시보드 → 리뷰 응답 → 성과 리포트, 3단계 5분)
→ 시스템 응답: 투어 완료 → 결제 페이지로 자동 이동

7단계: 토스페이먼츠 결제 (34.3만원, 첫 달 할인가)
→ 시스템 응답: 결제 완료 → 대시보드 접속 가능 상태로 변경 → 환영 이메일 발송

**총 시간**: 신청 → 결제까지 3~7일 (진단 대기 1일 + 고객 검토 2~6일)

---

### 시나리오 2: 기존 고객 일일 사용 흐름

**사용자**: 위 네일샵 원장, 집중 플랜 구독 중 (2주차)

1단계: 아침 9시 스마트폰 알림 수신 → "새로운 리뷰 1건 도착" 푸시 알림
→ 시스템 응답: 알림 클릭 → 리뷰 상세 페이지 로드 (리뷰 내용 + AI 자동 응답 제안)

2단계: AI 자동 응답 확인 → "감사합니다! 다음에도 방문해주세요" (자동 생성)
→ 시스템 응답: "이 응답으로 발송할까요?" 버튼 표시

3단계: "발송" 버튼 클릭
→ 시스템 응답: 네이버플레이스에 자동 발송 완료 → "응답 완료" 체크마크 표시

4단계: 저녁 6시 대시보드 접속 → 오늘의 평점·리뷰 추이 확인
→ 시스템 응답: 실시간 대시보드 로드 (평점 4.2 → 4.3으로 상승, 리뷰 응답률 30% → 50%로 상승)

5단계: "지난 주 성과 보기" 클릭 → 주간 리포트 확인 (리뷰 7건 응답, 평점 0.1 상승, 예약 3건 증가 추정)
→ 시스템 응답: 주간 리포트 그래프 표시 (막대 그래프 + 수치)

**총 시간**: 5분 (알림 확인 1분 + 응답 발송 1분 + 대시보드 확인 3분)

---

### 시나리오 3: 월말 성과 리포트 자동 생성

**사용자**: 위 네일샵 원장, 집중 플랜 구독 중 (1개월 후)

1단계: 월말 마지막 날 오후 6시 이메일 수신 → "9월 성과 리포트 도착"
→ 시스템 응답: 이메일에 PDF 리포트 첨부 + 대시보드 링크

2단계: PDF 리포트 확인 (1장, 요약 형식)
- 리뷰 응답률: 30% → 65% (↑ 35%p)
- 평점: 4.2 → 4.4 (↑ 0.2)
- 예약 증가: 추정 월 50만원 매출 증가
- ROI: 월 49만원 투자 → 월 50만원 매출 증가 (ROI 102%)

3단계: "다음 달도 계속 진행" 결정 → 자동 갱신 (별도 액션 불필요)
→ 시스템 응답: 자동 갱신 확인 이메일 발송

**총 시간**: 1분 (리포트 확인만)

---

## 6. 화면 명세

| 화면명 | URL/Route | 핵심 컴포넌트 | 동작 |
|--------|-----------|-------------|------|
| **naver-diagnosis 랜딩** | `/diagnosis` | 헤더 (로고) + 진단 설명 (3줄) + 입력 폼 (네이버플레이스 URL) + CTA 버튼 ("무료 진단 신청") + FAQ (3개) + 푸터 | URL 입력 → "신청 완료" 메시지 → 이메일 입력 폼 표시 |
| **진단 결과 페이지** | `/diagnosis/result/:id` | 헤더 + 진단 결과 요약 (카드 4개: 평점/리뷰 응답률/SEO 점수/경쟁사 비교) + 상세 분석 (그래프) + "집중 플랜 시작" CTA 버튼 | 결과 카드 클릭 → 상세 분석 모달 표시 |
| **가입 페이지** | `/signup` | 헤더 + 입력 폼 (이메일/비밀번호/사업장명/업종) + 약관 동의 체크박스 + "가입하기" 버튼 + 로그인 링크 | 폼 입력 → 유효성 검사 → 가입 완료 → 네이버 연동 페이지로 리다이렉트 |
| **네이버 계정 연동** | `/auth/naver` | 헤더 + "네이버로 로그인" 버튼 + 연동 설명 (3줄) | 버튼 클릭 → 네이버 로그인 팝업 → 권한 승인 → 토큰 저장 → 대시보드로 리다이렉트 |
| **기능 투어** | `/onboarding` | 스텝 1: 대시보드 소개 + "다음" 버튼 / 스텝 2: 리뷰 응답 소개 + "다음" 버튼 / 스텝 3: 성과 리포트 소개 + "완료" 버튼 | 각 스텝 클릭 → 다음 스텝으로 이동 → 완료 → 결제 페이지로 리다이렉트 |
| **결제 페이지** | `/checkout` | 헤더 + 플랜 선택 (주목/집중/시선 라디오 버튼) + 가격 표시 (할인가 강조) + "결제하기" 버튼 + 결제 수단 선택 (토스페이먼츠) | 플랜 선택 → 가격 업데이트 → "결제하기" 클릭 → 토스페이먼츠 팝업 → 결제 완료 → 대시보드로 리다이렉트 |
| **대시보드 (메인)** | `/dashboard` | 헤더 (로고 + 사용자명 + 플랜명) + 실시간 평점 카드 (큰 숫자 + 추이 화살표) + 리뷰 응답률 카드 + 이번 달 리뷰 수 카드 + 경쟁사 비교 카드 (막대 그래프) + 최근 리뷰 리스트 (5개) | 카드 클릭 → 상세 페이지로 이동 / 리뷰 클릭 → 리뷰 상세 페이지로 이동 |
| **리뷰 상세** | `/dashboard/reviews/:id` | 헤더 + 리뷰 내용 (별점 + 텍스트) + AI 자동 응답 제안 (회색 박스) + "이 응답으로 발송" 버튼 + "수정하기" 버튼 + "발송 안 함" 버튼 | "이 응답으로 발송" 클릭 → 네이버플레이스 API 호출 → "발송 완료" 메시지 표시 |
| **성과 리포트** | `/dashboard/report` | 헤더 + 월 선택 드롭다운 + 리포트 요약 (4개 KPI 카드: 응답률/평점/예약 증가/ROI) + 상세 그래프 (라인 차트 — 평점 추이) + "PDF 다운로드" 버튼 | 월 선택 → 리포트 업데이트 / "PDF 다운로드" 클릭 → PDF 생성 후 다운로드 |
| **설정** | `/settings` | 헤더 + 계정 정보 (이메일/사업장명/업종) + 네이버 연동 상태 + 플랜 정보 (현재 플랜/갱신일) + "플랜 변경" 버튼 + "구독 취소" 버튼 | "플랜 변경" 클릭 → 플랜 선택 페이지로 이동 / "구독 취소" 클릭 → 취소 확인 모달 표시 |
| **플랜 변경** | `/settings/plan` | 헤더 + 현재 플랜 강조 + 다른 플랜 카드 (주목/집중/시선) + "업그레이드" 또는 "다운그레이드" 버튼 | 플랜 선택 → "업그레이드" 클릭 → 결제 페이지로 이동 (차액 결제) |
| **고객 지원** | `/support` | 헤더 + FAQ (10개 Q&A) + 이메일 문의 폼 (제목/내용) + "제출" 버튼 | FAQ 클릭 → 답변 펼침 / 폼 입력 → "제출" 클릭 → "문의 완료" 메시지 표시 |

---

## 7. API 명세

### 7.1 인증 (Auth)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/auth/signup` | `{ email, password, businessName, businessType }` | `{ userId, token, refreshToken }` | 없음 |
| POST | `/api/auth/login` | `{ email, password }` | `{ userId, token, refreshToken }` | 없음 |
| POST | `/api/auth/refresh` | `{ refreshToken }` | `{ token }` | Refresh Token |
| GET | `/api/auth/naver/callback` | `{ code, state }` (쿼리 파라미터) | `{ userId, token, naverAccountId }` (리다이렉트) | 없음 |
| POST | `/api/auth/logout` | `{}` | `{ message: "로그아웃 완료" }` | Bearer Token |

### 7.2 진단 (Diagnosis)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/diagnosis/create` | `{ naverPlaceUrl, email }` | `{ diagnosisId, status: "pending" }` | 없음 |
| GET | `/api/diagnosis/:diagnosisId` | 없음 | `{ diagnosisId, score, rating, reviewResponseRate, seoScore, competitors: [...], createdAt }` | 없음 |
| POST | `/api/diagnosis/:diagnosisId/convert` | `{ planType: "starter\|pro\|enterprise" }` | `{ checkoutUrl }` (결제 페이지 리다이렉트) | 없음 |

### 7.3 리뷰 (Reviews)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/reviews` | `{ limit: 10, offset: 0, status: "pending\|responded\|ignored" }` | `{ reviews: [{ id, content, rating, author, createdAt, aiResponse, status }], total }` | Bearer Token |
| GET | `/api/reviews/:reviewId` | 없음 | `{ id, content, rating, author, createdAt, aiResponse, status, naverReviewId }` | Bearer Token |
| POST | `/api/reviews/:reviewId/respond` | `{ response, isAiGenerated: true\|false }` | `{ reviewId, status: "responded", naverResponseId }` | Bearer Token |
| POST | `/api/reviews/:reviewId/ignore` | `{}` | `{ reviewId, status: "ignored" }` | Bearer Token |
| POST | `/api/reviews/sync` | `{}` | `{ syncedCount, newReviews: [...] }` | Bearer Token |

### 7.4 대시보드 (Dashboard)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/dashboard/summary` | `{ period: "today\|week\|month" }` | `{ rating: 4.3, reviewResponseRate: 65%, newReviewsCount: 7, estimatedRevenueIncrease: 50000 }` | Bearer Token |
| GET | `/api/dashboard/rating-trend` | `{ period: "week\|month\|3months" }` | `{ data: [{ date, rating }], trend: "up\|down\|stable" }` | Bearer Token |
| GET | `/api/dashboard/competitors` | `{}` | `{ competitors: [{ name, rating, reviewCount, seoScore }] }` | Bearer Token |
| GET | `/api/dashboard/report/:month` | `{ month: "2024-09" }` | `{ month, rating, reviewResponseRate, estimatedRevenueIncrease, roi, pdf_url }` | Bearer Token |

### 7.5 설정 (Settings)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| GET | `/api/settings/account` | 없음 | `{ email, businessName, businessType, naverAccountId, createdAt }` | Bearer Token |
| PUT | `/api/settings/account` | `{ businessName, businessType }` | `{ email, businessName, businessType }` | Bearer Token |
| GET | `/api/settings/subscription` | 없음 | `{ planType: "pro", renewalDate: "2024-10-15", status: "active" }` | Bearer Token |
| POST | `/api/settings/subscription/cancel` | `{}` | `{ message: "구독이 취소되었습니다. 2024-10-15까지 서비스 이용 가능" }` | Bearer Token |
| POST | `/api/settings/subscription/upgrade` | `{ newPlanType: "enterprise" }` | `{ checkoutUrl }` (결제 페이지 리다이렉트) | Bearer Token |

### 7.6 결제 (Payment)

| Method | Endpoint | 요청 Body | 응답 | 인증 |
|--------|---------|-----------|------|------|
| POST | `/api/payment/create-order` | `{ planType: "starter\|pro\|enterprise", discountCode?: "FIRST30" }` | `{ orderId, amount, paymentKey, clientKey }` | Bearer Token |
| POST | `/api/payment/confirm` | `{ orderId, paymentKey, amount }` (토스페이먼츠 콜백) | `{ orderId, status: "success", subscriptionId }` | Webhook Secret |
| GET | `/api/payment/orders/:orderId` | 없음 | `{ orderId, amount, status: "pending\|success\|failed", createdAt }` | Bearer Token |

### 7.7 외부 API (네이버플레이스)

| Method | Endpoint (외부) | 요청 | 응답 | 인증 |
|--------|---------|------|------|------|
| GET | `https://place.naver.com/api/place/:placeId/reviews` | `{ limit: 100, offset: 0 }` | `{ reviews: [...], total }` | 네이버 API Key |
| GET | `https://place.naver.com/api/place/:placeId/info` | 없음 | `{ rating, reviewCount, category, address, phone, hours }` | 네이버 API Key |
| POST | `https://place.naver.com/api/place/:placeId/reviews/:reviewId/response` | `{ response }` | `{ responseId, status: "success" }` | 네이버 API Key + OAuth Token |

---

## 8. 데이터 모델

### 8.1 Users (사용자)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `id` | UUID | 사용자 고유 ID | PK |
| `email` | VARCHAR(255) | 이메일 | UNIQUE, NOT NULL |
| `passwordHash` | VARCHAR(255) | 비밀번호 해시 (bcrypt) | NOT NULL |
| `businessName` | VARCHAR(100) | 사업장명 | NOT NULL |
| `businessType` | ENUM('beauty', 'cafe', 'restaurant', 'clinic', 'academy') | 업종 | NOT NULL |
| `naverAccountId` | VARCHAR(100) | 네이버 계정 ID (OAuth) | UNIQUE, NULLABLE |
| `naverAccessToken` | TEXT | 네이버 API 액세스 토큰 (암호화) | NULLABLE |
| `naverRefreshToken` | TEXT | 네이버 API 리프레시 토큰 (암호화) | NULLABLE |
| `createdAt` | TIMESTAMP | 가입 일시 | DEFAULT CURRENT_TIMESTAMP |
| `updatedAt` | TIMESTAMP | 수정 일시 | DEFAULT CURRENT_TIMESTAMP |

### 8.2 Subscriptions (구독)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `id` | UUID | 구독 고유 ID | PK |
| `userId` | UUID | 사용자 ID | FK → Users.id |
| `planType` | ENUM('starter', 'pro', 'enterprise') | 플랜 유형 | NOT NULL |
| `status` | ENUM('active', 'cancelled', 'expired') | 구독 상태 | NOT NULL |
| `startDate` | DATE | 구독 시작일 | NOT NULL |
| `renewalDate` | DATE | 다음 갱신일 | NOT NULL |
| `cancelledAt` | TIMESTAMP | 취소 일시 | NULLABLE |
| `createdAt` | TIMESTAMP | 생성 일시 | DEFAULT CURRENT_TIMESTAMP |

### 8.3 Reviews (리뷰)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `id` | UUID | 리뷰 고유 ID | PK |
| `userId` | UUID | 사용자 ID | FK → Users.id |
| `naverReviewId` | VARCHAR(100) | 네이버 리뷰 ID | UNIQUE, NOT NULL |
| `content` | TEXT | 리뷰 내용 | NOT NULL |
| `rating` | INT (1-5) | 별점 | NOT NULL |
| `author` | VARCHAR(100) | 리뷰 작성자 | NOT NULL |
| `sentiment` | ENUM('positive', 'negative', 'neutral') | 감정 분류 (AI) | NOT NULL |
| `aiResponse` | TEXT | AI 자동 응답 제안 | NULLABLE |
| `status` | ENUM('pending', 'responded', 'ignored') | 응답 상태 | NOT NULL |
| `manualResponse` | TEXT | 사용자 수정 응답 | NULLABLE |
| `naverResponseId` | VARCHAR(100) | 네이버 응답 ID | NULLABLE |
| `createdAt` | TIMESTAMP | 리뷰 작성 일시 | NOT NULL |
| `respondedAt` | TIMESTAMP | 응답 일시 | NULLABLE |

### 8.4 RatingHistory (평점 추이)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `id` | UUID | 기록 고유 ID | PK |
| `userId` | UUID | 사용자 ID | FK → Users.id |
| `rating` | DECIMAL(2,1) | 평점 (예: 4.3) | NOT NULL |
| `reviewCount` | INT | 리뷰 총 개수 | NOT NULL |
| `responseRate` | INT (0-100) | 응답률 (%) | NOT NULL |
| `recordedAt` | TIMESTAMP | 기록 일시 | NOT NULL |

### 8.5 Diagnoses (진단)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `id` | UUID | 진단 고유 ID | PK |
| `email` | VARCHAR(255) | 신청자 이메일 | NOT NULL |
| `naverPlaceUrl` | VARCHAR(500) | 네이버플레이스 URL | NOT NULL |
| `naverPlaceId` | VARCHAR(100) | 네이버 장소 ID | NULLABLE |
| `status` | ENUM('pending', 'completed', 'converted') | 진단 상태 | NOT NULL |
| `score` | INT (0-100) | 종합 점수 | NULLABLE |
| `rating` | DECIMAL(2,1) | 평점 | NULLABLE |
| `reviewResponseRate` | INT (0-100) | 리뷰 응답률 (%) | NULLABLE |
| `seoScore` | INT (0-100) | SEO 점수 | NULLABLE |
| `competitors` | JSON | 경쟁사 비교 데이터 | NULLABLE |
| `createdAt` | TIMESTAMP | 신청 일시 | DEFAULT CURRENT_TIMESTAMP |
| `completedAt` | TIMESTAMP | 진단 완료 일시 | NULLABLE |
| `convertedAt` | TIMESTAMP | 유료 전환 일시 | NULLABLE |

### 8.6 Reports (월간 리포트)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `id` | UUID | 리포트 고유 ID | PK |
| `userId` | UUID | 사용자 ID | FK → Users.id |
| `month` | DATE | 리포트 월 (예: 2024-09-01) | NOT NULL |
| `reviewResponseRate` | INT (0-100) | 월간 응답률 (%) | NOT NULL |
| `ratingChange` | DECIMAL(2,1) | 평점 변화 (예: +0.2) | NOT NULL |
| `estimatedRevenueIncrease` | INT | 추정 매출 증가액 (원) | NOT NULL |
| `roi` | INT (0-200) | ROI (%) | NOT NULL |
| `pdfUrl` | VARCHAR(500) | PDF 리포트 URL (S3) | NULLABLE |
| `generatedAt` | TIMESTAMP | 생성 일시 | DEFAULT CURRENT_TIMESTAMP |

---

## 9. 성공 기준

### 9.1 OKR (1차 론칭 3개월 목표)

| KR | 측정 방법 | 목표치 | 현재치 (Day 0) | 임계값 (Go/No-Go) |
|-----|---------|--------|---------------|-----------------|
| **KR1**: 구독 고객 30개 사업장 확보 (MRR 1,470만원) | 대시보드 Subscriptions 테이블 COUNT (status='active') | 30명 | 0명 | 20명 이상 (67% 달성) = Go |
| **KR2**: AI 파이프라인 원가 40% 이하 유지 (건당 5만원 이하) | (고객 1명당 월 투입 시간 × 시급 + API 비용) ÷ 월 구독료 49만원 | ≤40% | 미측정 | 50% 이상 = No-Go (원가 구조 재설계 필요) |
| **KR3**: 3개월 유지율 70% 이상 (해지율 30% 미만) | (3개월 후 활성 구독 수) ÷ (초기 구독 수) | ≥70% | 0% (신규) | 50% 미만 = No-Go (AI 품질 또는 가격 문제) |

### 9.2 OMTM (One Metric That Matters)

| 지표 | 정의 | 측정 주기 | 목표 | 현재 |
|-----|------|---------|------|------|
| **naver-diagnosis 진단 → 결제 전환율** | (유료 전환 고객 수) ÷ (진단 신청 수) | 주간 | ≥30% | 0% (Day 0) |

**근거**: 이 지표가 30% 이상이면 KR1 (30명 확보)은 자동으로 달성됨. 역산: 30명 확보 = 진단 신청 100명 필요 (30 ÷ 0.3) → 네이버 카페 광고 월 50만원으로 1,000명 노출 → 신청 100명 (10% 전환율) 달성 가능.

### 9.3 고객 만족도 (NPS)

| 지표 | 정의 | 측정 주기 | 목표 | 측정 방법 |
|-----|------|---------|------|---------|
| **NPS (Net Promoter Score)** | "이 서비스를 친구에게 추천할 의향이 있나요?" (0~10점) | 월간 | ≥50 | 월말 이메일 설문 (고객 전체) |
| **CSAT (Customer Satisfaction)** | "서비스에 만족하나요?" (1~5점) | 월간 | ≥4.0 | 월말 인앱 팝업 설문 |
| **Churn Rate (월간)** | (해지 고객 수) ÷ (월초 활성 고객 수) | 월간 | ≤5% | 대시보드 Subscriptions 테이블 추적 |

### 9.4 기술 성능 (SLA)

| 지표 | 정의 | 목표 | 측정 도구 |
|-----|------|------|---------|
| **Uptime** | 서비스 가용성 | ≥99.5% | Sentry + CloudWatch |
| **API Response Time** | 평균 응답 시간 | ≤500ms (p95) | DataDog |
| **AI 응답 생성 시간** | 리뷰 발생 → AI 응답 생성까지 | ≤5분 | CloudWatch Logs |

---

## 10. 리스크

### 10.1 기술 리스크

| 리스크 | 심각도 | 발생 확률 | 대응 방안 |
|--------|--------|---------|---------|
| **네이버 API 정책 변경으로 크롤링 중단** | 높음 | 중간 (20%) | (1) 네이버 공식 API 문서 지속 모니터링 (2) 크롤링 대신 수동 입력 옵션 제공 (3) 네이버와 파트너십 협상 (P2) |
| **AI 리뷰 응답 품질 낮음 (프리랜서 대비)** | 높음 | 높음 (50%) | (1) OpenAI GPT-4 기반 프롬프트 최적화 (2) 사람 검수 + AI 학습 반복 (3) 초기 고객 3명 대상 품질 검증 후 확대 (4) 해지 시 "품질 개선" 피드백 수집 |
| **API 비용 초과 (OpenAI + 네이버)** | 중간 | 중간 (30%) | (1) API 사용량 모니터링 (DataDog) (2) 배치 처리로 API 호출 최소화 (3) 고객 수 증가 시 API 비용 협상 |

### 10.2 비즈니스 리스크

| 리스크 | 심각도 | 발생 확률 | 대응 방안 |
|--------|--------|---------|---------|
| **고객 획득 비용(CAC) 초과** | 높음 | 중간 (40%) | (1) 현재 CAC 추정 1.52만원 (네이버 카페 광고 50만원 + 인스타 광고 100만원 ÷ 99건 결제) — 실제 측정 후 조정 (2) 무료 채널(카카오 오픈채팅, 맘카페) 비중 확대 (3) 기존 고객 추천 프로그램 도입 (추천 1건당 1만원 할인) |
| **해지율 높음 (월 10% 이상)** | 높음 | 높음 (60%) | (1) 성과 리포트 자동화로 가시화 (월말 PDF 리포트) (2) 초기 고객 3명 대상 "평점 4.5 유지 보장" 성과 검증 (3) 해지 고객 대상 "품질 개선" 피드백 수집 (4) 전담 계정 매니저 추가 (시선 플랜 이상) |
| **경쟁사 진입 (Cafe24 기능 추가)** | 중간 | 높음 (70%) | (1) naver-diagnosis 자산으로 영업 훅

---

# V4 Framework (Pass 2)

## Aha Moment 정의

**Aha Moment:**
> 네이버플레이스 진단 결과에서 "평점 4.2, 리뷰 응답률 30%, 로컬 검색 2페이지" 문제를 즉시 인지한 후, AI 자동 리뷰 응답으로 첫 리뷰가 5분 내 자동 응답되는 순간.

**측정:**
- 가입부터 아하까지 예상 클릭 수 / 초
  - naver-diagnosis 신청 (1클릭) → 진단 결과 확인 (2초) → "집중 플랜 시작" 클릭 (1클릭) → 가입 (3클릭) → 네이버 연동 (1클릭) → 첫 리뷰 자동 응답 확인 (1클릭) = **총 7클릭, 120초**
- 목표: **60초 이내** (현재 추정 120초 → 온보딩 최적화로 60초 달성 가능)

**구현 방식:**
1. **온보딩 단축**: naver-diagnosis 진단 결과 페이지에서 "평점 4.2 → 4.5로 회복 보장" 메시지 + "지금 시작하기" 버튼 1개만 노출 (다른 플랜 선택지 숨김) → 클릭 수 2개 감소
2. **핵심 가치 즉시 노출**: 가입 완료 직후 "네이버플레이스 계정 연동" 페이지에서 "실시간 리뷰 모니터링 중..." 메시지 표시 → 첫 리뷰 발생 시 AI 자동 응답 팝업 즉시 표시 (대기 시간 제거)
3. **시각적 피드백**: 
   - AI 자동 응답 생성 중: 로딩 애니메이션 (1초)
   - 응답 완료: 초록색 체크마크 + "응답 완료" 토스트 메시지 (2초)
   - 대시보드 평점 실시간 업데이트: "평점 4.2 → 4.3 (↑0.1)" 숫자 강조 표시 (3초)

---

## JTBD Statement (민수 전략 → 서윤 Phase 1 기반)

**When I am** 네이버플레이스 평점이 4.2로 떨어져 예약이 줄어드는 상황에서,

**I want to** 리뷰 하나하나 수작업으로 응답하지 않고 AI가 24시간 자동으로 응답해주며, 로컬 검색 1페이지에 노출되도록 SEO 최적화되기를,

**so I can** 월 20시간 리뷰 관리 시간을 0시간으로 줄이고, 평점 4.5 이상 유지로 예약 20~30% 증가(월 200~300만원 매출 회복)하여, 장사에만 집중할 수 있다.

---

## Customer Forces Strategy (서윤 Phase 3 Canvas 기반)

### Push 요인 (경쟁사 불만 활용)

**현재 상태**: 
- Cafe24 사용 중 (네이버플레이스 단순 동기화만 지원, 리뷰 관리 기능 없음)
- 배달의민족 사용 중 (배달 음식 전용, 카페·뷰티숍 대상 아님)
- 수작업 + 프리랜서 고용 (월 30~50만원 비용 + 월 20시간 투입)

**경쟁사 불만** (서윤 Level 5 quote):
- "기존 툴에 돈 내고 있지만 기능 없어서 짜증" (Pain #4, 38세 피부과 원장, Cafe24 사용 중)
- "리뷰 하나하나 관리하느라 피곤" (Pain #2, 40세 헤어숍 사장, 수작업 중)
- "리뷰 응답 지연으로 평점 하락" (Pain #11, 37세 카페 운영자, "골목상권 생계 위협")

**우리의 Push**: 
> "Cafe24는 네이버플레이스 단순 동기화만, 배달의민족은 배달 음식 전용이라 카페·뷰티숍은 못 쓴다. 우리는 네이버플레이스 리뷰 자동 응답 + 로컬 SEO 최적화 + 정보 자동 업데이트를 한 곳에서 제공한다."

---

### Pull 요인 (차별 가치)

1. **AI 자동 리뷰 응답 (24시간 실시간)**
   - 구체적 가치: 리뷰 발생 시 5분 내 자동 응답 (긍정·부정·중립 자동 분류 + 맞춤 응답) → 월 20시간 수작업 → 0시간 절감, 야간 미응답으로 인한 평점 하락 방지
   - 근거: Pain #2 "리뷰 하나하나 관리하느라 피곤" (workaround_cost 월 20시간 + 통화비 10만원) + Pain #11 "리뷰 응답 지연으로 평점 하락" (current_solution_limit "야간 미응답")

2. **로컬 SEO 최적화 (키워드·카테고리·태그 자동 설정)**
   - 구체적 가치: 네이버 검색 알고리즘 분석하여 "강남 네일샵" 검색 시 1페이지 노출 보장 (3개월 내) → 로컬 검색 2~3페이지 → 1페이지, 신규 고객 유입 2배 증가
   - 근거: Pain #6 "네이버플레이스 SEO 최적화 모름" (JTBD goal "로컬 검색 1페이지 노출") + Pain #26 "네이버플레이스 카테고리 최적화" (노출 손실 월 100만원)

3. **네이버플레이스 정보 자동 업데이트 (메뉴·사진·영업시간·이벤트)**
   - 구체적 가치: 메뉴·사진 변경 시 1회 업로드하면 자동 동기화 + 캘린더 연동으로 영업시간·이벤트 자동 반영 → 월 10시간 + 월 5~8시간 수작업 → 1시간 절감, 고객 불만(영업시간 오류) 제로
   - 근거: Pain #14 "네이버플레이스 사진 업데이트 번거로움" (workaround_cost 월 10시간, current_solution_limit "퀄리티 불균일") + Pain #22 "네이버플레이스 이벤트 등록 잦은 변경" + Pain #31 "영업시간 업데이트 잦음"

---

### Inertia 감소 (전환 비용 최소화)

- **마이그레이션 도구**: 
  - Cafe24 사용 중인 고객: "Cafe24 네이버플레이스 연동 계정 → 우리 서비스로 1클릭 이전" 기능 제공 (데이터 손실 없음)
  - 수작업 중인 고객: "기존 리뷰 응답 기록 CSV 업로드" 기능 제공 (학습 데이터로 활용)
  - 프리랜서 고용 중인 고객: "프리랜서 계정 → 우리 AI로 전환" 가이드 제공 (비용 절감 계산기 포함)

- **학습 곡선 최소화**: 
  - 온보딩 플로우: 가입 → 네이버 연동 → 첫 진단 → 기능 투어 (3단계, 5분 소요)
  - 인앱 튜토리얼: 각 기능별 "?" 아이콘 클릭 시 30초 비디오 가이드 재생
  - 템플릿 제공: "AI 리뷰 응답 템플릿" 10개 사전 제공 (고객이 커스터마이즈 가능)

- **팀 확산**: 
  - 초대 기능: 사장 → 직원 초대 (권한 설정: 읽기 전용 / 응답 권한 / 관리자)
  - 공유 기능: 월 성과 리포트 "공유 링크" 생성 → 직원/가족에게 메일 발송 (로그인 불필요)
  - 팀 협업: 리뷰 응답 시 "사장 승인 필요" 옵션 (AI 응답 → 사장 검토 → 발송 워크플로우)

---

### Anxiety 해소 (신뢰 신호)

- **무료 체험**: 
  - naver-diagnosis 무료 진단 (선착순 20명 또는 월 100명 제한)
  - 범위: 평점·리뷰 응답률·SEO 점수·경쟁사 비교 (5분 내 결과 제공)
  - 조건: 이메일 입력만 필수, 신용카드 불필요
  - 목표: 진단 → 문제 인지 → 즉시 결제 전환 (추정 전환율 30%)

- **보증**: 
  - **평점 4.5 유지 보장**: 3개월 내 평점 4.5 이상 유지 못 시 "3개월 무료 연장" (단, 리뷰 발생 월 50건 이상 조건)
  - **환불 정책**: 첫 달 30일 내 해지 시 100% 환불 (신용카드 결제 취소)
  - **SLA**: 리뷰 응답 5분 이내 (99.5% 달성 목표), 미달 시 해당 월 구독료 10% 할인
  - **데이터 안전**: 네이버플레이스 계정 정보는 암호화 저장, 고객 요청 시 언제든 삭제 가능

- **사회적 증거**: 
  - **레퍼런스**: "35세 네일샵 원장, 평점 4.2 → 4.5 회복 (3개월), 예약 25% 증가" 사례 공개
  - **후기**: 구글 리뷰 / 네이버 카페 추천글 (초기 고객 3명 대상 무료 제공 후 후기 수집)
  - **케이스 스터디**: "강남 헤어숍, 월 리뷰 50건 → AI 자동 응답으로 응답률 30% → 65% 개선" PDF 다운로드 제공
  - **언론**: 초기 론칭 시 "소상공인 AI 마케팅 대행" 주제로 스타트업 매체 보도 유도

---

## Evidence Appendix (기능 ↔ 페인포인트 trace)

### P0 기능 1: AI 자동 리뷰 응답

> "리뷰 하나하나 관리하느라 피곤"
— https://cafe.naver.com/smallbusiness (Level 4, 40세 헤어숍 사장, 3인 사업장, 월 매출 1,200만원)

**반영 방식**: 이 quote는 Pain #2의 핵심 불만으로, "월 20시간 수작업 + 통화비 10만원"이라는 구체적 workaround_cost를 드러냅니다. 우리의 "AI 자동 리뷰 응답 (24시간 실시간, 긍정·부정·중립 자동 분류 + 맞춤 응답)"은 이 수작업을 완전히 제거합니다. MVP 기능 우선순위 P0로 설정한 근거입니다.

---

### P0 기능 2: 24시간 실시간 모니터링

> "리뷰 응답 지연으로 평점 하락" (골목상권 생계 위협)
— http://www.justice-platform.org/home/post_view.php?nd=270 (Level 4, 37세 카페 운영자, 2인 사업장, current_solution_limit "야간 미응답")

**반영 방식**: 이 quote는 Pain #11의 핵심으로, "야간·주말 리뷰 미응답으로 인한 평점 하락 → 예약 취소 월 50~100만원 매출 손실"을 의미합니다. 우리의 "24시간 실시간 모니터링 + 푸시 알림"은 야간 미응답 문제를 완전히 해결합니다. P0 기능으로 설정한 근거입니다.

---

### P0 기능 3: 평점 관리 대시보드

> "성과 지표 추적 다중 툴" (구글 시트 수동 합산, 월 12시간)
— https://blog.naver.com/graff-rindellheiger/224057332389 (Level 4, 37세 식당 사장, 5인 사업장, Pain #35)

**반영 방식**: 이 quote는 Pain #35의 workaround_cost "월 12시간 수동 합산"을 드러냅니다. 우리의 "평점 관리 대시보드 (실시간 평점·리뷰 추이·경쟁사 비교, 그래프 + 수치)"는 다중 툴 사용을 제거하고 단일 대시보드에서 모든 성과를 추적하게 합니다. 고객이 "성과를 본다" 느낌을 주어 해지율 관리에 핵심 기능입니다. P0로 설정.

---

### P0 기능 4: 로컬 SEO 최적화

> "네이버플레이스 SEO 최적화 모름" (로컬 검색 2~3페이지 노출, 신규 고객 유입 저조)
— http://www.justice-platform.org/home/post_view.php?nd=270 (Level 3, 30세 네일아트숍 원장, 1인 사업장, Pain #6, JTBD goal "로컬 검색 1페이지 노출")

**반영 방식**: 이 quote는 Pain #6의 핵심으로, "네이버플레이스 SEO 최적화 방법 모름 → 로컬 검색 2~3페이지 노출 → 신규 고객 유입 저조"를 의미합니다. 우리의 "로컬 SEO 최적화 (키워드·카테고리·태그 자동 설정)"는 네이버 검색 알고리즘을 분석하여 1페이지 노출을 보장합니다. P0 기능으로 설정한 근거입니다.

---

### P0 기능 5: 월 성과 리포트 자동 생성

> "월 마케팅 리포트 클라이언트 공유 어려움" (PDF 메일 발송, 월 20시간)
— https://cafe.naver.com/smallbusiness (Level 5, 34세 피부샵 사장, 1인 사업장, Pain #24)

**반영 방식**: 이 quote는 Pain #24의 workaround_cost "월 20시간 PDF 작성"을 드러냅니다. 우리의 "월 성과 리포트 자동 생성 (리뷰 응답률·평점 변화·예약 증가율 자동 계산 + PDF 리포트 생성)"은 이 수작업을 완전히 제거합니다. 고객 신뢰 확보 + 해지율 관리 (성과 가시화)에 핵심 기능입니다. P0로 설정.

---

### P0 기능 6: naver-diagnosis 무료 진단

> "기존 툴에 돈 내고 있지만 기능 없어서 짜증"
— https://www.g2.com/categories/marketing-automation (Level 5, 38세 피부과 에스테 원장, 4인 사업장, Pain #4, Cafe24 사용 중)

**반영 방식**: 이 quote는 Pain #4의 핵심으로, Cafe24 사용 중인 고객이 "SNS 광고 연동만 되고 실제 광고 운영(A/B 테스트, 타겟팅 최적화)은 수동"이라는 불만을 드러냅니다. 우리의 "naver-diagnosis 무료 진단 (평점·리뷰 응답률·SEO 점수·경쟁사 비교)"은 Cafe24 사용자도 유입시킬 수 있는 영업 훅입니다. 진단 → 문제 인지 → 유료 전환 (추정 전환율 30%)의 핵심 기능입니다. P0로 설정.

---

### P0 기능 7: 고객 온보딩 플로우

> "엑셀/수작업으로 버티는 중" (온보딩 가이드 부재, 학습 곡선 높음)
— http://www.justice-platform.org/home/post_view.php?nd=270 (Level 4, 다수 페르소나, Pain #3, #8, #35)

**반영 방식**: 이 quote는 소상공인들이 "새로운 도구 도입 시 학습 곡선이 높아 포기하는" 패턴을 드러냅니다. 우리의 "고객 온보딩 플로우 (가입 → 네이버플레이스 계정 연동 → 첫 진단 → 기능 투어, 3단계 5분 소요)"는 초기 고객 이탈을 방지합니다. P0 기능으로 설정한 근거입니다.

---

### P0 기능 8: 결제 시스템

> "플랫폼 수수료로 마케팅 예산 없음" (월 100만원 손실)
— https://www.newstomato.com/ReadNewspaper.aspx?epaper=1&no=837112 (Level 4, 42세 식당 사장, 5인 사업장, Pain #5)

**반영 방식**: 이 quote는 Pain #5의 핵심으로, 소상공인들이 "배달앱 수수료 때문에 마케팅 예산이 없다"는 불만을 드러냅니다. 우리의 "결제 시스템 (토스페이먼츠 연동, 월 구독 자동 갱신)"은 명확한 월 고정비 구조를 제공하여, 고객이 "월 49만원 투자 → 월 50~100만원 매출 회복"의 ROI를 명확히 계산할 수 있게 합니다. 수익화 필수 기능입니다. P0로 설정.

---

### P1 기능 1: 네이버플레이스 정보 자동 업데이트

> "네이버플레이스 사진 업데이트 번거로움" (월 10시간, 퀄리티 불균일)
— http://www.justice-platform.org/home/post_view.php?nd=270 (Level 4, 31세 피부샵 원장, 2인 사업장, Pain #14)

**반영 방식**: 이 quote는 Pain #14의 workaround_cost "월 10시간 휴대폰 촬영 + 업로드"를 드러냅니다. 우리의 "네이버플레이스 정보 자동 업데이트 (메뉴·사진·영업시간·이벤트 캘린더 연동)"는 이 수작업을 월 10시간 → 1시간으로 감소시킵니다. P1 기능으로 설정한 근거입니다.

---

### P1 기능 2: 부정 리뷰 대응 자동화

> "리뷰 하나하나 관리하느라 피곤" (부정 리뷰 수정 요청 전화 통화, 월 20시간)
— https://cafe.naver.com/smallbusiness (Level 4, 40세 헤어숍 사장, 3인 사업장, Pain #2, current_solution_limit "부정 리뷰 수정 요청 전화")

**반영 방식**: 이 quote는 Pain #2의 세부 workaround "부정 리뷰 발생 시 고객 전화로 수정 요청"을 드러냅니다. 우리의 "부정 리뷰 대응 자동화 (부정 리뷰 발생 시 고객에게 '대응 템플릿' 제안, 사람이 최종 승인 후 발송)"는 이 전화 통화를 간접적으로 해결합니다. P1 기능으로 설정.

---

### P1 기능 3: 인스타그램 콘텐츠 자동 생성

> "인스타그램 콘텐츠 직접 제작하니 시간 없어 장사에 집중 못 함" (주 10시간, 월 40만원 상당)
— https://cafe.naver.com/beautyowners (Level 4, 35세 네일샵 원장, 2인 사업장, Pain #1, evidence_quote "인스타 직접 올리다 지쳐서 포기한 상태")

**반영 방식**: 이 quote는 Pain #1의 핵심으로, "주말에 직접 촬영·편집하느라 지쳐서 포기"하는 패턴을 드러냅니다. 우리의 "인스타그램 콘텐츠 자동 생성 (AI 이미지 생성 + 캡션 자동 작성, 주 3회, 집중 플랜 이상)"은 이 수작업을 완전히 제거합니다. Pain #1 직접 해결 기능입니다. P1로 설정.

---

### P1 기능 4: 인스타 광고 A/B 테스트 자동화

> "인스타 광고 운영 스킬 없어 돈만 날림" (월 50만원 프리랜서 고용)
— https://www.g2.com/categories/marketing-automation (Level 5, 38세 피부과 에스테 원장, 4인 사업장, Pain #4, evidence_quote "기존 툴에 돈 내고 있지만 기능 없어서 짜증")

**반영 방식**: 이 quote는 Pain #4의 핵심으로, Cafe24 같은 기존 툴이 "광고 플랫폼 연결만 하고 실제 광고 운영(A/B 테스트, 타겟팅 최적화)은 수동"이라는 불만을 드러냅니다. 우리의 "인스타 광고 A/B 테스트 자동화 (크리에이티브 2개 자동 생성 + 성과 비교, 시선 플랜 이상)"는 Pain #4 직접 해결 기능입니다. P1로 설정.

---

### P1 기능 5: 블로그 체험단 매칭 플랫폼

> "블로그 체험단 모집 엑셀로 관리하니 오류 잦음" (월 15시간 + 프리랜서 20만원)
— http://www.justice-platform.org/home/post_view.php?nd=270 (Level 5, 32세 카페 사장, 1인 사업장, Pain #3, evidence_quote "엑셀/수작업으로 버티는 중")

**반영 방식**: 이 quote는 Pain #3의 핵심으로, "엑셀 시트 참가자 추적 → 데이터 누락 → 이벤트 실패"의 패턴을 드러냅니다. 우리의 "블로그 체험단 매칭 플랫폼 (체험단 모집 → 블로거 자동 매칭 → 포스팅 일정 관리, 시선 플랜 이상)"은 이 엑셀 관리를 완전히 제거합니다. Pain #3 직접 해결 기능입니다. P1로 설정.

---

### P1 기능 6: 통합 성과 대시보드

> "성과 지표 추적 다중 툴" (인스타 분석 + 네이버 분석 + 블로그 분석 + 구글 시트 수동 합산, 월 12시간)
— https://blog.naver.com/graff-rindellheiger/224057332389 (Level 4, 37세 식당 사장, 5인 사업장, Pain #35)

**반영 방식**: 이 quote는 Pain #35의 workaround_cost "월 12시간 다중 툴 합산"을 드러냅니다. 우리의 "통합 성과 대시보드 (인스타+네이버+블로그 성과 한 화면에서 추적, P1 기능 추가 후)"는 이 수작업을 완전히 제거합니다. P1 기능으로 설정한 근거입니다.

---

### P2 기능 1: 네이버 광고 대행

> "인스타 광고 운영 스킬 없어 돈만 날림" (월 50만원 프리랜서 고용, 타겟팅 부정확)
— https://www.g2.com/categories/marketing-automation (Level 5, 38세 피부과 에스테 원장, 4인 사업장, Pain #4)

**반영 방식**: 이 quote는 Pain #4의 확장으로, "인스타 광고뿐 아니라 네이버 광고도 전문가 운영 필요"를 의미합니다. 우리의 "네이버 광고 대행 (월 광고비 50만원 포함, 추가 광고비는 10% 수수료)"은 Pain #4를 완전히 해결하는 업셀링 기능입니다. P2로 설정.

---

### P2 기능 2: 전담 계정 매니저

> "리