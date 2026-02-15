"""Transformación de commentThreads.list al formato del modelo Comment."""
from typing import Any

from dateutil import parser as date_parser


def _parse_datetime(s: str | None) -> object | None:
    if not s:
        return None
    try:
        return date_parser.isoparse(s)
    except Exception:
        return None


def transform_comment(raw: dict[str, Any]) -> dict[str, Any]:
    """
    Convierte un comentario ya aplanado (de extract_all_comments_for_video)
    o un snippet de topLevelComment/reply en un dict para el modelo Comment.

    Args:
        raw: Dict con comment_id, video_id, author, text, published_at, like_count, parent_id, raw_snippet.

    Returns:
        Mismo formato normalizado (published_at como datetime si viene string).
    """
    out = {
        "comment_id": raw.get("comment_id"),
        "video_id": raw.get("video_id"),
        "author": raw.get("author"),
        "text": raw.get("text"),
        "published_at": raw.get("published_at"),
        "like_count": int(raw.get("like_count", 0)) if raw.get("like_count") is not None else 0,
        "parent_id": raw.get("parent_id"),
        "raw_snippet": raw.get("raw_snippet"),
    }
    if isinstance(out["published_at"], str):
        out["published_at"] = _parse_datetime(out["published_at"])
    return out


def transform_comments(raw_list: list[dict]) -> list[dict]:
    """Transforma una lista de comentarios en bruto."""
    return [transform_comment(c) for c in raw_list if c.get("comment_id")]
