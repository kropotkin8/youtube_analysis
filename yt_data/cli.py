"""CLI Typer: punto de entrada para comandos ETL YouTube -> PostgreSQL."""
import logging
import typer

from yt_data.commands import register_all
from yt_data.models import init_db

cli = typer.Typer(
    name="yt-data",
    help="YouTube Data ETL: extraer datos de la API v3 y cargar en PostgreSQL.",
)

# Registrar todos los subcomandos (videos, channels, video-stats, comments)
register_all(cli)


@cli.command()
def init_db_cmd() -> None:
    """Crea las tablas en PostgreSQL (channels, videos, video_stats_timeseries, comments)."""
    init_db()
    typer.echo("Tablas creadas correctamente.")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    cli()


if __name__ == "__main__":
    main()
