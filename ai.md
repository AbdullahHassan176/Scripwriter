# Scriptwriter — Project AI Guide

## Purpose
A workspace for writing, rewriting, and deeply analyzing short-form and long-form video scripts. Two core workflows:
1. **Creator Analysis** — ingest transcripts from `scripts/<creator>/`, fetch YouTube metadata via `bin/fetch_creator_stats.py`, and generate detailed creator analysis docs in `docs/`
2. **Script Writing** — use style reference transcripts + analysis docs to write new scripts modeled on a target creator's patterns

---

## Directory Structure
```
/scripts/<creator>/   # Manually-pulled Tactiq transcripts (one folder per creator)
/docs/                # Creator analysis MDs, style guides, VM_SETUP.md
/data/<creator>/      # Machine-fetched YouTube metadata (videos_metadata.json)
/bin/                 # Tools: fetch_creator_stats.py, run_channels, etc.
/src/ytchan/          # Python YouTube API client and transcript tooling
/tests/               # Unit tests for ytchan
/generatedScripts/    # Output scripts
/research/            # Raw source material
```

---

## Creator Profiles & Analysis Docs

| Creator | Format | Niche | Subs | Avg Views | Analysis Doc |
|---|---|---|---|---|---|
| **2and20** | Long-form (8–22 min) | Economics, geopolitics | 275K | 767K | `docs/2and20-analysis.md` |
| **h1t1** | Ultra-short (13–46s) | Viral callouts, debunking | 7.95M | 64.6M | `docs/h1t1-analysis.md` |
| **HTXStudio** | Long-form (4–14 min) | Maker, science experiments | 2.06M | 2.4M | `docs/HTXStudio-analysis.md` |
| **DougSharpe** | Ultra-short (29–59s) | Fun facts | 1.36M | 25.5M | `docs/DougSharpe-analysis.md` |
| **CleoAbram** | Short (35–59s) | Science curiosity | 7.9M | 53.8M | `docs/CleoAbram-analysis.md` |
| **thomasmulligan** | Short (43–59s) | Hypotheticals, thought experiments | 2.05M | 26.8M | `docs/thomasmulligan-analysis.md` |

---

## Workflow: Adding a New Creator

1. Drop Tactiq transcript `.txt` files into `scripts/<creator>/`
2. Run `python bin/fetch_creator_stats.py <creator>` — saves to `data/<creator>/videos_metadata.json`
3. Read all transcripts + metadata, then write `docs/<creator>-analysis.md`
4. Add the creator row to the table above

### fetch_creator_stats.py
- Extracts video IDs from filenames (`tactiq-free-transcript-<videoId>.txt`)
- Fetches metadata via yt-dlp (no API key required): views, likes, comments, duration, upload date, tags, description, subscriber count
- Caches existing results; run again to top-up new videos only
- Usage: `python bin/fetch_creator_stats.py <creator>` or `--all`

---

## Workflow: Writing New Scripts

1. Read this file (`ai.md`)
2. Read the target creator's analysis doc in `docs/`
3. Read 2-3 of their transcripts from `scripts/<creator>/`
4. Write the script in `generatedScripts/`, matching tone and structure per the analysis doc
5. Include STYLE NOTES section mapping script lines to identified creator techniques

---

## Creator Style Fingerprints (Quick Reference)

- **2and20:** Date + person cold open → "But..." flip → "I am [host] from 2&20. And this is [Country]: [subtitle]" → History lesson → thematic sponsor → literary conclusion with historical quote
- **h1t1:** "So," opener → viral situation → "And well, that's because it isn't." pivot → sardonic one-liner close → no CTA
- **HTXStudio:** Ambitious claim → "No AI, no screens" → personal origin story → failure arc → rigorous methodology → result
- **DougSharpe:** "Fun fact," → specific name + place + concrete numbers → unexpected twist → ironic final quote → no CTA
- **CleoAbram:** Question hook → familiar → surprising deeper fact → mind-blowing comparison → "follow for more"
- **thomasmulligan:** "Let's say you wake up..." → cascading consequence timeline → final reframe → no CTA

---

## Workflow: Visual Script Builder

Converts a script + production package into a production walkthrough (HTML + Word).

**Word-first:** Edit `visual_script.docx` (`[VO]`, `[TH]`, `[SHOW: …]`), then sync:
`python bin/build_visual_script.py SCRIPT.md --sync-docx visual_script.docx`

**Markdown-first:** Edit `script.md`, then build (no `--sync-docx`).

See `docs/visual_script_builder.md` for flags and editing conventions.

---

## Key Conventions
- Scripts are for spoken delivery — short sentences, natural rhythm
- Analysis docs live in `docs/<creator>-analysis.md` and follow the full hyper-analysis format (performance table, formula breakdown, what works, what doesn't, title tiers, key takeaways)
- Never add stage directions or B-roll notes unless explicitly asked
- Data in analysis docs comes from `data/<creator>/videos_metadata.json`
- See `docs/VM_SETUP.md` for environment setup
