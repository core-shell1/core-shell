"""
지호B — 팀 운영 참모 (신버전 시각)
Claude Sonnet 사용

역할: COO 시각에서 현재 운영 중인 팀들의 중복·빠진 역할·개선 필요 포인트 찾기
읽는 것: lian_company/teams/*/status.json, mission.md, company_context.md, PROCESSES.md

사용법:
  python watchdog_b.py
"""
import sys
import os
import io
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent          # lian_company/
REPO_ROOT = ROOT.parent               # core-shell/
TEAMS_DIR = ROOT / "teams"
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

import anthropic
from core.models import CLAUDE_SONNET

JIHO_B_PROMPT = """너는 지호야. 리안 컴퍼니의 참모(Chief of Staff)야. (지호B — 팀 운영 시각)

리안은 여러 팀을 동시에 운영하는 CEO야.
네 역할: 팀 운영 레벨에서 "중복되는 업무", "빠진 역할", "팀 간 시너지" 를 찾아내는 것.

분석 관점:
1. 중복 갭: 두 팀 이상이 같은 업무를 따로 하고 있나? (예: 두 팀이 모두 블로그 작성)
2. 역할 공백: 필요한데 담당 팀/에이전트가 없는 업무가 있나?
3. KPI 경보: 데이터가 쌓이고 있는데 개선이 안 된 팀은?
4. 연계 기회: A팀 산출물을 B팀이 인풋으로 쓰면 효율이 높아지는 경우?

출력 형식:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
지호B 참모 보고서 (팀 운영 시각)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[팀 현황 요약]

⚠️ 중복 업무:
- [팀A]와 [팀B]가 [무엇]을 따로 함 → 통합 제안

🕳️ 역할 공백:
- [무엇]을 하는 팀/에이전트가 없음

📈 KPI 경보:
- [팀명]: [상태]

🔗 연계 기회:
- [팀A] 산출물 → [팀B] 인풋으로 활용 가능

📋 우선순위 액션 (최대 3개):
1. [무엇을, 왜 지금]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
짧고 핵심만."""


def read_file_safe(path: Path, max_chars: int = 1000) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()[:max_chars]
    except Exception:
        return ""


def gather_context() -> str:
    parts = []

    # company_context.md — 회사 DNA
    ctx = read_file_safe(ROOT / "company_context.md", max_chars=1500)
    if ctx:
        parts.append(f"## 회사 컨텍스트\n{ctx}")

    # PROCESSES.md — 핵심 프로세스
    proc = read_file_safe(REPO_ROOT / "PROCESSES.md", max_chars=800)
    if proc:
        parts.append(f"## 핵심 프로세스\n{proc}")

    # 각 팀 status.json + mission.md
    if TEAMS_DIR.exists():
        team_summaries = []
        for team_dir in sorted(TEAMS_DIR.iterdir()):
            if not team_dir.is_dir():
                continue

            summary = f"### 팀: {team_dir.name}\n"

            # mission.md
            mission = read_file_safe(team_dir / "mission.md", max_chars=400)
            if mission:
                summary += f"**미션:**\n{mission}\n"

            # status.json
            status_path = team_dir / "status.json"
            if status_path.exists():
                try:
                    with open(status_path, encoding="utf-8") as f:
                        status = json.load(f)
                    kpi = status.get("kpi", {})
                    data_count = status.get("data_count", 0)
                    version = status.get("current_version", "v1")
                    next_action = status.get("next_action", "")
                    summary += f"**KPI:** {kpi}\n"
                    summary += f"**데이터:** {data_count}건 | **버전:** {version}\n"
                    if next_action:
                        summary += f"**다음액션:** {next_action}\n"
                except Exception:
                    pass

            # 에이전트 목록 (파일명으로 파악)
            agents = [f.stem for f in team_dir.glob("*.py")
                      if f.name not in ("pipeline.py", "__init__.py")]
            if agents:
                summary += f"**에이전트:** {', '.join(agents)}\n"

            team_summaries.append(summary)

        if team_summaries:
            parts.append("## 팀별 현황\n" + "\n\n".join(team_summaries))

    # 최근 보고사항들.md
    report = read_file_safe(REPO_ROOT / "보고사항들.md", max_chars=500)
    if report:
        parts.append(f"## 최근 보고사항\n{report}")

    return "\n\n".join(parts) if parts else ""


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ .env에 ANTHROPIC_API_KEY가 없어.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("지호B | 팀 운영 현황 분석 (Claude Sonnet)")
    print("=" * 60)
    print("팀 운영 현황 스캔 중...")

    context = gather_context()
    if not context:
        print("분석할 팀 정보가 없어. lian_company/teams/ 폴더를 확인해줘.")
        return

    client = anthropic.Anthropic(api_key=api_key)
    full_response = ""

    with client.messages.stream(
        model=CLAUDE_SONNET,
        max_tokens=800,
        system=JIHO_B_PROMPT,
        messages=[{"role": "user", "content": f"현재 팀 운영 현황:\n\n{context}"}],
        temperature=0.7,
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            full_response += text

    print("\n")

    # 보고사항들.md에 저장
    try:
        report_path = REPO_ROOT / "보고사항들.md"
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n## 지호B 참모 보고 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n")
            f.write(full_response)
        print(f"보고사항들.md에 저장 완료.")
    except Exception as e:
        print(f"저장 실패: {e}")


if __name__ == "__main__":
    main()
