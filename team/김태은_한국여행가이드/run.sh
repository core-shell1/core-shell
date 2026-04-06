#!/bin/bash
# Korea Local Guide — 실행 스크립트

cd "$(dirname "$0")"

# .env 로드 (lian_company/.env 공유 사용)
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
elif [ -f "../../lian_company/.env" ]; then
  export $(grep -v '^#' ../../lian_company/.env | xargs)
fi

# Python 경로 결정 (venv 우선)
VENV="../../lian_company/venv"
if [ -d "$VENV/Scripts" ]; then
  PYTHON="$VENV/Scripts/python.exe"
elif [ -d "$VENV/bin" ]; then
  PYTHON="$VENV/bin/python"
else
  PYTHON="python"
fi

# 패키지 설치
$PYTHON -m pip install -q -r requirements.txt

echo "Korea Local Guide 시작"
echo "→ http://localhost:8000"
$PYTHON -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
