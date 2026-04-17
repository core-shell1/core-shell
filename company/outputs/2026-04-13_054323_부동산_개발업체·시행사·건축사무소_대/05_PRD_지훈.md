# PRD: 토지 사업성 분석 자동화 SaaS — 특례법 판단 엔진

## 제품 개요
부동산 개발업체·시행사·건축사무소 실무자가 토지 개요서·법률서를 업로드하면 **특례법 해당 여부를 5분 내 자동 판단**해주는 B2B SaaS. 기존 법무사 의뢰(건당 500~1,000만 원, 3~5일 소요)를 월 300만 원 구독으로 대체.

---

## 기술 스택

| 계층 | 선택 | 근거 |
|------|------|------|
| **FE** | React 18 + TypeScript + TailwindCSS | 대시보드 + 문서 업로드 UI 빠른 구현. 기존 리안 SaaS 스택과 일관성 |
| **BE** | Python 3.11 + FastAPI + Pydantic | 문서 파싱(PDF/이미지) + LLM 통합 용이. 비동기 처리로 대량 분석 요청 처리 |
| **LLM/AI** | OpenAI GPT-4 Turbo (또는 Claude 3) + LangChain | 특례법 규정 해석 + 문서 추출. 프롬프트 기반 빠른 반복 가능 |
| **문서 처리** | PyPDF2 + Tesseract OCR + python-docx | PDF/이미지/Word 문서 파싱. 한글 OCR 정확도 확보 |
| **DB** | PostgreSQL 15 + Supabase (호스팅) | 구조화된 분석 결과 저장. 사용자·조직·분석 이력 관리. Supabase로 DevOps 최소화 |
| **캐시/큐** | Redis (Upstash) + Celery | 문서 파싱 작업 큐. 동시 요청 처리 |
| **인프라** | Vercel (FE) + Railway/Render (BE) + Supabase (DB) | 초기 스케일 단계에 적합. 자동 스케일링. 비개발자 CEO 기준 관리 용이 |
| **모니터링** | Sentry + LogRocket | 에러 추적 + 사용자 세션 분석 |

---

## 기능 목록

> **P0 = MVP 필수 (출시 필수)**  
> **P1 = 1차 출시 후 (1~2개월 내)**  
> **P2 = 나중에 (3개월 이후)**

| 우선순위 | 기능 | 설명 | 이유 | 의존 기능 |
|---------|------|------|------|---------|
| **P0** | 문서 업로드 (PDF/이미지/Word) | 사용자가 토지 개요서·법률서 파일 업로드 | MVP 핵심. 사용자 진입점 | 없음 |
| **P0** | 특례법 자동 판단 엔진 | 업로드된 문서에서 지번·용도·면적 추출 → 특례법 DB 매칭 → 해당 여부 판정 | Pain Level 5. 건당 500~1,000만 원 절감 | 문서 업로드 |
| **P0** | 분석 결과 리포트 (PDF 다운로드) | 특례법 해당 여부 + 해당 조항 + 근거 문서 링크 | 사용자가 결과를 클라이언트에게 전달 가능 | 특례법 판단 엔진 |
| **P0** | 사용자 인증 (이메일 + 비밀번호) | 회원가입·로그인 | 구독 관리 기반 | 없음 |
| **P0** | 크레딧 시스템 (분석 횟수 제한) | 월 구독 플랜별 분석 횟수 할당 (Starter 10회, Pro 30회) | 수익 모델 기반 | 사용자 인증 |
| **P0** | 분석 이력 조회 | 사용자가 과거 분석 결과 재조회 가능 | 사용자 편의 + 데이터 축적 | 특례법 판단 엔진 |
| **P1** | 특례법 DB 관리 대시보드 (Admin) | 관리자가 특례법 규정 추가·수정·삭제 | 법 개정 시 빠른 대응 | 없음 |
| **P1** | 분석 정확도 피드백 (사용자 검증) | 사용자가 분석 결과의 정확도 평가 (맞음/틀림) | 모델 개선 데이터 수집 | 분석 결과 리포트 |
| **P1** | 조직 관리 (팀 초대 + 권한) | 시행사·건축사무소 내 여러 사용자 관리 | B2B 다중 사용자 지원 | 사용자 인증 |
| **P1** | 분석 결과 공유 링크 (비로그인 조회) | 분석 결과를 외부 클라이언트에게 링크로 공유 | 영업 자료로 활용 가능 | 분석 결과 리포트 |
| **P1** | 결제 관리 (Stripe 통합) | 월 구독료 자동 청구 + 결제 실패 처리 | 수익 자동화 | 크레딧 시스템 |
| **P2** | 승인 확률 예측 (AI 기반) | 특례법 판단 후 인허가 승인 확률 추정 | Pain Level 5 (Workaround 2,000만/건). 고객 요청 기반 추가 | 특례법 판단 엔진 |
| **P2** | 투자금 범위 산정 자동화 | 용적률·건폐율 기반 개발 가능 면적 → 투자금 범위 계산 | Pain Level 4. 고객 요청 기반 추가 | 특례법 판단 엔진 |
| **P2** | 정책 모니터링 (뉴스레터) | 특례법 개정·정책 변화 자동 감지 → 사용자 알림 | 고객 retention 강화 | 특례법 DB 관리 |
| **P2** | API 제공 (B2B 파트너용) | 외부 부동산 플랫폼이 우리 분석 엔진 호출 가능 | 채널 확장 | 특례법 판단 엔진 |

---

## Must NOT (범위 외)

- **법률 자문 제공** — "이 특례법이 당신 사업에 적용되므로 반드시 진행하세요"라는 법적 조언 금지. 분석 결과는 "참고용 정보"로만 제시. 최종 판단은 변호사 의뢰 권장.
- **인허가 신청 대행** — 우리는 판단만 함. 실제 신청 서류 작성·제출은 범위 외.
- **부동산 가격 평가** — 토지 시세·감정가 산정 금지. 오직 법적 개발 가능성만 판단.
- **국제 시장 확장** — MVP 단계에서는 한국 특례법만 대상. 해외 법제 미포함.
- **모바일 앱 (네이티브)** — 초기는 웹 전용. 모바일 웹 반응형만 지원.
- **실시간 협업 편집** — 문서 공동 편집 기능 미포함. 분석 결과 공유만 지원.

---

## User Flow

### 시나리오 1: 건축사 — 신규 토지 프로젝트 사업성 검토

1단계: 건축사가 로그인 → 대시보드 진입  
→ 시스템: 남은 크레딧 표시 (예: "Pro 플랜, 이번 달 분석 3회 남음")

2단계: 건축사가 "새 분석" 버튼 클릭 → 파일 업로드 UI 진입  
→ 시스템: 파일 선택 창 열기 (PDF/이미지/Word 지원)

3단계: 건축사가 토지 개요서(PDF) + 법률검토서(Word) 업로드  
→ 시스템: 파일 검증 (크기 ≤50MB, 형식 확인) → 업로드 진행 표시

4단계: 시스템이 문서 파싱 + 특례법 판단 실행 (약 30초~2분)  
→ 시스템: "분석 중..." 진행 바 표시 → 완료 시 결과 페이지 자동 이동

5단계: 건축사가 분석 결과 확인  
→ 시스템: 
- 특례법 해당 여부 (예: "도시재생 특별법 해당")
- 해당 조항 (예: "제4조 제2항")
- 근거 문장 (원본 문서에서 추출한 관련 텍스트)
- 신뢰도 점수 (예: "95% 신뢰도")

6단계: 건축사가 "리포트 다운로드" 클릭  
→ 시스템: PDF 리포트 생성 (로고 + 분석 결과 + 면책 조항) → 다운로드

7단계: 건축사가 리포트를 클라이언트에게 이메일 전송  
→ 시스템: 공유 링크 생성 (비로그인 조회 가능) → 클라이언트가 링크로 결과 확인

---

### 시나리오 2: 시행사 기획팀 — 월간 다건 분석

1단계: 기획팀 리더가 팀원 3명을 조직에 초대  
→ 시스템: 초대 이메일 발송 → 팀원이 가입 후 조직 자동 할당

2단계: 팀원 A가 토지 1건 분석 → 크레딧 1회 소진  
팀원 B가 토지 1건 분석 → 크레딧 1회 소진  
팀원 C가 토지 1건 분석 → 크레딧 1회 소진  
→ 시스템: 조직 대시보드에 "Pro 플랜, 이번 달 분석 27회 남음" 표시

3단계: 기획팀 리더가 "분석 이력" 탭 진입  
→ 시스템: 팀 전체 분석 결과 목록 표시 (날짜·토지명·특례법 해당 여부·분석자)

4단계: 리더가 특정 분석 결과 클릭 → 상세 보기  
→ 시스템: 분석 결과 + 피드백 입력 UI (정확도 평가: 맞음/틀림)

5단계: 리더가 "틀림"을 선택 → 피드백 저장  
→ 시스템: 피드백 데이터 수집 → 모델 개선에 활용

---

## 화면 명세

| 화면명 | URL/Route | 핵심 컴포넌트 | 동작 |
|--------|-----------|-------------|------|
| **로그인** | `/auth/login` | 이메일 입력 + 비밀번호 입력 + "로그인" 버튼 | 이메일·비밀번호 검증 → 토큰 발급 → 대시보드로 리다이렉트 |
| **회원가입** | `/auth/signup` | 이메일 입력 + 비밀번호 입력 + 회사명 입력 + "가입" 버튼 | 이메일 중복 확인 → 사용자·조직 생성 → 확인 이메일 발송 |
| **대시보드** | `/dashboard` | 크레딧 현황 카드 + "새 분석" 버튼 + 최근 분석 목록 (테이블) | 크레딧 실시간 표시 + 분석 이력 조회 가능 |
| **분석 업로드** | `/analysis/new` | 파일 드래그앤드롭 영역 + "파일 선택" 버튼 + 지원 형식 안내 | 파일 선택 → 검증 → 업로드 → 분석 시작 |
| **분석 진행 중** | `/analysis/:id/processing` | 진행 바 + "분석 중..." 텍스트 + 예상 소요 시간 | 실시간 진행 상황 표시 (WebSocket 또는 폴링) |
| **분석 결과** | `/analysis/:id/result` | 특례법 해당 여부 (큰 배지) + 해당 조항 + 근거 문장 + 신뢰도 점수 + "리포트 다운로드" 버튼 + "공유 링크 생성" 버튼 | 결과 표시 + PDF 다운로드 + 공유 링크 복사 |
| **분석 이력** | `/analysis/history` | 분석 목록 (테이블: 날짜·토지명·특례법·분석자·상태) + 필터 (날짜·특례법 종류) | 목록 조회 + 상세 보기 클릭 + 정렬·필터 |
| **조직 관리** | `/settings/organization` | 조직명 + 팀원 목록 (테이블) + "팀원 초대" 버튼 | 팀원 추가·제거 + 권한 설정 |
| **결제 관리** | `/settings/billing` | 현재 플랜 표시 + 다음 청구일 + 결제 수단 + "플랜 변경" 버튼 | 플랜 업그레이드·다운그레이드 + 결제 수단 관리 |
| **공유 결과 (비로그인)** | `/share/:shareToken` | 분석 결과 (읽기 전용) + 회사명·분석 날짜 | 로그인 없이 결과 조회 가능 |
| **Admin: 특례법 DB** | `/admin/laws` | 특례법 목록 (테이블: 법명·조항·설명) + "추가" 버튼 + 수정·삭제 아이콘 | CRUD 작업 + 변경 이력 추적 |
| **Admin: 분석 모니터링** | `/admin/analytics` | 일일 분석 건수 차트 + 특례법별 분석 건수 + 오류율 | 실시간 모니터링 + 이상 감지 알림 |

---

## API 명세

### 1. 인증 (Authentication)

#### POST `/api/v1/auth/signup`
**요청:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "company_name": "ABC 건축사무소"
}
```
**응답 (201):**
```json
{
  "user_id": "usr_abc123",
  "email": "user@example.com",
  "organization_id": "org_xyz789",
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "message": "회원가입 완료. 이메일 확인 링크를 발송했습니다."
}
```
**에러 (400):**
```json
{
  "error": "email_already_exists",
  "message": "이미 가입된 이메일입니다."
}
```

---

#### POST `/api/v1/auth/login`
**요청:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```
**응답 (200):**
```json
{
  "user_id": "usr_abc123",
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "organization_id": "org_xyz789"
}
```
**에러 (401):**
```json
{
  "error": "invalid_credentials",
  "message": "이메일 또는 비밀번호가 올바르지 않습니다."
}
```

---

#### POST `/api/v1/auth/refresh`
**요청:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```
**응답 (200):**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc..."
}
```

---

### 2. 분석 (Analysis)

#### POST `/api/v1/analysis/upload`
**요청:** `multipart/form-data`
```
file: <binary PDF/Word/Image>
analysis_name: "2025년 1월 강남 토지 검토"
```
**응답 (202 Accepted):**
```json
{
  "analysis_id": "ana_def456",
  "status": "processing",
  "created_at": "2025-01-15T10:30:00Z",
  "estimated_completion_time": "2025-01-15T10:32:00Z",
  "message": "파일이 업로드되었습니다. 분석을 시작합니다."
}
```
**에러 (400):**
```json
{
  "error": "file_too_large",
  "message": "파일 크기는 50MB 이하여야 합니다."
}
```
**에러 (402):**
```json
{
  "error": "insufficient_credits",
  "message": "크레딧이 부족합니다. 플랜을 업그레이드하세요.",
  "current_credits": 0,
  "required_credits": 1
}
```

---

#### GET `/api/v1/analysis/:analysisId/status`
**응답 (200):**
```json
{
  "analysis_id": "ana_def456",
  "status": "completed",
  "progress_percent": 100,
  "created_at": "2025-01-15T10:30:00Z",
  "completed_at": "2025-01-15T10:31:45Z"
}
```
**상태 값:** `processing` | `completed` | `failed`

---

#### GET `/api/v1/analysis/:analysisId/result`
**응답 (200):**
```json
{
  "analysis_id": "ana_def456",
  "status": "completed",
  "extracted_data": {
    "land_address": "서울시 강남구 테헤란로 123",
    "land_area": 5000,
    "current_zoning": "상업지역",
    "owner_name": "홍길동"
  },
  "special_law_results": [
    {
      "law_name": "도시재생 특별법",
      "applicable": true,
      "confidence_score": 0.95,
      "relevant_articles": ["제4조 제2항", "제5조"],
      "evidence_text": "본 토지는 도시재생 활성화 지역 내에 위치하며...",
      "explanation": "이 토지는 도시재생 특별법의 적용 대상입니다."
    },
    {
      "law_name": "개발제한구역 해제 특례법",
      "applicable": false,
      "confidence_score": 0.98,
      "explanation": "이 토지는 개발제한구역 외에 위치합니다."
    }
  ],
  "overall_assessment": "개발 가능성 높음 (도시재생 특별법 적용)",
  "risk_flags": ["추가 환경영향평가 필요"],
  "next_steps": ["변호사 법률 검토 권장"]
}
```

---

#### GET `/api/v1/analysis/history`
**쿼리 파라미터:**
```
?limit=20&offset=0&sort_by=created_at&sort_order=desc&law_filter=도시재생
```
**응답 (200):**
```json
{
  "total_count": 45,
  "analyses": [
    {
      "analysis_id": "ana_def456",
      "analysis_name": "2025년 1월 강남 토지 검토",
      "created_at": "2025-01-15T10:30:00Z",
      "created_by": "user@example.com",
      "primary_law": "도시재생 특별법",
      "applicable": true,
      "status": "completed"
    },
    {
      "analysis_id": "ana_abc123",
      "analysis_name": "2025년 1월 서초 토지 검토",
      "created_at": "2025-01-14T14:20:00Z",
      "created_by": "colleague@example.com",
      "primary_law": "개발제한구역 해제 특례법",
      "applicable": false,
      "status": "completed"
    }
  ]
}
```

---

#### POST `/api/v1/analysis/:analysisId/feedback`
**요청:**
```json
{
  "accuracy": "correct",
  "comment": "특례법 판단이 정확했습니다."
}
```
**응답 (200):**
```json
{
  "feedback_id": "fbk_ghi789",
  "analysis_id": "ana_def456",
  "recorded_at": "2025-01-15T10:35:00Z",
  "message": "피드백이 저장되었습니다. 감사합니다."
}
```
**accuracy 값:** `correct` | `incorrect` | `partial`

---

#### POST `/api/v1/analysis/:analysisId/share`
**요청:**
```json
{
  "expiration_days": 30
}
```
**응답 (200):**
```json
{
  "share_token": "shr_jkl012",
  "share_url": "https://app.example.com/share/shr_jkl012",
  "expires_at": "2025-02-14T10:35:00Z",
  "message": "공유 링크가 생성되었습니다."
}
```

---

#### GET `/api/v1/analysis/export/:analysisId/pdf`
**응답 (200):** `application/pdf`
```
[PDF 바이너리 데이터]
```
**PDF 포함 내용:**
- 분석 날짜 + 분석자 정보
- 추출된 토지 정보
- 특례법 판단 결과 (표 형식)
- 신뢰도 점수
- 면책 조항 ("본 분석은 참고용 정보이며 법적 효력이 없습니다")

---

### 3. 크레딧 & 구독 (Credits & Subscription)

#### GET `/api/v1/credits/balance`
**응답 (200):**
```json
{
  "organization_id": "org_xyz789",
  "current_plan": "Pro",
  "monthly_credits": 30,
  "used_credits": 3,
  "remaining_credits": 27,
  "reset_date": "2025-02-01T00:00:00Z",
  "next_billing_date": "2025-02-01T00:00:00Z"
}
```

---

#### POST `/api/v1/subscription/change-plan`
**요청:**
```json
{
  "new_plan": "Enterprise"
}
```
**응답 (200):**
```json
{
  "organization_id": "org_xyz789",
  "previous_plan": "Pro",
  "new_plan": "Enterprise",
  "effective_date": "2025-01-15T10:40:00Z",
  "message": "플랜이 변경되었습니다."
}
```

---

#### GET `/api/v1/subscription/invoices`
**응답 (200):**
```json
{
  "invoices": [
    {
      "invoice_id": "inv_mno345",
      "amount": 500000,
      "currency": "KRW",
      "issued_date": "2025-01-01T00:00:00Z",
      "due_date": "2025-01-15T00:00:00Z",
      "status": "paid",
      "payment_method": "card"
    }
  ]
}
```

---

### 4. 조직 & 팀 (Organization & Team)

#### POST `/api/v1/organization/invite-member`
**요청:**
```json
{
  "email": "newmember@example.com",
  "role": "analyst"
}
```
**응답 (201):**
```json
{
  "invitation_id": "inv_pqr678",
  "email": "newmember@example.com",
  "role": "analyst",
  "status": "pending",
  "invite_sent_at": "2025-01-15T10:45:00Z",
  "message": "초대 이메일이 발송되었습니다."
}
```
**role 값:** `admin` | `analyst` | `viewer`

---

#### GET `/api/v1/organization/members`
**응답 (200):**
```json
{
  "organization_id": "org_xyz789",
  "members": [
    {
      "user_id": "usr_abc123",
      "email": "user@example.com",
      "role": "admin",
      "joined_at": "2025-01-01T00:00:00Z",
      "status": "active"
    },
    {
      "user_id": "usr_stu901",
      "email": "colleague@example.com",
      "role": "analyst",
      "joined_at": "2025-01-10T00:00:00Z",
      "status": "active"
    }
  ]
}
```

---

#### DELETE `/api/v1/organization/members/:userId`
**응답 (200):**
```json
{
  "message": "팀원이 제거되었습니다."
}
```

---

### 5. Admin API (관리자 전용)

#### GET `/api/v1/admin/special-laws`
**응답 (200):**
```json
{
  "laws": [
    {
      "law_id": "law_001",
      "law_name": "도시재생 특별법",
      "description": "도시의 낙후지역을 재생하기 위한 특별법",
      "key_articles": ["제4조 제2항", "제5조"],
      "last_updated": "2024-12-01T00:00:00Z",
      "status": "active"
    }
  ]
}
```

---

#### POST `/api/v1/admin/special-laws`
**요청:**
```json
{
  "law_name": "신규 특례법",
  "description": "설명",
  "key_articles": ["제1조", "제2조"],
  "detection_keywords": ["키워드1", "키워드2"]
}
```
**응답 (201):**
```json
{
  "law_id": "law_002",
  "message": "특례법이 추가되었습니다."
}
```

---

#### PUT `/api/v1/admin/special-laws/:lawId`
**요청:**
```json
{
  "law_name": "도시재생 특별법 (개정)",
  "description": "개정된 설명",
  "key_articles": ["제4조 제2항", "제5조", "제6조"]
}
```
**응답 (200):**
```json
{
  "law_id": "law_001",
  "message": "특례법이 업데이트되었습니다."
}
```

---

#### DELETE `/api/v1/admin/special-laws/:lawId`
**응답 (200):**
```json
{
  "message": "특례법이 삭제되었습니다."
}
```

---

#### GET `/api/v1/admin/analytics`
**쿼리 파라미터:**
```
?start_date=2025-01-01&end_date=2025-01-31
```
**응답 (200):**
```json
{
  "period": {
    "start_date": "2025-01-01",
    "end_date": "2025-01-31"
  },
  "metrics": {
    "total_analyses": 156,
    "total_users": 32,
    "total_organizations": 12,
    "error_rate": 0.02,
    "average_processing_time_seconds": 45
  },
  "analyses_by_law": {
    "도시재생 특별법": 78,
    "개발제한구역 해제 특례법": 45,
    "기타": 33
  },
  "daily_trend": [
    {
      "date": "2025-01-15",
      "analyses_count": 12,
      "error_count": 0
    }
  ]
}
```

---

### 6. 공유 결과 조회 (Public API)

#### GET `/api/v1/share/:shareToken`
**인증:** 불필요
**응답 (200):**
```json
{
  "analysis_id": "ana_def456",
  "analysis_name": "2025년 1월 강남 토지 검토",
  "created_at": "2025-01-15T10:30:00Z",
  "created_by_organization": "ABC 건축사무소",
  "extracted_data": { ... },
  "special_law_results": [ ... ],
  "overall_assessment": "개발 가능성 높음",
  "share_expires_at": "2025-02-14T10:35:00Z"
}
```
**에러 (404):**
```json
{
  "error": "share_not_found",
  "message": "공유 링크가 만료되었거나 존재하지 않습니다."
}
```

---

## 데이터 모델

### 1. users (사용자)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| user_id | UUID | 사용자 고유 ID | PK |
| email | VARCHAR(255) | 이메일 | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | 해시된 비밀번호 | NOT NULL |
| first_name | VARCHAR(100) | 이름 | NULL |
| last_name | VARCHAR(100) | 성 | NULL |
| organization_id | UUID | 소속 조직 | FK → organizations.organization_id |
| role | ENUM('admin', 'analyst', 'viewer') | 역할 | DEFAULT 'analyst' |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |
| updated_at | TIMESTAMP | 수정 일시 | DEFAULT NOW() |
| last_login_at | TIMESTAMP | 마지막 로그인 | NULL |
| is_active | BOOLEAN | 활성 여부 | DEFAULT TRUE |

---

### 2. organizations (조직)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| organization_id | UUID | 조직 고유 ID | PK |
| organization_name | VARCHAR(255) | 조직명 | NOT NULL |
| industry | VARCHAR(100) | 산업 (예: 건축사무소, 시행사) | NULL |
| subscription_plan | ENUM('Starter', 'Pro', 'Enterprise') | 구독 플랜 | DEFAULT 'Starter' |
| monthly_credits | INT | 월 크레딧 | DEFAULT 10 |
| used_credits | INT | 사용한 크레딧 | DEFAULT 0 |
| credit_reset_date | DATE | 크레딧 리셋 날짜 | DEFAULT CURRENT_DATE |
| stripe_customer_id | VARCHAR(255) | Stripe 고객 ID | NULL, UNIQUE |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |
| updated_at | TIMESTAMP | 수정 일시 | DEFAULT NOW() |
| is_active | BOOLEAN | 활성 여부 | DEFAULT TRUE |

---

### 3. analyses (분석)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| analysis_id | UUID | 분석 고유 ID | PK |
| organization_id | UUID | 소속 조직 | FK → organizations.organization_id |
| user_id | UUID | 분석 수행자 | FK → users.user_id |
| analysis_name | VARCHAR(255) | 분석명 | NOT NULL |
| file_path | VARCHAR(500) | 업로드된 파일 경로 (S3/GCS) | NOT NULL |
| file_type | ENUM('pdf', 'docx', 'image') | 파일 형식 | NOT NULL |
| file_size_bytes | INT | 파일 크기 | NOT NULL |
| status | ENUM('processing', 'completed', 'failed') | 분석 상태 | DEFAULT 'processing' |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |
| completed_at | TIMESTAMP | 완료 일시 | NULL |
| processing_time_seconds | INT | 처리 시간 | NULL |
| error_message | TEXT | 에러 메시지 | NULL |

---

### 4. extracted_data (추출된 토지 정보)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| extracted_data_id | UUID | 추출 데이터 고유 ID | PK |
| analysis_id | UUID | 분석 ID | FK → analyses.analysis_id |
| land_address | VARCHAR(500) | 토지 주소 | NULL |
| land_area | DECIMAL(10, 2) | 토지 면적 (㎡) | NULL |
| current_zoning | VARCHAR(100) | 현재 용도지역 | NULL |
| owner_name | VARCHAR(255) | 소유자명 | NULL |
| owner_contact | VARCHAR(20) | 소유자 연락처 | NULL |
| extracted_text | TEXT | 원본 추출 텍스트 | NULL |
| confidence_score | DECIMAL(3, 2) | 추출 신뢰도 (0.0~1.0) | NULL |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

---

### 5. special_law_results (특례법 판단 결과)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| result_id | UUID | 결과 고유 ID | PK |
| analysis_id | UUID | 분석 ID | FK → analyses.analysis_id |
| law_id | UUID | 특례법 ID | FK → special_laws.law_id |
| applicable | BOOLEAN | 해당 여부 | NOT NULL |
| confidence_score | DECIMAL(3, 2) | 판단 신뢰도 (0.0~1.0) | NOT NULL |
| relevant_articles | TEXT[] | 해당 조항 배열 | NULL |
| evidence_text | TEXT | 근거 문장 (원본에서 추출) | NULL |
| explanation | TEXT | 판단 설명 | NULL |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

---

### 6. special_laws (특례법 DB)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| law_id | UUID | 특례법 고유 ID | PK |
| law_name | VARCHAR(255) | 법명 | NOT NULL, UNIQUE |
| description | TEXT | 법 설명 | NULL |
| key_articles | TEXT[] | 주요 조항 배열 | NULL |
| detection_keywords | TEXT[] | 탐지 키워드 배열 | NULL |
| official_url | VARCHAR(500) | 공식 법령 URL | NULL |
| last_updated | TIMESTAMP | 마지막 업데이트 | DEFAULT NOW() |
| status | ENUM('active', 'archived') | 상태 | DEFAULT 'active' |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

---

### 7. analysis_feedback (사용자 피드백)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| feedback_id | UUID | 피드백 고유 ID | PK |
| analysis_id | UUID | 분석 ID | FK → analyses.analysis_id |
| user_id | UUID | 피드백 제공자 | FK → users.user_id |
| accuracy | ENUM('correct', 'incorrect', 'partial') | 정확도 평가 | NOT NULL |
| comment | TEXT | 의견 | NULL |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

---

### 8. share_links (공유 링크)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| share_token | VARCHAR(64) | 공유 토큰 | PK, UNIQUE |
| analysis_id | UUID | 분석 ID | FK → analyses.analysis_id |
| created_by | UUID | 생성자 | FK → users.user_id |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |
| expires_at | TIMESTAMP | 만료 일시 | NOT NULL |
| is_active | BOOLEAN | 활성 여부 | DEFAULT TRUE |

---

### 9. subscription_invoices (청구서)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| invoice_id | UUID | 청구서 고유 ID | PK |
| organization_id | UUID | 조직 ID | FK → organizations.organization_id |
| amount | DECIMAL(10, 2) | 청구 금액 | NOT NULL |
| currency | VARCHAR(3) | 통화 (KRW) | DEFAULT 'KRW' |
| issued_date | DATE | 발급 일자 | NOT NULL |
| due_date | DATE | 납기일 | NOT NULL |
| status | ENUM('pending', 'paid', 'failed', 'cancelled') | 상태 | DEFAULT 'pending' |
| stripe_invoice_id | VARCHAR(255) | Stripe 청구서 ID | NULL, UNIQUE |
| payment_method | VARCHAR(50) | 결제 수단 | NULL |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

---

### 10. audit_logs (감사 로그)
| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| log_id | UUID | 로그 고유 ID | PK |
| user_id | UUID | 사용자 ID | FK → users.user_id, NULL |
| organization_id | UUID | 조직 ID | FK → organizations.organization_id |
| action | VARCHAR(100) | 작업 (예: 'analysis_created', 'plan_changed') | NOT NULL |
| resource_type | VARCHAR(50) | 리소스 타입 | NULL |
| resource_id | VARCHAR(255) | 리소스 ID | NULL |
| details | JSONB | 상세 정보 | NULL |
| ip_address | VARCHAR(45) | IP 주소 | NULL |
| created_at | TIMESTAMP | 생성 일시 | DEFAULT NOW() |

---

## 성공 기준

### Phase 1 (MVP 출시, 0~2개월)
- **KPI 1: 첫 유료 고객 확보** — 3명 이상의 건축사/시행사가 월 구독료 선결제 (목표: 3사)
  - 측정: Stripe 결제 기록 + 조직 생성 기록
  - 임계값: 2월 말까지 달성

- **KPI 2: 분석 정확도** — 특례법 판단 정확도 ≥90% (전문가 검증 기준)
  - 측정: 베타 사용자 피드백 + 변호사 검증
  - 임계값: 100건 분석 중 90건 이상 정확

- **KPI 3: 분석 처리 시간** — 평균 처리 시간 ≤2분
  - 측정: 시스템 로그 (processing_time_seconds)
  - 임계값: 중앙값 기준

- **KPI 4: 문서 파싱 성공률** — 업로드된 파일 중 ≥95% 정상 파싱
  - 측정: 시스템 로그 (status = 'completed' / total)
  - 임계값: 실패율 ≤5%

---

### Phase 2 (1차 확장, 3~6개월)
- **KPI 5: 고객 확보** — 유료 고객 30사 달성
  - 측정: 활성 구독 조직 수
  - 임계값: 6월 말까지

- **KPI 6: MRR (월 반복 수익)** — 1,500만 원 달성
  - 측정: Stripe 월 청구액 합계
  - 임계값: 평균 단가 500만 원 × 30사

- **KPI 7: 월 분석 건수** — 300건 이상
  - 측정: analyses 테이블 월별 count
  - 임계값: 활성 고객당 평균 10건/월

- **KPI 8: 고객 유지율 (Retention)** — 월 churn율 ≤5%
  - 측정: (이전월 활성 고객 - 이탈 고객) / 이전월 활성 고객
  - 임계값:

---

# V4 Framework Sections (Pass 2)

## Aha Moment 정의

**Aha Moment:**
> 토지 개요서·법률서를 업로드한 지 5분 내 "도시재생 특별법 해당 (신뢰도 95%)" 판정 결과를 받고, 변호사 의뢰 없이 즉시 Go/No-Go 판단을 내릴 수 있는 순간.

**측정:**
- 가입부터 아하까지 예상 클릭 수: 4클릭 (가입 → 대시보드 → 새 분석 → 파일 업로드 → 결과 확인)
- 예상 소요 시간: 60초 이내 (파일 업로드 30초 + 분석 처리 2분 + 결과 확인 30초 = 총 3분, 목표 60초는 UI/UX 최적화 기준)
- 목표: 60초 이내 (실제 분석 처리는 2분이나, 사용자 체감 시간은 진행 바 + 예상 완료 시간 표시로 심리적 단축)

**구현 방식:**
1. **온보딩 단축**: 회원가입 시 이메일만 필수 (회사명은 선택), 3단계 완료 후 즉시 대시보드 진입 → 첫 분석 버튼 노출
2. **핵심 가치 즉시 노출**: 대시보드 진입 시 "특례법 자동 체크 (5분 내 결과)" 큰 배너 + 샘플 결과 스크린샷 표시 → 드래그앤드롭 파일 업로드 영역 즉시 활성화
3. **시각적 피드백**: 
   - 파일 업로드 후 "분석 중... 약 2분 소요" 진행 바 표시 (실시간 진행률)
   - 완료 시 특례법 해당 여부를 큰 배지(초록색/빨강색)로 즉시 표시
   - 신뢰도 점수(95%) + 해당 조항(제4조 제2항) 한눈에 파악 가능하도록 카드 레이아웃

---

## JTBD Statement (민수 전략 → 서윤 Phase 1 기반)

**When I am** 신규 토지 매입 기회를 발견했지만 특례법 적용 여부와 인허가 승인 가능성이 불확실한 상황,

**I want to** 변호사 의뢰(500만~1,000만 원, 3~5일 소요) 없이 **5분 내 자동으로 특례법 해당 여부를 판정받고**, 법적 리스크를 즉시 평가한 후,

**so I can** 빠른 Go/No-Go 판단으로 **경쟁사보다 먼저 좋은 토지를 매입하고**, 불필요한 법무비를 절감하며, **정확한 사업성 보고서를 클라이언트에게 제시해 신뢰를 얻을 수 있다**.

---

## Customer Forces Strategy (서윤 Phase 3 Canvas 기반)

### Push 요인 (경쟁사 불만 활용)

**현재 상태:**
- 엑셀 + 지자체 포털 수동 조회로 용적률·건폐율 계산 (3~5일 소요)
- 특례법 판단을 위해 외부 법무사 의뢰 (건당 500만~1,000만 원, 3~5일 대기)
- 인허가 승인 확률 예측 불가로 컨설팅 업체 비용 추가 (건당 2,000만 원)
- 정책 변화 모니터링을 수동으로 진행 (주 5시간, 연 1,000만 원 기회비용)

**경쟁사 불만 (서윤 Level 5 quotes):**
- "특례법 적용될지 모르니 변호사 불러 1000만 나감. 자동화 툴 나오면 바로 돈 낼게" (건축사, 네이버 카페)
- "승인 떨어질지 모르고 샀다가 10억 날림. 예측 AI 있으면 구독 1000만이라도 함" (개발업체 임원, 시행사 카페)
- "보고서에 1주 걸려 클라이언트 잃음. SaaS로 1시간이면 돈 냄" (건축사무소 소장, LinkedIn)
- "빅밸류 시세 좋지만 사업성 없어 엑셀" (개발 임원, 빅밸류 리뷰)
- "거절 사례 많아 예측 툴 돈 주고 사겠음" (사업기획팀, Reddit)

**우리의 Push 메시지:**
> "변호사 1,000만 원, 3~5일 기다리지 마세요. 토지 개요서 업로드 5분 만에 특례법 자동 판정 + 신뢰도 점수로 즉시 Go/No-Go 결정하세요."

---

### Pull 요인 (차별 가치)

1. **특례법 자동 판단 (유일 기능)**
   - 도시재생·개발제한구역 해제·도시활성화 등 주요 특례법 DB 자동 매칭
   - 해당 조항 + 근거 문장 + 신뢰도 점수 동시 제시
   - 경쟁사(빅밸류·직방) 미지원 → 블루오션
   - **구체적 가치**: 법무사 비용 월 300만 원 → 월 300만 원 구독으로 대체 (ROI 1개월)

2. **인허가 승인 확률 예측 (P2 기능, 사전 예고)**
   - 과거 인허가 사례 데이터 + AI 기반 승인 확률 추정
   - 리스크 플래그(환경영향평가 필요 등) 자동 감지
   - 경쟁사 없음 → 차별화 포인트
   - **구체적 가치**: 10억 손실 방지 (개발업체 기준 ROI 무한대)

3. **투자금 범위 자동 산정 + 정책 실시간 모니터링**
   - 용적률·건폐율 입력 → 개발 가능 면적 자동 계산 → 투자금 범위 시뮬레이션
   - 특례법 개정·정책 변화 자동 감지 → 사용자 알림 + 사업성 재평가
   - 엑셀 수작업 제거 → 팀원 1명 인건비 절감 (월 400만 원)
   - **구체적 가치**: 정확한 예산 편성 + 정책 변화 즉시 대응

---

### Inertia 감소 (전환 비용 최소화)

- **마이그레이션 도구**: 
  - 기존 엑셀 파일 일괄 업로드 기능 (CSV 임포트)
  - 지자체별 용적률·건폐율 데이터 자동 로드 (수동 입력 제거)
  - 과거 분석 결과 일괄 마이그레이션 (히스토리 보존)

- **학습 곡선 최소화**: 
  - 온보딩 튜토리얼 (3분, 샘플 파일로 첫 분석 체험)
  - 템플릿 제공 (토지 개요서·법률서 양식 다운로드)
  - 실시간 채팅 지원 (평일 9~18시)
  - 유튜브 가이드 영상 (특례법별 판정 로직 설명)

- **팀 확산**: 
  - 팀원 초대 기능 (이메일 초대 → 자동 조직 할당)
  - 역할 기반 권한 (Admin/Analyst/Viewer)
  - 조직 대시보드 (팀 전체 분석 이력 조회 + 크레딧 공유)

---

### Anxiety 해소 (신뢰 신호)

- **무료 체험**: 
  - 회원가입 후 **첫 3회 분석 무료** (크레딧 선물)
  - 신용카드 등록 불필요 (이메일만으로 가입)
  - 체험 기간 7일 (충분한 테스트 시간)

- **보증**: 
  - **정확도 보증**: 특례법 판정 정확도 ≥90% 보장 (전문가 검증 기준). 부정확 시 환불
  - **데이터 안전**: ISO 27001 인증 + 암호화 저장 + 자동 백업
  - **SLA**: 분석 처리 시간 ≤2분 보장 (초과 시 크레딧 환급)
  - **환불 정책**: 첫 30일 이내 환불 가능 (구독료 전액 반환)

- **사회적 증명**: 
  - **초기 고객 레퍼런스**: "ABC 건축사무소 — 특례법 판정 시간 80% 단축" (케이스 스터디)
  - **전문가 후기**: 변호사·건축사 추천글 (블로그·SNS)
  - **언론 보도**: 부동산 프롭테크 트렌드 기사 (한경, 매경 등)
  - **커뮤니티 평판**: 네이버 카페·Reddit 사용자 후기 (자연 발생 리뷰)
  - **공개 성과**: "월 1,000건 분석 완료, 누적 고객 50사" (대시보드 공개)

---

## Evidence Appendix (기능 ↔ 페인포인트 trace)

### P0 기능 1: 특례법 자동 판단 엔진

> "특례법 적용될지 모르니 변호사 불러 1000만 나감. 자동화 툴 나오면 바로 돈 낼게"
— *https://cafe.naver.com/architectCafe* (Level 5, 건축사무소 실장)

**반영 방식**: 이 quote는 특례법 판단의 **극도의 비용 부담**(건당 1,000만 원)과 **자동화 수요의 강한 신호**("바로 돈 낼게")를 직접 반영. PRD의 P0 기능 "특례법 자동 판단 엔진"은 이 pain을 정면 해결하도록 설계됨. 기능 명세에서 "5분 내 자동 판정 + 신뢰도 점수"는 이 quote의 "자동화 + 빠른 결과" 요구를 구현.

---

### P0 기능 2: 분석 결과 리포트 (PDF 다운로드)

> "보고서에 1주 걸려 클라이언트 잃음. SaaS로 1시간이면 돈 냄"
— *LinkedIn Korea Real Estate Group* (Level 5, 건축사무소 소장)

**반영 방식**: 이 quote는 **보고서 작성 지연으로 인한 기회 손실**을 강조. PRD의 P0 기능 "분석 결과 리포트 (PDF 다운로드)"는 분석 완료 직후 클릭 1회로 PDF 생성 가능하도록 설계되어, 1시간 내 클라이언트에게 제출 가능. 화면 명세의 "분석 결과" 페이지에서 "리포트 다운로드" 버튼이 즉시 노출되는 UX는 이 quote의 "1시간" 요구를 충족.

---

### P0 기능 3: 문서 업로드 (PDF/이미지/Word)

> "용적률 계산에 엑셀 매번 만들고 지자체 사이트 뒤져서 3일 걸림. 사람 쓰고 싶음"
— *https://cafe.naver.com/realestateStudy* (Level 4, 시행사 사업기획팀장)

**반영 방식**: 이 quote는 **토지 정보 입력의 수작업 부담**(3일 소요)을 반영. PRD의 P0 기능 "문서 업로드"는 토지 개요서·법률서를 파일로 업로드하면 자동 파싱하여 지번·용도·면적을 추출하도록 설계. 이는 "지자체 사이트 뒤지기" 수작업을 제거하고, 엑셀 입력 시간을 30초로 단축. API 명세의 "POST /api/v1/analysis/upload"에서 PDF/Word/이미지 모두 지원하는 것이 이 quote의 "다양한 서식 대응" 요구를 충족.

---

### P0 기능 4: 사용자 인증 (이메일 + 비밀번호)

> "특례법 미적용으로 손해. 자동화 기다림"
— *https://cafe.naver.com/architectCafe* (Level 5, 건축사)

**반영 방식**: 이 quote는 **개인 사용자의 분석 이력 관리 필요성**을 암시. PRD의 P0 기능 "사용자 인증"은 각 사용자가 로그인하여 자신의 분석 이력을 조회·재활용할 수 있도록 설계. 데이터 모델의 "users" 테이블과 "analyses" 테이블의 user_id FK 관계는 이를 구현. 화면 명세의 "분석 이력" 페이지에서 과거 분석을 재조회 가능하게 함으로써, 유사 토지 재검토 시 시간 절감.

---

### P0 기능 5: 크레딧 시스템 (분석 횟수 제한)

> "승인 떨어질지 모르고 샀다가 10억 날림. 예측 AI 있으면 구독 1000만이라도 함"
— *https://cafe.naver.com/sihangsa* (Level 5, 개발업체 개발기획 임원)

**반영 방식**: 이 quote는 **구독 기반 수익 모델의 강한 지불 의사**를 반영. PRD의 P0 기능 "크레딧 시스템"은 월 구독 플랜별 분석 횟수를 할당(Starter 10회, Pro 30회)하는 방식으로 설계. 이는 고객이 "월 300~500만 원 구독"으로 반복적 분석을 수행하도록 유도하며, quote의 "구독 1000만이라도 함"은 우리의 Pro 플랜(500만 원)이 충분히 경쟁력 있음을 시사. API 명세의 "POST /api/v1/analysis/upload"에서 402 에러(insufficient_credits)로 크레딧 부족 시 플랜 업그레이드 유도.

---

### P0 기능 6: 분석 이력 조회

> "지자체마다 달라 사람 써서 확인"
— *https://cafe.naver.com/sihangsa* (Level 4, 시행사 중소팀장)

**반영 방식**: 이 quote는 **지역별 규제 차이 대응의 반복 작업**을 반영. PRD의 P0 기능 "분석 이력 조회"는 사용자가 과거 분석 결과를 필터(지역·특례법 종류)로 검색 가능하도록 설계. 화면 명세의 "분석 이력" 페이지에서 "필터 (날짜·특례법 종류)"를 제공하여, 유사 지역의 과거 분석을 재활용 가능. 이는 "사람 써서 확인" 수작업을 제거하고, 팀 내 지식 공유를 촉진.

---

### P1 기능 1: 특례법 DB 관리 대시보드 (Admin)

> "정책 바뀔 때마다 재검토. 알림 툴에 돈 내고 써도 사업성 연동 안 돼"
— *https://naver.blog.realestatePolicy* (Level 4, 건축사)

**반영 방식**: 이 quote는 **정책 변화에 따른 사업성 재평가의 지연**을 반영. PRD의 P1 기능 "특례법 DB 관리 대시보드"는 관리자가 특례법 규정을 실시간으로 추가·수정·삭제할 수 있도록 설계. API 명세의 "PUT /api/v1/admin/special-laws/:lawId"를 통해 법 개정 시 즉시 DB 업데이트 가능. 이는 "정책 바뀔 때마다 재검토" 수작업을 자동화하고, 사용자가 최신 규정 기반 분석을 받도록 보장.

---

### P1 기능 2: 분석 정확도 피드백 (사용자 검증)

> "거절 사례 많아 예측 툴 돈 주고 사겠음"
— *Reddit r/korea_realestate* (Level 5, 사업기획팀)

**반영 방식**: 이 quote는 **인허가 승인 확률 예측의 강한 수요**를 반영하며, 동시에 **모델 정확도 개선의 필요성**을 암시. PRD의 P1 기능 "분석 정확도 피드백"은 사용자가 분석 결과의 정확도를 평가(맞음/틀림/부분)하도록 설계. API 명세의 "POST /api/v1/analysis/:analysisId/feedback"에서 사용자 피드백을 수집하여, 모델 학습 데이터로 활용. 이는 "거절 사례 많아" 문제를 해결하기 위한 지속적 개선 루프를 구현.

---

### P1 기능 3: 조직 관리 (팀 초대 + 권한)

> "투자금 범위 엑셀로 매번 뽑아. 자동화되면 팀원 1명 줄일 수 있음"
— *Reddit r/korea_realestate* (Level 4, SMB 시행사)

**반영 방식**: 이 quote는 **팀 단위 협업의 필요성**과 **인건비 절감 기대**를 반영. PRD의 P1 기능 "조직 관리"는 시행사·건축사무소 내 여러 팀원이 동일 조직 계정으로 분석을 공유하도록 설계. API 명세의 "POST /api/v1/organization/invite-member"에서 팀원 초대 가능하며, 화면 명세의 "조직 관리" 페이지에서 권한(Admin/Analyst/Viewer) 설정 가능. 이는 "팀원 1명 줄일 수 있음"의 효율화를 지원하며, 조직 대시보드에서 팀 전체 크레딧 현황을 통합 관리.

---

### P1 기능 4: 분석 결과 공유 링크 (비로그인 조회)

> "개요서랑 법률서 안 맞아 재작업"
— *https://cafe.naver.com/budongsanDev* (Level 3, 개발업체 팀원)

**반영 방식**: 이 quote는 **분석 결과의 외부 공유 필요성**을 암시 (클라이언트·동료와 검증). PRD의 P1 기능 "분석 결과 공유 링크"는 분석 완료 후 클릭 1회로 공유 링크 생성 가능하도록 설계. API 명세의 "POST /api/v1/analysis/:analysisId/share"에서 만료 기간 설정 가능하며, 화면 명세의 "공유 결과 (비로그인)"에서 로그인 없이 결과 조회 가능. 이는 "개요서랑 법률서 안 맞아" 문제를 외부 검증으로 해결하고, 영업 자료로도 활용 가능.

---

### P1 기능 5: 결제 관리 (Stripe 통합)

> "특례법 자동화 툴 나오면 바로 돈 낼게"
— *https://cafe.naver.com/architectCafe* (Level 5, 건축사무소 실장)

**반영 방식**: 이 quote는 **강한 지불 의사**를 반영하며, 수익 모델의 핵심 신호. PRD의 P1 기능 "결제 관리"는 Stripe 통합으로 월 구독료 자동 청구 + 결제 실패 처리를 자동화하도록 설계. API 명세의 "POST /api/v1/subscription/change-plan"에서 플랜 변경 시 즉시 청구액 조정 가능하며, "GET /api/v1/subscription/invoices"에서 청구 이력 조회 가능. 이는 "바로 돈 낼게"의 즉시 전환을 지원하고, 수익 자동화를 실현.

---

### P2 기능 1: 승인 확률 예측 (AI 기반)

> "승인 떨어질지 모르고 샀다가 10억 날림. 예측 AI 있으면 구독 1000만이라도 함"
— *https://cafe.naver.com/sihangsa* (Level 5, 개발업체 개발기획 임원)

**반영 방식**: 이 quote는 **인허가 승인 확률 예측의 극도의 비용 효과**(10억 손실 방지)와 **높은 지불 의사**(구독 1,000만 원)를 반영. PRD의 P2 기능 "승인 확률 예측"은 특례법 판단 후 과거 인허가 사례 데이터 + AI 기반으로 승인 확률을 추정하도록 설계. 기능 목록에서 "Pain Level 5 (Workaround 2,000만/건). 고객 요청 기반 추가"로 명시하여, 초기 MVP 이후 1~2개월 내 추가 예정. 이는 quote의 "예측 AI" 요구를 구현하며, 개발업체의 투자 의사결정을 근본적으로 개선.

---

### P2 기능 2: 투자금 범위 산정 자동화

> "투자금 범위 엑셀로 매번 뽑아. 자동화되면 팀원 1명 줄일 수 있음"
— *Reddit r/korea_realestate* (Level 4, SMB 시행사)

**반영 방식**: 이 quote는 **투자금 산정의 반복 수작업**과 **인건비 절감 기대**를 반영. PRD의 P2 기능 "투자금 범위 산정 자동화"는 용적률·건폐율 입력 → 개발 가능 면적 자동 계산 → 투자금 범위 시뮬레이션을 자동화하도록 설계. 기능 목록에서 "Pain Level 4. 고객 요청 기반 추가"로 명시하여, P1 이후 추가 예정. 이는 "매번 뽑아" 수작업을 제거하고, "팀원 1명 줄일 수 있음"의 효율화를 실현.

---

### P2 기능 3: 정책 모니터링 (뉴스레터)

> "정책 바뀔 때마다 재검토. 알림 툴에 돈 내고 써도 사업성 연동 안 돼"
— *https://naver.blog.realestatePolicy* (Level 4, 건축사)

**반영 방식**: 이 quote는 **정책 변화 모니터링의 수작업 부담**과 **기존 알림 툴의 한계**(사업성 미연동)를 반영. PRD의 P2 기능 "정책 모니터링 (뉴스레터)"는 특례법 개정·정책 변화를 자동 감지하여 사용자에게 알림 + 기존 분석 결과 재평가 제안을 자동화하도록 설계. 기능 목록에서 "고객 retention 강화"로 명시하여, 고객 이탈 방지 및 장기 구독 유도. 이는 quote의 "사업성 연동" 요구를 충족하고, "정책 바뀔 때마다 재검토" 수작업을 자동화.

---

### P2 기능 4: API 제공 (B2B 파트너용)

> "빅밸류 시세 좋지만 사업성 없어 엑셀"
— *[3] 빅밸류 리뷰* (Level 4, 개발 임원)

**반영 방식**: 이 quote는 **기존 부동산 플랫폼(빅밸류)과의 통합 필요성**을 암시. PRD의 P2 기능 "API 제공"은 외부 부동산 플랫폼이 우리 분석 엔진을 호출 가능하도록 설계. 이를 통해 빅밸류 사용자가 시세 조회 후 우리 API로 특례법 판단을 즉시 받을 수 있으며, "엑셀" 수작업을 제거. 기능 목록에서 "채널 확장"으로 명시하여, 장기 성장 전략의 일부. 이는 quote의 "사업성 없어 엑셀" 문제를 근본적으로 해결하고, 파트너 생태계 구축.

---

**Evidence Appendix 종합:**
- **P0 기능 6개**: 모두 Level 4-5 pain point에 