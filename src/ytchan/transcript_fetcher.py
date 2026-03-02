"""Transcript fetcher — two Playwright strategies:
  1. Fast path: extract captionTrack URL from ytInitialPlayerResponse and fetch json3.
  2. UI path:   click "Show transcript" in YouTube's actual UI, scrape DOM segments.
     This never calls /api/timedtext at all — YouTube can't block it without breaking
     their own site. Used automatically when the fast path returns HTTP 429.
"""

import csv
import http.cookiejar
import json
import logging
import random
import re
import time
from pathlib import Path

from rich.progress import BarColumn, Progress, SpinnerColumn, TaskProgressColumn, TextColumn

from ytchan.config import get_settings
from ytchan.resolver import resolve_channel
from ytchan.utils.paths import (
    channel_dir,
    transcript_json_path,
    transcript_txt_path,
    transcripts_dir,
    transcripts_index_path,
    videos_ranked_jsonl_path,
    videos_raw_path,
)

logger = logging.getLogger(__name__)


def _sleep(base: float, jitter: float = 2.0) -> None:
    time.sleep(max(0, base + random.uniform(0, jitter)))


def _parse_json3(data: dict) -> list[dict]:
    """Parse yt-dlp / YouTube json3 subtitle format into segment dicts."""
    segments = []
    for event in data.get("events", []):
        segs = event.get("segs")
        if not segs:
            continue
        text = "".join(s.get("utf8", "") for s in segs).strip()
        if not text or text == "\n":
            continue
        start_ms = event.get("tStartMs", 0)
        dur_ms = event.get("dDurationMs", 0)
        segments.append({"text": text, "start": start_ms / 1000, "duration": dur_ms / 1000})
    return segments


def _netscape_cookies_to_playwright(cookies_file: str) -> list[dict]:
    """Convert a Netscape cookies.txt file to Playwright's cookie format."""
    cookies = []
    try:
        for line in Path(cookies_file).read_text(encoding="utf-8").splitlines():
            if not line or line.startswith("#"):
                continue
            parts = line.strip().split("\t")
            if len(parts) < 7:
                continue
            domain, _, path, secure_str, expiry_str, name, value = parts[:7]
            try:
                expiry = int(expiry_str)
            except ValueError:
                expiry = -1
            cookies.append({
                "name": name,
                "value": value,
                "domain": domain,
                "path": path,
                "expires": expiry,
                "httpOnly": False,
                "secure": secure_str.upper() == "TRUE",
                "sameSite": "None",
            })
    except Exception as e:
        logger.warning("Failed to load cookies from %s: %s", cookies_file, e)
    return cookies


def _make_browser_ctx(pw, cookies_file: str | None):
    """Create a Playwright browser context with optional cookies."""
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        locale="en-US",
        viewport={"width": 1280, "height": 800},
    )
    if cookies_file and Path(cookies_file).exists():
        pw_cookies = _netscape_cookies_to_playwright(cookies_file)
        if pw_cookies:
            ctx.add_cookies(pw_cookies)
    return browser, ctx


def _fetch_timedtext(video_id: str, langs: list[str], cookies_file: str | None) -> tuple[list[dict] | None, str, str]:
    """Fast path: extract captionTrack URL from ytInitialPlayerResponse, fetch json3.
    Returns (segments, lang, error). Status 'blocked' means HTTP 429 — caller should retry via UI."""
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        return None, "error", "playwright not installed"

    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        with sync_playwright() as pw:
            browser, ctx = _make_browser_ctx(pw, cookies_file)
            page = ctx.new_page()
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_function("() => !!window.ytInitialPlayerResponse", timeout=15_000)
            except PWTimeout:
                browser.close()
                return None, "error", "Timeout loading video page"

            tracks = page.evaluate("""() => {
                const tl = window.ytInitialPlayerResponse
                    ?.captions?.playerCaptionsTracklistRenderer?.captionTracks;
                return tl ? tl.map(t => ({
                    languageCode: t.languageCode,
                    name: t.name?.simpleText || '',
                    baseUrl: t.baseUrl,
                    kind: t.kind || ''
                })) : null;
            }""")

            if not tracks:
                browser.close()
                return None, "unavailable", "No caption tracks in player response"

            def _score(t: dict) -> tuple[int, int]:
                lang = t.get("languageCode", "")
                lang_rank = next((i for i, l in enumerate(langs) if lang.startswith(l[:2])), 99)
                return (lang_rank, 0 if t.get("kind", "") != "asr" else 1)

            tracks.sort(key=_score)
            best = tracks[0]
            sub_url = best["baseUrl"] + "&fmt=json3"
            response = page.request.get(sub_url)
            browser.close()

            if response.status == 429:
                return None, "blocked", "timedtext 429"
            if not response.ok:
                return None, "error", f"HTTP {response.status}"

            segments = _parse_json3(response.json())
            if not segments:
                return None, "empty", "No segments after parsing"
            return segments, best["languageCode"], ""

    except Exception as e:
        return None, "error", str(e)[:200]


def _fetch_ui_click(video_id: str, cookies_file: str | None) -> tuple[list[dict] | None, str, str]:
    """UI path: open the video page, click 'Show transcript', scrape the DOM.

    Never calls /api/timedtext — uses YouTube's own UI transcript panel.
    Immune to timedtext rate-limiting; works on any IP that can load youtube.com.
    """
    try:
        from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
    except ImportError:
        return None, "error", "playwright not installed"

    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        with sync_playwright() as pw:
            browser, ctx = _make_browser_ctx(pw, cookies_file)
            page = ctx.new_page()

            try:
                page.goto(url, wait_until="domcontentloaded", timeout=30_000)
                page.wait_for_selector("ytd-watch-flexy", timeout=20_000)
            except PWTimeout:
                browser.close()
                return None, "error", "Timeout loading video page (UI)"

            # Dismiss cookie/consent banner if present
            try:
                page.click('button:has-text("Accept all")', timeout=3_000)
            except Exception:
                pass

            # Give the page JS a moment to settle
            time.sleep(1.5)

            # ── Try to open the transcript panel ──────────────────────────────
            # YouTube renders a direct "Show transcript" button with aria-label (no visible text).
            # If the panel is already open, "Close transcript" appears instead — skip clicking.
            opened = False

            # Check if already open
            already_open = page.locator('button[aria-label="Close transcript"]').count() > 0
            if already_open:
                opened = True

            if not opened:
                # Strategy 1: direct aria-label button (modern YouTube UI)
                for sel in [
                    'button[aria-label="Show transcript"]',
                    'button[aria-label="Transcript"]',
                    'button:has-text("Show transcript")',
                ]:
                    try:
                        btn = page.locator(sel).first
                        btn.scroll_into_view_if_needed(timeout=3_000)
                        btn.click(timeout=5_000)
                        opened = True
                        break
                    except Exception:
                        pass

            # Strategy 2: click the "More actions" menu (older/different UI)
            if not opened:
                for more_sel in [
                    'button[aria-label="More actions"]',
                    'ytd-menu-renderer yt-icon-button',
                ]:
                    try:
                        page.locator(more_sel).first.click(timeout=3_000)
                        time.sleep(0.5)
                        for item_sel in [
                            'ytd-menu-service-item-renderer:has-text("Show transcript")',
                            'tp-yt-paper-item:has-text("Show transcript")',
                        ]:
                            try:
                                page.locator(item_sel).click(timeout=3_000)
                                opened = True
                                break
                            except Exception:
                                pass
                        if opened:
                            break
                        page.keyboard.press("Escape")
                        time.sleep(0.3)
                    except Exception:
                        pass

            if not opened:
                browser.close()
                return None, "unavailable", "Could not open transcript panel (no captions or UI changed)"

            # ── Wait for transcript segments to appear ────────────────────────
            try:
                page.wait_for_selector("ytd-transcript-segment-renderer", timeout=15_000)
            except PWTimeout:
                browser.close()
                return None, "unavailable", "Transcript panel opened but no segments appeared"

            # ── Scrape segments ───────────────────────────────────────────────
            segments = page.evaluate("""() => {
                const nodes = document.querySelectorAll('ytd-transcript-segment-renderer');
                return Array.from(nodes).map(n => {
                    const ts   = n.querySelector('.segment-timestamp')?.textContent?.trim() || '0:00';
                    const text = n.querySelector('.segment-text')?.textContent?.trim()      || '';
                    const parts = ts.split(':').map(Number);
                    let secs = 0;
                    if (parts.length === 3) secs = parts[0]*3600 + parts[1]*60 + parts[2];
                    else if (parts.length === 2) secs = parts[0]*60 + parts[1];
                    return { text, start: secs, duration: 0 };
                }).filter(s => s.text);
            }""")
            browser.close()

            if not segments:
                return None, "empty", "No segments found in transcript panel"
            return segments, "en", ""

    except Exception as e:
        return None, "error", str(e)[:200]


def _fetch_via_playwright(video_id: str, langs: list[str], cookies_file: str | None) -> tuple[list[dict] | None, str, str]:
    """Dispatcher: try fast timedtext path first, fall back to UI-click on 429."""
    segments, status, error = _fetch_timedtext(video_id, langs, cookies_file)
    if segments is not None or status not in ("blocked", "error"):
        return segments, status, error
    # timedtext is blocked or failed — use the UI click approach
    logger.debug("Timedtext blocked for %s (%s), falling back to UI click", video_id, error)
    return _fetch_ui_click(video_id, cookies_file)


def _import_tactiq_file(txt_path: Path) -> tuple[list[dict] | None, str, str]:
    """Parse a tactiq.io transcript .txt file into segments."""
    try:
        lines = txt_path.read_text(encoding="utf-8").splitlines()
    except Exception as e:
        return None, "error", str(e)

    ts_re = re.compile(r"^(\d{2}:\d{2}:\d{2}[.,]\d+)\s+(.+)$")
    segments = []
    for line in lines:
        m = ts_re.match(line.strip())
        if not m:
            continue
        ts_str, text = m.group(1), m.group(2).strip()
        parts = re.split(r"[:.,]", ts_str)
        try:
            h, mi, s, ms = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]) if len(parts) > 3 else 0
            start = h * 3600 + mi * 60 + s + ms / 1000
        except (IndexError, ValueError):
            start = 0.0
        segments.append({"text": text, "start": start, "duration": 0.0})

    if not segments:
        return None, "empty", "No timestamped lines found in tactiq file"
    return segments, "en", ""


def fetch_transcripts(
    channel_input: str,
    *,
    max_videos: int | None = None,
    since: str | None = None,
    language: str = "en",
    force: bool = False,
    delay: float = 2.0,
) -> tuple[Path, int]:
    """Fetch transcripts via Playwright (headless browser). Returns (index_path, n_newly_fetched)."""
    from datetime import datetime

    channel = resolve_channel(channel_input)
    settings = get_settings()
    chan_dir = channel_dir(settings.DATA_DIR, channel.channel_id, channel.title)
    t_dir = transcripts_dir(chan_dir)

    ranked_path = videos_ranked_jsonl_path(chan_dir)
    raw_path = videos_raw_path(chan_dir)

    videos: list[dict] = []
    if ranked_path.exists():
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

    if since:
        try:
            since_dt = datetime.strptime(since, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("--since must be YYYY-MM-DD")
        filtered = []
        for v in videos:
            pub = v.get("publishedAt", "")[:10]
            try:
                if datetime.strptime(pub, "%Y-%m-%d").date() >= since_dt:
                    filtered.append(v)
            except ValueError:
                filtered.append(v)
        videos = filtered

    if max_videos:
        videos = videos[:max_videos]

    langs = [language] if language else ["en"]

    cookies_file = None
    try:
        cf = settings.YTCHAN_COOKIES_FILE
        cookies_file = str(cf).strip() if cf else None
    except Exception:
        pass

    index_rows: list[dict] = []
    n_newly_fetched = 0

    with Progress(SpinnerColumn(), TextColumn("[bold blue]{task.description}"), BarColumn(), TaskProgressColumn()) as progress:
        task = progress.add_task("Fetching transcripts...", total=len(videos))

        for rank, v in enumerate(videos, start=1):
            video_id = v.get("videoId", "")
            title = v.get("title", "")
            views = v.get("viewCount", 0)

            json_path = transcript_json_path(t_dir, video_id)
            txt_path = transcript_txt_path(t_dir, video_id)

            if json_path.exists() and not force:
                with open(json_path, encoding="utf-8") as f:
                    segs = json.load(f)
                text = " ".join(s.get("text", "") for s in segs)
                index_rows.append(_row(rank, video_id, title, views, "ok", "", "en", text))
                progress.advance(task)
                continue

            segments, status, error = _fetch_via_playwright(video_id, langs, cookies_file)

            if segments is not None:
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(segments, f, ensure_ascii=False)
                text = " ".join(s.get("text", "") for s in segments)
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
                n_newly_fetched += 1
                index_rows.append(_row(rank, video_id, title, views, "ok", "", status, text))
            else:
                index_rows.append(_row(rank, video_id, title, views, status, error, "", ""))

            progress.advance(task)
            _sleep(delay)

    _write_index(transcripts_index_path(chan_dir), index_rows)
    return transcripts_index_path(chan_dir), n_newly_fetched


def import_tactiq_transcripts(folder: Path, channel_input: str) -> int:
    """Import tactiq.io .txt transcript files from a folder into the channel data."""
    channel = resolve_channel(channel_input)
    settings = get_settings()
    chan_dir = channel_dir(settings.DATA_DIR, channel.channel_id, channel.title)
    t_dir = transcripts_dir(chan_dir)

    video_id_re = re.compile(r"youtube\.com/watch[/?]([A-Za-z0-9_-]{11})")
    n_imported = 0

    for txt_file in sorted(folder.glob("*.txt")):
        content = txt_file.read_text(encoding="utf-8", errors="replace")
        m = video_id_re.search(content)
        if not m:
            fm = re.search(r"-([A-Za-z0-9_-]{11})\.txt$", txt_file.name)
            if not fm:
                logger.warning("Cannot determine video ID from %s, skipping", txt_file.name)
                continue
            video_id = fm.group(1)
        else:
            video_id = m.group(1)

        json_path = transcript_json_path(t_dir, video_id)
        txt_dest = transcript_txt_path(t_dir, video_id)

        segments, status, error = _import_tactiq_file(txt_file)
        if segments is None:
            logger.warning("Failed to parse %s: %s", txt_file.name, error)
            continue

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(segments, f, ensure_ascii=False)
        text = " ".join(s.get("text", "") for s in segments)
        with open(txt_dest, "w", encoding="utf-8") as f:
            f.write(text)

        logger.info("Imported %s -> %s", txt_file.name, video_id)
        n_imported += 1

    return n_imported


def _row(rank, video_id, title, views, status, error, lang, text) -> dict:
    return {
        "popularity_rank": rank,
        "video_id": video_id,
        "title": title,
        "view_count": views,
        "has_transcript": "yes" if status == "ok" else "no",
        "transcript_status": status,
        "transcript_error_detail": error,
        "transcript_language": lang,
        "transcript_char_count": len(text),
        "transcript_word_count": len(text.split()) if text else 0,
    }


def _write_index(index_path: Path, rows: list[dict]) -> None:
    fieldnames = ["popularity_rank", "video_id", "title", "view_count", "has_transcript",
                  "transcript_status", "transcript_error_detail", "transcript_language",
                  "transcript_char_count", "transcript_word_count"]
    with open(index_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
