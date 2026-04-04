# 팀 자율 루프 — 빠른 시작 가이드

> 리안이 해야 할 최소 3개 명령어

## 1️⃣ 영업 결과 입력 (매일 또는 수시)

```bash
cd lian_company
python input_results.py "미용실 계약 성사"
```

**다양한 입력 예시:**
```bash
python input_results.py "포에트리헤어 계약"
python input_results.py "거절, 비싼이유"
python input_results.py "DM 5건 발송, 2건 답장"
python input_results.py "7일 만에 클로징"
```

**결과:**
- 입력 데이터가 자동으로 파싱되어 저장됨
- 5건 도달하면 팀이 자동으로 약점 분석
- 새로운 버전이 자동으로 생성됨 (v1 → v2 → v3...)

---

## 2️⃣ 전사 현황 확인 (2주에 한 번)

```bash
python orchestrate.py
```

**출력 예시:**
```
🏢 전사 팀 오케스트레이션

[1] 모든 팀의 status.json 로드 중...
    로드된 팀: 5개

## 팀별 KPI 현황

| 팀 | 데이터 | 버전 | 주요 KPI | 상태 |
|---|---|---|---|---|
| offline_marketing | 5 | v2 | 계약: 2건 | ✅ 진행 중 |
| 온라인영업팀 | 0 | v1 | N/A | ⏳ 데이터 대기 |
| ...

## 주의 필요 팀
- 온라인영업팀: 데이터 대기 중
```

**해석:**
- `데이터 대기 중` = 아직 결과를 입력하지 않음
- `진행 중` = 정상적으로 데이터 쌓이는 중
- `개선 준비` = 5건 모였는데 아직 개선 안 함

---

## 3️⃣ 팀에게 개선 지시 (필요할 때)

특정 팀을 즉시 개선하고 싶으면:

```python
# Python 콘솔에서
from teams.offline_marketing.pipeline import improve
improve()
```

**또는 자동으로:**
- 5건 도달 → 자동 개선
- 10건 도달 → 자동 개선
- 15건 도달 → 자동 개선
- (5의 배수마다)

---

## 🎯 리안이 알아야 할 핵심

### 상태 아이콘

| 아이콘 | 의미 | 조치 |
|---|---|---|
| ⏳ 데이터 대기 | 아직 입력 데이터 없음 | `input_results.py`로 입력 시작 |
| ✅ 진행 중 | 데이터 수집 중 | 계속 입력 |
| 🚀 개선 준비 | 5건 모였는데 아직 v1 | `improve()` 수동 실행 또는 자동 대기 |

### 버전의 의미

- `v1` = 원본 자료
- `v2` = 첫 데이터 기반 개선
- `v3` = 두 번째 개선
- ...

**버전이 올라간다** = **팀이 자동으로 자신을 개선하고 있다는 뜻**

### KPI의 의미

각 팀마다 다름:

**오프라인 마케팅팀:**
- 계약 건수 (목표: 월 5건)
- 답장률 (목표: 30% 이상)
- 클로징 사이클 (목표: 7일 이내)

**온라인 팀들:**
- 리드 생성
- 응답률
- 전환율
- 등

---

## 🔧 문제 해결

### Q: input_results.py가 안 돼요

```bash
# 1. 경로 확인 (lian_company 폴더에 있는지)
cd lian_company
ls input_results.py

# 2. Python 버전 확인
python --version

# 3. venv 활성화
venv\Scripts\activate

# 4. 다시 실행
python input_results.py "테스트"
```

### Q: 데이터 입력했는데 자동 개선이 안 돼요

5건 정확히 도달했는지 확인:

```bash
cat teams/offline_marketing/status.json | grep data_count
```

- `data_count: 5` → 자동 개선 실행됨 (이미 v2여야 함)
- `data_count: 3` → 아직 5건 미만 (더 입력 필요)

### Q: status.json 파일을 실수로 지웠어요

폴더에 다시 만들면 됨. 새로 입력하면 자동으로 다시 생성됨:

```bash
python input_results.py "테스트"
```

---

## 📋 명령어 치트시트

```bash
# 일일 업무
python input_results.py "영업결과"          # 결과 입력

# 주간 업무 (선택)
python orchestrate.py                       # 전사 현황 확인

# 수동 개선 (선택)
python -c "from teams.offline_marketing.pipeline import improve; improve()"

# 상태 확인
cat teams/offline_marketing/status.json

# 개선 이력 확인
ls teams/offline_marketing/results/
```

---

## 🚀 다음 단계

더 자세한 정보는 `AUTONOMOUS_LOOP.md` 참고:
- 각 팀의 KPI 정의
- 개선 알고리즘 상세
- 확장 기능 (자동 스케줄, 대시보드 등)

**모두 준비됐어요. 첫 번째 결과를 입력해보세요!** 🎯

---

**마지막 업데이트**: 2026-04-04
