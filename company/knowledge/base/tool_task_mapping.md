# AI 모델 Task 기준 재배치 분석

> 분석일: 2026-04-09
> 원칙: "more tools ≠ better output, you need a system" — 기능이 아닌 task 기준 최적 배치

---

## 1. 현재 매핑표 (코드 기반 실측)

### 이사팀 (main.py 파이프라인)

| 에이전트 | 코드상 모델 | model_loader 적용 | 실제 모델 | task 정의 |
|----------|------------|-------------------|-----------|-----------|
| 시은 | CLAUDE_SONNET | - | claude-sonnet-4-6 | 아이디어 명확화 + 오케스트레이션 + 팀설계 |
| 서윤 | SONAR_PRO | - | sonar-pro | 실시간 시장조사 (웹검색) |
| 태호 | CLAUDE_HAIKU | - | claude-haiku-4-5 | 트렌드 스카우팅 (요약) |
| 민수 | get_model("minsu") | budget_strategy | gpt-4o-mini | 비즈니스 전략 수립 |
| 하은 | GEMINI_FLASH | - | gemini-2.5-flash | 팩트체크 + 반론 |
| 준혁 | CLAUDE_SONNET | - | claude-sonnet-4-6 | GO/NO-GO 최종 판단 |
| 지훈 | get_model("jihun") | prd | claude-haiku-4-5 | PRD 작성 (템플릿 기반) |

**발견:** 준혁은 코드에 `CLAUDE_SONNET`이 하드코딩되어 있으나, model_loader의 AGENT_ROLE_MAP에서는 "judge" 역할로 `claude-opus-4-7`으로 매핑됨. 하지만 junhyeok.py는 `get_model()`을 사용하지 않고 직접 `CLAUDE_SONNET`을 임포트하므로, 실제로는 Sonnet이 사용됨. **설계 의도(Opus)와 실제 코드(Sonnet) 불일치.**

### 온라인영업팀 (6명 전원 동일 모델)

| 에이전트 | 실제 모델 | task 정의 |
|----------|-----------|-----------|
| 박탐정 | claude-sonnet-4-5 | 잠재고객 발굴 체크리스트 생성 |
| 이진단 | claude-sonnet-4-5 | 4채널 진단서 작성 (점수화) |
| 김작가 | claude-sonnet-4-5 | 콜드 DM/이메일 스크립트 생성 |
| 최제안 | claude-sonnet-4-5 | 맞춤 제안서 + 3Tier 가격표 |
| 정클로저 | claude-sonnet-4-5 | 미팅 대본 + 거절 대응 스크립트 |
| 한총괄 | claude-sonnet-4-5 | 파이프라인 총괄 + 실행 매뉴얼 |

**발견:** 6명 전원 구버전 Sonnet(4-5) 하드코딩. model_loader 미사용. 모델 교체 시 6개 파일 수동 수정 필요.

### 온라인납품팀 (7명 전원 동일 모델)

| 에이전트 | 실제 모델 | task 정의 |
|----------|-----------|-----------|
| 서진호 | claude-sonnet-4-5 | SEO 키워드 맵 설계 |
| 한서연 | claude-sonnet-4-5 | 네이버 블로그 포스팅 작성 |
| 박지우 | claude-sonnet-4-5 | 인스타 콘텐츠 (캡션/릴스/해시태그) |
| 최도현 | claude-sonnet-4-5 | 퍼포먼스 광고 카피 (GFA/메타/카카오) |
| 윤하은 | claude-sonnet-4-5 | 상세페이지 카피라이팅 |
| 정민재 | claude-sonnet-4-5 | 월간 성과 리포트 + 전략 수정 |
| 김태리 | claude-sonnet-4-5 | 납품 총괄 PM (스케줄/QA) |

**발견:** 7명 전원 구버전 Sonnet(4-5) 하드코딩. model_loader 미사용.

### 온라인마케팅팀 (6명 전원 동일 모델)

| 에이전트 | 실제 모델 | task 정의 |
|----------|-----------|-----------|
| 서진혁 | claude-sonnet-4-5 | 잠재 셀러 리스트 발굴 + 리드 스코어링 |
| 한소율 | claude-sonnet-4-5 | 콜드메일/DM 시퀀스 + 견적서 |
| 윤채원 | claude-sonnet-4-5 | 마케팅 전략서 (채널 조합 설계) |
| 박시우 | claude-sonnet-4-5 | 상세페이지/블로그/인스타/광고 카피 |
| 이도현 | claude-sonnet-4-5 | 실행사 발주/납품관리/보고서 |
| 강하린 | claude-sonnet-4-5 | 성과 분석 + A/B 테스트 리포트 |

**발견:** 6명 전원 구버전 Sonnet(4-5) 하드코딩. model_loader 미사용.

### 오프라인 마케팅팀 (model_loader 일부 사용)

| 에이전트 | 코드상 모델 | model_loader 적용 | 실제 모델 | task 정의 |
|----------|------------|-------------------|-----------|-----------|
| 재원(researcher) | SONAR_PRO | - | sonar-pro | 영업 자료 수집 (웹검색) |
| 승현(strategist) | CLAUDE_SONNET | - | claude-sonnet-4-6 | 영업 전략 수립 |
| 예진(copywriter) | get_model("copywriter") | content | claude-haiku-4-5 | DM/스크립트 카피 |
| 검증자(validator) | get_model("validator") | strategist | claude-sonnet-4-6 | 현장 검증 |
| pipeline 내부 | claude-sonnet-4-5/4-6, claude-opus-4-7 | - | 혼합 | 자기개선, 종합판단, 멘트생성 |

### 교육팀

| 에이전트 | 실제 모델 | task 정의 |
|----------|-----------|-----------|
| 도윤(curriculum) | get_model → claude-sonnet-4-6 | 커리큘럼 설계 |
| 서윤(trainer) | sonar-pro | 세계 최고 수준 지식 수집 |
| team_generator | claude-sonnet-4-5 | 팀 파일 자동 생성 (코드) |

---

## 2. 구조적 문제 발견

### 문제 A: 모델 버전 파편화
- 이사팀/오프라인팀: `claude-sonnet-4-6` (최신)
- 영업/납품/마케팅팀 19명: `claude-sonnet-4-5` (구버전 하드코딩)
- model_loader 존재하지만 3개 팀(19명)이 전혀 사용하지 않음

### 문제 B: 모델 다양성 부족 (전원 Sonnet 문제)
- 영업팀 6명, 납품팀 7명, 마케팅팀 6명 = **19명 전원 동일 Sonnet**
- task 성격(리서치/카피/분석/판단)이 다른데 모델이 전부 같음
- "more tools ≠ better output" 위반: 같은 모델을 19번 호출하는 구조

### 문제 C: 준혁 모델 불일치
- model_loader: junhyeok → judge → claude-opus-4-7
- 실제 코드: `MODEL = CLAUDE_SONNET` (get_model 미사용)
- GO/NO-GO 최종 판단이 Sonnet으로 돌아가고 있음

---

## 3. Task 기준 최적 모델 재배치 제안

### Task 유형별 최적 모델

| Task 유형 | 특성 | 최적 모델 | 근거 |
|-----------|------|-----------|------|
| **최종 판단** | 정밀도 최우선, 저빈도 | Opus | 의사결정 오류 비용 > 모델 비용 |
| **전략 설계** | 구조화 + 창의성, 중빈도 | Sonnet 4-6 | 복합 추론 필요 |
| **콘텐츠 생성** | 글쓰기 품질, 고빈도 | Sonnet 4-6 | 한국어 카피 품질 직결 |
| **템플릿 채우기** | 구조화된 포맷, 고빈도 | Haiku / GPT-4.1-mini | 포맷 정해져 있으면 저렴 모델로 충분 |
| **리서치** | 웹검색, 최신정보 | Sonar Pro | 대체 불가 (실시간 검색) |
| **팩트체크** | 교차검증, 중빈도 | Gemini Flash | 빠르고 저렴, 검증에 적합 |
| **데이터 분석** | 숫자 처리, 패턴 인식 | Gemini Flash / GPT-4.1-mini | 구조화 출력 강점 |
| **총괄/QA** | 일관성 검증, 저빈도 | Sonnet 4-6 | 전체 맥락 파악 필요 |

### 에이전트별 제안 매핑

#### 이사팀

| 에이전트 | 현재 | 제안 | 변경 이유 |
|----------|------|------|-----------|
| 시은 | Sonnet 4-6 | Sonnet 4-6 | 유지 (오케스트레이션에 적합) |
| 서윤 | Sonar Pro | Sonar Pro | 유지 (대체 불가) |
| 태호 | Haiku | Haiku | 유지 (트렌드 요약에 적합) |
| 민수 | GPT-4o-mini | GPT-4o-mini | 유지 (비용 최적화 완료) |
| 하은 | Gemini Flash | Gemini Flash | 유지 (팩트체크에 최적) |
| **준혁** | **Sonnet 4-6** | **Opus** | **GO/NO-GO = 최종 판단. 코드 수정 필요** |
| 지훈 | Haiku | Haiku | 유지 (PRD 템플릿 기반) |

#### 온라인영업팀

| 에이전트 | 현재 | 제안 | 변경 이유 |
|----------|------|------|-----------|
| 박탐정 | Sonnet 4-5 | **Haiku** | 체크리스트 생성 = 템플릿 채우기 |
| 이진단 | Sonnet 4-5 | **Sonnet 4-6** | 진단서 = 전략적 분석. 품질 중요. 버전만 업 |
| 김작가 | Sonnet 4-5 | **Sonnet 4-6** | DM 카피 = 전환율 직결. 한국어 품질 중요 |
| 최제안 | Sonnet 4-5 | **Sonnet 4-6** | 제안서 = 계약 결정. 품질 유지 |
| 정클로저 | Sonnet 4-5 | **Haiku** | 미팅 대본 = 구조화된 템플릿. 패턴 반복 |
| 한총괄 | Sonnet 4-5 | **Haiku** | 실행 매뉴얼 = 정리/포맷팅 작업 |

#### 온라인납품팀

| 에이전트 | 현재 | 제안 | 변경 이유 |
|----------|------|------|-----------|
| 서진호 | Sonnet 4-5 | **Sonar Pro** | SEO 키워드 = 실시간 검색량 데이터 필요 |
| 한서연 | Sonnet 4-5 | **Sonnet 4-6** | 블로그 글 = 한국어 품질 최우선. 버전 업 |
| 박지우 | Sonnet 4-5 | **Sonnet 4-6** | 인스타 캡션 = 창의적 카피. 버전 업 |
| 최도현 | Sonnet 4-5 | **Haiku** | 광고 카피 = 짧은 포맷, 패턴 기반 |
| 윤하은 | Sonnet 4-5 | **Sonnet 4-6** | 상세페이지 = 전환 카피. 품질 중요 |
| 정민재 | Sonnet 4-5 | **Gemini Flash** | 성과 리포트 = 데이터 분석. 숫자 처리 |
| 김태리 | Sonnet 4-5 | **Haiku** | PM 스케줄/체크리스트 = 구조화 작업 |

#### 온라인마케팅팀

| 에이전트 | 현재 | 제안 | 변경 이유 |
|----------|------|------|-----------|
| 서진혁 | Sonnet 4-5 | **Sonar Pro** | 셀러 리서치 = 실시간 데이터 수집 필요 |
| 한소율 | Sonnet 4-5 | **Sonnet 4-6** | 세일즈 시퀀스 = 전환 카피. 버전 업 |
| 윤채원 | Sonnet 4-5 | **Sonnet 4-6** | 마케팅 전략 = 복합 추론. 버전 업 |
| 박시우 | Sonnet 4-5 | **Sonnet 4-6** | 크리에이티브 = 한국어 카피 품질 |
| 이도현 | Sonnet 4-5 | **Haiku** | 발주서/보고서 = 템플릿 포맷팅 |
| 강하린 | Sonnet 4-5 | **Gemini Flash** | 성과 분석 = 데이터+숫자 처리 |

#### 오프라인 마케팅팀

| 에이전트 | 현재 | 제안 | 변경 이유 |
|----------|------|------|-----------|
| 재원 | Sonar Pro | Sonar Pro | 유지 |
| 승현 | Sonnet 4-6 | Sonnet 4-6 | 유지 |
| 예진 | Haiku | **Sonnet 4-6** | DM 카피 = 전환율 직결. Haiku는 품질 부족 |
| 검증자 | Sonnet 4-6 | Sonnet 4-6 | 유지 (Opus에서 이미 다운그레이드됨) |

---

## 4. 비용 최적화 분석

### 현재 비용 구조 (1회 실행 기준 추정, input+output)

| 모델 | $/1M input | $/1M output | 현재 사용 에이전트 수 |
|------|-----------|------------|---------------------|
| Opus | $15 | $75 | 0명 (pipeline 내부만) |
| Sonnet 4-6 | $3 | $15 | 이사팀 3명 + 오프라인 2명 |
| Sonnet 4-5 | $3 | $15 | 19명 (영업+납품+마케팅) |
| Haiku | $0.80 | $4 | 이사팀 2명 + 오프라인 1명 |
| GPT-4o-mini | $0.15 | $0.60 | 1명 (민수) |
| Gemini Flash | $0.15 | $0.60 | 1명 (하은) |
| Sonar Pro | $3 | $15 | 2명 (서윤, 재원) |

**현재 문제: 19명이 Sonnet($3/$15)을 쓰는데, 그중 7명은 Haiku/Flash로 충분한 task.**

### 제안 후 비용 변화

| 변경 | 에이전트 수 | 절감 효과 |
|------|------------|-----------|
| Sonnet → Haiku | 7명 (박탐정, 정클로저, 한총괄, 최도현, 김태리, 이도현 + 교육팀 포함 안 함) | 에이전트당 ~73% 절감 |
| Sonnet → Gemini Flash | 2명 (정민재, 강하린) | 에이전트당 ~95% 절감 |
| Sonnet → Sonar Pro | 2명 (서진호, 서진혁) | 비용 동일하지만 실시간 데이터 획득 |
| Haiku → Sonnet | 1명 (예진) | 비용 증가하지만 DM 품질 향상 |
| Sonnet → Opus | 1명 (준혁) | 비용 5배 증가하지만 판단 정확도 향상 |

**예상 총 절감: 팀 전체 실행 1회당 약 40~50% API 비용 절감**
(Sonnet 19명 → Sonnet 10명 + Haiku 5명 + Flash 2명 + Sonar 2명)

---

## 5. 즉시 실행 가능한 액션

### 우선순위 1 — 구조 수정 (model_loader 통합)
영업/납품/마케팅팀 19명의 하드코딩된 `MODEL = "claude-sonnet-4-6"`를 `get_model()` 방식으로 교체. 이후 config 한 곳에서 전체 모델 교체 가능.

### 우선순위 2 — 준혁 모델 수정
`junhyeok.py`에서 `MODEL = CLAUDE_SONNET`을 `MODEL = get_model("junhyeok")`으로 변경. model_loader에 이미 judge → Opus 매핑 존재.

### 우선순위 3 — task별 모델 재배치
model_loader의 DEFAULT_CONFIG roles에 아래 추가:
```python
"template_fill": "claude-haiku-4-5-20251001",   # 박탐정, 정클로저, 한총괄, 최도현, 김태리, 이도현
"sales_copy": "claude-sonnet-4-6",               # 김작가, 한소율, 박시우, 한서연, 박지우, 윤하은
"analysis": "gemini-2.5-flash",                   # 정민재, 강하린
"lead_research": "sonar-pro",                     # 서진호, 서진혁
"strategy": "claude-sonnet-4-6",                  # 이진단, 최제안, 윤채원
```

### 우선순위 4 — 구버전 Sonnet 4-5 전면 퇴출
model_loader를 통해 4-6으로 일괄 전환. 하드코딩 제거 후 config 한 줄로 해결.
