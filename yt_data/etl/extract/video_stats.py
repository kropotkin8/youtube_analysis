"""Extracción de estadísticas de video desde YouTube Data API v3 (videos.list part=statistics)."""
import logging
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from yt_data.config import YT_API_KEY

logger = logging.getLogger(__name__)


def extract_video_stats(
    video_ids: list[str],
    *,
    part: str = "statistics",
    max_results: int = 50,
) -> list[dict]:
    """
    Llama a videos.list con part=statistics para obtener métricas actuales.
    Pensado para snapshots de series temporales (video_stats_timeseries).

    Args:
        video_ids: Lista de IDs de video (máx 50 por request).
        part: Partes (por defecto solo statistics).
        max_results: Máximo por página.

    Returns:
        Lista de dicts con id y statistics por video.
    """
    if not video_ids:
        return []
    if not YT_API_KEY:
        raise ValueError("YT_API_KEY no configurada en .env")

    youtube = build("youtube", "v3", developerKey=YT_API_KEY)
    all_items = []
    chunk = video_ids[:max_results]

    try:
        request = youtube.videos().list(
            part=part,
            id=",".join(chunk),
            maxResults=len(chunk),
        )
        response = request.execute()
        all_items = response.get("items", [])
        logger.info("videos.list(statistics): %d videos obtenidos", len(all_items))
    except HttpError as e:
        logger.exception("videos.list(statistics) error: %s", e)
        raise

    return all_items
