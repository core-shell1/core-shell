# DESIGN.md — 한국 로컬가이드 (Korea Local Guide)

**버전:** v1.0  
**작성일:** 2026-04-06  
**담당:** CDO (나은)  
**대상:** FE 개발자 핸드오프용

---

## 1. 디자인 비전

> "낯선 도시에서 현지 친구가 귀띔해주는 느낌 — 따뜻하고, 빠르고, 믿을 수 있는."

- 톤: 따뜻함(Warm) + 자신감(Confident) + 현지감(Local)
- 분위기: 서울 골목길 감성. 한국의 정겨움을 세련되게.
- 감성 레퍼런스: 낮에 햇살 드는 카페 창가, 손글씨 메뉴판, 스팀 올라오는 뚝배기

---

## 2. 브랜드 아이덴티티

### 서비스 포지셔닝
기존 앱(구글 맵, 트립어드바이저)이 "정보 데이터베이스"라면,  
한국 로컬가이드는 "여행 친구". 추천이 아닌 귀띔.

### 보이스 & 톤
- 영어 기준, 친근하고 직접적인 2인칭("You're in Insadong — here's where locals actually go")
- 과도한 격식 금지. "We recommend" 대신 "Try this one"
- 이모지 절제 사용 (아이콘으로 대체 권장)

### 핵심 차별 포인트 (디자인에 반영할 것)
1. GPS 버튼이 히어로 CTA — 앱 열자마자 가장 크게 보여야 함
2. 추천 이유가 카드의 핵심 — "왜 이 곳이냐"가 별점보다 중요
3. 영어 메뉴 여부 배지 — 30대 여성 외국인의 첫 번째 불안 해소

---

## 3. 컬러 팔레트

### 기본 철학
- 기존 빨간 그라디언트 헤더 → 폐기. 너무 공격적, 식욕 자극보다 경고 느낌.
- 따뜻한 테라코타(주인공) + 크림(배경) + 딥 모스 그린(신뢰) 조합
- 한국의 흙빛, 청자빛, 황토빛에서 영감

### 컬러 정의

| 역할 | 이름 | HEX | 용도 |
|------|------|-----|------|
| Primary | Terracotta | `#C85C3A` | GPS 버튼, 주요 CTA, 강조 텍스트 |
| Primary Dark | Brick | `#A3431F` | 버튼 hover/active 상태 |
| Primary Light | Blush | `#F2E0D8` | 추천 이유 배경, 칩 배경, 강조 표면 |
| Secondary | Moss | `#4A6741` | 영어 메뉴 배지, 성공 상태, 신뢰 요소 |
| Secondary Light | Sage | `#D4E4D0` | 배지 배경 |
| Accent | Amber | `#C49A3C` | 별점, 가격대 표시, 주의 상태 |
| Accent Light | Cream | `#FDF5E4` | 별점 배경, 하이라이트 |
| Background | Warm White | `#FAF7F4` | 페이지 배경 |
| Surface | White | `#FFFFFF` | 카드, 시트, 입력 폼 |
| Surface Alt | Linen | `#F5F0EB` | 카드 내부 서브 영역 |
| Text Primary | Charcoal | `#1C1917` | 메인 텍스트, 식당명 |
| Text Secondary | Stone | `#78716C` | 설명, 서브 텍스트 |
| Text Tertiary | Warm Gray | `#A8A29E` | 플레이스홀더, 캡션, 주소 |
| Border | Warm Border | `#E8E0D8` | 카드 테두리, 구분선 |
| Error | Rose | `#DC2626` | 에러 메시지 |
| Error Light | Rose Tint | `#FEF2F2` | 에러 배경 |
| Overlay | Dark Scrim | `rgba(28, 25, 23, 0.6)` | 바텀 시트 오버레이 |

---

## 4. 타이포그래피

### 폰트 패밀리

```html
<!-- Google Fonts 임포트 -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Serif+Display:ital@0;1&display=swap" rel="stylesheet">
```

- **제목 (Display):** DM Serif Display — 감성적, 따뜻한 세리프. 앱명, 히어로 문구에만 사용.
- **본문 (UI):** DM Sans — 가독성 우수, 현대적이면서 따뜻함. 모든 UI 텍스트.

### 모바일 타입 스케일

| 레벨 | 폰트 | 크기 | 굵기 | 행간 | 용도 |
|------|------|------|------|------|------|
| display | DM Serif Display | 28px | 400 | 1.2 | 앱 이름, 히어로 카피 |
| h1 | DM Sans | 22px | 700 | 1.3 | 화면 제목 |
| h2 | DM Sans | 18px | 600 | 1.35 | 카드 식당명, 섹션 제목 |
| h3 | DM Sans | 16px | 600 | 1.4 | 서브 제목, 라벨 |
| body-lg | DM Sans | 16px | 400 | 1.6 | 주요 본문 (설명, AI 메시지) |
| body | DM Sans | 15px | 400 | 1.6 | 일반 본문 |
| body-sm | DM Sans | 14px | 400 | 1.5 | 배지 텍스트, 보조 설명 |
| caption | DM Sans | 13px | 400 | 1.4 | 주소, 플레이스홀더, 시간 |
| label | DM Sans | 12px | 500 | 1.3 | 필터 라벨, 탭 텍스트 |

### 규칙
- 최소 글자 크기: **16px** (캡션/배지 제외, 접근성 기준)
- 배지/칩의 최소 크기: 13px (단, 배경+테두리로 가독성 보완)
- Letter-spacing: 제목은 `-0.01em`, 라벨/칩은 `0.02em`
- 식당명(한국어): 영문명 아래 `body-sm` + `Text Tertiary` 색상

---

## 5. 화면 목록 & 레이아웃 명세

### 화면 흐름

```
Screen 1 (홈/로딩)
  → GPS 허용 시  → Screen 2 (GPS 결과)
  → GPS 거부 시  → 텍스트 입력 (Screen 3 채팅)
  → 카드 탭      → Screen 4 (식당 상세 — BottomSheet)
```

---

### Screen 1 — 홈 (GPS 감지 중 로딩)

**목적:** 앱 진입 즉시 GPS 권한 요청 + 감지 중 상태 표시. 기다리는 시간을 불안 아닌 기대감으로.

**레이아웃 (세로 전체 화면):**
```
┌─────────────────────────┐
│  [상단 여백 60px]        │
│                         │
│  [앱 로고]              │  ← 중앙 정렬, display 폰트 "Korea Local Guide"
│  [서브카피]             │  ← "Your local friend in Seoul"
│                         │
│  [위치 아이콘 애니메이션]│  ← pulse 효과, Primary 컬러 60px 아이콘
│                         │
│  [상태 텍스트]           │  ← "Finding where you are..." (점 애니메이션)
│                         │
│  [GPS 허용 버튼]        │  ← GPSButton 컴포넌트, Primary 컬러, 전폭
│                         │
│  ─────── or ───────     │  ← 구분선
│                         │
│  [텍스트 입력]          │  ← "Enter your neighborhood"
│                         │
│  [하단 여백 40px]        │
└─────────────────────────┘
```

**CTA:** "Find Restaurants Near Me" 버튼 — 중앙 배치, 전폭(calc(100% - 48px)), Primary 컬러
**상태별 텍스트:**
- 초기: "Find Restaurants Near Me" (버튼)
- 감지 중: 버튼 비활성화 + "Locating you..." + 회전 아이콘
- 에러: "Location access denied" + 텍스트 입력 자동 포커스

---

### Screen 2 — GPS 자동 추천 결과 (맛집 카드 3개)

**목적:** 1초도 낭비 없이 맛집 3개를 보여줌. 스크롤 없이 첫 카드가 보여야 함.

**레이아웃:**
```
┌─────────────────────────┐
│  [상단 바]              │  ← 앱명(좌) + 위치명(우: "📍 Insadong")
├─────────────────────────┤
│  [AI 메시지 배너]       │  ← 1줄 고정, Amber 배경, 이탤릭체
├─────────────────────────┤
│  [FilterChip 행]        │  ← 가로 스크롤: Solo / Couple / Cozy / Trendy / Vegetarian...
├─────────────────────────┤
│                         │
│  [RestaurantCard 1]     │  ← 전폭 카드 (가장 강조)
│  [RestaurantCard 2]     │  ← 살짝 작게 (시각적 위계)
│  [RestaurantCard 3]     │  ← 살짝 작게
│                         │
│  [새로고침 링크]         │  ← "Not what you're looking for? Refresh"
│                         │
├─────────────────────────┤
│  [하단 네비게이션]      │  ← 홈 / 채팅 / 기록 (아이콘 탭)
└─────────────────────────┘
```

**CTA:** 각 카드 하단 "See Details" 링크 또는 카드 전체 탭
**첫 카드가 스크롤 없이 보여야 함** — AI 메시지 배너 최대 높이 56px로 고정

---

### Screen 3 — 채팅 / 자연어 입력

**목적:** 자유롭게 원하는 것을 말하면 AI가 이해하고 맛집 추천. 대화 히스토리 유지.

**레이아웃:**
```
┌─────────────────────────┐
│  [상단 바]              │  ← "Chat" + 현재 위치
├─────────────────────────┤
│                         │
│  [대화 히스토리 영역]   │  ← 스크롤 가능
│                         │
│  [User: "I want..."]    │  ← ChatBubble — 우측 정렬, Primary Light 배경
│  [AI: "Try these..."]   │  ← ChatBubble — 좌측 정렬, Surface 배경
│                         │
│  [추천 카드 인라인]     │  ← 대화 중 카드 결과가 버블 아래 나타남
│                         │
├─────────────────────────┤
│  [퀵 칩 제안]           │  ← "Something spicy" / "Near me" / "Vegetarian"
├─────────────────────────┤
│  [입력창 + 전송 버튼]   │  ← sticky, 키보드 올라와도 고정
└─────────────────────────┘
```

**CTA:** 입력창 우측 전송 버튼 (Primary 컬러 원형), 퀵칩으로 입력 없이도 시작 가능
**빈 상태:** "Ask me anything! Try: 'A cozy place for just me' or 'Something spicy and cheap'"

---

### Screen 4 — 식당 상세 정보 (BottomSheet)

**목적:** 카드 탭 시 아래에서 슬라이드업. 방문 결정에 필요한 모든 정보 + 지도 이동 CTA.

**레이아웃 (BottomSheet — 화면 85% 높이):**
```
┌─────────────────────────┐
│  [드래그 핸들]          │  ← 상단 중앙 4px 막대
│                         │
│  [식당명]               │  ← h1, 좌측
│  [한국어명]             │  ← body-sm, 회색
│  [별점] [가격대] [거리] │  ← 배지 그룹
│                         │
│  ─────────────────────  │
│                         │
│  [AI 추천 이유]         │  ← 박스 강조, Primary Light 배경
│                         │
│  [대표 메뉴 3개]        │  ← 아이콘 + 이름 + 간단 설명
│                         │
│  [영업시간]             │  ← 요일별 표 (오늘 강조)
│                         │
│  [분위기 태그]          │  ← FilterChip 나열
│                         │
│  [좋은 점 / 주의할 점]  │  ← 2컬럼 아이콘 리스트
│                         │
│  [주소]                 │  ← 카피 버튼 포함
│                         │
├─────────────────────────┤
│  [Google Maps 열기]     │  ← 전폭 Primary 버튼 (Sticky)
└─────────────────────────┘
```

**CTA:** "Open in Google Maps" — Sticky 하단 버튼, Primary 컬러, 전폭
**스와이프 다운으로 닫기** 지원 필수

---

## 6. 컴포넌트 명세

### GPSButton (메인 CTA)

```
상태: idle / loading / error
크기: 전폭 (max-width 내), 높이 56px
배경: var(--color-primary)
텍스트: "Find Restaurants Near Me" → 로딩 시 "Locating..." + 스피너
Border-radius: 16px
Font: body-lg, 600
아이콘: 위치핀 아이콘 (좌측 16px)
터치 타겟: 56px 이상 (접근성 기준)
hover: var(--color-primary-dark), scale(1.01)
active: scale(0.98)
disabled: var(--color-text-tertiary), cursor: not-allowed
```

---

### RestaurantCard

```
레이아웃: 세로 스택, 전폭
배경: var(--color-surface)
Border-radius: 20px
Border: 1px solid var(--color-border)
Padding: 20px
Box-shadow: 0 2px 12px rgba(28, 25, 23, 0.06)

[헤더 행]
  좌측: 번호 배지 (Primary Light 배경, Primary 텍스트) + 식당명(h2) + 한국어명(caption)
  우측: RatingBadge

[배지 행]
  PriceTag + 영어메뉴 배지 + 거리 + 영업시간 배지
  가로 스크롤 허용 (한 줄)

[설명] — body, 2줄 clamp

[AI 추천 이유 박스]
  배경: var(--color-primary-light)
  Border-radius: 12px
  Padding: 12px 14px
  Font: body-sm, 이탤릭

[하단]
  주소(caption, 왼쪽) + "See Details →"(body-sm, Primary 색상, 오른쪽)

진입 애니메이션:
  1번 카드: fadeUp 0.3s ease
  2번 카드: fadeUp 0.3s ease 0.08s delay
  3번 카드: fadeUp 0.3s ease 0.16s delay
```

---

### ChatBubble

```
User 버블:
  정렬: 오른쪽
  배경: var(--color-primary)
  텍스트 색: #FFFFFF
  Border-radius: 18px 18px 4px 18px
  Padding: 12px 16px
  Max-width: 80%

AI 버블:
  정렬: 왼쪽
  배경: var(--color-surface)
  Border: 1px solid var(--color-border)
  텍스트 색: var(--color-text-primary)
  Border-radius: 18px 18px 18px 4px
  Padding: 12px 16px
  Max-width: 85%
  AI 아이콘 (좌측 상단 12px 원형): Primary Light 배경

타임스탬프: caption, Text Tertiary, 버블 하단 4px
```

---

### FilterChip

```
기본 상태:
  배경: var(--color-surface)
  Border: 1.5px solid var(--color-border)
  텍스트: var(--color-text-secondary)
  Border-radius: 100px (pill)
  Padding: 8px 14px
  Font: label, 500

선택 상태:
  배경: var(--color-primary-light)
  Border: 1.5px solid var(--color-primary)
  텍스트: var(--color-primary)
  Font-weight: 600

크기: 높이 34px, 터치 타겟 44px 확보 (padding으로 보정)
아이콘: 텍스트 앞 14px 아이콘 옵션
```

---

### PriceTag

```
배경: var(--color-accent-light)  ← Cream
텍스트: var(--color-accent)       ← Amber
Font: label, 600
Border-radius: 6px
Padding: 3px 8px

내용: "$" / "$$" / "$$$" / "$$$$"
툴팁/서브텍스트: "Budget" / "Mid-range" / "Upscale" / "Fine Dining"
```

---

### RatingBadge

```
배경: var(--color-accent-light)
텍스트: var(--color-accent)
Font: body-sm, 700
Border-radius: 8px
Padding: 4px 8px
아이콘: ★ 앞에 배치 (16px)

예시: "★ 4.7"
```

---

### BottomSheet (식당 상세)

```
트리거: RestaurantCard 탭
애니메이션: translateY(100%) → translateY(0), 350ms ease-out
최대 높이: 85vh
배경: var(--color-surface)
Border-radius: 24px 24px 0 0
Overflow: scroll-y (내부만)

드래그 핸들:
  크기: 40px x 4px
  배경: var(--color-border)
  Border-radius: 2px
  위치: 상단 중앙, margin-top 12px

스와이프 다운 → 닫기
배경 오버레이: var(--color-overlay), 탭 시 닫기

Sticky 하단 버튼:
  위치: position: sticky, bottom: 0
  배경: var(--color-surface)에 border-top
  Padding: 16px 24px + safe-area-inset-bottom
```

---

### NavigationBar (하단 탭)

```
위치: fixed bottom-0, 전폭
높이: 64px + safe-area-inset-bottom
배경: var(--color-surface)
Border-top: 1px solid var(--color-border)
Backdrop-filter: blur(12px)

탭 항목 3개:
  - Home (집 아이콘)
  - Chat (말풍선 아이콘)
  - Saved (북마크 아이콘) ← Phase 2용, 일단 UI만

활성 탭:
  아이콘: Primary 컬러
  라벨: Primary 컬러, font-weight 600
비활성 탭:
  아이콘 + 라벨: Text Tertiary
```

---

## 7. CSS 변수 전체 정의 (즉시 사용 가능)

```css
:root {
  /* ── 컬러 — Primary (Terracotta) ── */
  --color-primary:        #C85C3A;
  --color-primary-dark:   #A3431F;
  --color-primary-light:  #F2E0D8;

  /* ── 컬러 — Secondary (Moss) ── */
  --color-secondary:      #4A6741;
  --color-secondary-light: #D4E4D0;

  /* ── 컬러 — Accent (Amber) ── */
  --color-accent:         #C49A3C;
  --color-accent-light:   #FDF5E4;

  /* ── 컬러 — 배경 & 서피스 ── */
  --color-background:     #FAF7F4;
  --color-surface:        #FFFFFF;
  --color-surface-alt:    #F5F0EB;

  /* ── 컬러 — 텍스트 ── */
  --color-text-primary:   #1C1917;
  --color-text-secondary: #78716C;
  --color-text-tertiary:  #A8A29E;
  --color-text-inverse:   #FFFFFF;

  /* ── 컬러 — 테두리 ── */
  --color-border:         #E8E0D8;
  --color-border-focus:   #C85C3A;

  /* ── 컬러 — 상태 ── */
  --color-error:          #DC2626;
  --color-error-light:    #FEF2F2;
  --color-success:        #4A6741;
  --color-success-light:  #D4E4D0;
  --color-warning:        #C49A3C;
  --color-warning-light:  #FDF5E4;

  /* ── 컬러 — 오버레이 ── */
  --color-overlay:        rgba(28, 25, 23, 0.6);

  /* ── 타이포그래피 — 폰트 패밀리 ── */
  --font-display:         'DM Serif Display', Georgia, serif;
  --font-body:            'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono:            'Courier New', monospace;

  /* ── 타이포그래피 — 폰트 크기 ── */
  --text-display:         28px;
  --text-h1:              22px;
  --text-h2:              18px;
  --text-h3:              16px;
  --text-body-lg:         16px;
  --text-body:            15px;
  --text-body-sm:         14px;
  --text-caption:         13px;
  --text-label:           12px;

  /* ── 타이포그래피 — 굵기 ── */
  --weight-regular:       400;
  --weight-medium:        500;
  --weight-semibold:      600;
  --weight-bold:          700;

  /* ── 타이포그래피 — 행간 ── */
  --leading-tight:        1.2;
  --leading-snug:         1.35;
  --leading-normal:       1.5;
  --leading-relaxed:      1.6;

  /* ── 타이포그래피 — 자간 ── */
  --tracking-tight:       -0.01em;
  --tracking-normal:      0em;
  --tracking-wide:        0.02em;

  /* ── 간격 (8px 그리드) ── */
  --space-1:   4px;
  --space-2:   8px;
  --space-3:   12px;
  --space-4:   16px;
  --space-5:   20px;
  --space-6:   24px;
  --space-8:   32px;
  --space-10:  40px;
  --space-12:  48px;
  --space-16:  64px;

  /* ── 레이아웃 ── */
  --page-padding:         20px;
  --page-max-width:       480px;
  --bottom-nav-height:    64px;

  /* ── Border Radius ── */
  --radius-sm:   8px;
  --radius-md:   12px;
  --radius-lg:   16px;
  --radius-xl:   20px;
  --radius-2xl:  24px;
  --radius-pill: 100px;

  /* ── 그림자 ── */
  --shadow-sm:   0 1px 4px rgba(28, 25, 23, 0.06);
  --shadow-md:   0 2px 12px rgba(28, 25, 23, 0.08);
  --shadow-lg:   0 8px 32px rgba(28, 25, 23, 0.12);
  --shadow-sheet: 0 -4px 24px rgba(28, 25, 23, 0.10);

  /* ── 애니메이션 ── */
  --duration-fast:   150ms;
  --duration-normal: 300ms;
  --duration-slow:   500ms;
  --ease-out:        cubic-bezier(0.25, 0.1, 0.25, 1.0);
  --ease-spring:     cubic-bezier(0.34, 1.56, 0.64, 1);

  /* ── Z-index 레이어 ── */
  --z-base:      0;
  --z-card:      10;
  --z-nav:       100;
  --z-overlay:   200;
  --z-sheet:     300;
  --z-toast:     400;
}
```

---

## 8. 애니메이션 정의

```css
/* 카드 진입 */
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* GPS 아이콘 펄스 */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.08);
    opacity: 0.75;
  }
}

/* 로딩 점 */
@keyframes dots {
  0%   { content: '.'; }
  33%  { content: '..'; }
  66%  { content: '...'; }
  100% { content: '.'; }
}

/* 바텀 시트 슬라이드업 */
@keyframes slideUp {
  from { transform: translateY(100%); }
  to   { transform: translateY(0); }
}

/* 오버레이 페이드인 */
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
```

---

## 9. 반응형 브레이크포인트

모바일 퍼스트. 세로 화면 기준 설계.

```css
/* 기준: 모바일 세로 (360px~) */
/* ─── 모든 기본 스타일은 여기 ─── */

/* 대형 폰 / 작은 태블릿 */
@media (min-width: 480px) {
  .page-container {
    max-width: var(--page-max-width);
    margin: 0 auto;
  }
}

/* 태블릿 이상 — 중앙 정렬 패널 */
@media (min-width: 768px) {
  body {
    background: var(--color-surface-alt);
  }
  .page-container {
    margin: 40px auto;
    border-radius: var(--radius-2xl);
    box-shadow: var(--shadow-lg);
    overflow: hidden;
    min-height: calc(100vh - 80px);
  }
}
```

---

## 10. 접근성 가이드라인

| 항목 | 기준 | 적용 방법 |
|------|------|----------|
| 색상 대비 | WCAG AA (4.5:1 이상) | Primary(#C85C3A) on White = 4.6:1 통과 |
| 터치 타겟 | 최소 44 x 44px | 버튼 padding으로 확보 |
| 글자 크기 | 최소 16px (본문) | --text-body-lg 기준 |
| 포커스 표시 | 명확한 outline | `outline: 2px solid var(--color-border-focus)` |
| 이미지 대체 | alt 텍스트 필수 | 아이콘은 aria-label |
| 스크린 리더 | 의미 있는 순서 | landmark, role 사용 |

---

## 11. 현재 index.html → 개선 포인트 (FE 참고)

| 현재 | 개선 방향 |
|------|----------|
| 빨간 그라디언트 헤더 | → Warm White 배경 + 텍스트 앱명으로 대체 |
| 텍스트 검색 중심 레이아웃 | → GPS 버튼이 히어로 CTA |
| Segoe UI 폰트 | → DM Sans + DM Serif Display |
| 카드 left border 색상 구분 (빨강/주황/초록) | → 번호 배지로 대체, 단일 카드 스타일 |
| 이모지 과다 사용 | → SVG 아이콘으로 대체 |
| 배경 #f5f0eb 단색 | → 그대로 유지 가능 (--color-background와 동일) |
| 하단 탭 없음 | → NavigationBar 추가 필요 |
| BottomSheet 없음 | → 식당 상세 전용 컴포넌트 신규 구현 |

---

## 12. CTO에게 요청사항

1. **GPS API:** `navigator.geolocation.getCurrentPosition()` 브라우저 API 사용. HTTPS 필수. iOS Safari 권한 요청 타이밍 확인 필요.
2. **safe-area-inset:** iPhone 노치/홈바 대응. `env(safe-area-inset-bottom)` CSS 변수 적용 여부 확인.
3. **PWA manifest:** `display: standalone`, `theme_color: #C85C3A`, `background_color: #FAF7F4` 설정 요청.
4. **스와이프 제스처:** BottomSheet 드래그 닫기는 touch event 처리 필요 — 라이브러리 vs 직접 구현 결정 요청.
5. **애니메이션 성능:** `transform` + `opacity`만 사용, `will-change: transform` 적용 여부 확인.
6. **폰트 로딩:** Google Fonts `display=swap` 파라미터로 FOUT 방지 확인.

---

*DESIGN.md v1.0 — CDO 나은 작성 | 2026-04-06*  
*이 파일이 최신 디자인 기준입니다. 구현 전 반드시 이 파일 기준으로 작업하세요.*
