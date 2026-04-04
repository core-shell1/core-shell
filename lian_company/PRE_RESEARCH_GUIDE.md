# 자동 레퍼런스 수집 시스템 가이드

## 개요

팀이 콘텐츠를 만들기 전에 **자동으로 경쟁사/레퍼런스를 수집** 하고 분석하는 시스템.

```
task → [pre_research] → Perplexity 계정 검색 → gallery-dl 포스트 수집 → Gemini 패턴 분석 → knowledge/base/ 저장
```

## 구현 파일

### 1. `core/pre_research.py`

핵심 모듈. 다음 함수들을 제공:

```python
from core.pre_research import auto_research

# 키워드 기반 자동 수집
research = auto_research(
    keyword="소상공인 인스타그램 마케팅",
    max_accounts=3,           # 수집할 계정 수
    posts_per_account=3       # 계정당 포스트 수
)

# 반환값: 요약 텍스트 (에이전트 프롬프트에 주입 가능)
print(research)
```

**기능:**
- ✅ Perplexity로 해당 업종 성공 계정/광고 사례 검색
- ✅ gallery-dl로 최신 포스트 URL 추출
- ✅ Gemini Flash로 패턴 분석 (콘텐츠 유형, 카피 패턴, 비주얼 스타일 등)
- ✅ knowledge/base/research_*.md에 자동 저장
- ✅ 24시간 캐싱 (같은 키워드는 재검색 안 함)

**에러 처리:**
- gallery-dl 없거나 쿠키 파일 없어도 Perplexity 결과는 반환
- API 실패해도 팀 실행은 계속 진행
- 모든 에러는 try/except로 감쌈

## 팀별 통합

각 팀 pipeline.py의 `run()` 함수에서 자동으로 호출됨:

### 온라인납품팀 (teams/온라인납품팀/pipeline.py)
```python
# 자동 실행 — pipeline 시작 부분
if HAS_PRE_RESEARCH:
    research = auto_research(task, max_accounts=3, posts_per_account=3)
    if research:
        context["reference_research"] = research
        save(output_dir, "00_자동레퍼런스.md", research)
```

### 온라인마케팅팀 (teams/온라인마케팅팀/pipeline.py)
### 온라인영업팀 (teams/온라인영업팀/pipeline.py)

동일하게 구현됨.

## 에이전트가 사용하는 방법

각 에이전트 .py 파일에서:

```python
def run(context, client):
    # context에서 레퍼런스 추출
    reference_research = context.get("reference_research", "")
    
    # 프롬프트에 주입
    user_msg = f"""
업무: {context['task']}

=== 레퍼런스 ===
{reference_research}

이 레퍼런스를 참고해서 콘텐츠를 만들어줘.
"""
```

## 출력 위치

각 팀 실행 시:

```
team/
├── 온라인납품팀/
│   ├── 00_자동레퍼런스.md    ← 수집된 레퍼런스 + 패턴 분석
│   ├── 00_팀인터뷰.md
│   ├── 서진호_결과.md
│   └── ...
└── 온라인마케팅팀/
    ├── 00_자동레퍼런스.md
    └── ...
```

## 캐싱 정책

**저장 위치**: `knowledge/base/research_*.json`

**캐시 유지 기간**: 24시간

**언제 갱신**:
```python
# 같은 키워드로 24시간 내 재실행 → 캐시 사용 (API 비용 절약)
research = auto_research("소상공인 인스타그램 마케팅")  # 캐시 O

# 24시간 지나면 새로 수집
```

**수동 갱신**:
```bash
# 캐시 파일 삭제하면 다음 실행에 새로 수집
rm "C:/Users/lian1/Documents/Work/core/lian_company/knowledge/base/research_*.json"
```

## 환경변수 (이미 설정됨)

`.env` 파일에 필요한 것들:

```env
PERPLEXITY_API_KEY=       # Perplexity API 키
GOOGLE_API_KEY=            # Gemini API 키
```

## 수동 테스트

```bash
cd lian_company
python core/pre_research.py "소상공인 카페 인스타그램 마케팅"
```

출력:
```
📋 [자동 레퍼런스 수집] 소상공인 카페 인스타그램 마케팅
============================================================
  🔍 Perplexity로 레퍼런스 계정 검색 중...
    ✅ 3개 계정 찾음
  📸 [1/3] https://www.instagram.com/계정명/ 포스트 수집 중...
      → 3개 포스트 추출
  🤖 Gemini로 패턴 분석 중 (9개 포스트)...
    ✅ 분석 완료
  💾 저장: research_소상공인_카페_인스타그램_마케팅.md
============================================================
  ✅ 완료: 9개 포스트 분석, 3개 계정 참고

## 소상공인 카페 인스타그램 마케팅 — 자동 수집 레퍼런스

**수집 계정** (3개):
- https://www.instagram.com/cafename1/
- https://www.instagram.com/cafename2/
- https://www.instagram.com/cafename3/

**수집 포스트** (9개):
- https://www.instagram.com/p/XXX1/
- https://www.instagram.com/p/XXX2/
...

**패턴 분석**:
1. 주요 콘텐츠 유형 — 카페 매장/음료 컷샷, 고객 후기/리뷰, 주간 메뉴/신메뉴
...
```

## 주의사항

### 1. gallery-dl 필수
```
lian_company/venv/Scripts/gallery-dl.exe
```
이 파일이 없으면 포스트 URL 추출 실패.
하지만 Perplexity 결과는 여전히 반환됨.

### 2. Instagram 쿠키 파일 필수
```
lian_company/instagram_cookies.txt
```
이 파일이 없으면 gallery-dl이 작동 안 함.
쿠키는 설정 → 쿠키 복사 → 파일 저장.

### 3. API 비용
- **Perplexity**: sonar-pro 사용 (비교적 저렴)
- **Gemini**: gemini-2.5-flash 사용 (무료 한도 내)
- **캐싱**: 24시간 캐시로 중복 호출 방지

### 4. 포스트 분석의 한계
- 이미지만 추출 (영상 처리는 선택적)
- 캡션은 생략 (저장 용량 절약)
- 최신 포스트 5개만 상세 분석

## 트러블슈팅

### "레퍼런스 계정을 찾을 수 없습니다"
- Perplexity API 키 확인
- 네트워크 연결 확인
- API 쿼터 확인

### "포스트 수집 실패 (쿠키/gallery-dl 확인)"
- `lian_company/venv/Scripts/gallery-dl.exe` 확인
- `lian_company/instagram_cookies.txt` 확인
- 쿠키 파일이 유효한지 확인 (만료 가능)

### "Gemini 분석 실패"
- GOOGLE_API_KEY 확인
- API 쿼터 확인
- 포스트 이미지 파일 크기 확인 (10MB 초과 가능)

## 향후 개선

- [ ] 영상 분석 강화 (현재 선택적)
- [ ] 광고 라이브러리 통합 (Meta Ads Library)
- [ ] 댓글/engagement 분석 추가
- [ ] 경쟁사 다중 비교 분석
- [ ] 주간 트렌드 자동 리포트

---

**최종 업데이트**: 2026-04-05
**작성자**: Claude Code (Backend Engineer Agent)
