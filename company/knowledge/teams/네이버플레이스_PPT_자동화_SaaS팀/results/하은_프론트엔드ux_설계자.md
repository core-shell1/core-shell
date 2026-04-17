# 네이버플레이스 PPT 자동화 SaaS - 웹 UI/UX 설계 완전 가이드 v1.0

## 📊 핵심 지표 기반 설계 목표 (30초 요약)

| 메트릭 | 목표치 | 측정 방법 | 실패 기준 |
|--------|--------|-----------|----------|
| **Time to First PPT** | 3분 이내 | URL 입력 → 다운로드 완료 시간 | 5분 초과 시 UX 재설계 |
| **온보딩 완료율** | 70%+ | 가입 → 첫 PPT 생성 완료 비율 | 50% 미만 시 마찰 지점 분석 |
| **결제 전환율** | 15%+ | 무료 크레딧 소진 → 결제 전환 | 10% 미만 시 가격/가치 재검토 |
| **모바일 사용률** | 40%+ | 모바일 접속 비율 (마케터 특성) | 반응형 필수, 데스크톱 우선 |
| **이탈률 (Bounce)** | 30% 이하 | 랜딩 → 가입 전 이탈 | 40% 초과 시 헤드라인 수정 |

**설계 철학**: 마케터는 "읽지 않는다". 클릭 3회 안에 결과물 미리보기 없으면 이탈.

---

## 🎨 전체 페이지 플로우 (Wireframe Tree)

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. 랜딩 페이지 (/)                                               │
│ ├─ Hero: "네이버플레이스 URL 입력 → 3분 안에 PPT 완성"           │
│ ├─ 샘플 PPT 미리보기 (Before/After 슬라이더)                     │
│ ├─ CTA: "무료로 시작하기" (5 크레딧 제공)                        │
│ └─ 가격표 (스크롤 시 Sticky Header로 변환)                       │
└─────────────────────────────────────────────────────────────────┘
                    ↓ (클릭)
┌─────────────────────────────────────────────────────────────────┐
│ 2. 가입/로그인 (/auth)                                           │
│ ├─ SSO (Google/Naver) + 이메일 가입                             │
│ ├─ 필수 입력: 이메일, 비밀번호, 회사명 (선택)                    │
│ └─ 즉시 리다이렉트 → 대시보드 (설정 단계 스킵)                   │
└─────────────────────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────────────────────┐
│ 3. 대시보드 (/dashboard)                                         │
│ ├─ 상단: 크레딧 잔량 (5/5) + "충전하기" 버튼                     │
│ ├─ 메인: URL 입력창 (포커스 자동) + "PPT 생성" 버튼              │
│ ├─ 하단: 최근 생성 이력 (테이블: 날짜/상호명/상태/다운로드)      │
│ └─ Sidebar: 대시보드 / 생성 이력 / 크레딧 관리 / 설정           │
└─────────────────────────────────────────────────────────────────┘
                    ↓ (URL 입력 후 생성 클릭)
┌─────────────────────────────────────────────────────────────────┐
│ 4. 생성 진행 상태 (/dashboard/tasks/{task_id})                  │
│ ├─ 프로그레스바: 크롤링(30%) → 분석(60%) → 생성(90%) → 완료     │
│ ├─ 실시간 로그: "데이터 수집 중... 14/20 항목 완료"             │
│ ├─ 예상 완료 시간: "약 2분 30초 남음"                           │
│ └─ 완료 시 자동 리다이렉트 → 결과 페이지                        │
└─────────────────────────────────────────────────────────────────┘
                    ↓ (완료)
┌─────────────────────────────────────────────────────────────────┐
│ 5. 결과 페이지 (/dashboard/results/{task_id})                   │
│ ├─ PPT 미리보기 (썸네일 3장 + "전체 보기" 버튼)                 │
│ ├─ 다운로드 버튼 (1차: .pptx / 2차: .pdf 변환 옵션)             │
│ ├─ 공유 링크 생성 (48시간 유효)                                 │
│ └─ CTA: "다시 생성" / "크레딧 충전"                              │
└─────────────────────────────────────────────────────────────────┘
                    ↓ (크레딧 소진 시)
┌─────────────────────────────────────────────────────────────────┐
│ 6. 결제 페이지 (/pricing)                                        │
│ ├─ 플랜 선택: Basic(10건) / Pro(50건) / Enterprise(무제한)      │
│ ├─ 결제 수단: 카드 / 토스페이 / 계좌이체                        │
│ └─ 결제 후 즉시 크레딧 충전 → 대시보드 리다이렉트               │
└─────────────────────────────────────────────────────────────────┘
```

**마찰 지점 분석 (각 단계별 이탈 방지 전략)**:
- **1→2**: 랜딩에서 가입 전 이탈 → 샘플 PPT 다운로드 버튼 추가 (이메일 수집)
- **2→3**: 가입 후 빈 대시보드 → 샘플 URL 자동 입력 (예: 유명 카페)
- **3→4**: URL 입력 후 이탈 → 실시간 로그로 "작동 중임" 인지
- **4→5**: 생성 중 이탈 → 이메일/푸시 알림 "PPT 완성됨" 전송
- **5→6**: 결과 확인 후 결제 안 함 → 워터마크 추가 (결제 시 제거)

---

## 🖥️ 화면별 UI 컴포넌트 명세 (shadcn/ui 기반)

### **1. 랜딩 페이지 (Hero Section)**
```tsx
// components/landing/hero.tsx
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowRight, Zap } from "lucide-react";

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-blue-50 to-white dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-24 lg:py-32">
        {/* Badge */}
        <div className="mb-8 flex justify-center">
          <div className="inline-flex items-center gap-2 rounded-full bg-blue-100 px-4 py-2 text-sm dark:bg-blue-900">
            <Zap className="h-4 w-4 text-blue-600 dark:text-blue-400" />
            <span className="font-medium">지금 가입 시 무료 크레딧 5개 제공</span>
          </div>
        </div>

        {/* Headline */}
        <h1 className="mb-6 text-center text-4xl font-bold tracking-tight lg:text-6xl">
          네이버플레이스 URL 입력하면
          <br />
          <span className="text-blue-600 dark:text-blue-400">3분 안에 PPT 완성</span>
        </h1>

        {/* Sub-headline */}
        <p className="mb-12 text-center text-xl text-gray-600 dark:text-gray-400">
          수동으로 15분 걸리던 작업을 자동화. 마케터·대행사 업무 시간 80% 절감
        </p>

        {/* CTA Form */}
        <div className="mx-auto max-w-2xl">
          <div className="flex flex-col gap-4 sm:flex-row">
            <Input
              type="url"
              placeholder="https://m.place.naver.com/restaurant/..."
              className="h-14 flex-1 text-lg"
            />
            <Button size="lg" className="h-14 px-8 text-lg sm:w-auto">
              무료로 시작하기
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
          <p className="mt-4 text-center text-sm text-gray-500">
            신용카드 등록 불필요 · 5분 안에 첫 PPT 생성 가능
          </p>
        </div>

        {/* Social Proof */}
        <div className="mt-16 flex justify-center gap-8 text-center">
          <div>
            <p className="text-3xl font-bold text-blue-600">1,234+</p>
            <p className="text-sm text-gray-600">생성된 PPT</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-blue-600">4.9/5</p>
            <p className="text-sm text-gray-600">평균 만족도</p>
          </div>
          <div>
            <p className="text-3xl font-bold text-blue-600">2.8분</p>
            <p className="text-sm text-gray-600">평균 생성 시간</p>
          </div>
        </div>
      </div>

      {/* Background Decoration */}
      <div className="absolute inset-0 -z-10 h-full w-full bg