from PyQt6.QtWidgets import (
    QMainWindow, QStackedWidget, QToolBar, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon

from app.gui.screens.input_screen import InputScreen
from app.gui.screens.progress_screen import ProgressScreen
from app.gui.screens.result_screen import ResultScreen
from app.gui.screens.history_screen import HistoryScreen
from app.workers.collection_worker import CollectionWorker
from app.models.database import init_db


class MainWindow(QMainWindow):
    """메인 윈도우"""

    def __init__(self):
        super().__init__()
        self.worker = None
        self._init_db()
        self._init_ui()

    def _init_db(self):
        """데이터베이스 초기화"""
        try:
            init_db()
        except Exception as e:
            QMessageBox.critical(
                self,
                "DB 초기화 실패",
                f"데이터베이스 초기화 중 오류가 발생했습니다.\n\n{str(e)}"
            )

    def _init_ui(self):
        self.setWindowTitle("소상공인 연락처 수집 툴")
        self.setMinimumSize(900, 650)

        # 툴바
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f5f5f5;
                border-bottom: 2px solid #e0e0e0;
                spacing: 10px;
                padding: 5px;
            }
            QToolButton {
                font-family: 'Malgun Gothic';
                font-size: 12px;
                padding: 8px 15px;
                border-radius: 4px;
                background-color: #ffffff;
                border: 1px solid #cccccc;
            }
            QToolButton:hover {
                background-color: #e8e8e8;
            }
        """)

        home_action = QAction("홈", self)
        home_action.triggered.connect(lambda: self._switch_screen(0))
        toolbar.addAction(home_action)

        history_action = QAction("이력 보기", self)
        history_action.triggered.connect(self._show_history)
        toolbar.addAction(history_action)

        self.addToolBar(toolbar)

        # 스택 위젯
        self.stacked_widget = QStackedWidget()

        # 화면 생성
        self.input_screen = InputScreen()
        self.progress_screen = ProgressScreen()
        self.result_screen = ResultScreen()
        self.history_screen = HistoryScreen()

        # 화면 추가
        self.stacked_widget.addWidget(self.input_screen)  # 0
        self.stacked_widget.addWidget(self.progress_screen)  # 1
        self.stacked_widget.addWidget(self.result_screen)  # 2
        self.stacked_widget.addWidget(self.history_screen)  # 3

        self.setCentralWidget(self.stacked_widget)

        # 시그널 연결
        self.input_screen.start_collection.connect(self._start_collection)
        self.input_screen.show_history_detail.connect(self._show_history_detail)
        self.progress_screen.cancel_requested.connect(self._cancel_collection)
        self.result_screen.restart_collection.connect(lambda: self._switch_screen(0))
        self.history_screen.show_result.connect(self._show_result_from_history)
        self.history_screen.restart_with_params.connect(self._restart_with_params)

        # 스타일
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
        """)

    def _switch_screen(self, index: int):
        """화면 전환"""
        self.stacked_widget.setCurrentIndex(index)

    def _start_collection(self, region: str, keyword: str, platforms: list[str], do_verify: bool):
        """수집 시작"""
        self.progress_screen.reset()
        self._switch_screen(1)

        # Worker 생성 및 시작
        self.worker = CollectionWorker(region, keyword, platforms, do_verify)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished.connect(self._on_finished)
        self.worker.error.connect(self._on_error)
        self.worker.start()

    def _on_progress(self, msg: str, pct: int):
        """진행 상황 업데이트"""
        self.progress_screen.update_progress(msg, pct)

    def _on_finished(self, session_id: int, businesses: list[dict]):
        """수집 완료"""
        self.worker = None
        self.progress_screen.set_collected_count(len(businesses))

        if not businesses:
            QMessageBox.information(
                self,
                "수집 완료",
                "수집이 완료되었으나 데이터가 없습니다."
            )
            self._switch_screen(0)
            return

        self.result_screen.load_businesses(businesses)
        self._switch_screen(2)

        # 입력 화면 이력 갱신
        self.input_screen.load_recent_history()

    def _on_error(self, error_msg: str):
        """수집 오류"""
        self.worker = None
        QMessageBox.critical(
            self,
            "수집 오류",
            f"수집 중 오류가 발생했습니다.\n\n{error_msg}"
        )
        self._switch_screen(0)

    def _cancel_collection(self):
        """수집 중단"""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "수집 중단",
                "정말 수집을 중단하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.worker.stop()
                self.worker.wait()
                self.worker = None
                QMessageBox.information(self, "중단됨", "수집이 중단되었습니다.")
                self._switch_screen(0)

    def _show_history(self):
        """이력 화면 표시"""
        self.history_screen.load_history()
        self._switch_screen(3)

    def _show_history_detail(self, session_id: int):
        """이력 상세 보기 (입력 화면에서 호출)"""
        from app.services.history_service import get_session_businesses

        try:
            businesses = get_session_businesses(session_id)
            if businesses:
                self.result_screen.load_businesses(businesses)
                self._switch_screen(2)
            else:
                QMessageBox.information(self, "데이터 없음", "해당 이력에 저장된 데이터가 없습니다.")
        except Exception as e:
            QMessageBox.critical(
                self,
                "데이터 로드 실패",
                f"이력 데이터를 불러오는 중 오류가 발생했습니다.\n\n{str(e)}"
            )

    def _show_result_from_history(self, businesses: list[dict]):
        """이력 화면에서 결과 보기"""
        self.result_screen.load_businesses(businesses)
        self._switch_screen(2)

    def _restart_with_params(self, region: str, keyword: str, platforms: list[str]):
        """이력 화면에서 재수집"""
        self.input_screen.set_input_values(region, keyword, platforms)
        self._switch_screen(0)

    def closeEvent(self, event):
        """윈도우 종료 이벤트"""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self,
                "종료 확인",
                "수집이 진행 중입니다. 정말 종료하시겠습니까?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self.worker.stop()
                self.worker.wait()
                self._kill_playwright_zombies()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    @staticmethod
    def _kill_playwright_zombies():
        """강제 종료 후 남은 Playwright Chromium 프로세스 정리"""
        import subprocess
        import sys
        try:
            if sys.platform == "win32":
                subprocess.run(
                    ["taskkill", "/F", "/IM", "chrome.exe", "/T"],
                    capture_output=True,
                )
        except Exception:
            pass
