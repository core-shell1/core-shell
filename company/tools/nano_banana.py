"""
nano_banana.py — fal.ai nano-banana-2/edit 기반 제품 광고 이미지 자동 생성

사용처: 마케팅팀 에이전트의 카드뉴스/광고 이미지 생성

사용법:
    from tools.nano_banana import generate_ad_image, generate_from_references

    # 단순 이미지 편집/생성
    path = generate_ad_image(
        prompt="mystical forest with glowing trees",
        image_url="https://example.com/product.jpg",
        output_dir="outputs/"
    )

    # 레퍼런스 스타일 따라 제품 광고 이미지 생성
    path = generate_from_references(
        product_image="path/to/product.jpg",
        reference_images=["path/to/ref1.jpg", "path/to/ref2.jpg"],
        style_hint="luxury minimal, soft lighting",
        output_dir="outputs/"
    )
"""
import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Windows 인코딩
if sys.platform == "win32":
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# FAL_KEY 필수
if not os.getenv("FAL_KEY"):
    raise RuntimeError("FAL_KEY 환경변수 없음 (.env 확인)")

import fal_client
import requests


def _download(url: str, path: Path) -> Path:
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    path.write_bytes(r.content)
    return path


def generate_ad_image(
    prompt: str,
    image_url: str,
    output_dir: str | Path,
    aspect_ratio: str = "4:5",
    resolution: str = "2K",
    filename: str | None = None,
) -> Path | None:
    """
    nano-banana-2/edit으로 제품 이미지 편집.

    Args:
        prompt: 영어 프롬프트 (스타일 지시)
        image_url: 입력 이미지 URL (인터넷 접근 가능)
        output_dir: 저장 폴더
        aspect_ratio: "4:5", "1:1", "16:9", "9:16"
        resolution: "1K", "2K"
        filename: 저장 파일명 (없으면 타임스탬프)

    Returns:
        저장된 이미지 경로 or None
    """
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not filename:
        filename = f"nano_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

    result = fal_client.run(
        "fal-ai/nano-banana/edit",
        arguments={
            "prompt": prompt,
            "image_urls": [image_url],
            "aspect_ratio": aspect_ratio,
            "num_images": 1,
        },
    )

    # 결과에서 이미지 URL 추출
    images = result.get("images") or result.get("output", {}).get("images") or []
    if not images:
        print(f"[nano-banana] 이미지 생성 실패: {result}")
        return None

    img_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    if not img_url:
        return None

    saved = _download(img_url, out_dir / filename)
    print(f"[nano-banana] 저장: {saved}")
    return saved


def generate_from_references(
    product_image: str,
    reference_images: list[str],
    style_hint: str,
    output_dir: str | Path,
    aspect_ratio: str = "4:5",
) -> Path | None:
    """
    레퍼런스 이미지 스타일 분석 → 제품 이미지에 적용.
    fal_client.upload_file()로 로컬 파일 업로드 후 nano-banana에 전달.

    Args:
        product_image: 제품 이미지 로컬 경로
        reference_images: 스타일 레퍼런스 이미지 로컬 경로들
        style_hint: 스타일 힌트 (예: "luxury minimal", "street editorial")
        output_dir: 저장 폴더

    Returns:
        저장된 광고 이미지 경로
    """
    # 로컬 파일 → fal CDN 업로드
    product_url = fal_client.upload_file(product_image)
    ref_urls = [fal_client.upload_file(r) for r in reference_images]

    # 프롬프트 조합
    prompt = (
        f"Apply the visual style from reference images to this product. "
        f"Style: {style_hint}. "
        f"Keep product identity intact, match lighting, color grading, and composition of references. "
        f"High quality product advertisement."
    )

    # nano-banana edit은 image_urls에 여러 장 넣을 수 있음
    result = fal_client.run(
        "fal-ai/nano-banana/edit",
        arguments={
            "prompt": prompt,
            "image_urls": [product_url] + ref_urls,
            "aspect_ratio": aspect_ratio,
            "num_images": 1,
        },
    )

    images = result.get("images", [])
    if not images:
        print(f"[nano-banana refs] 생성 실패: {result}")
        return None

    img_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = f"ad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    saved = _download(img_url, out_dir / filename)
    print(f"[nano-banana refs] 저장: {saved}")
    return saved


if __name__ == "__main__":
    # CLI 테스트
    if len(sys.argv) < 3:
        print("사용법: python nano_banana.py <이미지URL> <프롬프트>")
        print("예시: python nano_banana.py https://example.com/p.jpg 'soft pastel background'")
        sys.exit(1)

    url = sys.argv[1]
    prompt = sys.argv[2]
    out = generate_ad_image(prompt=prompt, image_url=url, output_dir="outputs/nano_banana")
    print(f"결과: {out}")
