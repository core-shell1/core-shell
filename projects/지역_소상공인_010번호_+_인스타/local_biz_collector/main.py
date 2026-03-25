"""
소상공인 연락처 수집 툴
지역명 입력 → 구글맵/카카오맵/당근마켓/인스타그램/네이버에서
010번호 + 인스타계정 자동 수집 → 엑셀 출력

실행: python main.py
"""
import sys
import os
import subprocess

# Windows UTF-8 강제
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, os.path.dirname(__file__))


def _ensure_playwright_browser():
    """Playwright Chromium 브라우저 자동 설치 확인"""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
    except Exception:
        print("Playwright 브라우저 설치 중... (최초 1회)")
        subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            check=False,
        )


def _check_first_run():
    """최초 실행 시 .env 없으면 API 키 설정 다이얼로그 표시"""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        return

    from PyQt6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
        QPushButton, QGroupBox, QMessageBox
    )
    from PyQt6.QtGui import QFont

    dialog = QDialog()
    dialog.setWindowTitle("초기 설정 — API 키 입력")
    dialog.setMinimumWidth(500)

    layout = QVBoxLayout()
    layout.setSpacing(15)
    layout.setContentsMargins(25, 25, 25, 25)

    title = QLabel("API 키 설정 (선택)")
    title.setFont(QFont("Malgun Gothic", 14, QFont.Weight.Bold))
    title.setStyleSheet("color: #1a73e8;")
    layout.addWidget(title)

    info = QLabel(
        "API 키 없이도 자동 폴백 방식으로 수집됩니다.\n"
        "네이버/카카오 API 키가 있으면 더 빠르고 안정적으로 수집됩니다."
    )
    info.setStyleSheet("font-family: 'Malgun Gothic'; font-size: 12px; color: #555555;")
    info.setWordWrap(True)
    layout.addWidget(info)

    group = QGroupBox("API 키 (없으면 비워두세요)")
    group.setStyleSheet("""
        QGroupBox {
            font-family: 'Malgun Gothic'; font-size: 13px; font-weight: bold;
            color: #333333; border: 1px solid #e0e0e0; border-radius: 6px;
            margin-top: 8px; padding: 15px;
        }
        QGroupBox::title { subcontrol-origin: margin; padding: 0 8px; }
    """)
    group_layout = QVBoxLayout()
    group_layout.setSpacing(10)

    field_style = """
        QLineEdit {
            font-family: 'Malgun Gothic'; font-size: 12px; padding: 8px;
            border: 1px solid #cccccc; border-radius: 4px;
        }
        QLineEdit:focus { border: 2px solid #1a73e8; }
    """
    label_style = "font-family: 'Malgun Gothic'; font-size: 12px; color: #555555;"

    naver_id_label = QLabel("네이버 Client ID:")
    naver_id_label.setStyleSheet(label_style)
    naver_id_input = QLineEdit()
    naver_id_input.setPlaceholderText("NAVER_CLIENT_ID")
    naver_id_input.setStyleSheet(field_style)

    naver_secret_label = QLabel("네이버 Client Secret:")
    naver_secret_label.setStyleSheet(label_style)
    naver_secret_input = QLineEdit()
    naver_secret_input.setPlaceholderText("NAVER_CLIENT_SECRET")
    naver_secret_input.setStyleSheet(field_style)

    kakao_label = QLabel("카카오 REST API 키:")
    kakao_label.setStyleSheet(label_style)
    kakao_input = QLineEdit()
    kakao_input.setPlaceholderText("KAKAO_REST_API_KEY")
    kakao_input.setStyleSheet(field_style)

    for widget in [naver_id_label, naver_id_input, naver_secret_label,
                   naver_secret_input, kakao_label, kakao_input]:
        group_layout.addWidget(widget)

    group.setLayout(group_layout)
    layout.addWidget(group)

    btn_layout = QHBoxLayout()
    skip_btn = QPushButton("건너뛰기 (나중에 설정)")
    skip_btn.setStyleSheet("""
        QPushButton {
            font-family: 'Malgun Gothic'; font-size: 13px; padding: 10px 20px;
            border: 1px solid #cccccc; border-radius: 4px; background: #f5f5f5;
        }
        QPushButton:hover { background: #e8e8e8; }
    """)
    save_btn = QPushButton("저장하고 시작")
    save_btn.setStyleSheet("""
        QPushButton {
            font-family: 'Malgun Gothic'; font-size: 13px; font-weight: bold;
            padding: 10px 20px; border: none; border-radius: 4px;
            background: #1a73e8; color: white;
        }
        QPushButton:hover { background: #1557b0; }
    """)

    skip_btn.clicked.connect(dialog.reject)
    save_btn.clicked.connect(dialog.accept)
    btn_layout.addWidget(skip_btn)
    btn_layout.addWidget(save_btn)
    layout.addLayout(btn_layout)

    dialog.setLayout(layout)

    if dialog.exec() == QDialog.DialogCode.Accepted:
        lines = []
        if naver_id_input.text().strip():
            lines.append(f"NAVER_CLIENT_ID={naver_id_input.text().strip()}")
        if naver_secret_input.text().strip():
            lines.append(f"NAVER_CLIENT_SECRET={naver_secret_input.text().strip()}")
        if kakao_input.text().strip():
            lines.append(f"KAKAO_REST_API_KEY={kakao_input.text().strip()}")
        if lines:
            with open(env_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            # 저장된 키 즉시 적용
            from dotenv import load_dotenv
            load_dotenv(env_path, override=True)


def main():
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QFont
    from app.models.database import init_db
    from app.gui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setFont(QFont("Malgun Gothic", 10))
    app.setStyle("Fusion")

    # 최초 실행 체크 (API 키 설정)
    _check_first_run()

    init_db()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    _ensure_playwright_browser()
    main()
