from PyQt6.QtWidgets import QGroupBox, QHBoxLayout, QCheckBox


class PlatformCheckboxGroup(QGroupBox):
    """플랫폼 선택 체크박스 그룹 위젯"""

    PLATFORMS = [
        ("네이버", True),
        ("카카오맵", True),
        ("당근마켓", True),
        ("인스타그램", True),
        ("구글맵", False),
    ]

    def __init__(self, parent=None):
        super().__init__("플랫폼 선택", parent)
        self.checkboxes = {}
        self._init_ui()

    def _init_ui(self):
        layout = QHBoxLayout()
        layout.setSpacing(15)

        for platform_name, default_checked in self.PLATFORMS:
            checkbox = QCheckBox(platform_name)
            checkbox.setChecked(default_checked)
            checkbox.setStyleSheet("""
                QCheckBox {
                    font-family: 'Malgun Gothic';
                    font-size: 12px;
                    color: #333333;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                }
            """)
            self.checkboxes[platform_name] = checkbox
            layout.addWidget(checkbox)

        layout.addStretch()
        self.setLayout(layout)

        self.setStyleSheet("""
            QGroupBox {
                font-family: 'Malgun Gothic';
                font-size: 13px;
                font-weight: bold;
                color: #1a73e8;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
                background-color: #f9f9f9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 10px;
                background-color: #ffffff;
            }
        """)

    def get_selected(self) -> list[str]:
        """선택된 플랫폼 이름 리스트 반환"""
        return [
            platform_name
            for platform_name, checkbox in self.checkboxes.items()
            if checkbox.isChecked()
        ]

    def set_selected(self, platforms: list[str]):
        """플랫폼 선택 상태 설정"""
        for platform_name, checkbox in self.checkboxes.items():
            checkbox.setChecked(platform_name in platforms)
