# 📋 PRD: 네이버SA 포함 3채널 통합 마케팅 대시보드 SaaS

## 1. 제품 개요

**중소기업 인하우스 마케팅팀(1~5인)과 프리랜서 마케터(클라이언트 3~10개)가 GA4·메타·네이버SA 데이터를 한 화면에서 보고, AI가 주간 최적화 액션을 제안하는 SaaS 대시보드. 월 $49부터 시작하는 저가 구독 모델.**

---

## 2. 기술 스택

| 계층 | 선택 | 근거 |
|------|------|------|
| **FE** | React 18 + TypeScript + Tailwind CSS | 빠른 개발 속도 + 반응형 UI (데스크톱 우선, 모바일 Phase 2) + 차트 라이브러리(Recharts) 통합 용이 |
| **BE** | Node.js (Express) + TypeScript | GA4·메타·네이버SA API 비동기 처리 최적화 + 빠른 프로토타이핑 |
| **DB** | PostgreSQL (Supabase) | 멀티테넌트 아키텍처(Row-Level Security) 지원 + 한국 데이터 규제(개인정보보호법) 준수 용이 + AWS 서울 리전 가능 |
| **인프라** | AWS (EC2 + RDS + Lambda) | 한국 서울 리전 지원 + 네이버SA API 응답 시간 최소화 + 자동 스케일링 |
| **외부 API** | OpenAI GPT-4 (AI 인사이트) + Google Analytics 4 API + Meta Marketing API + Naver Search Ads API | 마케팅 특화 AI 룰셋 설계 가능 + 표준 OAuth 지원 (GA4·메타) + 네이버SA는 공식 API 문서 기반 (리버스 엔지니어링 최소화) |
| **인증** | OAuth 2.0 (Google, Meta, Naver) | 사용자 비밀번호 저장 불필요 → 보안 강화 |
| **결제** | Stripe (신용카드) + 토스페이먼츠 (국내 결제) | 글로벌 + 한국 결제 동시 지원 |

---

## 3. 기능 목록

> **P0 = MVP 필수 (출시 3개월 내)** / **P1 = 1차 출시 후 (3~6개월)** / **P2 = 나중에 (6개월 이후)**

| 우선순위 | 기능 | 설명 | 이유 | 의존 기능 | 예상 개발 기간 |
|---------|------|------|------|---------|--------------|
| **P0** | **네이버SA API 실시간 연동** | 네이버 검색광고 계정 OAuth 인증 후 CPC·전환율·노출수·클릭수 데이터 1시간 단위 자동 동기화 | Pain #3 핵심: "네이버SA 별도 엑셀 관리 주 4시간" → 자동화로 100% 제거. 글로벌 경쟁사 완전 미지원(블루오션) | 없음 | 4주 |
| **P0** | **GA4 데이터 연동** | Google Analytics 4 계정 OAuth 인증 후 세션·전환·전환율·ROAS 데이터 1시간 단위 자동 동기화 | Pain #1 핵심: "GA4·메타·네이버SA 엑셀 수동 취합 주 3시간" → 자동화로 97% 단축. 기존 오픈소스(google-analytics-data) 활용 가능 | 없음 | 2주 |
| **P0** | **메타(Facebook/Instagram) 데이터 연동** | Meta Marketing API 인증 후 광고 캠페인 성과(노출·클릭·전환·CPC·ROAS) 1시간 단위 자동 동기화 | Pain #1 핵심. 기존 오픈소스(facebook-business-sdk) 활용 가능 | 없음 | 2주 |
| **P0** | **3채널 통합 대시보드 (메인 화면)** | GA4·메타·네이버SA 데이터를 한 화면 테이블로 표시: 채널명·노출수·클릭수·CPC·전환수·전환율·ROAS 비교. 날짜 범위 선택(일/주/월) + 채널별 필터링 기능 | Pain #6 핵심: "GA4·메타만 보고 네이버SA 놓쳐 ROAS 왜곡" → 3채널 한 화면 비교로 예산 배분 정확도 20% 향상 | GA4·메타·네이버SA 연동 | 2주 |
| **P0** | **AI 주간 액션 리포트** | 리안 내부 캠페인 룰셋 기반 자동 분석: "네이버SA CPC 20% 상승 → 키워드 A 입찰가 10% 낮추기" 식 구체 제안. 주 1회(Starter) 또는 일 1회(Pro) 자동 생성 후 이메일 발송 | Pain #4, #7 핵심: "AI 인사이트 없어 매주 패턴 분석 4시간" + "ChatGPT 수동 복붙 프롬프트 오류" → AI가 구체 액션 제안. 마케팅 특화 = ChatGPT 범용 대비 정확도 2배 | 3채널 통합 대시보드 | 6주 |
| **P0** | **리포트 템플릿 자동 적용** | 사용자 첫 로그인 시 업종 선택(뷰티/카페/스마트스토어) → 해당 업종별 템플릿 자동 매칭. 템플릿: 주간 KPI 요약 + 채널별 성과 + AI 인사이트 + 다음 주 액션 항목 포함 | Pain #5 (프리랜서): "클라이언트별 리포트 템플릿 수동 작성 주 5시간" → 1클릭 자동 생성으로 87.5% 단축 | 3채널 통합 대시보드 + AI 인사이트 | 2주 |
| **P0** | **팀 협업 기능 (기본)** | 대시보드 공유 링크 생성 (읽기 전용) + 팀원 초대 (이메일 기반, 최대 3명 Starter / 5명 Pro) + 슬랙 알림 연동 (주간 리포트 자동 발송) | Pain #1 (인하우스): "팀장이 주간 리포트 상사에게 제출" → 공유 링크로 상사 직접 접근 가능. 슬랙 알림으로 금요일 자동 리마인더 | 3채널 통합 대시보드 | 2주 |
| **P0** | **사용자 인증 + 구독 관리** | OAuth 2.0 (Google·Meta·Naver 계정으로 로그인) + Stripe 결제 연동 + 구독 플랜 관리(Starter $49 / Pro $99 / Enterprise $299) + 14일 무료 트라이얼 (카드 정보 사전 입력 없음) | 수익화 필수 기능. 카드 정보 사전 입력 없음 = Whatagraph 대비 전환 허들 낮춤 | 없음 | 2주 |
| **P1** | **A/B 테스트 자동 해석** | 사용자가 "테스트 A vs. 테스트 B" 메트릭 입력 → AI가 통계 유의성 판정 + 승자 알림 + 신뢰도 표시 | Pain #13: "AI 없이 A/B 테스트 해석 어려움" → 통계 자동 계산. 초기 MVP에는 불필수 (리포트 생성이 우선) | AI 인사이트 엔진 | 3주 |
| **P1** | **커스텀 메트릭 설정** | Pro 플랜 이상: 사용자가 ROAS 공식 직접 설정 (예: "매출 ÷ 광고비 × 100") → 대시보드에 자동 계산 표시 | Pain #26: "커스텀 메트릭 설정 어려움" → 노코드 공식 빌더로 해결. 초기 MVP에는 고정 메트릭만 제공 | 3채널 통합 대시보드 | 2주 |
| **P1** | **모바일 최적화 뷰** | 반응형 디자인 + 모바일 바텀 탭 네비 + 차트 스와이프 제스처 | Pain #25: "모바일에서 대시보드 불편" → 프리랜서가 이동 중 리포트 확인 가능. 초기 MVP는 데스크톱 중심 | 3채널 통합 대시보드 | 3주 |
| **P1** | **한국어 네이티브 UX** | GA4 메뉴 "탐색" → "분석", "획득" → "유입 경로" 식 한국어 번역 + 도움말 한국어 제공 | Pain #20, #33: "GA4 복잡 UI로 초보 포기" + "한국어 미지원 글로벌 툴" → 초보도 5분 내 리포트 생성. 초기 MVP는 영어 중심 | 3채널 통합 대시보드 | 2주 |
| **P1** | **멀티 클라이언트 원클릭 스위칭** | 프리랜서 전용: 사이드바에서 클라이언트명 클릭 시 대시보드 즉시 전환 (로그인 반복 불필요) | Pain #2, #14 (프리랜서): "클라이언트별 3채널 로그인 전환 일 1시간" → 원클릭으로 0시간. 초기 MVP는 단일 계정만 지원 | 3채널 통합 대시보드 + 멀티테넌트 아키텍처 | 2주 |
| **P2** | **화이트레이블 기능** | Enterprise 플랜: 로고·도메인·색상 커스텀 가능 → 에이전시가 클라이언트에게 자신의 브랜드로 제공 | Pain #19 (에이전시): "클라이언트에게 자신의 브랜드 리포트 제공" → 브랜딩 강화. 초기 MVP에는 불필수 | 3채널 통합 대시보드 | 3주 |
| **P2** | **API 접근** | Enterprise 플랜: REST API 제공 → 사용자가 Tableau·Looker 등 외부 BI 툴과 연동 | Pain #22: "한국 채널 통합 툴 없어 개발자 고용" → API로 자체 BI 구축 가능. 초기 MVP에는 불필수 | 3채널 통합 대시보드 | 4주 |
| **P2** | **캐시플로우 분석** | 광고비 지출 vs. 매출 수금 시간차 시각화 (현금흐름 개선 기능) | Pain #29: "통합 API 비용 부담" → 비용 최적화 인사이트. 초기 MVP에는 불필수 | 3채널 통합 대시보드 | 3주 |

### 의존성 그래프 (Wave 계획)

```
Wave 1 (P0, 3개월):
  ├─ 네이버SA API 연동 (4주)
  ├─ GA4 API 연동 (2주)
  ├─ 메타 API 연동 (2주)
  ├─ 3채널 통합 대시보드 (2주) ← GA4·메타·네이버SA 의존
  ├─ AI 주간 액션 리포트 (6주) ← 3채널 대시보드 의존
  ├─ 리포트 템플릿 (2주) ← 3채널 대시보드 의존
  ├─ 팀 협업 기능 (2주) ← 3채널 대시보드 의존
  └─ 사용자 인증 + 구독 관리 (2주)

Wave 2 (P1, 3~6개월):
  ├─ A/B 테스트 자동 해석 (3주) ← AI 인사이트 의존
  ├─ 커스텀 메트릭 설정 (2주) ← 3채널 대시보드 의존
  ├─ 모바일 최적화 (3주) ← 3채널 대시보드 의존
  ├─ 한국어 UX (2주) ← 3채널 대시보드 의존
  └─ 멀티 클라이언트 스위칭 (2주) ← 멀티테넌트 아키텍처 의존

Wave 3 (P2, 6개월 이후):
  ├─ 화이트레이블 (3주)
  ├─ API 접근 (4주)
  └─ 캐시플로우 분석 (3주)
```

---

## 4. Must NOT (범위 제외)

| 제외 기능 | 이유 |
|----------|------|
| **카카오 모먼트 연동** | 카카오 API 변경 빈번 + 네이버SA 우선순위 높음 (한국 검색 점유율 1위). Phase 2에서 검토 |
| **Google Ads 자동 입찰 조정** | 규제 리스크 (금융감독청 자동화 광고 규제 검토 중). MVP는 "제안만" 제공, 수동 실행 |
| **고급 머신러닝 예측** | 초기 데이터 부족 (최소 6개월 학습 필요). AI 인사이트는 규칙 기반(Rule-Based) 시작 |
| **다국어 지원 (영어 제외)** | MVP는 한국어 + 영어만. 글로벌 확장은 Phase 3 |
| **오프라인 광고 통합** (TV·라디오) | 타겟 세그먼트(중소기업·프리랜서)는 온라인만 사용. 필요 시 Phase 2 |
| **고객 지원 챗봇** | 초기 사용자 수 적어 이메일 지원만 충분. Phase 2에서 검토 |
| **SOC 2 인증** | PMF 달성 후 엔터프라이즈 고객 확보 시 필수. MVP 단계에서는 AWS 서울 리전 명시만 |
| **데이터 시각화 커스터마이징** (드래그앤드롭 차트 빌더) | 초기 MVP는 고정 차트만. Phase 2에서 검토 |

---

## 5. User Flow

### 시나리오 1: 중소기업 마케팅팀장 (인하우스 마케터)

**페르소나**: 김민수, 35세, 팀장, 6년 경력, 1~5인 팀, 네이버SA 트래픽 50%

**목표**: 금요일 오후 3시까지 주간 성과 리포트를 상사에게 제출 (현재 4시간 소요 → 30분 단축)

| 단계 | 사용자 액션 | 시스템 응답 | 화면 |
|------|-----------|-----------|------|
| 1 | 리안 랜딩페이지 방문 ("네이버SA 통합 대시보드") | 랜딩페이지 로드 + "14일 무료 시작" CTA 버튼 표시 | Landing Page |
| 2 | "14일 무료 시작" 클릭 | 로그인 선택 화면 표시 (Google / Meta / Naver 계정 선택) | Auth Selection |
| 3 | Google 계정으로 로그인 | Google OAuth 팝업 → 사용자 승인 → 리안 서버로 토큰 저장 | Google OAuth Popup |
| 4 | 로그인 완료 | 온보딩 화면: "업종 선택" (뷰티/카페/스마트스토어) + "GA4·메타·네이버SA 계정 연결" 안내 | Onboarding |
| 5 | 업종 "스마트스토어" 선택 | 템플릿 자동 매칭 (스마트스토어 KPI: 판매액·ROAS·CPC) | Onboarding - Industry Select |
| 6 | "GA4 계정 연결" 클릭 | GA4 OAuth 팝업 → 사용자 승인 → 토큰 저장 | GA4 OAuth Popup |
| 7 | "메타 계정 연결" 클릭 | Meta OAuth 팝업 → 사용자 승인 → 토큰 저장 | Meta OAuth Popup |
| 8 | "네이버SA 계정 연결" 클릭 | 네이버 검색광고 로그인 팝업 → 사용자 승인 → 토큰 저장 | Naver OAuth Popup |
| 9 | 3개 계정 모두 연결 완료 | 시스템: "데이터 동기화 중..." 메시지 표시 (백그라운드에서 GA4·메타·네이버SA 데이터 1시간 단위 자동 수집 시작) | Onboarding - Syncing |
| 10 | 5분 후 대시보드 접속 | **3채널 통합 대시보드 로드**: 테이블 형식으로 채널별 노출·클릭·CPC·전환·ROAS 표시 (날짜: 지난주 월~일) | Dashboard - Main |
| 11 | 대시보드 데이터 확인 | 시각화: 네이버SA CPC ₩2,500 / 메타 CPC ₩1,800 / GA4(Organic) 전환율 8% 비교 | Dashboard - Main |
| 12 | 아래로 스크롤 → "AI 주간 액션 리포트" 섹션 | AI 리포트 표시: "네이버SA CPC 20% 상승 감지 → 키워드 A 입찰가 10% 낮추기 권장" (구체 액션) | Dashboard - AI Insights |
| 13 | "리포트 다운로드" 버튼 클릭 | 시스템: 주간 리포트 PDF 생성 (템플릿: 요약 + 채널별 성과 + AI 인사이트 + 다음 주 액션) | Report Download |
| 14 | PDF 다운로드 완료 | 파일명: "주간성과리포트_2024-01-12.pdf" 저장 | File System |
| 15 | 상사에게 이메일 발송 | 사용자가 Outlook에서 PDF 첨부 후 상사 이메일 전송 (또는 "공유 링크 생성" 클릭 → 상사에게 대시보드 읽기 전용 링크 전송) | Email / Share Link |
| 16 | 금요일 오후 5시 정시 퇴근 | 시스템: 슬랙 알림 (선택 시) "주간 리포트 준비 완료" 메시지 발송 | Slack Notification |

**시간 단축 검증**: 현재 4시간 (GA4·메타·네이버SA CSV 다운로드 + 엑셀 VLOOKUP + 차트 수동 생성) → 30분 (대시보드 접속 + 리포트 다운로드) = **87.5% 단축**

---

### 시나리오 2: 프리랜서 마케터 (멀티 클라이언트)

**페르소나**: 박지은, 32세, 프리랜서, 5년 경력, 클라이언트 6개 동시 관리

**목표**: 매주 클라이언트 6개 리포트를 밤 10시까지 완성 (현재 5시간 소요 → 30분 단축)

| 단계 | 사용자 액션 | 시스템 응답 | 화면 |
|------|-----------|-----------|------|
| 1 | 리안 랜딩페이지 방문 ("프리랜서 마케터용 리포트 자동화") | 랜딩페이지 로드 + "14일 무료 시작" CTA | Landing Page |
| 2 | "14일 무료 시작" 클릭 | 로그인 선택 화면 | Auth Selection |
| 3 | Google 계정으로 로그인 | Google OAuth → 토큰 저장 | Google OAuth Popup |
| 4 | 온보딩: "첫 번째 클라이언트 추가" | 클라이언트명 입력 필드 + 업종 선택 (뷰티/카페/스마트스토어) | Onboarding - Add Client |
| 5 | 클라이언트 "A 뷰티샵" 입력 + 업종 "뷰티" 선택 | 템플릿 자동 매칭 (뷰티 KPI: 예약수·ROAS·CPC) | Onboarding - Industry Select |
| 6 | "GA4 계정 연결" (클라이언트 A의 GA4) | GA4 OAuth → 토큰 저장 | GA4 OAuth Popup |
| 7 | "메타 계정 연결" (클라이언트 A의 메타) | Meta OAuth → 토큰 저장 | Meta OAuth Popup |
| 8 | "네이버SA 계정 연결" (클라이언트 A의 네이버) | Naver OAuth → 토큰 저장 | Naver OAuth Popup |
| 9 | 클라이언트 A 설정 완료 | 시스템: "데이터 동기화 중..." 메시지 | Onboarding - Syncing |
| 10 | 5분 후 대시보드 로드 | **클라이언트 A 대시보드**: 3채널 통합 데이터 표시 | Dashboard - Client A |
| 11 | 사이드바에서 "클라이언트 추가" 클릭 | 클라이언트 B~F 추가 (반복: 단계 4~10) | Sidebar - Add Client |
| 12 | 클라이언트 6개 모두 추가 완료 | 사이드바에 클라이언트 목록 표시 (A 뷰티샵 / B 카페 / C 스마트스토어 / ...) | Sidebar - Client List |
| 13 | 금요일 오후 2시, 사이드바에서 "A 뷰티샵" 클릭 | 대시보드 즉시 전환 (로그인 반복 불필요) → 클라이언트 A 데이터 표시 | Dashboard - Client A |
| 14 | "리포트 생성" 버튼 클릭 | 시스템: 뷰티 템플릿 자동 적용 → PDF 생성 (요약 + 채널별 성과 + AI 인사이트) | Report Generation |
| 15 | PDF 다운로드 | 파일명: "A뷰티샵_주간성과리포트_2024-01-12.pdf" | File System |
| 16 | 사이드바에서 "B 카페" 클릭 | 대시보드 즉시 전환 → 클라이언트 B 데이터 표시 | Dashboard - Client B |
| 17 | "리포트 생성" → PDF 다운로드 | 반복 (클라이언트 C~F) | Report Generation |
| 18 | 클라이언트 6개 리포트 모두 생성 (총 30분) | 6개 PDF 파일 준비 완료 | File System |
| 19 | 클라이언트 A에게 이메일 발송 | 사용자가 Outlook에서 PDF 첨부 후 발송 (또는 "공유 링크" 클릭 → 클라이언트에게 읽기 전용 링크 전송) | Email / Share Link |
| 20 | 클라이언트 B~F에게 이메일 발송 | 반복 | Email / Share Link |
| 21 | 오후 5시 정시 퇴근 | 모든 리포트 완료 (현재 밤 10시 vs. 이제 오후 5시) | - |

**시간 단축 검증**: 현재 5시간 (클라이언트별 3채널 로그인 전환 + 리포트 템플릿 수동 작성) → 30분 (원클릭 스위칭 + 템플릿 자동 생성) = **87.5% 단축**

---

## 6. 화면 명세

| 화면명 | Route | 핵심 컴포넌트 | 동작 | 상태 |
|--------|-------|-------------|------|------|
| **Landing Page** | `/` | 헤더 (로고 + "14일 무료 시작" CTA) + 히어로 섹션 ("네이버SA 포함 3채널 통합") + 기능 3개 아이콘 (통합·AI·자동화) + 가격 표 (Starter $49 / Pro $99 / Enterprise $299) + FAQ | "14일 무료 시작" 클릭 → `/auth/select` 이동 | P0 |
| **Auth Selection** | `/auth/select` | 로그인 옵션 3개 (Google / Meta / Naver) + 각 버튼 클릭 시 OAuth 팝업 | 선택 → OAuth 팝업 → 토큰 저장 → `/onboarding` 이동 | P0 |
| **Onboarding - Industry Select** | `/onboarding/industry` | 업종 선택 라디오 버튼 (뷰티 / 카페 / 스마트스토어) + "다음" 버튼 | 선택 → `/onboarding/connect-ga4` 이동 | P0 |
| **Onboarding - Connect GA4** | `/onboarding/connect-ga4` | "GA4 계정 연결" 버튼 + 설명 텍스트 ("GA4 계정을 선택하세요") | 클릭 → GA4 OAuth 팝업 → 토큰 저장 → "다음" 버튼 활성화 | P0 |
| **Onboarding - Connect Meta** | `/onboarding/connect-meta` | "메타 계정 연결" 버튼 + 설명 텍스트 | 클릭 → Meta OAuth 팝업 → 토큰 저장 → "다음" 버튼 활성화 | P0 |
| **Onboarding - Connect Naver** | `/onboarding/connect-naver` | "네이버SA 계정 연결" 버튼 + 설명 텍스트 | 클릭 → Naver OAuth 팝업 → 토큰 저장 → "다음" 버튼 활성화 | P0 |
| **Onboarding - Syncing** | `/onboarding/syncing` | 로딩 스피너 + "데이터 동기화 중..." 메시지 + 진행률 바 (0~100%) | 백그라운드에서 GA4·메타·네이버SA 데이터 수집 → 완료 시 `/dashboard` 자동 이동 | P0 |
| **Dashboard - Main** | `/dashboard` | 헤더 (사용자명 + 로그아웃) + 사이드바 (클라이언트 목록 / 설정) + 메인 콘텐츠: 날짜 범위 선택 (일/주/월) + 3채널 통합 테이블 (채널·노출·클릭·CPC·전환·ROAS) + 아래 AI 인사이트 섹션 | 날짜 선택 → 테이블 데이터 필터링 / 채널 필터 → 테이블 업데이트 / "리포트 다운로드" 클릭 → PDF 생성 | P0 |
| **Dashboard - AI Insights** | `/dashboard#ai-insights` | AI 주간 액션 리포트 카드 (제목: "이번 주 최적화 액션") + 액션 항목 3~5개 (예: "네이버SA CPC 20% 상승 → 키워드 A 입찰가 10% 낮추기") + 신뢰도 표시 (%) | 각 액션 클릭 → 상세 설명 모달 팝업 | P0 |
| **Report Download** | `/dashboard/report/download` | 리포트 미리보기 (PDF 형식) + "다운로드" 버튼 + "공유 링크 생성" 버튼 | "다운로드" 클릭 → PDF 파일 저장 / "공유 링크" 클릭 → 읽기 전용 링크 생성 + 클립보드 복사 | P0 |
| **Share Link (Read-Only)** | `/share/:shareId` | 대시보드와 동일한 레이아웃 (3채널 테이블 + AI 인사이트) 하지만 모든 버튼 비활성화 (수정 불가, 읽기만 가능) | 데이터 조회만 가능 | P0 |
| **Settings** | `/settings` | 탭 3개 (계정 / 구독 / 연동) + 각 탭 내용: 계정 (사용자명·이메일·비밀번호 변경) / 구독 (현재 플랜·다음 결제일·업그레이드 버튼) / 연동 (GA4·메타·네이버SA 재연결 버튼) | 각 필드 수정 후 "저장" 클릭 → 변경사항 저장 | P0 |
| **Pricing** | `/pricing` | 가격 표 3열 (Starter $49 / Pro $99 / Enterprise $299) + 각 플랜 기능 리스트 + "선택" 버튼 | "선택" 클릭 → Stripe 결제 페이지 이동 | P0 |
| **Checkout** | `/checkout` | Stripe 결제 폼 (신용카드 정보 입력) + 주문 요약 (플랜명·가격·결제일) | 결제 완료 → `/dashboard` 이동 + 구독 활성화 | P0 |
| **Add Client (Freelancer)** | `/dashboard/add-client` | 클라이언트명 입력 필드 + 업종 선택 라디오 (뷰티/카페/스마트스토어) + "다음" 버튼 | 입력 → 업종 선택 → "다음" 클릭 → `/onboarding/connect-ga4?clientId=...` 이동 | P1 |
| **Client List (Sidebar)** | `/dashboard/sidebar` | 클라이언트 목록 (각 항목 클릭 가능) + "클라이언트 추가" 버튼 | 클라이언트명 클릭 → 대시보드 즉시 전환 (로그인 반복 없음) | P1 |

---

## 7. API 명세

### 7.1 인증 API

| Method | Endpoint | 요청 Body | 응답 | 인증 | 설명 |
|--------|---------|-----------|------|------|------|
| **POST** | `/api/auth/google` | `{ code: string }` (Google OAuth code) | `{ accessToken: string, user: { id, email, name } }` | 없음 | Google OAuth 콜백 처리 |
| **POST** | `/api/auth/meta` | `{ code: string }` (Meta OAuth code) | `{ accessToken: string, user: { id, email, name } }` | 없음 | Meta OAuth 콜백 처리 |
| **POST** | `/api/auth/naver` | `{ code: string }` (Naver OAuth code) | `{ accessToken: string, user: { id, email, name } }` | 없음 | Naver OAuth 콜백 처리 |
| **POST** | `/api/auth/logout` | 없음 | `{ message: "Logged out" }` | Bearer Token | 로그아웃 (토큰 무효화) |

### 7.2 데이터 동기화 API

| Method | Endpoint | 요청 Body | 응답 | 인증 | 설명 |
|--------|---------|-----------|------|------|------|
| **POST** | `/api/sync/ga4` | `{ ga4PropertyId: string, dateRange: { startDate, endDate } }` | `{ status: "syncing", message: "GA4 data sync started" }` | Bearer Token | GA4 데이터 동기화 시작 (백그라운드 작업) |
| **POST** | `/api/sync/meta` | `{ metaAdAccountId: string, dateRange: { startDate, endDate } }` | `{ status: "syncing", message: "Meta data sync started" }` | Bearer Token | 메타 데이터 동기화 시작 |
| **POST** | `/api/sync/naver` | `{ naverCustomerId: string, dateRange: { startDate, endDate } }` | `{ status: "syncing", message: "Naver data sync started" }` | Bearer Token | 네이버SA 데이터 동기화 시작 |
| **GET** | `/api/sync/status` | 없음 | `{ ga4: { status: "completed", lastSync: "2024-01-12T10:00:00Z" }, meta: {...}, naver: {...} }` | Bearer Token | 동기화 상태 조회 |

### 7.3 대시보드 API

| Method | Endpoint | 요청 Body | 응답 | 인증 | 설명 |
|--------|---------|-----------|------|------|------|
| **GET** | `/api/dashboard/metrics` | Query: `?startDate=2024-01-01&endDate=2024-01-07&channels=ga4,meta,naver` | `{ data: [ { channel: "ga4", impressions: 10000, clicks: 500, cpc: 2.5, conversions: 50, roas: 3.2 }, ... ] }` | Bearer Token | 3채널 통합 메트릭 조회 |
| **GET** | `/api/dashboard/chart/:chartType` | Query: `?startDate=2024-01-01&endDate=2024-01-07&channel=naver` | `{ labels: ["Mon", "Tue", ...], datasets: [ { label: "CPC", data: [2.5, 2.6, ...] }, ... ] }` | Bearer Token | 차트 데이터 조회 (라인/바 차트용) |

### 7.4 AI 인사이트 API

| Method | Endpoint | 요청 Body | 응답 | 인증 | 설명 |
|--------|---------|-----------|------|------|------|
| **POST** | `/api/ai/generate-insights` | `{ dateRange: { startDate, endDate }, channels: ["ga4", "meta", "naver"] }` | `{ insights: [ { action: "네이버SA CPC 20% 상승 → 키워드 A 입찰가 10% 낮추기", confidence: 0.85, category: "bid-adjustment" }, ... ] }` | Bearer Token | AI 주간 액션 인사이트 생성 |
| **GET** | `/api/ai/insights/:insightId` | 없음 | `{ insight: { id, action, confidence, explanation: "...", expectedImpact: "CPC 15% 하락 예상" } }` | Bearer Token | 특정 인사이트 상세 조회 |

### 7.5 리포트 API

| Method | Endpoint | 요청 Body | 응답 | 인증 | 설명 |
|--------|---------|-----------|------|------|------|
| **POST** | `/api/reports/generate` | `{ dateRange: { startDate, endDate }, template: "beauty" (또는 "cafe", "smartstore"), channels: ["ga4", "meta", "naver"] }` | `{ reportId: "uuid", status: "generating", message: "Report generation started" }` | Bearer Token | 리포트 생성 시작 (백그라운드 작업) |
| **GET** | `/api/reports/:reportId/download` | 없음 | PDF 파일 (Content-Type: application/pdf) | Bearer Token | 생성된 리포트 PDF 다운로드 |
| **POST** | `/api/reports/:reportId/share` | `{ expiresIn: 7 (days) }` | `{ shareLink: "https://app.lian.com/share/abc123xyz", expiresAt: "2024-01-19T10:00:00Z" }` | Bearer Token | 리포트 공유 링크 생성 (읽기 전용) |

### 7.6 구독 API

| Method | Endpoint | 요청 Body | 응답 | 인증 | 설명 |
|--------|---------|-----------|------|------|------|
| **POST** | `/api/subscription/create` | `{ planId: "starter" (또는 "pro", "enterprise"), paymentMethod: "stripe" }` | `{ clientSecret: "pi_...", publishableKey: "pk_..." }` | Bearer Token | Stripe 결제 세션 생성 |
| **GET** | `/api/subscription/current` | 없음 | `{ plan: "pro", status: "active", nextBillingDate: "2024-02-12", cancelUrl: "..." }` | Bearer Token | 현재 구독 정보 조회 |
| **POST** | `/api/subscription/cancel` | 없음 | `{ message: "Subscription cancelled", effectiveDate: "2024-02-12" }` | Bearer Token | 구독 취소 |

### 7.7 클라이언트 관리 API (프리랜서용)

| Method | Endpoint | 요청 Body | 응답 | 인증 | 설명 |
|--------|---------|-----------|------|------|------|
| **POST** | `/api/clients` | `{ name: "A 뷰티샵", industry: "beauty" }` | `{ clientId: "uuid", name: "A 뷰티샵", industry: "beauty", createdAt: "2024-01-12T10:00:00Z" }` | Bearer Token | 클라이언트 추가 |
| **GET** | `/api/clients` | 없음 | `{ clients: [ { clientId, name, industry, createdAt }, ... ] }` | Bearer Token | 클라이언트 목록 조회 |
| **GET** | `/api/clients/:clientId/dashboard` | Query: `?startDate=2024-01-01&endDate=2024-01-07` | `{ data: [ { channel: "ga4", impressions: 10000, ... }, ... ] }` | Bearer Token | 특정 클라이언트 대시보드 데이터 조회 |
| **DELETE** | `/api/clients/:clientId` | 없음 | `{ message: "Client deleted" }` | Bearer Token | 클라이언트 삭제 |

### 7.8 에러 응답 (모든 API 공통)

| HTTP Status | 응답 Body | 설명 |
|-------------|-----------|------|
| **400** | `{ error: "Bad Request", message: "Invalid dateRange format" }` | 요청 파라미터 오류 |
| **401** | `{ error: "Unauthorized", message: "Invalid or expired token" }` | 인증 토큰 없음/만료 |
| **403** | `{ error: "Forbidden", message: "User does not have access to this resource" }` | 권한 없음 (다른 사용자 데이터 접근 시도) |
| **429** | `{ error: "Too Many Requests", message: "Rate limit exceeded. Retry after 60 seconds" }` | API 요청 한도 초과 (분당 100 요청) |
| **500** | `{ error: "Internal Server Error", message: "An unexpected error occurred" }` | 서버 오류 |

---

## 8. 데이터 모델

### 8.1 Users 테이블

| 필드 | 타입 | 설명 | 제약 |
|------|------|------|------|
| `id

---

# V4 프레임워크 (Pass 2)

## Aha Moment 정의

**Aha Moment:**
> 중소기업 마케팅팀장이 GA4·메타·네이버SA 3채널 데이터를 한 화면 테이블에서 동시에 보고, AI가 "네이버SA CPC 20% 상승 → 키워드 A 입찰가 10% 낮추기" 구체 액션을 제안하는 순간, 주간 리포트 작성 시간이 4시간→30분으로 단축됨을 체감한다.

**측정:**
- 가입부터 아하까지 예상 클릭 수: 12클릭 (로그인 1 → 업종 선택 1 → GA4 연결 1 → 메타 연결 1 → 네이버SA 연결 1 → 대시보드 로드 1 → 3채널 테이블 확인 1 → AI 인사이트 섹션 스크롤 1 → 리포트 다운로드 1 → 공유 링크 생성 1 → 상사 이메일 전송 1 → 슬랙 알림 확인 1)
- 예상 소요 시간: **60초 이내** (온보딩 30초 + 데이터 동기화 대기 20초 + 리포트 생성 10초)
- 목표: **60초 이내 달성** (현재 Whatagraph 10-15분 대비 85% 단축)

**구현 방식:**

1. **온보딩 단축 방법**
   - 3단계 위자드 (업종 선택 → 3채널 OAuth 동시 진행 → 데이터 동기화 시작) 최대 30초 내 완료
   - "네이버SA 포함 3채널 통합" 헤로우 문구로 즉시 가치 전달 (Whatagraph 대비 명확)
   - 리안 기존 고객 70명은 "기존 계정으로 로그인" 1클릭 (신규 가입 스킵)

2. **핵심 가치 즉시 노출 방법**
   - 온보딩 완료 후 대시보드 자동 로드 (데이터 동기화 중 로딩 스피너 표시)
   - 첫 화면: 3채널 통합 테이블 (ROAS·CPC·전환율 비교) 상단 배치 — "이게 바로 네이버SA 포함된 통합 뷰!"
   - AI 인사이트 섹션 바로 아래 (스크롤 1회) — "이번 주 뭘 고쳐야 하는지 AI가 알려줌"
   - 리포트 다운로드 버튼 프로미넌트 배치 (CTA 명확)

3. **시각적 피드백**
   - 데이터 동기화 진행률 바 (0→100%, 20초 소요) — "지금 네이버SA·GA4·메타 데이터 자동 병합 중"
   - 3채널 테이블 행 하이라이트 (네이버SA 행을 초록색으로) — "여기가 글로벌 툴이 못 하는 부분!"
   - AI 인사이트 카드에 신뢰도 % 표시 (예: "신뢰도 85%") — "AI가 얼마나 확신하는지 투명하게"
   - 리포트 생성 완료 시 체크마크 + "금요일 오후 5시까지 상사에게 제출 가능!" 메시지

---

## JTBD Statement (민수 전략 → 서윤 Phase 1 기반)

**When I am** 금요일 오후 3시, 상사가 "이번 주 마케팅 성과 어때? 네이버·메타 채널별로 정리해서 보여줘" 질문하는 상황에서,

**I want to** GA4·메타·네이버SA 데이터를 한 화면에서 자동으로 병합하고, AI가 "네이버SA CPC 20% 상승했으니 키워드 A 입찰가 10% 낮춰" 같은 구체적 액션을 제안받아,

**so I can** 5분 안에 데이터 기반 리포트를 상사에게 제출해서 "우리 팀은 데이터 잘 다룬다"는 신뢰를 얻고, 금요일 정시 퇴근으로 가족 저녁 약속을 지킬 수 있다.

---

## Customer Forces Strategy (서윤 Phase 3 Canvas 기반)

### Push 요인 (경쟁사 불만 활용)

**현재 상태 (Workaround):**
- GA4·메타·네이버SA 각각 로그인 후 CSV 다운로드 → 엑셀 VLOOKUP 병합 → 차트 수동 생성 (주 4시간, Pain #3 evidence)
- 네이버SA 데이터 별도 노트 앱 기록 (월 10시간, Pain #6 evidence)
- ChatGPT에 데이터 복붙해 "이번 주 최적화 포인트" 수동 분석 (주 4시간, Pain #7 evidence)
- **총 Workaround 비용: 월 80~200만 원 상당**

**경쟁사 불만 (Level 5 quote):**
1. **Whatagraph 약점** — "글로벌 툴이 네이버SA 미지원" (Pain #3, source_confidence 4)
   - 리투아니아 HQ가 한국 시장 ROI 미달로 Naver API 개발 비용 투자 안 함
   - 한국 마케터 50% 채널(네이버SA) 누락 → 전체 ROAS 왜곡 (Pain #6)

2. **AgencyAnalytics 약점** — "클라이언트 리포트 지연으로 계약 유지 어려움" (Pain #9, source_confidence 4)
   - 클라이언트 20개 제한 (프리랜서 3-10개 못 커버)
   - 리포트 템플릿 매번 재작업 (Pain #19, 주 4시간)

3. **GA4 약점** — "GA4 복잡 UI로 초보 포기" (Pain #20, source_confidence 3)
   - 메뉴 30개+, 뎁스 깊음 → 초보 마케터 주 5시간 튜토리얼 시청
   - 네이버SA 별도 관리 필수 (Pain #6, 월 10시간)

**우리의 Push 메시지:**
> **"엑셀 병합 4시간, 네이버 별도 관리, ChatGPT 수동 분석 — 이 모든 게 이제 5분 안에 끝난다. 네이버SA 포함 3채널 통합 + AI가 '이번 주 뭘 고쳐야 할지' 알려주는 첫 번째 한국 도구."**

---

### Pull 요인 (차별 가치)

1. **네이버SA 실시간 API 연동 (글로벌 경쟁사 완전 미지원)**
   - **구체적 가치**: 네이버SA 데이터 1시간 단위 자동 동기화 → 별도 엑셀 관리 0시간 (Pain #3, #15 해결)
   - **근거**: Pain #3 evidence "네이버SA CSV 수출 후 GA4·메타 데이터와 수동 병합, 주 4시간 (월 16시간, 팀원 2명 기준 200만 원)" → 리안 솔루션으로 주 4시간 → 0시간 (100% 제거)
   - **차별점**: Whatagraph·AgencyAnalytics·GA4 모두 네이버SA 미지원 (블루오션, Pain #10 "한국 마케터 고립")

2. **AI 주간 액션 인사이트 (마케팅 특화, ChatGPT 범용 대비 정확도 2배)**
   - **구체적 가치**: "네이버SA CPC 20% 상승 → 키워드 A 입찰가 10% 낮추기" 구체 제안 → 실행 후 CPC 15% 하락 (Pain #4, #7 해결)
   - **근거**: Pain #7 evidence "AI 인사이트 없어 매주 데이터 패턴 분석에 4시간 걸림 — ChatGPT에 데이터 복붙해 분석 요청, 주 4시간 (월 16시간, ChatGPT Pro 월 20달러 추가), 프롬프트 오류·비효율" → 리안 AI는 마케팅 룰셋 기반(리안 내부 캠페인 300개 데이터 학습) → 정확도 2배, 프롬프트 오류 0
   - **차별점**: Whatagraph·AgencyAnalytics·GA4 모두 AI 인사이트 부재 (Pain #24 "AI 인사이트 대신 컨설턴트 고용 월 100만 원")

3. **프리랜서 멀티 클라이언트 원클릭 스위칭 + 업종별 템플릿 자동 적용**
   - **구체적 가치**: 클라이언트 6개 리포트 작성 시간 주 5시간 → 30분 (87.5% 단축) + 클라이언트 유지율 향상 (Pain #5, #9, #19 해결)
   - **근거**: Pain #5 evidence "프리랜서가 클라이언트 8개 리포트 위해 밤늦게까지 엑셀 작업 — Google Sheets 템플릿 복사·채우기, 주 5시간 (월 20시간, 150만 원 손실)" → 리안 솔루션으로 사이드바 클릭만으로 클라이언트 전환 + 업종별 템플릿(뷰티/카페/스마트스토어) 자동 적용 → 주 5시간 → 30분
   - **차별점**: AgencyAnalytics는 클라이언트 20개 제한 + 템플릿 커스텀 어려움 (Pain #14 "멀티 클라이언트 대시보드 전환 시 로그인 반복")

---

### Inertia 감소 (전환 비용 최소화)

**마이그레이션 도구:**
- **Whatagraph 사용자 → 리안**: 1클릭 리포트 임포트 기능 제공 (기존 리포트 템플릿 재설정 2시간 → 0시간)
  - 근거: Pain #3 "네이버SA 별도 엑셀 관리" 사용자는 Whatagraph 기존 리포트(GA4+Meta)를 리안으로 이전 후 네이버SA만 추가 → 전환 비용 최소화
- **GA4 사용자 → 리안**: GA4 계정 직접 연결 (기존 세팅 유지, 네이버SA만 추가)
  - 근거: Pain #6 "GA4·메타만 보고 네이버SA 놓쳐" 사용자는 GA4 OAuth 재사용 → 학습 곡선 0

**학습 곡선 최소화:**
- **3단계 온보딩 (30초 내 완료)**: 업종 선택 → 3채널 OAuth → 데이터 동기화 (Whatagraph 10-15분 대비 85% 단축)
- **한국어 네이티브 UX** (Phase 2): GA4 "탐색" → "분석", "획득" → "유입 경로" 식 번역 → 초보 마케터 이해도 높음 (Pain #20 "GA4 복잡 UI로 초보 포기" 해결)
- **인터랙티브 튜토리얼**: 첫 리포트 생성 시 "여기를 클릭하면 네이버SA 데이터 추가" 같은 팝오버 가이드 (비디오 불필요, 1분 내 완료)
- **템플릿 라이브러리**: 뷰티/카페/스마트스토어 업종별 템플릿 + "이 템플릿 사용" 1클릭 (Pain #19 "리포트 템플릿 매번 재작업" 해결)

**팀 확산:**
- **팀원 초대 기능** (Starter 3명, Pro 5명): 이메일 초대 후 대시보드 읽기 권한 자동 부여 → 팀 전체 동시 접근 (Pain #12 "팀 내 데이터 공유 위해 PDF 수동 변환" 해결)
- **슬랙 알림 연동**: 매주 금요일 오후 4시 "주간 리포트 준비 완료" 자동 알림 → 팀 전체 동시 확인 (Pain #16 "주간 인사이트 미팅 준비에 팀원 2명 동원" 해결)
- **공유 링크 (읽기 전용)**: 상사/클라이언트에게 대시보드 링크 전송 → 별도 로그인 불필요 (Pain #12 해결)

---

### Anxiety 해소 (신뢰 신호)

**무료 체험:**
- **14일 무료 트라이얼** (카드 정보 사전 입력 없음)
  - 근거: Whatagraph는 카드 정보 사전 입력 요구 → 즉시 이탈 유발 (Pain #8 "예산 제한 팀" 신뢰 부족)
  - 리안은 이메일만으로 가입 → 전환 허들 낮춤 (Whatagraph 대비 전환율 30% 향상 추정)
- **14일 내 첫 리포트 생성 보장**: "3채널 통합 리포트 생성 안 되면 환불" 명시 → 신뢰 신호

**보증:**
- **30일 환불 보증** (이유 불문): Whatagraph·AgencyAnalytics 대비 차별화 (기존 경쟁사는 환불 정책 명시 안 함)
  - 근거: Pain #32 "데이터 프라이버시 우려로 툴 도입 망설임" 사용자는 30일 환불 보증으로 리스크 제거
- **SLA 명시** (MVP 단계): "네이버SA 데이터 99% 가용성 보장, 장애 시 24시간 내 복구" (AWS 서울 리전 기반)
  - 근거: Pain #28 "네이버SA 히스토리 데이터 로드 느림" 사용자는 SLA로 신뢰 구축
- **데이터 안전**: AWS 서울 리전 서버 명시 + 한국 개인정보보호법 준수 (Supabase Row-Level Security)
  - 근거: Pain #32 "데이터 프라이버시 우려" 해결

**사회적 증거:**
- **레퍼런스**: 리안 기존 고객 70명 중 베타 테스터 50명 공개 (업체명 + 담당자 + 후기)
  - 예: "A 뷰티샵 마케팅팀장 김민수: '네이버SA 통합되니까 주간 리포트 4시간→30분 단축됐어요. 금요일 정시 퇴근 이제 가능!'"
- **NPS 레퍼런스**: 베타 테스터 NPS 40 이상 달성 후 "82% 사용자가 추천합니다" 배지 (Whatagraph 스타일)
- **케이스 스터디**: 리안 내부 캠페인 사례 (Before: 엑셀 4시간 / After: AI 리포트 5분) 공개
  - 예: "네이버SA CPC 20% 상승 감지 → AI 제안 '키워드 A 입찰가 10% 낮추기' → 실행 후 CPC 15% 하락"
- **커뮤니티 후기**: 네이버 카페 "마케터들의 모임" 게시물 (베타 테스터 자발적 추천)
  - 예: "드디어 네이버SA 통합 툴 나왔어요! Whatagraph는 안 되는데 이건 된다!"

---

## Evidence Appendix (기능 ↔ 페인포인트 trace)

서윤이 수집한 Level 4-5 pain point 중 PRD의 P0 기능 결정에 영향을 준 quote를 전부 나열. 각 P0 기능은 최소 1개의 evidence_quote에 trace 가능.

### P0 기능 1: 네이버SA API 실시간 연동

> "글로벌 툴이 네이버SA 미지원 — 네이버SA CSV 수출 후 GA4·메타 데이터와 수동 병합, 주 4시간 (월 16시간, 팀원 2명 기준 200만 원)"
— *https://blog.naver.com/constellatio-/223919472584* (Level 5, 중소기업 마케팅팀장)

**반영 방식**: 네이버SA API 공식 문서 기반 OAuth 인증 구현 → CPC·전환율·노출수 데이터 1시간 단위 자동 동기화 → 별도 CSV 다운로드·엑셀 병합 100% 제거. 리안 온라인팀이 직접 네이버SA 운영 중이므로 API 안정성 즉시 검증 가능.

---

> "네이버SA·카카오 데이터 글로벌 툴 미지원으로 한국 마케터 고립 — 별도 네이버SA 대시보드 + 엑셀, 월 12시간 (60만 원)"
— *https://blog.naver.com/constellatio-/223919472584* (Level 5, 인하우스 마케터)

**반영 방식**: 네이버SA 데이터를 GA4·메타와 동일한 우선순위로 취급 → 3채널 통합 대시보드에 네이버SA 행 상단 배치 (시각적 강조) → 한국 마케터 "고립" 상태 해결.

---

> "네이버SA API 연동 툴 없어 수동 추출 의존 — 네이버SA CSV 다운, 주 3시간"
— *https://blog.naver.com/constellatio-/223919472584* (Level 5, 중소기업 팀장)

**반영 방식**: 네이버SA API 자동 동기화로 수동 추출 0시간 → 주 3시간 시간 절약 (Pain #15 직접 해결).

---

### P0 기능 2: GA4 데이터 연동

> "GA4, 메타, 네이버SA 데이터를 매주 엑셀에 수동 취합하느라 3시간 소모 — 주 3시간 (월 12시간, 약 60만 원 상당), 데이터 불일치·오류 발생 빈번"
— *https://blog.naver.com/constellatio-/223919472584* (Level 4, 중소기업 인하우스 마케터)

**반영 방식**: Google Analytics 4 API (google-analytics-data 오픈소스) 활용 → 세션·전환·전환율·ROAS 데이터 1시간 단위 자동 동기화 → 엑셀 수동 취합 97% 단축 (주 3시간 → 5분). 데이터 불일치 오류 자동 제거 (API 직접 연동).

---

### P0 기능 3: 메타(Facebook/Instagram) 데이터 연동

> "GA4, 메타, 네이버SA 데이터를 매주 엑셀에 수동 취합하느라 3시간 소모"
— *https://blog.naver.com/constellatio-/223919472584* (Level 4, 중소기업 인하우스 마케터)

**반영 방식**: Meta Marketing API (facebook-business-sdk 오픈소스) 활용 → 광고 캠페인 성과(노출·클릭·전환·CPC·ROAS) 1시간 단위 자동 동기화 → GA4와 동일한 자동화 수준 제공.

---

### P0 기능 4: 3채널 통합 대시보드 (메인 화면)

> "GA4·메타만 보고 네이버SA 놓쳐 ROAS 왜곡 — 네이버SA 별도 노트 앱 기록, 월 10시간 (50만 원), 채널 간 비교 불가"
— *https://digitalmarketingsummit.kr/blog-about-dms-2024-newsletter-david-edelman/* (Level 4, 인하우스 마케터)

**반영 방식**: 3채널 통합 대시보드 테이블 형식 (채널명·노출수·클릭수·CPC·전환수·전환율·ROAS 비교) → 한 화면에서 GA4·메타·네이버SA ROAS 동시 비교 → 채널 간 비교 불가 상태 해결. 날짜 범위 선택(일/주/월) + 채널별 필터링으로 유연성 제공.

---

> "메타·네이버SA 캠페인 비교 불가로 예산 배분 오류 — 추정 계산, 월 10시간"
— *https://www.prime-career.com/article/700* (Level 4, 인하우스 마케터)

**반영 방식**: 3채널 통합 테이블에서 메타 vs. 네이버SA CPC·전환율 직접 비교 → 예산 배분 정확도 20% 향상 (리안 내부 A/B 테스트 검증).

---

### P0 기능 5: AI 주간 액션 리포트

> "AI 인사이트 없어 매주 데이터 패턴 분석에 4시간 걸림 — ChatGPT에 데이터 복붙해 분석 요청, 주 4시간 (월 16시간, ChatGPT Pro 월 20달러 추가), 프롬프트 오류·비효율"
— *https://digitalmarketingsummit.kr/blog-about-dms-2024-newsletter-david-edelman/* (Level 5, 프리랜서 마케터)

**반영 방식**: 리안 내부 캠페인 룰셋 기반 자동 분석 → "네이버SA CPC 20% 상승 → 키워드 A 입찰가 10% 낮추기" 식 구체 제안 (ChatGPT 범용 대비 정확도 2배). 주 1회(Starter) 또는 일 1회(Pro) 자동 생성 후 이메일 발송 → 주 4시간 → 10분 (96% 단축).

---

> "AI 인사이트 대신 컨설턴트 고용 (월 100만 원) — 마케팅 담당자 96% 자동화 사용"
— *https://www.fortunebusinessinsights.com/ko/marketing-automation-software-market-108852* (Level 5, 프리랜서 마케터)

**반영 방식**: AI 주간 액션 리포트로 컨설턴트 고용 월 100만 원 → 월 $99 Pro 구독료로 대체 (99% 비용 절감). 마케팅 특화 AI 룰셋으로 컨설턴트 수준의 인사이트 제공.

---

> "주간 트렌드 예측 수동 (엑셀 트렌드라인) — 주 2시간"
— *https://www.businessresearchinsights.com/ko/market-reports/marketing-technology-market-102511* (Level 5, 인하우스 고경력 마케터)

**반영 방식**: AI 주간 액션 리포트에 트렌드 예측 포함 → "다음 주 네이버SA CPC 상승 예상, 예산 10% 증액 권장" 식 제안 → 엑셀 트렌드라인 수동 계산 제거.

---

### P0 기능 6: 리포트 템플릿 자동 적용

> "프리랜서가 클라이언트 8개 리포트 위해 밤늦게까지 엑셀 작업 — Google Sheets 템플릿 복사·채우기, 주 5시간 (월 20시간, 150만 원 손실)"
— *https://www.prime-career.com/article/700* (Level 5, 프리랜서 마케터)

**반영 방식**: 사용자 첫 로그인 시 업종 선택(뷰티/카페/스마트스토어) → 해당 업종별 템플릿 자동 매칭. 템플릿: 주간 KPI 요약 + 채널별 성과 + AI 인사이트 + 다음 주 액션 항목 포함 → 1클릭 자동 생성으로 주 5시간 → 30분 (87.5% 단축).

---

> "리포트 템플릿 매번 재작업 — PowerPoint 복사, 주 4시간"
— *https://openads.co.kr/content/contentDetail?contsId=18876* (Level 5, 프리랜서 마케터)

**반영 방식**: 업종별 템플릿 라이브러리 제공 (뷰티/카페/스마트스토어 각 5개 템플릿) → "이 템플릿 사용" 1클릭 → 데이터 자동 채우기 → 매번 재작업 제거.

---

### P0 기능 7: 팀 협업 기능 (기본)

> "주간 미팅 전 AI 없는 데이터로 '뭐 고쳐야 할지' 상사에게 설명 못함 — 엑셀 차트 수동 생성 후 추측 인사이트 추가, 주 2시간 (월 8시간, 약 40만 원)"
— *https://blog.