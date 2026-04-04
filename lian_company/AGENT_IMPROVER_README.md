# 에이전트 자기 개선 루프 — 구현 문서

## 개요

리안 컴퍼니의 에이전트들이 **자동으로 성과를 모니터링하고 프롬프트를 개선**하는 자기 개선 시스템입니다.

**핵심 원칙:**
- 리안이 문제를 발견하는 게 아니라 **시스템이 스스로 감지**
- 개선안은 **리안의 승인 후에만 적용** (자동 수정 금지)
- 개선 이력은 모두 기록되어 패턴 분석에 활용

---

## 작동 방식

### 1. 주간 리뷰에서 자동 실행

```
autopilot.run_weekly()
  ↓
propose_improvements()  ← agent_improver.py 호출
  ↓
  [저품질 에이전트 탐지]
  ↓
  [Perplexity로 베스트 프랙티스 수집]
  ↓
  [Claude로 개선 프롬프트 생성]
  ↓
  .pending_improvements.json 저장
  ↓
  보고사항들.md 업데이트
```

### 2. 리안의 승인 및 적용

```
1. 리안이 보고사항들.md에서 "## 에이전트 자기 개선 제안" 섹션 확인
2. 각 개선안 검토 후:
   - "적용" → apply_improvement("에이전트명")
   - "검토 후" → 수정 후 적용
   - "스킵" → 이번에는 안 함

3. apply_improvement() 실행
   ↓
   agents/{agent_name}.py 파일 프롬프트 업데이트
   ↓
   improvements_history.jsonl에 이력 기록
```

---

## 주요 함수

### propose_improvements()
**호출 시점:** 매주 autopilot.run_weekly()에서 자동
**역할:** 저품질 에이전트 탐지 → 개선안 생성 → 보고

```python
from core.agent_improver import propose_improvements

propose_improvements()
```

**동작:**
1. improvements.jsonl에서 최근 2주 파이프라인 리뷰 분석
2. 평가 점수 6~7.5점 범위 에이전트 식별
3. 각 에이전트별로:
   - Perplexity로 최신 베스트 프랙티스 수집
   - Claude Sonnet으로 개선 프롬프트 생성
4. .pending_improvements.json에 저장
5. 보고사항들.md 업데이트

---

### apply_improvement(agent_name)
**호출 시점:** 리안이 수동으로 승인 후
**역할:** 개선안을 실제 에이전트 파일에 적용

```python
from core.agent_improver import apply_improvement

# 예: 민수의 개선안 적용
apply_improvement("minsu")
```

**동작:**
1. .pending_improvements.json에서 해당 에이전트 개선안 로드
2. agents/{agent_name}.py 파일의 SYSTEM_PROMPT 교체
3. improvements_history.jsonl에 이력 기록
4. 개선안 상태를 "applied"로 마크

---

### 기타 함수

#### _extract_low_quality_agents() → list[dict]
improvements.jsonl에서 저품질 에이전트 자동 탐지

```python
low = _extract_low_quality_agents()
# [
#   {"agent": "sieun", "score": 6.5, "metadata": {...}},
#   ...
# ]
```

#### _get_agent_current_prompt(agent_name) → str
에이전트의 현재 프롬프트 추출

```python
prompt = _get_agent_current_prompt("junhyeok")
print(prompt[:300])  # 현재 프롬프트의 첫 300자
```

#### get_pending_improvements() → dict
미승인 개선안 목록 조회

```python
pending = get_pending_improvements()
# {
#   "minsu": {"improved_prompt": "...", "status": "pending_approval"},
#   ...
# }
```

---

## CLI 사용법

### 개선안 생성
```bash
python -m core.agent_improver propose
```

### 개선안 적용
```bash
python -m core.agent_improver apply minsu
python -m core.agent_improver apply junhyeok
```

### 미승인 개선안 목록 조회
```bash
python -m core.agent_improver list
```

---

## 파일 구조

```
lian_company/
├── core/
│   ├── agent_improver.py        ← 메인 구현
│   └── autopilot.py             ← 주간 호출 추가됨
├── .pending_improvements.json    ← 미승인 개선안 (리안 승인 대기)
├── knowledge/
│   ├── improvements.jsonl        ← 파이프라인 품질 평가
│   └── improvements_history.jsonl ← 적용된 개선안 이력
└── agents/
    ├── sieun.py
    ├── minsu.py
    ├── junhyeok.py
    └── ...
```

---

## 에이전트 메타데이터

현재 등록된 에이전트들:

| 에이전트 | 이름 | 역할 | 모델 |
|---------|------|------|------|
| sieun | 시은 | 오케스트레이터 및 팀 설계 | Claude Sonnet |
| seoyun | 서윤 | 시장 조사 | Perplexity API |
| minsu | 민수 | 비즈니스 전략 | GPT-4o |
| haeun | 하은 | 팩트 검증 | Gemini |
| junhyeok | 준혁 | GO/NO-GO 판단 | Claude Opus |
| taeho | 태호 | 트렌드 스카우팅 | Claude Haiku |

---

## 개선 판단 기준

### 저품질 판정 조건
- improvements.jsonl에서 최근 파이프라인 리뷰의 "전체 점수"가 **6~7.5점**
- (6점 미만: 시스템 전체 문제 / 7.5점 이상: 개선 불필요)

### 개선 대상 선택
- 점수 낮은 순으로 정렬
- 주마다 상위 3개 에이전트만 개선 (비용 제한)

### 개선 방법
1. **Perplexity 리서치**
   - 해당 역할의 2026 최신 베스트 프랙티스
   - 성공 사례 및 레퍼런스 수집

2. **Claude Sonnet 프롬프트 생성**
   - 현재 프롬프트 분석
   - 베스트 프랙티스 통합
   - 구체적 예시 추가
   - 피해야 할 패턴 명시

---

## 보고 형식 (보고사항들.md)

```markdown
## 에이전트 자기 개선 제안

**생성 시간**: 2026-04-04 10:30

**대기 중인 개선안**: 2개

### 시은
- 역할: 오케스트레이터 및 팀 설계자
- 상태: pending_approval
- 개선 내용:
  - 팀 설계 프롬프트에 "빠르면 1주" 같은 정량적 기준 추가
  - 교육팀 커리큘럼 구조화 개선
  - 팀 설계 결과물 체크리스트 추가

### 준혁
- 역할: GO/NO-GO 판단
- 상태: pending_approval
- 개선 내용:
  - 수익성 평가 기준에 "초기 현금흐름 없는 모델" 정의 추가
  - 조건부 GO의 조건들을 더 명시적으로
  - 피벗 판단 기준 추가

---

## 리안에게
위의 에이전트들이 자동 분석 결과 개선이 필요한 상태입니다.
각 개선안을 검토한 후 다음 중 하나를 선택해주세요:
- "적용" → 해당 에이전트 프롬프트 자동 업데이트
- "검토 후" → 수정 후 적용
- "스킵" → 이번에는 적용 안 함

적용 방법: `apply_improvement("에이전트명")`
```

---

## 주의사항

### 절대 금지
- 리안 승인 없이 프롬프트 자동 변경 (apply_improvement는 수동 호출만)
- 6점 미만 또는 7.5점 이상 에이전트의 개선 제안 (검증 필요)
- 에이전트 로직 변경 (프롬프트 문자열만 교체)

### 개선 효과 확인
개선안 적용 후 다음 파이프라인 실행 시:
- self_improve.py가 결과물 품질 재평가
- improvements.jsonl에 새로운 점수 기록
- 점수 개선 여부 확인 가능

---

## 향후 개선 방향

1. **더 정교한 저품질 탐지**
   - daily_log.jsonl 성공률 분석
   - 에이전트별 개별 평가 (지금은 파이프라인 수준)

2. **A/B 테스트**
   - 개선 전/후 비교 실행
   - 효과 입증 후 적용

3. **자동 학습**
   - 리안 피드백 수집
   - 개선안 생성 프롬프트 자체 개선

4. **다중 선택지 제시**
   - 하나의 개선안이 아니라 3개 선택지 제시
   - 리안이 최선의 방향 선택

---

## 문의 및 피드백

이 시스템에 대한 피드백이나 개선 사항은:
1. 보고사항들.md에 직접 작성
2. 다음 주간 리뷰에서 반영됨

---

**최종 업데이트**: 2026-04-04
**담당**: Claude (에이전트 자기 개선 시스템)
