# PM 계획 — 지역 소상공인 010번호 + 인스타 수집 툴

## 개발 태스크 우선순위

### Must (핵심)
1. models/database.py + business.py + history.py (SQLAlchemy)
2. collectors/base_collector.py (인터페이스)
3. collectors/naver_place.py (기존 main_v2.py 재활용)
4. collectors/kakao_maps.py (신규, 가장 중요)
5. validators/phone_filter.py (010 필터링)
6. validators/deduplicator.py (중복 제거)
7. services/collection_service.py (오케스트레이터)
8. services/export_service.py (엑셀 내보내기)
9. workers/collection_worker.py (QThread)
10. GUI 4개 화면

### Should
11. validators/naver_place.py (실존 검증)
12. collectors/daangn.py (기존 main_v2.py 재활용)
13. collectors/instagram.py (보조)
14. services/history_service.py (이력 관리)

### Could
15. collectors/google_maps.py (선택 옵션, 봇 차단 리스크)
16. collectors/naver_blog.py (보조)
