em = '\u2014'
arr = '\u2192'
bull = '\u00b7'
star = '\u2605'
lq = '\u201c'
rq = '\u201d'

path = r'd:\Experimentation\Youtube\Scripwriter\generatedScripts\Male Loneliness Epidemic\male_loneliness_gaming_script.md'
with open(path, encoding='utf-8') as f:
    content = f.read()

replacements = [
    (
        f'[SHOW: data card {em} {lq}Men with zero close friends: 3% (1990) {arr} 15% (2021){rq} {em} Survey Center on American Life, AEI (May 2021) {em} aei.org/articles/mens-social-circles-are-shrinking]',
        f'[SHOW: EMERALD data card {em} {lq}Men with zero close friends: 3% (1990) {arr} 15% (2021){rq} {em} Survey Center on American Life, AEI (May 2021) {em} aei.org/articles/mens-social-circles-are-shrinking]'
    ),
    (
        f'[SHOW: world map {em} loneliness rates by country {em} Meta-Gallup Global State of Social Connections (2023) {em} gallup.com/analytics/509675]',
        f'[SHOW: EMERALD map overlay {em} loneliness rates by country, Cream text labels on Emerald callout boxes {em} Meta-Gallup Global State of Social Connections (2023) {em} gallup.com/analytics/509675]'
    ),
    (
        f'[SHOW: news montage {em} gaming addiction headlines, screen addiction stereotypes]',
        f'[SHOW: news montage {em} gaming addiction headlines, screen addiction stereotypes {em} archival grade: sepia/grain; BURGUNDY lower-third label: "THE CONCERN"]'
    ),
    (
        f'[SHOW: data card {em} {lq}High-risk gamers: depression 9.5%, anxiety 14.5% {em} Low-risk gamers: depression 4.5%, anxiety 9.1%{rq} {em} Jung et al., Psychiatry Investigation 2025 {em} doi.org/10.30773/pi.2023.0385]',
        f'[SHOW: BURGUNDY data card {em} {lq}High-risk gamers: depression 9.5%, anxiety 14.5% {em} Low-risk gamers: depression 4.5%, anxiety 9.1%{rq} {em} Jung et al., Psychiatry Investigation 2025 {em} doi.org/10.30773/pi.2023.0385]'
    ),
    (
        f'[SHOW: Tyler Prochnow / Texas A&M headline {em} digital third place]',
        f'[SHOW: CREAM card {em} Tyler Prochnow / Texas A&M research headline {em} Near Black on Parchment Cream, Burgundy 4px left accent bar]'
    ),
    (
        f'[SHOW: data card {em} ONE GRAPH: Korean nationwide study {em} low-risk gamers vs non-gamers vs high-risk gamers on loneliness scores]',
        f'[SHOW: EMERALD data card {em} bar chart: low-risk gamers vs non-gamers vs high-risk gamers on loneliness scores {em} staggered column build animation {em} Korean nationwide study, Jung et al. 2025]'
    ),
    (
        f'[SHOW: split card {em} Recreational gamer / Achiever / Escaper]',
        f'[SHOW: {star} KEY VISUAL {em} split card {em} Soft Cream (#FBF7F1) background {bull} three columns: RECREATIONAL (Emerald #1F6F54) / ACHIEVER (Antique Gold #C6A15B) / ESCAPER (Burgundy #6B1F2A) {bull} outcome rows: depression rate / anxiety rate / social withdrawal {bull} Fong et al. 2021 data in monospace {bull} source citation bottom-right in Subtle Taupe {bull} staggered column reveal animation]'
    ),
    (
        f'[SHOW: data card {em} Fong et al. 2021: depression, anxiety and social withdrawal outcomes by motivation group {em} pmc.ncbi.nlm.nih.gov/articles/PMC8671754]',
        f'[SHOW: EMERALD data card {em} Fong et al. 2021: depression, anxiety and social withdrawal outcomes by motivation group {em} pmc.ncbi.nlm.nih.gov/articles/PMC8671754]'
    ),
    (
        f'[SHOW: quote card {em} Surgeon General advisory on loneliness, 2023 {em} white on black]',
        f'[SHOW: GOLD quote card {em} Obsidian Charcoal (#121212) background {bull} quote text in Parchment Cream (#F5EFE6) {bull} 6px Antique Gold (#C6A15B) left accent bar {bull} attribution in Antique Gold caps {bull} no music {em} full silence]'
    ),
    (
        f'[SHOW: quote {em} white on black, no music]',
        f'[SHOW: GOLD quote {em} Obsidian Charcoal (#121212) background {bull} Parchment Cream text {bull} Antique Gold attribution {bull} no music {em} full silence until CTA]'
    ),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f'OK: {old[:70]}'.encode('ascii', 'replace').decode())
    else:
        print(f'MISS: {old[:70]}'.encode('ascii', 'replace').decode())

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
