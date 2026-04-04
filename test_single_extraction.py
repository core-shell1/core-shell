#!/usr/bin/env python3
"""한 개 분석에서 인사이트 추출 테스트"""
import sys
import os
from pathlib import Path

# 경로 설정
sys.path.insert(0, str(Path(__file__).parent / "lian_company"))

# .env 로드
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / "lian_company" / ".env")

from core.insight_extractor import _extract_analysis_sections, categorize_insight, INSIGHT_CATEGORIES
import google.genai as genai
from core.models import GEMINI_FLASH

report_path = Path(__file__).parent / "보고사항들.md"
with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 파싱
sections = _extract_analysis_sections(content)
if not sections:
    print("분석 섹션 없음")
    sys.exit(1)

# 첫 번째 섹션만 테스트
url, analysis = sections[0]
print(f"테스트 분석:")
print(f"  URL: {url}")
print(f"  분석 텍스트 (처음 300자): {analysis[:300]}\n")

# Gemini 클라이언트 초기화
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 각 카테고리별 인사이트 추출
print("인사이트 추출 시작...\n")
for category in INSIGHT_CATEGORIES:
    print(f"[{category}]", end=" ", flush=True)
    try:
        insight = categorize_insight(analysis, category, client)
        if insight:
            print(f"OK - {len(insight)}자")
            print(f"  {insight[:100]}...\n")
        else:
            print("(없음)")
    except Exception as e:
        print(f"ERROR: {e}")

print("테스트 완료!")
