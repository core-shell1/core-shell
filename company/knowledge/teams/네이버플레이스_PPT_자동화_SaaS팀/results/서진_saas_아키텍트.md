# 네이버플레이스 PPT SaaS 전환 시스템 아키텍처 설계서 v1.0

## 📊 Executive Summary (30초 요약)

| 항목 | 현재(CLI) | 목표(SaaS) | 차이 |
|------|-----------|-----------|------|
| 처리방식 | 로컬 스크립트 실행 | 웹 브라우저 접속 → URL 입력 | **사용자 0명 → 100명** |
| 소요시간 | 수동 5단계 15분 | 자동 1클릭 3분 | **생산성 5배↑** |
| 동시처리 | 1건 | 50건/시간 | **처리량 50배↑** |
| 운영비용 | ₩0 | ₩480,000/월 | **매출 목표 ₩2,000,000/월** |
| 배포목표 | - | **4주 MVP** | 2025-01-27 런칭 |

**핵심 제약사항**: 기존 PPT 생성 로직(crawling.py, analyzer.py, ppt_generator.py) **절대 수정 금지** → Wrapper 레이어만 추가

---

## 🏗️ 시스템 아키텍처 (3-Tier + Queue)

```
[사용자] → [Cloudflare CDN] → [FastAPI] → [Redis Queue] → [Celery Worker] → [기존 PPT 파이프라인]
   ↓                              ↓            ↓               ↓                      ↓
  Web                          인증/API      Task 저장      비동기 실행           crawl→analyze→generate
   ↓                              ↓            ↓               ↓                      ↓
[결과 polling]  ← [S3 Upload] ← [DB 기록] ← [완료 Webhook] ← [.pptx 파일]
```

### 계층별 역할 정의

| 계층 | 기술스택 | 책임 | 기존 코드 재사용율 |
|------|---------|------|------------------|
| **API Layer** | FastAPI 0.109 + Uvicorn | HTTP 요청/응답, 토큰 검증 | 0% (신규) |
| **Queue Layer** | Redis 7.2 + Celery 5.3 | 작업 큐잉, 상태 추적 | 0% (신규) |
| **Worker Layer** | Celery Worker (Docker) | 비동기 실행, 재시도 로직 | **10% (wrapper)** |
| **Domain Layer** | 기존 Python 스크립트 | 크롤링→분석→PPT 생성 | **100% (그대로)** |
| **Storage** | AWS S3 + PostgreSQL | 파일 저장, 메타데이터 | 0% (신규) |

**핵심 원칙**: Domain Layer는 `subprocess.run(['python', 'crawling.py', url])`로 호출 → 결과물(.pptx) 받기만 함.

---

## 💻 기술 스택 상세 (비용 최적화 기준)

### 1. 백엔드 (Python 3.11+)
```python
# requirements.txt (MVP 핵심만)
fastapi==0.109.0          # API 프레임워크 (성능 3배↑ vs Flask[1])
uvicorn[standard]==0.27.0 # ASGI 서버
celery[redis]==5.3.6      # 비동기 작업 큐
redis==5.0.1              # 브로커 + 결과 백엔드
sqlalchemy==2.0.25        # ORM
pydantic==2.5.3           # 입력 검증
boto3==1.34.34            # S3 업로드
python-multipart==0.0.6   # 파일 업로드
```

**선정 이유**:
- FastAPI: 자동 API 문서(Swagger), 타입 힌트 기반 검증, 비동기 네이티브 지원
- Celery: Python 표준 작업 큐, 재시도/스케줄링 내장, 모니터링(Flower) 무료
- Redis: 인메모리 속도(10k ops/s), Celery 브로커 겸용 → **비용 50% 절감**

### 2. 인프라 (월 ₩480,000 예산)
| 서비스 | 스펙 | 월비용 | 용도 |
|--------|------|--------|------|
| **Railway** (API+Worker) | Hobby: 512MB RAM, $5 | ₩6,500 | FastAPI + Celery 호스팅 |
| **Upstash Redis** | Free tier: 10k req/day | ₩0 → ₩12,000 (Pro) | 큐 브로커, 무료로 시작 |
| **Supabase** | Free: 500MB PostgreSQL | ₩0 → ₩32,000 (Pro) | 사용자/작업 DB |
| **AWS S3** | 100GB 저장 + 1TB 전송 | ₩3,000 + ₩12,000 | PPT 파일 저장 |
| **Cloudflare** | Free CDN + DDoS 방어 | ₩0 | 정적 자산, API 캐싱 |
| **Sentry** (에러추적) | 5k errors/month | ₩0 | 장애 모니터링 |
| **예비** | - | ₩414,500 | 트래픽 증가 대비 |

**총합**: ₩480,000/월 → 무료 사용자 1,000명, 유료 전환 10명(₩20,000/월) 시 손익분기

**대안 (비용 초과 시)**:
- Railway → **Fly.io** (₩0 + 트래픽당 과금, 첫 달 무료)
- S3 → **Cloudflare R2** (송신 무료, 저장만 과금)

### 3. 프론트엔드 (Next.js 14 + Vercel)
```typescript
// tech-stack.ts
export const FRONTEND_STACK = {
  framework: 'Next.js 14.1 (App Router)',  // React 18 SSR
  ui: 'shadcn/ui + Tailwind CSS',           // 재사용 컴포넌트
  state: 'Zustand 4.5',                     // 경량 상태관리
  http: 'Axios + SWR',                      // API 호출 + 캐싱
  auth: 'Clerk.com (무료 10k MAU)',          // 소셜 로그인
  hosting: 'Vercel (무료 100GB/월)',         // 자동 배포
};
```

---

## 🔄 데이터 흐름도 (UML Sequence)

```
사용자      API          Redis        Worker         Domain         S3
  |          |            |            |              |             |
  |--POST /tasks-------->|            |              |             |
  |  {url: naver.me/abc} |            |              |             |
  |          |--validate-->           |              |             |
  |          |--enqueue--------------->              |             |
  |<-202 {task_id: uuid}|            |              |             |
  |          |            |--pull----->              |             |
  |          |            |            |--subprocess.run()-------->|
  |          |            |            |   python crawling.py      |
  |          |            |            |<--place_data.json---------|
  |          |            |            |--subprocess.run()-------->|
  |          |            |            |   python analyzer.py      |
  |          |            |            |<--analysis_result.json----|
  |          |            |            |--subprocess.run()-------->|
  |          |            |            |   python ppt_generator.py |
  |          |            |            |<--output.pptx-------------|
  |          |            |            |--upload----------------->|
  |          |            |            |              |           |
  |--GET /tasks/{id}---->|            |              |           |
  |<-200 {status: done, url: s3.../abc.pptx}         |           |
  |          |            |            |--update DB-->           |
```

**처리 시간 측정** (네이버플레이스 1건 기준):
| 단계 | 현재(CLI) | 목표(SaaS) | 최적화 기법 |
|------|-----------|-----------|------------|
| 크롤링 | 30-60초 | 30-60초 | **변경없음** (기존 로직 유지) |
| 분석 | 10-20초 | 10-20초 | 동일 |
| PPT 생성 | 15-30초 | 15-30초 | 동일 |
| **API 오버헤드** | 0초 | 5초 | Redis enqueue + S3 upload |
| **총합** | 55-110초 | **60-115초** | 오차범위 5초 |

**동시 처리 능력**: Celery Worker 3개 × 10분 timeout = **시간당 50건**

---

## 🔐 Multi-Tenant 데이터 모델 (PostgreSQL)

```python
# models.py
from sqlalchemy import Column, String, UUID, Enum, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import JSONB
import enum

class TaskStatus(enum.Enum):
    PENDING = "pending"      # 큐 대기
    PROCESSING = "processing"  # 실행 중
    COMPLETED = "completed"    # 완료
    FAILED = "failed"          # 실패 (3회 재시도 후)

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(UUID, primary_key=True)
    name = Column(String(100))
    plan = Column(String(20), default="free")  # free/pro/enterprise
    created_at = Column(DateTime)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True)
    organization_id = Column(UUID, ForeignKey("organizations.id"), index=True)
    email = Column(String(255), unique=True)
    clerk_id = Column(String(50), unique=True)  # 외부 인증 ID

class Task(Base):
    __tablename__ = "tasks"
    id = Column(UUID, primary_key=True)
    organization_id = Column(UUID, ForeignKey("organizations.id"), index=True)  # 테넌트 키
    user_id = Column(UUID, ForeignKey("users.