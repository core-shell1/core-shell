# 진행 상태

> Claude Code 켤 때마다 여기부터 확인. 마지막 업데이트: 2026-03-30 (CTO 기술 설계 완료)

---

## ✅ 2026-03-30 Wave 1 CTO 기술 설계 완료

**작성 항목**: wave1_cto.md (소상공인 카카오톡 자동 응대 챗봇 빌더)

**포함 내용**:
- Cloudflare 스택 아키텍처 (Pages + Workers + D1 + R2 + Queues)
- 카카오 API 격리 모듈 설계 (정책 변경 1~2일 대응)
- 데이터 모델 (6개 테이블: users, chatbots, templates, responses, messages, analytics)
- API 엔드포인트 (15개: 인증 3개, 온보딩 4개, 챗봇 관리 4개, 대시보드 2개, 웹훅 1개, 관리 1개)
- 온보딩 플로우 (액션 10회, 7분 목표, 시간 로깅)
- 보안 설계 (HTTPS, CSRF, Rate Limiting, 토큰 암호화, 비밀번호 해싱)
- 성능 요구사항 (API 응답 < 500ms, 동시 100명 수용)
- 기술 리스크 및 대응책 (NextAuth.js 호환성, SQLite 성능, 카카오 정책 변경)
- 배포 블로커 체크리스트 (Cloudflare 계정, D1 생성, 카카오 OAuth 테스트)

**준혁 조건 반영**:
1. ✅ MVP 범위 강제 (AI 개인화/ROI 대시보드 제외)
2. ✅ 비용 팝업 필수 (온보딩 Step 3)
3. ✅ 5분 완성 검증 (액션 10회 이내, 시간 로깅)
4. ✅ 카카오 API 격리 모듈 (services/kakao/ 폴더만 수정)

**최종 판단**: **CONDITIONAL_GO**
- 전제 1: Cloudflare Workers 계정 + D1 생성 (리안 담당)
- 전제 2: 카카오 OAuth 손수 테스트 (리안 담당)
- 전제 3: Wave 2-3 코드 후 온보딩 실제 테스트 (7분 이내)
- 유효기간: 2026-04-15 (2주)

**다음 단계**: Wave 2 CDO 화면 설계 → Wave 3 FE/BE 코드

---

## ✅ 2026-03-30 Wave 1 CPO 분석 완료

**작성 항목**: wave1_cpo.md (소상공인 카카오톡 자동 응대 챗봇 빌더)

**포함 내용**:
- 제품 전략 (포지셔닝 + 핵심 메시지)
- MVP 범위 5가지 기능
- 가격 전략 (3단계 플랜 + LTV/CAC 분석)
- 배포 경로 (3개월 로드맵 + 월별 성장)
- 성공 기준 KPI (30일/90일 목표)
- 배포 블로커 체크리스트
- CTO 요청 (4대 필수 + 권장 구현)
- 리스크 & 기회 분석
- CPO 최종 판단 (GO, 제약 조건 있음)

**준혁 조건 반영**:
- MVP 범위 강제 준수 (AI 개인화/ROI 대시보드 제외)
- 카카오 메시지 비용 안내 팝업 필수 (온보딩 3단계)
- 5분 완성 검증 (액션 10회 이내, 로깅 필수)
- 카카오 API 격리 아키텍처

**다음 단계**: CTO Wave 1 기술 설계 실행 (wave1_cto.md)

---

## ✅ 2026-03-30 폴더 이름 변경 완료

- `LAINCP - 복사본` → `LIANCP` (이름 변경 완료)
- memory 복사 완료 (LAINCP → LIANCP memory 폴더)
- CLAUDE.md 경로 참조 LAINCP → LIANCP 수정 완료

### 이어서 할 것
- 디스코드 봇 설계 + 구현 (토론 중이었음)
- /work 자동 연결 (pipeline.py 마지막에 claude -p "/work" 추가)

---

## 2026-03-30 세션에서 한 것

**1. E2E 테스트 완료**
- `python main.py` 전체 파이프라인 완주 확인
- 이사팀(태호→서윤→민수→하은→토론→준혁) + 실행팀(지훈→종범→수아) 전부 작동
- 버그 수정: Windows 폴더명 콜론 오류, surrogate 유니코드 오류

**2. 시은 방향 확인 추가**
- 명확화 후 4줄 요약 보여줌 ("이 방향 맞아? [맞아/아니]")
- 틀리면 수정 받고 재요약
- 파일: `lian_company/agents/sieun.py`

**3. Cloudflare 스택으로 전환**
- Vercel → Cloudflare Pages
- Supabase → Cloudflare D1 + R2
- 백엔드 → Cloudflare Workers (Hono, TypeScript)
- 파일: `.claude/agents/cto.md`, `.claude/agents/be.md`, `.claude/commands/work.md`

**4. 아키텍처 토론 결론**
- 지금 구조(Python 이사팀 + Claude Code 개발팀) = 업계 정석 (CrewAI, AutoGen과 동일)
- Python 통합(A안) = 퀄 안 좋아짐, 할 필요 없음
- 디스코드 봇으로 자동화(B안) = 맞는 방향

**5. 디스코드 봇 설계 토론 (미완, 이어서 할 것)**

```
이사팀 (Python 직접 호출) → 디스코드 채널에 실시간 출력 ✅ 쉬움
개발팀 (Claude Code /work) → 두 가지 안:
  A) 봇이 claude -p "/work" 백그라운드 실행 후 결과만 전송
  B) 개발팀도 디스코드 캐릭터로 등장 (Claude API 직접 호출)
```

**추천: A안 먼저, 나중에 B안으로 업그레이드**

---

---

## 마지막 세션 (2026-03-29 — LAINCP 복사본 Phase 1 업그레이드 완료)

**뭘 했나 (2026-03-29 세션):**
인스타 10개 + 유튜브 14개 분석 → 5대 문제 도출 → 복사본에 Phase 1 전체 구현.

**핵심 변경 사항:**

1. **모델 최적화** — Opus 5회→1회 (비용 ~60% 절감)
   - junhyeok.py: Opus→Sonnet
   - CPO/CTO/BE 에이전트: Opus→Sonnet
   - CTO Wave 4 통합 리뷰만 Opus 유지 (전체 파이프라인 유일한 Opus 사용)

2. **품질 안전장치**
   - junhyeok.py: JSON 파싱 실패 기본값 GO→CONDITIONAL_GO (안전방향)
   - jihun.py: 하은 반론을 PRD 리스크 섹션에 강제 반영
   - temperature 전 에이전트 명시: 판단=0, 창의=0.7, 균형=0.3
   - haeun.py: JSON 구조 출력 (verdict + severity + critical_risks)

3. **토론 루프** — 민수↔하은 최대 2라운드
   - 신규: `lian_company/core/discussion.py` (DiscussionRoom 클래스)
   - pipeline.py: [4.5/9] 토론 루프 단계 추가
   - junhyeok.py: 토론 결과 transcript 참조

4. **CDO 레퍼런스 사냥** — Perplexity로 경쟁사 디자인 수집 후 설계
   - cdo.md: "레퍼런스 사냥" 섹션 추가 (작업 전 필수)

5. **FE CDO 준수** — CDO 설계 스펙 그대로 구현 강제
   - fe.md: "CDO 설계 준수 원칙" 섹션 추가

6. **QA 5항목 체크리스트**
   - qa.md: 단순 "Must Have 작동" → 5개 항목 표 (보안/에러/CDO/모바일 포함)

7. **work.md 업데이트**
   - Wave 3.5 린터 단계 추가 (ESLint + Ruff 자동 수정)
   - Wave 4 CTO 리뷰 Opus로 변경

8. **jongbum.py 업그레이드**
   - 준혁 조건/주의사항 → "구현 주의사항" 섹션으로 전달
   - 토론 transcript 참조 추가
   - temperature=0

**변경된 파일 (복사본):**
- `lian_company/agents/junhyeok.py` — 모델+기본값+토론참조+temperature
- `lian_company/agents/jihun.py` — 하은참조+temperature
- `lian_company/agents/haeun.py` — JSON출력+temperature
- `lian_company/agents/sieun.py` — temperature
- `lian_company/agents/minsu.py` — temperature
- `lian_company/agents/jongbum.py` — 준혁조건+토론참조+temperature
- `lian_company/core/discussion.py` — 신규 생성
- `lian_company/core/pipeline.py` — 토론루프 추가
- `.claude/agents/cdo.md` — 레퍼런스 사냥 섹션
- `.claude/agents/cto.md` — 모델 명시
- `.claude/agents/cpo.md` — 모델 명시
- `.claude/agents/be.md` — 모델 명시
- `.claude/agents/fe.md` — CDO 준수 원칙, 모델 업그레이드
- `.claude/agents/qa.md` — 5항목 체크리스트, 모델 업그레이드
- `.claude/commands/work.md` — Wave 3.5 린터, CTO Opus 명시

**다음에 할 것:**
- 복사본에서 E2E 테스트 (python main.py "테스트 아이디어")
- 테스트 통과하면 원본 LAINCP에 반영
- Phase 2: 텔레그램 봇 연동 (telegram_bot.py + notifier.py)

---

## 마지막 세션 (2026-03-29 — 인스타+유튜브 분석)

**뭘 했나 (2026-03-29 세션 前):**
- video_analyzer.py 생성 (Gemini로 영상/이미지 분석)
- 인스타 10개 폴더 분석 → `업그레이드 해야할거/_전체분석결과.md`
- 유튜브 14개 스크립트 분석 → `11/_유튜브분석결과.md`
- 심층 분석 → `_심층분석_종합.md` (5대 문제 + 해결 설계)

---

## 마지막 세션 (2026-03-28 — 팀플 Wave 1 CDO 분석 완료)

**뭘 했나 (2026-03-28 세션):**
항해 팀플 Voyage App Wave 1 CDO 분석 완료.
디자인 시스템 + 컴포넌트 목록 + 화면 레이아웃 + 애니메이션 설계 전체.

**CDO 주요 결정:**
- 컬러 팔레트: ocean-deep(#4B9FE1) / sand(#FFE4A0) / coral(#FF8A7A) / gold(#FFD95A)
- 팀원 아바타: 4색 고정 (파랑/노랑/코랄/보라) — created_at 순서로 자동 배정
- 배 7단계: 이모지 + CSS 조합 (이모지: 🪵→⛵→⛵→🚢→🚢→🚢→🏴‍☠️+🚢)
- 승선 애니메이션: 아바타 포물선 이동 (섬→배), Framer Motion 키프레임
- 출항 애니메이션: 배 곡선 이동 + ConfettiEffect (2.5초)
- 리텐션 트릭 8개: 미완성 루프, 스트릭 공개, AI 메시지 기대감 등

**신규 생성 파일:**
- `projects/[진행] 팀플/wave1_cdo.md` ← CDO 분석 완성본 (디자인 시스템 + 전체 화면 설계)

이전 세션 (2026-03-28 — PRD + CPO + CTO 분석):
- `projects/[진행] 팀플/PRD.md` ← 완전한 PRD
- `projects/[진행] 팀플/CLAUDE.md` ← 기술 스택 + 데이터 모델
- `projects/[진행] 팀플/wave1_cpo.md` ← CPO 분석
- `projects/[진행] 팀플/wave1_cto.md` ← CTO 분석

**다음 세션에서 이어할 것:**
- Wave 2: FE + BE 코드 작성 실행
- Supabase 프로젝트 생성 (URL/KEY 확보)
- Google OAuth 설정 (CLIENT_ID/SECRET 확보)
- `projects/[진행] 팀플/voyage-app/` 폴더에서 Next.js 프로젝트 생성

---

## 마지막 세션 (2026-03-27 — 소상공인 비대면 영업 가이드 최종본 완성)

**뭘 했나 (2026-03-27 세션):**
소상공인 영업툴 — 방문 미팅 중심에서 비대면(카카오/문자) 클로징 중심으로 전략 전환.
UltraProduct CPO + 마케팅(수아) 에이전트 Wave 1 실행 후, 리안 컨펌 받아 최종 가이드 완성.

**결정 사항:**
- 패키지: 주목 29만 / 집중 49만 / 시선 89만 (월, 최저 할인가, 3개월 이상 계약)
- 패키지 나열 순서: 89→49→29 (앵커링)
- 비대면 메인: 집중 플랜 49만원 중심
- 하루 발송: 50건, 오전 10시 고정
- 계약: 무조건 3개월 이상 (월 단위 없음)
- 1차 메시지 D형(경쟁사 움직임형) 추가
- PPT는 2차에서 안 보냄, 3차 이후 이미지 3장만
- CTA: 이중선택형 ("집중이랑 주목 중 어떤 게 맞으세요?")
- 4차 이후: 2주/1개월/2개월 장기 nurturing

**신규 생성 파일:**
- `projects/[진행중] 오프라인 마케팅/소상공인_영업툴/영업_실전가이드_최종.md` ← 지금 쓸 수 있는 완성본
- `projects/[진행중] 오프라인 마케팅/소상공인_영업툴/wave1_cpo_영업퍼널_재설계.md`
- `projects/[진행중] 오프라인 마케팅/소상공인_영업툴/marketing/비대면_퍼널_전환최적화.md`

**다음 세션에서 이어할 것:**
- 글로싸인 계약서 템플릿 만들기 (비대면 서명용)
- 카카오페이 송금 링크 세팅
- 영업 트래킹 구글시트 만들기 (업체명/단계/날짜/메모)
- 원한다면 진단 툴에 메시지 자동 생성 기능 추가 (복붙만 하면 되게)

---

## 마지막 세션 (2026-03-26 — Wave 5 마케팅 전략 완료)

**뭘 했나 (2026-03-26 세션):**
소상공인 영업툴 Wave 5 마케팅 전략 + 콘텐츠 완성.

**Wave 5-1 채널 전략 (marketing/wave5_1_채널전략.md):**
- 채널 TOP 3 선정: 네이버 블로그 (SEO 장기 자산) / 네이버 카페 (즉시 타겟 접촉) / 인스타 (신뢰 보강)
- 채널별 타겟팅 방법 + 예상 효과 수치 명시
- 세일즈 퍼널 4단계 (미끼→주목 29만→집중 49만→시선 89만) 설계
- Cold/Warm/Hot 방문자 온도별 콘텐츠 전략 분리
- 실행 우선순위 타임라인 (지금 바로 / 이번 주 / 2주 후)

**Wave 5-2 콘텐츠 완성 (marketing/wave5_2_콘텐츠.md):**
- 블로그 SEO 글 전문 2,000자+ (제목 A/B/C 3안, 추천 A안)
- 네이버 카페 글 3개 (지역 소상공인 카페/맘카페/직접 타겟 스타일 각각 다름)
- 인스타 캡션 A/B/C (Hook-Story-Offer 구조, PAS 카피) + DALL-E 이미지 프롬프트 3종
- 해시태그 30개 (대형/중형/소형/지역/업종 분류)
- 발행 스케줄 4주 플랜 + 성과 측정 기준

**신규 생성 파일:**
- `projects/[진행중] 오프라인 마케팅/소상공인_영업툴/marketing/wave5_1_채널전략.md`
- `projects/[진행중] 오프라인 마케팅/소상공인_영업툴/marketing/wave5_2_콘텐츠.md`

**이전 세션 (Wave 3 CTO 통합 리뷰):**
CTO 리뷰 결과: PASS, 버그 6개 발견 → 즉시 수정 완료

**다음 세션에서 이어할 것:**
- [ ] **즉시 실행**: `cd naver-diagnosis && pip install openpyxl`
- [ ] **즉시 실행**: `.env` 파일에 `DB_RESET=true` 추가 → 서버 재시작 → 제거
- [ ] 단건 진단 1건 테스트 (양주 미용실) → /result/{id} 페이지 렌더링 확인
- [ ] 메시지 탭 4개 정상 표시 확인
- [ ] xlsx 배치 처리 5개 업체 테스트
- [ ] lian_company/.env 생성 후 파이프라인 테스트

---

## 리안 컴퍼니 (기획 엔진)

| 항목 | 상태 |
|------|------|
| 에이전트 코드 | ✅ 완료 (멀티 AI: Perplexity/GPT-4o/Gemini/Claude) |
| 패키지 설치 | ✅ 완료 (openai, google-genai, anthropic) |
| jongbum.py 시장 리서치 | ✅ 완료 (서윤/태호/하은 데이터 → CLAUDE.md에 포함) |
| .env 파일 | ❌ 없음 — `lian_company/.env` 만들어야 실행 가능 |

**.env에 필요한 키**: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY, PERPLEXITY_API_KEY
**키 위치**: `새 폴더/api.txt`

---

## UltraProduct 에이전트 지식 통합 (2026-03-26)

| 에이전트 | 주입된 지식 | 상태 |
|----------|------------|------|
| CDO | UX 원칙, 화면별 설계, 비주얼 디자인, 전환 최적화, 채널→디자인 | ✅ 완료 |
| 수아(마케팅) | 세일즈 퍼널, 가치 사다리, Hook-Story-Offer, PAS, 방문자 온도 | ✅ 완료 |
| /work 플로우 | Wave 1에 수아 채널 사전 판단 추가 | ✅ 완료 |

---

## 프로젝트별 상태

| 프로젝트 | 코드 | 배포 | 마지막 작업 |
|----------|------|------|-------------|
| 마케터_고객_플랫폼 (채팅+매칭 통합) | ✅ 있음 | ❌ 미배포 | 2026-03-24 |
| 소상공인_영업툴 (진단+연락처 통합) | ✅ 있음 | ❌ 미배포 | 2026-03-24 |
| 지역_소상공인_010번호+인스타 수집 툴 | ✅ 완료 | ❌ 미배포 | 2026-03-24 |
| 인스타 자동화 | ✅ 있음 | ❌ 미배포 | - |
| 포천 영업타겟 발굴 | ✅ 있음 | ❌ 미배포 | - |
| 네이버 플레이스 자동 진단 PPT | ✅ Wave 3 QA PASS | ❌ 미배포 | 2026-03-26 |

---

## Git 상태

| 항목 | 상태 |
|------|------|
| Git 초기화 | ✅ 완료 |
| 자동 커밋 hook | ✅ 작동 중 (Edit/Write 시 자동 커밋+push) |
| GitHub 원격 | ✅ 연결됨 (https://github.com/lian1803/LianCP.git) |
| 자동 push | ✅ 작동 중 |

---

## 최근 변경 이력

| 날짜 | 변경 내용 | 파일 |
|------|----------|------|
| 2026-03-26 | Wave 5 마케팅 전략 + 콘텐츠 완성 (블로그/카페/인스타) | marketing/wave5_1_채널전략.md, wave5_2_콘텐츠.md |
| 2026-03-26 | CTO 통합 리뷰 — 치명 버그 4개 + 중간 2개 수정 | main.py, routers/crawl.py, routers/batch.py |
| 2026-03-26 | /history, /batch 페이지 라우터 추가 | main.py |
| 2026-03-26 | messages 구조 변환 + sales_priority 동적 속성 | main.py |
| 2026-03-26 | crawl.py 경쟁사 크롤링/우선순위/메시지 통합 | routers/crawl.py |
| 2026-03-26 | CTO 리뷰 결과 저장 | qa/cto_review.md |
| 2026-03-26 | 영업툴 Wave 3 QA 검증 완료 (조건부 통과, 버그 2건 수정) | naver-diagnosis/ + qa/ |
| 2026-03-26 | CDO 에이전트 UX/비주얼/전환 업그레이드 | .claude/agents/cdo.md |
| 2026-03-26 | 수아 마케팅 퍼널/PAS/Hook 업그레이드 | .claude/agents/marketing.md |
| 2026-03-26 | /work Wave 1 순서 변경 | .claude/commands/work.md |
| 2026-03-26 | 종범 시장 리서치 포함 | lian_company/agents/jongbum.py |
| 2026-03-26 | 루트 CLAUDE.md 전면 업데이트 | CLAUDE.md |
| 2026-03-26 | 영업툴 백엔드 업그레이드 (메시지/배치/경쟁사/PPT9슬라이드) | naver-diagnosis/ |
| 2026-03-25 | 네이버 진단 PPT QA PASS | projects/번호로 자동으로 분석까지/ |

---

## 다음에 해야 할 것

- [ ] lian_company/.env 생성 후 파이프라인 테스트
- [ ] GitHub 레포 생성 → URL → 자동 push 연결
- [ ] 전체 E2E 테스트 (python main.py → /work)
- [ ] 각 프로젝트 배포 순서 결정

## 소상공인 수집툴 — 나중에 추가할 것

- [ ] 공공데이터포털 (data.go.kr) API — 이미 가입함
- [ ] 배달의민족 — 음식점 010번호
- [ ] 야놀자/여기어때 — 숙박업체

## 영업 문서 현황

| 파일 | 위치 |
|------|------|
| 영업_플레이북.md | projects/소상공인_영업툴/ |
| 영업_스크립트.md | projects/소상공인_영업툴/ |
