"""Build dataset.jsonl: ranked video metadata + transcript text."""

import csv
import json
import logging
from pathlib import Path

from ytchan.config import get_settings
from ytchan.resolver import resolve_channel
from ytchan.utils.paths import (
    channel_dir,
    dataset_path,
    transcript_txt_path,
    transcripts_dir,
    transcripts_index_path,
    videos_ranked_jsonl_path,
    videos_raw_path,
)

logger = logging.getLogger(__name__)


def build_dataset(channel_input: str) -> Path:
    """Build dataset.jsonl in popularity order (rank 1 = most viewed)."""
    channel = resolve_channel(channel_input)
    settings = get_settings()
    chan_dir = channel_dir(settings.DATA_DIR, channel.channel_id, channel.title)
    t_dir = transcripts_dir(chan_dir)

    ranked_path = videos_ranked_jsonl_path(chan_dir)
    raw_path = videos_raw_path(chan_dir)

    if ranked_path.exists():
        videos: list[dict] = []
        with open(ranked_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    videos.append(json.loads(line))
    elif raw_path.exists():
        with open(raw_path, encoding="utf-8") as f:
            videos = json.load(f)
    else:
        raise FileNotFoundError("Run 'ytchan fetch-videos' and 'ytchan rank' first.")

    index_by_video: dict[str, dict] = {}
    index_path = transcripts_index_path(chan_dir)
    if index_path.exists():
        with open(index_path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                vid = row.get("video_id") or row.get("videoId", "")
                index_by_video[vid] = row

    out_path = dataset_path(chan_dir)
    rows: list[dict] = []

    for rank, v in enumerate(videos, start=1):
        video_id = v.get("videoId", "")
        idx = index_by_video.get(video_id, {})
        status = idx.get("transcript_status", "")
        lang = idx.get("transcript_language") or None
        has_transcript = status == "ok"

        transcript_text = ""
        if has_transcript:
            txt = transcript_txt_path(t_dir, video_id)
            if txt.exists():
                with open(txt, encoding="utf-8") as f:
                    transcript_text = f.read()

        rows.append({
            "popularity_rank": rank,
            "videoId": video_id,
            "title": v.get("title", ""),
            "publishedAt": v.get("publishedAt", ""),
            "views": v.get("viewCount", 0),
            "likes": v.get("likeCount", 0),
            "comments": v.get("commentCount", 0),
            "duration": v.get("duration", 0),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "has_transcript": has_transcript,
            "transcript_text": transcript_text,
            "transcript_language": lang if transcript_text else None,
        })

    with open(out_path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    logger.info("Built dataset with %d rows -> %s", len(rows), out_path)
    return out_path
