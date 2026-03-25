#!/usr/bin/env python3
"""
파이프라인 복구 스크립트 — 저장된 파일에서 컨텍스트 복원 후 나머지 단계 실행
사용법: python resume_pipeline.py <output_dir>
"""
import sys
import os
import io
import json

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from agents import jihun, jongbum, sua
from core.pipeline import get_client
from core.output import save_file


def main():
    if len(sys.argv) < 2:
        print("사용법: python resume_pipeline.py <output_dir>")
        sys.exit(1)

    output_dir = sys.argv[1]
    print(f"\n📂 복구 중: {output_dir}\n")

    # 저장된 파일에서 컨텍스트 복원
    def read_file(filename):
        path = os.path.join(output_dir, filename)
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                return f.read()
        return ""

    with open(os.path.join(output_dir, "04_최종판단_준혁.json"), encoding='utf-8') as f:
        junhyeok_data = json.load(f)

    idea = "지역 소상공인 010번호 + 인스타 자동 수집 시스템. 오프라인 마케팅(문자 영업)용. 지역명 입력하면 구글맵, 카카오맵, 당근마켓, 인스타그램, 네이버블로그/카페에서 업체명과 010번호(문자수신가능) 또는 인스타계정을 수집. 031/032 등 유선번호 자동제거. 수집 후 네이버플레이스에서 실제 업체 존재 검증. 없는 업체 제거. 최종 엑셀: 업체명-010번호-네이버플레이스URL-인스타URL. 전업종 대상."

    context = {
        "idea": idea,
        "clarified": idea,
        "is_commercial": False,
        "taeho": read_file("08_트렌드_태호.md"),
        "seoyun": read_file("01_시장조사_서윤.md"),
        "minsu": read_file("02_전략_민수.md"),
        "haeun": read_file("03_검증_하은.md"),
        "junhyeok_text": junhyeok_data["text"],
        "verdict": junhyeok_data["verdict"],
        "score": junhyeok_data["score"],
    }

    client = get_client()

    # [6/9] PRD
    print("\n[6/9] PRD 작성...")
    jihun_result = jihun.run(context, client)
    context["jihun"] = jihun_result
    save_file(output_dir, "05_PRD_지훈.md", jihun_result)
    print("  [저장] 05_PRD_지훈.md")

    # [7/9] 구현 지시서
    print("\n[7/9] 구현 지시서...")
    jongbum_result = jongbum.run(context, client)
    context["jongbum"] = jongbum_result
    save_file(output_dir, "06_구현지시서_종범.md", jongbum_result)
    print("  [저장] 06_구현지시서_종범.md")

    # projects/ 폴더에 CLAUDE.md 저장
    project_name = idea[:20].strip().replace(" ", "_")
    project_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "projects", project_name
    )
    os.makedirs(project_dir, exist_ok=True)

    from datetime import date
    claude_md_header = f"""> **LAINCP 자동 생성 프로젝트**
> 리안 컴퍼니 파이프라인이 생성한 구현 지시서야.
> 이 폴더에서 Claude Code 열고 `/work` 입력하면 Wave 1~6 자동 실행돼.
>
> - **프로젝트 유형**: 개인 툴
> - **아이디어**: {idea[:80]}
> - **생성일**: {date.today()}

---

"""
    save_file(project_dir, "CLAUDE.md", claude_md_header + jongbum_result)
    print(f"  /work 준비 완료: projects/{project_name}/CLAUDE.md")

    # [9/9] 마케팅
    print("\n[9/9] 마케팅 전략...")
    sua_result = sua.run(context, client)
    context["sua"] = sua_result
    save_file(output_dir, "07_마케팅_수아.md", sua_result)
    print("  [저장] 07_마케팅_수아.md")

    print(f"\n\n{'='*60}")
    print(f"  완료!")
    print(f"  산출물: {output_dir}")
    print(f"  /work 실행: projects/{project_name}/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
