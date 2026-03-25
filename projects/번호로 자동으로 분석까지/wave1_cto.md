# CTO 분석 --- 네이버 플레이스 자동 진단 + 영업 제안서 시스템

## 1. 기술 스택 결정

| 항목 | 선택 | 이유 |
|------|------|------|
| 언어 | Python 3.11 | 이미 사용 중. Playwright, openpyxl 생태계 최적 |
| 크롤링 | Playwright (async) | 네이버 플레이스는 JS 렌더링 필수. 이미 안정적으로 동작 중 |
| HTTP | httpx (async) | 네이버 광고 API 호출용. 이미 사용 중 |
| 엑셀 | openpyxl | 인풋/아웃풋 모두 처리. 유지 |
| PPT | python-pptx | 템플릿 기반 생성. 유지 |
| 추가 없음 | - | 현재 스택으로 충분. 새 라이브러리 도입 불필요 |

**판단**: 기존 스택 100% 유지. 새 의존성 추가 없음. 코드 구조만 재설계.

---

## 2. 코드 구조 재설계

### 현재 문제
- 668줄 단일 파일 (process.py)
- 크롤링, API 호출, PPT 생성, 점수 계산이 전부 한 파일
- 경쟁사 크롤링 추가하면 1000줄 초과 예상
- 테스트/디버깅 시 전체 파일을 읽어야 함

### 목표 구조

```
번호로 자동으로 분석까지/
├── main.py                    # 엔트리포인트 (50줄 이하)
├── config.py                  # 경로, API 키, 상수 (40줄)
├── crawlers/
│   ├── __init__.py
│   ├── place_crawler.py       # 플레이스 홈 크롤링 (사진/리뷰/기본정보)
│   ├── rank_crawler.py        # 키워드 순위 크롤링
│   └── competitor_crawler.py  # 경쟁사 상위 5개 크롤링 (신규)
├── api/
│   ├── __init__.py
│   └── keyword_api.py         # 네이버 광고 API (키워드 통계)
├── scoring/
│   ├── __init__.py
│   └── engine.py              # 점수 계산 엔진 (신규)
├── generators/
│   ├── __init__.py
│   └── ppt_generator.py       # PPT 생성 + 텍스트 교체
├── io/
│   ├── __init__.py
│   └── excel_reader.py        # 엑셀 읽기
├── 샘플/                       # 기존 유지
│   ├── 샘플.xlsx
│   └── *.pptx (템플릿)
└── output/                    # 생성물
```

### 모듈별 책임

| 모듈 | 줄 수 (예상) | 역할 |
|------|-------------|------|
| main.py | ~50 | 파이프라인 오케스트레이션만. 로직 없음 |
| config.py | ~40 | BASE_DIR, API 키, USER_AGENTS, 경로 |
| place_crawler.py | ~180 | crawl_place() 함수. 사진/리뷰/기본정보/저장수/새소식 등 |
| rank_crawler.py | ~60 | get_keyword_rank() 함수 |
| competitor_crawler.py | ~120 | 상위 5개 업체 place_id 추출 + 동시 크롤링 |
| keyword_api.py | ~80 | 광고 API HMAC 서명 + 키워드 통계 |
| engine.py | ~150 | 22개 항목 점수 계산 (절대 + 상대) |
| ppt_generator.py | ~200 | PPT 생성, 슬라이드별 데이터 매핑 |
| excel_reader.py | ~40 | 엑셀에서 URL 행 읽기 |

**총 예상**: ~920줄 (현재 668 + 신규 기능 250줄). 단일 파일 대비 파일당 평균 100줄.

### 분리 순서 (의존성 역순)

1. config.py (의존성 없음)
2. io/excel_reader.py (config만 의존)
3. api/keyword_api.py (config만 의존)
4. crawlers/place_crawler.py (config만 의존)
5. crawlers/rank_crawler.py (config만 의존)
6. crawlers/competitor_crawler.py (place_crawler 재활용)
7. scoring/engine.py (독립)
8. generators/ppt_generator.py (독립)
9. main.py (전체 조립)

---

## 3. 경쟁사 동시 크롤링 전략

### 흐름

```
1) 메인 키워드로 네이버 플레이스 검색
2) 상위 5개 업체의 place_id 추출
3) 우리 업체 + 경쟁사 5개 = 총 6개 동시 크롤링
4) 결과를 상대 비교 점수에 사용
```

### place_id 추출 방법

모바일 네이버 검색 결과 (`m.search.naver.com/search.naver?query={keyword}&where=m_local`)에서:

```python
# 방법 1: HTML에서 place_id 직접 추출 (가장 안정적)
# 네이버 검색 결과 HTML에 place.naver.com/place/{id} 링크가 포함됨
place_ids = re.findall(r'place\.naver\.com/\w+/(\d+)', page_content)
# 중복 제거 후 상위 5개
place_ids = list(dict.fromkeys(place_ids))[:5]
```

```python
# 방법 2: 네이버 검색 API (REST) - 더 안정적이지만 결과가 다를 수 있음
# GET https://openapi.naver.com/v1/search/local.json?query={keyword}&display=5
# 이미 NAVER_CLIENT_ID/SECRET 있으므로 바로 사용 가능
# 단, API 결과에는 place_id가 없고 link에 포함됨
```

**추천: 방법 1 (HTML 파싱)** -- 실제 플레이스 검색 순위와 동일한 결과를 얻을 수 있음.

### 브라우저 컨텍스트 전략

```
브라우저 1개 (chromium.launch)
  ├── Context 1: 우리 업체 크롤링
  ├── Context 2: 경쟁사 1 크롤링
  ├── Context 3: 경쟁사 2 크롤링
  ├── Context 4: 경쟁사 3 크롤링
  ├── Context 5: 경쟁사 4 크롤링
  └── Context 6: 경쟁사 5 크롤링
```

**동시 실행 수**: 최대 3개 (asyncio.Semaphore(3))

- 6개 동시: 메모리 과다 + 네이버 차단 위험
- 1개 순차: 너무 느림 (업체당 ~15초 x 6 = 90초)
- **3개 동시: 30초 내 완료 가능 + 안정적** (권장)

### 구현 골격

```python
# competitor_crawler.py

async def find_top_competitors(browser, keyword: str, my_place_id: str, count: int = 5) -> list[str]:
    """검색 결과에서 상위 place_id 추출 (내 업체 제외)"""
    context = await browser.new_context(...)
    page = await context.new_page()
    encoded = urllib.parse.quote(keyword)
    url = f"https://m.search.naver.com/search.naver?query={encoded}&where=m_local"
    await page.goto(url, timeout=30000)
    await page.wait_for_load_state("networkidle", timeout=20000)
    content = await page.content()
    await page.close()
    await context.close()

    place_ids = re.findall(r'place\.naver\.com/\w+/(\d+)', content)
    place_ids = list(dict.fromkeys(place_ids))  # 중복 제거, 순서 유지
    # 내 업체 제외
    place_ids = [pid for pid in place_ids if pid != my_place_id]
    return place_ids[:count]


async def crawl_competitors(browser, place_ids: list[str], max_concurrent: int = 3) -> list[dict]:
    """여러 업체 동시 크롤링 (세마포어로 동시 실행 수 제한)"""
    sem = asyncio.Semaphore(max_concurrent)

    async def _crawl_one(pid):
        async with sem:
            await asyncio.sleep(random.uniform(1.0, 3.0))  # 랜덤 딜레이
            return await crawl_place(browser, pid)

    tasks = [_crawl_one(pid) for pid in place_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if isinstance(r, dict)]
```

### 차단 방지 대책

| 대책 | 구현 |
|------|------|
| User-Agent 랜덤 | 이미 적용됨 (2개). 5개로 확장 권장 |
| 요청 간 딜레이 | random.uniform(1.0, 3.0)초 |
| 세마포어 | 동시 3개 제한 |
| Context 분리 | 업체마다 별도 context (쿠키/세션 격리) |
| 타임아웃 | 개별 업체 크롤링 실패 시 스킵 (전체 중단 안 함) |

---

## 4. 저장 수 / 새소식 / 기타 신규 크롤링 방법

### 4-1. 저장 수

네이버 플레이스 모바일 홈 페이지에서 "저장" 버튼 근처 텍스트로 추출.

```python
# 방법 1: 텍스트 파싱
save_match = re.search(r'저장\s*([\d,]+)', text)
if save_match:
    save_count = int(save_match.group(1).replace(',', ''))

# 방법 2: HTML에서 JSON 추출 (더 정확)
# 네이버 플레이스 HTML 내 __NEXT_DATA__ 또는 window.__PLACE_STATE__ JSON에
# "saveCount" 또는 "bookmarkCount" 필드가 있음
save_match = re.search(r'"(?:saveCount|bookmarkCount)"\s*:\s*(\d+)', content)
```

### 4-2. 새소식 마지막 업데이트 날짜

```python
# /feed 페이지에서 최신 게시물 날짜 추출
feed_url = f"https://m.place.naver.com/restaurant/{place_id}/feed"
# 또는
feed_url = f"https://m.place.naver.com/place/{place_id}/feed"

# 페이지 내 날짜 패턴 추출
date_matches = re.findall(r'(\d{4}\.\d{1,2}\.\d{1,2})', feed_text)
# 또는 상대 날짜
relative_matches = re.findall(r'(\d+일 전|\d+시간 전|어제|오늘)', feed_text)
```

### 4-3. 영수증 리뷰 수 (방문자 리뷰와 분리)

이미 process.py에 패턴이 있음 (183번줄). 현재 동작 확인 필요:

```python
rv3 = re.search(r"영수증 리뷰\s*([\d,]+)", text)
```

단, 네이버 플레이스에서 "영수증 리뷰"가 별도 탭으로 분리되어 있을 수 있음.
`/review/visitor` 페이지에서 탭별 카운트를 추출하는 것이 더 정확:

```python
# /review/visitor 페이지
review_url = f"https://m.place.naver.com/restaurant/{place_id}/review/visitor"
# "전체 N", "영수증 N" 패턴 파싱
```

### 4-4. 사장님 답글 응답률

```python
# /review/visitor 페이지에서 전체 리뷰 수 vs 사장님 답글이 있는 리뷰 수 비율
# "사장님" 또는 "답글" 키워드가 있는 리뷰 블록 카운트
# 정확한 비율은 어렵지만, "사장님 댓글 N개" 패턴이 있을 수 있음

# 실용적 접근: 리뷰 페이지 첫 20개 리뷰 중 사장님 답글 비율
owner_replies = len(re.findall(r'사장님.*?답[글변]', review_text, re.DOTALL))
total_visible_reviews = len(re.findall(r'리뷰\s*\d+', review_text))  # 또는 리뷰 블록 수
reply_rate = owner_replies / max(total_visible_reviews, 1)
```

### 4-5. 해시태그 설정 여부

```python
# 홈 페이지 HTML에서 해시태그 블록 존재 여부
has_hashtag = bool(re.search(r'#[가-힣a-zA-Z0-9_]+', text))
# 또는 "태그" 섹션 존재 여부
has_hashtag = "태그" in text or "#" in text
```

### 4-6. 네이버 예약 / 톡톡 / 스마트콜 / 쿠폰

현재 텍스트 매칭으로 구현됨. 더 정확하게 하려면:

```python
# HTML에서 JSON 데이터로 확인
has_booking = '"booking"' in content or '"naverBooking"' in content
has_talktalk = '"talktalk"' in content or '"naverTalkTalk"' in content
has_smartcall = '"smartCall"' in content or '"virtualNumber"' in content
has_coupon = '"coupon"' in content
```

### 4-7. 인스타 / 카카오 채널 연동

```python
# HTML 링크에서 확인
has_instagram = bool(re.search(r'instagram\.com/[a-zA-Z0-9_.]+', content))
has_kakao_channel = bool(re.search(r'pf\.kakao\.com/[a-zA-Z0-9]+', content))
# 또는 텍스트에서
has_kakao_channel = "카카오톡 채널" in text or "카카오채널" in text
```

---

## 5. 점수 계산 엔진 설계

### 5-1. 점수 구조

```
총점 = 절대 점수 (100점 만점) + 상대 점수 (경쟁사 대비 등급)
```

**절대 점수**: 이 업체가 네이버 플레이스를 얼마나 잘 관리하고 있는가?
**상대 점수**: 같은 키워드 경쟁사 상위 5개 대비 어디에 위치하는가?

### 5-2. 절대 점수 (100점 만점) --- 22개 항목

#### 카테고리 A: 기본 정보 완성도 (20점)

| # | 항목 | 배점 | 채점 기준 |
|---|------|------|-----------|
| 1 | 업체명 등록 | 2 | 있으면 2, 없으면 0 |
| 2 | 카테고리 등록 | 2 | 있으면 2, 없으면 0 |
| 3 | 주소 등록 | 2 | 있으면 2, 없으면 0 |
| 4 | 전화번호 등록 | 2 | 있으면 2, 없으면 0 |
| 5 | 영업시간 등록 | 4 | 있으면 4, 없으면 0 |
| 6 | 메뉴/가격 등록 | 4 | 있으면 4, 없으면 0 |
| 7 | 소개글 등록 | 4 | 있으면 4, 없으면 0 |

#### 카테고리 B: 콘텐츠 활성도 (35점)

| # | 항목 | 배점 | 채점 기준 |
|---|------|------|-----------|
| 8 | 사진 수 | 8 | 0장=0, 1~4장=2, 5~19장=4, 20~49장=6, 50장+=8 |
| 9 | 방문자 리뷰 수 | 8 | 0=0, 1~9=2, 10~49=4, 50~199=6, 200+=8 |
| 10 | 블로그 리뷰 수 | 5 | 0=0, 1~4=1, 5~19=3, 20+=5 |
| 11 | 영수증 리뷰 수 | 4 | 0=0, 1~9=1, 10~49=2, 50+=4 |
| 12 | 저장 수 | 5 | 0=0, 1~9=1, 10~49=3, 50+=5 |
| 13 | 새소식 활성도 | 5 | 없음=0, 30일 이내=5, 90일 이내=3, 그 이상=1 |

#### 카테고리 C: 관리 운영 (20점)

| # | 항목 | 배점 | 채점 기준 |
|---|------|------|-----------|
| 14 | 사장님 답글 응답률 | 8 | 0%=0, 1~19%=2, 20~49%=4, 50~79%=6, 80%+=8 |
| 15 | 해시태그 설정 | 4 | 있으면 4, 없으면 0 |
| 16 | 키워드 등록 | 4 | 0개=0, 1~2개=2, 3개+=4 |
| 17 | 대표 키워드 순위 | 4 | 1~3위=4, 4~10위=3, 11~30위=2, 30위+=1, 미노출=0 |

#### 카테고리 D: 플랫폼 연동 (15점)

| # | 항목 | 배점 | 채점 기준 |
|---|------|------|-----------|
| 18 | 네이버 예약 | 3 | 있으면 3, 없으면 0 |
| 19 | 네이버 톡톡 | 3 | 있으면 3, 없으면 0 |
| 20 | 스마트콜 | 3 | 있으면 3, 없으면 0 |
| 21 | 쿠폰/이벤트 | 3 | 있으면 3, 없으면 0 |
| 22 | SNS 연동 (인스타/카카오) | 3 | 2개=3, 1개=2, 없음=0 |

#### 카테고리 E: 검색 노출 (10점)

검색 노출은 위 항목들의 결과이므로 보너스 성격:

- 대표 키워드 검색 시 상위 5위 이내: +10점
- 6~10위: +7점
- 11~20위: +4점
- 21위 이하: +2점
- 미노출: 0점

**주의**: 카테고리 D의 17번과 E가 겹치지만, 17번은 "키워드 관리 노력"을 평가하고 E는 "실제 결과"를 평가하는 차이. 만약 중복이 문제라면 17번을 제거하고 C를 16점으로 조정.

### 5-3. 상대 점수 (경쟁사 대비 등급)

경쟁사 상위 5개의 절대 점수 평균을 기준으로:

```
내 점수 / 경쟁사 평균 점수 = 비율

비율 >= 1.2  →  A등급 (상위 업체 수준)
비율 >= 1.0  →  B등급 (평균)
비율 >= 0.8  →  C등급 (개선 필요)
비율 >= 0.6  →  D등급 (심각)
비율 <  0.6  →  F등급 (즉시 조치 필요)
```

추가로 항목별 비교 테이블 제공:

```
| 항목 | 우리 업체 | 경쟁사 평균 | 차이 |
|------|----------|-----------|------|
| 사진 수 | 12장 | 45장 | -33장 |
| 리뷰 수 | 23개 | 180개 | -157개 |
| ...  | ...  | ...  | ... |
```

### 5-4. 구현 골격

```python
# scoring/engine.py

class ScoreEngine:
    """22개 항목 절대 점수 + 경쟁사 대비 상대 점수"""

    THRESHOLDS = {
        "photo_count": [(0, 0), (1, 2), (5, 4), (20, 6), (50, 8)],
        "visitor_review_count": [(0, 0), (1, 2), (10, 4), (50, 6), (200, 8)],
        # ... 나머지 항목
    }

    def calc_absolute(self, data: dict) -> dict:
        """절대 점수 100점 계산. 카테고리별 소계 + 총점 반환"""
        scores = {}
        # 카테고리 A: 기본 정보
        scores["name"] = 2 if data.get("name") else 0
        scores["category"] = 2 if data.get("category") else 0
        # ... 22개 항목 전부
        scores["total"] = sum(scores.values())
        return scores

    def calc_relative(self, my_scores: dict, competitor_scores: list[dict]) -> dict:
        """경쟁사 대비 상대 등급 계산"""
        if not competitor_scores:
            return {"grade": "N/A", "ratio": 0}
        avg = sum(s["total"] for s in competitor_scores) / len(competitor_scores)
        ratio = my_scores["total"] / max(avg, 1)
        grade = "A" if ratio >= 1.2 else "B" if ratio >= 1.0 else "C" if ratio >= 0.8 else "D" if ratio >= 0.6 else "F"
        return {"grade": grade, "ratio": round(ratio, 2), "competitor_avg": round(avg, 1)}
```

---

## 6. Engineering Rules (FE/BE 필수 준수)

이 프로젝트는 Python 백엔드만 있으므로 BE 규칙:

### 규칙 1: 크롤링 함수는 반드시 개별 try/except + 타임아웃
```python
# 좋은 예
try:
    result = await crawl_place(browser, place_id)
except Exception as e:
    print(f"[Crawl] {place_id} 실패: {e}")
    result = default_place_data()  # 기본값 반환, 전체 중단 안 함

# 나쁜 예 - 하나 실패하면 전체 죽음
results = await asyncio.gather(*tasks)  # return_exceptions=True 없음
```

### 규칙 2: API 키를 코드에 하드코딩하지 않는다
현재 process.py 37~41번줄에 네이버 API 키가 하드코딩되어 있음. **반드시 config.py에서 환경변수 또는 .env로 분리**.

```python
# config.py
import os
from dotenv import load_dotenv
load_dotenv()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")
```

### 규칙 3: 크롤링 결과는 항상 기본값이 있는 dict로 반환
```python
# 모든 크롤링 함수는 실패해도 빈 값이 채워진 dict를 반환해야 함
# None 반환 금지. 호출부에서 None 체크 불필요하게 만들 것.
```

### 규칙 4: Playwright context는 반드시 finally에서 close
```python
context = None
try:
    context = await browser.new_context(...)
    # 작업
finally:
    if context:
        await context.close()
```
현재 코드에서 page만 close하고 context를 close하지 않는 부분이 있음 (92~254줄). 메모리 누수 원인.

### 규칙 5: 경쟁사 크롤링 실패는 무시하고 진행
경쟁사 5개 중 3개만 성공해도 상대 점수 계산 가능. 전체 파이프라인을 중단하지 않는다.

### 규칙 6: print 대신 구조화된 로깅
현재 print()로 로그를 찍고 있음. 당장은 유지하되, 함수명 + 타임스탬프를 포함:
```python
def log(tag: str, msg: str):
    print(f"[{tag}] {msg}")
```

### 규칙 7: 한 함수 100줄 초과 금지
현재 crawl_place()가 162줄 (92~254). 사진 크롤링, 리뷰 파싱, 키워드 추출을 서브 함수로 분리.

### 규칙 8: PPT 템플릿 슬라이드 인덱스는 상수로 관리
```python
# 나쁜 예
slide5 = prs.slides[4]

# 좋은 예
SLIDE_INDEX = {
    "cover": 0,
    "keyword_overview": 1,
    "keyword_expand": 2,
    "exposure_status": 3,
    "diagnosis": 4,
}
slide5 = prs.slides[SLIDE_INDEX["diagnosis"]]
```

---

## 7. 기술 리스크

| 리스크 | 심각도 | 해결 방법 |
|--------|--------|-----------|
| 네이버 크롤링 차단 (IP 밴) | HIGH | 세마포어 3, 랜덤 딜레이, UA 로테이션. 차단 시 headless=False로 전환 테스트 |
| 네이버 HTML 구조 변경 | HIGH | 정규식 기반이므로 유연하지만, 핵심 패턴 3개(사진수, 리뷰수, 키워드)는 월 1회 검증 필요 |
| API 키 노출 (현재 하드코딩) | CRITICAL | 즉시 .env 분리. .gitignore에 .env 추가. 이미 Git에 올라간 키는 로테이션 권장 |
| 경쟁사 크롤링으로 실행 시간 증가 | MEDIUM | 세마포어 3으로 30초 내 완료. 타임아웃 개별 15초. 전체 최대 60초 |
| PPT 템플릿 슬라이드 순서 변경 | LOW | 상수 인덱스로 관리. 템플릿 변경 시 상수만 수정 |

---

## 8. CDO에게 요청

1. PPT 템플릿에 **경쟁사 비교 슬라이드** 1장 추가 필요 (표 형태: 우리 vs 경쟁사 5개)
2. PPT 템플릿에 **점수 게이지/차트** 슬라이드 1장 추가 필요 (100점 만점 시각화)
3. 현재 PPT 템플릿의 슬라이드 순서가 코드에 하드코딩되어 있으므로, 슬라이드 추가/순서 변경 시 반드시 CTO에게 알릴 것

---

## 9. CPO에게 피드백

1. **경쟁사 크롤링 범위 확인 필요**: "상위 5개"를 네이버 플레이스 검색 결과 기준으로 할 것인지, 같은 동네+같은 업종 기준으로 할 것인지 결정 필요. 현재는 "메인 키워드 검색 결과 상위 5개"로 설계함.

2. **사장님 답글 응답률 정확도 한계**: 리뷰 페이지에서 보이는 최근 20개 리뷰 기준으로만 측정 가능. 전체 리뷰 대비 응답률은 네이버가 API를 제공하지 않는 한 불가능. 근사치임을 PPT에 명시해야 함.

3. **저장 수 크롤링 불확실성**: 네이버 플레이스 모바일 홈에서 저장 수가 항상 노출되는지 업종별로 다를 수 있음. 추출 실패 시 "확인 불가"로 표시하는 것이 맞는지 확인 필요.

4. **엑셀 인풋 vs 직접 URL 인풋**: 현재 엑셀 파일에서 첫 번째 URL만 처리. 여러 업체 일괄 처리(배치) 기능이 필요한지 우선순위 결정 필요. 기술적으로는 for 루프만 추가하면 되지만, 크롤링 시간이 업체당 30~60초이므로 10개면 5~10분 소요.

---

## 10. 구현 우선순위 (BE에게 전달)

| 순서 | 작업 | 예상 시간 |
|------|------|----------|
| 1 | config.py 분리 + .env 생성 + API 키 이동 | 15분 |
| 2 | 모듈 분리 (crawlers/, api/, generators/, io/) | 30분 |
| 3 | 경쟁사 place_id 추출 + 동시 크롤링 구현 | 45분 |
| 4 | 저장 수 / 새소식 / 응답률 등 신규 크롤링 항목 | 30분 |
| 5 | 점수 계산 엔진 구현 | 30분 |
| 6 | PPT 생성기에 경쟁사 비교 + 점수 슬라이드 추가 | 30분 |
| 7 | 전체 통합 테스트 | 20분 |

**총 예상: 약 3시간**

---

*CTO 분석 완료. 2026-03-25*
