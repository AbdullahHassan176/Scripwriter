"""ytchan CLI – YouTube channel analytics tool."""

import logging
import time
from datetime import datetime
from pathlib import Path

import typer
from rich.console import Console

from ytchan import __version__
from ytchan.collector import fetch_channel_videos
from ytchan.config import get_settings
from ytchan.dataset import build_dataset
from ytchan.ranker import rank_videos
from ytchan.resolver import resolve_channel
from ytchan.transcript_fetcher import fetch_transcripts, import_tactiq_transcripts
from ytchan.utils.paths import channel_dir

app = typer.Typer(
    name="ytchan",
    help="YouTube channel analytics: fetch videos, rank by popularity, fetch transcripts, export to JSONL/CSV",
)
console = Console()


def _setup_logging(verbose: bool) -> None:
    try:
        settings = get_settings()
        log_dir = settings.LOGS_DIR
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s %(levelname)s %(name)s %(message)s",
            handlers=[logging.FileHandler(log_file, encoding="utf-8")],
        )
    except Exception:
        logging.basicConfig(level=logging.WARNING)


@app.callback()
def main(verbose: bool = typer.Option(False, "--verbose", "-v")) -> None:
    """ytchan – YouTube channel analytics CLI."""
    _setup_logging(verbose)


@app.command()
def version() -> None:
    """Print version."""
    console.print(f"ytchan {__version__}")


@app.command()
def resolve(
    channel_input: str = typer.Argument(..., help="Channel URL, @handle, or channel ID"),
) -> None:
    """Resolve a channel input to its ID and title."""
    try:
        ch = resolve_channel(channel_input)
        console.print(f"[bold]Channel:[/bold] {ch.title}")
        console.print(f"[bold]Channel ID:[/bold] {ch.channel_id}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command(name="fetch-videos")
def fetch_videos(
    channel_input: str = typer.Argument(..., help="Channel URL, @handle, or channel ID"),
) -> None:
    """Fetch all video metadata for a channel."""
    try:
        path = fetch_channel_videos(channel_input)
        console.print(f"[green]Saved[/green] {path}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def rank(
    channel_input: str = typer.Argument(..., help="Channel URL, @handle, or channel ID"),
    metric: str = typer.Option("views", "--metric", "-m", help="views | likes | comments | engagement"),
) -> None:
    """Rank videos by popularity and write videos_ranked.csv / .jsonl."""
    valid = ("views", "likes", "comments", "engagement")
    if metric not in valid:
        console.print(f"[red]Invalid metric. Choose from: {', '.join(valid)}[/red]")
        raise typer.Exit(1)
    try:
        csv_path, jsonl_path = rank_videos(channel_input, metric=metric)  # type: ignore[arg-type]
        console.print(f"[green]Ranked by {metric}[/green]  CSV: {csv_path.name}  JSONL: {jsonl_path.name}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command(name="fetch-transcripts")
def fetch_transcripts_cmd(
    channel_input: str = typer.Argument(..., help="Channel URL, @handle, or channel ID"),
    max_videos: int | None = typer.Option(None, "--max", "-n", help="Max videos to process this run"),
    since: str | None = typer.Option(None, "--since", "-s", help="Only videos on/after YYYY-MM-DD"),
    language: str = typer.Option("en", "--language", "-l", help="Preferred transcript language"),
    force: bool = typer.Option(False, "--force", "-f", help="Re-fetch already downloaded transcripts"),
    delay: float = typer.Option(3.0, "--delay", "-d", help="Seconds between requests (default 3)"),
) -> None:
    """Fetch transcripts via yt-dlp (in popularity order, skips already-fetched)."""
    try:
        path, n_new = fetch_transcripts(
            channel_input, max_videos=max_videos, since=since,
            language=language, force=force, delay=delay,
        )
        console.print(f"[green]Index[/green] {path}  ({n_new} newly fetched)")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command(name="import-transcripts")
def import_transcripts_cmd(
    folder: Path = typer.Argument(..., help="Folder containing tactiq .txt transcript files"),
    channel_input: str = typer.Argument(..., help="Channel URL, @handle, or channel ID"),
) -> None:
    """Import manually-downloaded tactiq.io transcripts into a channel's data folder.

    Tactiq files are named like: tactiq-free-transcript-<videoId>.txt
    They contain timestamped lines in the format:  00:00:00.000 text...
    """
    if not folder.exists():
        console.print(f"[red]Folder not found:[/red] {folder}")
        raise typer.Exit(1)
    try:
        n = import_tactiq_transcripts(folder, channel_input)
        console.print(f"[green]Imported {n} transcript(s)[/green] from {folder}")
        if n:
            console.print("Run [bold]ytchan build-dataset[/bold] to update dataset.jsonl")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command(name="build-dataset")
def build_dataset_cmd(
    channel_input: str = typer.Argument(..., help="Channel URL, @handle, or channel ID"),
) -> None:
    """Build dataset.jsonl (popularity order, with has_transcript flag)."""
    try:
        path = build_dataset(channel_input)
        console.print(f"[green]Dataset[/green] {path}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command(name="fetch-transcripts-loop")
def fetch_transcripts_loop_cmd(
    channels: list[str] = typer.Argument(..., help="One or more channel URLs / @handles"),
    max_per_round: int = typer.Option(25, "--max-per-round", "-n", help="Max new fetches per channel per round"),
    wait_minutes: float = typer.Option(5.0, "--wait-minutes", "-w", help="Minutes to wait between rounds"),
    max_rounds: int = typer.Option(0, "--max-rounds", "-r", help="Max rounds (0 = until done)"),
    delay: float = typer.Option(3.0, "--delay", "-d", help="Seconds between requests within a round"),
) -> None:
    """Auto-loop: fetch up to N transcripts per channel, wait, retry. Stops when no new transcripts.

    Example:
        ytchan fetch-transcripts-loop @Channel1 @Channel2 --max-per-round 25 --wait-minutes 5
    """
    if not channels:
        console.print("[red]Provide at least one channel.[/red]")
        raise typer.Exit(1)
    try:
        round_num = 0
        while True:
            round_num += 1
            console.print(f"\n[bold cyan]── Round {round_num} ──────────────────────────[/bold cyan]")
            total_new = 0
            for ch in channels:
                try:
                    _, n_new = fetch_transcripts(ch, max_videos=max_per_round, delay=delay)
                    build_dataset(ch)
                    console.print(f"  [green]{ch}[/green]: {n_new} new")
                    total_new += n_new
                except Exception as e:
                    console.print(f"  [red]{ch}:[/red] {e}")

            if total_new == 0:
                console.print("\n[green]No new transcripts this round — all done![/green]")
                break
            if max_rounds and round_num >= max_rounds:
                console.print(f"\n[yellow]Reached max rounds ({max_rounds}).[/yellow]")
                break

            wait_sec = max(0, wait_minutes * 60)
            console.print(f"\nWaiting {wait_minutes:.1f} min before next round… (Ctrl+C to stop)")
            time.sleep(wait_sec)
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopped.[/yellow]")


@app.command(name="all")
def all_cmd(
    channel_input: str = typer.Argument(..., help="Channel URL, @handle, or channel ID"),
    metric: str = typer.Option("views", "--metric", "-m", help="Ranking metric"),
    skip_transcripts: bool = typer.Option(False, "--skip-transcripts", help="Only fetch metadata and rank"),
) -> None:
    """Run full pipeline: fetch-videos → rank → fetch-transcripts → build-dataset."""
    try:
        ch = resolve_channel(channel_input)
        console.print(f"[bold]Channel:[/bold] {ch.title} ({ch.channel_id})")

        console.print("\n[bold]1. Fetching videos…[/bold]")
        fetch_channel_videos(channel_input)

        console.print(f"\n[bold]2. Ranking by[/bold] {metric}")
        rank_videos(channel_input, metric=metric)  # type: ignore[arg-type]

        if not skip_transcripts:
            console.print("\n[bold]3. Fetching transcripts…[/bold]")
            fetch_transcripts(channel_input, delay=3.0)

            console.print("\n[bold]4. Building dataset…[/bold]")
        else:
            console.print("\n[bold]3. Building dataset (no transcripts)…[/bold]")

        build_dataset(channel_input)

        settings = get_settings()
        chan_dir = channel_dir(settings.DATA_DIR, ch.channel_id, ch.title)
        console.print(f"\n[green]Done![/green] Output in {chan_dir}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command(name="fetch-metadata")
def fetch_metadata_cmd(
    channel_input: str = typer.Argument(..., help="Channel URL, @handle, or channel ID"),
    metric: str = typer.Option("views", "--metric", "-m", help="Ranking metric"),
) -> None:
    """Fetch videos and rank only (no transcripts). Fast — uses YouTube API only."""
    try:
        ch = resolve_channel(channel_input)
        console.print(f"[bold]Channel:[/bold] {ch.title}")
        fetch_channel_videos(channel_input)
        rank_videos(channel_input, metric=metric)  # type: ignore[arg-type]
        build_dataset(channel_input)
        settings = get_settings()
        chan_dir = channel_dir(settings.DATA_DIR, ch.channel_id, ch.title)
        console.print(f"[green]Done![/green] {chan_dir}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
