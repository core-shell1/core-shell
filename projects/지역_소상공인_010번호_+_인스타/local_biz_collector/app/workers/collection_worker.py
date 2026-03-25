"""QThread 기반 수집 워커 — GUI 블로킹 방지"""
import asyncio
import sys

from PyQt6.QtCore import QThread, pyqtSignal

from app.services.collection_service import CollectionService


class CollectionWorker(QThread):
    """백그라운드에서 수집 실행. 메인 스레드 GUI 블로킹 없음."""

    progress = pyqtSignal(str, int)     # 메시지, 퍼센트 (-1 = 업데이트 없음)
    finished = pyqtSignal(int, list)    # session_id, businesses (dict list)
    error    = pyqtSignal(str)

    def __init__(
        self,
        region: str,
        keyword: str,
        platforms: list,
        do_verify: bool = True,
        limit: int = 500,
    ):
        super().__init__()
        self.region     = region
        self.keyword    = keyword
        self.platforms  = platforms
        self.do_verify  = do_verify
        self.limit      = limit
        self._service   = None

    def stop(self):
        if self._service:
            self._service.stop()

    def run(self):
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        def on_progress(msg: str, pct: int):
            self.progress.emit(msg, pct)

        self._service = CollectionService(progress_callback=on_progress)

        try:
            session_id, businesses = asyncio.run(
                self._service.run(
                    region    = self.region,
                    keyword   = self.keyword,
                    platforms = self.platforms,
                    do_verify = self.do_verify,
                    limit     = self.limit,
                )
            )
            self.finished.emit(session_id, businesses)
        except Exception as e:
            self.error.emit(str(e))
