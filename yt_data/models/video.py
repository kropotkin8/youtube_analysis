"""Modelo SQLAlchemy para videos de YouTube."""
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

from yt_data.models.base import Base


class Video(Base):
    __tablename__ = "videos"

    video_id = Column(String(64), primary_key=True)
    channel_id = Column(String(64), nullable=True, index=True)
    title = Column(String(1024), nullable=True)
    description = Column(Text, nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    duration = Column(String(32), nullable=True)  # ISO 8601 (ej. PT5M30S)
    category_id = Column(String(32), nullable=True)
    raw_snippet = Column(JSONB, nullable=True)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow)
