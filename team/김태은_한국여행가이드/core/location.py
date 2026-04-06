import math
from typing import Optional


RADIUS_STEPS = [1.0, 2.0, 5.0]  # km


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """두 GPS 좌표 간 거리를 km로 반환 (Haversine 공식)."""
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def walk_minutes(distance_km: float) -> int:
    """거리를 도보 시간(분)으로 변환. 도보 속도 80m/분 기준."""
    return max(1, round(distance_km / 0.08))


def filter_by_radius(
    restaurants: list,
    lat: float,
    lng: float,
    radius_km: float = 1.0,
) -> Optional[list]:
    """
    주어진 반경(km) 내 식당 필터링.
    거리 기준 오름차순 정렬.
    결과 없으면 None 반환.
    """
    nearby = []
    for r in restaurants:
        r_lat = r.get("lat")
        r_lng = r.get("lng")
        if r_lat is None or r_lng is None:
            continue
        d = haversine(lat, lng, r_lat, r_lng)
        if d <= radius_km:
            nearby.append({**r, "distance_km": round(d, 2), "walk_minutes": walk_minutes(d)})

    if not nearby:
        return None

    nearby.sort(key=lambda x: x["distance_km"])
    return nearby


def auto_expand_radius(restaurants: list, lat: float, lng: float) -> tuple[list, float]:
    """
    1km → 2km → 5km 자동 확장.
    결과 있으면 (식당 리스트, 적용된 반경) 반환.
    모든 반경에도 없으면 전체 식당 거리순 반환 (반경 99.0).
    """
    for radius in RADIUS_STEPS:
        result = filter_by_radius(restaurants, lat, lng, radius)
        if result:
            return result, radius

    # 최후 fallback: 전체 식당 거리순 반환
    all_with_distance = []
    for r in restaurants:
        r_lat = r.get("lat")
        r_lng = r.get("lng")
        if r_lat is None or r_lng is None:
            d = 99.0
        else:
            d = haversine(lat, lng, r_lat, r_lng)
        all_with_distance.append({**r, "distance_km": round(d, 2), "walk_minutes": walk_minutes(d)})

    all_with_distance.sort(key=lambda x: x["distance_km"])
    return all_with_distance[:10], 99.0
