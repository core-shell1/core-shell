# core-shell 전용 Claude Custom Skills 설계서

> 작성일: 2026-04-09
> 목적: Claude Skill Creator로 제작할 core-shell 전용 커스텀 스킬 5개 설계

---

## Claude Skills란?

Claude Skills는 `.claude/skills/<이름>/SKILL.md` 형식의 폴더 기반 확장 도구다.
- **SKILL.md** 파일 1개 필수 (YAML frontmatter + Markdown 지시문)
- 선택적으로 scripts/, references/, templates/ 등 보조 파일 추가 가능
- SKILL.md 500줄 이내 권장, 상세 자료는 별도 파일로 분리
- `name` (64자) + `description` (200자) 필수 — description이 자동 호출 트리거

### SKILL.md 기본 구조
```yaml
---
name: skill-name
description: "트리거 설명. Use when [조건]."
allowed-tools: ["Bash", "Read", "Write"]
---
# 지시문 (Markdown)
```

### 배치 위치
프로젝트 레벨: `.claude/skills/<이름>/SKILL.md`
글로벌: `~/.claude/skills/<이름>/SKILL.md`

---

## 스킬 1: 소상공인 PDF 진단서 생성

### SKILL.md
```yaml
---
name: diagnosis-pdf
description: "소상공인 네이버 플레이스 진단서 PDF 생성. Use when 업체명/업종/진단 데이터로 PDF 진단서를 만들 때."
allowed-tools: ["Bash", "Read", "Write", "Edit"]
---
```

### 입력
| 필드 | 필수 | 예시 |
|------|------|------|
| business_name | O | "헤어림 미용실" |
| category | O | "미용실" |
| address | X | "경기도 양주시..." |
| diagnosis_data | O | DB에서 가져온 DiagnosisHistory 레코드 또는 JSON |

### 출력
- HTML 기반 PDF 진단서 (html_templates/ 중 업종 맞는 템플릿 자동 선택)
- 7개 항목 점수 (사진/리뷰/블로그/정보/키워드/편의기능/참여도)
- 개선 포인트 3개 + 예상 효과

### 프롬프트 핵심 지시문
```markdown
# 실행 순서
1. diagnosis.db에서 해당 업체 데이터 조회 (없으면 JSON 직접 파싱)
2. scorer.py 로직으로 7개 항목 점수 산출
3. 업종 감지 → industry_weights.py에서 가중치 적용
4. html_templates/ 중 업종 톤에 맞는 템플릿 선택:
   - 미용실/뷰티: template_10_pastel_modern
   - 카페/음식: template_04_energy_orange
   - 전문직/의료: template_01_dark_premium
   - 기본: template_02_clean_white
5. generate_html_pdf.py 호출하여 PDF 생성

# 규칙
- 총점은 100점 만점, 등급은 A~F (A:90+ B:80+ C:70+ D:60+ E:50+ F:50미만)
- 개선 포인트는 점수 낮은 순 3개, 각각 "현재 → 목표 → 예상 효과" 포맷
- 경쟁사 평균 대비 표현 필수 ("같은 지역 미용실 평균 72점 대비 54점")
```

### 파이프라인 삽입 위치
`naver-diagnosis/main.py` 크롤링 완료 후 → 이 스킬 호출 → PDF 생성 → CRM에 자동 등록

---

## 스킬 2: 업종별 DM 템플릿 자동 선택

### SKILL.md
```yaml
---
name: dm-template
description: "업종/등급별 최적 영업 DM 메시지 생성. Use when 소상공인에게 보낼 DM이나 영업 메시지를 만들 때."
allowed-tools: ["Bash", "Read"]
---
```

### 입력
| 필드 | 필수 | 예시 |
|------|------|------|
| category | O | "카페" |
| grade | O | "D" |
| business_name | O | "카페 모닝" |
| pain_points | X | ["사진 0장", "리뷰 3개"] |
| stage | X | "1차" (기본값) / "2차" / "거절대응" |

### 출력
- 해당 단계의 완성된 DM 메시지 (복붙 가능)
- 3가지 버전 (공감형 / 데이터형 / 손실강조형)
- 각 버전별 "왜 이 접근인지" 1줄 설명

### 프롬프트 핵심 지시문
```markdown
# 업종별 톤 매트릭스
- 미용실/네일: 친근 + 비주얼 강조 ("인스타에 예쁜 시술 사진이 있으면...")
- 카페/음식점: 감성 + 후기 강조 ("요즘 카페 고르는 기준, 리뷰 먼저 보잖아요")
- 의료/전문직: 신뢰 + 데이터 ("월 검색량 8,000회인데 노출 순위가...")
- 학원/교육: 학부모 시선 + 비교 ("근처 학원 3곳은 이미 블로그 리뷰가...")
- 기타 서비스: 범용 손실 프레임 ("매달 놓치는 고객이 약 X명...")

# 메시지 규칙 (message_generator.py 원칙 준수)
- 문제는 확실히 보여주되 해결법은 절대 안 알려준다
- 총액(6개월 합계) 노출 금지 → 월 단위로만 표현
- [업체명], [지역] 변수 자동 치환
- CTA는 "무료 진단서 보내드릴까요?" 또는 "10분 통화 가능하실까요?"
- 이모지 최소 (프로페셔널 톤 유지)
```

### 파이프라인 삽입 위치
`sales_crm/app.py` 채팅 메시지 생성 시 → 이 스킬 호출 → 업종+등급 기반 최적 DM 반환

---

## 스킬 3: 멀티채널 콘텐츠 변환

### SKILL.md
```yaml
---
name: multichannel
description: "하나의 원본 콘텐츠를 인스타/블로그/카카오 3채널로 최적화 변환. Use when 콘텐츠를 여러 채널에 맞게 변환할 때."
allowed-tools: ["Bash", "Read", "Write"]
---
```

### 입력
| 필드 | 필수 | 예시 |
|------|------|------|
| source_content | O | 원본 텍스트 (블로그 글, 기획안 등) |
| target_channels | X | ["instagram", "blog", "kakao"] (기본: 전부) |
| brand_tone | X | "친근+전문" |
| cta_link | X | "https://..." |

### 출력
각 채널별 완성된 콘텐츠:
- **인스타**: 캡션 (2200자 이내) + 해시태그 30개 + 캐러셀 슬라이드 텍스트 안
- **블로그**: 네이버 SEO 최적화 본문 (H2/H3 구조, 키워드 밀도 2-3%)
- **카카오**: 채널 메시지용 짧은 카드 (제목 20자 + 설명 50자 + CTA)

### 프롬프트 핵심 지시문
```markdown
# 채널별 최적화 규칙

## 인스타그램
- 첫 줄 = 후킹 (질문/충격/공감 중 택1, hook_library.md 참고)
- 줄바꿈 활용 (3줄마다 공백줄)
- 해시태그: 대형(100만+) 5개 + 중형(1만~100만) 15개 + 소형(1만 미만) 10개
- CTA: "저장하고 나중에 다시 보세요" 또는 "DM으로 무료 상담"

## 네이버 블로그
- 제목: 핵심키워드 앞배치 + 숫자 활용 ("2026년 양주 미용실 마케팅 3가지 핵심")
- 본문 1500자 이상, 이미지 삽입 위치 표시 [이미지: 설명]
- 소제목 H2 3개 이상, 각 섹션 300자 이상
- 마무리: 업체 정보 + 네이버 플레이스 링크

## 카카오 채널
- 제목 20자, 설명 50자 이내 (잘리지 않게)
- 버튼: "자세히 보기" + 링크
- 톤: 간결하고 직접적
```

### 파이프라인 삽입 위치
`온라인납품팀/pipeline.py` 콘텐츠 생성 후 → 이 스킬로 3채널 동시 변환
`daily_auto.py` 매일 콘텐츠 생성 시 자동 호출

---

## 스킬 4: 브랜드 톤 자동 적용

### SKILL.md
```yaml
---
name: brand-tone
description: "클라이언트 브랜드 정보를 분석해 모든 콘텐츠에 일관된 톤/보이스 적용. Use when 특정 브랜드 톤으로 콘텐츠를 작성하거나 수정할 때."
allowed-tools: ["Read", "Write"]
---
```

### 입력
| 필드 | 필수 | 예시 |
|------|------|------|
| brand_info | O | 업체명, 업종, 타겟 고객, 기존 콘텐츠 샘플 |
| content | O | 톤 적용할 원본 텍스트 |
| output_type | X | "dm" / "blog" / "instagram" / "ppt" |

### 출력
- 브랜드 톤 프로필 (첫 호출 시 자동 생성, 이후 재사용)
- 톤 적용된 콘텐츠
- 톤 일관성 체크리스트 (5항목 통과/미통과)

### 프롬프트 핵심 지시문
```markdown
# 브랜드 톤 추출 프로세스
1. brand_info에서 키워드 추출: 업종 특성, 타겟 연령대, 가격대, 분위기
2. 톤 매트릭스 4축 점수화 (각 1~10):
   - 격식도: 캐주얼(1) ↔ 포멀(10)
   - 감성도: 이성적(1) ↔ 감성적(10)
   - 에너지: 차분(1) ↔ 활기(10)
   - 전문도: 대중적(1) ↔ 전문적(10)
3. 점수 조합 → 톤 키워드 3개 도출 (예: "따뜻한 + 전문적 + 차분한")

# 톤 적용 규칙
- 문장 길이: 격식도 높으면 긴 문장 허용, 낮으면 15자 이내 짧은 문장
- 이모지: 감성도 7 이상이면 허용, 미만이면 금지
- 존칭: 격식도 6 이상이면 "~합니다", 미만이면 "~해요"
- 전문 용어: 전문도 7 이상이면 업종 용어 사용, 미만이면 쉬운 말로 풀어쓰기

# 톤 프로필 저장
knowledge/teams/{클라이언트명}_brand_tone.json에 저장
다음 호출 시 자동 로드하여 일관성 유지
```

### 파이프라인 삽입 위치
모든 콘텐츠 생성 에이전트(copywriter.py, 온라인납품팀 전원)의 최종 출력 전 → 이 스킬로 톤 검증+적용
`offline_sales.py` 영업 자료 생성 시 클라이언트별 톤 자동 적용

---

## 스킬 5: 영업 성과 분석

### SKILL.md
```yaml
---
name: sales-analytics
description: "CRM 데이터에서 영업 성과 분석 — 전환율, 응답률, 최적 시간대, 업종별 성과. Use when 영업 성과를 분석하거나 전략을 개선할 때."
allowed-tools: ["Bash", "Read"]
---
```

### 입력
| 필드 | 필수 | 예시 |
|------|------|------|
| period | X | "이번 주" / "이번 달" / "전체" (기본: 전체) |
| focus | X | "전환율" / "업종별" / "시간대" / "전체" (기본: 전체) |

### 출력
- 핵심 지표 대시보드 (전환율, 응답률, 평균 응답시간)
- 업종별 성과 랭킹 (어떤 업종이 전환율 높은지)
- 최적 DM 발송 시간대 (응답률 기준)
- 가장 효과적인 DM 버전 (A/B/C 중)
- 다음 주 액션 제안 3가지

### 프롬프트 핵심 지시문
```markdown
# 데이터 소스
1. sales_crm.db: conversations 테이블 (업체별 대화 기록, 상태, 타임스탬프)
2. diagnosis.db: diagnosis_history 테이블 (진단 점수, 업종, 지역)

# 분석 프레임워크
## 전환 퍼널
DM 발송 → 읽음 → 답장 → 통화 → 계약
각 단계 이탈률 계산, 병목 지점 식별

## 업종별 분석
업종 그룹핑 → 각 그룹의 평균 전환율/응답률/계약 단가
상위 3개 업종 = "공격 대상", 하위 3개 업종 = "보류 또는 접근 변경"

## 시간대 분석
DM 발송 시각 vs 응답 시각 → 응답률 높은 시간대 도출
요일별 패턴 포함

## DM 효과 분석
버전(A/B/C)별 응답률 비교 → 가장 효과적인 메시지 패턴 식별

# 출력 형식
숫자는 반드시 % 또는 건수로 표현. "좋다/나쁘다" 같은 추상적 표현 금지.
액션 제안은 "~하면 전환율 X% 개선 예상" 형식으로 구체적 수치 포함.
```

### 파이프라인 삽입 위치
`daily_auto.py` 주간 루프에서 자동 호출 → 보고사항들.md에 주간 성과 리포트 저장
`ops_loop.py` 성과 리뷰 시 이 스킬로 데이터 기반 방향 수정 제안

---

## 구현 순서 (우선순위)

| 순서 | 스킬 | 이유 |
|------|------|------|
| 1 | dm-template | 현재 영업 진행중, 즉시 효과 |
| 2 | diagnosis-pdf | CRM 연동으로 영업 효율 극대화 |
| 3 | sales-analytics | 데이터 쌓이면 바로 필요 |
| 4 | multichannel | 온라인 마케팅 본격화 시 |
| 5 | brand-tone | 클라이언트 수 늘어나면 |

## 설치 방법

```bash
# 각 스킬 폴더 생성
mkdir -p .claude/skills/diagnosis-pdf
mkdir -p .claude/skills/dm-template
mkdir -p .claude/skills/multichannel
mkdir -p .claude/skills/brand-tone
mkdir -p .claude/skills/sales-analytics

# SKILL.md 배치 후 Claude Code 재시작하면 자동 인식
# /diagnosis-pdf 또는 /dm-template 로 슬래시 커맨드 호출 가능
# description 매칭되면 자동 호출도 됨
```
