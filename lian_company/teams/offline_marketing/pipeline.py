import os
import json
import anthropic
from datetime import datetime
from dotenv import load_dotenv
from teams.offline_marketing import researcher, strategist, copywriter, validator

load_dotenv()

TEAM_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "team", "[진행중] 오프라인 마케팅", "소상공인_영업툴")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def get_client() -> anthropic.Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(".env에 ANTHROPIC_API_KEY 없음")
    return anthropic.Anthropic(api_key=api_key)


def save(filename: str, content: str):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n💾 저장: {path}")


def _read_current_state() -> dict:
    """현재 팀 산출물 + 피드백 전부 읽어서 상태 파악."""
    state = {}
    files = {
        "스크립트": "영업_스크립트_v2.md",
        "전략": "영업_전략_재설계.md",
        "검증": "영업_사업검증.md",
        "실전가이드": "영업_실전가이드_최종.md",
        "퍼널": "영업_퍼널_설계.md",
        "플레이북": "영업_플레이북.md",
    }
    for key, fname in files.items():
        path = os.path.join(OUTPUT_DIR, fname)
        try:
            with open(path, encoding="utf-8") as f:
                content = f.read()
            state[key] = {"exists": True, "preview": content[:500], "size": len(content)}
        except Exception:
            state[key] = {"exists": False}

    # 피드백 파일 확인
    feedback_path = os.path.join(OUTPUT_DIR, "_feedback.json")
    try:
        with open(feedback_path, encoding="utf-8") as f:
            state["feedback"] = json.load(f)
    except Exception:
        state["feedback"] = {}

    return state


def _self_assess(client, state: dict, mission: str) -> dict:
    """팀이 스스로 현재 상태 진단 → 이번 실행에서 뭘 집중할지 결정."""
    existing = [k for k, v in state.items() if isinstance(v, dict) and v.get("exists")]
    missing = [k for k, v in state.items() if isinstance(v, dict) and not v.get("exists") and k != "feedback"]
    feedback_text = str(state.get("feedback", {}))

    prompt = f"""너는 오프라인 마케팅팀 팀장이야.

=== 팀 미션 ===
{mission}

=== 현재 산출물 상태 ===
있는 것: {existing}
없는 것: {missing}

=== 최근 피드백 ===
{feedback_text if feedback_text != '{}' else '피드백 없음 (첫 실행 또는 아직 없음)'}

=== 지시 ===
지금 우리 팀이 가장 임팩트 있는 결과를 내려면 이번에 뭘 집중해야 하는지 판단해라.

반환 형식 (JSON만):
{{
  "assessment": "현재 상태 한 줄 요약",
  "priority": "이번 실행 최우선 과제 (research/strategy/copy/validation/full 중 하나)",
  "reason": "왜 이게 우선인지",
  "focus": "이번 실행에서 특히 집중할 포인트 (구체적으로)"
}}"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    text = response.content[0].text.strip()
    # JSON 파싱
    if "```" in text:
        text = text.split("```")[1].replace("json", "").strip()
    try:
        return json.loads(text)
    except Exception:
        return {"assessment": "판단 실패", "priority": "full", "reason": "자동 판단 불가", "focus": "전체 실행"}


def run(industry: str = "소상공인 네이버 플레이스 마케팅 대행"):
    client = get_client()
    context = {"industry": industry}

    print(f"\n{'='*60}")
    print(f"🏢 오프라인 마케팅 팀 가동")
    print(f"대상: {industry}")
    print(f"{'='*60}")

    # 현재 영업 자료 로드 (개선 참고용)
    try:
        with open(os.path.join(OUTPUT_DIR, "영업_스크립트.md"), encoding="utf-8") as f:
            context["current_materials"] = f.read()
    except Exception:
        context["current_materials"] = ""

    # Step 1: 리서처 — 영업 전문가 자료 방대 수집
    print("\n[1/3] 영업 전문가 자료 수집...")
    research = researcher.run(context)
    context["research"] = research
    save("_research_영업전문가자료.md", research)

    # Step 2: 전략가 — 영업 전략 재설계
    print("\n[2/3] 영업 전략 재설계...")
    strategy = strategist.run(context, client)
    context["strategy"] = strategy
    save("영업_전략_재설계.md", strategy)

    # Step 3: 카피라이터 — 스크립트 + PPT 생성
    print("\n[3/4] 스크립트 + PPT 카피 생성...")
    copy = copywriter.run(context, client)
    context["copy"] = copy
    save("영업_스크립트_v2.md", copy)

    # Step 4: 검증자 — 현장 관점 사업 검증 (Claude Opus)
    print("\n[4/4] 현장 관점 사업 검증...")
    validation = validator.run(context, client)
    context["validation"] = validation
    save("영업_사업검증.md", validation)

    # 보고사항들.md 업데이트
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from knowledge.manager import write_report, save_team_result, collect_feedback

        # 결과물 지식으로 저장
        save_team_result("offline_marketing", "_research_영업전문가자료.md", research,
                         tags=["영업", "SPIN", "Challenger", "클로징", "소상공인"])
        save_team_result("offline_marketing", "영업_전략_재설계.md", strategy,
                         tags=["영업", "전략", "퍼널", "소상공인"])
        save_team_result("offline_marketing", "영업_스크립트_v2.md", copy,
                         tags=["영업", "DM", "스크립트", "카피"])

        # 보고
        report_content = (
            f"**{industry}** 영업 자료 완성.\n\n"
            f"- 재원: 영업 전문가 자료 수집 완료\n"
            f"- 승현: 영업 전략 재설계 완료 (운영 7개 항목 포함)\n"
            f"- 예진: DM 스크립트 + PPT 카피 완성\n"
            f"- 검증자: 현장 관점 사업 검증 완료\n\n"
            f"저장 위치: `{OUTPUT_DIR}`\n\n"
            f"리안, **영업_사업검증.md 먼저 봐줘.** "
            f"영업 시작 전에 고쳐야 할 것들 정리되어 있어."
        )
        write_report("재원/승현/예진/검증자", "오프라인 마케팅팀", report_content)

        # 피드백 수집
        collect_feedback("offline_marketing")
    except Exception as e:
        print(f"\n보고/저장 실패: {e}")

    print(f"\n{'='*60}")
    print("✅ 오프라인 마케팅 팀 완료")
    print(f"저장 위치: {OUTPUT_DIR}")
    print(f"{'='*60}")

    return context
