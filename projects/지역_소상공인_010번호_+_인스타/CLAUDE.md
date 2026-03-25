> **LAINCP 자동 생성 프로젝트**
> 리안 컴퍼니 파이프라인이 생성한 구현 지시서야.
> 이 폴더에서 Claude Code 열고 `/work` 입력하면 Wave 1~6 자동 실행돼.
>
> - **프로젝트 유형**: 개인 툴
> - **아이디어**: 지역 소상공인 010번호 + 인스타 자동 수집 시스템. 오프라인 마케팅(문자 영업)용. 지역명 입력하면 구글맵, 카카오맵, 당근마켓, 인스타그램
> - **생성일**: 2026-03-24

---

# 구현 지시서 v1.0 — 지역 소상공인 데이터 수집·검증 툴

> 담당: 종범 (실행팀 구현 지시서) | 대상: Claude Code 직접 실행용

---

## 기술 스택

| 항목 | 선택 | 버전 |
|------|------|------|
| 런타임 | Python | 3.11.x |
| GUI 프레임워크 | PyQt6 | 6.6.1 |
| 웹 스크래핑 (정적) | requests + BeautifulSoup4 | requests 2.31.0 / bs4 0.0.2 |
| 웹 스크래핑 (동적) | playwright | 1.40.0 |
| 데이터 처리 | pandas | 2.1.4 |
| 엑셀 출력 | openpyxl | 3.1.2 |
| 로컬 DB | SQLite3 | 내장 |
| ORM | SQLAlchemy | 2.0.23 |
| 번호 파싱 | phonenumbers | 8.13.27 |
| 비동기 처리 | asyncio + QThread | 내장 |
| 환경변수 | python-dotenv | 1.0.0 |
| 패키지 관리 | pip + requirements.txt | - |
| 빌드 (배포용) | PyInstaller | 6.3.0 |

---

## 폴더 구조

```
local_biz_collector/
├── main.py                          # 앱 진입점
├── requirements.txt
├── .env
├── .gitignore
│
├── app/
│   ├── __init__.py
│   ├── config.py                    # 설정값 및 상수 관리
│   │
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py           # 메인 윈도우 (탭 컨테이너)
│   │   ├── screens/
│   │   │   ├── __init__.py
│   │   │   ├── input_screen.py      # ① 메인 입력 화면
│   │   │   ├── progress_screen.py   # ② 수집 진행 화면
│   │   │   ├── result_screen.py     # ③ 결과 미리보기 화면
│   │   │   └── history_screen.py    # ④ 수집 이력 화면
│   │   └── widgets/
│   │       ├── __init__.py
│   │       ├── platform_checkbox.py # 플랫폼 선택 체크박스 그룹
│   │       ├── progress_bar.py      # 플랫폼별 진행 상태 바
│   │       └── result_table.py      # 편집 가능한 결과 테이블
│   │
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base_collector.py        # 공통 인터페이스 (ABC)
│   │   ├── google_maps.py           # 구글맵 수집 모듈
│   │   ├── kakao_maps.py            # 카카오맵 수집 모듈
│   │   ├── daangn.py                # 당근마켓 수집 모듈
│   │   ├── instagram.py             # 인스타그램 수집 모듈
│   │   └── naver_blog.py            # 네이버블로그/카페 수집 모듈
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── phone_filter.py          # 010 번호 필터링
│   │   ├── naver_place.py           # 네이버플레이스 검증
│   │   └── deduplicator.py          # 중복 제거 및 병합
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py              # SQLAlchemy 엔진 및 세션
│   │   ├── business.py              # Business ORM 모델
│   │   └── history.py               # CollectionHistory ORM 모델
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── collection_service.py    # 수집 오케스트레이터
│   │   ├── export_service.py        # 엑셀 내보내기
│   │   └── history_service.py       # 이력 관리
│   │
│   └── workers/
│       ├── __init__.py
│       └── collection_worker.py     # QThread 기반 백그라운드 워커
│
├── data/
│   ├── db/
│   │   └── local.db                 # SQLite DB 파일 (자동 생성)
│   └── exports/                     # 엑셀 내보내기 기본 저장 경로
│
└── logs/
    └── app.log                      # 로그 파일 (자동 생성)
```

---

## 데이터 모델

```python
# app/models/business.py — SQLAlchemy ORM

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base
from datetime import datetime

class Business(Base):
    __tablename__ = "businesses"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    session_id       = Column(Integer, ForeignKey("collection_history.id"), nullable=False)
    
    # 핵심 데이터
    name             = Column(String(200), nullable=False)       # 업체명
    phone            = Column(String(20), nullable=True)         # 010-XXXX-XXXX 또는 NULL
    phone_status     = Column(String(20), default="확인")        # "확인" | "번호미확인"
    insta_url        = Column(String(500), nullable=True)        # 인스타그램 URL
    naver_place_url  = Column(String(500), nullable=True)        # 네이버플레이스 URL
    
    # 수집 메타
    sources          = Column(String(200), nullable=False)       # "구글맵,카카오맵" (콤마 구분)
    raw_address      = Column(String(500), nullable=True)        # 수집된 주소 원본
    
    # 검증 상태
    verify_status    = Column(String(20), default="미확인")      # "확인됨" | "미확인" | "폐업의심"
    
    # 타임스탬프
    collected_at     = Column(DateTime, default=datetime.utcnow)
    verified_at      = Column(DateTime, nullable=True)

    # 관계
    session          = relationship("CollectionHistory", back_populates="businesses")


# app/models/history.py — SQLAlchemy ORM

class CollectionHistory(Base):
    __tablename__ = "collection_history"

    id               = Column(Integer, primary_key=True, autoincrement=True)
    region           = Column(String(200), nullable=False)       # "의정부시 신곡동"
    keyword          = Column(String(200), nullable=True)        # "카페" 또는 NULL(전체)
    platforms        = Column(String(200), nullable=False)       # "구글맵,카카오맵,당근마켓,인스타그램,네이버"
    
    # 결과 요약
    total_count      = Column(Integer, default=0)
    verified_count   = Column(Integer, default=0)
    unverified_count = Column(Integer, default=0)
    closed_count     = Column(Integer, default=0)
    no_phone_count   = Column(Integer, default=0)
    
    # 상태
    status           = Column(String(20), default="진행중")      # "진행중" | "완료" | "오류" | "중단"
    error_log        = Column(Text, nullable=True)               # JSON 문자열로 플랫폼별 오류 저장
    
    started_at       = Column(DateTime, default=datetime.utcnow)
    completed_at     = Column(DateTime, nullable=True)

    businesses       = relationship("Business", back_populates="session", cascade="all, delete-orphan")
```

```sql
-- 인덱스 (database.py 초기화 시 자동 생성)
CREATE INDEX idx_businesses_session   ON businesses(session_id);
CREATE INDEX idx_businesses_phone     ON businesses(phone);
CREATE INDEX idx_businesses_verify    ON businesses(verify_status);
CREATE INDEX idx_history_region       ON collection_history(region);
CREATE INDEX idx_history_started      ON collection_history(started_at DESC);
```

---

## API 엔드포인트

> 데스크톱 로컬 툴이므로 외부 HTTP API 없음.  
> 내부 서비스 인터페이스를 아래와 같이 정의.

| 서비스 | 메서드 | 시그니처 | 설명 |
|--------|--------|---------|------|
| CollectionService | `start()` | `start(region, keyword, platforms) -> session_id` | 수집 오케스트레이터 시작 |
| CollectionService | `stop()` | `stop(session_id) -> bool` | 수집 중단 |
| CollectionService | `get_status()` | `get_status(session_id) -> dict` | 플랫폼별 현황 반환 |
| BaseCollector | `collect()` | `collect(region, keyword, limit) -> list[dict]` | 각 플랫폼 수집 공통 인터페이스 |
| PhoneFilter | `filter()` | `filter(records) -> tuple[list, list]` | (통과목록, 제거목록) |
| NaverPlaceValidator | `validate()` | `validate(businesses) -> list[Business]` | 검증 결과 반환 |
| Deduplicator | `run()` | `run(records) -> list[dict]` | 병합된 레코드 반환 |
| ExportService | `to_excel()` | `to_excel(session_id, save_path) -> str` | xlsx 파일 경로 반환 |
| HistoryService | `list()` | `list(limit=30) -> list[CollectionHistory]` | 최근 이력 목록 |
| HistoryService | `compare()` | `compare(session_id_a, session_id_b) -> dict` | 신규/삭제/변경 비교 |

---

## 핵심 구현 포인트

### 1. BaseCollector 공통 인터페이스
```python
# app/collectors/base_collector.py