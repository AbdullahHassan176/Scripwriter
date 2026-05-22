#!/usr/bin/env python3
"""
Fetch YouTube metadata for all videos in a creator's transcript folder.

Usage:
    python bin/fetch_creator_stats.py 2and20
    python bin/fetch_creator_stats.py --all

Reads transcript filenames from scripts/<creator>/ to extract video IDs,
then fetches metadata via yt-dlp (no API key required).
Saves output to data/<creator>/videos_metadata.json
"""

import json
import re
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
DATA_DIR = Path(__file__).parent.parent / "data"
VIDEO_ID_RE = re.compile(r"tactiq-free-transcript-([A-Za-z0-9_\-]+)\.txt$")


def extract_video_ids(creator: str) -> list[str]:
    folder = SCRIPTS_DIR / creator
    if not folder.exists():
        raise FileNotFoundError(f"No transcript folder found: {folder}")
    ids = []
    for f in sorted(folder.iterdir()):
        m = VIDEO_ID_RE.match(f.name)
        if m:
            ids.append(m.group(1))
    return ids


def fetch_video_metadata(video_id: str) -> dict | None:
    url = f"https://www.youtube.com/watch?v={video_id}"
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--dump-json",
        "--no-playlist",
        "--quiet",
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"  [WARN] yt-dlp failed for {video_id}: {result.stderr.strip()[:120]}")
            return None
        raw = json.loads(result.stdout)
        return {
            "video_id": video_id,
            "url": url,
            "title": raw.get("title"),
            "duration_seconds": raw.get("duration"),
            "upload_date": raw.get("upload_date"),
            "view_count": raw.get("view_count"),
            "like_count": raw.get("like_count"),
            "comment_count": raw.get("comment_count"),
            "description": raw.get("description", "")[:800],
            "tags": raw.get("tags", [])[:20],
            "categories": raw.get("categories", []),
            "channel": raw.get("channel"),
            "channel_id": raw.get("channel_id"),
            "channel_url": raw.get("channel_url"),
            "subscriber_count": raw.get("channel_follower_count"),
            "age_limit": raw.get("age_limit"),
            "availability": raw.get("availability"),
        }
    except subprocess.TimeoutExpired:
        print(f"  [WARN] Timeout fetching {video_id}")
        return None
    except json.JSONDecodeError as e:
        print(f"  [WARN] JSON parse error for {video_id}: {e}")
        return None


def run_creator(creator: str, delay: float = 2.0) -> Path:
    print(f"\n=== Fetching stats for: {creator} ===")
    video_ids = extract_video_ids(creator)
    print(f"  Found {len(video_ids)} video IDs")

    out_dir = DATA_DIR / creator
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "videos_metadata.json"

    existing: dict[str, dict] = {}
    if out_file.exists():
        try:
            existing = {v["video_id"]: v for v in json.loads(out_file.read_text(encoding="utf-8"))}
            print(f"  Already have {len(existing)} cached entries")
        except Exception:
            pass

    results = list(existing.values())
    fetched_ids = set(existing.keys())

    for i, vid_id in enumerate(video_ids):
        if vid_id in fetched_ids:
            print(f"  [{i+1}/{len(video_ids)}] {vid_id} — cached, skipping")
            continue
        print(f"  [{i+1}/{len(video_ids)}] {vid_id} — fetching…", end=" ", flush=True)
        meta = fetch_video_metadata(vid_id)
        if meta:
            results.append(meta)
            safe_title = (meta.get('title') or '')[:60].encode('ascii', errors='replace').decode('ascii')
            print(f"OK  {safe_title}")
        else:
            print("FAIL")
        if i < len(video_ids) - 1:
            time.sleep(delay)

    out_file.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  Saved {len(results)} records -> {out_file}")
    return out_file


def main():
    args = sys.argv[1:]
    all_creators = [d.name for d in SCRIPTS_DIR.iterdir() if d.is_dir()]

    if not args or args[0] == "--help":
        print(__doc__)
        print(f"Available creators: {', '.join(sorted(all_creators))}")
        sys.exit(0)

    if args[0] == "--all":
        targets = sorted(all_creators)
    else:
        targets = args

    for creator in targets:
        run_creator(creator)

    print("\nDone.")


if __name__ == "__main__":
    main()
