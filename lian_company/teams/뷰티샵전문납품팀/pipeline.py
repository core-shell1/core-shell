import os
import sys
import anthropic
from dotenv import load_dotenv
from teams.뷰티샵전문납품팀 import 한소율
from teams.뷰티샵전문납품팀 import 박채린
from teams.뷰티샵전문납품팀 import 윤다인
from teams.뷰티샵전문납품팀 import 정하윤
from teams.뷰티샵전문납품팀 import 이서진
from teams.뷰티샵전문납품팀 import 강민재

load_dotenv()

OUTPUT_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "team")


def get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def save(output_dir: str, filename: str, content: str):
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n💾 저장: {path}")


def team_interview(task: str, client: anthropic.Anthropic) -> str:
    """팀 시작 전 리안한테 디테일 인터뷰."""
    print("\n" + "="*60)
    print("🎤 팀 인터뷰 | 리안한테 디테일 파악")
    print("="*60)

    interview_prompt = "너는 뷰티샵전문납품팀의 팀 리더야. 리안(CEO, 비개발자)한테 실제 업무를 파악해야 해. 구체적이고 실용적인 질문 3~5개를 한번에 물어봐. 짧고 친근하게."

    resp = ""
    with client.messages.stream(
        model="claude-sonnet-4-5",
        max_tokens=400,
        system=interview_prompt,
        messages=[{"role": "user", "content": f"업무: {task}"}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            resp += text

    print("\n\n리안: ", end="")
    try:
        answer = input().strip()
    except EOFError:
        answer = ""

    return f"리안 답변:\n{answer}"


def run(task: str = ""):
    client = get_client()
    context = {"task": task}

    print(f"\n{'='*60}")
    print(f"🏢 뷰티샵전문납품팀 가동")
    print(f"업무: {task}")
    print(f"{'='*60}")

    output_dir = os.path.join(OUTPUT_BASE, "뷰티샵전문납품팀")

    # 미션 + 학습 자동 로드 (에이전트한테 자동 전달)
    try:
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from core.pipeline_utils import enrich_context, self_critique_all
        context = enrich_context(context, team_slug="뷰티샵전문납품팀")
    except Exception as e:
        print(f"⚠️ 미션/학습 로드 실패: {e}")

    # 팀 인터뷰 (리안한테 디테일 파악)
    interview = team_interview(task, client)
    context["interview"] = interview
    save(output_dir, "00_팀인터뷰.md", interview)

    print("\n[1/6] 한소율...")
    result_한소율 = 한소율.run(context, client)
    context["한소율"] = result_한소율
    save(output_dir, "한소율_결과.md", result_한소율)

    print("\n[2/6] 박채린...")
    result_박채린 = 박채린.run(context, client)
    context["박채린"] = result_박채린
    save(output_dir, "박채린_결과.md", result_박채린)

    print("\n[3/6] 윤다인...")
    result_윤다인 = 윤다인.run(context, client)
    context["윤다인"] = result_윤다인
    save(output_dir, "윤다인_결과.md", result_윤다인)

    print("\n[4/6] 정하윤...")
    result_정하윤 = 정하윤.run(context, client)
    context["정하윤"] = result_정하윤
    save(output_dir, "정하윤_결과.md", result_정하윤)

    print("\n[5/6] 이서진...")
    result_이서진 = 이서진.run(context, client)
    context["이서진"] = result_이서진
    save(output_dir, "이서진_결과.md", result_이서진)

    print("\n[6/6] 강민재...")
    result_강민재 = 강민재.run(context, client)
    context["강민재"] = result_강민재
    save(output_dir, "강민재_결과.md", result_강민재)


    # 결과물을 지식으로 저장 + 리안 피드백 수집
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        from knowledge.manager import save_team_result, collect_feedback
        for key, val in context.items():
            if key not in ("task", "interview") and isinstance(val, str) and len(val) > 100:
                save_team_result("뷰티샵전문납품팀", f"{key}.md", val)
        collect_feedback("뷰티샵전문납품팀")
    except Exception as e:
        print(f"\n⚠️ 지식 저장/피드백 수집 실패: {e}")

    print(f"\n{'='*60}")
    print("✅ 완료")
    print(f"저장 위치: {output_dir}")
    print(f"{'='*60}")
    return context
