# 네이버플레이스 PPT 자동화 SaaS - 품질 최적화 전략서 v1.0

## 🎯 Executive Summary (30초 요약)

| 품질 지표 | 현재(CLI) | 목표(SaaS) | 달성 방법 |
|---------|-----------|-----------|----------|
| **PPT 완성도** | 60% (수정 필요) | **95%+ (바로 사용)** | 3종 템플릿 + 데이터 검증 |
| **사용자 만족도** | - | **NPS 40+** | 피드백 루프 2주 주기 |
| **품질 점수** | - | **평균 8.5/10** | 주간 5% 랜덤 검수 |
| **오류율** | 30% (크롤링 실패) | **5%↓** | 자동 재시도 + 품질 게이트 |
| **생성 시간** | 15분 | **3분** | 병렬 처리 + 캐싱 |

**핵심 철학**: "수정 없이 바로 사장님께 보여줄 수 있는가?"가 품질의 유일한 기준.

---

## 📋 PPT 품질 가이드라인 (3단계 체크)

### 1단계: 데이터 정확성 (Gate 1)
```python
# 품질 게이트 검증 로직 (Celery Worker에 삽입)
class QualityGate:
    def validate_crawled_data(self, place_data: dict) -> bool:
        """크롤링 데이터 최소 기준 검증"""
        required_fields = {
            'place_name': (str, 1),      # 업체명 1자 이상
            'category': (str, 2),         # 카테고리 2자 이상
            'review_count': (int, 0),     # 리뷰수 0 이상
            'rating': (float, 0.0),       # 평점 0.0 이상
            'location': (str, 5),         # 주소 5자 이상
        }
        
        for field, (dtype, min_val) in required_fields.items():
            if field not in place_data:
                raise ValueError(f"필수 필드 누락: {field}")
            
            value = place_data[field]
            if not isinstance(value, dtype):
                raise TypeError(f"{field} 타입 오류: {type(value)} → {dtype}")
            
            if isinstance(min_val, int) and value < min_val:
                raise ValueError(f"{field} 최소값 미달: {value} < {min_val}")
        
        return True
    
    def validate_analysis_results(self, analysis: dict) -> bool:
        """분석 결과 품질 검증"""
        critical_insights = [
            'top_keywords',      # 최소 3개 키워드
            'competitor_gap',    # 경쟁사 비교 데이터
            'action_items',      # 최소 2개 액션 아이템
        ]
        
        for insight in critical_insights:
            if insight not in analysis or not analysis[insight]:
                raise ValueError(f"핵심 인사이트 누락: {insight}")
        
        # 키워드 최소 개수 검증
        if len(analysis['top_keywords']) < 3:
            raise ValueError(f"키워드 부족: {len(analysis['top_keywords'])}개 < 3개")
        
        # 액션 아이템 구체성 검증
        for action in analysis['action_items']:
            if len(action) < 10:  # 10자 미만은 너무 추상적
                raise ValueError(f"액션 아이템이 추상적: '{action}'")
        
        return True
```

**검증 실패 시 처리**:
- 크롤링 실패 → 자동 3회 재시도 (5초 간격)
- 재시도 실패 → 사용자에게 "일시적 오류" 알림 + 환불 처리
- 부분 데이터 → 경고 표시하며 PPT 생성 (예: "리뷰 데이터 없음")

---

### 2단계: 슬라이드 구성 (외부 판매 수준)

#### 표준 구성 (15장 고정, 3분 발표 기준)

| 슬라이드 번호 | 제목 | 필수 요소 | 데이터 매핑 |
|-------------|------|----------|-----------|
| **1** | 표지 | 업체명 + 분석 기간 | `place_name`, `datetime.now()` |
| **2** | 목차 | 5개 섹션 요약 | 자동 생성 |
| **3** | 핵심 요약 (Executive Summary) | 3가지 주요 발견 + 1줄 액션 | `top_3_insights` 추출 |
| **4** | 상권 분석 | 반경 1km 유동인구 + 업종 분포 | 네이버 통계 API |
| **5** | 경쟁사 비교 (1) | 상위 3개 경쟁사 테이블 | `competitor_data` |
| **6** | 경쟁사 비교 (2) | 가로 막대 그래프 (평점/리뷰수) | matplotlib → PNG |
| **7** | 키워드 분석 | 워드클라우드 + 상위 10개 키워드 | `wordcloud.generate()` |
| **8** | 리뷰 감정 분석 | 긍정/부정 비율 파이차트 | Naive Bayes 분류 |
| **9** | 시간대별 방문 패턴 | 꺾은선 그래프 (시간대별 리뷰 빈도) | `review_timestamps` |
| **10** | 사진 품질 진단 | 체크리스트 (5개 항목) | 이미지 메타데이터 분석 |
| **11** | 영업정보 완성도 | 프로그레스 바 (7개 항목) | `business_info` |
| **12** | 개선 제안 (1) | 우선순위 Top 3 액션 아이템 | `action_items[:3]` |
| **13** | 개선 제안 (2) | Before/After 예시 | 템플릿 이미지 |
| **14** | 예상 효과 | 3개월 후 예측 지표 (표) | ROI 계산식 |
| **15** | 감사 인사 + CTA | 연락처 + QR코드 | 사용자 입력 정보 |

**슬라이드 3 (핵심 요약) 생성 로직**:
```python
def generate_executive_summary(analysis: dict) -> dict:
    """3가지 핵심 인사이트 자동 추출"""
    insights = []
    
    # 1. 경쟁력 지표
    if analysis['rating'] > analysis['competitor_avg_rating']:
        gap = analysis['rating'] - analysis['competitor_avg_rating']
        insights.append(f"평점 경쟁력 우수: 경쟁사 대비 +{gap:.1f}점")
    else:
        gap = analysis['competitor_avg_rating'] - analysis['rating']
        insights.append(f"⚠️ 평점 개선 필요: 경쟁사 대비 -{gap:.1f}점")
    
    # 2. 리뷰 분석
    positive_ratio = analysis['positive_reviews'] / analysis['review_count']
    if positive_ratio > 0.7:
        insights.append(f"고객 만족도 높음: 긍정 리뷰 {positive_ratio*100:.0f}%")
    else:
        insights.append(f"⚠️ 부정 리뷰 대응 필요: {(1-positive_ratio)*100:.0f}%")
    
    # 3. 키워드 기회
    top_keyword = analysis['top_keywords'][0]
    insights.append(f"핵심 강점 키워드: '{top_keyword}' (언급 {analysis['keyword_counts'][top_keyword]}회)")
    
    # 1줄 액션
    if len(insights) > 0 and '⚠️' in insights[0]:
        action = "→ 우선 조치: 리뷰 응답률 향상 (목표 90%)"
    else:
        action = f"→ 강화 전략: '{top_keyword}' 키워드 마케팅 집중"
    
    return {
        'insights': insights,
        'action': action
    }
```

---

### 3단계: 디자인 품질 (3종 템플릿)

#### 템플릿 A: 기본형 (무료)
```python
# 템플릿 명세서 (JSON 형식으로 관리)
TEMPLATE_BASIC = {
    "name": "Clean & Simple",
    "target": "빠른 내부 공유용",
    "color_scheme": {
        "primary": "#2E5BFF",      # 네이버 블루
        "secondary": "#8C8C8C",    # 회색
        "accent": "#FF6B00",       # 강조 오렌지
        "background": "#FFFFFF",   # 흰색
        "text": "#1A1A1A"          # 진한 회색
    },
    "fonts": {
        "title": ("Noto Sans KR Bold", 36),
        "heading": ("Noto Sans KR Medium", 24),
        "body": ("Noto Sans KR Regular", 14)
    },
    "layout_rules": {
        "margin": "0.5 inch",
        "title_position": "top_center",
        "content_align": "left",
        "chart_size": "60% width"
    }
}
```

#### 템플릿 B: 프리미엄 (유료 ₩5,000)
- 그라데이션 배경 + 아이콘 삽입
- 커스텀 차트 디자인 (Seaborn 스타일)
- 애니메이션 효과 (Fade In)

#### 템플릿 C: 대행사용 (유료 ₩10,000)
- 브랜딩 페이지 추가 (로고 삽입 공간)
- 고급 인포그래픽 (Timeline, Process 다이