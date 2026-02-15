"""Comando: extraer comentarios de un video y cargar en PostgreSQL."""
from typing import Optional

import typer

from yt_data.etl.extract import extract_all_comments_for_video
from yt_data.etl.transform import transform_comments
from yt_data.etl.load import load_comments

app = typer.Typer(help="Fetch comments for a video and load into PostgreSQL")


@app.command("for-video")
def fetch_for_video(
    video_id: str = typer.Argument(..., help="YouTube video ID"),
    max_pages: Optional[int] = typer.Option(None, "--max-pages", "-n", help="Max API pages (default: all)"),
) -> None:
    """Fetch all comment threads + replies for a video and load into DB."""
    raw = extract_all_comments_for_video(video_id, max_pages=max_pages)
    if not raw:
        typer.echo("No comments returned.")
        raise typer.Exit(0)
    rows = transform_comments(raw)
    count = load_comments(rows)
    typer.echo(f"Loaded {count} comments for video {video_id}.")


def register(parent: typer.Typer) -> None:
    parent.add_typer(app, name="comments")
