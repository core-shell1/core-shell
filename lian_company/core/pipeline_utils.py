"""
pipeline_utils.py — 모든 팀 파이프라인 공통 유틸

이 파일의 함수들을 pipeline.py에서 호출하면:
1. 미션 + 학습자료가 에이전트한테 자동 전달
2. 결과물 자가점검 자동 실행
3. 에이전트 .py 파일은 수정할 필요 없음

사용법 (각 팀 pipeline.py에서):
    from core.pipeline_utils import enrich_context, self_critique_all

    # 에이전트 실행 전
    context = enrich_context(context, team_slug="온라인영업팀")

    # 에이전트 실행 후
    critique = self_critique_all(context, client)
"""
import os
import anthropic
from core.models import CLAUDE_SONNET

TEAMS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "teams")


def enrich_context(context: dict, team_slug: str) -> dict:
    """미션 + 학습자료를 context['task']에 합쳐서 에이전트가 자동으로 읽게 함.

    기존 에이전트 .py의 user_msg = f"업무: {context['task']}..." 이므로,
    task 문자열 자체에 미션과 학습자료를 넣으면 모든 에이전트가 읽음.
    """
    original_task = context.get("task", "")

    # 1. 미션 로드
    team_dir = _find_team_dir(team_slug)
    if team_dir:
        mission_path = os.path.join(team_dir, "mission.md")
        try:
            with open(mission_path, encoding="utf-8") as f:
                mission = f.read()
            context["mission"] = mission
            print(f"📋 미션 로드 완료")
        except FileNotFoundError:
            mission = ""
    else:
        mission = ""

    # 2. 학습 (Perplexity)
    fresh_knowledge = ""
    try:
        from core.continuous_learning import learn_before_run
        fresh_knowledge = learn_before_run(team_slug)
        if fresh_knowledge:
            context["fresh_knowledge"] = fresh_knowledge
    except Exception as e:
        print(f"⚠️ 학습 스킵: {e}")

    # 3. task에 합치기 (에이전트가 자동으로 읽음)
    enriched = original_task
    if mission:
        # 미션에서 핵심만 추출 (존재 이유 + 하는 일 + 절대 금지)
        enriched += f"\n\n=== 팀 미션 (반드시 따를 것) ===\n{mission[:1500]}\n==="
    if fresh_knowledge:
        enriched += f"\n\n=== 최신 학습 자료 (이걸 반영해서 결과물 내라) ===\n{fresh_knowledge[:3000]}\n==="

    context["task"] = enriched
    context["_original_task"] = original_task  # 원본 보존
    return context


def self_critique_all(context: dict, client: anthropic.Anthropic, team_name: str = "") -> dict:
    """모든 팀 공통 자가점검. 결과물을 Sonnet으로 점검 → 이슈 있으면 수정.

    Args:
        context: 파이프라인 결과가 담긴 context dict
        client: Anthropic client
        team_name: 팀 이름 (보고용)

    Returns:
        {"passed": bool, "score": int, "issues": list, "improved": str}
    """
    # 결과물 수집 (에이전트들이 만든 텍스트)
    results = []
    for key, val in context.items():
        if key not in ("task", "_original_task", "interview", "mission", "fresh_knowledge") \
           and isinstance(val, str) and len(val) > 100:
            results.append(f"[{key}]\n{val[:1500]}")

    if not results:
        return {"passed": True, "score": 10, "issues": [], "improved": ""}

    all_results = "\n\n---\n\n".join(results)
    mission = context.get("mission", "")

    critique_prompt = f"""너는 QA 검수관이야. 팀 결과물을 점검하고 점수를 매겨.

=== 팀 미션 ===
{mission[:1000]}

=== 점검 기준 (각 10점 만점) ===
1. **실행 가능성**: 리안이 이걸 받고 바로 실행할 수 있는가? 복붙 가능한가?
2. **설득력**: 고객(타겟)이 이걸 보고 "이거다" 할 것 같은가?
3. **구체성**: 수치, 날짜, 이름, 구체적 행동이 명시돼 있는가?
4. **차별화**: 다른 대행사도 할 수 있는 뻔한 내용인가, 우리만의 관점이 있는가?

=== 결과물 ===
{all_results[:6000]}

=== 출력 ===
각 기준 점수 + 총점(40점 만점) + 이슈 목록.
이슈가 있으면 "이렇게 고쳐라"까지 구체적으로.
점수와 이슈를 이 형식으로 마지막에 반드시 출력:
SCORE: XX/40
ISSUES: [이슈1] | [이슈2] | ...
"""

    print(f"\n{'='*60}")
    print(f"🔍 자가점검 | {team_name}")
    print("="*60)

    full_response = ""
    try:
        with client.messages.stream(
            model=CLAUDE_SONNET,
            max_tokens=1500,
            messages=[{"role": "user", "content": critique_prompt}],
            system="너는 냉정한 QA 검수관이야. 점수 후하게 주지 마. 리안이 직접 했을 때보다 못하면 0점이야.",
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text
        print()
    except Exception as e:
        print(f"\n⚠️ 자가점검 실패: {e}")
        return {"passed": False, "score": 0, "issues": [str(e)], "improved": ""}

    # 점수 파싱
    score = 0
    import re
    score_match = re.search(r'SCORE:\s*(\d+)/40', full_response)
    if score_match:
        score = int(score_match.group(1))

    issues = []
    issues_match = re.search(r'ISSUES:\s*(.+)', full_response)
    if issues_match:
        issues = [i.strip() for i in issues_match.group(1).split('|') if i.strip()]

    passed = score >= 28  # 70% 이상이면 통과

    result = {
        "passed": passed,
        "score": score,
        "issues": issues,
        "full_critique": full_response,
    }

    if passed:
        print(f"\n✅ 자가점검 통과 ({score}/40)")
    else:
        print(f"\n❌ 자가점검 미통과 ({score}/40) — 이슈 {len(issues)}개")

    return result


def _find_team_dir(team_slug: str) -> str | None:
    """팀 디렉토리 찾기."""
    exact = os.path.join(TEAMS_DIR, team_slug)
    if os.path.isdir(exact):
        return exact
    for d in os.listdir(TEAMS_DIR):
        if team_slug.lower() in d.lower():
            path = os.path.join(TEAMS_DIR, d)
            if os.path.isdir(path):
                return path
    return None
