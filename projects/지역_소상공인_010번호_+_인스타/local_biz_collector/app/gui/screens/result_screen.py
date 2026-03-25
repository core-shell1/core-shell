from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QDesktopServices
from PyQt6.QtCore import QUrl

from app.gui.widgets.result_table import ResultTableWidget
from app.services.export_service import to_excel


class ResultScreen(QWidget):
    """결과 미리보기 화면"""

    restart_collection = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_businesses = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 타이틀
        title = QLabel("수집 결과")
        title.setFont(QFont("Malgun Gothic", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1a73e8; margin-bottom: 10px;")
        layout.addWidget(title)

        # 요약 레이블
        self.summary_label = QLabel()
        self.summary_label.setFont(QFont("Malgun Gothic", 12))
        self.summary_label.setStyleSheet("""
            color: #333333;
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
        """)
        layout.addWidget(self.summary_label)

        # 탭 위젯
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QTabBar::tab {
                font-family: 'Malgun Gothic';
                font-size: 12px;
                padding: 10px 20px;
                margin-right: 2px;
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #1a73e8;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #e8e8e8;
            }
        """)

        self.all_table = ResultTableWidget()
        self.confirmed_table = ResultTableWidget()
        self.unconfirmed_table = ResultTableWidget()
        self.closed_table = ResultTableWidget()

        self.tab_widget.addTab(self.all_table, "전체")
        self.tab_widget.addTab(self.confirmed_table, "확인됨")
        self.tab_widget.addTab(self.unconfirmed_table, "미확인")
        self.tab_widget.addTab(self.closed_table, "폐업의심")

        layout.addWidget(self.tab_widget)

        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.export_button = QPushButton("엑셀 내보내기")
        self.export_button.setMinimumHeight(45)
        self.export_button.clicked.connect(self._on_export_clicked)
        self.export_button.setStyleSheet("""
            QPushButton {
                font-family: 'Malgun Gothic';
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: #34a853;
                border: none;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2d8e47;
            }
            QPushButton:pressed {
                background-color: #1e7a35;
            }
        """)
        button_layout.addWidget(self.export_button)

        self.restart_button = QPushButton("다시 수집")
        self.restart_button.setMinimumHeight(45)
        self.restart_button.clicked.connect(self.restart_collection.emit)
        self.restart_button.setStyleSheet("""
            QPushButton {
                font-family: 'Malgun Gothic';
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: #1a73e8;
                border: none;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        button_layout.addWidget(self.restart_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_businesses(self, businesses: list[dict]):
        """업체 데이터 로드"""
        self.current_businesses = businesses

        # 전체 탭
        self.all_table.load_businesses(businesses)

        # 검증 상태별 분류
        confirmed = [b for b in businesses if b.get("verify_status") == "확인됨"]
        unconfirmed = [b for b in businesses if b.get("verify_status") == "미확인"]
        closed = [b for b in businesses if b.get("verify_status") == "폐업의심"]

        self.confirmed_table.load_businesses(confirmed)
        self.unconfirmed_table.load_businesses(unconfirmed)
        self.closed_table.load_businesses(closed)

        # 요약 업데이트
        total = len(businesses)
        confirmed_count = len(confirmed)
        unconfirmed_count = len(unconfirmed)
        closed_count = len(closed)

        summary_text = (
            f"<b>전체:</b> {total}건 | "
            f"<b style='color: #34a853;'>확인됨:</b> {confirmed_count}건 | "
            f"<b style='color: #fbbc04;'>미확인:</b> {unconfirmed_count}건 | "
            f"<b style='color: #ea4335;'>폐업의심:</b> {closed_count}건"
        )
        self.summary_label.setText(summary_text)

    def _on_export_clicked(self):
        """엑셀 내보내기 버튼 클릭"""
        if not self.current_businesses:
            QMessageBox.warning(self, "내보내기 실패", "내보낼 데이터가 없습니다.")
            return

        try:
            # 현재 선택된 탭의 데이터 내보내기
            current_index = self.tab_widget.currentIndex()

            if current_index == 0:  # 전체
                businesses_to_export = self.all_table.get_businesses()
            elif current_index == 1:  # 확인됨
                businesses_to_export = self.confirmed_table.get_businesses()
            elif current_index == 2:  # 미확인
                businesses_to_export = self.unconfirmed_table.get_businesses()
            else:  # 폐업의심
                businesses_to_export = self.closed_table.get_businesses()

            if not businesses_to_export:
                QMessageBox.warning(self, "내보내기 실패", "현재 탭에 데이터가 없습니다.")
                return

            filepath = to_excel(businesses_to_export)

            # 파일 열기
            QDesktopServices.openUrl(QUrl.fromLocalFile(filepath))

            QMessageBox.information(
                self,
                "내보내기 완료",
                f"엑셀 파일이 생성되었습니다.\n\n{filepath}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "내보내기 실패",
                f"엑셀 내보내기 중 오류가 발생했습니다.\n\n{str(e)}"
            )
