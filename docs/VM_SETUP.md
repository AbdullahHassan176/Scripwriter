# VM Setup — Run Transcripts on a Fresh IP

Follow these steps on the Virtual Machine. The metadata is already fetched (saved in `data/`),
so you only need to install, add cookies, and run the transcript loop.

---

## 1. Install Python dependencies

```bat
pip install -e .
playwright install chromium
```

---

## 2. Export browser cookies from the VM

You need cookies from a YouTube-logged-in browser session on **this VM** (not your main PC).

**Option A — Chrome extension (easiest)**
1. Install: [Get cookies.txt LOCALLY](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
2. Go to `https://www.youtube.com` while logged in
3. Click the extension → Export → save as `cookies.txt` in the project root

**Option B — Edge extension**
Same extension exists for Edge. Export from `youtube.com`.

The file must be Netscape format (starts with `# Netscape HTTP Cookie File`).

---

## 3. Confirm `.env`

The `.env` file should contain:
```
YOUTUBE_API_KEY=your_youtube_api_key_here
YTCHAN_COOKIES_FILE=cookies.txt
```

`cookies.txt` should sit in the project root next to `.env`.

---

## 4. Run the transcript loop

Run from the project root:

```bat
bin\run_transcripts_loop.bat
```

- Fetches up to **25 transcripts per channel per round**
- **Waits 5 minutes** between rounds
- Skips videos already fetched
- Stops automatically when all channels are done

Override defaults:
```bat
bin\run_transcripts_loop.bat 50 10
```

---

## 5. (Optional) Re-fetch metadata from scratch

Only needed if you want to start completely fresh without the existing `data/` folder:

```bat
bin\run_channels.bat
```

This runs the YouTube API metadata step (~30 seconds, no transcript fetching).

---

## Output

Each channel gets a folder under `data/`:
```
data/
  Thomas Mulligan/
    videos_ranked.jsonl      ← all videos sorted by views (highest first)
    transcripts_index.csv    ← popularity_rank + has_transcript for every video
    transcripts/             ← individual transcript files
    dataset.jsonl            ← final output: one row per video with transcript
```
