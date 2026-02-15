"""Modelo SQLAlchemy para canales de YouTube."""
from datetime import datetime
from sqlalchemy import Column, String, BigInteger, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB

from yt_data.models.base import Base


class Channel(Base):
    __tablename__ = "channels"

    channel_id = Column(String(64), primary_key=True)
    title = Column(String(512), nullable=True)
    description = Column(Text, nullable=True)
    subscriber_count = Column(BigInteger, default=0)
    raw_snippet = Column(JSONB, nullable=True)
    inserted_at = Column(DateTime(timezone=True), default=datetime.utcnow)
