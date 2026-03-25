"""네이버 API로 양주 지역 업체 수만 세기 (상세 수집 없이)"""
import asyncio
import re
import sys
from typing import Dict, List, Set

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import httpx

REGION = "양주"
NAVER_CLIENT_ID = "o0776HJDmQVO6J9Lez1m"
NAVER_CLIENT_SECRET = "ZXG0lPbgH9"

CATEGORIES = [
    "음식점", "카페", "미용실", "네일샵", "병원", "학원",
    "마트", "헬스장", "세탁소", "꽃집", "약국", "치과",
    "피부과", "노래방", "베이커리", "부동산", "숙박",
    "자동차", "인테리어", "옷가게", "필라테스", "요가",
    "안경원", "펜션", "고깃집", "닭갈비", "횟집", "술집", "편의점",
]


async def fetch(category: str) -> List[Dict]:
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
    }
    all_items = []
    # 네이버 API 최대 display=50, start=1~1000
    for start in range(1, 1000, 50):
        params = {"query": f"{REGION} {category}", "display": 50, "start": start}
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    "https://openapi.naver.com/v1/search/local.json",
                    headers=headers, params=params, timeout=10.0
                )
                resp.raise_for_status()
                data = resp.json()
                items = data.get("items", [])
                if not items:
                    break
                all_items.extend(items)
                total = data.get("total", 0)
                if start + 50 > total:
                    break
        except Exception as e:
            print(f"  [오류] {category} start={start}: {e}")
            break
        await asyncio.sleep(0.2)
    return all_items


async def main():
    print(f"=== {REGION} 네이버 API 업체 수 확인 ===\n")
    seen: Set[str] = set()
    total = 0
    phone_010 = 0

    for cat in CATEGORIES:
        items = await fetch(cat)
        added = 0
        cat_010 = 0
        for item in items:
            name = re.sub(r"<[^>]+>", "", item.get("title", "")).strip()
            if name not in seen:
                seen.add(name)
                added += 1
                tel = item.get("telephone", "")
                if tel.startswith("010"):
                    cat_010 += 1
        total += added
        phone_010 += cat_010
        print(f"  {REGION} {cat:<8}: +{added}개 (010: {cat_010}개)  누적: {total}개")

    print(f"\n=== 결과 ===")
    print(f"총 업체: {total}개 (중복제거)")
    print(f"010 번호: {phone_010}개")


asyncio.run(main())
