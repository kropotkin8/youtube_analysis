"""Comandos Typer para ETL YouTube (uso en CLI y GitHub Actions)."""
import typer
from yt_data.commands.fetch_videos import register as register_videos
from yt_data.commands.fetch_channels import register as register_channels
from yt_data.commands.fetch_video_stats import register as register_video_stats
from yt_data.commands.fetch_comments import register as register_comments
from yt_data.commands.fetch_search import register as register_search


def register_all(parent: typer.Typer) -> None:
    register_videos(parent)
    register_channels(parent)
    register_video_stats(parent)
    register_comments(parent)
    register_search(parent)
