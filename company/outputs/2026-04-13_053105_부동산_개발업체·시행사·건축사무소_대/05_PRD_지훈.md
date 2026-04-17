# PRD: 토지 사업성 분석 자동화 SaaS (LandAnalytics)

## 제품 개요
부동산 개발업체·시행사·건축사무소가 토지 개요서·법률서를 업로드하면 AI가 승인 확률·특례법 해당 여부·개발 가능성·투여 금액 범위·정책 흐름을 자동 산출하는 B2B SaaS.

---

## 기술 스택

| 계층 | 선택 | 근거 |
|------|------|------|
| **FE** | React 18 + TypeScript + TailwindCSS + React Query | 대시보드·폼 기반 UI, 실시간 분석 결과 표시 필요. 기업용 SaaS 표준 스택. |
| **BE** | Python 3.11 + FastAPI + Uvicorn | AI/LLM 통합 용이. 법률 도메인 NLP 라이브러리(spaCy, transformers) 기본 지원. 비동기 처리로 장시간 분석 작업 최적화. |
| **AI/ML** | LangChain + OpenAI GPT-4 (또는 Anthropic Claude) + 한국 특화 LLM (KoGPT, Upstage Solar) | 건축법·특례법 해석 + 정책 흐름 분석. 한국 법률 도메인 특화 모델 필수. 초기는 GPT-4 API, 장기는 파인튜닝 또는 자체 모델 검토. |
| **DB** | PostgreSQL 15 + TimescaleDB 확장 | 구조화된 분석 결과(승인 확률, 투자금 범위 등) 저장. 정책 변동 이력 시계열 추적. 트랜잭션 안정성 필수(법률 관련 데이터). |
| **문서 처리** | PyPDF2 + python-docx + Tesseract OCR | 토지 개요서(PDF), 법률서(DOCX) 자동 파싱. 스캔 이미지 포함 문서 처리. |
| **인프라** | AWS (EC2 + RDS + S3 + Lambda) 또는 GCP (Compute Engine + Cloud SQL + Cloud Storage) | 스케일 가능한 API 서버. 문서 저장소. 정책 데이터 자동 수집 파이프라인(Lambda/Cloud Functions). 초기: 단일 리전, 장기: 멀티 리전 고려. |
| **배포** | Docker + GitHub Actions + Kubernetes (EKS/GKE) | 컨테이너화로 개발·테스트·프로덕션 환경 일관성. CI/CD 자동화. 초기는 Docker Compose, 고객 증가 시 K8s 전환. |
| **모니터링** | Datadog / New Relic + Sentry | API 응답 시간, 분석 정확도, 에러율 추적. 법률 해석 오류 감지 알림. |
| **보안** | OAuth 2.0 (Google/Naver) + JWT + TLS 1.3 + IP 화이트리스트 | B2B 기업 고객 대상. SSO 지원. 민감한 부동산 데이터 암호화 저장. |

---

## 기능 목록

> **Wave 전략**: P0(MVP, 1차 출시) → P1(1차 출시 후 2~3개월) → P2(6개월 이후)

| 우선순위 | 기능 | 설명 | 이유 | 의존 기능 | 예상 개발 기간 |
|---------|------|------|------|---------|--------------|
| **P0** | 문서 업로드 & 파싱 | 토지 개요서(PDF), 법률서(DOCX) 업로드 → 자동 텍스트 추출 | MVP 핵심. 사용자 입력 게이트웨이. | 없음 | 2주 |
| **P0** | 기본 정보 추출 | 문서에서 토지 위치, 면적, 용도지역, 현황 자동 추출 | 분석의 기초 데이터. 수작업 입력 제거. | 문서 파싱 | 1.5주 |
| **P0** | 승인 확률 산출 | 입력 데이터 기반 인허가 승인 확률(%) 자동 계산 | 핵심 의사결정 지표. 고객이 가장 원하는 기능. | 기본 정보 추출 | 3주 |
| **P0** | 분석 결과 대시보드 | 승인 확률, 개발 가능성, 투자금 범위 한눈에 표시 | 결과 시각화. 고객이 즉시 의사결정 가능. | 승인 확률 산출 | 2주 |
| **P0** | 결과 PDF 리포트 생성 | 분석 결과를 고객사 제안용 PDF 리포트로 자동 생성 | 건축사무소·시행사가 고객에게 제출할 자료. 수익화 핵심. | 분석 결과 대시보드 | 1.5주 |
| **P0** | 사용자 인증 & 계정 관리 | 이메일 회원가입, 로그인, 팀 초대 기능 | 멀티테넌트 SaaS 기본. | 없음 | 1주 |
| **P1** | 특례법 해당 여부 판정 | 도시재생·혁신도시·규제자유특구 등 특례법 자동 판정 | 고객 Pain Point Level 4. 현재 외주 비용 월 50만원+. | 기본 정보 추출 | 3주 |
| **P1** | 정책 흐름 분석 | 해당 지역의 최근 정책 변동(용도지역 변경, 규제 완화 등) 자동 수집 & 분석 | 정책 변동기(2024~2025) 긴급성 높음. 경쟁사 공백. | 기본 정보 추출 | 4주 |
| **P1** | 투자금 범위 예측 | 토지 규모·용도·지역 기반 개발 투자금 범위 자동 산출 | 사업성 검토의 핵심. 고객이 자금 조달 계획 수립 가능. | 기본 정보 추출 | 3주 |
| **P1** | 비교 분석 (다중 토지) | 여러 토지를 동시 분석 후 비교 테이블 생성 | 개발업체 심사팀이 포트폴리오 스크리닝 시 필수. | 분석 결과 대시보드 | 2주 |
| **P1** | 분석 이력 저장 & 검색 | 과거 분석 결과 저장, 검색, 재분석 기능 | 고객이 같은 토지 재분석 시 비용 절감. 구독 유지율 향상. | 분석 결과 대시보드 | 1.5주 |
| **P1** | API 제공 (기본) | 외부 시스템(부동산 관리 소프트웨어)과 연동 가능한 REST API | 고객사 자체 시스템 통합 필요. 업셀 트리거. | 분석 결과 대시보드 | 2주 |
| **P2** | 실시간 정책 모니터링 & 알림 | 구독 고객 대상 지역별 정책 변동 자동 감지 & 이메일/Slack 알림 | 정책 변동 시 즉시 대응 필요한 고객 대상. 구독료 정당화. | 정책 흐름 분석 | 3주 |
| **P2** | 협력사 네트워크 (건축사·법무사) | 분석 결과 기반 추천 건축사·법무사 매칭 | 고객 만족도 향상. 파트너사 수수료 수익 모델. | 분석 결과 대시보드 | 4주 |
| **P2** | 고급 시뮬레이션 | 용도 변경·규모 조정 등 시나리오별 승인 확률 재계산 | 고객이 "만약 이렇게 하면?" 질문에 즉시 답변 가능. | 승인 확률 산출 | 3주 |
| **P2** | 분석 정확도 피드백 루프 | 고객이 실제 인허가 결과 입력 → 모델 재학습 | 시간이 지날수록 정확도 향상. 경쟁 우위 고착화. | 승인 확률 산출 | 지속적 |

---

## Must NOT (범위 외)

- **실제 법률 자문 제공** — "이 토지는 반드시 승인됩니다"같은 법적 보증 금지. "참고용 분석"으로만 표시. 법무사·건축사 자문 필수.
- **부동산 거래 중개** — 토지 매매 중개 서비스 금지. 분석만 제공.
- **자금 조달 서비스** — 투자금 범위 산출 후 대출·투자 알선 금지. 금융감독 규제 회피.
- **정부 인허가 신청 자동화** — 실제 인허가 신청서 작성·제출 자동화 금지. 행정 규제 위반.
- **글로벌 확장** — 초기 한국 시장만 집중. 다른 국가 법률 체계 상이.
- **모바일 앱 (초기)** — 웹 기반만. 모바일은 P2 이후 검토.
- **AI 학습용 고객 데이터 재판매** — 고객 분석 데이터를 제3자에게 판매 금지. 신뢰 손실.

---

## User Flow

### 시나리오 1: 시행사 실무자의 토지 사업성 빠른 스크리닝

**배경**: 시행사가 새로운 토지 매입 기회를 발견. 의사결정까지 48시간 내 사업성 검토 필요.

1단계: 사용자가 LandAnalytics 대시보드 로그인
   → 시스템: 최근 분석 목록 표시

2단계: 사용자가 "새 분석 시작" 클릭
   → 시스템: 문서 업로드 페이지 표시

3단계: 사용자가 토지 개요서(PDF) + 법률서(DOCX) 드래그앤드롭
   → 시스템: 파일 검증(크기, 형식) → 업로드 시작

4단계: 시스템이 문서 자동 파싱 (2~5분)
   → 사용자에게 "분석 중..." 진행률 표시

5단계: 파싱 완료 후 기본 정보 추출 결과 표시
   → 사용자가 자동 추출된 "토지 위치, 면적, 용도지역" 검증 & 수정 가능

6단계: 사용자가 "분석 실행" 클릭
   → 시스템: AI 모델 실행 (승인 확률, 특례법 판정, 투자금 범위 계산)

7단계: 분석 완료 (1~3분)
   → 시스템: 대시보드에 결과 표시
      - 승인 확률: 78%
      - 특례법 해당: 도시재생 특구 (O)
      - 개발 가능성: 높음
      - 투자금 범위: 50억~80억 원
      - 정책 흐름: 최근 3개월 해당 지역 정책 변동 요약

8단계: 사용자가 "PDF 리포트 생성" 클릭
   → 시스템: 분석 결과를 고객사 제안용 PDF로 생성 & 다운로드

9단계: 사용자가 리포트를 고객사에 제출
   → 의사결정 완료

**소요 시간**: 기존 외주(5~7일) → 자동화(30분)

---

### 시나리오 2: 건축사무소 소장의 고객 제안용 리포트 생성

**배경**: 건축사무소가 신규 고객으로부터 토지 설계 의뢰 받음. 인허가 가능성을 사전 검토한 후 제안서 작성 필요.

1단계: 소장이 LandAnalytics 접속
   → 시스템: 팀 멤버 목록 표시 (소장 + 실무자 2명)

2단계: 소장이 "팀 멤버 초대" 클릭 → 실무자 이메일 입력
   → 시스템: 초대 이메일 발송

3단계: 실무자가 초대 수락 & 로그인
   → 시스템: 팀 대시보드 접근 권한 부여

4단계: 실무자가 고객 토지 정보 입력 & 문서 업로드
   → 시스템: 자동 분석 실행

5단계: 분석 완료 후 "비교 분석" 기능으로 유사 토지 3개 추가 분석
   → 시스템: 4개 토지 비교 테이블 생성

6단계: 소장이 비교 결과 검토 후 "고객 제안용 PDF" 생성
   → 시스템: 브랜딩된 PDF (건축사무소 로고 포함) 생성

7단계: 소장이 PDF를 고객에게 이메일 발송
   → 고객이 리포트 검토 후 설계 의뢰 확정

**소요 시간**: 기존 수작업(3~5일) → 자동화(2시간)

---

### 시나리오 3: 개발업체 심사팀의 포트폴리오 스크리닝

**배경**: 개발업체가 월 20개 토지 기회 검토. 현재 각 토지마다 외부 컨설턴트에 의뢰 (건당 100만원, 월 2,000만원 비용).

1단계: 심사팀이 LandAnalytics 대시보드 접속
   → 시스템: 이번 달 분석 현황 표시 (분석 건수, 평균 승인 확률 등)

2단계: 심사팀이 20개 토지 정보를 CSV로 일괄 업로드
   → 시스템: 각 토지별 문서 자동 파싱 & 분석 큐에 추가

3단계: 시스템이 배치 분석 실행 (병렬 처리)
   → 사용자에게 진행률 표시

4단계: 분석 완료 후 "비교 분석" 테이블 자동 생성
   → 승인 확률 순으로 정렬된 20개 토지 목록 표시

5단계: 심사팀이 상위 5개 토지만 상세 검토
   → 나머지 15개는 자동 거절 리스트로 분류

6단계: 상위 5개 토지에 대해 "고급 시뮬레이션" 실행
   → "용도 변경 시 승인 확률", "규모 축소 시 투자금" 등 시나리오 계산

7단계: 최종 의사결정 후 "분석 이력 저장"
   → 향후 유사 토지 재분석 시 참고 가능

**소요 시간**: 기존 외주(월 20일) → 자동화(월 2일) → **월 1,500만원 비용 절감**

---

## 화면 명세

| 화면명 | URL/Route | 핵심 컴포넌트 | 동작 |
|--------|-----------|-------------|------|
| **로그인** | `/login` | 이메일 입력, 비밀번호 입력, "로그인" 버튼, "회원가입" 링크 | 이메일/비밀번호 검증 → JWT 토큰 발급 → 대시보드 리다이렉트 |
| **회원가입** | `/signup` | 이메일, 비밀번호, 회사명, 직급 입력 필드, "가입" 버튼 | 이메일 중복 검증 → 계정 생성 → 확인 이메일 발송 |
| **메인 대시보드** | `/dashboard` | 최근 분석 목록 (카드형), "새 분석 시작" 버튼, 월 분석 건수 그래프, 팀 멤버 목록 | 분석 목록 클릭 → 상세 결과 페이지 이동. "새 분석" 클릭 → 문서 업로드 페이지 이동 |
| **문서 업로드** | `/analysis/new` | 드래그앤드롭 영역 (토지 개요서 + 법률서), 파일 선택 버튼, "분석 시작" 버튼 | 파일 검증(PDF/DOCX, 크기 ≤50MB) → 업로드 → 파싱 시작 → 진행률 표시 |
| **기본 정보 검증** | `/analysis/{id}/verify` | 자동 추출된 정보 (위치, 면적, 용도지역, 현황) 표시, 각 필드 수정 가능, "확인" 버튼 | 사용자가 수정 → "확인" 클릭 → 분석 실행 페이지로 이동 |
| **분석 진행 중** | `/analysis/{id}/processing` | 진행률 바 (0~100%), "분석 중..." 메시지, 예상 소요 시간 | 실시간 진행률 업데이트 (WebSocket). 완료 시 자동으로 결과 페이지로 이동 |
| **분석 결과 대시보드** | `/analysis/{id}/result` | 승인 확률 (큰 숫자 + 게이지), 특례법 판정 (O/X), 개발 가능성 (높음/중간/낮음), 투자금 범위 (슬라이더), 정책 흐름 (타임라인), "PDF 생성" 버튼, "비교 분석" 버튼 | 각 섹션 클릭 → 상세 설명 팝업. "PDF 생성" → 리포트 다운로드. "비교 분석" → 다중 분석 페이지로 이동 |
| **비교 분석** | `/analysis/compare` | 최대 5개 토지 선택 체크박스, 비교 테이블 (승인 확률, 투자금, 특례법 등 컬럼), 정렬/필터 옵션 | 테이블 헤더 클릭 → 정렬. 필터 선택 → 테이블 업데이트. 특정 토지 클릭 → 상세 결과 페이지 이동 |
| **고급 시뮬레이션** | `/analysis/{id}/simulation` | 시나리오 선택 (용도 변경, 규모 축소 등), 파라미터 슬라이더, "재계산" 버튼, 결과 비교 (기존 vs 시뮬레이션) | 파라미터 조정 → "재계산" 클릭 → 새로운 승인 확률·투자금 표시 |
| **분석 이력** | `/analysis/history` | 분석 목록 (날짜, 토지명, 승인 확률, 상태), 검색/필터 옵션, 페이지네이션 | 목록 클릭 → 상세 결과 페이지. 검색 입력 → 실시간 필터링 |
| **팀 관리** | `/team/settings` | 팀 멤버 목록, "멤버 초대" 버튼, 권한 설정 (Admin/Editor/Viewer), 멤버 삭제 옵션 | "초대" 클릭 → 이메일 입력 폼 → 초대 이메일 발송. 권한 드롭다운 → 권한 변경 |
| **구독 & 결제** | `/billing` | 현재 플랜 (Starter/Pro/Enterprise), 월 사용량 (분석 건수), "플랜 변경" 버튼, 결제 이력 | "플랜 변경" → 플랜 선택 페이지 → 결제 → 구독 업데이트 |
| **설정** | `/settings` | 프로필 (이메일, 회사명, 직급), 비밀번호 변경, 알림 설정 (정책 변동 알림 ON/OFF), 데이터 삭제 옵션 | 각 필드 수정 → "저장" 클릭 → 변경 사항 저장 |

---

## API 명세

### 인증 (Authentication)

| Method | Endpoint | 요청 Body | 응답 | 상태 코드 |
|--------|---------|-----------|------|----------|
| POST | `/api/v1/auth/signup` | `{ "email": "user@example.com", "password": "...", "company_name": "...", "role": "..." }` | `{ "user_id": "uuid", "email": "...", "token": "jwt_token" }` | 201 |
| POST | `/api/v1/auth/login` | `{ "email": "user@example.com", "password": "..." }` | `{ "user_id": "uuid", "token": "jwt_token", "expires_in": 3600 }` | 200 |
| POST | `/api/v1/auth/refresh` | `{ "refresh_token": "..." }` | `{ "token": "new_jwt_token", "expires_in": 3600 }` | 200 |
| POST | `/api/v1/auth/logout` | `{}` | `{ "message": "Logged out successfully" }` | 200 |

**인증 방식**: Bearer Token (JWT). 모든 API 요청 헤더에 `Authorization: Bearer {token}` 포함.

---

### 분석 (Analysis)

| Method | Endpoint | 요청 Body | 응답 | 상태 코드 | 인증 |
|--------|---------|-----------|------|----------|------|
| POST | `/api/v1/analysis/upload` | FormData: `files[]` (PDF/DOCX), `project_name` (string) | `{ "analysis_id": "uuid", "status": "parsing", "progress": 0 }` | 202 | Required |
| GET | `/api/v1/analysis/{analysis_id}/status` | - | `{ "analysis_id": "uuid", "status": "parsing\|verifying\|analyzing\|completed", "progress": 0~100 }` | 200 | Required |
| GET | `/api/v1/analysis/{analysis_id}/extracted-info` | - | `{ "location": "서울시 강남구...", "area_sqm": 5000, "zoning": "상업지역", "current_status": "...", "extracted_at": "2024-01-15T10:30:00Z" }` | 200 | Required |
| PUT | `/api/v1/analysis/{analysis_id}/verify` | `{ "location": "...", "area_sqm": 5000, "zoning": "...", "current_status": "..." }` | `{ "analysis_id": "uuid", "status": "analyzing" }` | 200 | Required |
| GET | `/api/v1/analysis/{analysis_id}/result` | - | `{ "analysis_id": "uuid", "approval_probability": 78, "special_law": { "applicable": true, "law_name": "도시재생 특구" }, "development_feasibility": "high", "investment_range": { "min": 5000000000, "max": 8000000000 }, "policy_flow": [...], "created_at": "2024-01-15T10:30:00Z" }` | 200 | Required |
| POST | `/api/v1/analysis/{analysis_id}/report/pdf` | `{ "include_comparison": false, "branding": { "company_logo_url": "..." } }` | `{ "report_url": "https://s3.../report_uuid.pdf", "expires_in": 3600 }` | 200 | Required |
| GET | `/api/v1/analysis/list` | Query: `limit=10&offset=0&sort_by=created_at&order=desc` | `{ "total": 45, "analyses": [ { "analysis_id": "uuid", "project_name": "...", "approval_probability": 78, "created_at": "..." }, ... ] }` | 200 | Required |
| DELETE | `/api/v1/analysis/{analysis_id}` | - | `{ "message": "Analysis deleted successfully" }` | 200 | Required |

---

### 비교 분석 (Comparison)

| Method | Endpoint | 요청 Body | 응답 | 상태 코드 | 인증 |
|--------|---------|-----------|------|----------|------|
| POST | `/api/v1/analysis/compare` | `{ "analysis_ids": ["uuid1", "uuid2", "uuid3"] }` | `{ "comparison_id": "uuid", "analyses": [ { "analysis_id": "uuid", "project_name": "...", "approval_probability": 78, "investment_range": {...}, ... }, ... ] }` | 200 | Required |

---

### 시뮬레이션 (Simulation)

| Method | Endpoint | 요청 Body | 응답 | 상태 코드 | 인증 |
|--------|---------|-----------|------|----------|------|
| POST | `/api/v1/analysis/{analysis_id}/simulate` | `{ "scenario": "zoning_change\|size_reduction\|use_change", "parameters": { "new_zoning": "주거지역", "new_area_sqm": 4000 } }` | `{ "simulation_id": "uuid", "status": "processing" }` | 202 | Required |
| GET | `/api/v1/analysis/{analysis_id}/simulate/{simulation_id}/result` | - | `{ "simulation_id": "uuid", "scenario": "zoning_change", "original_approval_probability": 78, "simulated_approval_probability": 85, "original_investment_range": {...}, "simulated_investment_range": {...} }` | 200 | Required |

---

### 팀 관리 (Team Management)

| Method | Endpoint | 요청 Body | 응답 | 상태 코드 | 인증 |
|--------|---------|-----------|------|----------|------|
| POST | `/api/v1/team/invite` | `{ "email": "member@example.com", "role": "editor\|viewer" }` | `{ "invitation_id": "uuid", "email": "...", "status": "pending" }` | 201 | Required (Admin only) |
| GET | `/api/v1/team/members` | - | `{ "team_id": "uuid", "members": [ { "user_id": "uuid", "email": "...", "role": "admin\|editor\|viewer", "joined_at": "..." }, ... ] }` | 200 | Required |
| PUT | `/api/v1/team/members/{user_id}/role` | `{ "role": "editor\|viewer" }` | `{ "user_id": "uuid", "role": "editor" }` | 200 | Required (Admin only) |
| DELETE | `/api/v1/team/members/{user_id}` | - | `{ "message": "Member removed successfully" }` | 200 | Required (Admin only) |

---

### 구독 & 결제 (Billing)

| Method | Endpoint | 요청 Body | 응답 | 상태 코드 | 인증 |
|--------|---------|-----------|------|----------|------|
| GET | `/api/v1/billing/plans` | - | `{ "plans": [ { "plan_id": "starter", "name": "Starter", "price_monthly": 150000, "features": [...] }, ... ] }` | 200 | Optional |
| POST | `/api/v1/billing/subscribe` | `{ "plan_id": "pro", "payment_method": "card\|bank_transfer" }` | `{ "subscription_id": "uuid", "plan_id": "pro", "status": "active", "next_billing_date": "2024-02-15" }` | 201 | Required |
| GET | `/api/v1/billing/subscription` | - | `{ "subscription_id": "uuid", "plan_id": "pro", "status": "active", "current_period_start": "2024-01-15", "current_period_end": "2024-02-15", "analyses_used": 12, "analyses_limit": 50 }` | 200 | Required |
| POST | `/api/v1/billing/cancel` | - | `{ "subscription_id": "uuid", "status": "cancelled", "cancellation_date": "2024-01-20" }` | 200 | Required |

---

### 정책 모니터링 (Policy Monitoring) — P2

| Method | Endpoint | 요청 Body | 응답 | 상태 코드 | 인증 |
|--------|---------|-----------|------|----------|------|
| GET | `/api/v1/policy/updates` | Query: `region=서울시&limit=10` | `{ "updates": [ { "policy_id": "uuid", "title": "용도지역 변경 안내", "region": "서울시 강남구", "effective_date": "2024-02-01", "summary": "...", "source_url": "..." }, ... ] }` | 200 | Required |
| POST | `/api/v1/policy/subscribe` | `{ "regions": ["서울시", "경기도"], "notification_method": "email\|slack" }` | `{ "subscription_id": "uuid", "regions": [...], "status": "active" }` | 201 | Required |

---

### 에러 응답 (공통)

모든 에러는 다음 형식:
```json
{
  "error": {
    "code": "INVALID_FILE_FORMAT",
    "message": "Uploaded file must be PDF or DOCX",
    "details": "File type: .txt"
  }
}
```

**주요 에러 코드**:
- `INVALID_FILE_FORMAT` (400): 파일 형식 오류
- `FILE_SIZE_EXCEEDED` (400): 파일 크기 초과 (>50MB)
- `PARSING_FAILED` (500): 문서 파싱 실패
- `ANALYSIS_FAILED` (500): AI 분석 실패
- `UNAUTHORIZED` (401): 인증 토큰 없음/만료
- `FORBIDDEN` (403): 권한 없음
- `NOT_FOUND` (404): 리소스 없음
- `RATE_LIMIT_EXCEEDED` (429): API 호출 제한 초과
- `INTERNAL_SERVER_ERROR` (500): 서버 오류

---

## 데이터 모델

### 1. users (사용자)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| user_id | UUID | 사용자 고유 ID | PK, NOT NULL |
| email | VARCHAR(255) | 이메일 주소 | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | 해시된 비밀번호 | NOT NULL |
| company_name | VARCHAR(255) | 회사명 | NOT NULL |
| role | ENUM('admin', 'editor', 'viewer') | 팀 내 역할 | NOT NULL, DEFAULT 'editor' |
| team_id | UUID | 소속 팀 ID | FK → teams.team_id |
| created_at | TIMESTAMP | 계정 생성 시간 | NOT NULL, DEFAULT NOW() |
| updated_at | TIMESTAMP | 마지막 수정 시간 | NOT NULL, DEFAULT NOW() |
| deleted_at | TIMESTAMP | 소프트 삭제 시간 | NULL (활성 사용자) |

**인덱스**: `email` (UNIQUE), `team_id`, `created_at`

---

### 2. teams (팀/조직)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| team_id | UUID | 팀 고유 ID | PK, NOT NULL |
| team_name | VARCHAR(255) | 팀명 (회사명) | NOT NULL |
| admin_user_id | UUID | 팀 관리자 ID | FK → users.user_id, NOT NULL |
| subscription_plan | ENUM('starter', 'pro', 'enterprise') | 구독 플랜 | NOT NULL, DEFAULT 'starter' |
| analyses_limit | INT | 월 분석 건수 제한 | NOT NULL (Starter: 10, Pro: 50, Enterprise: unlimited) |
| created_at | TIMESTAMP | 팀 생성 시간 | NOT NULL, DEFAULT NOW() |
| updated_at | TIMESTAMP | 마지막 수정 시간 | NOT NULL, DEFAULT NOW() |

**인덱스**: `admin_user_id`, `subscription_plan`

---

### 3. analyses (분석 결과)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| analysis_id | UUID | 분석 고유 ID | PK, NOT NULL |
| team_id | UUID | 소속 팀 ID | FK → teams.team_id, NOT NULL |
| created_by_user_id | UUID | 분석 생성자 ID | FK → users.user_id, NOT NULL |
| project_name | VARCHAR(255) | 프로젝트명 (토지명) | NOT NULL |
| status | ENUM('parsing', 'verifying', 'analyzing', 'completed', 'failed') | 분석 상태 | NOT NULL, DEFAULT 'parsing' |
| progress | INT | 진행률 (0~100) | NOT NULL, DEFAULT 0 |
| extracted_info | JSONB | 자동 추출된 기본 정보 | `{ "location": "...", "area_sqm": 5000, "zoning": "상업지역", "current_status": "..." }` |
| approval_probability | INT | 승인 확률 (0~100) | NULL (분석 완료 후) |
| special_law | JSONB | 특례법 판정 결과 | `{ "applicable": true, "law_name": "도시재생 특구", "details": "..." }` |
| development_feasibility | ENUM('high', 'medium', 'low') | 개발 가능성 | NULL (분석 완료 후) |
| investment_range | JSONB | 투자금 범위 | `{ "min": 5000000000, "max": 8000000000, "currency": "KRW" }` |
| policy_flow | JSONB | 정책 흐름 분석 | `[ { "date": "2024-01-15", "policy": "용도지역 변경", "impact": "positive" }, ... ]` |
| document_urls | JSONB | 업로드된 문서 S3 URL | `{ "overview": "s3://...", "legal": "s3://..." }` |
| error_message | TEXT | 분석 실패 시 에러 메시지 | NULL (성공 시) |
| created_at | TIMESTAMP | 분석 생성 시간 | NOT NULL, DEFAULT NOW() |
| updated_at | TIMESTAMP | 마지막 수정 시간 | NOT NULL, DEFAULT NOW() |
| deleted_at | TIMESTAMP | 소프트 삭제 시간 | NULL (활성 분석) |

**인덱스**: `team_id`, `created_by_user_id`, `status`, `created_at`, `approval_probability`

---

### 4. simulations (시뮬레이션 결과)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| simulation_id | UUID | 시뮬레이션 고유 ID | PK, NOT NULL |
| analysis_id | UUID | 원본 분석 ID | FK → analyses.analysis_id, NOT NULL |
| scenario | ENUM('zoning_change', 'size_reduction', 'use_change') | 시나리오 유형 | NOT NULL |
| parameters | JSONB | 시뮬레이션 파라미터 | `{ "new_zoning": "주거지역", "new_area_sqm": 4000 }` |
| simulated_approval_probability | INT | 시뮬레이션 후 승인 확률 | NOT NULL |
| simulated_investment_range | JSONB | 시뮬레이션 후 투자금 범위 | `{ "min": ..., "max": ... }` |
| created_at | TIMESTAMP | 시뮬레이션 생성 시간 | NOT NULL, DEFAULT NOW() |

**인덱스**: `analysis_id`, `created_at`

---

### 5. subscriptions (구독 정보)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| subscription_id | UUID | 구독 고유 ID | PK, NOT NULL |
| team_id | UUID | 팀 ID | FK → teams.team_id, NOT NULL |
| plan_id | ENUM('starter', 'pro', 'enterprise') | 구독 플랜 | NOT NULL |
| status | ENUM('active', 'cancelled', 'past_due') | 구독 상태 | NOT NULL, DEFAULT 'active' |
| current_period_start | DATE | 현재 청구 기간 시작 | NOT NULL |
| current_period_end | DATE | 현재 청구 기간 종료 | NOT NULL |
| payment_method | ENUM('card', 'bank_transfer') | 결제 수단 | NOT NULL |
| next_billing_date | DATE | 다음 청구 예정일 | NOT NULL |
| created_at | TIMESTAMP | 구독 시작 시간 | NOT NULL, DEFAULT NOW() |
| cancelled_at | TIMESTAMP | 구독 취소 시간 | NULL (활성 구독) |

**인덱스**: `team_id`, `status`, `next_billing_date`

---

### 6. policy_updates (정책 업데이트) — P2

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| policy_id | UUID | 정책 고유 ID | PK, NOT NULL |
| region | VARCHAR(255) | 지역 (시/도/구) | NOT NULL |
| title | VARCHAR(255) | 정책 제목 | NOT NULL |
| summary | TEXT | 정책 요약 | NOT NULL |
| effective_date | DATE | 정책 시행일 | NOT NULL |
| source_url | VARCHAR(500) | 정책 출처 URL | NOT NULL |
| impact_type | ENUM('positive', 'negative', 'neutral') | 부동산 개발에 미치는 영향 | NOT NULL |
| created_at | TIMESTAMP | 정책 수집 시간 | NOT NULL, DEFAULT NOW() |

**인덱스**: `region`, `effective_date`, `created_at`

---

### 7. policy_subscriptions (정책 구독) — P2

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| subscription_id | UUID | 구독 고유 ID | PK, NOT NULL |
| user_id | UUID | 사용자 ID | FK → users.user_id, NOT NULL |
| region | VARCHAR(255) | 구독 지역 | NOT NULL |
| notification_method | ENUM('email', 'slack') | 알림 방식 | NOT NULL |
| is_active | BOOLEAN | 활성 여부 | NOT NULL, DEFAULT TRUE |
| created_at | TIMESTAMP | 구독 시작 시간 | NOT NULL, DEFAULT NOW() |

**인덱스**: `user_id`, `region`, `is_active`

---

### 8. audit_logs (감사 로그)

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| log_id | UUID | 로그 고유 ID | PK, NOT NULL |
| user_id | UUID | 사용자 ID | FK → users.user_id, NOT NULL |
| action | VARCHAR(255) | 수행한 작업 (e.g., "analysis_created", "report_downloaded") | NOT NULL |
| resource_type | VARCHAR(100) | 리소스 타입 (e.g., "analysis", "subscription") | NOT NULL |
| resource_id | UUID | 리소스 ID | NOT NULL |
| details | JSONB | 작업 상세 정보 | NULL |
| created_at | TIMESTAMP | 로그 생성 시간 | NOT NULL, DEFAULT NOW() |

**인덱스**: `user_id`, `action`, `created_at`

---

## 성공 기준

### 1단계 (MVP 출시, 3개월)

| KPI | 목표치 | 측정 방법 | 임계값 |
|-----|--------|---------|--------|
| **유료 파일럿 고객 확보** | 10개사 | 구독 활성 팀 수 | ≥10 |
| **분석 정확도** | 80% 이상 | 고객 피드백 기반 (실제 인허가 결과와 비교) | 승인

---

# V4 Framework Sections (Pass 2)

## Aha Moment 정의

**Aha Moment:**
> 시행사 실무자가 토지 개요서·법률서를 업로드한 후 **60초 내에 "승인 확률 78%, 도시재생 특구 해당, 투자금 50~80억" 결과를 한눈에 보고 "이 토지는 진행할 가치가 있다"고 즉시 판단하는 순간.**

**측정:**
- 가입부터 아하까지 예상 클릭 수: 5클릭 (로그인 → 새 분석 → 파일 업로드 → 확인 → 결과 보기)
- 예상 소요 시간: 60초 이내
- 목표: 첫 분석 완료 후 "다시 사용하겠다" 의향 80% 이상

**구현 방식:**
1. **온보딩 단축**: 회원가입 스킵 가능 (Google/Naver OAuth), 첫 분석은 3단계만 (파일 업로드 → 자동 추출 → 결과)
2. **핵심 가치 즉시 노출**: 대시보드 진입 시 "승인 확률" 큰 숫자(게이지) + "특례법 해당 여부"(O/X) + "투자금 범위"(슬라이더) 3개만 상단에 배치. 나머지는 "상세 보기" 탭으로 숨김
3. **시각적 피드백**: 파일 업로드 후 진행률 바(0→100%) 실시간 표시, 각 단계별 체크마크 애니메이션 (파싱 완료 ✓ → 분석 중 → 완료 ✓)

---

## JTBD Statement (민수 전략 → 서윤 Phase 1 기반)

**When I am** 새로운 토지 매입 기회를 발견했는데 의사결정까지 48시간밖에 없는 상황,

**I want to** 토지 개요서와 법률서만 업로드해서 인허가 승인 확률, 특례법 해당 여부, 개발 가능성, 투자금 범위를 자동으로 산출받고,

**so I can** 외부 컨설턴트 의뢰(5~7일 소요, 건당 100~200만원 비용) 없이 빠르게 1차 스크리닝을 완료하고 경영진에게 "진행/중단" 의사결정을 올릴 수 있다.

---

## Customer Forces Strategy (서윤 Phase 1 Canvas 기반)

### Push 요인 (현재 상태의 불만)

**현재 상태**: 토지 사업성 검토를 위해 토지대장·건축물대장·법률서를 수작업으로 분석하거나, 외부 컨설턴트(건축사·법무사·개발 컨설팅사)에 의뢰 중

**경쟁사 불만** (서윤 Phase 1 evidence):
- 크레마오 암시: *"토지대장, 건축물대장 등 많은 서류 검토와 현장 방문을 통한 시장 조사를 단 한 번의 클릭만으로 끝내는"* → 기존 프로세스가 너무 오래 걸린다는 암시적 불만 (Level 3)
- 부동산플래닛 언급: *"거래가 적어 시세 추정이 어려워서다"* → 정보 부족으로 인한 의사결정 지연 (Level 3)
- 토지프로 포지셔닝: *"정보 비대칭성을 해소하고 의사결정 과정을 효율적으로 혁신"* → 현재 프로세스가 비효율적이라는 인정 (Level 3)

**우리의 Push 메시지**: 
> *"토지 사업성 검토, 이제 외주 없이 60초면 끝낸다. 승인 확률·특례법·투자금을 AI가 자동 산출."*

---

### Pull 요인 (차별 가치)

1. **승인 확률 자동 산출 (경쟁사 미흡)**
   - 토지프로·크레마오·부동산플래닛 모두 "사업성 분석"을 표방하지만, 구체적인 "인허가 승인 확률(%)" 산출 기능은 명시되지 않음
   - **우리의 가치**: 문서 업로드만으로 용도지역·건축법·지역 규제 기반 승인 확률 자동 계산 → 시행사가 "진행/중단" 의사결정을 수치로 정당화 가능

2. **특례법 자동 판정 (블루오션)**
   - 경쟁사 중 도시재생·혁신도시·규제자유특구 등 특례법 해당 여부를 자동 판정하는 기능 명시 없음
   - **우리의 가치**: 토지 위치 기반 특례법 자동 매칭 → 건축사무소가 고객에게 "이 토지는 특구 해당으로 규제 완화 가능" 즉시 제안 가능

3. **정책 흐름 모니터링 (P1 기능, 경쟁사 부재)**
   - 모든 경쟁사가 "정책 변동 자동 감지 & 알림" 기능 미표기
   - **우리의 가치**: 해당 지역의 최근 3개월 정책 변동(용도지역 변경, 규제 완화 등)을 자동 수집 & 분석 → 정책 변동기(2024~2025)에 경쟁사 공백 활용

---

### Inertia 감소 (전환 비용 최소화)

- **마이그레이션 도구**: 기존 엑셀·PDF 분석 자료를 업로드하면 자동 파싱 (OCR + 텍스트 추출) → 수작업 재입력 제거
- **학습 곡선 최소화**: 
  - 온보딩: 3단계 (파일 업로드 → 자동 추출 검증 → 분석 실행)
  - 템플릿: 토지 개요서·법률서 샘플 제공 (어떤 문서를 준비해야 하는지 명확)
  - 튜토리얼: 5분 데모 영상 (시행사 실무자 기준)
- **팀 확산**: 팀 멤버 초대 기능 (소장 + 실무자 2명 동시 접근) → 한 번의 구독으로 팀 전체 사용 가능

---

### Anxiety 해소 (신뢰 신호)

- **무료 체험**: 
  - 가입 후 첫 분석 1건 무료 (크레딧 제공)
  - 기간: 14일 무제한 사용 (신용카드 등록 불필요)
  - 조건: 이메일 인증만 필수
  
- **보증**:
  - 데이터 안전: "모든 업로드 문서는 암호화 저장, 고객 동의 없이 제3자 공유 금지" 명시
  - 환불: 첫 30일 내 만족하지 않으면 100% 환불 (구독료)
  - SLA: "분석 결과 생성 시간 ≤5분 보장, 초과 시 크레딧 환급"
  
- **사회적 증명**:
  - 초기 파일럿 고객 3~5개사 사례 (회사명 + 업종 + "분석 시간 80% 단축" 정량 결과)
  - 건축사협회·시행사협회 추천 (Phase 2 목표)
  - 언론 보도: "AI로 토지 사업성 검토 시간 5일→30분" (PR 기획)

---

## Evidence Appendix (기능 ↔ 페인포인트 trace)

### P0 기능 1: 문서 업로드 & 파싱

> *"토지대장, 건축물대장 등 많은 서류 검토와 현장 방문을 통한 시장 조사를 단 한 번의 클릭만으로 끝내는"*
— 크레마오 포지셔닝 (서윤 Phase 1, Level 3, 시행사/건축사무소)

**반영 방식**: 기존 수작업(서류 검토 + 현장 방문)을 "파일 업로드 1회"로 단축하기 위해, 토지 개요서(PDF)·법률서(DOCX) 자동 파싱 기능을 P0 최우선으로 설정. OCR + 텍스트 추출로 스캔 이미지 포함 문서도 처리 가능하게 구현.

---

### P0 기능 2: 기본 정보 추출

> *"정보 비대칭성을 해소하고 의사결정 과정을 효율적으로 혁신"*
— 토지프로 포지셔닝 (서윤 Phase 1, Level 2~3, 개발업체/시행사)

**반영 방식**: 문서에서 토지 위치·면적·용도지역·현황을 자동 추출하여, 시행사가 "정보 부족으로 인한 의사결정 지연"을 해소할 수 있도록 설계. 추출된 정보는 사용자가 검증·수정 가능하게 함 (신뢰도 향상).

---

### P0 기능 3: 승인 확률 산출

> *"거래가 적어 시세 추정이 어려워서다"* (정보 부족 → 의사결정 어려움)
— 부동산플래닛 언급 (서윤 Phase 1, Level 3, 개발업체)

**반영 방식**: 기존 경쟁사는 "시세 추정"에만 집중했으나, 우리는 한 단계 더 나아가 "인허가 승인 확률"을 자동 산출. 용도지역·건축법·지역 규제를 AI가 분석하여 "이 토지가 실제로 개발 승인될 확률은 몇 %인가"를 정량화. 시행사가 "진행/중단" 의사결정을 수치로 정당화 가능.

---

### P0 기능 4: 분석 결과 대시보드

> *"단 한 번의 클릭만으로 끝내는"*
— 크레마오 (서윤 Phase 1, Level 3)

**반영 방식**: 분석 결과(승인 확률, 개발 가능성, 투자금 범위)를 한눈에 보는 대시보드로 설계. 복잡한 리포트 대신 "게이지 + 숫자 + 슬라이더" 시각화로 의사결정 속도 극대화.

---

### P0 기능 5: 결과 PDF 리포트 생성

> *"토지대장, 건축물대장 등 많은 서류 검토"* (현재 수작업으로 리포트 작성)
— 크레마오 (서윤 Phase 1, Level 3, 건축사무소)

**반영 방식**: 건축사무소가 고객에게 제출할 "제안용 PDF 리포트"를 자동 생성. 기존에는 분석 결과를 수작업으로 PowerPoint/Word에 정리했으나, 우리는 "PDF 생성" 버튼 1클릭으로 브랜딩된 리포트 생성. 건축사무소의 고객 제안 시간 단축.

---

### P1 기능 1: 특례법 해당 여부 판정

> *"정보 비대칭성을 해소"* (특례법 해당 여부를 모르면 의사결정 불가)
— 토지프로 (서윤 Phase 1, Level 2~3)

**반영 방식**: 도시재생·혁신도시·규제자유특구 등 특례법을 토지 위치 기반으로 자동 판정. 경쟁사(크레마오·부동산플래닛·랜드업)는 이 기능을 명시하지 않았으므로 블루오션. 시행사가 "이 토지는 특구 해당으로 규제 완화 가능"을 즉시 파악 가능.

---

### P1 기능 2: 정책 흐름 분석

> *"정보 비대칭성을 해소하고 의사결정 과정을 효율적으로 혁신"*
— 토지프로 (서윤 Phase 1, Level 2~3)

**반영 방식**: 해당 지역의 최근 3개월 정책 변동(용도지역 변경, 규제 완화 등)을 자동 수집 & 분석하여 대시보드에 타임라인으로 표시. 정책 변동기(2024~2025)에 경쟁사가 제공하지 않는 기능으로, 시행사가 "정책 변동으로 인한 기회/위험"을 사전 파악 가능.

---

### P1 기능 3: 투자금 범위 예측

> *"거래가 적어 시세 추정이 어려워서다"* (투자금 범위 추정 어려움)
— 부동산플래닛 (서윤 Phase 1, Level 3)

**반영 방식**: 토지 규모·용도·지역 기반으로 개발 투자금 범위(최소~최대)를 자동 산출. 시행사가 자금 조달 계획 수립 시 "이 토지에 50~80억 원 투자 필요"를 즉시 파악 가능. 경쟁사는 "사업성 분석"을 표방하지만 구체적인 투자금 범위 산출 기능은 미흡.

---

### P1 기능 4: 비교 분석 (다중 토지)

> *"정보 비대칭성을 해소"* (여러 토지를 동시 비교하려면 각각 분석 필요)
— 토지프로 (서윤 Phase 1, Level 2~3, 개발업체 심사팀)

**반영 방식**: 개발업체 심사팀이 월 20개 토지를 검토할 때, 각 토지를 개별 분석 후 비교 테이블로 정렬(승인 확률 순). 기존에는 각 토지마다 외부 컨설턴트 의뢰(건당 100만원, 월 2,000만원 비용)가 필요했으나, 우리는 자동화로 "월 1,500만원 비용 절감" 실현.

---

### P1 기능 5: 분석 이력 저장 & 검색

> *"거래가 적어 시세 추정이 어려워서다"* (같은 토지 재분석 시 비용 중복)
— 부동산플래닛 (서윤 Phase 1, Level 3)

**반영 방식**: 과거 분석 결과를 저장하여, 같은 토지 재분석 시 크레딧 비용 절감. 시행사가 "이 토지는 3개월 전에 분석했는데, 정책 변동이 있었나?" 확인 가능. 구독 유지율 향상.

---

### P1 기능 6: API 제공 (기본)

> *"정보 비대칭성을 해소"* (외부 시스템과 연동 필요)
— 토지프로 (서윤 Phase 1, Level 2~3, 대형 개발업체)

**반영 방식**: 고객사가 자체 부동산 관리 소프트웨어(ERP 등)와 LandAnalytics를 연동하려면 REST API 제공 필수. 대형 개발업체는 "우리 시스템과 통합 가능한가"를 구매 조건으로 제시하므로, API 제공으로 업셀 트리거 확보.

---

**종합 평가**:
- **P0 기능 5개**: 모두 서윤 Phase 1 evidence (Level 2~3)에 trace 가능
- **P1 기능 6개**: 모두 경쟁사 미흡 또는 블루오션 갭 기반 설계
- **미trace 기능**: 없음 (모든 P0/P1 기능이 pain point 또는 경쟁사 약점 기반)