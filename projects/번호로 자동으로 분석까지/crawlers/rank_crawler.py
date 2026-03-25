"""
crawlers/rank_crawler.py — 네이버 플레이스 키워드 순위 조회
"""
import sys
import os
import re
import random
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import USER_AGENTS, log


async def get_keyword_rank(browser, keyword: str, business_name: str, place_id: str = "") -> int:
    """
    모바일 네이버 플레이스 검색에서 업체 순위 반환.
    place_id가 있으면 URL 매칭으로 더 정확하게 탐색.
    못 찾으면 0 반환.
    """
    context = None
    page = None
    try:
        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 390, "height": 844},
            locale="ko-KR",
        )
        page = await context.new_page()
        encoded = urllib.parse.quote(keyword)
        url = f"https://m.search.naver.com/search.naver?query={encoded}&where=m_local"
        await page.goto(url, timeout=30000)
        await page.wait_for_load_state("networkidle", timeout=20000)

        content = await page.content()

        # place_id 기반 정확한 순위 탐색
        if place_id:
            place_ids = re.findall(r'place\.naver\.com/\w+/(\d+)', content)
            seen = []
            for pid in place_ids:
                if pid not in seen:
                    seen.append(pid)
            if place_id in seen:
                rank = seen.index(place_id) + 1
                log("Rank", f"'{keyword}' → place_id 매칭 {rank}위")
                return rank

        # 업체명 기반 순위 탐색 (fallback)
        text = await page.inner_text("body")
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        short_name = business_name.split()[0] if " " in business_name else business_name

        for i, line in enumerate(lines):
            if short_name in line:
                place_items = [l for l in lines[:i] if len(l) > 2]
                rank = min(len(place_items) // 3 + 1, 99)
                log("Rank", f"'{keyword}' → '{business_name}' 텍스트 매칭 {rank}위 (줄 {i})")
                return rank

        log("Rank", f"'{keyword}' → '{business_name}' 미발견 (순위 외)")
        return 0

    except Exception as e:
        log("Rank", f"오류: {e}")
        return 0
    finally:
        if page:
            try:
                await page.close()
            except Exception:
                pass
        if context:
            try:
                await context.close()
            except Exception:
                pass
