"""Comando: extraer videos (trending o por IDs), transformar y cargar en PostgreSQL."""
import logging
from typing import Optional

import typer

from yt_data.etl.extract import extract_videos
from yt_data.etl.transform import transform_videos
from yt_data.etl.load import load_videos

logger = logging.getLogger(__name__)
app = typer.Typer(help="Fetch videos (trending or by IDs) and load into PostgreSQL")


@app.command("trending")
def fetch_trending(
    region: str = typer.Option("ES", "--region", "-r", help="Region code (e.g. ES, US)"),
    category_id: Optional[str] = typer.Option(None, "--category", "-c", help="Video category ID"),
    limit: int = typer.Option(50, "--limit", "-n", help="Max results (1-50)"),
) -> None:
    """Fetch trending videos (videos.list chart=mostPopular) and load into DB."""
    raw = extract_videos(chart="mostPopular", region_code=region or None, video_category_id=category_id, max_results=limit)
    if not raw:
        typer.echo("No videos returned.")
        raise typer.Exit(0)
    rows = transform_videos(raw)
    count = load_videos(rows)
    typer.echo(f"Loaded {count} videos (trending, region={region}).")


@app.command("by-ids")
def fetch_by_ids(
    video_ids: str = typer.Argument(..., help="Comma-separated video IDs"),
) -> None:
    """Fetch videos by IDs (videos.list id=...) and load into DB."""
    ids = [x.strip() for x in video_ids.split(",") if x.strip()]
    if not ids:
        typer.echo("No video IDs provided.")
        raise typer.Exit(1)
    raw = extract_videos(video_ids=ids)
    if not raw:
        typer.echo("No videos returned.")
        raise typer.Exit(0)
    rows = transform_videos(raw)
    count = load_videos(rows)
    typer.echo(f"Loaded {count} videos.")


def register(parent: typer.Typer) -> None:
    parent.add_typer(app, name="videos")
