import os
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.models import SONAR_PRO

MODEL = SONAR_PRO

# 온라인 마케팅 기반 지식 쿼리
BASE_QUERIES = [
    "한국 소상공인 온라인 마케팅 대행 서비스 종류 상품 구성 네이버 블로그 인스타 유튜브 퍼포먼스 광고 2025",
    "온라인 마케팅 대행사 고객 유치 방법 인스타그램 DM 유튜브 댓글 블로그 잠재고객 발굴 한국 2025",
    "소상공인 온라인 마케팅 대행 월 단가 가격 블로그 포스팅 SNS 운영 퍼포먼스 광고 패키지",
    "네이버 파워링크 GFA 카카오모먼트 메타 구글 광고 소상공인 대행 수수료 구조 2025",
    "스마트스토어 쿠팡 위탁판매 운영 대행 소상공인 온라인 판로 서비스 단가",
    "인스타그램 릴스 유튜브 쇼츠 콘텐츠 제작 대행 소상공인 가격 패키지 한국",
    "온라인 마케팅 대행 계약 따는 법 무료 진단 제안서 미팅 클로징 성공 사례",
    "소상공인 온라인 마케팅 Pain Point 불만 대행사 선택 기준 왜 안 쓰는지 이유",
    "한국 온라인 마케팅 대행사 경쟁 구도 차별화 전략 소규모 대행사 생존법 2025",
    "퍼포먼스 마케팅 ROI 측정 소상공인 전환율 광고비 대비 효과 설득 방법",
    "콜드 DM 온라인 영업 응답률 높이는 첫 문장 한국 소상공인 대상 2025",
    "온라인 마케팅 패키지 상품 설계 소상공인 가격 저항 낮추는 구성 방법",
]


def _query_single(perplexity: OpenAI, query: str) -> str:
    try:
        resp = perplexity.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "온라인 마케팅 전문 리서처야. 한국 소상공인 대상 온라인 마케팅 대행 시장을 조사해. 실전에서 바로 쓸 수 있는 수치, 사례, 가격 위주로. 이론 최소화.",
                },
                {
                    "role": "user",
                    "content": f"다음 주제 핵심만 조사해줘:\n\n{query}",
                },
            ],
            max_tokens=800,
        )
        return f"### {query}\n\n{resp.choices[0].message.content}\n"
    except Exception as e:
        return f"### {query}\n\n조사 실패: {e}\n"


def run(context: dict, client=None) -> str:
    print("\n" + "=" * 60)
    print("🔍 재원 | 온라인 마케팅 시장 조사 (Perplexity)")
    print("=" * 60)

    industry = context.get("industry", "소상공인 온라인 마케팅 대행")

    perplexity = OpenAI(
        api_key=os.getenv("PERPLEXITY_API_KEY"),
        base_url="https://api.perplexity.ai",
        timeout=120.0,
    )

    # 업종별 추가 쿼리
    industry_queries = [
        f"{industry} 온라인 마케팅 현황 Pain Point 어떤 채널 쓰는지 광고 효과 2025",
        f"{industry} 온라인 마케팅 대행 계약 성공 사례 거절 이유 극복 방법",
        f"{industry} 소상공인 SNS 사용 현황 인스타 유튜브 네이버 블로그 활용도",
    ]
    all_queries = BASE_QUERIES + industry_queries

    print(f"총 {len(all_queries)}개 쿼리 병렬 수집 중...")

    results = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_query = {
            executor.submit(_query_single, perplexity, q): q for q in all_queries
        }
        for i, future in enumerate(as_completed(future_to_query), 1):
            q = future_to_query[future]
            result = future.result()
            results[q] = result
            print(f"  [{i}/{len(all_queries)}] 완료: {q[:40]}...")

    full_report = f"# 온라인 마케팅 시장 조사 보고서\n\n대상 업종: {industry}\n\n"
    for q in all_queries:
        full_report += results.get(q, "") + "\n"

    print("\n✅ 자료 수집 완료")
    return full_report
