import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'd:\Experimentation\Youtube\Scripwriter\generatedScripts\Male Loneliness Epidemic\male_loneliness_gaming_script.md'
with open(path, encoding='utf-8') as f:
    content = f.read()

em = '\u2014'
arr = '\u2192'
bull = '\u00b7'
star = '\u2605'
lq = '\u201c'
rq = '\u201d'

fixes = []

# ── FIX 1 + 2: Section 1 — move zero-close-friends card mid-paragraph,
#               separate stacked cards, split COVID paragraph around map overlay
old1 = (
    f'[SHOW: EMERALD data card {em} {lq}Men with zero close friends: 3% (1990) {arr} 15% (2021){rq} {em} Survey Center on American Life, AEI (May 2021) {em} aei.org/articles/mens-social-circles-are-shrinking]\n'
    '\n'
    f'Men\u2019s friendships in adolescence and early adulthood tend to form around shared activities and structured environments {em} school, sports, university, military service, religious groups. When those structures dissolve, the friendships often dissolve with them. Unlike women, who are generally more likely to maintain close friendships through deliberate social effort, men frequently find themselves socially stranded in their late twenties and thirties with no clear infrastructure through which to rebuild. The share of men reporting no close friends at all grew from three in every hundred in 1990 to fifteen in every hundred by 2021. Researchers consistently find that men with no close confidants are significantly more likely to experience depression, anxiety, and suicidal ideation {em} and men account for approximately three-quarters of suicides in both the United States and the United Kingdom.\n'
    '\n'
    f'[SHOW: EMERALD stat card {em} {lq}Suicide: 2nd leading cause of death, ages 15{em}34 (US). Men: 4x more likely than women.{rq} {em} AFSP (2024) / WHO Suicide Fact Sheet (2025)]\n'
    '\n'
    f'[SHOW: EMERALD map overlay {em} loneliness rates by country, Cream text labels on Emerald callout boxes {em} Meta-Gallup Global State of Social Connections (2023) {em} gallup.com/analytics/509675]\n'
    '\n'
    f'Those spaces were already in decline before COVID arrived. A global survey across 142 countries found that young adults between nineteen and twenty-nine are now the loneliest age group on earth {em} one in four, the highest of any generation. When the pandemic arrived and closed what was left of those spaces overnight, men who had been quietly managing with one or two connections were left with none. By 2023, the World Health Organization had classified loneliness as a public health priority on the same level as smoking, and the U.S. Surgeon General had named it a public health epidemic.'
)

new1 = (
    f'Men\u2019s friendships in adolescence and early adulthood tend to form around shared activities and structured environments {em} school, sports, university, military service, religious groups. When those structures dissolve, the friendships often dissolve with them. Unlike women, who are generally more likely to maintain close friendships through deliberate social effort, men frequently find themselves socially stranded in their late twenties and thirties with no clear infrastructure through which to rebuild.\n'
    '\n'
    f'[SHOW: EMERALD data card {em} {lq}Men with zero close friends: 3% (1990) {arr} 15% (2021){rq} {em} Survey Center on American Life, AEI (May 2021) {em} aei.org/articles/mens-social-circles-are-shrinking]\n'
    '\n'
    f'The share of men reporting no close friends at all grew from three in every hundred in 1990 to fifteen in every hundred by 2021. Researchers consistently find that men with no close confidants are significantly more likely to experience depression, anxiety, and suicidal ideation {em} and men account for approximately three-quarters of suicides in both the United States and the United Kingdom.\n'
    '\n'
    f'[SHOW: EMERALD stat card {em} {lq}Suicide: 2nd leading cause of death, ages 15{em}34 (US). Men: 4x more likely than women.{rq} {em} AFSP (2024) / WHO Suicide Fact Sheet (2025)]\n'
    '\n'
    f'Those spaces were already in decline before COVID arrived. A global survey across 142 countries found that young adults between nineteen and twenty-nine are now the loneliest age group on earth {em} one in four, the highest of any generation.\n'
    '\n'
    f'[SHOW: EMERALD map overlay {em} loneliness rates by country, Cream text labels on Emerald callout boxes {em} Meta-Gallup Global State of Social Connections (2023) {em} gallup.com/analytics/509675]\n'
    '\n'
    f'When the pandemic arrived and closed what was left of those spaces overnight, men who had been quietly managing with one or two connections were left with none. By 2023, the World Health Organization had classified loneliness as a public health priority on the same level as smoking, and the U.S. Surgeon General had named it a public health epidemic.'
)

if old1 in content:
    content = content.replace(old1, new1)
    fixes.append('FIX 1+2: Section 1 card positions and stacked cards resolved.')
else:
    fixes.append('MISS 1+2: Section 1 block not found.')

# ── FIX 3: Section 3 — move Korean chart to mid-paragraph
old3 = (
    f'[SHOW: EMERALD data card {em} bar chart: low-risk gamers vs non-gamers vs high-risk gamers on loneliness scores {em} staggered column build animation {em} Korean nationwide study, Jung et al. 2025]\n'
    '\n'
    f'Prochnow found that users who reported greater feelings of depression and less access to real-life support were about forty percent more likely to form and maintain social bonds within the online gaming space compared to users who already had strong offline networks. In other words, these communities were doing the most for the men who had the least support everywhere else. The Korean nationwide study reinforced this {em} low-risk male gamers scored significantly lower on loneliness measures than either non-gamers or high-risk gamers.'
)

new3 = (
    f'Prochnow found that users who reported greater feelings of depression and less access to real-life support were about forty percent more likely to form and maintain social bonds within the online gaming space compared to users who already had strong offline networks. In other words, these communities were doing the most for the men who had the least support everywhere else.\n'
    '\n'
    f'[SHOW: EMERALD data card {em} bar chart: low-risk gamers vs non-gamers vs high-risk gamers on loneliness scores {em} staggered column build animation {em} Korean nationwide study, Jung et al. 2025]\n'
    '\n'
    f'The Korean nationwide study reinforced this {em} low-risk male gamers scored significantly lower on loneliness measures than either non-gamers or high-risk gamers.'
)

if old3 in content:
    content = content.replace(old3, new3)
    fixes.append('FIX 3: Korean chart moved to mid-paragraph (after Prochnow findings).')
else:
    fixes.append('MISS 3: Section 3 block not found.')

# ── FIX 4: Section 4 — KEY VISUAL starts headers-only; data card is the reveal
old4 = (
    f'[SHOW: {star} KEY VISUAL {em} split card {em} Soft Cream (#FBF7F1) background {bull} three columns: RECREATIONAL (Emerald #1F6F54) / ACHIEVER (Antique Gold #C6A15B) / ESCAPER (Burgundy #6B1F2A) {bull} outcome rows: depression rate / anxiety rate / social withdrawal {bull} Fong et al. 2021 data in monospace {bull} source citation bottom-right in Subtle Taupe {bull} staggered column reveal animation]'
)

new4 = (
    f'[SHOW: {star} KEY VISUAL {em} split card {em} initially show COLUMN HEADERS ONLY: RECREATIONAL / ACHIEVER / ESCAPER {bull} outcome rows hidden until EMERALD data card reveal below {bull} Soft Cream (#FBF7F1) background {bull} column header colours: Emerald #1F6F54 / Antique Gold #C6A15B / Burgundy #6B1F2A {bull} staggered header reveal animation]'
)

if old4 in content:
    content = content.replace(old4, new4)
    fixes.append('FIX 4: KEY VISUAL updated to headers-only; data card is the outcome reveal.')
else:
    fixes.append('MISS 4: KEY VISUAL tag not found.')

# ── FIX 5: Close — remove duplicate [SHOW:] before verbal setup; reorder to verbal → card → quote
old5 = (
    f'[SHOW: GOLD quote card {em} Obsidian Charcoal (#121212) background {bull} quote text in Parchment Cream (#F5EFE6) {bull} 6px Antique Gold (#C6A15B) left accent bar {bull} attribution in Antique Gold caps {bull} no music {em} full silence]\n'
    '\n'
    'In 2023, the U.S. Surgeon General put it this way:\n'
    '\n'
    f'[SHOW: GOLD quote {em} Obsidian Charcoal (#121212) background {bull} Parchment Cream text {bull} Antique Gold attribution {bull} no music {em} full silence until CTA]'
)

new5 = (
    'In 2023, the U.S. Surgeon General put it this way:\n'
    '\n'
    f'[SHOW: GOLD quote card {em} Obsidian Charcoal (#121212) background {bull} quote text in Parchment Cream (#F5EFE6) {bull} 6px Antique Gold (#C6A15B) left accent bar {bull} attribution in Antique Gold caps {bull} no music {em} full silence until CTA]'
)

if old5 in content:
    content = content.replace(old5, new5)
    fixes.append('FIX 5: Close quote — verbal setup now precedes card reveal.')
else:
    fixes.append('MISS 5: Close quote block not found.')

# ── FIX 6: Close — add B-roll direction after [PAUSE]
old6 = '[PAUSE]\n\nNo single app or platform'
new6 = '[PAUSE]\n\n[SHOW: B-roll \u2014 men in voice chat, laughing between rounds; cut back to cross-generational gaming community from Section 3]\n\nNo single app or platform'

if old6 in content:
    content = content.replace(old6, new6)
    fixes.append('FIX 6: B-roll direction added after [PAUSE].')
else:
    fixes.append('MISS 6: [PAUSE] block not found.')

# ── FIX 7: Differentiate the two news montages
old7a = '[SHOW: news montage \u2014 gaming addiction headlines, 2000s\u20132010s \u2014 archival grade: sepia/grain treatment to separate from present-day footage]'
new7a = '[SHOW: news montage \u2014 print headlines and early internet forums, gaming addiction discourse, 2000s\u2013early 2010s \u2014 archival grade: sepia/grain \u2014 use different footage from Section 2 montage]'

old7b = '[SHOW: news montage \u2014 gaming addiction headlines, screen addiction stereotypes \u2014 archival grade: sepia/grain; BURGUNDY lower-third label: "THE CONCERN"]'
new7b = '[SHOW: news montage \u2014 TV segments, YouTube commentary, social media discourse on screen addiction, 2010s\u20132020s \u2014 archival grade: sepia/grain; BURGUNDY lower-third label: "THE CONCERN" \u2014 use different footage from Hook montage]'

if old7a in content:
    content = content.replace(old7a, new7a)
    fixes.append('FIX 7a: Hook montage note updated (print/early internet).')
else:
    fixes.append('MISS 7a: Hook montage tag not found.')

if old7b in content:
    content = content.replace(old7b, new7b)
    fixes.append('FIX 7b: Section 2 montage note updated (TV/social media era).')
else:
    fixes.append('MISS 7b: Section 2 montage tag not found.')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

for fix in fixes:
    print(fix)
print('Done.')
