"""Extracción de videos desde YouTube Data API v3 (videos.list)."""
import logging
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from yt_data.config import YT_API_KEY

logger = logging.getLogger(__name__)


def extract_videos(
    video_ids: Optional[list[str]] = None,
    *,
    chart: Optional[str] = None,
    region_code: Optional[str] = None,
    video_category_id: Optional[str] = None,
    part: str = "snippet,contentDetails,statistics",
    max_results: int = 50,
) -> list[dict]:
    """
    Llama a videos.list y devuelve la lista de recursos en bruto.

    Args:
        video_ids: Lista de IDs de video (máx 50). Si se pasa, se usa id=...
        chart: Si "mostPopular", obtiene trending (ignora video_ids).
        region_code: Código de región (ej. ES, US) para chart=mostPopular.
        video_category_id: Categoría para chart (opcional).
        part: Partes a solicitar.
        max_results: Máximo por página (1-50).

    Returns:
        Lista de dicts con la respuesta de la API por cada video.
    """
    if not YT_API_KEY:
        raise ValueError("YT_API_KEY no configurada en .env")

    youtube = build("youtube", "v3", developerKey=YT_API_KEY)
    all_items = []

    try:
        if chart == "mostPopular":
            kwargs = {
                "part": part,
                "chart": "mostPopular",
                "maxResults": min(max_results, 50),
            }
            if region_code:
                kwargs["regionCode"] = region_code
            if video_category_id:
                kwargs["videoCategoryId"] = video_category_id
            request = youtube.videos().list(**kwargs)
        elif video_ids:
            request = youtube.videos().list(
                part=part,
                id=",".join(video_ids[:50]),
                maxResults=min(len(video_ids), 50),
            )
        else:
            logger.warning("extract_videos: se requiere video_ids o chart=mostPopular")
            return []

        response = request.execute()
        all_items = response.get("items", [])
        logger.info("videos.list: %d videos obtenidos", len(all_items))
    except HttpError as e:
        logger.exception("videos.list error: %s", e)
        raise

    return all_items
