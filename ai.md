# Scriptwriter — Project AI Guide

## Purpose
A workspace for writing and rewriting short-form video scripts. The core workflow is:
1. Ingest reference transcripts from a target creator (stored in named folders like `h1t1/`)
2. Ingest raw source material (stored in `DropBox/`)
3. Output polished scripts (stored in `scripts/`) modeled on the target creator's style

---

## Directory Structure
```
/h1t1/          # Reference transcripts for creator "h1t1" (YouTube short-form)
/DropBox/       # Raw source material: transcripts, articles, research docs
/scripts/       # Output: finished scripts (Markdown, one file per video)
/docs/          # Extended style guides and creator profiles (see below)
```

---

## Creator Profiles

### h1t1 — Style Guide
Short-form (~20–60 sec). See `/docs/h1t1-style.md` for full breakdown.
Key markers: `"So,"` opener · concrete details · `"And well,"` / `"The thing is,"` pivots · sardonic close · no CTAs

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
