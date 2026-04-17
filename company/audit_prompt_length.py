"""
audit_prompt_length.py — 에이전트/스킬 프롬프트 길이 감사

2026-04-12 원칙: 150줄 초과하면 attention 분산 + 토큰 낭비.
지식은 knowledge/ 에 별도로, 프롬프트는 짧게.
"""
import sys
from pathlib import Path

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
LIMIT = 150

def scan(folder: Path, label: str):
    if not folder.exists():
        return []
    violations = []
    for md in folder.rglob("*.md"):
        try:
            lines = md.read_text(encoding="utf-8", errors="ignore").splitlines()
            if len(lines) > LIMIT:
                rel = md.relative_to(ROOT)
                violations.append((str(rel), len(lines)))
        except Exception:
            continue
    return violations


def main():
    print(f"=== 프롬프트 150줄 원칙 위반 감사 ===\n")
    agents = scan(ROOT / ".claude" / "agents", "Agents")
    skills = scan(ROOT / ".claude" / "skills", "Skills")
    commands = scan(ROOT / ".claude" / "commands", "Commands")
    rules = scan(ROOT / ".claude" / "rules", "Rules")

    for label, items in [("Agents", agents), ("Skills", skills), ("Commands", commands), ("Rules", rules)]:
        if items:
            print(f"[{label}] 위반 {len(items)}개:")
            for path, cnt in sorted(items, key=lambda x: -x[1]):
                print(f"  {cnt}줄 — {path}")
            print()
        else:
            print(f"[{label}] OK (전부 150줄 이하)")

    total = len(agents) + len(skills) + len(commands) + len(rules)
    print(f"\n=== 총 위반: {total}개 ===")


if __name__ == "__main__":
    main()
