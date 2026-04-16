# Scriptwriter — Project AI Guide

## Purpose
A workspace for writing and rewriting short-form video scripts. The core workflow is:
1. Ingest reference transcripts from a target creator (stored in named folders like `h1t1/`)
2. Ingest raw source material (stored in `DropBox/`)
3. Output polished scripts (stored in `scripts/`) modeled on the target creator's style

---

## Directory Structure
```
/h1t1/              # Style-reference transcripts — creator "h1t1"
/DougSharpe/        # Style-reference transcripts — Doug Sharpe
/CleoAbram/         # Style-reference transcripts — Cleo Abram
/thomasmulligan/    # Style-reference transcripts — Thomas Mulligan
/DropBox/           # Raw source material: articles, transcripts, research PDFs/docs
/scripts/           # Output: finished scripts (Markdown, one file per video)
/docs/              # Style guides, creator profiles, VM_SETUP.md
/data/              # Machine-fetched YouTube metadata & transcripts (ytchan output)
/src/ytchan/        # Python tooling: YouTube API client, transcript fetcher, CLI
/tests/             # Unit tests for ytchan tooling
/bin/               # Batch runners: run_channels, run_transcripts_batched, run_transcripts_loop
```

---

## Creator Profiles

### h1t1 — Style Guide
Short-form (~20–60 sec). See `/docs/h1t1-style.md` for full breakdown.
Key markers: `"So,"` opener · concrete details · `"And well,"` / `"The thing is,"` pivots · sardonic close · no CTAs

### Doug Sharpe — Style Guide
Short-form fun fact (~30–60 sec). Style-reference transcripts in `/DougSharpe/`.
Key markers: invariant `"Fun fact,"` opener · immediate concrete numbers · deadpan/no editorializing · "and/but" chaining · direct quote as ironic end kicker · no CTAs · no pivot phrases

### Cleo Abram — Style Guide
Style-reference transcripts in `/CleoAbram/`. Full style guide TBD in `/docs/`.

### Thomas Mulligan — Style Guide
Style-reference transcripts in `/thomasmulligan/`. Full style guide TBD in `/docs/`.

---

## Script File Format (`/scripts/*.md`)
Each script file includes:
- **Front matter:** style target, format (length), topic
- **## SCRIPT** — the actual spoken content (clean, no stage directions)
- **## STYLE NOTES** — breakdown of how the script maps to the target creator's patterns

---

## Workflow for New Scripts
1. Read `ai.md` (this file)
2. Read all transcripts in the relevant creator folder (e.g. `h1t1/`)
3. Read the source material from `DropBox/`
4. Identify the creator's style fingerprints (see `/docs/` for detailed guides)
5. Write or rewrite the script in `/scripts/`, matching tone and structure

---

## Key Conventions
- Scripts are written for spoken delivery — short sentences, natural rhythm
- Never add stage directions or B-roll notes unless explicitly asked
- Style notes section should map specific lines to specific creator techniques
- Keep scripts under the target duration — trim ruthlessly
