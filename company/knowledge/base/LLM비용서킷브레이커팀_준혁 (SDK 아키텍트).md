
### OpenAI Python SDK monkey-patching interceptor pattern 2024 best practice
### OpenAI Python SDK Monkey-Patching Interceptor (2024 Best Practices)

**wrapt 라이브러리 사용: 안전한 런타임 패치로 OpenAI 클라이언트 메서드(OpenAI().chat.completions.create 등) 인터셉트. 직접 대체 대신 wrapper로 로깅/재시도/프록시 적용. Scoped patching + 테스트로 사이드 이펙트 0%** [2][3]

#### 1. 핵심 패턴: wrapt Function Wrapper (권장, gevent/eventlet 문제 피함)
```python
# 설치: pip install wrapt
import wrapt
from openai import OpenAI
import time, logging

@wrapt.patch_function_wrapper('openai', 'OpenAI.chat.completions.create')  # 모듈.클래스.메서드 지정
def interceptor(wrapped, instance, args, kwargs):
    start = time.time()
    try:
        response = wrapped(*args, **kwargs)  # 원본 호출
        latency = time.time() - start
        logging.info(f"OpenAI call: {latency:.2f}s, model={kwargs.get('model', 'gpt-4o')}")
        return response
    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        raise  # 재시도 로직 추가 가능 (exponential backoff)

# 자동 패치: 이 모듈 import 시 즉시 적용 (import 순서 무관) [2]
client = OpenAI(api_key="env:OPENAI_API_KEY")  # 사용법 동일
```
**효과**: 모든 OpenAI 인스턴스에서 글로벌 인터셉트. MRO 영향 없음 [3]. **사용 사례**: 로깅(99% 지연 추적), 재시도(5xx 에러 3회, backoff 2^x), 프록시(로컬 LLM fallback).

#### 2. 클래스 메서드 직접 패치 (간단 프로토타입, LangChain 스타일) [1]
```python
import types
from openai import OpenAI

def openai_interceptor(self, *args, **kwargs):
    print("Intercepted OpenAI call")
    original = self.chat.completions.create  # 원본 저장
    result = original(*args, **kwargs)
    print(f"Response: {result.choices[0].message.content[:50]}...")
    return result

# 패치 적용 (첫 호출 전)
OpenAI.chat.completions.create = types.MethodType(openai_interceptor, None)  # 클래스 레벨
```
**메트릭**: 1회 패치로 100% 커버리지. **위험**: import 순서 의존 (OpenAI 먼저 import) [2]. **대안**: functools.wraps로 데코레이터.

#### 3. 생산 환경 프레임워크 (2024 베스트)
| 패턴 | 코드 라인 | 지연 오버헤드 | 안전성 | 사용 사례 |
|------|-----------|---------------|--------|----------|
| **wrapt (권장)** | 10줄 | <1ms | 높음 (MRO 무시) | Prod 로깅/재시도 [2] |
| **직접 set attr** | 5줄 | 0ms | 중간 (순서 의존) | Dev 프로토 [1] |
| **Mock (테스트)** | 3줄 | 0ms | 높음 | unittest.mock [5] |

**재시도 + Backoff 통합** (OpenAI 에러 핸들링 베스트 [4][6]):
```python
import tenacity

@wrapt.patch_function_wrapper('openai', 'OpenAI.chat.completions.create')
@tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10), stop=tenacity.stop_after_attempt(3))
def retry_wrapper(wrapped, instance, args, kwargs):
    return wrapped(*args, **kwargs)
```
**수치**: 95% 5xx 복구율, 토큰 비용 20% 절감 (n=1, best_of=1 고정 [6]).

#### 4. 제한 + 체크리스트
- **Scoped**: unittest 내만 `with patch()` [3][5].
- **테스트**: 100% 커버리지 (patched vs original 비교).
- **Anti-pattern 피함**: API 키 하드코딩 금지 (dotenv), rate limit 무시 NO [4].
- **대안 우선**: Subclassing (`class LoggingClient(OpenAI)

### Anthropic Claude token counting before request streaming implementation
### **Claude Token Counting 핵심: 요청 전 비용/속도 사전 제어**

**핵심 목적**: 메시지 전송 **전** 토큰 수 계산 → 비용 예측, 속도 제한(RPM) 준수, 프롬프트 최적화[1][3].

#### **1. 실전 적용 프레임워크 (3단계)**
```
1. count_tokens() 호출 → 토큰 수 확인
2. 기준 초과 시: 프롬프트 압축/모델 라우팅
3. 실제 messages.create() 실행
```
**예시 비용 절감 사례**: 10만 토큰 프롬프트 → count_tokens로 8만 토큰 압축 → **20% 비용 ↓**[1][4].

#### **2. Python 실전 코드 (가장 빈번한 사용)**
```python
import anthropic
client = anthropic.Anthropic()

# 기본 텍스트
tokens = client.messages.count_tokens(
    model="claude-3-5-sonnet-20240620",  # 호환 모델: 3.5 Sonnet/Haiku, 3 Opus 등[3]
    system="You are a scientist",
    messages=[{"role": "user", "content": "Hello, Claude"}]
)
print(tokens.json())  # {'usage': {'input_tokens': 12, 'output_tokens': 0}}

# Tools 포함
tokens = client.messages.count_tokens(
    model="claude-3-5-sonnet-20240620",
    tools=[{"name": "get_weather", "input_schema": {...}}],  # Tool schema 토큰 추가
    messages=[{"role": "user", "content": "SF 날씨?"}]
)

# 이미지/PDF (base64 필수)
tokens = client.messages.count_tokens(
    model="claude-3-5-sonnet-20240620",
    messages=[{
        "role": "user",
        "content": [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_img}},
                    {"type": "text", "text": "Describe"}]
    }]
)
```
**수치**: 이미지 1장 ≈ 500-2000 토큰, PDF 1페이지 ≈ 1000-3000 토큰[1].

#### **3. Curl 실전 (배치/테스트용)**
```bash
curl https://api.anthropic.com/v1/messages/count_tokens \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "content-type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-3-5-sonnet-20240620",
    "messages": [{"role": "user", "content": "Your prompt here"}]
  }'
```
**응답 예**: `{"usage": {"input_tokens": 150, "output_tokens": 0}}`[1].

#### **4. 스트리밍 전 필수 체크리스트 (요청 → SSE 흐름 최적화)**
스트리밍(SSE)은 토큰 **생성 중** 즉시 전송되지만, **입력 토큰 초과 시 429 에러** → 사전 count_tokens로 방지[2][5].

| 체크 항목 | 임계값 | 액션 |
|-----------|--------|------|
| **RPM 제한** | Tier1:100, Tier4:8000[1] | count_tokens로 분당 호출 제한 |
| **입력 토큰** | 모델별 200K (Sonnet)[1] | >80% 시 프롬프트 자르기 |
| **출력 예비** | max_tokens=1024[2] | count_tokens(output_tokens=0) + 여유 20% |
| **스트리밍 비용** | 입력+출력 동시 청구[4] | 첫 토큰 시간(TTFT) 단축: 200ms 이내[5] |

**사례**: 긴 채팅(10턴) → count_tokens로 50K→30K 압축 → **요청 성공률 99%**, 비용 40%↓[1][4].

#### **5. 고급 최적화 (세계 최고 수준 트릭)**
- **Thinking 블록**: `thinking: {"budget_tokens": 16000}` → 추가

### Google Gemini API token estimation pre-call Python library
# Google Gemini API 토큰 사전 추정 Python 라이브러리

## 핵심 기능

**`count_tokens()` 메서드**가 API 호출 전 정확한 토큰 수를 계산합니다.[1][2] 이를 통해 비용 예측과 레이트 리밋 관리가 가능합니다.

## 실전 적용 코드

### 기본 텍스트 토큰 계산
```python
from google import genai

client = genai.Client()
prompt = "The quick brown fox jumps over the lazy dog."

total_tokens = client.models.count_tokens(
    model="gemini-2.0-flash", 
    contents=prompt
)
print("total_tokens: ", total_tokens)
# 출력 예: total_tokens: 10
```

### 멀티모달 입력 (이미지 포함)
```python
import PIL.Image

your_image_file = PIL.Image.open("organ.jpg")
token_count = client.models.count_tokens(
    model="gemini-2.0-flash",
    contents=["Tell me about this image", your_image_file]
)
# 출력 예: total_tokens: 263
```

### PDF 문서 토큰 계산
```python
sample_pdf = client.files.upload(file="test.pdf")

token_count = client.models.count_tokens(
    model="gemini-2.0-flash",
    contents=["Give me a summary of this document.", sample_pdf]
)
```

### 채팅 히스토리 토큰 계산
```python
from google.genai import types

chat = client.chats.create(
    model="gemini-2.0-flash",
    history=[
        types.Content(role="user", parts=[types.Part(text="Hi my name is Bob")]),
        types.Content(role="model", parts=[types.Part(text="Hi Bob!")])
    ]
)

# 히스토리만 계산
history_tokens = client.models.count_tokens(
    model="gemini-2.0-flash", 
    contents=chat.get_history()
)

# 히스토리 + 새 메시지 함께 계산
new_message = types.UserContent(
    parts=[types.Part(text="What is the meaning of life?")]
)
combined_history = chat.get_history()
combined_history.append(new_message)

total_tokens = client.models.count_tokens(
    model="gemini-2.0-flash", 
    contents=combined_history
)
```

### 캐시된 콘텐츠 토큰 계산
```python
your_file = client.files.upload(file="a11.txt")

cache = client.caches.create(
    model="gemini-1.5-flash-001",
    config={
        "contents": ["Here the Apollo 11 transcript:", your_file],
        "system_instruction": None,
        "tools": None,
    }
)

# 캐시 생성 후 프롬프트만 계산
prompt_tokens = client.models.count_tokens(
    model="gemini-2.0-flash", 
    contents="Please give a short summary of this file."
)
# 캐시된 콘텐츠는 따로 계산하지 않음

client.caches.delete(name=cache.name)
```

## 토큰-텍스트 변환 기준

- **1 토큰 ≈ 4 글자**[2]
- **100 토큰 ≈ 60-80 영어 단어**[2]

## 실제 API 호출과의 비교

`count_tokens()` 반환값과 `generate_content()`

### LLM agent loop infinite recursion detection circuit breaker pattern
### LLM Agent Loop 무한 재귀 탐지 & Circuit Breaker 핵심 패턴

**무한 루프 80% 원인: 반복 tool call + 상태 미변화. 비용 폭발 방지 위해 **3단계 circuit breaker** 필수 (탐지 → 차단 → 복구).[3][4][5]**

#### 1. **재귀 깊이 제한 (Recursion Limit) - 즉시 적용**
   - **최대 깊이**: 10~20회 (LangGraph 권장). 초과 시 **강제 Kill**.[3][4]
   - **코드 프레임워크** (Python/LangGraph):
     ```python
     max_iterations = 15  # 실전: 비용/지연 trade-off
     for i in range(max_iterations):
         state = agent.step(state)
         if no_change(state): break  # 상태 변화 없음 감지
     ```
   - **사례**: Deer-Flow 에이전트, 동일 tool 반복 → recursion_limit으로 $12k 청구 방지.[4][5]

#### 2. **상태 반복 탐지 (Loop Detection) - 90% 무한 루프 차단**
   - **방법**: **Hash 기반 캐시** (상태/도구 호출 시그니처 저장).
     - **중복 임계**: 3회 동일 hash → **Immediate Stop**.
   - **프레임워크**:
     | 패턴 | 구현 | 성공률 |
     |------|------|--------|
     | **State Hash** | `hash(frozenset(state.items()))` | 95%[3] |
     | **Tool Args Hash** | `hash((tool_name, *args))` | 반복 tool 100% 차단[4] |
     | **Rolling Window** | 최근 5스텝 중 80% 중복 → Trip | Portkey 표준[2] |
   - **LangGraph 적용**:
     ```python
     seen_states = set()
     if hash_state in seen_states: raise LoopError("Infinite recursion detected")
     seen_states.add(hash_state)
     ```
   - **사례**: RAG 에이전트, 지식 검색 반복 → 5분 내 $12k 절감.[5]

#### 3. **Circuit Breaker (실전 Production 패턴) - Cascading Failure 방지**
   - **3 상태 전이**: **Closed(정상) → Open(차단) → Half-Open(테스트)**.[1][2]
   - **설정 수치** (LLM 최적화):
     | Threshold | 값 | 이유 |
     |-----------|----|------|
     | **Failure Rate** | 50% (5/10 req) | Rate limit/Timeout 급증[1] |
     | **Open Timeout** | 30~60s | Provider 복구 시간[2] |
     | **Success to Close** | 2/3 연속 성공 | False positive 최소[1] |
     | **Status Codes** | 429,502,503,504 | Retryable만[1] |
   - **동시 적용**: Retry(3회, exponential backoff) → Fallback(다른 model) → Breaker Trip.[1][2]
   - **라이브러리**:
     - **Portkey/Bifrost**: Gateway 레벨 자동 (no code).[1][2]
     - **Python**: `pybreaker` - `breaker.call(func, timeout=30)`.
     - **LangGraph**: Custom Node로 삽입 → Cycle 최적화 70%↑.[3]

#### 4. **비용/성능 지표 & 모니터링**
   - **실전 KPI**:
     | Metric | 목표 | 알람 |
     |--------|------|------|
     | Loop Rate | <1% | 5%↑ Breaker Trip |
     | Iteration Avg | 5~8 | 15↑ Alert |
     | Cost/Loop | $0.01 미만 | $0.1↑ Kill |
   - **Early Stop 로직** (Tad Duval): Token 소비 80% 도달 → Hard Stop. YouTube 데모: 2줄 코드로 99% 안전.[7]

#### 5. **전체 Loop 아키텍처 (Deploy 즉시)**
```
Request → [Retry 3x] → [State Hash Check] → [Depth <15?] → Agent Step
                  ↓ No              ↓ Yes                  ↓
             Fallback Model    Breaker Trip (30s)    Continue
                  ↓
             Observability Log (LangSmit

### tiktoken vs tokenizers library accuracy benchmark for GPT-4o Claude-3-5 Gemini
### 핵심 벤치마크 결과 (2025년 7월 기준, 영어/코드 중심)[1]
**tiktoken (GPT-4o o200k_base)**이 **tiktoken (GPT-4 cl100k_base)**보다 토큰 효율 4-6% ↑, 속도 7% ↑. transformers SentencePiece (Llama 3)는 둘 다 열위. HuggingFace tokenizers는 직접 비교 없음 (tiktoken이 OpenAI 공식 BPE 구현)[5][6].

#### 토큰 효율 (tokens per 1,000 chars, ±표준편차)
| 텍스트 유형 | GPT-4o (tiktoken) | GPT-4 (tiktoken) | Llama 3 (SentencePiece) |
|-------------|-------------------|------------------|-------------------------|
| **영어 산문** | **176 ±8** | 185 ±9 | 190 ±10 [1] |
| **Python 코드** | **155 ±15** | 165 ±16 | 170 ±17 [1] |
| **중국어** | ~1,000 | ~1,000 | 유사 [1] |

- **코드 적용**: GPT-4o가 5% 효율 ↑ → 대규모 코드 앱에서 비용 5% 절감[1].
- **Claude-3.5/Gemini**: 직접 벤치 없음. tiktoken은 OpenAI 전용 (Claude/Gemini는 자체 BPE, transformers 호환 가능하나 정확도 미검증)[1].

#### 속도 (tokens/sec, Python 단일/12스레드)
| 토크나이저 | 단일 스레드 | 12 스레드 | 스케일링 |
|------------|-------------|-----------|----------|
| **GPT-4o (tiktoken)** | **150k** | **1.8M** | 12x [1] |
| GPT-4 (tiktoken) | 140k | 1.68M | 12x [1] |
| Llama 3 (SentencePiece) | 85k | 1.02M | 12x [1] |

- **메모리**: GPT-4o 2.3MB, GPT-4 **2.1MB 최저**, Llama 3 2.8MB[1].
- **대안 (TokenDagger)**: tiktoken보다 4x 빠름 (코드), 2-3x (1GB 텍스트, 단일스레드). Rust/JIT regex 최적화[3].

### 실전 프레임워크: 정확도 100% 보장 선택법
```
def select_tokenizer(text_type, scale_factor):
    if text_type == "code" or scale_factor > 1e9:  # 10억 토큰+
        return "tiktoken o200k_base"  # 5% 효율 ↑[1]
    elif memory_limit < 2.2e6:  # 2.2MB 미만
        return "tiktoken cl100k_base"  # 메모리 최저[1]
    else:
        return "SentencePiece"  # 멀티언어 우선[1]

# 사용 예: GPT-4o 메시지 토큰 수 (tiktoken 필수, 모델별 오버헤드 +3/-1)[2]
import tiktoken
enc = tiktoken.get_encoding("o200k_base")  # GPT-4o 전용
tokens = len(enc.encode("your text")) + 3  # <|start|>assistant<|end|> 등
```

### Claude-3-5/Gemini 대응 (추론 기반, 벤치 부족)
- **tiktoken**: GPT 전용 → Claude/Gemini에서 **부정확** (o200k_base는 GPT-4o 한정)[2].
- **HuggingFace tokenizers**: 범용 BPE 지원 (Gemini 1.5 ~150-180 tok/1k 영어 추정, 공식 벤치 미비). Llama 3처럼 5-10% 덜 효율[1].
- **테스트 프레임**: `tiktoken` vs `tokenizers.BertWordPieceTokenizer` 직접 비교 (variance ±10% 코드 기준)[1].

**최대 스케일 팁**: 12스레드 병렬 + GPT-4o = 1.8M tok/s → 1GB 텍스트 9초 처리[1]. CJK는 모든 BPE 약점 (~1k tok
