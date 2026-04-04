#!/usr/bin/env python3
"""insight_extractor 파싱 로직 테스트"""
import sys
from pathlib import Path

# 경로 설정
sys.path.insert(0, str(Path(__file__).parent / "lian_company"))

from core.insight_extractor import _extract_analysis_sections

report_path = Path(__file__).parent / "보고사항들.md"
with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

sections = _extract_analysis_sections(content)
print(f"추출된 섹션: {len(sections)}개\n")

for i, (url, analysis) in enumerate(sections, 1):
    print(f"[섹션 {i}]")
    print(f"URL: {url}")
    print(f"분석 길이: {len(analysis)}자")
    print(f"분석 내용:\n{analysis}\n")
    print("-" * 60)
