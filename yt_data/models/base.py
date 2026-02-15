"""Base SQLAlchemy y sesión para PostgreSQL."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from yt_data.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    """Factory de sesión para uso en ETL."""
    return SessionLocal()


def init_db():
    """Crea todas las tablas definidas en los modelos."""
    Base.metadata.create_all(bind=engine)
