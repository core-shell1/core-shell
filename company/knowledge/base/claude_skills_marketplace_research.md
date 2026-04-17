# Claude Skills 마켓플레이스 조사 결과 (2026-04-09)

## 1. 마켓플레이스 4곳 + 공식 저장소

### (1) SkillsMP — skillsmp.com
- **규모:** 700,000+ 스킬 (최대 규모)
- **특징:** Claude Code, Codex CLI, ChatGPT 호환. 직업별/인기순/작성자별 필터링
- **설치:** `npx skills add <org>/<repo>` 또는 마켓 페이지에서 복사
- **비용:** 무료 (오픈 SKILL.md 표준)

### (2) Claude Code Plugin Marketplace — claudemarketplaces.com
- **규모:** 2,400+ 스킬, 2,500+ 플러그인 마켓, 770+ MCP 서버
- **특징:** 커뮤니티 큐레이션. 투표/댓글 시스템. 설치수+깃헙스타 기반 품질 정렬
- **카테고리:** Agent Skills / Plugin Marketplaces / MCP Servers
- **설치:** 상세 페이지에서 설치 명령어 복사 → 터미널 실행
- **비용:** 완전 무료

### (3) Claude Skills Market — skills.pawgrammer.com
- **규모:** 280+ 스킬
- **특징:** 커뮤니티 기여형. 카테고리: 개발, 비즈니스, 마케팅/세일즈, 데이터분석, 라이팅
- **주목 스킬:** Marketing Skills Pack (33개 SaaS 마케팅 스킬), clawfu-skills (175개 마케팅 방법론)
- **설치:** SKILL.md 파일을 .claude/skills/에 복사
- **비용:** 무료

### (4) MCP Market — mcpmarket.com/tools/skills
- **규모:** 수백 개 (정확한 수 미공개)
- **특징:** Agent Skills + MCP 서버 통합 디렉토리. Claude/Codex/ChatGPT 호환
- **설치:** 페이지별 설치 명령어 제공
- **비용:** 무료

### (공식) Anthropic Skills Repository — github.com/anthropics/skills
- **규모:** 17+ 공식 스킬 (87,000+ 깃헙 스타)
- **포함:** frontend-design, brand-guidelines, canvas-design, theme-factory, skill-creator, PDF, DOCX, PPTX, XLSX 등
- **설치:** `npx skills add anthropics/skills --skill <이름>`

---

## 2. 인스타에서 언급된 6개 스킬 상세

### (1) Frontend Design — 공식 Anthropic 스킬
- **기능:** AI slop 없는 고품질 프론트엔드 코드. 디자인 시스템+철학을 코드 전에 주입. 대담한 미학, 의도적 애니메이션
- **설치수:** 277,000+ (가장 인기)
- **설치:** `npx skills add anthropics/skills --skill frontend-design`
- **비용:** 무료
- **우리 적용:** 랜딩페이지/웹사이트 퀄리티 향상. 현재 CLAUDE.md의 Three.js 기준과 병행 가능

### (2) Figma to Code
- **기능:** Figma 링크 → 레이아웃/타이포/컬러/컴포넌트 구조 추출 → React/Vue 코드 생성
- **출처:** Figma 공식 MCP 서버 + 커뮤니티 스킬 다수
- **설치:** `npx skills add figma-design-to-code` 또는 Figma MCP 서버 연결
- **비용:** 무료 (Figma 계정 필요)
- **우리 적용:** 디자인 → 코드 자동화. FE 에이전트와 연동 가능

### (3) Theme Factory — 공식 Anthropic 스킬
- **기능:** 10개 프리디자인 테마 즉시 생성. 컬러팔레트+폰트 조합. 슬라이드/문서/리포트/HTML 랜딩에 적용
- **출력:** CSS custom properties (디자인 토큰) → frontend-design 스킬이 소비
- **설치:** `npx skills add anthropics/skills --skill theme-factory`
- **비용:** 무료
- **우리 적용:** 클라이언트별 브랜딩 자동화. 오프라인 마케팅 PDF에 즉시 적용 가능

### (4) Brand Guidelines — 공식 Anthropic 스킬
- **기능:** 브랜드 컬러/타이포/비주얼 가이드라인 자동 적용. 일관된 브랜딩 유지
- **설치:** `npx skills add anthropics/skills --skill brand-guidelines`
- **비용:** 무료
- **우리 적용:** 클라이언트 브랜드 가이드 입력 → 모든 산출물에 자동 반영

### (5) Canvas Design — 공식 Anthropic 스킬
- **기능:** 실제 비주얼 PNG/PDF 내보내기. 포스터/아트/디자인 생성. 90% 비주얼 + 10% 텍스트
- **작동:** Visual Philosophy(미학 철학) .md 생성 → PDF/PNG 아티팩트 출력
- **설치:** `npx skills add anthropics/skills --skill canvas-design`
- **비용:** 무료
- **우리 적용:** 영업 자료 비주얼(명함/전단/포스터) 자동 생성

### (6) Skill Creator — 공식 Anthropic 스킬
- **기능:** 커스텀 스킬 직접 제작. 4가지 모드: Create(생성), Eval(평가), Improve(개선), Benchmark(벤치마크)
- **작동:** 인터랙티브 Q&A → 완전한 SKILL.md 디렉토리 자동 생성
- **설치:** `npx skills add anthropics/skills --skill skill-creator`
- **플러그인:** claude.com/plugins/skill-creator 에서도 사용 가능
- **비용:** 무료
- **우리 적용:** ⭐ 핵심. 우리 에이전트 전용 스킬 직접 제작 가능 (소상공인 진단, 영업 스크립트 등)

---

## 3. 소상공인 영업자동화 활용 가능 스킬

### 콘텐츠 생성
| 스킬 | 설치 | 용도 |
|------|------|------|
| copywriting | `npx skills add coreyhaines31/marketingskills --skill copywriting` | 카피라이팅 전문 |
| social-content | 동일 레포 --skill social-content | SNS 콘텐츠 |
| cold-email | 동일 레포 --skill cold-email | B2B 콜드메일 |
| email-sequence | 동일 레포 --skill email-sequence | 이메일 시퀀스 |
| seo-audit | 동일 레포 --skill seo-audit | SEO 감사 |

### CRM/영업 자동화
| 스킬 | 설치 | 용도 |
|------|------|------|
| revops | `npx skills add coreyhaines31/marketingskills --skill revops` | 리드 스코어링, CRM 자동화 |
| sales-enablement | 동일 레포 --skill sales-enablement | 피치덱, 제안서, 이의처리 |
| competitor-alternatives | 동일 레포 --skill competitor-alternatives | 경쟁사 비교 페이지 |

### 디자인/비주얼
| 스킬 | 설치 | 용도 |
|------|------|------|
| canvas-design | `npx skills add anthropics/skills --skill canvas-design` | 포스터/전단 PNG/PDF |
| theme-factory | `npx skills add anthropics/skills --skill theme-factory` | 브랜드 테마 자동 생성 |
| brand-guidelines | `npx skills add anthropics/skills --skill brand-guidelines` | 브랜드 일관성 |
| frontend-design | `npx skills add anthropics/skills --skill frontend-design` | 웹 UI 고품질 |

### 마케팅 방법론
| 스킬 | 설치 | 용도 |
|------|------|------|
| clawfu-skills (175개) | `git clone github.com/guia-matthieu/clawfu-skills` → .claude/skills/ 복사 | Cialdini 설득, Hormozi 오퍼, Ogilvy 광고 등 전문 방법론 |
| marketing-ideas | `npx skills add coreyhaines31/marketingskills --skill marketing-ideas` | 마케팅 아이디어 |
| marketing-psychology | 동일 레포 --skill marketing-psychology | 심리학 기반 마케팅 |
| pricing-strategy | 동일 레포 --skill pricing-strategy | 가격 전략 |
| launch-strategy | 동일 레포 --skill launch-strategy | 런칭 전략 |

---

## 4. 우리 시스템 적용 계획

### 즉시 설치 (우선순위 높음)
1. **skill-creator** — 우리 에이전트 전용 스킬 직접 만들기 (소상공인 진단서, 영업 멘트 등)
2. **copywriting** — 온라인납품팀/오프라인마케팅팀 카피 품질 향상
3. **canvas-design** — 영업 자료(전단/포스터) 비주얼 자동 생성
4. **theme-factory** — 클라이언트별 브랜드 테마 자동 적용

### 검토 후 설치
5. **cold-email + sales-enablement** — 온라인영업팀 아웃리치 강화
6. **clawfu-skills** — 175개 마케팅 방법론 (Hormozi 오퍼 프레임 등) → 에이전트 전문성 강화
7. **frontend-design** — 웹 랜딩페이지 퀄리티 (현재 CLAUDE.md 기준과 통합)
8. **seo-audit** — 네이버/구글 SEO 진단 자동화

### 자체 제작 대상 (Skill Creator 활용)
- 소상공인-진단서-생성 스킬 (네이버 플레이스 분석 → PDF 진단서)
- 오프라인-영업멘트 스킬 (업종별 맞춤 영업 스크립트)
- 카카오톡-메시지 스킬 (PC카톡 연동 자동 메시지)
- 한국형-블로그-SEO 스킬 (네이버 블로그 최적화)

### 설치 방법 요약
```bash
# 공식 Anthropic 스킬 (프로젝트 루트에서)
npx skills add anthropics/skills --skill skill-creator
npx skills add anthropics/skills --skill canvas-design
npx skills add anthropics/skills --skill theme-factory
npx skills add anthropics/skills --skill brand-guidelines
npx skills add anthropics/skills --skill frontend-design

# 마케팅 스킬 팩
npx skills add coreyhaines31/marketingskills

# clawfu 마케팅 방법론 (175개)
git clone https://github.com/guia-matthieu/clawfu-skills
cp -r clawfu-skills/skills/* .claude/skills/
```

---

## 5. 핵심 정리

- **SKILL.md 표준:** Anthropic이 2025.12 공개한 오픈 표준. Claude Code/Codex/ChatGPT/Cursor 등 14개+ 플랫폼 호환
- **스킬 = 폴더:** SKILL.md(메타데이터+지시) + 선택적 스크립트/템플릿. 에이전트가 컨텍스트 기반 자동 활성화
- **우리 시스템과의 시너지:** 에이전트 프롬프트에 스킬 지식을 주입하면 → 교육팀 커리큘럼 품질 향상 + 영업팀 산출물 품질 향상
- **Skill Creator가 킬러:** 우리만의 소상공인 특화 스킬을 직접 만들 수 있음 → 경쟁력
