# Scriptwriter

A workspace for writing short-form video scripts modeled on target creators' styles. Source material lives in `DropBox/`, finished scripts in `scripts/`, and creator style-reference transcripts in their named folders (`h1t1/`, `DougSharpe/`, etc.). See `ai.md` for the full workflow.

---

## ytchan — YouTube Transcript Tool

`ytchan` is the bundled CLI for fetching video metadata and transcripts from YouTube channels. It outputs ranked datasets to `data/<channel>/` which feed the script research process.

YouTube channel analytics CLI: fetch video metadata, rank by popularity, fetch transcripts (via **yt-dlp**), export to JSONL/CSV.

## Setup

Requires **Python 3.11+**.

```bash
pip install -e .
```

### YouTube Data API key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **YouTube Data API v3**
3. Create an API key under APIs & Services → Credentials

Copy `.env.example` to `.env` and fill in your key:

```
YOUTUBE_API_KEY=your_key_here
```

Optional settings in `.env`:
```
YTCHAN_COOKIES_FILE=cookies.txt     # Netscape cookies file — best for bypassing 429s (see below)
YTCHAN_COOKIES_BROWSER=chrome       # Auto-extract from browser (may fail if browser is open)
YTCHAN_PROXY=http://...             # HTTP proxy
```

### Bypassing YouTube rate limits (HTTP 429)

YouTube blocks IPs that make too many requests. The most reliable fix is a **cookies.txt** file:

1. Install the **[Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)** Chrome extension
2. Go to **youtube.com** while signed in
3. Click the extension → **Export** → save as `cookies.txt` in the project root
4. Add to `.env`: `YTCHAN_COOKIES_FILE=cookies.txt`

yt-dlp will then send your authenticated cookies with every subtitle request, bypassing rate limits. Alternatively, wait 30–60 minutes for a temporary block to clear.

---

## Commands

| Command | Description |
|---------|-------------|
| `ytchan fetch-metadata <channel>` | Fetch videos + rank (fast, API only — no transcripts) |
| `ytchan fetch-videos <channel>` | Fetch raw video metadata |
| `ytchan rank <channel> [--metric views]` | Rank videos by popularity |
| `ytchan fetch-transcripts <channel>` | Fetch transcripts via yt-dlp (`--max`, `--delay`, `--force`) |
| `ytchan fetch-transcripts-loop <ch> ...` | Auto-loop: fetch N/channel/round, wait, retry until done |
| `ytchan import-transcripts <folder> <channel>` | Import tactiq.io .txt transcripts from a local folder |
| `ytchan build-dataset <channel>` | Build `dataset.jsonl` (popularity order, with `has_transcript`) |
| `ytchan all <channel>` | Full pipeline (add `--skip-transcripts` for metadata only) |

---

## Recommended workflow

### Step 1 — Fetch metadata for all channels (fast)

```bat
bin\run_channels.bat
```

This uses the YouTube Data API only. No transcript fetching, no blocking. Takes ~1–2 min for all 7 channels.

### Step 2 — Import any tactiq.io transcripts you already have

If you've manually downloaded transcripts from [tactiq.io](https://tactiq.io/tools/youtube-transcript), drop the `.txt` files in a folder and import them:

```bat
python -m ytchan import-transcripts h1t1\ "@H1T1"
python -m ytchan import-transcripts thomasmulligan\ "@thomasmulligan"
```

Then rebuild datasets:

```bat
python -m ytchan build-dataset "@H1T1"
python -m ytchan build-dataset "@thomasmulligan"
```

### Step 3 — Auto-fetch remaining transcripts via yt-dlp

```bat
bin\run_transcripts_loop.bat          # 25/channel/round, 5 min wait
bin\run_transcripts_loop.bat 50 10    # 50/channel/round, 10 min wait
```

The loop runs rounds automatically: fetches up to N per channel, waits, retries. Already-fetched transcripts are skipped. Stops when no new transcripts are found. Press **Ctrl+C** to pause.

> **yt-dlp vs youtube-transcript-api**: yt-dlp is far more robust — it's the same engine used by tools like tactiq.io. It respects your proxy setting (`YTCHAN_PROXY`) and has much lower block rates.

---

## Output structure

```
data/<channel_name>/
├── README.txt                   # Folder docs
├── channel_info.json            # Channel ID + title
├── videos_metadata_raw.json     # All videos from API
├── videos_ranked.csv            # Ranked by popularity (spreadsheet)
├── videos_ranked.jsonl          # Ranked by popularity (one JSON per line)
├── transcripts_index.csv        # Status per video: popularity_rank, has_transcript
├── dataset.jsonl                # Metadata + transcript text (line 1 = top video)
└── transcripts/
    ├── <videoId>.json           # Segment data (timestamps)
    └── <videoId>.txt            # Plain text
```

`dataset.jsonl` fields: `popularity_rank`, `videoId`, `title`, `publishedAt`, `views`, `likes`, `comments`, `duration`, `url`, `has_transcript`, `transcript_text`, `transcript_language`.

With a request limit, the first N lines of `dataset.jsonl` are always the top N videos by views.

---

## API quotas

YouTube Data API v3 default quota: 10,000 units/day.

- `channels.list`: 1 unit
- `playlistItems.list`: 1 unit per 50 items
- `videos.list`: 1 unit per 50 videos

A 500-video channel costs ~15 units. Transcripts use yt-dlp (no quota).

---

## Tests

```bash
YOUTUBE_API_KEY=test-key python -m pytest tests/ -v
```
