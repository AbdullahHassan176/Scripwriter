"""Video collector: fetch all uploads from a channel via uploads playlist."""

import json
import logging
from pathlib import Path

from rich.progress import Progress, SpinnerColumn, TextColumn

from ytchan.api_client import YouTubeApiClient
from ytchan.config import get_settings
from ytchan.models import video_from_api_item
from ytchan.resolver import resolve_channel
from ytchan.utils.paths import channel_dir, channel_info_path, readme_path, videos_raw_path

logger = logging.getLogger(__name__)


def fetch_channel_videos(channel_input: str) -> Path:
    """Fetch all videos from a channel and save to videos_metadata_raw.json."""
    channel = resolve_channel(channel_input)
    settings = get_settings()
    chan_dir = channel_dir(settings.DATA_DIR, channel.channel_id, channel.title)
    out_path = videos_raw_path(chan_dir)

    manifest_path = channel_info_path(chan_dir)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"channel_id": channel.channel_id, "channel_title": channel.title}, f, indent=2)

    readme_path(chan_dir).write_text(
        f"""ytchan - YouTube Channel Data: {channel.title}
Channel ID: {channel.channel_id}

FOLDER STRUCTURE
================
videos_metadata_raw.json  - Raw video metadata from YouTube API (all videos)
videos_ranked.csv         - Videos ranked by popularity (spreadsheet)
videos_ranked.jsonl       - Videos ranked by popularity (one JSON per line)
transcripts_index.csv     - Transcript fetch status per video
dataset.jsonl             - Combined metadata + transcript text for analysis
channel_info.json         - Channel ID and title (manifest)
transcripts/              - Per-video transcript files
  <videoId>.json          - Raw transcript segments (timestamps)
  <videoId>.txt           - Plain text transcript

NOTE ON TRANSCRIPTS (popularity order)
--------------------------------------
Transcripts are fetched in popularity order (rank 1 = most viewed). With a request
limit, the first N transcripts you get are the channel's top N videos by views.
- transcripts_index.csv has popularity_rank (1-based) and has_transcript (yes/no).
- dataset.jsonl is built in the same order: line 1 = top video; each row has
  popularity_rank and has_transcript so you can filter or slice easily.
Use `ytchan import-transcripts <folder>` to import tactiq-downloaded transcripts.
""",
        encoding="utf-8",
    )

    client = YouTubeApiClient()

    channels = client.channels_list(channel_id=channel.channel_id)
    if not channels:
        raise ValueError(f"Channel not found: {channel.channel_id}")

    uploads_id = (
        channels[0].get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
    )
    if not uploads_id:
        raise ValueError(f"No uploads playlist for channel {channel.channel_id}")

    video_ids: list[str] = []
    page_token: str | None = None

    with Progress(SpinnerColumn(), TextColumn("[bold blue]{task.description}")) as progress:
        task = progress.add_task("Fetching video IDs...")
        while True:
            resp = client.playlist_items_list(uploads_id, page_token=page_token)
            for item in resp.get("items", []):
                vid = item.get("contentDetails", {}).get("videoId")
                if vid:
                    video_ids.append(vid)
            page_token = resp.get("nextPageToken")
            progress.update(task, description=f"Fetching video IDs... {len(video_ids)} so far")
            if not page_token:
                break

    with Progress(SpinnerColumn(), TextColumn("[bold blue]{task.description}")) as progress:
        task = progress.add_task(f"Fetching video metadata... 0/{len(video_ids)}")
        videos: list[dict] = []
        for i in range(0, len(video_ids), 50):
            chunk = video_ids[i : i + 50]
            items = client.videos_list(chunk)
            for item in items:
                videos.append(video_from_api_item(item))
            progress.update(task, description=f"Fetching video metadata... {len(videos)}/{len(video_ids)}")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    logger.info("Saved %d videos for %s -> %s", len(videos), channel.title, out_path)
    return out_path
