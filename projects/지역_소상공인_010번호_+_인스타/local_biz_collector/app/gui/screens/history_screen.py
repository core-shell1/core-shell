from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from app.services.history_service import list_history, get_session_businesses


class HistoryScreen(QWidget):
    """수집 이력 화면"""

    show_result = pyqtSignal(list)  # businesses
    restart_with_params = pyqtSignal(str, str, list)  # region, keyword, platforms

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 타이틀
        title = QLabel("수집 이력")
        title.setFont(QFont("Malgun Gothic", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1a73e8; margin-bottom: 10px;")
        layout.addWidget(title)

        # 이력 테이블
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels([
            "날짜", "지역", "업종", "전체건수", "확인됨", "상태", "ID"
        ])

        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)

        self.history_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.history_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.history_table.setAlternatingRowColors(True)

        self.history_table.setStyleSheet("""
            QTableWidget {
                font-family: 'Malgun Gothic';
                font-size: 12px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: #ffffff;
                gridline-color: #e8e8e8;
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #000000;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #1a73e8;
                font-weight: bold;
                color: #333333;
            }
        """)

        layout.addWidget(self.history_table)

        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.view_button = QPushButton("결과 보기")
        self.view_button.setMinimumHeight(45)
        self.view_button.clicked.connect(self._on_view_clicked)
        self.view_button.setStyleSheet("""
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
        button_layout.addWidget(self.view_button)

        self.restart_button = QPushButton("재수집")
        self.restart_button.setMinimumHeight(45)
        self.restart_button.clicked.connect(self._on_restart_clicked)
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

    def load_history(self):
        """이력 로드"""
        self.history_table.setRowCount(0)

        try:
            sessions = list_history()
            self.history_table.setRowCount(len(sessions))

            for row, session in enumerate(sessions):
                # 날짜
                date_item = QTableWidgetItem(session.get('created_at', ''))
                self.history_table.setItem(row, 0, date_item)

                # 지역
                region_item = QTableWidgetItem(session.get('region', ''))
                self.history_table.setItem(row, 1, region_item)

                # 업종
                keyword_item = QTableWidgetItem(session.get('keyword') or '전체')
                self.history_table.setItem(row, 2, keyword_item)

                # 전체건수
                total_item = QTableWidgetItem(str(session.get('total_count', 0)))
                total_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_table.setItem(row, 3, total_item)

                # 확인됨
                confirmed_item = QTableWidgetItem(str(session.get('confirmed_count', 0)))
                confirmed_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_table.setItem(row, 4, confirmed_item)

                # 상태
                status = session.get('status', 'completed')
                status_text = {
                    'completed': '완료',
                    'in_progress': '진행중',
                    'failed': '실패',
                    'cancelled': '중단'
                }.get(status, status)
                status_item = QTableWidgetItem(status_text)
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_table.setItem(row, 5, status_item)

                # ID (숨김)
                id_item = QTableWidgetItem(str(session.get('id', '')))
                id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_table.setItem(row, 6, id_item)

        except Exception as e:
            QMessageBox.critical(
                self,
                "이력 로드 실패",
                f"수집 이력을 불러오는 중 오류가 발생했습니다.\n\n{str(e)}"
            )

    def _on_view_clicked(self):
        """결과 보기 버튼 클릭"""
        selected_rows = self.history_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "선택 오류", "결과를 볼 이력을 선택해주세요.")
            return

        row = selected_rows[0].row()
        session_id_item = self.history_table.item(row, 6)

        if not session_id_item:
            return

        try:
            session_id = int(session_id_item.text())
            businesses = get_session_businesses(session_id)

            if not businesses:
                QMessageBox.information(self, "데이터 없음", "해당 세션에 저장된 데이터가 없습니다.")
                return

            self.show_result.emit(businesses)

        except Exception as e:
            QMessageBox.critical(
                self,
                "결과 로드 실패",
                f"수집 결과를 불러오는 중 오류가 발생했습니다.\n\n{str(e)}"
            )

    def _on_restart_clicked(self):
        """재수집 버튼 클릭"""
        selected_rows = self.history_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "선택 오류", "재수집할 이력을 선택해주세요.")
            return

        row = selected_rows[0].row()

        region = self.history_table.item(row, 1).text()
        keyword = self.history_table.item(row, 2).text()
        if keyword == '전체':
            keyword = ''

        # 플랫폼 정보는 DB에 없으므로 기본값 사용
        platforms = ["네이버", "카카오맵", "당근마켓", "인스타그램"]

        self.restart_with_params.emit(region, keyword, platforms)
