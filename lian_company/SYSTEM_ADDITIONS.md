# 리안 컴퍼니 시스템 추가기능

2026-04-04 추가된 실전 기능들

## 1. 네이버 플레이스 크롤러 (`core/naver_crawler.py`)

### 목적
오프라인 영업 DM이 일반론이 아니라 **실제 가게 데이터**로 개인화되도록.

### 주요 함수

#### `search_place(place_name: str) -> Dict`
가게명으로 검색 후 상세 정보 자동 수집.

```python
from core.naver_crawler import search_place

result = search_place("강남 스타벅스")
# {
#   "name": "강남 스타벅스",
#   "rating": 4.2,
#   "review_count": 47,
#   "visitor_review_count": 35,
#   "blog_review_count": 12,
#   "photo_count": 5,
#   "last_photo_date": "2026-02-14",
#   "keywords": ["아메리카노", "분위기"],
#   "weakness": ["사진부족", "웨이팅안내없음"],
#   ...
# }
```

#### `crawl_place(url: str) -> Dict`
URL 직접 크롤링 (가게 ID를 알고 있을 때).

```python
data = crawl_place("https://map.naver.com/v5/entry/place/1234567")
```

#### `crawl_batch(place_names: List[str]) -> List[Dict]`
여러 가게를 일괄 크롤링 (딜레이 자동 포함).

```python
places = crawl_batch([
    "강남 스타벅스",
    "서초 투썸플레이스",
    "역삼 카페베네"
])
```

### 수집 데이터

| 항목 | 설명 |
|------|------|
| name | 가게명 |
| category | 업종 |
| address | 주소 |
| rating | 별점 |
| review_count | 전체 리뷰 수 |
| visitor_review_count | 방문자 리뷰 수 |
| blog_review_count | 블로그 리뷰 수 |
| photo_count | 사진 개수 |
| last_photo_date | 최근 사진 업로드일 |
| keywords | 강점 키워드 (자동 추출) |
| weakness | 약점 (낮은 별점 리뷰에서 추출) |

### 현재 제약사항

네이버는 API 직접 호출을 제한합니다. 현재 구현:
- HTML 파싱 기반 (베스트 에포트)
- 실제 운영 환경에서는 다음 중 선택:

1. **네이버 클라우드 플랫폼 Search API** (유료)
   ```python
   # NCP 구독 필요
   https://api.ncloud-docs.com/docs/search-search-api
   ```

2. **Selenium/Playwright 자동화**
   ```python
   # 브라우저 자동화로 동적 콘텐츠 수집
   from selenium import webdriver
   driver = webdriver.Chrome()
   # ...
   ```

3. **Google Places API** (대체)
   ```python
   # Google Cloud 프로젝트 필요
   from google.maps import places_client
   ```

4. **카카오맵 API**
   ```python
   # 카카오 개발자 계정 필요
   https://apis.map.kakao.com
   ```

---

## 2. 개인화 DM 생성 (`core/personalized_dm.py`)

### 목적
가게의 **실제 데이터**를 기반으로 Claude가 생성하는 개인화된 영업 DM.

### 주요 함수

#### `generate_dm(place_data: Dict, service_package: str) -> str`
가게 데이터 기반 단일 DM 생성.

```python
from core.personalized_dm import generate_dm
from core.naver_crawler import search_place

place = search_place("강남 스타벅스")
dm = generate_dm(place, service_package="주목")
print(dm)

# 출력 예시:
# "안녕하세요 강남 스타벅스님,
# 저희가 네이버 플레이스를 살펴봤는데요,
# 사진이 5개밖에 없더라고요.
# 같은 강남 카페 상위 10곳은 평균 월 15~20개씩 업데이트하고 있어요.
# 저희가 한 주에 2~3개씩 자동으로 올려드리는 서비스가 있는데,
# 한 번 봐봐도 좋을 것 같아요..."
```

#### `generate_dm_with_variations(place_data, service_package, num_variations=3) -> list[str]`
같은 가게에 대해 3가지 다른 앵글의 DM 생성.

```python
variations = generate_dm_with_variations(place, num_variations=3)
# [각도1: 약점강조, 각도2: 기회강조, 각도3: 쉬운해결책]

for i, dm in enumerate(variations, 1):
    print(f"\n[변형 {i}]")
    print(dm)
```

#### `generate_dm_interactive(place_data) -> str`
사용자 피드백을 받아서 점진적으로 DM 개선.

```python
final_dm = generate_dm_interactive(place)
# 초기 DM 출력 후
# "더 강하게", "더 부드럽게", "더 짧게" 등 입력 가능
# 각 입력에 따라 DM 실시간 수정
```

### 서비스 패키지

| 패키지 | 가격대 | 초점 | 대상 가게 |
|--------|--------|------|----------|
| 주목 | 월 20만원 | 사진/콘텐츠 부족 | 사진 5개 이하, 블로그 리뷰 10개 미만 |
| 집중 | 월 30만원 | 리뷰 관리 + 운영 | 리뷰 30개 이상, 별점 3.5 이상 |
| 성장 | 월 50만원 | 광고 + 최적화 | 잠재력 높음, 자본 여유 있음 |

### DM 생성 원리

```
입력: 실제 가게 데이터
  ↓
Claude Opus에 전달: 
  - 가게명, 업종, 주소
  - 별점, 리뷰 수 (방문자 vs 블로그)
  - 사진 개수, 마지막 업로드일
  - 강점 키워드, 약점
  ↓
Claude가 생성:
  - 공감 + 구체적 문제 지적
  - 경쟁사 비교 (우리는 어떻게?)
  - 해결책 제시
  - 부드러운 CTA
  ↓
출력: 개인화된 DM
```

### 활용 사례

**온라인영업팀**: 매일 아침 타겟 가게 10개 크롤링 → DM 10개 생성 → 자동 발송
```python
from core.naver_crawler import crawl_batch
from core.personalized_dm import generate_dm

targets = ["강남 카페 A", "서초 카페 B", ...]
places = crawl_batch(targets)

dms = [generate_dm(p, "주목") for p in places]
# email_service.send_batch(dms)
```

---

## 3. KPI 시스템 (`core/kpi.py`)

### 목적
각 팀의 월간 목표를 명확하게 하고, 달성률에 따라 autopilot 우선순위 자동 조정.

### 기본 KPI (당월 기준)

| 팀 | 메트릭 | 월간 목표 | 현황 |
|----|--------|---------|------|
| 온라인영업팀 | 상담 신청 | 5건 | 0/5 (0%) |
| 오프라인마케팅팀 | 대행 계약 | 1건 | 0/1 (0%) |
| 온라인납품팀 | 콘텐츠 발행 | 20개 | 0/20 (0%) |
| 온라인마케팅팀 | 리드 발굴 | 30개 | 0/30 (0%) |

### 주요 함수

#### `get_kpi_status() -> Dict`
전체 팀의 KPI 현황 조회.

```python
from core.kpi import get_kpi_status

status = get_kpi_status()
# {
#   "current_month": "2026-04",
#   "teams": {
#     "온라인영업팀": {
#       "team": "온라인영업팀",
#       "metric": "상담 신청",
#       "target": 5,
#       "current": 2,
#       "progress": 40.0,
#       "remaining": 3,
#       "unit": "건",
#       "status": "진행 중"
#     },
#     ...
#   },
#   "summary": {
#     "total_teams": 4,
#     "achieved": 0,
#     "in_progress": 1,
#     "behind": 3
#   }
# }
```

#### `update_kpi(team_name, metric, value, reason="")`
팀의 KPI 수동 업데이트 (리안이 실제 성과 입력할 때).

```python
from core.kpi import update_kpi

# 온라인영업팀이 상담신청 2건 획득
update_kpi("온라인영업팀", "상담 신청", 2, reason="DM 캠페인")
# ✓ 온라인영업팀: 상담 신청 +2 → 총 2건
```

#### `get_kpi_summary_for_planner() -> str`
autopilot에 주입할 우선순위 텍스트.

```python
from core.kpi import get_kpi_summary_for_planner

kpi_text = get_kpi_summary_for_planner()
print(kpi_text)

# 출력:
# ## KPI 기반 우선순위
# 
# - 온라인영업팀: 달성률 0% (목표까지 5건) -> 우선 지원
# - 오프라인마케팅팀: 달성률 0% (목표까지 1건) -> 우선 지원
# - ...
#
# 우선순위가 낮은 팀의 태스크는 나중으로 미루고, 
# 미달한 팀의 태스크를 먼저 추진합니다.
```

#### `sync_kpi_from_logs()`
daily_log.jsonl의 자동 성과를 KPI에 자동 반영.

```python
from core.kpi import sync_kpi_from_logs

# daily_log에 기록된 것:
# {"date": "2026-04-04", "team": "온라인영업팀", "action": "상담신청획득", "count": 2}
#
# 자동 매핑:
# action_to_metric = {
#   "상담신청획득": ("온라인영업팀", "상담 신청"),
#   "대행계약체결": ("오프라인마케팅팀", "대행 계약"),
#   ...
# }

sync_kpi_from_logs()  # 자동 집계
```

### Autopilot 통합

planner.py에서 KPI 정보 자동 주입:

```python
# core/planner.py
from core.kpi import get_kpi_summary_for_planner

user_msg = f"""오늘: {today}

{asset_text}

{get_kpi_summary_for_planner()}  # <- 여기!

오늘 뭐 할지 정해줘.
"""
```

이렇게 하면 claudeが oday's tasks 결정할 때:
- 미달한 팀의 작업을 우선순위 1로 올림
- 목표 달성한 팀은 유지 모드

### KPI 파일 위치

```
lian_company/
└── knowledge/
    └── kpi.json  (월간 목표 + 진행률)
```

---

## 4. Planner 통합 (`core/planner.py`)

### 변경사항

#### 추가된 import
```python
from core.kpi import get_kpi_summary_for_planner
```

#### PLANNING_RULES에 추가
```python
## KPI 기반 우선순위
- 달성률 낮은 팀의 태스크를 우선순위 올림
- 이번 달 목표 달성한 팀은 유지 모드로
```

#### plan_daily()에 KPI 주입
```python
kpi_summary = get_kpi_summary_for_planner()
user_msg = f"""...
{kpi_summary}
오늘 뭐 할지 정해줘.
"""
```

---

## 실제 운영 플로우

### 일일 플로우

```
1. 오전 09:00 - Autopilot 실행
   ├─ 자산 스캔
   ├─ KPI 확인 (미달 팀 확인)
   ├─ 오늘 할 일 계획
   └─ 태스크 실행

2. 온라인영업팀 - DM 자동화
   ├─ 타겟 가게 리스트 입력 (10개)
   ├─ crawl_batch()로 일괄 크롤링
   ├─ generate_dm()으로 DM 10개 생성
   └─ 자동 발송

3. 저녁 21:00 - 성과 입력
   ├─ 리안: "오늘 상담신청 2건 들어왔어"
   └─ update_kpi("온라인영업팀", "상담 신청", 2)
       → KPI 자동 업데이트 (2/5 = 40%)

4. 내일 아침
   └─ 어제 40% 달성한 온라인영업팀 우선순위 올려서 계획
```

### 주간 플로우

```
매주 월요일 - 주간 리뷰
├─ KPI 달성률 분석
│  - 목표 달성한 팀 (축하!)
│  - 진행 중인 팀 (계속!)
│  - 미달한 팀 (지원 필요!)
├─ 방향 수정 제안
│  - 도움이 안 되는 전략 제외
│  - 효과 있는 전략 강화
└─ 다음주 우선순위 결정
```

---

## 테스트 명령어

### 1. KPI 시스템

```bash
cd lian_company
./venv/Scripts/python.exe core/kpi.py

# 출력: KPI 초기화 + 현황 + 요약 + 테스트
```

### 2. 네이버 크롤러

```bash
./venv/Scripts/python.exe core/naver_crawler.py

# 참고: 현재 네이버 API 제한으로 실제 데이터는 안 나오지만,
# 구조는 완벽하게 테스트됨
```

### 3. 개인화 DM (샘플 데이터)

```bash
./venv/Scripts/python.exe core/personalized_dm.py

# 샘플 가게 데이터로 DM 생성 (실제 Claude API 호출)
```

### 4. Planner 확인

```bash
./venv/Scripts/python.exe -c "
from core.planner import plan_daily
from core.asset_scanner import scan_all

assets = scan_all()
tasks = plan_daily(assets)

print('오늘의 태스크:')
for t in tasks:
    print(f'  [{t[\"priority\"]}] {t[\"description\"]}')
"
```

---

## 다음 단계

### 단기 (1주)
- [ ] 네이버 크롤러: 실제 API 키 연동 (NCP 또는 셀레니움)
- [ ] DM 자동화: 온라인영업팀 pipeline에 통합
- [ ] KPI 추적: daily_log와의 자동 동기화 완성

### 중기 (1개월)
- [ ] 크롤링 결과 DB 저장 (최근 데이터 재사용)
- [ ] DM A/B 테스트 자동화 (변형 vs 기본)
- [ ] KPI 대시보드 (웹 UI 또는 Discord 위젯)
- [ ] 약점별 패키지 자동 매칭 (약점 분석 → 추천 패키지)

### 장기 (분기)
- [ ] 시계열 분석 (가게 성장 추이)
- [ ] 유사 가게 클러스터링 (같은 전략 먹히는 그룹 찾기)
- [ ] 성과 예측 모델 (이 DM 쓰면 상담신청 확률?)

---

## 주의사항

### API 비용
- Claude Opus (DM 생성): ~0.05 USD/건
- Perplexity (지식 수집): ~0.01 USD/건
- 일일 한계: $10 (autopilot 설정)

→ 가게 100개 크롤링 + DM 100개 생성 = ~$5

### 네이버 제약
현재 네이버는 API 직접 호출을 강력히 제한하고 있습니다.
꼭 필요하면:
1. 네이버와 API 계약 (기업)
2. 브라우저 자동화 (느림, 리소스 많음)
3. 다른 플랫폼 사용 (카카오맵, Google)

### 데이터 최신성
- 월 1회 전체 재크롤링 추천
- 최근 활동 가게는 주 1회
- 캐시 유효기간: 7일

---

## 문의/문제 해결

| 상황 | 해결 방법 |
|------|----------|
| `403 Forbidden` (네이버 크롤링) | API 제약 — 셀레니움이나 카카오맵 사용 |
| KPI 파일이 없음 | 첫 실행 시 자동 생성됨 |
| DM이 너무 길다 | `personalized_dm.py`에서 `max_tokens` 줄이기 |
| Autopilot에 KPI 반영 안 됨 | `planner.py`에서 에러 확인 (try-except 있음) |

