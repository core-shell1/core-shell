# Wave 6.5 — CRITICAL 자동 수정 내역

## 1차 Gemini 검증 → 발견된 CRITICAL 2개

### CRITICAL #1: Playwright 브라우저 미설치
**파일**: `local_biz_collector/main.py`
**수정 내용**: `_ensure_playwright_browser()` 함수 추가
- 앱 시작 시 Playwright Chromium 작동 여부 확인
- 없으면 `playwright install chromium` 자동 실행

### CRITICAL #2: .env 파일 미존재
**파일**: `local_biz_collector/main.py`
**수정 내용**: `_check_first_run()` 함수 추가
- 최초 실행 시 `.env` 없으면 API 키 입력 다이얼로그 팝업
- 비개발자가 GUI에서 바로 API 키 입력 가능
- 비워두고 건너뛰기 → Playwright 폴백으로 작동

## 재검증 결과 → 추가 CRITICAL 수동 수정 완료 (2026-03-24)

### CRITICAL #1: 엑셀 파일 열림 상태에서 저장 실패 ✅ 수정 완료
- **파일**: `app/services/export_service.py`
- **수정 내용**: `_resolve_save_path()` 함수 추가
  - 저장 전 파일 쓰기 가능 여부 테스트
  - PermissionError 발생 시 `파일명_1.xlsx`, `파일명_2.xlsx` 로 자동 변경 (최대 99회)

### CRITICAL #2: 앱 강제 종료 시 Playwright 좀비 프로세스 ✅ 수정 완료
- **파일**: `app/gui/main_window.py`
- **수정 내용**: `closeEvent`에 `_kill_playwright_zombies()` 호출 추가
  - Windows: `taskkill /F /IM chrome.exe /T` 실행

## HIGH 이슈 추가 수정 완료 (2026-03-24)

### HIGH #1: SQLite WAL 모드 미적용 ✅ 수정 완료
- **파일**: `app/models/database.py`
- **수정 내용**: `init_db()`에 `PRAGMA journal_mode=WAL` 추가

### HIGH #2: 지역명 모호성 경고 없음 ✅ 수정 완료
- **파일**: `app/gui/screens/input_screen.py`
- **수정 내용**: `_AMBIGUOUS_REGIONS` dict + `_on_start_clicked()` 경고 다이얼로그 추가
  - 광주, 김포, 성남, 부천, 안산 등 동음이의 지역 감지 → 확인 다이얼로그 표시
