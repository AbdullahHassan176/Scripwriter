"""Popularity ranking: sort videos by views, likes, comments, or engagement."""

import csv
import json
import logging
from pathlib import Path
from typing import Literal

from ytchan.config import get_settings
from ytchan.resolver import resolve_channel
from ytchan.utils.paths import channel_dir, videos_raw_path, videos_ranked_csv_path, videos_ranked_jsonl_path

logger = logging.getLogger(__name__)

RankMetric = Literal["views", "likes", "comments", "engagement"]


def _engagement_rate(v: dict) -> float:
    views = v.get("viewCount") or 0
    likes = v.get("likeCount") or 0
    if views and likes:
        return likes / views
    return 0.0


def _sort_key(metric: RankMetric):
    def key(v: dict):
        if metric == "views":
            return -(v.get("viewCount") or 0)
        if metric == "likes":
            return -(v.get("likeCount") or 0)
        if metric == "comments":
            return -(v.get("commentCount") or 0)
        if metric == "engagement":
            return -_engagement_rate(v)
        return 0
    return key


def rank_videos(channel_input: str, metric: RankMetric = "views") -> tuple[Path, Path]:
    """Rank videos and write videos_ranked.csv and videos_ranked.jsonl. Returns (csv, jsonl)."""
    channel = resolve_channel(channel_input)
    settings = get_settings()
    chan_dir = channel_dir(settings.DATA_DIR, channel.channel_id, channel.title)
    raw_path = videos_raw_path(chan_dir)

    if not raw_path.exists():
        raise FileNotFoundError(f"Run 'ytchan fetch-videos {channel_input}' first.")

    with open(raw_path, encoding="utf-8") as f:
        videos = json.load(f)

    sorted_videos = sorted(videos, key=_sort_key(metric))

    csv_path = videos_ranked_csv_path(chan_dir)
    jsonl_path = videos_ranked_jsonl_path(chan_dir)

    internal_fields = ["videoId", "title", "publishedAt", "duration", "viewCount", "likeCount", "commentCount", "tags", "description", "thumbnailUrl"]
    csv_headers = ["video_id", "title", "published_at", "duration_seconds", "view_count", "like_count", "comment_count", "tags", "description", "thumbnail_url"]
    field_to_header = dict(zip(internal_fields, csv_headers))

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers, extrasaction="ignore")
        writer.writeheader()
        for v in sorted_videos:
            row = {field_to_header[k]: v.get(k) for k in internal_fields}
            tags = v.get("tags")
            row["tags"] = "|".join(tags) if isinstance(tags, list) else str(tags or "")
            writer.writerow(row)

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for v in sorted_videos:
            f.write(json.dumps(v, ensure_ascii=False) + "\n")

    logger.info("Ranked %d videos by %s -> %s", len(sorted_videos), metric, jsonl_path)
    return csv_path, jsonl_path
