# 토큰 효율 규칙 — Claude 비용 절감

## 원칙
모든 Claude/GPT/Gemini 호출은 이 규칙 따름. 에이전트 스폰 시 자동 적용.

## 1. 출력 제어 (최우선)
에이전트/Claude 호출 프롬프트 끝에 **반드시** 포함:
- 목록형 응답 필요 시: `"불릿 포인트만"`, `"최대 5개"`, `"한 줄씩"`
- 설명 필요 시: `"150자 이내"`, `"한 단락"`
- 코드만 필요 시: `"설명 없이 코드만"`, `"주석 없이"`
- JSON 필요 시: `"JSON만 출력 (```json 블록 없이)"`

**절대 금지:** 길이 제한 없는 오픈 프롬프트 (`"이거 분석해줘"` 같은 거)

## 2. 반복 지시 → System Prompt로
에이전트 프롬프트에 매번 들어가는 역할/톤/규칙은 `system` 메시지에 한 번만.
user 메시지에는 **이번 태스크 고유 정보만**.

**예시:**
```python
# ❌ 토큰 낭비
client.messages.create(messages=[
    {"role": "user", "content": "너는 카피라이터야. 한국어로, 짧게. 이번 태스크: 헤드라인 써줘."}
])

# ✅ 효율적
client.messages.create(
    system="한국어 카피라이터. 모든 응답 짧게.",
    messages=[{"role": "user", "content": "헤드라인 써줘."}]
)
```

## 3. 컨텍스트 압축
대화/작업 길어지면 주기적으로:
- `"지금까지 3줄로 요약. 다음엔 이 요약으로 이어간다"` 명령
- 또는 Claude Code `/compact` 자동 호출 (AUTOCOMPACT_PCT_OVERRIDE=50 권장)

## 4. 모델 라우팅 (핵심)
태스크 난이도에 따라 모델 분리:
- **Haiku** — 분류, 추출, 단순 변환, 요약, 포맷 변환
- **Sonnet** — 기획, 분석, 작성, 일반 코딩 (기본)
- **Opus** — 최종 판단, 복잡한 추론, 크리티컬 결정 (아끼기)

`.claude/settings.json`에 `CLAUDE_CODE_SUBAGENT_MODEL: "haiku"` 설정하면 서브에이전트는 자동으로 Haiku 사용.

## 5. 에이전트 호출 시 cost_tracker 사용
`company/tools/cost_tracker.py` 있음. 새 에이전트 호출 로직에:
```python
from tools.cost_tracker import log_call, track

with track(agent="yejin", task="DM 카피", model="sonnet"):
    result = call_claude(...)
```
주간 요약: `python tools/cost_tracker.py 7` (최근 7일)

## 6. 프롬프트 구조화
긴 프롬프트는 `Task/Data/Goal/Output` 형태로:
```
Task: 상품 설명 리라이트
Data: {product_name, features, target_customer}
Goal: 클릭률 올리는 헤드라인
Output: 3개 후보, 각 40자 이내
```

## 금지
- 범용 AI 조언 ("전문적으로", "자세하게") — 모델이 길어짐
- 근거 없는 "분석해줘" — 항상 출력 형식 지정
- 대화 히스토리 무한 누적 — 주기적 압축 필수
