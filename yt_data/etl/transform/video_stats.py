"""Transformación de statistics de videos.list al formato VideoStats (snapshot)."""
from datetime import datetime, timezone
from typing import Any


def _int_or_zero(v: Any) -> int:
    try:
        return int(v) if v is not None else 0
    except (TypeError, ValueError):
        return 0


def transform_video_stats(
    item: dict[str, Any],
    snapshot_time: datetime | None = None,
) -> dict[str, Any]:
    """
    Convierte un item de videos.list (con statistics) en un registro de video_stats_timeseries.

    Args:
        item: Elemento de videos.list con al menos "id" y "statistics".
        snapshot_time: Momento del snapshot; por defecto now UTC.

    Returns:
        Dict con video_id, snapshot_time, view_count, like_count, comment_count, favorite_count.
    """
    vid = item.get("id")
    if not vid:
        return {}
    stats = item.get("statistics", {})
    return {
        "video_id": vid,
        "snapshot_time": snapshot_time or datetime.now(timezone.utc),
        "view_count": _int_or_zero(stats.get("viewCount")),
        "like_count": _int_or_zero(stats.get("likeCount")),
        "comment_count": _int_or_zero(stats.get("commentCount")),
        "favorite_count": _int_or_zero(stats.get("favoriteCount")),
    }


def transform_video_stats_batch(
    items: list[dict],
    snapshot_time: datetime | None = None,
) -> list[dict]:
    """Transforma una lista de items a registros de video_stats_timeseries."""
    return [transform_video_stats(i, snapshot_time) for i in items if i.get("id")]
