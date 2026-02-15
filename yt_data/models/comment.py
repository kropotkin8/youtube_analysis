"""Modelo SQLAlchemy para comentarios de YouTube."""
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, BigInteger, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from yt_data.models.base import Base


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(String(128), primary_key=True)
    video_id = Column(String(64), ForeignKey("videos.video_id", ondelete="CASCADE"), nullable=False, index=True)
    author = Column(String(256), nullable=True)
    text = Column(Text, nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    like_count = Column(BigInteger, default=0)
    parent_id = Column(String(128), nullable=True, index=True)
    raw_snippet = Column(JSONB, nullable=True)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow)
