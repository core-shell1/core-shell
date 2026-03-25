"""
crawlers/place_crawler.py — 네이버 플레이스 홈 크롤링
기존 process.py의 검증된 로직 유지 + 신규 항목 추가
"""
import sys
import os
import re
import random
from dataclasses import dataclass, field
from typing import List, Optional

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import USER_AGENTS, OUTPUT_DIR, log


@dataclass
class PlaceData:
    place_id: str = ""
    name: str = ""
    category: str = ""
    address: str = ""
    phone: str = ""
    # 콘텐츠
    photo_count: int = 0
    keywords: List[str] = field(default_factory=list)
    # 리뷰
    visitor_review_count: int = 0
    blog_review_count: int = 0
    receipt_review_count: int = 0
    save_count: int = 0
    owner_reply_rate: float = 0.0
    # 기본정보 여부
    has_hours: bool = False
    has_menu: bool = False
    has_intro: bool = False
    has_price: bool = False
    # 기능 연동
    has_reservation: bool = False
    has_talktalk: bool = False
    has_smartcall: bool = False
    has_coupon: bool = False
    has_news: bool = False
    has_hashtag: bool = False
    has_naver_pay: bool = False
    # 외부 채널
    has_instagram: bool = False
    has_kakao: bool = False
    # 새소식
    news_last_days: int = 9999  # 마지막 새소식으로부터 경과 일수
    news_count_monthly: int = 0


def _default_place_data(place_id: str) -> PlaceData:
    """크롤링 실패 시 반환할 기본값"""
    return PlaceData(place_id=place_id)


async def _crawl_photos(context, place_id: str) -> int:
    """사진 수 크롤링 (검증된 SasImage 패턴 유지)"""
    for photo_url in [
        f"https://m.place.naver.com/restaurant/{place_id}/photo",
        f"https://m.place.naver.com/place/{place_id}/photo",
    ]:
        page = None
        try:
            page = await context.new_page()
            await page.goto(photo_url, timeout=25000)
            await page.wait_for_load_state("networkidle", timeout=20000)
            photo_html = await page.content()

            m1 = re.findall(r'SasImage[^}]*total["\s:]+(\d+)', photo_html)
            if m1:
                return max(int(v) for v in m1)

            m2 = re.findall(
                r'"relation"\s*:\s*"[^"]*사진[^"]*"[^}]*"total"\s*:\s*(\d+)',
                photo_html
            )
            if m2:
                return max(int(v) for v in m2)
        except Exception:
            pass
        finally:
            if page:
                try:
                    await page.close()
                except Exception:
                    pass

    return 0


async def _crawl_save_count(content: str, text: str) -> int:
    """저장 수 추출"""
    # JSON 필드 우선
    m = re.search(r'"(?:saveCount|bookmarkCount)"\s*:\s*(\d+)', content)
    if m:
        return int(m.group(1))
    # 텍스트 패턴
    m2 = re.search(r'저장\s*([\d,]+)', text)
    if m2:
        return int(m2.group(1).replace(",", ""))
    m3 = re.search(r'북마크\s*([\d,]+)', text)
    if m3:
        return int(m3.group(1).replace(",", ""))
    return 0


async def _crawl_keywords(page, context, place_id: str, content: str) -> List[str]:
    """키워드 추출 (기존 검증된 로직 유지)"""
    frames_html = content
    try:
        for frame in page.frames:
            try:
                fc = await frame.content()
                frames_html += fc
            except Exception:
                pass
    except Exception:
        pass

    kw_matches = re.findall(r'"keywordList"\s*:\s*\[([^\]]+)\]', frames_html)
    if kw_matches:
        keywords = re.findall(r'"([^"]{2,20})"', kw_matches[0])
        if keywords:
            return keywords[:10]

    # 데스크톱 버전에서 재시도
    page2 = None
    try:
        dk_url = f"https://place.map.naver.com/place/{place_id}/home"
        page2 = await context.new_page()
        await page2.goto(dk_url, timeout=20000)
        await page2.wait_for_load_state("networkidle", timeout=15000)
        dk_html = await page2.content()
        for frame in page2.frames:
            try:
                dk_html += await frame.content()
            except Exception:
                pass
        kw2 = re.findall(r'"keywordList"\s*:\s*\[([^\]]+)\]', dk_html)
        if kw2:
            keywords2 = re.findall(r'"([^"]{2,20})"', kw2[0])
            return keywords2[:10]
    except Exception:
        pass
    finally:
        if page2:
            try:
                await page2.close()
            except Exception:
                pass

    return []


async def _crawl_owner_reply_rate(context, place_id: str) -> float:
    """사장님 답글 응답률 추정 (최근 리뷰 샘플 기준)"""
    page = None
    context2 = None
    try:
        context2 = await _new_context_from(context)
        page = await context2.new_page()
        review_url = f"https://m.place.naver.com/place/{place_id}/review/visitor"
        await page.goto(review_url, timeout=20000)
        await page.wait_for_load_state("networkidle", timeout=15000)
        text = await page.inner_text("body")

        # 사장님 답글이 있는 블록 카운트
        reply_count = len(re.findall(r'사장님\s*(?:답글|답변|댓글)', text))
        # 전체 리뷰 블록 추정 (별점 패턴)
        total_blocks = len(re.findall(r'[\u2605\u2606]{1,5}', text))
        total_blocks = max(total_blocks, 1)
        rate = min(reply_count / total_blocks, 1.0)
        return round(rate, 2)
    except Exception:
        return 0.0
    finally:
        if page:
            try:
                await page.close()
            except Exception:
                pass
        if context2:
            try:
                await context2.close()
            except Exception:
                pass


async def _new_context_from(browser_or_context):
    """브라우저 또는 컨텍스트에서 새 컨텍스트 생성 (브라우저 직접 전달 권장)"""
    # browser 객체를 직접 받을 수 없으므로 전달받은 context의 browser 속성 사용
    try:
        browser = browser_or_context.browser
        return await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 390, "height": 844},
            locale="ko-KR",
        )
    except Exception:
        return browser_or_context


async def _crawl_news_info(context, place_id: str):
    """새소식 마지막 업데이트 경과 일수 및 월 포스팅 수 추정"""
    page = None
    context2 = None
    try:
        try:
            browser = context.browser
            context2 = await browser.new_context(
                user_agent=random.choice(USER_AGENTS),
                viewport={"width": 390, "height": 844},
                locale="ko-KR",
            )
        except Exception:
            context2 = None

        target_ctx = context2 if context2 else context
        page = await target_ctx.new_page()

        for feed_url in [
            f"https://m.place.naver.com/place/{place_id}/feed",
            f"https://m.place.naver.com/restaurant/{place_id}/feed",
        ]:
            try:
                await page.goto(feed_url, timeout=20000)
                await page.wait_for_load_state("networkidle", timeout=15000)
                feed_text = await page.inner_text("body")

                # 절대 날짜 패턴 (2024.12.01 형식)
                date_matches = re.findall(r'(\d{4})\.(\d{1,2})\.(\d{1,2})', feed_text)
                if date_matches:
                    from datetime import date
                    today = date.today()
                    dates = []
                    for y, mo, d in date_matches[:5]:
                        try:
                            dt = date(int(y), int(mo), int(d))
                            dates.append(dt)
                        except Exception:
                            pass
                    if dates:
                        dates.sort(reverse=True)
                        last_days = (today - dates[0]).days
                        # 월 포스팅 수 추정: 최근 3개 날짜 간격으로 계산
                        monthly = 0
                        if len(dates) >= 2:
                            span = (dates[0] - dates[-1]).days or 1
                            monthly = int(len(dates) / max(span / 30, 1))
                        return last_days, max(monthly, 1 if dates else 0)

                # 상대 날짜 패턴 (N일 전, N시간 전)
                relative = re.findall(r'(\d+)일 전', feed_text)
                if relative:
                    return int(relative[0]), 0

                break
            except Exception:
                continue

    except Exception:
        pass
    finally:
        if page:
            try:
                await page.close()
            except Exception:
                pass
        if context2:
            try:
                await context2.close()
            except Exception:
                pass

    return 9999, 0


async def crawl_place(browser, place_id: str) -> PlaceData:
    """네이버 플레이스 홈 크롤링 — 모든 데이터 수집"""
    url = f"https://m.place.naver.com/place/{place_id}/home"
    data = _default_place_data(place_id)

    context = None
    page = None
    try:
        context = await browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={"width": 390, "height": 844},
            locale="ko-KR",
        )
        page = await context.new_page()
        log("Crawl", f"시작: {url}")
        await page.goto(url, timeout=30000)
        await page.wait_for_load_state("networkidle", timeout=30000)

        text = await page.inner_text("body")
        content = await page.content()

        # ── 기본 정보 추출 (JSON 패턴) ──────────────────
        name_m = re.search(r'"name"\s*:\s*"([^"]+)"', content)
        if name_m:
            data.name = name_m.group(1)

        addr_m = re.search(r'"roadAddress"\s*:\s*"([^"]+)"', content)
        if not addr_m:
            addr_m = re.search(r'"address"\s*:\s*"([^"]+)"', content)
        if addr_m:
            data.address = addr_m.group(1)

        phone_m = re.search(r'"phone"\s*:\s*"([0-9\-]+)"', content)
        if phone_m:
            data.phone = phone_m.group(1)

        cat_m = re.search(r'"category"\s*:\s*"([^"]+)"', content)
        if cat_m:
            data.category = cat_m.group(1)

        # ── 사진 수 (검증된 SasImage 패턴) ─────────────
        data.photo_count = await _crawl_photos(context, place_id)

        # ── 리뷰 수 ─────────────────────────────────────
        rv = re.search(r"방문자 리뷰\s*([\d,]+)", text)
        if rv:
            data.visitor_review_count = int(rv.group(1).replace(",", ""))

        rv2 = re.search(r"블로그 리뷰\s*([\d,]+)", text)
        if rv2:
            data.blog_review_count = int(rv2.group(1).replace(",", ""))

        rv3 = re.search(r"영수증 리뷰\s*([\d,]+)", text)
        if rv3:
            data.receipt_review_count = int(rv3.group(1).replace(",", ""))

        # ── 저장 수 ─────────────────────────────────────
        data.save_count = await _crawl_save_count(content, text)

        # ── 기본정보 여부 ────────────────────────────────
        data.has_hours = any(k in text for k in ["영업", "운영시간", "오전", "오후"])
        data.has_menu = "메뉴" in text
        data.has_intro = any(k in text for k in ["소개", "안내", "정보"])
        data.has_price = "가격" in text or "원" in text

        # ── 기능 연동 (HTML JSON + 텍스트 이중 확인) ────
        data.has_reservation = '"booking"' in content or '"naverBooking"' in content or "예약" in text
        data.has_talktalk = '"talktalk"' in content or '"naverTalkTalk"' in content or "톡톡" in text
        data.has_smartcall = '"smartCall"' in content or '"virtualNumber"' in content or "스마트콜" in text
        data.has_coupon = '"coupon"' in content or any(k in text for k in ["쿠폰", "이벤트", "할인"])
        data.has_news = "새소식" in text or "소식" in text
        data.has_hashtag = bool(re.search(r'#[가-힣a-zA-Z0-9_]+', text)) or "태그" in text
        data.has_naver_pay = '"naverPay"' in content or "네이버페이" in text

        # ── 외부 채널 ────────────────────────────────────
        data.has_instagram = bool(re.search(r'instagram\.com/[a-zA-Z0-9_.]+', content)) or "인스타" in text
        data.has_kakao = bool(re.search(r'pf\.kakao\.com/[a-zA-Z0-9]+', content)) or "카카오톡 채널" in text

        # ── 키워드 추출 (검증된 로직 유지) ──────────────
        data.keywords = await _crawl_keywords(page, context, place_id, content)

        # ── 새소식 날짜 (소식 탭이 있는 경우만) ─────────
        if data.has_news:
            data.news_last_days, data.news_count_monthly = await _crawl_news_info(context, place_id)

        # ── 사장님 답글 응답률 ───────────────────────────
        if data.visitor_review_count > 0:
            data.owner_reply_rate = await _crawl_owner_reply_rate(context, place_id)

        log("Crawl", (
            f"완료 — 사진={data.photo_count}, "
            f"방문자리뷰={data.visitor_review_count}, "
            f"블로그={data.blog_review_count}, "
            f"저장={data.save_count}, "
            f"키워드={data.keywords[:3]}"
        ))

    except Exception as e:
        log("Crawl", f"오류 (기본값 반환): {e}")
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

    return data


async def capture_search_screenshot(browser, keyword: str, output_dir: str) -> str:
    """네이버 플레이스 검색 결과 스크린샷 저장, 파일 경로 반환"""
    import urllib.parse
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
        await page.goto(url, timeout=25000)
        await page.wait_for_load_state("networkidle", timeout=20000)

        import re
        safe_kw = re.sub(r'[\\/:*?"<>|]', "_", keyword)
        path = os.path.join(output_dir, f"{safe_kw}_search.png")
        await page.screenshot(path=path, full_page=False)
        log("Screenshot", f"저장: {path}")
        return path
    except Exception as e:
        log("Screenshot", f"실패: {e}")
        return ""
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
