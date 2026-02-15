"""Carga de videos en PostgreSQL."""
import logging
from typing import Sequence

from sqlalchemy.dialects.postgresql import insert as pg_insert

from yt_data.models import Video, get_session

logger = logging.getLogger(__name__)


def load_videos(rows: Sequence[dict], *, upsert: bool = True) -> int:
    """
    Inserta o actualiza videos en la tabla videos.

    Args:
        rows: Lista de dicts con video_id, channel_id, title, description, published_at, duration, category_id, raw_snippet.
        upsert: Si True, ON CONFLICT (video_id) DO UPDATE.

    Returns:
        Número de filas afectadas.
    """
    if not rows:
        return 0
    session = get_session()
    try:
        if upsert:
            stmt = pg_insert(Video).values(rows)
            stmt = stmt.on_conflict_do_update(
                index_elements=["video_id"],
                set_={
                    Video.channel_id: stmt.excluded.channel_id,
                    Video.title: stmt.excluded.title,
                    Video.description: stmt.excluded.description,
                    Video.published_at: stmt.excluded.published_at,
                    Video.duration: stmt.excluded.duration,
                    Video.category_id: stmt.excluded.category_id,
                    Video.raw_snippet: stmt.excluded.raw_snippet,
                },
            )
            result = session.execute(stmt)
        else:
            for r in rows:
                session.merge(Video(**r))
            result = None
        session.commit()
        count = len(rows) if result is None else result.rowcount
        logger.info("load_videos: %d filas", count)
        return count or len(rows)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
