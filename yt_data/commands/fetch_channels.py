"""Comando: extraer canales por IDs, transformar y cargar en PostgreSQL."""
import typer

from yt_data.etl.extract import extract_channels
from yt_data.etl.transform import transform_channels
from yt_data.etl.load import load_channels

app = typer.Typer(help="Fetch channels by IDs and load into PostgreSQL")


@app.command("by-ids")
def fetch_by_ids(
    channel_ids: str = typer.Argument(..., help="Comma-separated channel IDs"),
) -> None:
    """Fetch channels by IDs (channels.list) and load into DB."""
    ids = [x.strip() for x in channel_ids.split(",") if x.strip()]
    if not ids:
        typer.echo("No channel IDs provided.")
        raise typer.Exit(1)
    raw = extract_channels(channel_ids=ids)
    if not raw:
        typer.echo("No channels returned.")
        raise typer.Exit(0)
    rows = transform_channels(raw)
    count = load_channels(rows)
    typer.echo(f"Loaded {count} channels.")


def register(parent: typer.Typer) -> None:
    parent.add_typer(app, name="channels")
