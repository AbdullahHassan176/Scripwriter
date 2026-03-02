"""Path utilities for data/<channel_name>/ structure."""

import re
from pathlib import Path


def _slugify_channel_name(title: str) -> str:
    if not title or not title.strip():
        return "unknown_channel"
    s = re.sub(r'[<>:"/\\|?*]', " ", title)
    s = re.sub(r"\s+", " ", s).strip()
    return s or "unknown_channel"


def channel_dir(data_dir: Path, channel_id: str, channel_title: str) -> Path:
    path = data_dir / _slugify_channel_name(channel_title)
    path.mkdir(parents=True, exist_ok=True)
    return path


def transcripts_dir(channel_dir_path: Path) -> Path:
    path = channel_dir_path / "transcripts"
    path.mkdir(parents=True, exist_ok=True)
    return path


def videos_raw_path(channel_dir_path: Path) -> Path:
    return channel_dir_path / "videos_metadata_raw.json"


def videos_ranked_csv_path(channel_dir_path: Path) -> Path:
    return channel_dir_path / "videos_ranked.csv"


def videos_ranked_jsonl_path(channel_dir_path: Path) -> Path:
    return channel_dir_path / "videos_ranked.jsonl"


def transcripts_index_path(channel_dir_path: Path) -> Path:
    return channel_dir_path / "transcripts_index.csv"


def transcript_json_path(transcripts_dir_path: Path, video_id: str) -> Path:
    return transcripts_dir_path / f"{video_id}.json"


def transcript_txt_path(transcripts_dir_path: Path, video_id: str) -> Path:
    return transcripts_dir_path / f"{video_id}.txt"


def dataset_path(channel_dir_path: Path) -> Path:
    return channel_dir_path / "dataset.jsonl"


def channel_info_path(channel_dir_path: Path) -> Path:
    return channel_dir_path / "channel_info.json"


def readme_path(channel_dir_path: Path) -> Path:
    return channel_dir_path / "README.txt"
