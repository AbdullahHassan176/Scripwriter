# Abdullah Hassan — Scriptwriting Decisions & Production Preferences

> Practical decisions about how scripts are structured, sourced, and built for production.
> This file captures choices made *while writing*, not just style rules.
> **Update this file** whenever a new structural decision, sourcing preference, or format change is confirmed through editing a real script.

**Voice & sentence rules:** [`writing-style-guide.md`](writing-style-guide.md)
**AI tells to avoid:** [`avoid-ai-sounding-writing.md`](avoid-ai-sounding-writing.md)
**Before/after edit patterns:** [`edit-patterns-from-sa-script.md`](edit-patterns-from-sa-script.md)
**Speak vs show decisions:** [`speak-vs-show-checklist.md`](speak-vs-show-checklist.md)

---

## 1. Script Format

**Default structure:** 2and20-style. See `docs/2and20-analysis.md` for the full breakdown.

| Beat | What goes here |
|------|----------------|
| Cold open | Date + place + named person or policy moment |
| Contradiction flip | What the headline said vs what the data shows |
| Title card (TH) | *"I am Abdullah Hassan. And this is [Title]."* |
| Sections | Mechanism → evidence → honest limits |
| Mid sub-nudge | Short TH subscribe line — only once, deep in the video |
| Close | Reframe + historical quote (white on black) + `[PAUSE]` |

**Script header block** — always include estimated runtime and word count:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SCRIPT: [Title]
Estimated Runtime: ~X mins (~N words spoken)
Audience: International — explain every term, assume nothing
Recording draft: vX — 2and20 structure · Abdullah voice
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 2. Runtime Targets

| Format | Target | Approximate word count at ~128 WPM |
|--------|--------|-------------------------------------|
| Flagship (Africa/economics) | 15–20 min | 1,900–2,600 words |
| Sub-10 topic video | < 10 min | ~1,280 words |

When over target: cut essay bridges and recap layers first, never the hook or thesis.

---

## 3. Visual Sourcing Discipline

**Rule: every spoken stat needs a `[SHOW:]` before it.** Never state a number into the air without something on screen. The stat card covers you evidentially and gives the viewer something to read while you speak.

**`[SHOW:]` format for data cards:**
```
[SHOW: stat card — "Male suicide rates up ~20%" — source: Men's Health Network / PCORI Expert Panel Report, Oct 2019]
```

**Include the source name on the card itself.** Viewers can pause and read it; it also functions as an on-screen citation.

**When writing a script, include actual URLs** for the AI or editor to locate chart assets. Place them in the `KEY DATA SOURCES` block at the bottom, not mid-script.

```
KEY DATA SOURCES format:
- **Source name (Year)** — one-line description — URL — *what specific chart/graphic to pull from it*
```

---

## 4. Global Framing First

**Default audience:** International. Do not anchor loneliness, health, or social statistics to the United States alone unless the data point is specifically about the US.

**Preferred approach:**
- Use concrete **policy moments from multiple countries** as global anchors (e.g. UK Minister for Loneliness Jan 2018, Japan Minister for Loneliness Feb 2021).
- Use **global survey data** where available (e.g. Meta-Gallup 142-country study 2023) for the world map visual beat.
- US-specific stats (Cigna, Surgeon General) are supporting evidence, not the primary frame.

**Pattern:**
1. Concrete dated policy moment in a non-US country → establishes global reach
2. Global survey data → provides the world map or multi-country graphic
3. COVID or event → accelerant framing, not origin

---

## 5. TH (Talking Head) Discipline

- TH only on **thesis declarations**, title card, and subscribe nudge.
- Target: 2–3 TH clips per sub-10 min video; 5–6 clips per 15–20 min video.
- TH title card always ends: *"And this is [spoken show title]."*
- TH credential line should match the **video's topic** — for male loneliness, drop "regional expert in African economies." Use the plain name only: *"I am Abdullah Hassan."*

---

## 6. Spoken Delivery Checks (before calling a draft done)

These are the most common failures found while editing real scripts:

1. **Causal connectivity** — if two sentences share a cause/effect relationship, connect them grammatically. Do not leave a blank line between a stat and its reason. (See `edit-patterns-from-sa-script.md` §11.)
2. **Fragment chains** — no staccato one-liners in a row. Merge into flowing sentences.
3. **Parallel staccato evidence** — two or more short sentences building parallel supporting points ("Rates were climbing. Researchers were publishing.") should be joined with *and* or a comma rather than left as separate sentences.
4. **Contrast rhythm** — banned in all forms: em-dash flip, explicit contrast, and split-sentence contrast (two short punchy sentences where B negates or qualifies A). If sentence B qualifies sentence A, merge them into one. (See `avoid-ai-sounding-writing.md` §4.1–4.1c.)
5. **Consistent number units** — when comparing two data points, use the same format throughout the comparison. Do not switch from fractions to percentages to counts mid-sentence. Pick one and stay with it. *(Male Loneliness Gaming script, Jun 2026)*
6. **Rhetorical question ladders for social silence** — when explaining why a stigma or silence persists, prefer 2–4 building questions over declarative statements. Open with the factual contradiction, ask the genuine question, ask the consequence, close with one plain declarative. See `edit-patterns-from-sa-script.md` §13. *(Male Loneliness Gaming script, Jun 2026)*
7. **"That matters"** — never used as a standalone narrator line. Prove it with the next sentence.
8. **Read aloud test** — if you pause mid-sentence to process grammar, rewrite it.

---

## 7. How to Update This File

Add a new entry under the relevant section whenever:

- Abdullah explicitly rejects or rewrites a phrasing pattern in a real script
- A new structural decision is confirmed (e.g. a new section beat, a new visual format)
- A sourcing convention is established (e.g. a preferred dataset for a topic)
- A runtime or format decision changes

Each update should include a one-line note of **which script it came from and the date**, so the rule has a traceable origin. Example:

> *(Male Loneliness Gaming script, Jun 2026)* — global framing preferred over US-only stats; use multi-country policy moments as anchors.

---

## 8. Johnny Harris Explanatory Patterns (apply where complex concepts appear)

Johnny Harris grounds every concept the moment it is introduced. Do not assume the listener knows the term. Use these moves:

| Pattern | Example |
|---------|---------|
| Name the concept, then immediately define it in plain speech | *"There is an idea in sociology called a third place. Your first place is home. Your second place is work. The third place is everything else."* |
| Make research feel active and curious, not passive and formal | *"A researcher named X decided to study..."* not *"X followed members for a year"* |
| After a clinical comparison, state what it actually means | *"Not as a metaphor — as an actual measured risk to how long you live."* |
| Use "And remember" to callback earlier points across sections | *"And remember, these are the same communities that..."* |

**When to use:** Any time you introduce a term from sociology, psychology, or public health that a non-specialist audience might not know. Define it in the next sentence, in spoken language, before moving on. *(Male Loneliness Gaming script, Jun 2026)*

---

## 9. Scripts in Production (Reference Implementations)

| Script | Location | Notes |
|--------|----------|-------|
| SA Captured Rainbow | `generatedScripts/SA Captured Rainbow/` | Flagship format; 15–20 min; Mandela/economics |
| Male Loneliness Epidemic | `generatedScripts/Male Loneliness Epidemic/` | Sub-10 min format; health/social topic |

---

*Created: Jun 2026. Update incrementally — do not let this file exceed 120 lines. Defer topic-specific sourcing notes to the relevant production package.*
