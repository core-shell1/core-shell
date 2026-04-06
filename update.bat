@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ================================================
echo   혜경님 업데이트 검토 시스템
echo ================================================
echo.

:: GitHub 최신 정보 가져오기 (적용 안 함)
echo GitHub 변경사항 확인 중...
git fetch origin >nul 2>&1

:: 변경된 파일 목록 확인
for /f %%i in ('git diff HEAD origin/main --name-only 2^>nul') do set HAS_CHANGES=1

if not defined HAS_CHANGES (
    echo.
    echo ✅ 이미 최신 상태입니다. 업데이트 없음.
    echo.
    pause
    exit /b 0
)

echo.
echo === 변경된 파일 목록 ===
git diff HEAD origin/main --name-only
echo.

echo === 상세 변경 내용 보기 ===
set /p VIEW_DETAIL="자세한 내용도 볼까요? (y/n): "
if /i "%VIEW_DETAIL%"=="y" (
    git diff HEAD origin/main --stat
    echo.
    set /p VIEW_MORE="한 줄씩 내용도 볼까요? (y/n): "
    if /i "%VIEW_MORE%"=="y" (
        git diff HEAD origin/main
        echo.
    )
)

echo.
echo ================================================
echo   hkyoun_company/ 는 절대 변경되지 않습니다.
echo   위 파일들만 업데이트됩니다.
echo ================================================
echo.

set /p APPLY="업데이트 적용할까요? (y/n): "
if /i "%APPLY%"=="y" (
    echo.
    echo 업데이트 적용 중...
    git merge origin/main
    echo.
    echo ✅ 업데이트 완료!
) else (
    echo.
    echo ❌ 업데이트 취소. 현재 상태 유지됩니다.
)

echo.
pause
