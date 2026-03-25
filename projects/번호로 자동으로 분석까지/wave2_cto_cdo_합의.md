# CTO x CDO 합의문 — 네이버 플레이스 자동 진단 영업 제안서 시스템

*작성일: 2026-03-25*
*작성자: CTO (Wave 2 크로스 토론)*

---

## 합의 배경

CDO가 요청한 11슬라이드 PPT 구조와 막대 차트, 색상 코딩 등의 시각화 요소가
기술적으로 구현 가능한지 검토하고, 불가능한 부분은 대안을 확정한다.

---

## 합의 포인트 1: python-pptx로 막대 차트 구현 가능한가?

### 결론: 가능. 단, 방식을 명확히 선택해야 한다.

python-pptx는 두 가지 방식으로 차트를 삽입할 수 있다.

**방식 A: python-pptx 내장 차트 (권장)**

python-pptx는 `pptx.chart.data.ChartData` + `slide.shapes.add_chart()`를 통해
막대 차트를 코드로 직접 생성할 수 있다. 추가 라이브러리 불필요.

```python
from pptx.util import Inches, Pt
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.dml.color import RGBColor

# 슬라이드 4 경쟁사 비교 막대 차트 예시
chart_data = ChartData()
chart_data.categories = ['리뷰 수', '저장 수', '사진 수']
chart_data.add_series('경쟁사 평균', (68, 234, 18))
chart_data.add_series('내 업체', (12, 45, 3))

chart = slide.shapes.add_chart(
    XL_CHART_TYPE.BAR_CLUSTERED,  # 가로형 막대
    Inches(0.5), Inches(1.5), Inches(9), Inches(4.5),
    chart_data
).chart

# 시리즈 색상 개별 지정
series_competitor = chart.series[0]
series_mine = chart.series[1]
series_competitor.format.fill.fore_color.rgb = RGBColor(0x2E, 0xCC, 0x71)  # 초록
series_mine.format.fill.fore_color.rgb = RGBColor(0x95, 0xA5, 0xA6)       # 회색
```

**방식 B: matplotlib 이미지 생성 후 삽입 (백업)**

matplotlib으로 차트 PNG를 생성한 뒤 `slide.shapes.add_picture()`로 삽입.
폰트, 퍼센트 라벨, 커스텀 스타일링이 더 자유롭지만 의존성이 추가된다.

### 최종 합의: 방식 A (python-pptx 내장 차트) 우선 시도

이유: 신규 라이브러리 추가 없음. 현재 스택 유지. 시리즈별 색상 지정 가능.
단, CDO가 요구하는 "-82%" 퍼센트 라벨을 차트 위에 텍스트박스로 오버레이하는
추가 작업이 필요하다. 이는 구현 가능하며 BE에게 전달한다.

---

## 합의 포인트 2: 11슬라이드 PPT 자동 생성 — 기술 복잡도와 구현 방식

### 복잡도 평가

| 슬라이드 | 내용 | 구현 방식 | 복잡도 |
|---------|------|----------|--------|
| 1 | 표지 | 텍스트 교체 (업체명) | LOW |
| 2 | 업체 개요 | 텍스트 교체 6개 필드 | LOW |
| 3 | 검색 결과 스크린샷 | Playwright screenshot + 이미지 삽입 | MEDIUM |
| 4 | 경쟁사 비교 막대 차트 | python-pptx 내장 차트 + 텍스트 오버레이 | MEDIUM |
| 5 | 22개 항목 체크리스트 + 등급 | 텍스트 교체 + 도형 색상 변경 | MEDIUM |
| 6 | 치명적 3가지 블록 | 텍스트 교체 3개 블록 | LOW |
| 7 | 키워드 카드 7개 | 텍스트 교체 반복 | LOW |
| 8 | 패키지 비교 3개 | 텍스트 교체 (고정 콘텐츠) | LOW |
| 9 | 패키지 상세 | 텍스트 교체 + 동적 숫자 | LOW |
| 10 | 3개월 타임라인 | 텍스트 교체 3구간 | LOW |
| 11 | 견적서 | 텍스트 교체 | LOW |

### 구현 방식 확정: 템플릿 기반 텍스트 교체 + 차트 신규 삽입 혼합

기존 ppt_generator.py의 방식(템플릿 PPTX에서 텍스트 교체)을 유지하되,
슬라이드 4(막대 차트)는 python-pptx로 동적 생성한다.

```
구현 전략:
1. PPT 템플릿 (11슬라이드) 준비 — CDO가 레이아웃 잡아서 제공
2. 각 슬라이드의 텍스트 자리표시자(placeholder)에 {{변수명}} 태그 삽입
3. ppt_generator.py가 태그를 실제 데이터로 교체
4. 슬라이드 4: 차트 영역은 빈 도형으로 남겨두고
   코드가 해당 위치에 python-pptx 차트를 새로 삽입
5. 슬라이드 5: 체크리스트 텍스트 + 색상 코딩은 텍스트 교체 + RGBColor 적용
```

**총 구현 시간 재추정**: 기존 CTO 분석의 30분 추정에서 +30분 추가.
슬라이드 3 스크린샷 삽입 로직과 슬라이드 4 차트 생성이 추가됐기 때문.
실질적 예상: 슬라이드 4~5 처리 포함 약 1시간.

---

## 합의 포인트 3: 색상 코딩 (초록/빨강/회색) — python-pptx 적용 방법

### 결론: 완전히 구현 가능

python-pptx의 `RGBColor`로 도형 채우기, 텍스트 색상, 차트 시리즈 색상을
모두 코드에서 제어할 수 있다.

### 색상 상수 정의 (config.py에 추가)

```python
# config.py 추가 항목
from pptx.dml.color import RGBColor

COLOR = {
    "green_success":  RGBColor(0x2E, 0xCC, 0x71),  # 경쟁사 막대, 완료 체크
    "red_danger":     RGBColor(0xE7, 0x4C, 0x3C),  # 차이 퍼센트, 미완료 X
    "orange_warning": RGBColor(0xE6, 0x7E, 0x22),  # D등급, 경고
    "gray_neutral":   RGBColor(0x95, 0xA5, 0xA6),  # 내 업체 막대
    "blue_good":      RGBColor(0x34, 0x98, 0xDB),  # A등급
    "purple_perfect": RGBColor(0x9B, 0x59, 0xB6),  # S등급
    "yellow_normal":  RGBColor(0xF3, 0x9C, 0x12),  # C등급
}
```

### 사용 패턴

**텍스트 색상 변경**:
```python
for paragraph in text_frame.paragraphs:
    for run in paragraph.runs:
        run.font.color.rgb = COLOR["red_danger"]
```

**도형 채우기 색상 변경**:
```python
shape.fill.solid()
shape.fill.fore_color.rgb = COLOR["green_success"]
```

**체크리스트 항목 색상 (슬라이드 5)**:
```python
def get_item_color(passed: bool) -> RGBColor:
    return COLOR["green_success"] if passed else COLOR["red_danger"]
```

**등급별 색상 (슬라이드 5 등급 표시)**:
```python
GRADE_COLOR = {
    "S": COLOR["purple_perfect"],
    "A": COLOR["blue_good"],
    "B": COLOR["green_success"],
    "C": COLOR["yellow_normal"],
    "D": COLOR["orange_warning"],
    "F": COLOR["red_danger"],
}
```

---

## 합의 포인트 4: CDO UX vs 기술 제약 — 타협점 확정

### 4-1. 원형 차트 (슬라이드 5 좌측 등급 표시)

**CDO 요청**: 등급을 원형 차트로 표시.
**기술 판단**: python-pptx의 도넛 차트(`XL_CHART_TYPE.DOUGHNUT`)로 구현 가능하나,
중앙에 텍스트를 동적으로 넣는 것이 불편하다. 중앙 텍스트박스를 차트 위에 오버레이해야 한다.

**합의**: 원형 차트 대신 **사각형 도형 + 등급 텍스트** 방식 채택.
- 중앙 큰 정사각형 도형 (테두리 없음, 등급 색상 배경)
- 중앙에 등급 문자 (72pt, 흰색)
- 하단에 점수 (32pt, 회색)
- CDO가 요구하는 시각적 충격은 동일하게 달성 가능.
- 구현 복잡도: LOW.

### 4-2. 스크린샷 삽입 (슬라이드 3)

**CDO 요청**: 실제 검색 결과 스크린샷을 PPT에 삽입.
**기술 판단**: Playwright로 스크린샷 촬영 후 `slide.shapes.add_picture()`로 삽입. 구현 가능.
단, 스크린샷 촬영에 추가 시간이 필요하다 (업체당 5~10초).

**합의**: 구현한다. 크롤링 파이프라인에 스크린샷 단계를 추가.
```python
# place_crawler.py에 추가
async def capture_search_screenshot(browser, keyword: str) -> str:
    """네이버 플레이스 검색 결과 스크린샷 저장, 파일 경로 반환"""
    url = f"https://m.search.naver.com/search.naver?query={keyword}&where=m_local"
    # ... Playwright screenshot
    path = output_dir / f"{keyword}_search.png"
    await page.screenshot(path=str(path), full_page=False)
    return str(path)
```

### 4-3. 체크리스트 체크박스 (슬라이드 5 우측)

**CDO 요청**: ✅ / ❌ 유니코드 아이콘.
**기술 판단**: python-pptx에서 유니코드 문자는 폰트에 의존한다.
Pretendard 폰트가 PPT에 임베딩되어 있지 않으면 다른 폰트로 렌더링되어
표시가 깨질 수 있다.

**합의**: 유니코드 대신 **텍스트 O/X + 색상** 방식 채택.
- 완료: "O" (초록 #2ECC71, Bold)
- 미완료: "X" (빨강 #E74C3C, Bold)
- Windows/Mac/모바일 환경 모두에서 동일하게 렌더링됨.
- 시각적 충격은 동일.

### 4-4. 폰트 (Pretendard)

**CDO 요청**: Pretendard Bold/ExtraBold 사용.
**기술 판단**: python-pptx는 폰트를 `run.font.name = "Pretendard"`로 지정한다.
단, PPT 파일을 여는 기기에 Pretendard가 설치되어 있어야 한다.
설치되지 않으면 기본 시스템 폰트로 대체된다.

**합의**: PPT 템플릿 파일 자체에 Pretendard를 사전 설정해두고,
코드는 폰트 이름을 변경하지 않는다 (텍스트 내용만 교체).
Pretendard 없는 환경 대비: 나눔고딕 또는 맑은 고딕을 폴백으로 지정.

### 4-5. 슬라이드 3 스크린샷 — 플레이스/블로그 분리 레이아웃

**CDO 요청**: 좌측 플레이스 검색 결과 + 우측 블로그 검색 결과 (2개 스크린샷).
**기술 판단**: Playwright로 두 URL 각각 스크린샷 가능. 2장 촬영 = +10~15초.

**합의**: 구현한다. 두 스크린샷 파일 경로를 PPT 생성기에 전달.

---

## 최종 합의 요약표

| 항목 | CDO 요청 | CTO 판단 | 합의 결과 |
|------|---------|---------|---------|
| 막대 차트 | 가로형 막대 비교 | python-pptx 내장 가능 | python-pptx 내장 차트 사용 |
| 차트 색상 | 초록/회색/빨강 | RGBColor로 완전 제어 가능 | CDO 색상 코드 그대로 적용 |
| 원형 등급 차트 | 도넛 차트 중앙에 등급 | 구현 번거로움 | 사각형 도형 + 텍스트로 대체 |
| 체크리스트 아이콘 | ✅ / ❌ 유니코드 | 폰트 의존성 위험 | "O" / "X" + 색상으로 대체 |
| 스크린샷 삽입 | 검색 결과 스크린샷 2장 | Playwright로 구현 가능 | 구현. 파이프라인에 추가 |
| 폰트 | Pretendard | 기기 의존성 있음 | 템플릿에 사전 설정, 코드 불변 |
| 퍼센트 라벨 (-82%) | 차트 위 텍스트 | 텍스트박스 오버레이 필요 | 차트 옆 별도 텍스트박스로 구현 |
| 11슬라이드 구조 | 심리 흐름 기반 11장 | 구현 가능 | 확정. 템플릿 기반으로 구현 |

---

## BE에게 전달하는 추가 구현 항목

Wave 1 CTO 분석의 구현 우선순위에 다음을 추가한다:

| 순서 | 작업 | 담당 파일 | 추가 이유 |
|------|------|---------|---------|
| 6-1 | 슬라이드 3 스크린샷 촬영 | crawlers/place_crawler.py | CDO 합의 |
| 6-2 | 슬라이드 4 막대 차트 동적 생성 | generators/ppt_generator.py | CDO 합의 |
| 6-3 | 슬라이드 5 등급 도형 색상 코딩 | generators/ppt_generator.py | CDO 합의 |
| 6-4 | 슬라이드 5 체크리스트 O/X 색상 | generators/ppt_generator.py | CDO 합의 |
| 6-5 | COLOR 상수 config.py에 추가 | config.py | 색상 관리 통일 |

**수정된 총 예상 시간**: 기존 3시간 + 1시간 = **약 4시간**

---

## CDO에게 요청 (확정 사항)

1. **PPT 템플릿 (11슬라이드) 제작 필요**: 슬라이드 4에 차트 삽입 영역 빈 자리 확보.
   코드가 해당 좌표에 차트를 삽입하므로, 다른 도형과 겹치지 않도록 여백 확보.

2. **슬라이드 5 등급 표시 영역**: 사각형 도형으로 변경된 것 인지 필요.
   원형 차트 대신 정사각형 도형 + 텍스트로 구현됨.

3. **체크리스트 아이콘**: ✅/❌ 대신 O/X + 색상으로 변경된 것 인지 필요.
   시각적 임팩트는 동일하게 유지됨.

4. **슬라이드 순서 변경 금지 원칙**: 확정된 11슬라이드 순서는 코드의 `SLIDE_INDEX` 상수와
   1:1로 연결됨. 이후 순서 변경 시 반드시 CTO에게 사전 통보.

---

*Wave 2 CTO x CDO 합의 완료. 2026-03-25*
