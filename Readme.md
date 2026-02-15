# yt_data – ETL YouTube → PostgreSQL

Paquete con **Typer** que ejecuta comandos para extraer datos de **YouTube Data API v3**, transformarlos y cargarlos en **PostgreSQL**, usando modelos **SQLAlchemy**. Los secretos se leen desde un fichero **.env**.

## Estructura del proyecto

```
yt_data/
├── cli.py                 # Punto de entrada Typer
├── config.py               # YT_API_KEY, DATABASE_URL desde .env
├── models/                 # Modelos SQLAlchemy (un fichero por modelo)
│   ├── base.py
│   ├── channel.py
│   ├── video.py
│   ├── video_stats.py
│   └── comment.py
├── etl/
│   ├── extract/            # Llamadas a YouTube Data API v3
│   │   ├── channel.py      # channels.list
│   │   ├── video.py        # videos.list
│   │   ├── video_stats.py  # videos.list (statistics)
│   │   ├── comment.py      # commentThreads.list
│   │   └── search.py       # search.list
│   ├── transform/          # Formato API → modelo DB
│   │   ├── channel.py
│   │   ├── video.py
│   │   ├── video_stats.py
│   │   └── comment.py
│   └── load/               # Inserción en PostgreSQL
│       ├── channel.py
│       ├── video.py
│       ├── video_stats.py
│       └── comment.py
└── commands/               # Comandos para CLI y GitHub Actions
    ├── fetch_videos.py     # videos trending | by-ids
    ├── fetch_channels.py  # channels by-ids
    ├── fetch_video_stats.py # video-stats snapshot
    ├── fetch_comments.py  # comments for-video
    └── fetch_search.py    # search videos
```

## Requisitos

- Python 3.10+
- PostgreSQL (por ejemplo con `docker compose up -d`)
- **YT_API_KEY** en [Google Cloud Console](https://console.cloud.google.com/) (YouTube Data API v3)

## Instalación

1. Crear y activar entorno virtual:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

2. Instalar dependencias del ETL:

```bash
pip install -r requirements.txt
```

3. Instalar el proyecto en modo editable (desde la raíz del repo):

```bash
pip install -e .
```

Para ejecutar sin `pip install -e .`, ejecutar desde la raíz del proyecto:

```bash
cd youtube_analysis
python -m yt_data --help
```

4. Copiar `.env.example` a `.env` y rellenar:

```bash
cp .env.example .env
# Editar .env: YT_API_KEY=..., DATABASE_URL=...
```

5. Levantar PostgreSQL:

```bash
docker compose up -d
```

6. Crear tablas:

```bash
python -m yt_data init-db
```

## Uso de comandos (CLI y GitHub Actions)

- **Videos (trending):** `python -m yt_data videos trending --region ES --limit 50`
- **Videos por IDs:** `python -m yt_data videos by-ids "id1,id2,id3"`
- **Búsqueda por keyword:** `python -m yt_data search videos "machine learning" --limit 25`
- **Canales por IDs:** `python -m yt_data channels by-ids "UC...,UC..."`
- **Snapshot de estadísticas:** `python -m yt_data video-stats snapshot`
- **Comentarios de un video:** `python -m yt_data comments for-video "VIDEO_ID"`

En GitHub Actions, configurar secrets: **YT_API_KEY**, **DATABASE_URL**.

## Modelos (tablas)

- **channels:** channel_id, title, description, subscriber_count, raw_snippet, inserted_at
- **videos:** video_id, channel_id, title, description, published_at, duration, category_id, raw_snippet, inserted_at
- **video_stats_timeseries:** id, video_id, snapshot_time, view_count, like_count, comment_count, favorite_count
- **comments:** comment_id, video_id, author, text, published_at, like_count, parent_id, raw_snippet, inserted_at
