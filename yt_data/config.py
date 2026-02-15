"""Configuración cargada desde variables de entorno (.env)."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto (donde está el CLI)
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)

YT_API_KEY = os.getenv("YT_API_KEY", "")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://yt_user:yt_password@localhost:5432/youtube_analysis",
)

if not YT_API_KEY:
    import warnings
    warnings.warn("YT_API_KEY no definida en .env; las llamadas a la API fallarán.")
