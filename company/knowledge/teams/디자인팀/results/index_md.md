# Design System Index — 이펙트 & 컴포넌트 카탈로그

> **이 파일은 사이트 만들 때 반드시 먼저 읽어라.**
> 각 이펙트의 실제 소스 코드 경로가 있다. 코드를 읽고 vanilla JS/WebGL로 포팅해서 써라.
> 절대 내 기본 패턴(파티클, 와이어프레임, 기본 페이드인)으로 짜지 마라.

---

## 배경 셰이더 (Background Shaders)

| 이펙트 | 느낌 | 소스 경로 | 포팅 난이도 |
|--------|------|-----------|-------------|
| **LiquidChrome** | 크롬 액체, 마우스 반응 물결 | `components/react-bits/src/content/Backgrounds/LiquidChrome/LiquidChrome.jsx` | 쉬움 (OGL→WebGL) |
| **Silk** | 부드러운 실크 직물 패턴 | `components/react-bits/src/content/Backgrounds/Silk/Silk.jsx` | 쉬움 (R3F→Three.js) |
| **Aurora** | 오로라 빛 | `components/react-bits/src/content/Backgrounds/Aurora/` | 중간 |
| **Hyperspeed** | 하이퍼스페이스 워프 | `components/react-bits/src/content/Backgrounds/Hyperspeed/` | 중간 |
| **Galaxy** | 은하계 파티클 | `components/react-bits/src/content/Backgrounds/Galaxy/` | 중간 |
| **Iridescence** | 무지개빛 반사 | `components/react-bits/src/content/Backgrounds/Iridescence/` | 중간 |
| **LiquidEther** | 에테르 유체 | `components/react-bits/src/content/Backgrounds/LiquidEther/` | 중간 |
| **Waves** | 파도 웨이브 | `components/react-bits/src/content/Backgrounds/Waves/` | 쉬움 |
| **Threads** | 실 가닥 | `components/react-bits/src/content/Backgrounds/Threads/` | 쉬움 |
| **GridDistortion** | 그리드 왜곡 | `components/react-bits/src/content/Backgrounds/GridDistortion/` | 중간 |
| **Plasma** | 플라즈마 | `components/react-bits/src/content/Backgrounds/Plasma/` | 쉬움 |
| **Orb** | 빛나는 구체 | `components/react-bits/src/content/Backgrounds/Orb/` | 쉬움 |
| **Liquid Background** | Three.js 액체 메탈릭 | `snippets/liquid-background.html` | 즉시 사용 |
| **ShaderGradient** | 움직이는 3D 그라데이션 | `motion/shadergradient/` | npm 설치 |

### 선택 가이드
- **SaaS / B2B**: LiquidChrome, Silk, Waves (절제된 고급감)
- **크리에이티브 / 브랜드**: Aurora, Iridescence, Hyperspeed (임팩트)
- **미니멀**: Threads, GridDistortion, Orb (깔끔)
- **다크 퓨처리스틱**: LiquidChrome + grain overlay (검증됨 — showcase.html)

---

## 텍스트 애니메이션 (Text Animations)

| 이펙트 | 느낌 | 소스 경로 |
|--------|------|-----------|
| **SplitText** | 글자 하나씩 등장 | `components/react-bits/src/content/TextAnimations/SplitText/` |
| **BlurText** | 블러에서 선명하게 | `components/react-bits/src/content/TextAnimations/BlurText/` |
| **GlitchText** | 글리치/노이즈 | `components/react-bits/src/content/TextAnimations/GlitchText/` |
| **DecryptedText** | 암호 해독 느낌 | `components/react-bits/src/content/TextAnimations/DecryptedText/` |
| **ShinyText** | 빛 반사 스윕 | `components/react-bits/src/content/TextAnimations/ShinyText/` |
| **ScrollFloat** | 스크롤 따라 떠오름 | `components/react-bits/src/content/TextAnimations/ScrollFloat/` |
| **ScrollVelocity** | 스크롤 속도 반응 | `components/react-bits/src/content/TextAnimations/ScrollVelocity/` |
| **TextPressure** | 마우스 거리 반응 굵기 | `components/react-bits/src/content/TextAnimations/TextPressure/` |
| **ScrambledText** | 글자 셔플 | `components/react-bits/src/content/TextAnimations/ScrambledText/` |
| **FuzzyText** | 퍼지/흐릿 | `components/react-bits/src/content/TextAnimations/FuzzyText/` |

### 선택 가이드
- **히어로 타이틀**: SplitText + GSAP (split text reveal — 검증됨)
- **SaaS 기능 섹션**: BlurText, ScrollFloat
- **테크/해커 느낌**: DecryptedText, GlitchText, ScrambledText
- **고급/럭셔리**: ShinyText, TextPressure

---

## 커서 (Cursors)

| 이펙트 | 느낌 | 소스 경로 |
|--------|------|-----------|
| **BlobCursor** | 부드러운 블롭 따라다님 | `components/react-bits/src/content/Animations/BlobCursor/` |
| **SplashCursor** | 클릭 시 스플래시 | `components/react-bits/src/content/Animations/SplashCursor/` |
| **GhostCursor** | 잔상 트레일 | `components/react-bits/src/content/Animations/GhostCursor/` |
| **Crosshair** | 십자선 | `components/react-bits/src/content/Animations/Crosshair/` |
| **PixelTrail** | 픽셀 트레일 | `components/react-bits/src/content/Animations/PixelTrail/` |
| **dot + lagging ring** | 기본 커스텀 (CSS) | 직접 구현 (showcase.html 참고) |

### 선택 가이드
- **기본값**: dot + lagging ring (가볍고 범용)
- **크리에이티브**: BlobCursor, SplashCursor
- **미니멀**: Crosshair

---

## 스크롤 패턴 (Scroll Patterns)

| 패턴 | 구현 | 비고 |
|------|------|------|
| **Lenis smooth scroll** | `<script src="unpkg.com/lenis@1.1.18">` | 기본 적용 필수 |
| **Horizontal scroll section** | GSAP ScrollTrigger pin + scrub | showcase.html 참고 |
| **Word-by-word reveal** | IntersectionObserver + class toggle | showcase.html manifesto 참고 |
| **Parallax depth** | GSAP ScrollTrigger + y offset | 레이어별 속도 차이 |
| **Scroll velocity text** | ScrollVelocity 컴포넌트 | react-bits 참고 |

---

## 카드/UI 컴포넌트 (Cards & UI)

| 소스 | 개수 | 경로 | 특징 |
|------|------|------|------|
| **uiverse Buttons** | 다수 | `components/uiverse/Buttons/` | HTML/CSS 즉시 사용 |
| **uiverse Cards** | 726 | `components/uiverse/Cards/` | HTML/CSS 즉시 사용 |
| **uiverse Inputs** | 다수 | `components/uiverse/Inputs/` | HTML/CSS 즉시 사용 |
| **uiverse Loaders** | 다수 | `components/uiverse/loaders/` | HTML/CSS 즉시 사용 |

---

## 디자인 시스템 레퍼런스 (DESIGN.md)

| 카테고리 | 기업 | 경로 |
|----------|------|------|
| SaaS | stripe, linear.app, notion, figma, airtable, cursor | `design-systems/design-md/{name}/` |
| AI/Tech | openai, cohere, replicate, elevenlabs, claude | `design-systems/design-md/{name}/` |
| Brand | apple, bmw, ferrari, spotify, airbnb | `design-systems/design-md/{name}/` |
| Dev Tools | vercel, supabase, expo, hashicorp | `design-systems/design-md/{name}/` |

---

## 3D 예제

| 이름 | 스택 | 경로 |
|------|------|------|
| threejs-landing | Three.js + GSAP | `3d/threejs-landing/` |
| threejs-portfolio | Three.js models + camera | `3d/threejs-portfolio/` |
| r3f-portfolio | React Three Fiber + Framer | `3d/r3f-portfolio/` |
| r3f-example | R3F 기본 패턴 | `3d/r3f-example/` |
| r3f-examples | R3F 다양한 패턴 | `3d/r3f-examples/` |

---

## 검증된 조합 (Proven Recipes)

### 다크 퓨처리스틱 SaaS (showcase.html)
- 배경: LiquidChrome shader + grain overlay
- 스크롤: Lenis smooth
- 텍스트: Split text reveal (line by line)
- 레이아웃: 좌하단 히어로 + horizontal scroll cards + word reveal manifesto
- 커서: dot + lagging ring
- 색감: 웜 블랙 + 골드 accent

### 클린 미니멀 SaaS (추천)
- 배경: Silk shader (부드러운 톤)
- 스크롤: Lenis + parallax
- 텍스트: BlurText reveal
- 커서: Crosshair
- 색감: 화이트 + 단일 accent

### 브랜드/크리에이티브 (추천)
- 배경: Aurora 또는 Iridescence
- 스크롤: Horizontal full-page
- 텍스트: GlitchText 또는 TextPressure
- 커서: BlobCursor
- 색감: 비비드 그라데이션
