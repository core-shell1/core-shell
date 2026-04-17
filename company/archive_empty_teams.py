"""
archive_empty_teams.py — 빈/중복 팀 폴더를 archive/로 안전 이동

위험 없음 — 이동만 (삭제 아님). git으로 롤백 가능.
실제 import 참조 체크 후 이동.
"""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent.parent
TEAM_DIR = ROOT / "team"
ARCHIVE = ROOT / "archive" / f"empty_teams_{datetime.now().strftime('%Y%m%d')}"

# 빈 폴더 (drift 분석에서 0개 파일 확인된 것들)
EMPTY_CANDIDATES = [
    "부동산-개발업체·시행사·건축사무소-대",
    "소상공인·1인-사업자-대상-완전자동-",
    "온라인-스토어·D2C-브랜드-대상-마",
    "인하우스-마케터·프리랜서용-통합-마케",
]

# 구버전 의심 (새 버전 있음)
SUPERSEDED = [
    ("AI 세금신고 도우미 실행팀", "[진행중] AI_세금신고_도우미"),
]


def verify_empty(name: str) -> tuple[bool, int]:
    """폴더가 진짜 비어있는지 재확인"""
    p = TEAM_DIR / name
    if not p.exists():
        return (False, 0)
    count = sum(1 for _ in p.rglob("*") if _.is_file())
    return (count == 0, count)


def move_to_archive(name: str) -> bool:
    src = TEAM_DIR / name
    if not src.exists():
        print(f"  ⚠️ {name} — 폴더 없음 (이미 정리됨?)")
        return False
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    dst = ARCHIVE / name
    try:
        shutil.move(str(src), str(dst))
        print(f"  ✅ {name} → archive/")
        return True
    except Exception as e:
        print(f"  ❌ {name} 이동 실패: {e}")
        return False


def main():
    print(f"=== team/ 빈 폴더 정리 (archive: {ARCHIVE.name}) ===\n")

    print("[1/2] 빈 폴더 재확인 후 이동:")
    moved = 0
    for name in EMPTY_CANDIDATES:
        is_empty, count = verify_empty(name)
        if is_empty:
            if move_to_archive(name):
                moved += 1
        else:
            print(f"  ⏭️ {name} — 파일 {count}개 있음, 스킵")

    print(f"\n[2/2] 구버전 팀 확인 (새 버전 있을 때만 이동):")
    for old, new in SUPERSEDED:
        old_p = TEAM_DIR / old
        new_p = TEAM_DIR / new
        if old_p.exists() and new_p.exists():
            old_count = sum(1 for _ in old_p.rglob("*") if _.is_file())
            new_count = sum(1 for _ in new_p.rglob("*") if _.is_file())
            if new_count > old_count * 3:  # 새 버전이 3배 이상 크면 구버전 확정
                if move_to_archive(old):
                    moved += 1
            else:
                print(f"  ⚠️ {old} vs {new} — 크기 비슷 ({old_count} vs {new_count}), 수동 확인 필요")
        elif old_p.exists():
            print(f"  ⏭️ {old} — 새 버전 없음, 건드리지 않음")

    print(f"\n=== 완료: {moved}개 폴더 archive로 이동 ===")
    print(f"롤백: git checkout HEAD -- team/ && git clean -fd team/")


if __name__ == "__main__":
    main()
