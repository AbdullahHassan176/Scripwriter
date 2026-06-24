import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'd:\Experimentation\Youtube\Scripwriter\generatedScripts\Male Loneliness Epidemic\male_loneliness_gaming_script.md'
with open(path, encoding='utf-8') as f:
    content = f.read()

# Find the director's notes block to replace
# We'll replace from the v2.0 line through the "cards needed" block
old_block = (
    "**v2.0 full rewrite** \u2014 script rebuilt from author\u2019s own article (Male Loneliness Epidemic and Gaming.docx). "
    "Voice, arguments, and structure aligned to how Abdullah naturally writes. "
    "See AbdullahHassan/edit-patterns-from-sa-script.md \u00a715 for new patterns extracted from this article.\n"
    "\n"
    "**2and20 beats:** parallel-trend cold open \u2192 early-research headline \u2192 \u201cconsiderably more complicated\u201d flip \u2192 title card question \u2192 "
    "Section 1 (third places + male friendship structure) \u2192 Section 2 (case against + Korean data) \u2192 "
    "Section 3 (Prochnow + Korean loneliness) \u2192 Section 4 (motivation question = key reframe) \u2192 "
    "Close (societal reframe + Surgeon General + CTA).\n"
    "\n"
    "**NEW in v2.0:** Section 4 (The Motivation Question) \u2014 Fong et al. 2021 study (recreational / achiever / escaper) "
    "is the central reframe that resolves the apparent contradiction between Sections 2 and 3. "
    "Do not cut this section. It is the structural heart of the argument.\n"
    "\n"
    "**Runtime:** ~1,420 words \u00b7 ~11 min at 128 WPM \u00b7 ~9\u201310 min at 150 WPM. "
    "If cutting for sub-10: trim the age-dynamics paragraph in Section 3 (~60 words) and tighten the platform/society paragraph in the Close (~50 words).\n"
    "\n"
    "**TH clips:** 2 total \u2014 title card (end of Hook) + mid sub-nudge (start of Section 4).\n"
    "\n"
    "**New [SHOW:] cards needed:**\n"
    "- WHO stat card (280M depression)\n"
    "- Fong et al. 2021 motivation split card (3 groups + outcomes)"
)

new_block = (
    "**v2.0 full rewrite** \u2014 script rebuilt from author\u2019s own article (Male Loneliness Epidemic and Gaming.docx). "
    "Voice, arguments, and structure aligned to how Abdullah naturally writes. "
    "See AbdullahHassan/edit-patterns-from-sa-script.md \u00a715 for new patterns extracted from this article.\n"
    "\n"
    "**2and20 beats:** parallel-trend cold open \u2192 early-research headline \u2192 \u201cconsiderably more complicated\u201d flip \u2192 title card question \u2192 "
    "Section 1 (third places + male friendship structure) \u2192 Section 2 (case against + Korean data) \u2192 "
    "Section 3 (Prochnow + Korean loneliness) \u2192 Section 4 (motivation question = key reframe) \u2192 "
    "Close (societal reframe + Surgeon General + CTA).\n"
    "\n"
    "**NEW in v2.0:** Section 4 (The Motivation Question) \u2014 Fong et al. 2021 study (recreational / achiever / escaper) "
    "is the central reframe that resolves the apparent contradiction between Sections 2 and 3. "
    "Do not cut this section. It is the structural heart of the argument.\n"
    "\n"
    "**Runtime:** ~1,420 words \u00b7 ~11 min at 128 WPM \u00b7 ~9\u201310 min at 150 WPM. "
    "If cutting for sub-10: trim the age-dynamics paragraph in Section 3 (~60 words) and tighten the platform/society paragraph in the Close (~50 words).\n"
    "\n"
    "**TH clips:** 2 total \u2014 title card (end of Hook) + mid sub-nudge (start of Section 4).\n"
    "\n"
    "**New [SHOW:] cards needed:**\n"
    "- WHO stat card (280M depression)\n"
    "- Fong et al. 2021 motivation split card (3 groups + outcomes)\n"
    "\n"
    "---\n"
    "\n"
    "**\u2605 KEY VISUAL**\n"
    "The Fong et al. motivation split card (Section 4, \u2605 KEY VISUAL tag) is the napkin drawing for this video. Every prior data card builds to this one.\n"
    "- Structure: one controller icon \u2192 three branching paths \u2192 columns: RECREATIONAL / ACHIEVER / ESCAPER \u2192 three outcome rows beneath each: depression rate / anxiety rate / social withdrawal\n"
    "- Column colours: Recreational = Emerald #1F6F54 \u00b7 Achiever = Antique Gold #C6A15B \u00b7 Escaper = Burgundy #6B1F2A\n"
    "- Background: Soft Cream #FBF7F1. Numbers in monospace. Source citation bottom-right in Subtle Taupe.\n"
    "- Animation: staggered column reveal \u2014 one column at a time, 60\u2013100ms stagger. Hold each column 2 seconds before next appears.\n"
    "- Do not cut or abbreviate. Hold the complete card on screen for at least 5 seconds after the final column reveals.\n"
    "\n"
    "---\n"
    "\n"
    "**EDITING STYLE**\n"
    "- **Pattern interrupt every 90\u2013120 seconds:** new B-roll cut, TH clip, data card, or timeline jump. Never hold one visual type longer than 2 minutes.\n"
    "- **Visual leads narration:** cut to the visual BEFORE Abdullah references it. The eye precedes the ear \u2014 audience sees it first, then hears the explanation.\n"
    "- **Data breathe:** hold every data card or stat card on screen for a minimum of 3\u20135 seconds before cutting. Do not rush data moments.\n"
    "- **Silence is a tool:** near-silence or no music under all data cards; full silence before and after the Surgeon General quote. Let the weight land before the CTA.\n"
    "- **Cold open audio:** no music in the first 30 seconds. Ambient sound only; a subtle low-frequency score enters under the WHO/depression stats (~lines 20\u201324 of script).\n"
    "- **Score arc:** understated tension build through Sections 1\u20133. Score builds only in the final 90 seconds (Close). Music fades completely under the Surgeon General quote; returns quietly as VO resumes after [PAUSE].\n"
    "- **J-cut into Section 1:** let pub/sports archival audio begin one beat before the news montage cuts away. Creates pull into the third-place narrative.\n"
    "- **Archive footage** (gaming headlines, 2000s\u20132010s): apply sepia/grain grade to visually separate from present-day footage. Do not use the same grade for historical and contemporary material.\n"
    "- **TH grade:** warmer, slightly higher contrast for authority. B-roll slightly cooler and more cinematic. Never match TH and B-roll grades identically.\n"
    "- **TH jump cuts:** acceptable for pacing \u2014 remove hesitations, keep natural rhythm.\n"
    "- **Primary source quote (Surgeon General):** music fades completely under the quote. The quote speaks alone. Score returns as VO resumes.\n"
    "\n"
    "---\n"
    "\n"
    "**BRAND COLOUR GUIDE \u2014 GRAPHICS**\n"
    "All graphics use the four-colour palette only. Quick reference for this script:\n"
    "\n"
    "| Card type | Background | Number / stat | Label / body | Accent |\n"
    "|-----------|-----------|---------------|--------------|--------|\n"
    "| EMERALD stat/data card (verified fact) | Deep Emerald #1F6F54 | Antique Gold #C6A15B \u00b7 Inter 900 mono | Parchment Cream #F5EFE6 \u00b7 Inter 600 caps | \u2014 |\n"
    "| BURGUNDY data card (case against / contrarian) | Imperial Burgundy #6B1F2A | Antique Gold #C6A15B | Parchment Cream #F5EFE6 | \u2014 |\n"
    "| CREAM card (researcher / paper credit) | Parchment Cream #F5EFE6 | Near Black #1A1A1A \u00b7 Inter 700 | Muted Ash-Brown #5F5A55 \u00b7 Inter 400 | 4px Burgundy left bar |\n"
    "| \u2605 KEY VISUAL split card | Soft Cream #FBF7F1 | Per column (see above) | Near Black #1A1A1A \u00b7 Inter 700 | Column colour as header fill |\n"
    "| GOLD quote card (Surgeon General) | Obsidian Charcoal #121212 | \u2014 | Parchment Cream #F5EFE6 \u00b7 italic | 6px Antique Gold #C6A15B left bar |\n"
    "| Lower third (name / role) | Parchment Cream #F5EFE6 | \u2014 | Near Black Inter 700 / Ash-Brown Inter 400 | 4px Burgundy left bar |\n"
    "| Source citations (all cards) | Transparent overlay | \u2014 | Subtle Taupe #B8AEA1 \u00b7 Inter 400 \u00b7 small | \u2014 |\n"
    "\n"
    "**General rules:**\n"
    "- Never use pure white (#FFF) or pure black (#000) \u2014 use Parchment Cream and Obsidian Charcoal instead.\n"
    "- Brand gradient (Burgundy #6B1F2A \u2192 Emerald #1F6F54 \u2192 Gold #C6A15B, 135\u00b0) applies to exactly ONE focal element per frame \u2014 thumbnail keyword or title card only \u2014 never to backgrounds.\n"
    "- Data chart builds: grow from zero values, staggered 60\u2013100ms per element. Hold 3\u20135 seconds after complete.\n"
    "- Glow effects if used: maximum 0.2\u20130.4 opacity. Subtle authority, never neon."
)

if old_block in content:
    content = content.replace(old_block, new_block)
    print("OK: Director's notes replaced.")
else:
    print("MISS: Could not find old block.")
    # Debug: show chars around the v2.0 line
    idx = content.find("v2.0 full rewrite")
    if idx != -1:
        print(f"Found v2.0 at index {idx}. Nearby repr:")
        print(repr(content[idx:idx+200]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
