@echo off
echo ============================================
echo  소상공인 연락처 수집 툴 - 설치
echo ============================================

python --version >nul 2>&1
if errorlevel 1 (
    echo Python이 설치되어 있지 않습니다.
    echo https://www.python.org 에서 Python 3.11 이상 설치 후 다시 실행하세요.
    pause
    exit /b 1
)

echo [1/3] 가상환경 생성 중...
python -m venv venv

echo [2/3] 패키지 설치 중...
venv\Scripts\pip install -r requirements.txt

echo [3/3] Playwright 브라우저 설치 중...
venv\Scripts\playwright install chromium

echo.
echo ============================================
echo  설치 완료! run.bat 으로 실행하세요.
echo ============================================
pause
