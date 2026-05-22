# Visual Script Builder

Builds a production walkthrough from your script markdown: HTML (browser) + DOCX (Word).

## Edit in Word → sync everything

1. Generate once (creates `visual_script.docx` with editable markers):

   ```powershell
   python bin/build_visual_script.py "generatedScripts/<project>/script.md" --package "generatedScripts/<project>/production_package.md" --context "South Africa"
   ```

2. Open **`visual_script.docx`** in Word and edit:
   - **`[VO]`** — voiceover (default narration over B-roll)
   - **`[TH]`** — talking head / on camera
   - **`[SP]`** — sponsor read
   - **`[SUB]`** — subscribe bump
   - **`[SHOW: …]`** — what appears on screen (one line per visual)
   - **`[PAUSE]`** — hold / beat
   - Dark shaded lines — section headers (e.g. HOOK, SECTION 1)
   - **`---`** — section break

3. After saving in Word, sync back to markdown + HTML:

   ```powershell
   python bin/build_visual_script.py "generatedScripts/<project>/script.md" --sync-docx "generatedScripts/<project>/visual_script.docx" --package "generatedScripts/<project>/production_package.md" --context "South Africa" --no-fetch
   ```

   This updates:
   - `script.md` (source script body)
   - `visual_script.html` (production layout with charts + delivery tags)
   - `visual_script.docx` (refreshed from your edits; image tables regenerated)

Use **`--no-fetch`** while drafting (fast). Omit it when you want Wikimedia thumbnails refreshed.

## Edit markdown → build outputs

Edit `script.md` directly, then run the build command (without `--sync-docx`).

## Flags

| Flag | Purpose |
|------|---------|
| `--package` | Production package for shot numbers / sources |
| `--context` | Topic hint for image search |
| `--no-fetch` | Skip Wikimedia (faster) |
| `--html-only` | Skip DOCX |
| `--docx-only` | Skip HTML |
| `--sync-docx` | Import edits from Word |
