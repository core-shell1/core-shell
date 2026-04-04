import os
from openai import OpenAI
from core.models import GPT4O
from core.context_loader import inject_context

MODEL = GPT4O


def run(context: dict, client=None) -> str:
    print("\n" + "="*60)
    print("📈 민수 | 전략 수립 (GPT-4o)")
    print("="*60)

    idea = context.get("clarified", context.get("idea", ""))
    market_research = context.get("seoyun", "")

    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system = """너는 민수야. 리안 컴퍼니의 비즈니스 전략가야.

서윤의 시장조사를 바탕으로 전략을 수립해:
1. 포지셔닝 (한 줄 정의)
2. 수익 모델 2~3개 (구체적 금액 포함)
3. 가격 전략 (경쟁사 대비 포지셔닝)
4. 초기 진입 전략 (첫 10명 → 100명 어떻게)
5. 6주 로드맵

출력 형식:
## 포지셔닝
[한 줄]

## 수익 모델
[모델 설명]

## 가격 전략
| 플랜 | 가격 | 포함 내용 |
|------|------|---------|

## 초기 진입 전략
[구체적 액션 3가지 — "내일 당장 할 수 있는 것" 위주]

## 6주 로드맵
[주차별 목표]

## 핵심 가설 (검증 필요)
| 가설 | 검증 방법 | 기간 |
|------|---------|------|

핵심 원칙:
- 이론 금지. "린캔버스에 따르면~" 이런 거 쓰지 마. 바로 실행 가능한 전략만.
- 우리가 이미 가진 자산(회사 컨텍스트 참고)을 최대한 활용해라.
- "좋아요 100개"보다 "결제 1건"이 중요하다. 허영 지표 쓰지 마.
- 만들기 전에 팔아라 (Demo-Sell-Build). 데모로 지불 의사 확인 먼저.
- 초기 10명에게 직접 서비스하고 검증한 후 확장해라.
- 피벗 신호: 핵심 지표 정체, 유료 전환 0, 고객이 다른 문제를 말함.
"""

    content = f"아이디어: {idea}\n\n[서윤의 시장조사]\n{market_research}\n\n전략을 수립해줘."

    full_response = ""
    stream = openai_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": inject_context(system)},
            {"role": "user", "content": content}
        ],
        stream=True,
        temperature=0.7
    )
    for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        print(text, end="", flush=True)
        full_response += text

    print()
    return full_response
