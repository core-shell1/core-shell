# 토지 사업성 분석 자동화 SaaS — PRD (Product Requirements Document)

## 제품 개요

부동산 개발업체·시행사·건축사무소 대상으로, 토지 개요서·법률서 업로드 시 **48시간 내 인허가 승인 확률 자동 산출 + 유사 사례 3건 제시**하여 의사결정 속도를 3배 향상하고 매입 후 거절 손실(평균 5억 원)을 사전 제거하는 B2B SaaS.

---

## 기술 스택

- **FE**: React 18 + TypeScript + Tailwind CSS (반응형 웹앱 + 모바일 지원)
  - 라이브러리: React Query (데이터 페칭), Zustand (상태 관리), React Hook Form (폼 검증)
  - PDF 뷰어: PDF.js (업로드된 개요서 미리보기)
  
- **BE**: Python 3.11 + FastAPI (비동기 API 서버)
  - 라이브러리: SQLAlchemy (ORM), Pydantic (데이터 검증), python-docx (문서 파싱)
  - OCR: Tesseract 또는 AWS Textract (PDF → 텍스트 추출)
  - ML: scikit-learn (초기 로지스틱 회귀 모델) → 추후 XGBoost 또는 LightGBM 고도화
  
- **DB**: PostgreSQL 15 (관계형 데이터 저장) + Redis (캐시, 세션 관리)
  - 스키마: 사용자(users), 프로젝트(projects), 분석 결과(analyses), 과거 사례(case_studies)
  
- **인프라**: AWS (EC2 + RDS + S3 + Lambda)
  - 배포: Docker + ECS (컨테이너 오케스트레이션)
  - CI/CD: GitHub Actions
  - 모니터링: CloudWatch + Sentry (에러 추적)

---

## 기능 목록

> **P0 = MVP 필수 (6개월 내 출시)**  
> **P1 = 1차 출시 후 (6~12개월)**  
> **P2 = 나중에 (12개월 이후)**

| 우선순위 | 기능 | 설명 | 이유 | 의존 기능 |
|---------|------|------|------|---------|
| **P0** | 사용자 인증 (회원가입/로그인) | 이메일 기반 회원가입 + 비밀번호 해싱 (bcrypt) + JWT 토큰 기반 세션 관리 | MVP 필수: 사용자 데이터 격리 | 없음 |
| **P0** | 개요서 PDF 업로드 | 최대 10MB PDF 파일 업로드 → S3 저장 + 파일 메타데이터(파일명, 업로드 시간, 사용자 ID) 저장 | 핵심 입력 인터페이스 | 사용자 인증 |
| **P0** | OCR (텍스트 추출) | 업로드된 PDF → AWS Textract 또는 Tesseract로 텍스트 추출 → 추출된 텍스트 DB 저장 | 개요서 자동 분석의 전제 | 개요서 PDF 업로드 |
| **P0** | 지자체 기준 DB (용도지역, 건폐율, 용적률) | 서울/경기 주요 지자체 25곳 기준 정보 (용도지역, 건폐율, 용적률, 높이 제한 등) 수동 입력 → 매월 1회 업데이트 | 인허가 승인 확률 산출의 기초 데이터 | 없음 |
| **P0** | 인허가 승인 확률 ML 모델 (초기) | 과거 인허가 데이터 100~300건 학습 → 로지스틱 회귀 모델 → 입력(지자체, 용도지역, 건폐율, 용적률) → 출력(승인 확률 %) | Pain #2 핵심 기능: "인허가 거절 위험 사전 제거" | 지자체 기준 DB, OCR |
| **P0** | 유사 사례 매칭 (초기) | 입력된 토지 정보(지자체, 용도지역, 건폐율) → 과거 승인/거절 사례 DB에서 유사도 90% 이상 사례 3건 자동 검색 | Pain #21 "분양성 판단 시 객관적 근거 제공" | 인허가 승인 확률 ML 모델 |
| **P0** | 리포트 생성 (PDF) | 승인 확률 % + 신뢰도 ★★★★☆ + 유사 사례 3건 + 지자체 기준 정보 → PDF 리포트 자동 생성 | 사용자에게 최종 산출물 제공 | 인허가 승인 확률 ML 모델, 유사 사례 매칭 |
| **P0** | 리포트 이메일 발송 | 리포트 생성 완료 후 사용자 이메일로 PDF 자동 발송 (SendGrid 또는 AWS SES) | 사용자 편의성: 48시간 내 자동 전달 | 리포트 생성 |
| **P0** | 대시보드 (분석 이력 조회) | 사용자가 지금까지 분석한 모든 프로젝트 목록 조회 (프로젝트명, 분석 날짜, 승인 확률, 상태) | 사용자가 과거 분석 결과 재확인 가능 | 사용자 인증 |
| **P0** | 가격 플랜 페이지 + 결제 | Starter (14일 무료, 1건) / Pro (월 69만원, 월 10건) / Enterprise (월 150만원, 무제한) → Stripe 또는 PG사 결제 연동 | 수익화 필수 | 사용자 인증 |
| **P1** | 특례법 자동 판독 (NLP) | 도시재생법, 주거환경개선사업법 등 주요 특례법 텍스트 DB 구축 → NLP 모델로 개요서에서 특례법 자동 감지 → "해당 여부: Yes/No" + 근거 조항 인용 | Pain #3, #29 "특례법 변호사 리뷰 월 300만원 → 자동화" | OCR, 지자체 기준 DB |
| **P1** | 현금흐름 시뮬레이터 (What-If) | 금리, 건설비, 분양가 입력 → 현금흐름 자동 계산 → "금리 ±0.5% 변화 시 ROI 재계산" 시나리오 제공 | Pain #4, #20, #28, #30 "투자 금액·수익성 자동 산출" | 없음 (독립 기능) |
| **P1** | 부동산 정책 모니터링 (뉴스 크롤링) | 부동산 정책 뉴스 자동 크롤링 (네이버 뉴스, 정책브리핑) → 키워드 분류 (도시재생, 분양가상한제, 재건축 등) → 주간 요약 리포트 이메일 발송 | Pain #5, #18, #27 "정책 변화 실시간 모니터링" | 없음 (독립 기능) |
| **P1** | 토지 가격 적정성 평가 (감정평가 로직) | 토지 가격 배점 기준 자동 적용 (위치, 접근성, 용도지역 등) → 시세 비교 대시보드 (부동산114 API 연동) → "적정 가격 범위" 제시 | Pain #6, #17, #24 "토지 가격 과다 매입 방지" | 없음 (독립 기능) |
| **P1** | API 제공 (Enterprise용) | 자사 시스템에서 우리 API 호출 → 분석 결과 JSON 반환 | Enterprise 고객 자동화 요구 | 인허가 승인 확률 ML 모델 |
| **P1** | 전담 컨설턴트 (Enterprise용) | Enterprise 고객 대상 월 2회 화상 미팅 (분석 결과 해석, 전략 수립 지원) | Enterprise 고객 유지율 향상 | 없음 (서비스 기능) |
| **P2** | 모바일 앱 (iOS/Android) | React Native 또는 Flutter로 모바일 앱 개발 → 현장에서 토지 사진 촬영 후 분석 | 사용자 편의성 (현장 확인 시) | 웹앱 완성 후 |
| **P2** | 머신러닝 고도화 (XGBoost/LightGBM) | 초기 로지스틱 회귀 → XGBoost 또는 LightGBM으로 모델 고도화 → 정확도 75% → 80% 향상 | 예측 정확도 개선 | 인허가 승인 확률 ML 모델 (초기) |
| **P2** | 지자체별 담당자 연동 (API) | 지자체 인허가 담당자와 API 연동 → 실시간 인허가 기준 업데이트 (월 1회 → 실시간) | 데이터 최신성 보장 | 지자체 기준 DB |

---

## Must NOT (범위 외)

- **법률 자문 제공** — "이 토지는 반드시 승인됩니다"라는 법적 보증 금지. 우리는 "과거 데이터 기반 확률 제시"만 제공. 법적 책임은 사용자 또는 변호사에게 귀속 (면책 조항 필수)
- **감정평가 자격증 대체** — 공식 감정평가사 자격증 없이 "감정평가" 용어 사용 금지. 대신 "토지 가격 적정성 평가" 또는 "시세 비교 분석"으로 표현 (P1 기능, 법률 검토 필수)
- **실시간 인허가 기준 업데이트** — MVP 단계에서는 지자체 기준을 월 1회 수동 업데이트만 제공. 실시간 업데이트는 P2 (지자체 API 연동 필요)
- **다른 부동산 도메인 확장** — 초기는 "토지 인허가 승인 확률"만 집중. 주택 분양가, 상업용부동산 임대료 등 다른 도메인은 범위 외
- **국제 시장 진출** — MVP는 한국(서울/경기) 지역만 대상. 해외 진출은 P2 이후

---

## User Flow

### 시나리오 1: 신규 사용자 (시행사 대표) — 첫 토지 분석

**목표**: 토지 개요서 업로드 → 48시간 내 인허가 승인 확률 리포트 수신 → 의사결정

1단계: 사용자가 웹사이트 방문 → "14일 무료 체험" CTA 클릭 → 회원가입 페이지 이동
- 시스템 응답: 회원가입 폼 표시 (이메일, 비밀번호, 회사명, 직급)

2단계: 사용자가 이메일 입력 후 "가입" 버튼 클릭
- 시스템 응답: 인증 이메일 발송 → 사용자가 이메일 링크 클릭 → 계정 활성화

3단계: 사용자가 대시보드 진입 → "새 프로젝트" 버튼 클릭
- 시스템 응답: 프로젝트 생성 폼 표시 (프로젝트명, 지자체, 용도지역 선택)

4단계: 사용자가 프로젝트명("강남구 토지 A") 입력 → 지자체 드롭다운에서 "서울 강남구" 선택 → 용도지역 드롭다운에서 "상업지역" 선택
- 시스템 응답: 폼 검증 완료 → "다음" 버튼 활성화

5단계: 사용자가 "다음" 클릭 → 개요서 PDF 업로드 페이지 이동
- 시스템 응답: 파일 업로드 인터페이스 표시 (드래그 앤 드롭 또는 파일 선택)

6단계: 사용자가 개요서 PDF 파일(10MB 이하) 드래그 앤 드롭 → 업로드 시작
- 시스템 응답: 파일 S3 업로드 시작 → 진행률 표시 (0% → 100%) → 업로드 완료 후 "분석 시작" 버튼 활성화

7단계: 사용자가 "분석 시작" 버튼 클릭
- 시스템 응답: 
  - 백엔드에서 비동기 작업 시작 (Celery 또는 AWS Lambda)
  - 사용자에게 "분석 중입니다. 48시간 내 이메일로 리포트를 보내드리겠습니다" 메시지 표시
  - 대시보드에서 프로젝트 상태 = "분석 중" (진행률 표시)

8단계: 백엔드 비동기 작업 (48시간 이내):
- OCR 실행: PDF → 텍스트 추출 (Textract 또는 Tesseract)
- 지자체 기준 매칭: 추출된 텍스트에서 건폐율, 용적률 파싱 → 지자체 기준 DB와 비교
- ML 모델 실행: 입력(지자체, 용도지역, 건폐율, 용적률) → 로지스틱 회귀 모델 → 승인 확률 % 산출 (예: 78%)
- 유사 사례 검색: 입력 정보 → 과거 사례 DB에서 유사도 90% 이상 사례 3건 검색
- 리포트 생성: 승인 확률 78% + 신뢰도 ★★★★☆ + 유사 사례 3건 + 지자체 기준 정보 → PDF 리포트 자동 생성
- 이메일 발송: 리포트 PDF를 사용자 이메일로 발송 (SendGrid)

9단계: 사용자가 이메일에서 리포트 PDF 다운로드 → 열어보기
- 시스템 응답: PDF 리포트 표시
  - 제목: "강남구 토지 A — 인허가 승인 확률 분석 리포트"
  - 내용:
    - 승인 확률: 78% (신뢰도 ★★★★☆)
    - 지자체 기준: 용도지역 상업지역, 건폐율 80%, 용적률 400%
    - 유사 사례 3건:
      - 사례 1: 강남구 토지 B (2022년 승인, 유사도 95%)
      - 사례 2: 강남구 토지 C (2021년 승인, 유사도 92%)
      - 사례 3: 서초구 토지 D (2023년 거절, 유사도 91%)

10단계: 사용자가 리포트 검토 후 "이 토지 매입하자" 또는 "이 토지 패스하자" 의사결정
- 시스템 응답: 없음 (사용자 의사결정 단계)

11단계: 사용자가 2건째 분석 시도 → "새 프로젝트" 클릭
- 시스템 응답: Paywall 노출 → "Pro 플랜(월 69만원) 가입 필요합니다. 지금 가입하고 다음 달 50% 할인 받으세요" 메시지 + CTA "지금 가입"

---

### 시나리오 2: 유료 고객 (Pro 플랜) — 월 10건 분석

**목표**: 월 10건 토지 분석 → 의사결정 속도 3배 향상 (기존 2주 → 48시간)

1단계: 사용자가 Pro 플랜 가입 (월 69만원) → Stripe 결제 완료
- 시스템 응답: 결제 확인 이메일 발송 → 계정 업그레이드 (Pro 플랜 활성화) → 대시보드에서 "월 10건 분석 가능" 표시

2단계: 사용자가 대시보드 진입 → "새 프로젝트" 클릭 → 프로젝트 생성 (반복)
- 시스템 응답: 프로젝트 생성 폼 표시

3단계: 사용자가 월 10건 분석 → 각 분석마다 48시간 내 리포트 수신
- 시스템 응답: 각 분석마다 비동기 작업 실행 → 리포트 PDF 이메일 발송

4단계: 사용자가 월 11건째 분석 시도
- 시스템 응답: "월 10건 한도 초과. 추가 분석은 건당 8만원입니다. 지금 추가 결제하시겠습니까?" 메시지 + CTA "추가 결제" 또는 "Enterprise 플랜으로 업그레이드(월 150만원, 무제한)"

---

### 시나리오 3: Enterprise 고객 — API 연동 + 전담 컨설턴트

**목표**: 자사 시스템에서 우리 API 호출 → 분석 결과 자동 통합 → 월 2회 컨설턴트 미팅

1단계: Enterprise 고객이 가입 (월 150만원) → API 키 발급
- 시스템 응답: API 문서 페이지 제공 (엔드포인트, 요청/응답 형식, 인증 방식)

2단계: 고객이 자사 시스템에서 우리 API 호출
- 요청: POST /api/v1/analyze (토지 정보 JSON)
- 응답: 승인 확률 %, 유사 사례 3건 JSON

3단계: 고객이 월 2회 전담 컨설턴트와 화상 미팅 (Zoom)
- 시스템 응답: 미팅 일정 자동 예약 (Calendly 또는 자체 예약 시스템) → 미팅 전 분석 결과 요약 이메일 발송

---

## 화면 명세

| 화면명 | URL/Route | 핵심 컴포넌트 | 동작 |
|--------|-----------|-------------|------|
| **랜딩 페이지** | `/` | 헤드라인 ("토지 매입 전 인허가 거절 위험 75% 제거"), 서브헤드 ("48시간 내 승인 확률 자동 산출"), CTA ("14일 무료 체험"), 가격 플랜 카드 (Starter/Pro/Enterprise), FAQ, 고객 후기 | 사용자가 "14일 무료 체험" 클릭 → 회원가입 페이지 이동 |
| **회원가입** | `/auth/signup` | 이메일 입력, 비밀번호 입력, 회사명 입력, 직급 선택 드롭다운, "가입" 버튼 | 사용자가 정보 입력 → "가입" 클릭 → 인증 이메일 발송 → 이메일 링크 클릭 → 계정 활성화 |
| **로그인** | `/auth/login` | 이메일 입력, 비밀번호 입력, "로그인" 버튼, "비밀번호 찾기" 링크 | 사용자가 이메일/비밀번호 입력 → "로그인" 클릭 → JWT 토큰 발급 → 대시보드 리다이렉트 |
| **대시보드 (메인)** | `/dashboard` | 좌측 사이드바 (네비게이션: 대시보드, 분석 이력, 설정, 로그아웃), 메인 영역 (프로젝트 목록 테이블: 프로젝트명, 분석 날짜, 승인 확률, 상태), "새 프로젝트" 버튼 | 사용자가 "새 프로젝트" 클릭 → 프로젝트 생성 페이지 이동 |
| **프로젝트 생성 (Step 1)** | `/projects/create/step1` | 프로젝트명 입력, 지자체 드롭다운 (서울/경기 25곳), 용도지역 드롭다운 (주거/상업/공업 등), "다음" 버튼 | 사용자가 정보 입력 → "다음" 클릭 → Step 2로 이동 |
| **프로젝트 생성 (Step 2)** | `/projects/create/step2` | 개요서 PDF 업로드 (드래그 앤 드롭 또는 파일 선택), 파일 미리보기 (PDF.js), 업로드 진행률 표시, "분석 시작" 버튼 | 사용자가 PDF 업로드 → "분석 시작" 클릭 → 비동기 작업 시작 → "분석 중" 상태 표시 |
| **분석 결과 (대기 중)** | `/projects/{projectId}/analyzing` | 프로젝트명, "분석 중입니다. 48시간 내 이메일로 리포트를 보내드리겠습니다" 메시지, 진행률 표시 (0% → 100%), 예상 완료 시간 | 사용자가 페이지 새로고침 → 진행률 업데이트 (실시간 또는 폴링) |
| **분석 결과 (완료)** | `/projects/{projectId}/result` | 프로젝트명, 승인 확률 % (큰 폰트), 신뢰도 ★★★★☆, 지자체 기준 정보 (용도지역, 건폐율, 용적률), 유사 사례 3건 (카드 형식), "리포트 다운로드" 버튼, "새 프로젝트" 버튼 | 사용자가 "리포트 다운로드" 클릭 → PDF 다운로드 또는 "새 프로젝트" 클릭 → Step 1로 이동 |
| **분석 이력** | `/projects/history` | 프로젝트 목록 테이블 (프로젝트명, 분석 날짜, 승인 확률, 상태, 액션: 상세보기/삭제), 필터 (지자체, 용도지역, 날짜 범위), 페이지네이션 | 사용자가 프로젝트 클릭 → 상세 결과 페이지 이동 또는 "삭제" 클릭 → 삭제 확인 → 삭제 |
| **가격 플랜** | `/pricing` | 3개 플랜 카드 (Starter/Pro/Enterprise), 각 카드에 월 가격, 포함 내용, "선택" 또는 "업그레이드" 버튼, 비교 테이블 (기능별 포함 여부) | 사용자가 "선택" 클릭 → 결제 페이지 이동 (Stripe) |
| **결제** | `/checkout` | 플랜 정보 (월 가격, 포함 내용), 결제 정보 입력 (카드번호, 유효기간, CVC), "결제" 버튼 | 사용자가 결제 정보 입력 → "결제" 클릭 → Stripe API 호출 → 결제 완료 → 확인 이메일 발송 → 대시보드 리다이렉트 |
| **설정** | `/settings` | 계정 정보 (이메일, 회사명, 직급), 구독 정보 (현재 플랜, 갱신 날짜, 청구 주소), "플랜 변경" 버튼, "구독 취소" 버튼, 비밀번호 변경, 로그아웃 | 사용자가 정보 수정 → "저장" 클릭 → 업데이트 완료 또는 "플랜 변경" 클릭 → 가격 플랜 페이지 이동 |
| **Paywall (2건째 분석)** | `/paywall` | "월 10건 한도 초과" 메시지, Pro 플랜 가격 (월 69만원), "지금 가입하고 다음 달 50% 할인" 오퍼, "지금 가입" 버튼, "Enterprise 플랜 보기" 링크 | 사용자가 "지금 가입" 클릭 → 결제 페이지 이동 |

---

## API 명세

### 1. 사용자 인증

#### 1-1. 회원가입
```
POST /api/v1/auth/signup
Content-Type: application/json

요청 Body:
{
  "email": "user@example.com",
  "password": "securePassword123",
  "company_name": "ABC 시행사",
  "job_title": "대표이사"
}

응답 (201 Created):
{
  "user_id": "uuid-1234",
  "email": "user@example.com",
  "message": "인증 이메일을 발송했습니다. 이메일 링크를 클릭하여 계정을 활성화하세요."
}

응답 (400 Bad Request):
{
  "error": "이미 가입된 이메일입니다."
}
```

#### 1-2. 로그인
```
POST /api/v1/auth/login
Content-Type: application/json

요청 Body:
{
  "email": "user@example.com",
  "password": "securePassword123"
}

응답 (200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "user_id": "uuid-1234",
    "email": "user@example.com",
    "company_name": "ABC 시행사",
    "plan": "pro"
  }
}

응답 (401 Unauthorized):
{
  "error": "이메일 또는 비밀번호가 잘못되었습니다."
}
```

---

### 2. 프로젝트 관리

#### 2-1. 프로젝트 생성
```
POST /api/v1/projects
Content-Type: application/json
Authorization: Bearer {access_token}

요청 Body:
{
  "project_name": "강남구 토지 A",
  "city": "서울",
  "district": "강남구",
  "land_use": "상업지역",
  "building_coverage_ratio": 80,
  "floor_area_ratio": 400
}

응답 (201 Created):
{
  "project_id": "proj-5678",
  "project_name": "강남구 토지 A",
  "status": "created",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### 2-2. 프로젝트 목록 조회
```
GET /api/v1/projects
Authorization: Bearer {access_token}

쿼리 파라미터:
- page: 1 (기본값)
- limit: 10 (기본값)
- district: "강남구" (선택)
- land_use: "상업지역" (선택)

응답 (200 OK):
{
  "projects": [
    {
      "project_id": "proj-5678",
      "project_name": "강남구 토지 A",
      "district": "강남구",
      "land_use": "상업지역",
      "analysis_date": "2024-01-15T10:30:00Z",
      "approval_probability": 78,
      "status": "completed"
    }
  ],
  "total": 25,
  "page": 1,
  "limit": 10
}
```

#### 2-3. 프로젝트 상세 조회
```
GET /api/v1/projects/{projectId}
Authorization: Bearer {access_token}

응답 (200 OK):
{
  "project_id": "proj-5678",
  "project_name": "강남구 토지 A",
  "district": "강남구",
  "land_use": "상업지역",
  "building_coverage_ratio": 80,
  "floor_area_ratio": 400,
  "analysis_date": "2024-01-15T10:30:00Z",
  "approval_probability": 78,
  "confidence": 4,
  "status": "completed",
  "report_url": "https://s3.amazonaws.com/reports/proj-5678.pdf"
}
```

---

### 3. 분석 (핵심)

#### 3-1. PDF 업로드
```
POST /api/v1/projects/{projectId}/upload
Content-Type: multipart/form-data
Authorization: Bearer {access_token}

요청:
- file: [PDF 파일, 최대 10MB]

응답 (200 OK):
{
  "project_id": "proj-5678",
  "file_url": "https://s3.amazonaws.com/uploads/proj-5678.pdf",
  "file_size": 2048000,
  "uploaded_at": "2024-01-15T10:30:00Z",
  "message": "파일이 업로드되었습니다. '분석 시작' 버튼을 클릭하세요."
}

응답 (400 Bad Request):
{
  "error": "파일 크기가 10MB를 초과합니다."
}
```

#### 3-2. 분석 시작 (비동기)
```
POST /api/v1/projects/{projectId}/analyze
Content-Type: application/json
Authorization: Bearer {access_token}

요청 Body:
{
  "project_id": "proj-5678"
}

응답 (202 Accepted):
{
  "project_id": "proj-5678",
  "status": "analyzing",
  "message": "분석이 시작되었습니다. 48시간 내 이메일로 리포트를 보내드리겠습니다.",
  "estimated_completion": "2024-01-17T10:30:00Z"
}
```

#### 3-3. 분석 결과 조회
```
GET /api/v1/projects/{projectId}/result
Authorization: Bearer {access_token}

응답 (200 OK):
{
  "project_id": "proj-5678",
  "status": "completed",
  "approval_probability": 78,
  "confidence": 4,
  "confidence_description": "★★★★☆",
  "analysis_date": "2024-01-15T10:30:00Z",
  "district_criteria": {
    "land_use": "상업지역",
    "building_coverage_ratio": 80,
    "floor_area_ratio": 400,
    "height_limit": 35
  },
  "similar_cases": [
    {
      "case_id": "case-001",
      "location": "강남구 토지 B",
      "approval_year": 2022,
      "approval_status": "승인",
      "similarity": 95,
      "building_coverage_ratio": 80,
      "floor_area_ratio": 400
    },
    {
      "case_id": "case-002",
      "location": "강남구 토지 C",
      "approval_year": 2021,
      "approval_status": "승인",
      "similarity": 92,
      "building_coverage_ratio": 78,
      "floor_area_ratio": 390
    },
    {
      "case_id": "case-003",
      "location": "서초구 토지 D",
      "approval_year": 2023,
      "approval_status": "거절",
      "similarity": 91,
      "building_coverage_ratio": 82,
      "floor_area_ratio": 410
    }
  ],
  "report_url": "https://s3.amazonaws.com/reports/proj-5678.pdf"
}

응답 (202 Accepted, 분석 중):
{
  "project_id": "proj-5678",
  "status": "analyzing",
  "progress": 65,
  "estimated_completion": "2024-01-17T10:30:00Z"
}
```

---

### 4. 결제 (Stripe 연동)

#### 4-1. 결제 의도 생성
```
POST /api/v1/payments/create-intent
Content-Type: application/json
Authorization: Bearer {access_token}

요청 Body:
{
  "plan": "pro",
  "amount": 690000,
  "currency": "KRW"
}

응답 (200 OK):
{
  "client_secret": "pi_1234567890_secret_abcdefg",
  "amount": 690000,
  "currency": "KRW",
  "status": "requires_payment_method"
}
```

#### 4-2. 결제 확인
```
POST /api/v1/payments/confirm
Content-Type: application/json
Authorization: Bearer {access_token}

요청 Body:
{
  "payment_intent_id": "pi_1234567890",
  "plan": "pro"
}

응답 (200 OK):
{
  "payment_id": "pay-9999",
  "status": "succeeded",
  "plan": "pro",
  "amount": 690000,
  "currency": "KRW",
  "next_billing_date": "2024-02-15",
  "message": "결제가 완료되었습니다. Pro 플랜이 활성화되었습니다."
}
```

---

### 5. Enterprise API (API 키 인증)

#### 5-1. 분석 요청 (JSON)
```
POST /api/v1/enterprise/analyze
Content-Type: application/json
Authorization: ApiKey {api_key}

요청 Body:
{
  "project_name": "강남구 토지 A",
  "city": "서울",
  "district": "강남구",
  "land_use": "상업지역",
  "building_coverage_ratio": 80,
  "floor_area_ratio": 400
}

응답 (200 OK):
{
  "project_id": "proj-5678",
  "approval_probability": 78,
  "confidence": 4,
  "similar_cases": [
    {
      "location": "강남구 토지 B",
      "approval_status": "승인",
      "similarity": 95
    }
  ]
}
```

---

## 데이터 모델

### 1. users (사용자)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| user_id | UUID | 사용자 고유 ID | PK, 자동 생성 |
| email | VARCHAR(255) | 이메일 주소 | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | 비밀번호 해시 (bcrypt) | NOT NULL |
| company_name | VARCHAR(255) | 회사명 | NOT NULL |
| job_title | VARCHAR(100) | 직급 (대표이사, 팀장, 소장 등) | NOT NULL |
| plan | ENUM('starter', 'pro', 'enterprise') | 구독 플랜 | DEFAULT 'starter' |
| plan_start_date | TIMESTAMP | 플랜 시작 날짜 | NOT NULL |
| plan_end_date | TIMESTAMP | 플랜 종료 날짜 (자동 갱신) | NOT NULL |
| monthly_analysis_count | INT | 월 분석 건수 (Pro 플랜 기준 10) | DEFAULT 10 |
| created_at | TIMESTAMP | 계정 생성 날짜 | DEFAULT NOW() |
| updated_at | TIMESTAMP | 계정 수정 날짜 | DEFAULT NOW() |
| is_active | BOOLEAN | 계정 활성화 여부 | DEFAULT FALSE (이메일 인증 후 TRUE) |

### 2. projects (프로젝트)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| project_id | UUID | 프로젝트 고유 ID | PK, 자동 생성 |
| user_id | UUID | 사용자 ID | FK (users.user_id), NOT NULL |
| project_name | VARCHAR(255) | 프로젝트명 | NOT NULL |
| city | VARCHAR(50) | 시도 (서울, 경기 등) | NOT NULL |
| district | VARCHAR(50) | 구군 (강남구, 서초구 등) | NOT NULL |
| land_use | VARCHAR(50) | 용도지역 (주거, 상업, 공업 등) | NOT NULL |
| building_coverage_ratio | INT | 건폐율 (%) | NOT NULL |
| floor_area_ratio | INT | 용적률 (%) | NOT NULL |
| file_url | VARCHAR(500) | 업로드된 개요서 PDF URL (S3) | NULLABLE |
| status | ENUM('created', 'analyzing', 'completed', 'failed') | 분석 상태 | DEFAULT 'created' |
| created_at | TIMESTAMP | 프로젝트 생성 날짜 | DEFAULT NOW() |
| updated_at | TIMESTAMP | 프로젝트 수정 날짜 | DEFAULT NOW() |

### 3. analyses (분석 결과)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| analysis_id | UUID | 분석 고유 ID | PK, 자동 생성 |
| project_id | UUID | 프로젝트 ID | FK (projects.project_id), NOT NULL |
| approval_probability | INT | 승인 확률 (0~100) | NOT NULL |
| confidence | INT | 신뢰도 (1~5 별) | NOT NULL |
| extracted_text | TEXT | OCR로 추출된 텍스트 | NULLABLE |
| ml_model_version | VARCHAR(50) | ML 모델 버전 (v1.0, v1.1 등) | NOT NULL |
| analysis_date | TIMESTAMP | 분석 완료 날짜 | DEFAULT NOW() |
| report_url | VARCHAR(500) | 생성된 리포트 PDF URL (S3) | NULLABLE |
| error_message | TEXT | 분석 실패 시 에러 메시지 | NULLABLE |

### 4. case_studies (과거 사례)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| case_id | UUID | 사례 고유 ID | PK, 자동 생성 |
| location | VARCHAR(255) | 토지 위치 (예: 강남구 토지 B) | NOT NULL |
| city | VARCHAR(50) | 시도 | NOT NULL |
| district | VARCHAR(50) | 구군 | NOT NULL |
| land_use | VARCHAR(50) | 용도지역 | NOT NULL |
| building_coverage_ratio | INT | 건폐율 (%) | NOT NULL |
| floor_area_ratio | INT | 용적률 (%) | NOT NULL |
| approval_status | ENUM('승인', '거절') | 인허가 결과 | NOT NULL |
| approval_year | INT | 인허가 연도 | NOT NULL |
| approval_date | DATE | 인허가 날짜 | NOT NULL |
| source | VARCHAR(100) | 데이터 출처 (지자체, 공공데이터 등) | NOT NULL |
| created_at | TIMESTAMP | 사례 등록 날짜 | DEFAULT NOW() |

### 5. district_criteria (지자체 기준)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| criteria_id | UUID | 기준 고유 ID | PK, 자동 생성 |
| city | VARCHAR(50) | 시도 | NOT NULL |
| district | VARCHAR(50) | 구군 | NOT NULL |
| land_use | VARCHAR(50) | 용도지역 | NOT NULL |
| building_coverage