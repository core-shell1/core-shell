from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QTextEdit, QPushButton
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont


class ProgressScreen(QWidget):
    """수집 진행 화면"""

    cancel_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # 타이틀
        title = QLabel("수집 진행 중...")
        title.setFont(QFont("Malgun Gothic", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #1a73e8; margin-bottom: 10px;")
        layout.addWidget(title)

        # 프로그레스 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                font-family: 'Malgun Gothic';
                font-size: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #f5f5f5;
                text-align: center;
                height: 30px;
            }
            QProgressBar::chunk {
                background-color: #1a73e8;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # 수집된 건수 표시
        self.count_label = QLabel("수집된 업체: 0건")
        self.count_label.setFont(QFont("Malgun Gothic", 13))
        self.count_label.setStyleSheet("color: #333333; padding: 5px;")
        layout.addWidget(self.count_label)

        # 로그 텍스트
        log_label = QLabel("수집 로그:")
        log_label.setStyleSheet("font-family: 'Malgun Gothic'; font-size: 13px; color: #555555;")
        layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Malgun Gothic';
                font-size: 11px;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: #fafafa;
                padding: 10px;
                color: #333333;
            }
        """)
        layout.addWidget(self.log_text)

        # 중단 버튼
        self.cancel_button = QPushButton("중단")
        self.cancel_button.setMinimumHeight(45)
        self.cancel_button.clicked.connect(self.cancel_requested.emit)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                font-family: 'Malgun Gothic';
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                background-color: #d32f2f;
                border: none;
                border-radius: 6px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
            QPushButton:pressed {
                background-color: #8b0000;
            }
        """)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)
        self.collected_count = 0

    def update_progress(self, msg: str, pct: int):
        """로그 추가 및 프로그레스 업데이트"""
        self.log_text.append(msg)
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )

        # pct가 -1이면 progress bar 업데이트하지 않음
        if pct >= 0:
            self.progress_bar.setValue(pct)

        # 수집 건수 업데이트 (메시지에서 파싱)
        if "수집:" in msg or "발견:" in msg:
            try:
                # 간단한 카운트 증가
                self.collected_count += 1
                self.count_label.setText(f"수집된 업체: {self.collected_count}건")
            except:
                pass

    def reset(self):
        """진행 초기화"""
        self.progress_bar.setValue(0)
        self.log_text.clear()
        self.collected_count = 0
        self.count_label.setText("수집된 업체: 0건")

    def set_collected_count(self, count: int):
        """수집 건수 직접 설정"""
        self.collected_count = count
        self.count_label.setText(f"수집된 업체: {count}건")
