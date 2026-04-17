"""
audit_hub.py — 모든 감사 통합 + AI 파싱용 로그 + 자동 조치

변경 철학:
- 리안은 리포트 안 본다 → 리포트는 "서연(AI)용 컨텍스트"
- 자동 조치 가능한 건 즉시 실행 (빈 폴더 archive 등)
- 진짜 리안 결정 필요한 것만 `보고사항들.md`에 짧게 (5줄 이내)
- 원본 데이터는 JSONL 로그 (AI가 파싱)

출력:
1. `company/logs/audits.jsonl` — 원본 감사 데이터 (AI용, 파싱 가능)
2. `보고사항들.md` — 조치 필요한 것만 요약
"""
import os
import sys
import re
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# 실패 시 디스코드 자동 알림
sys.path.insert(0, os.path.dirname(__file__))
try:
    from core.notifier import install_crash_notifier
    install_crash_notifier("audit_hub")
except Exception:
    pass  # notifier 임포트 실패해도 감사는 진행

ROOT = Path(__file__).parent.parent
LOGS = ROOT / "company" / "logs"
LOGS.mkdir(parents=True, exist_ok=True)
AUDIT_LOG = LOGS / "audits.jsonl"
REPORT = ROOT / "보고사항들.md"


def log_event(audit: str, data: dict, severity: str = "info"):
    """AI 파싱용 구조화 로그."""
    entry = {
        "ts": datetime.now().isoformat(),
        "audit": audit,
        "severity": severity,
        **data,
    }
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ───────── 감사 모듈 ─────────

def audit_prompts() -> dict:
    """프롬프트 150줄 초과 스캔. 자동 조치 없음 (큰 작업)."""
    violations = []
    for folder in ["agents", "skills", "commands", "rules"]:
        path = ROOT / ".claude" / folder
        if not path.exists():
            continue
        for md in path.rglob("*.md"):
            try:
                lines = md.read_text(encoding="utf-8", errors="ignore").splitlines()
                if len(lines) > 150:
                    violations.append({
                        "path": str(md.relative_to(ROOT)),
                        "lines": len(lines),
                        "category": folder,
                    })
            except Exception:
                pass
    return {"count": len(violations), "items": violations}


def audit_dead_teams() -> dict:
    """company/teams/ 활성 여부. 자동 조치 없음."""
    teams_dir = ROOT / "company" / "teams"
    company = ROOT / "company"
    exclude = {"venv", "__pycache__", ".git", "archive"}
    if not teams_dir.exists():
        return {"count": 0, "items": []}

    dead = []
    for d in teams_dir.iterdir():
        if not d.is_dir() or d.name.startswith("__"):
            continue
        name = d.name
        has_run = any((company / f"run_{v}.py").exists() for v in [name, name.replace("-", "_")])
        has_import = False
        for py in company.rglob("*.py"):
            if any(p in py.parts for p in exclude):
                continue
            if py.parent.name == name:
                continue
            try:
                text = py.read_text(encoding="utf-8", errors="ignore")
                if re.search(rf"(from|import)\s+teams\.{re.escape(name)}", text):
                    has_import = True
                    break
            except Exception:
                pass
        if not has_run and not has_import:
            dead.append({"name": name})
    return {"count": len(dead), "items": dead}


def audit_capabilities_drift() -> dict:
    """CAPABILITIES.md에 등록 안 된 신규 능력."""
    caps = ROOT / ".claude" / "CAPABILITIES.md"
    if not caps.exists():
        return {"count": 0, "items": []}

    text = caps.read_text(encoding="utf-8")
    registered = set(re.findall(r'`([a-zA-Z0-9_\-\.]+)`', text))

    actual = {
        "skills": {p.stem if p.suffix else p.name
                   for p in (ROOT / ".claude" / "skills").iterdir()
                   if p.exists() and not p.name.startswith("_")} if (ROOT / ".claude" / "skills").exists() else set(),
        "tools": {p.stem for p in (ROOT / "company" / "tools").glob("*.py")} |
                 {p.stem for p in (ROOT / "company" / "utils").glob("*.py")},
    }
    missing = []
    for category, items in actual.items():
        for name in items:
            if name.startswith("_"):
                continue
            if name not in text:
                missing.append({"category": category, "name": name})
    return {"count": len(missing), "items": missing}


def audit_report_size() -> dict:
    """보고사항들.md 1000줄 초과 감시. 자동 로테이션."""
    if not REPORT.exists():
        return {"rotated": False, "lines": 0}
    lines = REPORT.read_text(encoding="utf-8", errors="replace").splitlines()
    count = len(lines)
    if count > 1000:
        backup = ROOT / "archive" / f"보고사항_auto_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPORT, backup)
        # 최근 200줄만 유지
        REPORT.write_text("\n".join(lines[-200:]), encoding="utf-8")
        return {"rotated": True, "old_lines": count, "kept": 200, "backup": str(backup.name)}
    return {"rotated": False, "lines": count}


def audit_log_size() -> dict:
    """audits.jsonl 10MB 초과 시 로테이션."""
    if not AUDIT_LOG.exists():
        return {"rotated": False}
    size = AUDIT_LOG.stat().st_size
    if size > 10 * 1024 * 1024:
        backup = AUDIT_LOG.parent / f"audits_{datetime.now().strftime('%Y%m%d')}.jsonl"
        shutil.move(str(AUDIT_LOG), str(backup))
        return {"rotated": True, "backup": str(backup.name), "old_size_mb": round(size / 1024 / 1024, 1)}
    return {"rotated": False, "size_mb": round(size / 1024 / 1024, 2)}


# ───────── 메인 ─────────

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[audit_hub] 시작 {now}")

    results = {
        "prompts": audit_prompts(),
        "dead_teams": audit_dead_teams(),
        "caps_drift": audit_capabilities_drift(),
        "report_size": audit_report_size(),
        "log_size": audit_log_size(),
    }

    for name, data in results.items():
        severity = "warning" if data.get("count", 0) > 0 else "info"
        log_event(name, data, severity)
        print(f"  {name}: {json.dumps(data, ensure_ascii=False)[:120]}")

    # 보고사항들.md — 조치 필요한 것만 짧게
    action_items = []
    if results["prompts"]["count"] > 0:
        action_items.append(f"⚠️ 프롬프트 150줄 초과 {results['prompts']['count']}개 — 필요시 `audit_prompt_length.py`")
    if results["dead_teams"]["count"] > 0:
        action_items.append(f"❌ 죽은 팀 {results['dead_teams']['count']}개 — `audit_dead_teams.py` 확인")
    if results["caps_drift"]["count"] > 0:
        action_items.append(f"🔔 CAPABILITIES 미등록 {results['caps_drift']['count']}개 — `capability_audit.py` 확인")
    if results["report_size"].get("rotated"):
        action_items.append(f"♻️ 보고사항들.md 자동 로테이션: {results['report_size']['old_lines']}→200줄")

    if action_items:
        summary = f"\n---\n## 🤖 audit_hub — {now}\n" + "\n".join(f"- {x}" for x in action_items) + "\n"
        with open(REPORT, "a", encoding="utf-8") as f:
            f.write(summary)

    print(f"[audit_hub] 완료 — 로그: {AUDIT_LOG.relative_to(ROOT)}")
    print(f"  조치 필요 {len(action_items)}건")


if __name__ == "__main__":
    main()
