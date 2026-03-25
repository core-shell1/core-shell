from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices, QColor


class ResultTableWidget(QTableWidget):
    """결과 테이블 위젯"""

    COLUMNS = ["업체명", "010번호", "검증상태", "네이버플레이스URL", "인스타URL", "수집출처", "업종"]

    STATUS_COLORS = {
        "확인됨": QColor("#d4edda"),
        "미확인": QColor("#fff3cd"),
        "폐업의심": QColor("#f8d7da"),
        "": QColor("#ffffff")
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        self.setColumnCount(len(self.COLUMNS))
        self.setHorizontalHeaderLabels(self.COLUMNS)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # 업체명
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # 010번호
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # 검증상태
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # 네이버
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # 인스타
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # 출처
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # 업종

        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked)

        self.cellClicked.connect(self._on_cell_clicked)

        self.setStyleSheet("""
            QTableWidget {
                font-family: 'Malgun Gothic';
                font-size: 12px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: #ffffff;
                gridline-color: #e8e8e8;
            }
            QTableWidget::item {
                padding: 8px;
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

    def load_businesses(self, businesses: list[dict]):
        """업체 데이터 로드"""
        self.setRowCount(0)
        self.setRowCount(len(businesses))

        for row, biz in enumerate(businesses):
            # 업체명
            name_item = QTableWidgetItem(biz.get("name", ""))
            name_item.setFlags(name_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.setItem(row, 0, name_item)

            # 010번호
            phone_item = QTableWidgetItem(biz.get("phone", ""))
            phone_item.setFlags(phone_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.setItem(row, 1, phone_item)

            # 검증상태
            status = biz.get("verify_status", "")
            status_item = QTableWidgetItem(status)
            status_item.setFlags(status_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            status_item.setBackground(self.STATUS_COLORS.get(status, QColor("#ffffff")))
            self.setItem(row, 2, status_item)

            # 네이버플레이스URL
            naver_url = biz.get("naver_place_url", "")
            naver_item = QTableWidgetItem(naver_url if naver_url else "")
            naver_item.setForeground(QColor("#1a73e8"))
            naver_item.setFlags(naver_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.setItem(row, 3, naver_item)

            # 인스타URL
            insta_url = biz.get("insta_url", "")
            insta_item = QTableWidgetItem(insta_url if insta_url else "")
            insta_item.setForeground(QColor("#1a73e8"))
            insta_item.setFlags(insta_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.setItem(row, 4, insta_item)

            # 수집출처
            source_item = QTableWidgetItem(biz.get("sources", ""))
            source_item.setFlags(source_item.flags() ^ Qt.ItemFlag.ItemIsEditable)
            self.setItem(row, 5, source_item)

            # 업종
            category_item = QTableWidgetItem(biz.get("category", ""))
            category_item.setFlags(category_item.flags() | Qt.ItemFlag.ItemIsEditable)
            self.setItem(row, 6, category_item)

    def _on_cell_clicked(self, row: int, column: int):
        """셀 클릭 이벤트 - URL 컬럼 클릭 시 브라우저 열기"""
        if column in [3, 4]:  # 네이버플레이스URL 또는 인스타URL
            item = self.item(row, column)
            if item:
                url = item.text().strip()
                if url:
                    QDesktopServices.openUrl(QUrl(url))

    def keyPressEvent(self, event):
        """Delete 키로 선택된 행 삭제"""
        if event.key() == Qt.Key.Key_Delete:
            selected_rows = set(index.row() for index in self.selectedIndexes())
            for row in sorted(selected_rows, reverse=True):
                self.removeRow(row)
        else:
            super().keyPressEvent(event)

    def get_businesses(self) -> list[dict]:
        """현재 테이블의 데이터를 dict 리스트로 반환"""
        businesses = []
        for row in range(self.rowCount()):
            biz = {
                "name": self.item(row, 0).text() if self.item(row, 0) else "",
                "phone": self.item(row, 1).text() if self.item(row, 1) else "",
                "verify_status": self.item(row, 2).text() if self.item(row, 2) else "",
                "naver_place_url": self.item(row, 3).text() if self.item(row, 3) else "",
                "insta_url": self.item(row, 4).text() if self.item(row, 4) else "",
                "sources": self.item(row, 5).text() if self.item(row, 5) else "",
                "category": self.item(row, 6).text() if self.item(row, 6) else "",
            }
            businesses.append(biz)
        return businesses
