# CTO 분석 — 지역 소상공인 010번호 + 인스타 자동 수집 시스템

## 기술 스택 결정

| 항목 | 선택 | 이유 |
|------|------|------|
| GUI 프레임워크 | PyQt6 6.6.1 | Windows 데스크톱 앱, 확정됨. QThread로 비동기 작업과 분리 |
| 스크래핑 엔진 | Playwright 1.40.0 | 동적 JS 렌더링 필수 (카카오맵, 구글맵, 당근). 확정됨 |
| 정적 수집 | requests + BeautifulSoup4 | 네이버 블로그/카페 등 정적 페이지 전용. 빠르고 가벼움 |
| 데이터 처리 | pandas 2.1.4 | 중복 제거, 정렬, 필터링 |
| 엑셀 출력 | openpyxl 3.1.2 | 하이퍼링크/색상 포함 엑셀 생성. 기존 코드 재활용 가능 |
| 데이터 저장 | SQLite3 + SQLAlchemy 2.0.23 | 세션 간 중복 방지, 캐시. 개인툴이므로 외부 DB 불필요 |
| 전화번호 처리 | phonenumbers 8.13.27 | 010 여부 검증, 형식 정규화 |
| 배포 | 로컬 실행 (배포 없음) | 개인 내부 툴. 패키징 필요 시 PyInstaller |

추가 변경 없음. 요구사항에 최적화된 스택이다.

---

## 아키텍처

```
[PyQt6 GUI — MainWindow]
        |
        | QThread 신호/슬롯
        v
[CollectorOrchestrator]  ← 지역명, 카테고리 입력받아 전체 파이프라인 실행
        |
        |── [KakaoMapCollector]     Playwright (headless)
        |── [GoogleMapCollector]    Playwright (headless, stealth mode 필수)
        |── [NaverLocalCollector]   기존 main_v2.py 네이버 Local API 재활용
        |── [DaangnCollector]       Playwright (headless)
        |── [NaverBlogCafeCollector] requests + BeautifulSoup4
        |
        v
[DeduplicationEngine]   SQLite — 업체명+전화번호 기준 중복 제거
        |
        v
[InstagramFinder]       구글/네이버 검색 경유 ("[업체명] instagram") — 로그인 불필요
        |
        v
[NaverPlaceVerifier]    기존 main_v2.py get_place_detail() 재활용
        |
        v
[ScoreEngine]           기존 calc_score() 로직 재활용 + 010번호/인스타 보너스
        |
        v
[ExcelExporter]         기존 save_excel() 재활용 + 인스타 컬럼 추가
```

### 데이터 흐름

```
지역명 입력
    → 각 Collector 병렬 실행 (QThread 풀)
    → 결과 SQLite 임시 저장
    → 중복 제거 (업체명 유사도 + 전화번호 일치)
    → InstagramFinder 순차 실행 (rate limit 준수)
    → NaverPlaceVerifier 순차 실행 (실존 확인)
    → 점수 계산 → 엑셀 출력
```

---

## Engineering Rules (FE/BE 필수 준수)

### 1. Collector 독립성
각 Collector(카카오맵, 구글맵, 네이버, 당근, 네이버블로그카페)는 독립 클래스로 분리한다. 공통 인터페이스는 `collect(region: str, categories: list) -> list[BizRecord]`. 1개 Collector가 예외를 던져도 try/except로 감싸서 나머지 Collector는 계속 실행한다.

```python
class BaseCollector:
    async def collect(self, region: str, categories: list[str]) -> list[BizRecord]:
        raise NotImplementedError
```

### 2. GUI 블로킹 금지
모든 Playwright/HTTP 작업은 QThread 안에서 실행한다. asyncio 이벤트 루프는 QThread 내부에서 `asyncio.run()` 으로 생성한다. 진행 상황은 `pyqtSignal(str, int)` 로 메인 스레드에 전달한다.

```python
class CollectorWorker(QThread):
    progress = pyqtSignal(str, int)   # 메시지, 퍼센트
    finished = pyqtSignal(list)       # BizRecord 리스트
    error = pyqtSignal(str)

    def run(self):
        asyncio.run(self._async_run())
```

### 3. Rate Limiting 필수
모든 외부 요청 사이에 delay를 적용한다.
- 네이버 플레이스/검색: 0.8~1.2초 (랜덤)
- 카카오맵: 1.0~1.5초 (랜덤)
- 구글맵: 2.0~3.0초 (랜덤, 봇 감지 위험 높음)
- 당근마켓: 0.5~1.0초 (랜덤)
- 인스타그램 간접 검색: 1.0초

```python
import random
await asyncio.sleep(random.uniform(low, high))
```

### 4. User-Agent Rotation
Playwright 컨텍스트 생성 시 매 세션마다 UA를 교체한다. 최소 5개 데스크탑 + 3개 모바일 UA 풀을 유지한다. 카카오맵/네이버 플레이스는 모바일 UA를 기본으로 사용한다 (기존 코드 방식 유지).

### 5. SQLite 중복 방지
수집 즉시 SQLite에 INSERT OR IGNORE 한다. 키는 `normalized_name + phone`. 이름 정규화는 공백/특수문자 제거 + 소문자화. 동일 세션 내 재시도 시 이미 수집된 업체를 건너뛴다.

```sql
CREATE TABLE IF NOT EXISTS businesses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    normalized_name TEXT NOT NULL,
    phone TEXT,
    source TEXT,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(normalized_name, phone)
);
```

### 6. 기존 코드 재활용 원칙
`main_v2.py`의 다음 함수들은 그대로 재활용한다. 수정하지 않는다.
- `get_place_detail()` — 네이버 플레이스 상세 수집
- `_extract_instagram_from_html()` — HTML에서 인스타 URL 추출
- `find_instagram_via_naver()` — 네이버 검색 경유 인스타 수집
- `find_daangn_biz()` — 당근마켓 네이버 검색 경유 수집
- `calc_score()` / `priority_label()` — 점수 계산
- `save_excel()` — 엑셀 출력 (컬럼 추가 시 최소한으로 수정)

### 7. 예외 처리 계층
```
Collector 레벨: 개별 업체 수집 실패 → 로그 기록 후 다음 업체 진행
Collector 전체: 특정 플랫폼 전체 실패 → GUI에 경고 표시 후 다른 플랫폼으로 계속
애플리케이션: 치명적 오류만 팝업. 나머지는 상태바 메시지
```

---

## 기술 리스크

### 리스크 1: 구글맵 봇 차단 (높음)
구글은 Playwright 감지 기술이 강하다. CAPTCHA 또는 빈 결과 반환 가능성 높음.
- 해결: `playwright-stealth` 또는 `undetected-playwright` 적용. 요청 간격 2~3초. 구글맵은 보조 소스로 취급하고, 카카오맵/네이버를 메인으로 설정.
- Fallback: 구글맵 차단 시 자동으로 건너뛰고 다른 소스로 보완.

### 리스크 2: 카카오맵 DOM 구조 변경 (중간)
카카오맵은 CSS 클래스명을 주기적으로 변경한다.
- 해결: aria-label, data-* 속성, 텍스트 기반 선택자를 CSS 클래스보다 우선 사용. 실패 시 전체 텍스트에서 정규식으로 전화번호 추출하는 fallback 유지.

### 리스크 3: 인스타그램 계정 매칭 정확도 (중간)
"[업체명] instagram" 검색 결과가 무관한 계정을 반환할 수 있음.
- 해결: URL 추출 후 업체명과 인스타 계정명 유사도 검사(difflib). 신뢰도 낮은 경우 빈 값으로 처리. 기존 `_extract_instagram_from_html()` 의 EXCLUDE 필터 유지.

### 리스크 4: PyQt6 + asyncio 통합 (낮음)
QThread 내부에서 `asyncio.run()` 사용 시 Windows 이벤트 루프 정책 충돌 가능.
- 해결: QThread.run() 시작 시 `asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())` 명시 적용. 기존 main_v2.py가 이미 `if sys.platform == "win32"` 처리를 하고 있으므로 패턴 동일하게 유지.

### 리스크 5: 네이버 Local API 할당량 (낮음)
무료 API는 하루 25,000건 제한. 카테고리 20개 × 지역 여러 개 동시 실행 시 소진 가능.
- 해결: API 응답을 SQLite에 캐시. 동일 지역+카테고리는 24시간 내 재요청 없음.

---

## 모듈 구조 (권장)

```
local_biz_collector/
├── main.py                     PyQt6 앱 진입점
├── gui/
│   ├── main_window.py          메인 윈도우
│   └── progress_widget.py      진행상황 표시
├── collectors/
│   ├── base.py                 BaseCollector, BizRecord 데이터클래스
│   ├── kakao_map.py            카카오맵 Playwright 수집
│   ├── google_map.py           구글맵 Playwright 수집 (보조)
│   ├── naver_local.py          네이버 Local API + 플레이스 상세 (main_v2.py 재활용)
│   ├── daangn.py               당근마켓 수집 (main_v2.py 재활용)
│   └── naver_blog_cafe.py      네이버 블로그/카페 (정적)
├── enrichers/
│   ├── instagram_finder.py     인스타 계정 수집 (main_v2.py 재활용)
│   └── naver_place_verifier.py 실존 검증 (main_v2.py 재활용)
├── core/
│   ├── orchestrator.py         전체 파이프라인 조율
│   ├── deduplicator.py         SQLite 기반 중복 제거
│   ├── scorer.py               점수 계산 (main_v2.py 재활용)
│   └── ua_pool.py              User-Agent 풀 관리
├── output/
│   └── excel_exporter.py       엑셀 출력 (main_v2.py 재활용)
├── db/
│   └── models.py               SQLAlchemy 모델
└── requirements.txt
```

---

## CDO에게 요청

1. 진행 상황 UI는 단순하게: 텍스트 로그 + 단일 프로그레스 바로 충분하다. Collector별 별도 진행바는 QThread 관리 복잡도를 높이므로 Wave 1에서는 제외 요청.
2. 결과 미리보기 테이블은 QTableWidget으로 구현. 정렬/필터 인터랙션은 최소화 (엑셀에서 하면 됨).
3. 오류 발생 시 팝업 남발 금지. 상태바 + 로그 텍스트박스로 통합 요청.

---

## CPO에게 피드백

1. 카카오맵 + 구글맵 동시 실행은 봇 차단 리스크 때문에 Wave 1에서는 카카오맵 단독으로 시작하고 구글맵은 옵션 처리를 권장한다. 기능 범위 조정 가능 여부 확인 필요.
2. "네이버 플레이스 실존 검증" 단계는 업체당 1회 추가 요청이 발생한다. 100개 업체 기준 약 15~20분 소요. 검증 단계를 선택 옵션(체크박스)으로 처리하는 것이 UX 측면에서 낫다고 판단한다.
3. 인스타그램 계정 수집 정확도는 50~70% 수준으로 예상한다 (로그인 없이 간접 검색 방식의 한계). PRD에서 이 한계를 명시하고 사용자 기대치를 조정할 것을 권장한다.

---

## 구현 우선순위 (Wave 3 FE/BE 작업 순서)

1. BizRecord 데이터클래스 + BaseCollector 인터페이스 정의 (BE 선행)
2. NaverLocalCollector — main_v2.py 코드 이식, 즉시 동작 확인
3. CollectorWorker (QThread) + 기본 GUI 연결
4. KakaoMapCollector — 신규 구현 (가장 중요한 소스)
5. InstagramFinder + NaverPlaceVerifier — main_v2.py 재활용
6. ScoreEngine + ExcelExporter — main_v2.py 재활용
7. DaangnCollector — main_v2.py 재활용
8. GoogleMapCollector — 마지막 (봇 차단 리스크, 선택 기능)
9. SQLite 중복 제거 통합

---

_Wave 1 CTO 분석 완료. 2026-03-24_
