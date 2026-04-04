#!/usr/bin/env python3
"""extract_and_save 함수 테스트"""
import sys
import os
from pathlib import Path

# 경로 설정
sys.path.insert(0, str(Path(__file__).parent / "lian_company"))

# .env 로드
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / "lian_company" / ".env")

from core.insight_extractor import extract_and_save

print("extract_and_save 함수 실행 중...\n")
extract_and_save()
print("\n완료!")
