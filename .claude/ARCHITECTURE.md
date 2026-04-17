# ARCHITECTURE — 리안용 폴더 지도

> 헷갈릴 때 이거만 봐. 1분이면 전체 구조 파악.

## 최상위 2개 — 역할이 완전 다름

```
core/                ← Claude Code 환경 (사무실)
└── company/         ← Python 자동화 엔진 (지하 공장)
```

| | `core/` (사무실) | `core/company/` (공장) |
|---|---|---|
| **누가 읽음** | Claude Code, 에이전트들 | Python 인터프리터 |
| **주요 파일** | `.claude/`, `CLAUDE.md`, `team/` | `main.py`, `daily_auto.py`, `venv/` |
| **건드리면** | 상대적으로 안전 | 자동화 스크립트 깨짐 위험 |

---

## `core/` 하위 (사무실 안)

| 폴더 | 역할 |
|---|---|
| `.claude/` | Claude Code 설정 — agents/skills/commands/rules/CAPABILITIES.md |
| `team/` | **팀이 만든 결과물** (CLAUDE.md, 웹 앱, SaaS) |
| `design_system/` | 디자인 레퍼런스 + Anthropic Skills 17개 |
| `knowledge/` | 지식 베이스 (에이전트 런타임 로드용) |
| `decisions/` | 과거 중요 결정 기록 |
| `archive/` | 과거 작업 보관 (절대 건드리지 마) |
| `test/` | 임시 실험 파일 (작업 끝나면 즉시 삭제) |

## `core/company/` 하위 (공장 안)

| 폴더 | 역할 |
|---|---|
| `teams/` | **팀 실행 엔진** (Python 모듈, run_*.py가 import) |
| `tools/` | 공용 Python 툴 (nano_banana, cost_tracker, image_generator 등) |
| `utils/` | 공용 유틸 (insta_browse, naver_crawler, meta_ads 등) |
| `core/` | 내부 Python 모듈 (ops_loop, insight_extractor, design_router 등) |
| `knowledge/` | 에이전트 런타임 로드 지식 (prompts, templates) |
| `outputs/` | 자동화 스크립트 결과물 |
| `venv/` | Python 가상환경 (절대 건드리지 마) |

---

## 헷갈리기 쉬운 것 — 명확히

### Q: `team/` vs `company/teams/` 차이는?
- `core/team/디자인팀/` = 디자인팀이 만든 **실제 프로젝트/결과물**
- `core/company/teams/디자인팀/` = 디자인팀의 **AI 실행 로직** (Python)
- 같은 이름이어도 내용은 완전 다름

### Q: 새 팀 만들 때 어디에?
- `python company/build_team.py "팀명"` 실행하면 **둘 다 자동 생성**
- 수동으로 만들지 마

### Q: 태스크 받으면 어디부터?
- `.claude/CAPABILITIES.md` 트리거 매핑 확인
- 있으면 바로 사용, 없으면 리안에게 제안

---

## 절대 규칙
- 구조 바꾸지 마. 돌아가는 거 깨짐
- 새 파일은 규칙대로 (`.claude/rules/apply-insights.md` 참고)
- 테스트 파일은 `test/` 안 + 작업 끝나면 즉시 삭제
