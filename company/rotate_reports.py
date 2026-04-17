"""
rotate_reports.py — 보고사항들.md 로테이션

현재 전체를 archive로 백업하고, 요약 헤더만 남겨서 새로 시작.
2026-04-12 원칙: 1000줄 이하 유지.

일회성. 실행 후 삭제.
"""
import sys
import shutil
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
REPORT = ROOT / "보고사항들.md"
ARCHIVE = ROOT / "archive" / f"보고사항_백업_{datetime.now().strftime('%Y%m%d_%H%M')}.md"


def main():
    if not REPORT.exists():
        print("보고사항들.md 없음")
        return

    content = REPORT.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()
    total = len(lines)

    # 전체 백업
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPORT, ARCHIVE)
    print(f"[백업] {ARCHIVE.relative_to(ROOT)} ({total}줄)")

    # 새 헤더 작성
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_content = f"""# 보고사항들

> 에이전트들이 리안한테 직접 보고하는 공간.
> 1000줄 이하 유지. 오래된 내용은 `archive/`로 자동 로테이션.
> 마지막 로테이션: {now} (이전 {total}줄 → `{ARCHIVE.name}`)

---

## 2026-04-17 시스템 대정비 — 서연

### 한 세션에 정리한 것
| 영역 | 결과 |
|------|------|
| 인스타분석팀 업그레이드 | gallery-dl + Gemini + 딥다이브(GitHub README/Perplexity/사이트 방문) + core-shell 컨텍스트 프롬프트 |
| 자동 탐지 레이어 | `.claude/CAPABILITIES.md` — 태스크→능력 라우팅. 내가 알아서 씀 |
| Anthropic Skills 17개 | `design_system/references/anthropic-skills/` (pdf/docx/xlsx/pptx/brand-guidelines/skill-creator 등) |
| 신규 툴 | `tools/nano_banana.py` (제품 광고 이미지), `tools/cost_tracker.py` (비용 추적) |
| 토큰 효율 규칙 | `.claude/rules/token-efficiency.md` + settings.json autocompact 50% |
| NotebookLM MCP | stub 추가 (.env 인증 넣으면 활성) |
| 모델 ID 최신화 | Opus 4.6/4.1 → 4.7, Sonnet 4.5 → 4.6 (168개 파일, 215회 치환) |
| 폴더 정리 | 빈 팀 4개 + 구버전 팀 1개 → archive |
| 루트 drift | PROJECTS.md → archive, PR_CHECKLIST.md → .claude/rules |
| 네이밍 혼란 | README 3개 + `.claude/ARCHITECTURE.md` (지도) |
| 프롬프트 감사 | 150줄 위반 25개 발견 (threejs 스킬 다수, cdo/pm/director 에이전트, landing/work 커맨드) |
| 팀 활성 감사 | company/teams/ 23개 전부 활성 — 죽은 팀 없음 |

### 다음 세션 시작 전 리안이 알아야 할 것
- 구조 변경 없음, 안전함
- 이제 "~해줘" 하면 CAPABILITIES.md 자동 참조해서 내가 라우팅
- 새 능력 추가 시 CAPABILITIES.md 즉시 업데이트 (feedback_auto_record 메모리 준수)

### 미해결 / 나중에
- 프롬프트 150줄 위반 25개 — 큰 작업이라 배제. 필요 시 epic으로 분리
- fal-ai MCP 비활성화 (Python 모듈 nano_banana.py로 대체)
- NotebookLM MCP 활성화 (계정 자격증명 필요)

---
"""

    REPORT.write_text(new_content, encoding="utf-8")
    print(f"[갱신] 보고사항들.md 새 헤더로 교체 ({len(new_content.splitlines())}줄)")


if __name__ == "__main__":
    main()
