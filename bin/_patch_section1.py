import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'd:\Experimentation\Youtube\Scripwriter\generatedScripts\Male Loneliness Epidemic\male_loneliness_gaming_script.md'
with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# Find the key line numbers
idx_data_card = None   # EMERALD data card — zero close friends
idx_paragraph = None   # Men's friendships paragraph
idx_suicide   = None   # EMERALD stat card — Suicide
idx_map       = None   # EMERALD map overlay
idx_covid     = None   # Those spaces were already in decline

for i, line in enumerate(lines):
    if idx_data_card is None and 'zero close friends' in line and 'EMERALD data card' in line:
        idx_data_card = i
    if idx_paragraph is None and "Men\u2019s friendships" in line and 'adolescence' in line:
        idx_paragraph = i
    if idx_suicide is None and 'EMERALD stat card' in line and 'Suicide' in line:
        idx_suicide = i
    if idx_map is None and 'EMERALD map overlay' in line:
        idx_map = i
    if idx_covid is None and 'Those spaces were already in decline' in line:
        idx_covid = i

print(f'data_card={idx_data_card}, paragraph={idx_paragraph}, suicide={idx_suicide}, map={idx_map}, covid={idx_covid}')

if None in (idx_data_card, idx_paragraph, idx_suicide, idx_map, idx_covid):
    print('ERROR: Could not find all lines.')
    sys.exit(1)

# The paragraph at idx_paragraph needs to be split at "no clear infrastructure through which to rebuild."
para = lines[idx_paragraph]
split_marker = 'with no clear infrastructure through which to rebuild.'
split_pos = para.find(split_marker)
if split_pos == -1:
    print('ERROR: split marker not found in paragraph.')
    sys.exit(1)
split_pos += len(split_marker)

para_part1 = para[:split_pos].rstrip() + '\n'
para_part2 = para[split_pos:].lstrip()

# The COVID paragraph at idx_covid needs to be split at "one in four, the highest of any generation."
covid_para = lines[idx_covid]
covid_split_marker = 'one in four, the highest of any generation.'
covid_split_pos = covid_para.find(covid_split_marker)
if covid_split_pos == -1:
    print('ERROR: covid split marker not found.')
    sys.exit(1)
covid_split_pos += len(covid_split_marker)

covid_part1 = covid_para[:covid_split_pos].rstrip() + '\n'
covid_part2 = covid_para[covid_split_pos:].lstrip()

# Build the new block that replaces lines from idx_data_card to idx_covid (inclusive)
# We'll replace lines[idx_data_card .. idx_covid] with the new structure

new_block = (
    para_part1 + '\n'
    + lines[idx_data_card]  # data card
    + '\n'
    + para_part2
    + '\n'
    + lines[idx_suicide]    # suicide stat card
    + '\n'
    + covid_part1 + '\n'
    + lines[idx_map]        # map overlay
    + '\n'
    + covid_part2
)

# Replace from idx_data_card to idx_covid (inclusive), preserving surrounding blank lines
# We need to be careful about blank lines between sections
# The block spans: idx_data_card, blank, idx_paragraph, blank, idx_suicide, blank, idx_map, blank, idx_covid

# Find the range: first non-blank before idx_paragraph (should be idx_data_card)
# Last line in range: idx_covid
start = idx_data_card
# Walk back to include any blank line before idx_data_card that's part of this block
# (we don't want to eat the archival B-roll line above)

end = idx_covid  # inclusive

# Build replacement lines
replacement_lines = new_block.split('\n')
# Ensure each entry ends with \n
replacement_lines_proper = [l + '\n' if not l.endswith('\n') else l for l in replacement_lines]
# The last line might have a trailing newline already

# Actually let's just replace the slice
new_lines = lines[:start] + [new_block] + lines[end + 1:]

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f'OK: Restructured lines {start}–{end}. Section 1 flow fixed.')
