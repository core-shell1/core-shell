import os
import anthropic
from dotenv import load_dotenv
from teams.뷰티샵전문납품팀 import 한서연
from teams.뷰티샵전문납품팀 import 박도윤
from teams.뷰티샵전문납품팀 import 최예린
from teams.뷰티샵전문납품팀 import 정민호
from teams.뷰티샵전문납품팀 import 윤하은
from teams.뷰티샵전문납품팀 import 강태현
from teams.뷰티샵전문납품팀 import 이수빈

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

    # 팀 인터뷰 (리안한테 디테일 파악)
    interview = team_interview(task, client)
    context["interview"] = interview
    save(output_dir, "00_팀인터뷰.md", interview)

    print("\n[1/7] 한서연...")
    result_한서연 = 한서연.run(context, client)
    context["한서연"] = result_한서연
    save(output_dir, "한서연_결과.md", result_한서연)

    print("\n[2/7] 박도윤...")
    result_박도윤 = 박도윤.run(context, client)
    context["박도윤"] = result_박도윤
    save(output_dir, "박도윤_결과.md", result_박도윤)

    print("\n[3/7] 최예린...")
    result_최예린 = 최예린.run(context, client)
    context["최예린"] = result_최예린
    save(output_dir, "최예린_결과.md", result_최예린)

    print("\n[4/7] 정민호...")
    result_정민호 = 정민호.run(context, client)
    context["정민호"] = result_정민호
    save(output_dir, "정민호_결과.md", result_정민호)

    print("\n[5/7] 윤하은...")
    result_윤하은 = 윤하은.run(context, client)
    context["윤하은"] = result_윤하은
    save(output_dir, "윤하은_결과.md", result_윤하은)

    print("\n[6/7] 강태현...")
    result_강태현 = 강태현.run(context, client)
    context["강태현"] = result_강태현
    save(output_dir, "강태현_결과.md", result_강태현)

    print("\n[7/7] 이수빈...")
    result_이수빈 = 이수빈.run(context, client)
    context["이수빈"] = result_이수빈
    save(output_dir, "이수빈_결과.md", result_이수빈)


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
