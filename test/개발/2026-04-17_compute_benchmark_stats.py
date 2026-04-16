#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
benchmark_premium 테이블에서 카테고리별 벤치마크 통계 계산.
서울 핫플 상위권 데이터를 기반으로 실제 수치 산출.
"""
import sys
import asyncio
from pathlib import Path
from statistics import quantiles, mean
from collections import defaultdict

PROJECT_ROOT = Path("C:/Users/lian1/Documents/Work/core/team/[진행중] 오프라인 마케팅/소상공인_영업툴/naver-diagnosis")
sys.path.insert(0, str(PROJECT_ROOT))

import os
from dotenv import load_dotenv

# core/company/.env 중앙 로드
for _p in Path(__file__).resolve().parents:
    if (_p / "company" / ".env").exists():
        load_dotenv(_p / "company" / ".env")
        break
else:
    load_dotenv()

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from models import BenchmarkPremium

DB_URL = os.getenv("DATABASE_URL", f"sqlite+aiosqlite:///{PROJECT_ROOT}/diagnosis.db")


async def main():
    """메인 함수: 벤치마크 통계 계산 및 출력."""

    engine = create_async_engine(DB_URL, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession)

    async with async_session() as db:
        # benchmark_premium 전체 데이터 로드
        result = await db.execute(select(BenchmarkPremium))
        records = result.scalars().all()

        print(f"\n========== Benchmark Premium Statistics ==========")
        print(f"Total records: {len(records)}\n")

        # 카테고리별 분류
        by_category = defaultdict(list)
        for record in records:
            by_category[record.category].append(record)

        # 카테고리별 통계 계산
        stats_by_category = {}

        for category in sorted(by_category.keys()):
            records_for_cat = by_category[category]
            count = len(records_for_cat)

            # 데이터 추출
            photos = [r.photo_count for r in records_for_cat]
            total_reviews = [
                r.visitor_review_count + r.receipt_review_count
                for r in records_for_cat
            ]
            blogs = [r.blog_review_count for r in records_for_cat]

            # Boolean 필드 채택률
            has_booking = sum(1 for r in records_for_cat if r.has_booking) / count
            has_instagram = sum(1 for r in records_for_cat if r.has_instagram) / count
            has_owner_reply = sum(1 for r in records_for_cat if r.has_owner_reply) / count
            has_coupon = sum(1 for r in records_for_cat if r.has_coupon) / count
            has_talktalk = sum(1 for r in records_for_cat if r.has_talktalk) / count
            has_news = sum(1 for r in records_for_cat if r.has_news) / count

            # 백분위수 계산 (statistics.quantiles 사용)
            def calc_percentiles(data):
                if not data:
                    return {"p10": 0, "p25": 0, "p50": 0, "p75": 0, "p90": 0, "mean": 0}
                if len(data) == 1:
                    return {"p10": data[0], "p25": data[0], "p50": data[0], "p75": data[0], "p90": data[0], "mean": data[0]}

                # quantiles(data, n=10) = [p10, p20, ..., p90]
                q10 = quantiles(data, n=10)
                q4 = quantiles(data, n=4)  # [p25, p50, p75]

                return {
                    "p10": int(q10[0]),
                    "p25": int(q4[0]),
                    "p50": int(q4[1]),
                    "p75": int(q4[2]),
                    "p90": int(q10[8]),
                    "mean": int(mean(data)),
                }

            photo_stats = calc_percentiles(photos)
            review_stats = calc_percentiles(total_reviews)
            blog_stats = calc_percentiles(blogs)

            stats_by_category[category] = {
                "sample_size": count,
                "photo": photo_stats,
                "total_review": review_stats,
                "blog": blog_stats,
                "adoption_rates": {
                    "has_booking": round(has_booking, 3),
                    "has_instagram": round(has_instagram, 3),
                    "has_owner_reply": round(has_owner_reply, 3),
                    "has_coupon": round(has_coupon, 3),
                    "has_talktalk": round(has_talktalk, 3),
                    "has_news": round(has_news, 3),
                }
            }

            # 출력
            print(f"\n--- Category: {category} (n={count}) ---")
            print(f"Photo count:")
            print(f"  p10: {photo_stats['p10']}, p25: {photo_stats['p25']}, p50: {photo_stats['p50']}, p75: {photo_stats['p75']}, p90: {photo_stats['p90']}, mean: {photo_stats['mean']}")
            print(f"Total review (visitor + receipt):")
            print(f"  p10: {review_stats['p10']}, p25: {review_stats['p25']}, p50: {review_stats['p50']}, p75: {review_stats['p75']}, p90: {review_stats['p90']}, mean: {review_stats['mean']}")
            print(f"Blog review:")
            print(f"  p10: {blog_stats['p10']}, p25: {blog_stats['p25']}, p50: {blog_stats['p50']}, p75: {blog_stats['p75']}, p90: {blog_stats['p90']}, mean: {blog_stats['mean']}")
            print(f"Adoption rates (0.0~1.0):")
            for k, v in stats_by_category[category]["adoption_rates"].items():
                print(f"  {k}: {v}")

        # 권장 COMPETITOR_FALLBACK 값 (p25를 기반으로 함)
        print(f"\n========== Recommended COMPETITOR_FALLBACK ==========")
        print(f"Use p25 for avg values, p75 for top_review\n")

        for category in sorted(stats_by_category.keys()):
            stats = stats_by_category[category]
            # p25를 avg, p75를 top_review로 사용 (지역 경쟁사 평균 수준)
            rec = {
                "avg_review": stats["total_review"]["p25"],
                "avg_photo": stats["photo"]["p25"],
                "avg_blog": stats["blog"]["p25"],
                "top_review": stats["total_review"]["p75"],
            }

            # industry_weights.py의 키로 매핑
            # 간단히 카테고리명 그대로 사용 (실제 수정 시 매핑 필요)
            print(f'    "{category}": {{')
            print(f'        "avg_review": {rec["avg_review"]},')
            print(f'        "avg_photo": {rec["avg_photo"]},')
            print(f'        "avg_blog": {rec["avg_blog"]},')
            print(f'        "top_review": {rec["top_review"]},')
            print(f'    }},')

        print()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
