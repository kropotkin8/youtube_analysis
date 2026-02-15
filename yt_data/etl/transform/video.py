"""Transformación de respuestas videos.list al formato del modelo Video."""
from datetime import datetime
from typing import Any

from dateutil import parser as date_parser


def _parse_datetime(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return date_parser.isoparse(s)
    except Exception:
        return None


def transform_video(item: dict[str, Any]) -> dict[str, Any]:
    """
    Convierte un item de videos.list en un dict listo para insertar en Video.

    Args:
        item: Elemento de response["items"] de videos.list (con snippet, contentDetails, statistics).

    Returns:
        Dict con video_id, channel_id, title, description, published_at, duration, category_id, raw_snippet.
    """
    vid = item.get("id")
    if not vid:
        return {}
    snippet = item.get("snippet", {})
    content = item.get("contentDetails", {})
    return {
        "video_id": vid,
        "channel_id": snippet.get("channelId"),
        "title": snippet.get("title"),
        "description": snippet.get("description"),
        "published_at": _parse_datetime(snippet.get("publishedAt")),
        "duration": content.get("duration"),
        "category_id": snippet.get("categoryId"),
        "raw_snippet": snippet,
    }


def transform_videos(items: list[dict]) -> list[dict]:
    """Transforma una lista de items de videos.list."""
    return [transform_video(i) for i in items if i]
