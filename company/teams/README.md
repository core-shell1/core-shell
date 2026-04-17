# company/teams/ — 팀 실행 엔진 (Python 모듈)

이 폴더는 **팀의 AI 실행 코드**다. 결과물이 아니다.

## 들어가는 것
- 에이전트 실행 로직 (Python 모듈)
- 팀 파이프라인 스크립트 (team pipeline)
- `run_*.py`가 import 하는 모듈들

## 들어가지 않는 것
- 팀이 만든 프로젝트 결과물 → `core/team/` 에
- 일반 유틸 함수 → `company/utils/` 또는 `company/tools/` 에

## 네이밍 규칙
- Python import 가능하도록 **언더스코어** 사용 (`광고수익형_트래픽_사이트팀`)
- 하이픈(`-`) 금지 (Python identifier 불가)

## 예시
- `광고수익형_트래픽_사이트팀/` — 실행 로직
- `온라인마케팅팀/` — `run_온라인마케팅팀.py`가 여기 소속 모듈 사용
- `analysis/` — 공통 분석 모듈
