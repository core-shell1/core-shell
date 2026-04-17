"""
Phase 7 message_generator.py 검증 테스트
- _enrich_with_benchmark() 벤치마크 채우기
- 업종별 레이블 매핑
- generate_first_message() — A타입 벤치마크 수치
- generate_second_message() — 블로그 갭 노출
- generate_third_message() — 블로그 갭 노출
- generate_fourth_messages() — 보류/비싸다 벤치마크 수치
- generate_all_messages() — 통합 엔드투엔드
"""
import sys, os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent / "team" / "[진행중] 오프라인 마케팅" / "소상공인_영업툴" / "naver-diagnosis"
sys.path.insert(0, str(PROJECT_ROOT))

from services.message_generator import (
    _enrich_with_benchmark,
    generate_first_message,
    generate_second_message,
    generate_third_message,
    generate_fourth_messages,
    generate_all_messages,
)

# ─────────── helpers ───────────

PASS = 0
FAIL = 0

def check(name: str, condition: bool, detail: str = ""):
    global PASS, FAIL
    if condition:
        print(f"  ✅ {name}")
        PASS += 1
    else:
        print(f"  ❌ {name}" + (f" — {detail}" if detail else ""))
        FAIL += 1

def section(title: str):
    print(f"\n{'─'*50}")
    print(f"  {title}")
    print(f"{'─'*50}")

# ─────────── 기본 데이터 픽스처 ───────────

HAIRIM_DATA = {
    "business_name": "헤어림",
    "category": "미용실",
    "visitor_review_count": 10,
    "receipt_review_count": 5,
    "blog_review_count": 2,
    "photo_count": 8,
    "naver_place_rank": 15,
    "news_last_days": 30,
    "total_score": 35.0,
    "grade": "D",
    "photo_score": 45,
    "review_score": 20,
    "blog_score": 15,
    "info_score": 60,
    "keyword_score": 70,
    "convenience_score": 80,
    "engagement_score": 90,
    "estimated_lost_customers": 30,
    # competitor 필드 없음 → fallback 테스트
}

CAFE_DATA = {
    "business_name": "달빛카페",
    "category": "카페",
    "visitor_review_count": 50,
    "receipt_review_count": 20,
    "blog_review_count": 10,
    "photo_count": 15,
    "naver_place_rank": 5,
    "news_last_days": 20,
    "total_score": 55.0,
    "grade": "C",
    "photo_score": 70,
    "review_score": 40,
    "blog_score": 30,
    "info_score": 80,
    "keyword_score": 75,
    "convenience_score": 85,
    "engagement_score": 90,
    "estimated_lost_customers": 15,
}

UNKNOWN_DATA = {
    "business_name": "테스트집",
    "category": "학습지방문",
    "visitor_review_count": 5,
    "receipt_review_count": 0,
    "blog_review_count": 1,
    "photo_count": 3,
    "grade": "D",
    "total_score": 25.0,
    "estimated_lost_customers": 5,
}


# ─────────── 1. _enrich_with_benchmark ───────────

section("1. _enrich_with_benchmark()")

enriched_hairim = _enrich_with_benchmark(HAIRIM_DATA)

check("미용실 competitor_avg_review = 1451",
      enriched_hairim["competitor_avg_review"] == 1451,
      f"got {enriched_hairim.get('competitor_avg_review')}")

check("미용실 competitor_avg_blog = 370",
      enriched_hairim["competitor_avg_blog"] == 370,
      f"got {enriched_hairim.get('competitor_avg_blog')}")

check("미용실 competitor_avg_photo = 770",
      enriched_hairim["competitor_avg_photo"] == 770,
      f"got {enriched_hairim.get('competitor_avg_photo')}")

check("review_count = visitor + receipt (10+5=15)",
      enriched_hairim["review_count"] == 15,
      f"got {enriched_hairim.get('review_count')}")

check("_industry_label = '서울 상위 미용실'",
      enriched_hairim["_industry_label"] == "서울 상위 미용실",
      f"got {enriched_hairim.get('_industry_label')}")

enriched_cafe = _enrich_with_benchmark(CAFE_DATA)
check("카페 competitor_avg_review = 437",
      enriched_cafe["competitor_avg_review"] == 437,
      f"got {enriched_cafe.get('competitor_avg_review')}")

check("카페 _industry_label = '서울 상위 카페'",
      enriched_cafe["_industry_label"] == "서울 상위 카페",
      f"got {enriched_cafe.get('_industry_label')}")

enriched_unknown = _enrich_with_benchmark(UNKNOWN_DATA)
check("알 수 없는 업종 → _industry_label = '상위 경쟁사'",
      enriched_unknown["_industry_label"] == "상위 경쟁사",
      f"got {enriched_unknown.get('_industry_label')}")


# ─────────── 2. generate_first_message ───────────

section("2. generate_first_message() — 미용실 (no live data)")

first = generate_first_message(HAIRIM_DATA)

check("타입 = A (리뷰격차 3배 이상: 1451 vs 15)",
      first["type"] == "A",
      f"got {first.get('type')}")

check("텍스트에 '1,451' 포함",
      "1,451" in first["text"],
      f"text snippet: {first['text'][:100]}")

check("텍스트에 '서울 상위 미용실' 포함",
      "서울 상위 미용실" in first["text"],
      f"text snippet: {first['text'][:100]}")

check("텍스트에 '15' 포함 (내 리뷰)",
      "15" in first["text"],
      f"text snippet: {first['text'][:100]}")


# ─────────── 3. generate_second_message ───────────

section("3. generate_second_message() — 블로그 갭 노출")

second_hairim = generate_second_message(HAIRIM_DATA)

check("2차 메시지에 '1,451' 포함 (리뷰 벤치마크)",
      "1,451" in second_hairim,
      f"text: {second_hairim[:200]}")

check("2차 메시지에 '블로그 리뷰' 포함 (미용실 = 블로그 핵심)",
      "블로그 리뷰" in second_hairim,
      f"text: {second_hairim[:300]}")

check("2차 메시지에 '370' 포함 (avg_blog)",
      "370" in second_hairim,
      f"text: {second_hairim[:300]}")

# 카페: 블로그 리뷰 10건 < 298건 → 블로그 갭 나와야 함
second_cafe = generate_second_message(CAFE_DATA)
check("카페 2차 메시지에 블로그 갭 포함",
      "블로그 리뷰" in second_cafe,
      f"text: {second_cafe[:300]}")


# ─────────── 4. generate_third_message ───────────

section("4. generate_third_message() — 블로그 갭 노출")

third_hairim = generate_third_message(HAIRIM_DATA)

check("3차 메시지에 '1,451' 포함",
      "1,451" in third_hairim,
      f"text: {third_hairim[:200]}")

check("3차 메시지에 '블로그 리뷰' 포함",
      "블로그 리뷰" in third_hairim,
      f"text: {third_hairim[:300]}")

check("3차 메시지에 '서울 상위 미용실' 포함",
      "서울 상위 미용실" in third_hairim,
      f"text: {third_hairim[:300]}")


# ─────────── 5. generate_fourth_messages ───────────

section("5. generate_fourth_messages() — 보류/비싸다 벤치마크")

fourth = generate_fourth_messages(HAIRIM_DATA)

check("보류 메시지에 '1,451' 포함",
      "1,451" in fourth["보류"],
      f"text: {fourth['보류'][:200]}")

check("보류 메시지에 '서울 상위 미용실' 포함",
      "서울 상위 미용실" in fourth["보류"],
      f"text: {fourth['보류'][:200]}")

check("비싸다 메시지에 '1,451' 포함 (손실 > 패키지비 케이스)",
      "1,451" in fourth["비싸다"],
      f"text: {fourth['비싸다'][:200]}")

check("무응답 메시지 있음",
      len(fourth["무응답"]) > 20,
      f"text: {fourth['무응답'][:50]}")

check("직접 메시지 있음",
      len(fourth["직접"]) > 20,
      f"text: {fourth['직접'][:50]}")


# ─────────── 6. generate_all_messages ───────────

section("6. generate_all_messages() — 통합 테스트")

all_msgs = generate_all_messages(HAIRIM_DATA)

check("first 키 있음", "first" in all_msgs)
check("second 키 있음", "second" in all_msgs)
check("third 키 있음", "third" in all_msgs)
check("fourth 키 있음", "fourth" in all_msgs)
check("fifth 키 있음", "fifth" in all_msgs)
check("recommended_package 있음", "recommended_package" in all_msgs)

check("first.type = A",
      all_msgs["first"]["type"] == "A",
      f"got {all_msgs['first'].get('type')}")

check("fourth에 5개 상황 포함",
      set(all_msgs["fourth"].keys()) == {"보류", "무응답", "비싸다", "직접", "경험있음"},
      f"got {set(all_msgs['fourth'].keys())}")

# 에러 없이 문자열 반환되는지 확인
check("second가 비어있지 않음", len(all_msgs["second"]) > 50)
check("third가 비어있지 않음", len(all_msgs["third"]) > 50)
check("fifth가 비어있지 않음", len(all_msgs["fifth"]) > 50)


# ─────────── 7. 엣지케이스 ───────────

section("7. 엣지케이스")

# 리뷰 0개 업체
zero_review_data = dict(HAIRIM_DATA)
zero_review_data["visitor_review_count"] = 0
zero_review_data["receipt_review_count"] = 0
all_zero = generate_all_messages(zero_review_data)
check("리뷰 0개 업체도 오류 없이 생성",
      all_zero["first"]["type"] != "오류",
      f"got type={all_zero['first']['type']}")

# 경쟁사 데이터 이미 있을 때 덮어쓰지 않아야 함
has_live_data = dict(HAIRIM_DATA)
has_live_data["competitor_avg_review"] = 999
enriched_live = _enrich_with_benchmark(has_live_data)
check("live 데이터 있으면 fallback으로 덮어쓰지 않음 (999 유지)",
      enriched_live["competitor_avg_review"] == 999,
      f"got {enriched_live.get('competitor_avg_review')}")

# review_count 이미 있을 때 재계산하지 않아야 함
has_review_count = dict(HAIRIM_DATA)
has_review_count["review_count"] = 100
enriched_rc = _enrich_with_benchmark(has_review_count)
check("review_count 이미 있으면 재계산 안 함 (100 유지)",
      enriched_rc["review_count"] == 100,
      f"got {enriched_rc.get('review_count')}")


# ─────────── 결과 ───────────

print(f"\n{'='*50}")
print(f"  결과: {PASS}개 통과 / {FAIL}개 실패")
if FAIL == 0:
    print("  모두 통과 ✅")
else:
    print("  실패 항목 있음 ❌")
print(f"{'='*50}\n")
