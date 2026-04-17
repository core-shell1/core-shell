# AI 에이전트 도구/리소스 조사 (2026-04-09)

## 1. Oneshot — 스크린샷 → AI 에이전트 전달 유틸리티

**GitHub:** https://github.com/Kalypsokichu-code/shots-for-agents
**사이트:** https://oneshot.zip/
**라이선스:** MIT | **플랫폼:** macOS 전용 (Swift + ScreenCaptureKit)
**Stars:** 11 (소규모 프로젝트)

### 핵심 메커니즘
- 스크린샷 캡처 → localhost HTTP 서버(9853)에 저장 → curl 명령어를 클립보드에 복사
- AI 에이전트가 URL fetch는 못하지만 shell 명령은 실행 가능하다는 점 활용
- `curl -s -o /tmp/shot-A1B2C3D4.png http://localhost:9853/s/A1B2C3D4.png`
- 1회 읽으면 자동 삭제 (미열람 10분, 열람 후 60초 만료)
- 메모리에만 저장, 앱 종료 시 전부 소멸

### 우리 시스템 적용 가능성
- **직접 사용: 불가** — macOS 전용, Swift 네이티브
- **벤치마킹 가능한 아이디어:**
  - 로컬 HTTP 서버로 에이전트에게 시각 자료 전달하는 패턴
  - 우리 분석팀(Gemini Vision)이 스크린샷 분석할 때 유사 구조 적용 가능
  - Python으로 Flask/FastAPI 미니 서버 + 자동만료 엔드포인트 구현하면 동일 효과
  - 현재 우리는 파일 경로 직접 전달 방식이므로 더 단순 → 교체 필요 없음

---

## 2. 우리 시스템에 적용 가능한 도구 (우선순위순)

### A. Langfuse — LLM 모니터링/관찰 (★★★ 강력 추천)
- **GitHub:** https://github.com/langfuse/langfuse (오픈소스, 셀프호스팅 가능)
- **핵심:** 모든 LLM 호출 추적, 비용 계산, 성능 분석, 프롬프트 버전 관리
- **Python:** `@observe()` 데코레이터 2줄로 기존 코드에 통합
- **적용:** 우리 에이전트(Claude/GPT/Gemini/Perplexity) 전부 추적 가능
- **왜 필요:** 현재 어떤 에이전트가 토큰/비용을 얼마나 쓰는지 추적 불가 → 이걸로 해결
- **도입 난이도:** 낮음 (Docker 셀프호스팅 or 클라우드 무료 플랜)

### B. AgentOps — 에이전트 세션 리플레이 (★★☆)
- **GitHub:** https://github.com/agentops-ai/agentops (MIT 라이선스)
- **핵심:** 에이전트 실행 과정 녹화/재생, 실패 감지, 비용 추적
- **Python:** `pip install agentops` → 2줄로 통합
- **적용:** 팀 파이프라인 실행 시 각 에이전트 동작 추적 + 디버깅
- **무료 플랜:** 5,000 이벤트/월 — 우리 규모에 충분
- **도입 난이도:** 매우 낮음

### C. Crawl4AI — 웹 크롤링 → LLM용 마크다운 (★★★ 강력 추천)
- **GitHub:** https://github.com/unclecode/crawl4ai (58K+ stars, 오픈소스)
- **핵심:** 웹페이지를 LLM이 읽기 좋은 마크다운으로 변환
- **Python:** `pip install crawl4ai` — 완전 Python 네이티브
- **적용:**
  - 온라인영업팀 잠재고객 웹사이트 분석 자동화
  - 오프라인마케팅팀 경쟁사 분석
  - Perplexity 대체/보완으로 직접 크롤링 → 비용 절감
- **도입 난이도:** 낮음

### D. Browser Use — AI 브라우저 자동화 (★★☆)
- **GitHub:** https://github.com/browser-use/browser-use (78K+ stars)
- **핵심:** AI가 브라우저를 사람처럼 조작 (클릭, 입력, 스크롤)
- **Python:** Playwright 기반, LangChain 통합
- **적용:**
  - 인스타그램/네이버 자동 작업 (현재 수동 스크립트 대체)
  - 소상공인 네이버플레이스 데이터 자동 수집
- **주의:** Playwright 의존 → 이미 우리 환경에 있으므로 호환 문제 없음
- **도입 난이도:** 중간 (에이전트 연동 설계 필요)

### E. Composio — 외부 서비스 통합 레이어 (★☆☆ 참고용)
- **GitHub:** https://github.com/ComposioHQ/composio (27K stars, 오픈소스)
- **핵심:** 500+ 앱 연동 (카카오톡/슬랙/노션 등) + OAuth 자동 처리
- **적용:** 디스코드/카카오톡 연동 시 인증 처리 자동화
- **현재 필요도:** 낮음 — 우리는 아직 외부 서비스 연동이 적음

### F. n8n — 비주얼 워크플로우 자동화 (★☆☆ 참고용)
- **GitHub:** https://github.com/n8n-io/n8n (150K+ stars)
- **핵심:** 노코드 AI 에이전트 워크플로우 빌더, 500+ 앱 연동
- **셀프호스팅:** Docker로 무료 무제한 실행
- **적용:** daily_auto.py 같은 스케줄 작업을 GUI로 관리 가능
- **현재 필요도:** 낮음 — 우리는 Python 직접 실행이 더 빠르고 유연

---

## 3. 에이전트 프레임워크 현황 (2026년 기준)

| 프레임워크 | Stars | 특징 | 우리 시스템 관련성 |
|-----------|-------|------|------------------|
| LangGraph | 24K | 그래프 기반 멀티에이전트 오케스트레이션 | 중 — 파이프라인 복잡해지면 검토 |
| CrewAI | 44K | 역할 기반 에이전트 팀 (우리와 유사) | 높 — 설계 참고용 벤치마크 |
| OpenAI Agents SDK | 19K | 경량 멀티에이전트 프레임워크 | 중 — GPT 에이전트 전환 시 |
| Anthropic Agent SDK | 4.6K | Claude 네이티브 에이전트 | 높 — Claude 기반 에이전트 개선 시 |
| Pydantic AI | - | 타입 안전 에이전트 + 평가 시스템 | 중 — 에이전트 평가 도구로 |
| Google ADK | 17K | Gemini 최적화 에이전트 키트 | 중 — 하은/분석팀 업그레이드 시 |
| Smolagents (HuggingFace) | - | 경량, 즉시 Python 실행 | 낮 — 오픈소스 모델 전용 |

---

## 4. 주요 리소스 디렉토리

- **AI Agents Directory:** https://aiagentslist.com/ — 600+ AI 도구/에이전트 목록
- **StackOne 2026 Landscape:** https://www.stackone.com/blog/ai-agent-tools-landscape-2026/ — 120+ 도구 11개 카테고리
- **awesome-ai-agents-2026:** https://github.com/caramaschiHG/awesome-ai-agents-2026 — 300+ 리소스 GitHub 목록
- **Firecrawl 프레임워크 비교:** https://www.firecrawl.dev/blog/best-open-source-agent-frameworks — 오픈소스 프레임워크 비교

---

## 5. 즉시 적용 액션 플랜

| 순서 | 도구 | 작업 | 효과 |
|------|------|------|------|
| 1 | Crawl4AI | pip install → 영업팀 잠재고객 웹 분석에 적용 | 크롤링 비용 0원, Perplexity 호출 절감 |
| 2 | Langfuse | Docker 설치 → 전 에이전트 @observe() 적용 | 토큰/비용/성능 실시간 대시보드 |
| 3 | AgentOps | pip install → pipeline.py에 2줄 추가 | 에이전트 실행 디버깅 + 실패 자동 감지 |
| 4 | Browser Use | 인스타 자동화 스크립트 고도화 | 수동 스크립트 → AI 자율 브라우징 |

> CrewAI는 우리 시스템과 가장 유사한 "역할 기반 에이전트 팀" 구조.
> 설계 패턴 참고용으로 코드 분석 추천 (전환할 필요 없이 아이디어만 벤치마킹).
