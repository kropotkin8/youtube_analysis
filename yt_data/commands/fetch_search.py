"""Comando: búsqueda por keyword (search.list) y carga de videos en PostgreSQL."""
from typing import Optional

import typer

from yt_data.etl.extract import extract_search, extract_videos
from yt_data.etl.transform import transform_videos
from yt_data.etl.load import load_videos

app = typer.Typer(help="Search videos by keyword and load into PostgreSQL")


@app.command("videos")
def search_videos(
    query: str = typer.Argument(..., help="Search query (keyword)"),
    limit: int = typer.Option(25, "--limit", "-n", help="Max results (1-50)"),
    region: Optional[str] = typer.Option(None, "--region", "-r", help="Region code"),
) -> None:
    """Search videos (search.list) and fetch details (videos.list), then load into DB."""
    video_ids, _ = extract_search(query, max_results=limit, region_code=region)
    if not video_ids:
        typer.echo("No video IDs from search.")
        raise typer.Exit(0)
    raw = extract_videos(video_ids=video_ids)
    if not raw:
        typer.echo("No video details returned.")
        raise typer.Exit(0)
    rows = transform_videos(raw)
    count = load_videos(rows)
    typer.echo(f"Loaded {count} videos for query '{query}'.")


def register(parent: typer.Typer) -> None:
    parent.add_typer(app, name="search")
