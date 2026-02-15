"""Transformación de respuestas channels.list al formato del modelo Channel."""
from typing import Any


def transform_channel(item: dict[str, Any]) -> dict[str, Any]:
    """
    Convierte un item de channels.list en un dict listo para insertar en Channel.

    Args:
        item: Elemento de response["items"] de channels.list.

    Returns:
        Dict con channel_id, title, description, subscriber_count, raw_snippet.
    """
    sid = item.get("id") or item.get("snippet", {}).get("channelId")
    if not sid:
        return {}
    snippet = item.get("snippet", {})
    statistics = item.get("statistics", {})
    try:
        sub_count = int(statistics.get("subscriberCount", 0))
    except (TypeError, ValueError):
        sub_count = 0
    return {
        "channel_id": sid,
        "title": snippet.get("title"),
        "description": snippet.get("description"),
        "subscriber_count": sub_count,
        "raw_snippet": snippet,
    }


def transform_channels(items: list[dict]) -> list[dict]:
    """Transforma una lista de items de channels.list."""
    return [transform_channel(i) for i in items if i]
