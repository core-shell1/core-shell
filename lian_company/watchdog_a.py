"""
지호A — 전체 프로젝트 참모 (구버전 시각)
Gemini 2.5 Flash 사용 (무료 티어)

역할: CEO 시각에서 전체 프로젝트의 빠진 것, 겹치는 것, 지금 해야 하는 것 찾기
읽는 것: PROJECTS.md, STATUS.md, team/ 폴더, 보고사항들.md

사용법:
  python watchdog_a.py
"""
import sys
import os
import io
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent          # lian_company/
REPO_ROOT = ROOT.parent               # core-shell/
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from google import genai
from google.genai import types

MODEL = "gemini-2.5-flash"

JIHO_A_PROMPT = """너는 지호야. 리안 컴퍼니의 참모(Chief of Staff)야. (지호A — 프로젝트 전체 시각)

리안은 여러 프로젝트를 동시에 돌리는 CEO야. 바빠서 전체 그림을 놓치는 경우가 많아.
네 역할: 전체 현황을 보고 "빠진 것", "연결 고리", "지금 당장 해야 하는 것"을 찾아내는 것.

분석 관점:
1. 인프라 갭: 홈페이지, SNS, 포트폴리오 등 기본 인프라가 빠져 있나?
2. 연결 갭: 프로젝트 간 시너지를 놓치고 있나?
3. 타이밍 갭: 완성됐는데 홍보 안 한 것, 지금 해야 하는데 미루는 것?
4. 리소스 갭: 같은 일을 두 팀이 따로 하고 있나?

출력 형식:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
지호A 참모 보고서 (프로젝트 전체 시각)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[현황 요약]

🔴 지금 당장 해야 할 것:
1. [항목] — [이유]

🔗 연결하면 시너지:
1. [A]의 [무엇]을 [B]에 활용

💡 리안이 놓치고 있는 것:
[발견]

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

    # PROJECTS.md
    projects = read_file_safe(REPO_ROOT / "PROJECTS.md")
    if projects:
        parts.append(f"## PROJECTS.md\n{projects}")

    # STATUS.md
    status = read_file_safe(REPO_ROOT / "STATUS.md", max_chars=800)
    if status:
        parts.append(f"## STATUS.md (최근)\n{status}")

    # team/ 폴더 (구버전 프로젝트)
    team_dir = REPO_ROOT / "team"
    if team_dir.exists():
        active_projects = []
        for folder in team_dir.iterdir():
            if folder.is_dir() and "[중단]" not in folder.name:
                project_info = f"### {folder.name}\n"
                for fname in ["CLAUDE.md", "PRD.md", "README.md"]:
                    fpath = folder / fname
                    if fpath.exists():
                        project_info += read_file_safe(fpath, max_chars=300)
                        break
                active_projects.append(project_info)
        if active_projects:
            parts.append("## 진행중 프로젝트 (team/)\n" + "\n\n".join(active_projects))

    # 최근 보고사항들.md
    report = read_file_safe(REPO_ROOT / "보고사항들.md", max_chars=600)
    if report:
        parts.append(f"## 최근 보고사항\n{report}")

    return "\n\n".join(parts) if parts else ""


def main():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ .env에 GOOGLE_API_KEY가 없어. Google AI Studio에서 무료 발급 후 추가해줘.")
        print("   https://aistudio.google.com/app/apikey")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("지호A | 프로젝트 전체 현황 분석 (Gemini Flash — 무료)")
    print("=" * 60)
    print("전체 프로젝트 스캔 중...")

    context = gather_context()
    if not context:
        print("분석할 프로젝트 정보가 없어. PROJECTS.md 또는 STATUS.md가 있어야 해.")
        return

    client = genai.Client(api_key=api_key)
    full_response = ""

    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=f"현재 리안 컴퍼니 전체 현황:\n\n{context}",
        config=types.GenerateContentConfig(
            system_instruction=JIHO_A_PROMPT,
            max_output_tokens=800,
            temperature=0.7,
        ),
    ):
        text = chunk.text or ""
        print(text, end="", flush=True)
        full_response += text

    print("\n")

    # 보고사항들.md에 저장
    try:
        report_path = REPO_ROOT / "보고사항들.md"
        with open(report_path, "a", encoding="utf-8") as f:
            f.write(f"\n\n---\n## 지호A 참모 보고 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n")
            f.write(full_response)
        print(f"보고사항들.md에 저장 완료.")
    except Exception as e:
        print(f"저장 실패: {e}")


if __name__ == "__main__":
    main()
