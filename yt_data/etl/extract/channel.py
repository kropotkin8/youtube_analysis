"""Extracción de canales desde YouTube Data API v3 (channels.list)."""
import logging
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from yt_data.config import YT_API_KEY

logger = logging.getLogger(__name__)


def extract_channels(
    channel_ids: Optional[list[str]] = None,
    *,
    part: str = "snippet,statistics",
    max_results: int = 50,
) -> list[dict]:
    """
    Llama a channels.list y devuelve la lista de recursos en bruto.

    Args:
        channel_ids: Lista de IDs de canal (máx 50 por request). Si None, no se hace request.
        part: Partes a solicitar (snippet, statistics, etc.).
        max_results: Máximo por página (1-50).

    Returns:
        Lista de dicts con la respuesta de la API por cada canal.
    """
    if not channel_ids:
        return []
    if not YT_API_KEY:
        raise ValueError("YT_API_KEY no configurada en .env")

    youtube = build("youtube", "v3", developerKey=YT_API_KEY)
    all_items = []
    ids_chunk = channel_ids[:max_results]

    try:
        request = youtube.channels().list(
            part=part,
            id=",".join(ids_chunk),
            maxResults=len(ids_chunk),
        )
        response = request.execute()
        all_items.extend(response.get("items", []))
        logger.info("channels.list: %d canales obtenidos", len(all_items))
    except HttpError as e:
        logger.exception("channels.list error: %s", e)
        raise

    return all_items
