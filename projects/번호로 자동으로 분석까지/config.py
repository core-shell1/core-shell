"""
config.py — 경로, API 키, 색상 상수 관리
"""
import sys
import os
from dotenv import load_dotenv
from pptx.dml.color import RGBColor

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# .env 로드
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ── 경로 ────────────────────────────────────────────────
EXCEL_PATH = os.path.join(BASE_DIR, "샘플", "샘플.xlsx")
TEMPLATE_PATH = os.path.join(BASE_DIR, "샘플", "Black and Grey Minimalist Company Project Proposal.pptx")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── 네이버 API 키 ──────────────────────────────────────
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "")
NAVER_AD_CUSTOMER_ID = os.getenv("NAVER_AD_CUSTOMER_ID", "")
NAVER_AD_ACCESS_LICENSE = os.getenv("NAVER_AD_ACCESS_LICENSE", "")
NAVER_AD_SECRET_KEY = os.getenv("NAVER_AD_SECRET_KEY", "")

# ── User-Agent 풀 ──────────────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36",
]

# ── 경쟁사 크롤링 세마포어 수 ──────────────────────────
COMPETITOR_SEMAPHORE = 3

# ── 색상 상수 (RGBColor) ───────────────────────────────
COLOR = {
    "GOOD":    RGBColor(0x2E, 0xCC, 0x71),  # 초록 — 완료, 경쟁사 막대
    "BAD":     RGBColor(0xE7, 0x4C, 0x3C),  # 빨강 — 미완료, 경고
    "NEUTRAL": RGBColor(0x95, 0xA5, 0xA6),  # 회색 — 내 업체 막대
    "PRIMARY": RGBColor(0x03, 0xC7, 0x5A),  # 네이버 블루-그린
    "DARK":    RGBColor(0x2C, 0x3E, 0x50),  # 어두운 텍스트
    "WARNING": RGBColor(0xE6, 0x7E, 0x22),  # 주황 — D등급
    "BLUE":    RGBColor(0x34, 0x98, 0xDB),  # 파랑 — A등급
    "PURPLE":  RGBColor(0x9B, 0x59, 0xB6),  # 보라 — S등급
    "YELLOW":  RGBColor(0xF3, 0x9C, 0x12),  # 노랑 — C등급
    "WHITE":   RGBColor(0xFF, 0xFF, 0xFF),
}

# ── 등급 기준 ──────────────────────────────────────────
GRADE_THRESHOLDS = [
    (91, "S"),
    (76, "A"),
    (56, "B"),
    (31, "C"),
    (0,  "D"),
]

GRADE_COLOR = {
    "S": COLOR["PURPLE"],
    "A": COLOR["BLUE"],
    "B": COLOR["GOOD"],
    "C": COLOR["YELLOW"],
    "D": COLOR["BAD"],
    "F": COLOR["BAD"],
}

# ── 슬라이드 인덱스 상수 ───────────────────────────────
SLIDE_INDEX = {
    "cover":        0,   # 1: 표지
    "score":        1,   # 2: 종합 점수 + 등급
    "competitor":   2,   # 3: 경쟁사 비교 차트
    "biz_info":     3,   # 4: 업체 기본정보 + 키워드 조회수
    "keywords":     4,   # 5: 확장 키워드
    "screenshot":   5,   # 6: 검색 결과 스크린샷
    "checklist":    6,   # 7: 22항목 진단 체크리스트
    "weak_points":  7,   # 8: 치명적 3가지
    "package":      8,   # 9: 패키지 소개
    "package_detail": 9, # 10: 패키지 상세
    "estimate":     10,  # 11: 견적서
}


def get_grade(score: int) -> str:
    """점수 → 등급 반환"""
    for threshold, grade in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return "D"


def log(tag: str, msg: str):
    """구조화된 로그 출력"""
    print(f"[{tag}] {msg}")
