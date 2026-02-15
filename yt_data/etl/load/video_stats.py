"""Carga de snapshots de estadísticas en video_stats_timeseries."""
import logging
from typing import Sequence

from yt_data.models import VideoStats, get_session

logger = logging.getLogger(__name__)


def load_video_stats(rows: Sequence[dict]) -> int:
    """
    Inserta filas en video_stats_timeseries (siempre insert, sin upsert; es serie temporal).

    Args:
        rows: Lista de dicts con video_id, snapshot_time, view_count, like_count, comment_count, favorite_count.

    Returns:
        Número de filas insertadas.
    """
    if not rows:
        return 0
    session = get_session()
    try:
        for r in rows:
            session.add(VideoStats(**r))
        session.commit()
        logger.info("load_video_stats: %d filas", len(rows))
        return len(rows)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
