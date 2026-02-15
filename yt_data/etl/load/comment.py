"""Carga de comentarios en PostgreSQL."""
import logging
from typing import Sequence

from sqlalchemy.dialects.postgresql import insert as pg_insert

from yt_data.models import Comment, get_session

logger = logging.getLogger(__name__)


def load_comments(rows: Sequence[dict], *, upsert: bool = True) -> int:
    """
    Inserta o actualiza comentarios en la tabla comments.

    Args:
        rows: Lista de dicts con comment_id, video_id, author, text, published_at, like_count, parent_id, raw_snippet.
        upsert: Si True, ON CONFLICT (comment_id) DO UPDATE.

    Returns:
        Número de filas afectadas.
    """
    if not rows:
        return 0
    session = get_session()
    try:
        if upsert:
            stmt = pg_insert(Comment).values(rows)
            stmt = stmt.on_conflict_do_update(
                index_elements=["comment_id"],
                set_={
                    Comment.video_id: stmt.excluded.video_id,
                    Comment.author: stmt.excluded.author,
                    Comment.text: stmt.excluded.text,
                    Comment.published_at: stmt.excluded.published_at,
                    Comment.like_count: stmt.excluded.like_count,
                    Comment.parent_id: stmt.excluded.parent_id,
                    Comment.raw_snippet: stmt.excluded.raw_snippet,
                },
            )
            result = session.execute(stmt)
        else:
            for r in rows:
                session.merge(Comment(**r))
            result = None
        session.commit()
        count = len(rows) if result is None else result.rowcount
        logger.info("load_comments: %d filas", count)
        return count or len(rows)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
