# Frontend Design Skill — 서연 표준

웹 페이지/UI를 만들 때 자동으로 적용되는 디자인 원칙.
리안이 따로 말하지 않아도 이 기준 이상으로 출력한다.

## 1. 레이아웃 & 공간

- 여백은 항상 8px 배수 (8/16/24/32/48/64/80/96px)
- 섹션 간격 최소 80px — 답답하게 붙이지 마라
- 최대 너비: 콘텐츠 1200px, 텍스트 720px
- 그리드: 12컬럼 기준, gap 1px + 배경색으로 구분선 처리
- 모바일 first — clamp() 반응형 필수

## 2. 타이포그래피

- 헤드라인: `clamp(36px, 6vw, 100px)` — 절대 고정 px 쓰지 마라
- letter-spacing: 헤드라인 -2px~-4px / 레이블 +3px~+6px
- line-height: 헤드라인 0.9~1.0 / 본문 1.6~1.7
- font-weight: 900(히어로) / 700(제목) / 400(본문) — 중간값(500/600) 남발 금지
- 그라디언트 텍스트: background-clip: text + animation 필수

## 3. 색상 & 대비

- 배경은 #000 또는 #fff 중 하나로 확실히 — 어중간한 회색 금지
- 다크 테마: 텍스트 계층 #fff / #888 / #444 / #222
- 강조색: 프로젝트 톤에 맞게 — 억지로 퍼플/블루/그린 넣지 마라
- WCAG AA 최소 준수 — 배경 대비 4.5:1 이상

## 4. 애니메이션 & 모션

- 필수 3종: fadeUp(등장) + IntersectionObserver(스크롤) + 카운트업(숫자)
- easing: cubic-bezier(0.16, 1, 0.3, 1) — ease-in-out 금지
- 지연: stagger 0.07~0.1s 간격으로 순차 등장
- 파티클/3D: Three.js — 정적 배경 절대 금지
- 호버: transform translateY(-2~-4px) + box-shadow 변화

## 5. 인터랙션

- 커스텀 커서: dot(6~8px) + lagging ring — mix-blend-mode: difference
- 카드 hover: 마우스 위치 추적 radial-gradient glow
- 버튼: before/after pseudo로 hover 효과 — border 변화만으론 부족
- 링크: cursor: none (커스텀 커서 있을 때)

## 6. 신뢰/퀄리티 체크

- 노이즈 텍스처 오버레이: SVG filter fractalNoise — 그레인감 필수
- 마퀴 배너: 서비스명/키워드 흘려보내기 — 빈 공간 채우기
- 스크롤 인디케이터: 히어로 하단 animated line
- 푸터: border-top + 좌우 split 레이아웃

## 7. SaaS 구조 기본값

- 마케팅/랜딩 페이지 → 위 모든 규칙 풀 적용
- 앱/대시보드 UI → Stitch 설계 + 클린/미니멀 (파티클 없음)
- 레퍼런스 수준: https://www.instagram.com/reel/DWswXHYDP-a/

## 출력 체크리스트

웹 페이지 뽑기 전 이것만 확인:
- [ ] Three.js 파티클 or 동급 배경 있나?
- [ ] 커스텀 커서 있나?
- [ ] clamp() 타이포 썼나?
- [ ] IntersectionObserver 스크롤 애니메이션 있나?
- [ ] 노이즈 텍스처 있나?
- [ ] 모바일 반응형 있나?
