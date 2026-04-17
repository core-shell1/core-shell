"""
execute_cleanup.py — 루트 drift 정리 + fal-ai MCP 처리

1. PROJECTS.md → archive/ (내용 간소해서 기능 상실, 최신은 memory에)
2. PR_CHECKLIST.md → .claude/rules/ (규칙성 문서)
3. COLLABORATION_GUIDE.md → 유지 (외부 팀원용)
4. .mcp.json fal-ai → comment 처리 (Python 모듈로 대체됨)

일회성 스크립트. 실행 후 삭제.
"""
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
ARCHIVE = ROOT / "archive" / f"root_drift_{datetime.now().strftime('%Y%m%d')}"


def step_1_projects_to_archive():
    src = ROOT / "PROJECTS.md"
    if not src.exists():
        print("  ⏭️ PROJECTS.md 없음")
        return
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(ARCHIVE / "PROJECTS.md"))
    print(f"  ✅ PROJECTS.md → archive/ (memory에 최신 상태 있음)")


def step_2_pr_checklist_to_rules():
    src = ROOT / "PR_CHECKLIST.md"
    if not src.exists():
        print("  ⏭️ PR_CHECKLIST.md 없음")
        return
    dst = ROOT / ".claude" / "rules" / "pr-checklist.md"
    shutil.move(str(src), str(dst))
    print(f"  ✅ PR_CHECKLIST.md → .claude/rules/pr-checklist.md (자동 로드됨)")


def step_3_collaboration_keep():
    src = ROOT / "COLLABORATION_GUIDE.md"
    if src.exists():
        print(f"  ✅ COLLABORATION_GUIDE.md — 유지 (외부 팀원용 git 가이드)")


def step_4_disable_fal_mcp():
    mcp_file = ROOT / ".mcp.json"
    if not mcp_file.exists():
        print("  ⏭️ .mcp.json 없음")
        return
    data = json.loads(mcp_file.read_text(encoding="utf-8"))
    if "fal-ai" in data.get("mcpServers", {}):
        # 제거 + 주석으로 남김
        del data["mcpServers"]["fal-ai"]
        data["_disabled_fal_ai"] = {
            "reason": "fal-mcp-server uvx 연결 불안정. 대신 company/tools/nano_banana.py 사용",
            "restore": "이 블록 복원 + mcpServers 안으로 이동"
        }
        mcp_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"  ✅ fal-ai MCP 비활성화 (Python 모듈로 대체: tools/nano_banana.py)")
    else:
        print("  ⏭️ fal-ai 이미 없음")


def main():
    print("=== 루트 drift + MCP 정리 ===\n")
    print("[1/4] PROJECTS.md 정리:")
    step_1_projects_to_archive()
    print("\n[2/4] PR_CHECKLIST.md 이동:")
    step_2_pr_checklist_to_rules()
    print("\n[3/4] COLLABORATION_GUIDE.md:")
    step_3_collaboration_keep()
    print("\n[4/4] fal-ai MCP:")
    step_4_disable_fal_mcp()
    print("\n=== 완료 ===")


if __name__ == "__main__":
    main()
