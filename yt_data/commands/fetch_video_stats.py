"""Comando: snapshot de estadísticas de videos (video_stats_timeseries)."""
from datetime import datetime, timezone

import typer
from sqlalchemy import select

from yt_data.etl.extract import extract_video_stats
from yt_data.etl.transform import transform_video_stats_batch
from yt_data.etl.load import load_video_stats
from yt_data.models import Video, get_session

app = typer.Typer(help="Snapshot video statistics into video_stats_timeseries")


@app.command("snapshot")
def snapshot_stats(
    video_ids: str = typer.Argument(None, help="Comma-separated video IDs (optional; if omitted, use all video_ids from DB)"),
) -> None:
    """Fetch current statistics for videos and insert a new snapshot row."""
    if video_ids:
        ids = [x.strip() for x in video_ids.split(",") if x.strip()]
    else:
        session = get_session()
        try:
            ids = list(session.scalars(select(Video.video_id)))
        finally:
            session.close()
        if not ids:
            typer.echo("No video IDs provided and no videos in DB.")
            raise typer.Exit(1)
    if not ids:
        typer.echo("No video IDs.")
        raise typer.Exit(1)
    raw = extract_video_stats(ids)
    if not raw:
        typer.echo("No stats returned.")
        raise typer.Exit(0)
    snapshot_time = datetime.now(timezone.utc)
    rows = transform_video_stats_batch(raw, snapshot_time=snapshot_time)
    count = load_video_stats(rows)
    typer.echo(f"Inserted {count} stats snapshots at {snapshot_time.isoformat()}.")


def register(parent: typer.Typer) -> None:
    parent.add_typer(app, name="video-stats")
