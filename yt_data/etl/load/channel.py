"""Carga de canales en PostgreSQL."""
import logging
from typing import Sequence

from sqlalchemy.dialects.postgresql import insert as pg_insert

from yt_data.models import Channel, get_session

logger = logging.getLogger(__name__)


def load_channels(rows: Sequence[dict], *, upsert: bool = True) -> int:
    """
    Inserta o actualiza canales en la tabla channels.

    Args:
        rows: Lista de dicts con channel_id, title, description, subscriber_count, raw_snippet.
        upsert: Si True, hace ON CONFLICT (channel_id) DO UPDATE.

    Returns:
        Número de filas afectadas.
    """
    if not rows:
        return 0
    session = get_session()
    try:
        if upsert:
            stmt = pg_insert(Channel).values(rows)
            stmt = stmt.on_conflict_do_update(
                index_elements=["channel_id"],
                set_={
                    Channel.title: stmt.excluded.title,
                    Channel.description: stmt.excluded.description,
                    Channel.subscriber_count: stmt.excluded.subscriber_count,
                    Channel.raw_snippet: stmt.excluded.raw_snippet,
                },
            )
            result = session.execute(stmt)
        else:
            for r in rows:
                session.merge(Channel(**r))
            result = None
        session.commit()
        count = len(rows) if result is None else result.rowcount
        logger.info("load_channels: %d filas", count)
        return count or len(rows)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
