from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QCheckBox, QListWidget, QGroupBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

from app.gui.widgets.platform_checkbox import PlatformCheckboxGroup
from app.services.history_service import list_history


class InputScreen(QWidget):
    """메인 입력 화면"""

    start_collection = pyqtSignal(str, str, list, bool)  # region, keyword, platforms, do_verify
    show_history_detail = pyqtSignal(int)  # session_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 타이틀
        title = QLabel("소상공인 연락처 수집 툴")
        title.setFont(QFont("Malgun Gothic", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #1a73e8; margin-bottom: 10px;")
        layout.addWidget(title)

        # 입력 영역
        input_group = QGroupBox("수집 조건")
        input_group.setStyleSheet("""
            QGroupBox {
                font-family: 'Malgun Gothic';
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding: 20px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
            }
        """)
        input_layout = QVBoxLayout()
        input_layout.setSpacing(15)

        # 지역명
        region_layout = QHBoxLayout()
        region_label = QLabel("지역명:")
        region_label.setFixedWidth(80)
        region_label.setStyleSheet("font-family: 'Malgun Gothic'; font-size: 13px; color: #555555;")
        self.region_input = QLineEdit()
        self.region_input.setPlaceholderText("예: 의정부시, 포천, 양주")
        self.region_input.setStyleSheet("""
            QLineEdit {
                font-family: 'Malgun Gothic';
                font-size: 12px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #1a73e8;
            }
        """)
        region_layout.addWidget(region_label)
        region_layout.addWidget(self.region_input)
        input_layout.addLayout(region_layout)

        # 업종 키워드
        keyword_layout = QHBoxLayout()
        keyword_label = QLabel("업종:")
        keyword_label.setFixedWidth(80)
        keyword_label.setStyleSheet("font-family: 'Malgun Gothic'; font-size: 13px; color: #555555;")
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("예: 카페, 음식점 (비워두면 전체업종)")
        self.keyword_input.setStyleSheet("""
            QLineEdit {
                font-family: 'Malgun Gothic';
                font-size: 12px;
                padding: 10px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #1a73e8;
            }
        """)
        keyword_layout.addWidget(keyword_label)
        keyword_layout.addWidget(self.keyword_input)
        input_layout.addLayout(keyword_layout)

        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # 플랫폼 선택
        self.platform_group = PlatformCheckboxGroup()
        layout.addWidget(self.platform_group)

        # 네이버플레이스 검증 옵션
        self.verify_checkbox = QCheckBox("네이버플레이스 검증 포함 (수집 시간 증가)")
        self.verify_checkbox.setChecked(True)
        self.verify_checkbox.setStyleSheet("""
            QCheckBox {
                font-family: 'Malgun Gothic';
                font-size: 13px;
                color: #333333;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 20px;
                height: 20px;
            }
        """)
        layout.addWidget(self.verify_checkbox)

        # 수집 시작 버튼
        self.start_button = QPushButton("수집 시작")
        self.start_button.setMinimumHeight(50)
        self.start_button.clicked.connect(self._on_start_clicked)
        self.start_button.setStyleSheet("""
            QPushButton {
                font-family: 'Malgun Gothic';
                font-size: 15px;
                font-weight: bold;
                color: #ffffff;
                background-color: #1a73e8;
                border: none;
                border-radius: 6px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #1557b0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        layout.addWidget(self.start_button)

        # 최근 수집 이력
        history_label = QLabel("최근 수집 이력 (클릭하여 상세보기)")
        history_label.setStyleSheet("font-family: 'Malgun Gothic'; font-size: 13px; color: #555555; margin-top: 10px;")
        layout.addWidget(history_label)

        self.history_list = QListWidget()
        self.history_list.setMaximumHeight(150)
        self.history_list.itemClicked.connect(self._on_history_clicked)
        self.history_list.setStyleSheet("""
            QListWidget {
                font-family: 'Malgun Gothic';
                font-size: 12px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: #f9f9f9;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eeeeee;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
            }
            QListWidget::item:selected {
                background-color: #bbdefb;
                color: #000000;
            }
        """)
        layout.addWidget(self.history_list)

        layout.addStretch()
        self.setLayout(layout)

        # 초기 이력 로드
        self.load_recent_history()

    # 동음이의 지역명 → 힌트 메시지
    _AMBIGUOUS_REGIONS = {
        "광주": "광주 (경기도 광주시) 또는 광주 (광주광역시)?\n예: '광주시' 또는 '광주광역시'로 입력하면 더 정확합니다.",
        "김포": "김포 (경기도 김포시)가 맞나요?\n서울 강서구 근처 지역이면 '김포시'로 입력하세요.",
        "성남": "성남 (경기도 성남시)이 맞나요?\n분당·수정·중원구 등 세부 지역을 추가하면 더 정확합니다.",
        "부천": "부천 (경기도 부천시)이 맞나요?",
        "안산": "안산 (경기도 안산시)이 맞나요? 단원구·상록구로 세분화할 수 있습니다.",
    }

    def _on_start_clicked(self):
        """수집 시작 버튼 클릭"""
        from PyQt6.QtWidgets import QMessageBox

        region = self.region_input.text().strip()
        if not region:
            QMessageBox.warning(self, "입력 오류", "지역명을 입력해주세요.")
            return

        # 모호한 지역명 경고
        for ambiguous, hint in self._AMBIGUOUS_REGIONS.items():
            if region == ambiguous:
                reply = QMessageBox.question(
                    self,
                    "지역명 확인",
                    f"'{region}'은(는) 여러 지역에 해당할 수 있습니다.\n\n{hint}\n\n이대로 진행하시겠습니까?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No,
                )
                if reply == QMessageBox.StandardButton.No:
                    self.region_input.setFocus()
                    return
                break

        keyword = self.keyword_input.text().strip()
        platforms = self.platform_group.get_selected()

        if not platforms:
            QMessageBox.warning(self, "입력 오류", "최소 1개 이상의 플랫폼을 선택해주세요.")
            return

        do_verify = self.verify_checkbox.isChecked()

        self.start_collection.emit(region, keyword, platforms, do_verify)

    def load_recent_history(self):
        """최근 수집 이력 5건 로드"""
        self.history_list.clear()
        try:
            sessions = list_history(limit=5)
            for session in sessions:
                text = f"{session['created_at']} | {session['region']} | {session['keyword'] or '전체'} | 총 {session['total_count']}건"
                item = self.history_list.addItem(text)
                self.history_list.item(self.history_list.count() - 1).setData(Qt.ItemDataRole.UserRole, session['id'])
        except Exception as e:
            print(f"이력 로드 실패: {e}")

    def _on_history_clicked(self, item):
        """이력 항목 클릭"""
        session_id = item.data(Qt.ItemDataRole.UserRole)
        if session_id:
            self.show_history_detail.emit(session_id)

    def set_input_values(self, region: str, keyword: str, platforms: list[str]):
        """입력 필드 값 설정 (재수집용)"""
        self.region_input.setText(region)
        self.keyword_input.setText(keyword)
        self.platform_group.set_selected(platforms)
