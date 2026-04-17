# Claude Connectors 조사 결과

> 조사일: 2026-04-09 | 목적: core-shell 시스템 적용 가능성 평가

---

## 1. Claude Connectors란?

Claude가 외부 서비스(Gmail, Stripe, Supabase 등)를 **대화 안에서 직접 제어**할 수 있게 해주는 통합 기능. 모든 커넥터는 **MCP(Model Context Protocol)** 기반으로 구축됨.

### 두 가지 사용 경로

| 경로 | 설명 | 우리 시스템 적용 |
|------|------|-----------------|
| **claude.ai UI 커넥터** | 채팅 인터페이스에서 클릭으로 연결. OAuth 인증. Pro/Max/Team/Enterprise 유료 플랜 필요 | 리안 개인 사용 가능 |
| **Messages API MCP connector** | Python/TS SDK에서 프로그래매틱하게 MCP 서버 연결. API 키 과금 | **우리 파이프라인에서 사용 가능** |

### 현재 상태

- **UI 커넥터 디렉터리**: GA (2025-07-14 공개). 50개+ 커넥터. 매주 추가 중
- **API MCP connector**: Beta (`anthropic-beta: mcp-client-2025-11-20` 헤더 필요)
- **가격**: UI 커넥터는 유료 플랜(Pro $20/월~) 포함. API는 일반 Messages API 토큰 과금 + MCP 서버측 비용

---

## 2. 연동 가능한 서비스 (확인된 목록)

### 우리 사업 관련 핵심 서비스

| 서비스 | 커넥터 존재 | 기능 | 비고 |
|--------|------------|------|------|
| **Gmail** | 공식 (1st party) | 이메일 검색/읽기, 초안 작성, 라벨 관리 | 첨부파일 내용 접근 불가(메타데이터만) |
| **Google Calendar** | 공식 (1st party) | 일정 조회/생성/수정/삭제, 참석자 관리 | 공유 캘린더 포함 |
| **Google Drive** | 공식 (1st party) | 문서 검색/읽기, 파일 권한 조회 | 이미지 처리 불가 |
| **Stripe** | 공식 커넥터 | 고객 생성/관리, 결제 처리, 구독 관리, 환불, 인보이스 | Read & Write |
| **Supabase** | 공식 커넥터 | DB 테이블 설계/마이그레이션/쿼리, API 키 관리, 인증 설정 | MCP 서버 공식 제공 |
| **Jotform** | 공식 커넥터 | 폼 생성/편집, 제출 데이터 조회, 분석 | MCP 서버: mcp.jotform.com |
| **Notion** | 공식 커넥터 | 페이지/DB 읽기/쓰기 | |
| **Slack** | 공식 (1st party) | 메시지 전송/검색, 채널 관리 | |
| **monday.com** | 공식 커넥터 | 태스크 상태 확인/업데이트, 프로젝트 모니터링 | |

### 기타 확인된 커넥터

Salesforce, HubSpot, Apollo, Clay, Outreach, Figma, Canva, GitHub, GitLab, Jira, Linear, Sentry, Asana, ClickUp, Zapier, Cloudflare, Intercom, Plaid, Square, Twilio, DocuSign, Box, Indeed, ActiveCampaign, Airtable, Ahrefs, SimilarWeb, FactSet, Hex, Gamma, Granola, Vercel 등

---

## 3. 프로그래매틱 사용법 (Python 파이프라인)

### API MCP Connector로 우리 파이프라인에서 직접 호출 가능

```python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=1000,
    messages=[{"role": "user", "content": "최근 미결제 고객 목록 조회해줘"}],
    mcp_servers=[
        {
            "type": "url",
            "url": "https://mcp.stripe.com/sse",  # Stripe MCP 서버
            "name": "stripe",
            "authorization_token": "STRIPE_TOKEN",
        }
    ],
    tools=[{"type": "mcp_toolset", "mcp_server_name": "stripe"}],
    betas=["mcp-client-2025-11-20"],
)
```

### 핵심 제약사항

- MCP 서버가 **공개 HTTPS 엔드포인트**여야 함 (로컬 STDIO 서버 직접 연결 불가)
- **Beta 상태** — `anthropic-beta` 헤더 필수. 스펙 변경 가능성 있음
- MCP 스펙 중 **tool calls만 지원** (prompts, resources 미지원 — API에서)
- AWS Bedrock, Google Vertex에서는 미지원
- ZDR(Zero Data Retention) 미적용 — 데이터 보존됨
- OAuth 토큰은 **우리가 직접 획득/갱신** 관리해야 함

### 복수 서버 동시 연결 가능

한 번의 API 호출에서 Stripe + Supabase + Gmail을 동시에 연결할 수 있음.

---

## 4. 우리 시스템(core-shell) 적용 가능성 분석

### 현재 n8n 워크플로우 vs Connectors 대체 가능성

| 현재 워크플로우 | Connectors 대체 | 판단 |
|----------------|----------------|------|
| Jotform 폼 제출 → CRM 등록 | Jotform MCP + Supabase MCP로 체인 가능 | **가능** — 단, Claude API 호출 비용 발생 |
| Gmail DM 자동 발송 | Gmail 커넥터로 초안 작성 가능 | **부분 가능** — 자동 전송은 확인 필요 |
| Stripe 결제 자동화 | Stripe 커넥터로 고객/구독/인보이스 관리 | **가능** |
| Supabase CRM read/write | Supabase MCP로 직접 쿼리 가능 | **가능** |
| 카카오톡 발송 | 커넥터 없음 | **불가** — 기존 방식 유지 |
| 네이버 관련 작업 | 커넥터 없음 | **불가** — 기존 방식 유지 |

### Jotform → CRM → Gmail 체인 시나리오

**기술적으로 가능하지만 비효율적.** 이유:
1. 매 단계마다 Claude API 호출 필요 (토큰 비용)
2. n8n은 이벤트 트리거(webhook) 기반이라 실시간, Connectors는 폴링 또는 수동 호출
3. n8n의 단순 데이터 이동에 LLM을 끼우면 과잉 설계

**Connectors가 유리한 경우:**
- 데이터를 **해석/판단/생성**해야 하는 단계 (예: 고객 데이터 보고 맞춤 이메일 작성)
- AI가 **여러 서비스를 동시에 참조**해야 하는 경우 (예: CRM + 결제 + 캘린더 크로스체크)

---

## 5. 우선순위 액션 아이템

### 즉시 적용 가능 (높은 가치)

1. **Supabase MCP → CRM 에이전트 강화**
   - 현재: Python에서 직접 Supabase API 호출
   - 변경: 에이전트가 MCP로 CRM 데이터 직접 조회/수정하면서 자연어로 복합 쿼리 가능
   - 예: "최근 30일 미접촉 고객 중 매출 상위 10개 업체 뽑아줘"

2. **Stripe MCP → 결제/구독 관리 자동화**
   - 견적서 발행, 결제 상태 확인, 미결제 알림을 에이전트가 직접 처리

### 중기 적용 (테스트 후)

3. **Gmail MCP → 영업 이메일 자동화**
   - 에이전트가 CRM 데이터 참조하면서 맞춤 이메일 초안 작성 + 발송
   - 주의: Gmail 커넥터의 자동 발송 범위 확인 필요

4. **Google Calendar MCP → 미팅 일정 자동 관리**
   - 영업 미팅 스케줄링 자동화

### 보류 (n8n 유지가 나은 것)

5. **단순 데이터 이동 워크플로우** — n8n이 비용/속도 모두 우월
6. **카카오톡/네이버 연동** — 커넥터 없음. 기존 방식 유지
7. **실시간 이벤트 트리거** — n8n webhook이 적합. Connectors는 폴링 방식

---

## 6. 결론

**Claude Connectors(MCP)는 "AI가 판단하면서 외부 서비스를 제어"하는 시나리오에 강력함.**
단순 데이터 이동은 n8n, 판단이 필요한 복합 작업은 Connectors로 **하이브리드 구성**이 최적.

우리 Python 파이프라인에서 Messages API MCP connector로 **프로그래매틱하게 사용 가능** 확인됨.
다만 Beta 상태이므로 프로덕션 의존도는 점진적으로 높이는 것이 안전.

핵심 한계: 한국 서비스(카카오, 네이버) 커넥터가 없어서 우리 핵심 채널은 여전히 직접 구현 필요.

---

## 출처

- [Claude Connectors Directory](https://claude.com/blog/connectors-directory)
- [MCP Connector API Docs](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)
- [Google Workspace Connectors Help](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)
- [Custom Connectors via Remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)
- [Supabase MCP Server](https://supabase.com/docs/guides/getting-started/mcp)
- [Jotform MCP Server](https://www.jotform.com/developers/mcp/)
- [Stripe Connector](https://claude.com/connectors/stripe)
- [Claude Pricing](https://claude.com/pricing)
