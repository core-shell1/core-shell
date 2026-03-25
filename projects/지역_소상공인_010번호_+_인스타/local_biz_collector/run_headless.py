"""
GUI 없이 수집 실행 — CLI 모드
사용: python run_headless.py [지역] [키워드(선택)]
"""
import asyncio
import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    # ProactorEventLoop: subprocess(Playwright) 지원. SelectorEventLoop은 NotImplementedError
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

from app.models.database import init_db
from app.services.collection_service import CollectionService
from app.services.export_service import to_excel

REGION   = sys.argv[1] if len(sys.argv) > 1 else "포천"
KEYWORD  = sys.argv[2] if len(sys.argv) > 2 else ""
PLATFORMS = ["네이버", "카카오맵", "구글", "덕덕고", "인스타그램"]
# 네이버 = API(빠름), 카카오맵 = Playwright, 구글+덕덕고 = ddgs, 인스타 = 네이버검색
DO_VERIFY = False  # 대량 수집 시 검증 생략 (속도 우선)


def progress(msg: str, pct: int):
    bar = ""
    if pct >= 0:
        filled = int(pct / 5)
        bar = f" [{'█'*filled}{'░'*(20-filled)}] {pct}%"
    print(f"{msg}{bar}", flush=True)


async def main():
    print(f"=== 포천 소상공인 수집 시작 ===")
    print(f"지역: {REGION} | 업종: {KEYWORD or '전체'} | 플랫폼: {', '.join(PLATFORMS)}")
    print()

    init_db()

    service = CollectionService(progress_callback=progress)
    session_id, businesses = await service.run(
        region=REGION,
        keyword=KEYWORD,
        platforms=PLATFORMS,
        do_verify=DO_VERIFY,
        limit=999999,
    )

    if not businesses:
        print("수집된 데이터가 없습니다.")
        return

    # 엑셀 저장
    excel_path = to_excel(businesses)
    print()
    print(f"=== 완료 ===")
    print(f"총 {len(businesses)}건 수집")
    confirmed = sum(1 for b in businesses if b.get("verify_status") == "확인됨")
    print(f"확인됨: {confirmed}건 / 미확인: {len(businesses)-confirmed}건")
    print(f"엑셀 저장: {excel_path}")


asyncio.run(main())
