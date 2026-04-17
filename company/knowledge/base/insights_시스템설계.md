# 시스템설계 인사이트 모음

기획·개발·마케팅 과정에서 실제로 적용한 기법들


## 2026-04-05 04:02 (출처: https://www.instagram.com/p/DVz5qUgkbCv/)
*   캡션 작성 시 "X초 컷" 등 시간 기반 이점 문구를 필수 포함하는 워크플로우 확립.
*   영상 제작 가이드라인에 "시작 1초 이내 제품 노출"을 필수 항목으로 추가.
*   AI로 '구매 의도', '호기심' 댓글을 자동 분류하고, 구매 링크 포함 표준 응대 스크립트를 즉시 적용하는 워크플로우 구축.

## 2026-04-05 04:03 (출처: https://www.instagram.com/p/DWdycirlLto/)
*   AI 챗봇을 활용하여 댓글 및 DM의 가격 관련 질문에 자동 응답하는 시스템 구축.
*   영상 제작 워크플로우에 '시작 3초 내 비포/애프터 시각화' 및 '최종 길이 20-30초' 준수를 필수 검토 항목으로 추가.
*   모든 마케팅 카피라이팅(캡션, 스크립트) 워크플로우에 '문제-솔루션-행동강령' 구조 적용을 표준화.

## 2026-04-05 04:10 (출처: https://www.instagram.com/p/DVz5qUgkbCv/)
*   영상 편집 워크플로우에 '시작 1초 내 제품 노출' 규칙 의무화 및 AI 기반 준수 여부 자동 검수 시스템 도입.
*   캡션 제작 시 'X초 컷' 문구를 포함하는 템플릿을 표준화하고, AI로 해당 패턴의 캡션 초안 자동 생성.
*   댓글에서 '직구', '구매' 등 구매 신호 키워드 AI 자동 감지 및 CS/영업팀 실시간 알림/할당 워크플로우 구축.

## 2026-04-05 04:10 (출처: https://www.instagram.com/p/DWdycirlLto/)
- AI 글쓰기 도구를 '문제 → 솔루션 → 행동강령' 구조에 맞춰 프롬프트 엔지니어링하여 마케팅 카피 자동 생성 시스템을 구축한다.
- 댓글 가격 질문 빈도에 대응하여 AI 챗봇 또는 자동 응답 시스템을 구축, 가격 문의 시 표준화된 정보를 즉시 제공한다.
- 영상 제작 워크플로우에 '첫 3초 before/after 대비'를 필수로 포함하는 표준화된 인트로 가이드를 명시한다.

## 2026-04-17 07:43 (출처: https://www.instagram.com/p/DXBlIgDj3Dl/?img_index=2&igsh=MWRhZWtiNTJ2OGZodg==)
*   반복 업무 자동화를 위한 AI 에이전트 개발 및 기존 사내 시스템(메신저, ERP 등) 연동.
*   사내 SOP 및 지식 문서 기반 RAG 챗봇 구축으로 온보딩 및 Q&A 업무 자동화.
*   작업 특성별 최적 LLM 선정, 클라우드 기반 CLI/병렬 처리 및 AI API 리소스 관리로 워크플로우 효율화.

## 2026-04-17 07:51 (출처: https://www.instagram.com/p/DXBsJPUk1ov/?img_index=4&igsh=MXFwa2VycDNqMThjaA==)
- 모든 AI 자동화 기능(PDF 진단서, DM, CRM, 카드뉴스 생성)의 Claude API 호출 프롬프트 템플릿에 컨텍스트 요약, 구조화, 출력 제어, 시스템 프롬프트 활용 기법 즉시 적용.
- 이사팀, 영업팀, 마케팅팀, 납품팀 등 모든 에이전트의 Claude API 프롬프트에 `Task: [작업], Data: [데이터], Goal: [목표], Output: [형식]` 패턴을 표준화하여 적용.

## 2026-04-17 07:55 (출처: https://www.instagram.com/p/DW5M7tmAfN0/?img_index=1&igsh=YnN4YmJkN213dGw1)
- 마케팅팀의 카드뉴스 자동생성 워크플로우에 Formia 같은 툴을 활용한 2D 로고 3D 변환 및 AI 생성 이미지 합성 단계를 추가.
- 납품팀의 PDF 진단서 자동생성 시스템에 클라이언트 3D 로고를 표지에 적용하는 기능을 구현.
- Formia의 'Upload 2D -> Convert to 3D'와 같은 간결한 UI/UX를 내부 툴 및 core-shell 시스템 개발 시 워크플로우 설계 참고 자료로 활용.

## 2026-04-17 08:04 (출처: https://www.instagram.com/p/DWyVpqQCOf3/?img_index=3&igsh=MTllMTU3aXFodXpmeA==)
*   Claude Code 워크플로우 프롬프트 엔지니어링 및 토큰 관리 로직을 `agent-skills-for-context-engineering` 레포 기술(토큰 감소, 프롬프트 구조화, KV-캐시 최적화)로 개선하여 비용 절감 및 에이전트 품질 향상.
*   `skill-creator` 레포의 `Skill.md` 생성 로직을 활용하여 Claude Code 워크플로우의 에이전트 스킬 정의 시 `Skill.md` 파일을 자동 생성하고 일관된 워크플로우 구축.
*   `brand-guidelines` 레포의 브랜드 요소(톤, 스타일, 색상, 메시지) 인코딩 방법을 참조하여 마케팅/영업팀 AI 생성 콘텐츠(카드뉴스, DM)에 브랜드 일관성을 자동 적용.

## 2026-04-17 08:05 (출처: https://www.instagram.com/p/DXBxiZ8CBHJ/)
*   Google Stitch (`https://stitch.withgoogle.com`)로 영업/마케팅팀 고객 대시보드 UI를 자연어 입력으로 자동 생성하고, MCP를 통해 Claude Code (`https://code.claude.com/docs/ko/setup`)로 앱 코드를 즉시 자동 생성하는 파이프라인 구축.
*   카드뉴스 디자인 개선 워크플로우에 Google Stitch로 디자인 초안을 신속히 생성하고, MCP-Claude Code 연동으로 구현 코드를 자동 생성하여 디자인-개발 협업 효율화.
