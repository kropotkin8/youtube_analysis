"""Modelo SQLAlchemy para series temporales de estadísticas de video."""
from datetime import datetime
from sqlalchemy import Column, Integer, BigInteger, DateTime, ForeignKey, String

from yt_data.models.base import Base


class VideoStats(Base):
    __tablename__ = "video_stats_timeseries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(String(64), ForeignKey("videos.video_id", ondelete="CASCADE"), nullable=False, index=True)
    snapshot_time = Column(DateTime(timezone=True), nullable=False)
    view_count = Column(BigInteger, default=0)
    like_count = Column(BigInteger, default=0)
    comment_count = Column(BigInteger, default=0)
    favorite_count = Column(BigInteger, default=0)
