"""Extracción de búsqueda desde YouTube Data API v3 (search.list)."""
import logging
from typing import Optional

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from yt_data.config import YT_API_KEY

logger = logging.getLogger(__name__)


def extract_search(
    q: str,
    *,
    type: str = "video",
    max_results: int = 25,
    page_token: Optional[str] = None,
    region_code: Optional[str] = None,
) -> tuple[list[str], Optional[str]]:
    """
    Llama a search.list y devuelve una lista de video IDs (para luego usar videos.list).

    Args:
        q: Query de búsqueda.
        type: Tipo de recurso (video, channel, playlist).
        max_results: 1-50.
        page_token: Paginación.
        region_code: Código de región.

    Returns:
        (lista de video_ids, next_page_token o None).
    """
    if not YT_API_KEY:
        raise ValueError("YT_API_KEY no configurada en .env")

    youtube = build("youtube", "v3", developerKey=YT_API_KEY)
    try:
        kwargs = {
            "part": "id",
            "q": q,
            "type": type,
            "maxResults": min(max_results, 50),
        }
        if page_token:
            kwargs["pageToken"] = page_token
        if region_code:
            kwargs["regionCode"] = region_code
        request = youtube.search().list(**kwargs)
        response = request.execute()
        items = response.get("items", [])
        video_ids = []
        for it in items:
            vid = it.get("id", {}).get("videoId")
            if vid:
                video_ids.append(vid)
        next_token = response.get("nextPageToken")
        logger.info("search.list q=%r: %d video IDs", q, len(video_ids))
        return video_ids, next_token
    except HttpError as e:
        logger.exception("search.list error: %s", e)
        raise
