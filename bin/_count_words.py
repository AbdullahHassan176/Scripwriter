import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'd:\Experimentation\Youtube\Scripwriter\generatedScripts\Male Loneliness Epidemic\male_loneliness_gaming_script.md'
with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# Stop counting at the director's notes separator
spoken_lines = []
for line in lines:
    if line.strip().startswith('DIRECTOR') or line.strip().startswith('KEY DATA'):
        break
    stripped = line.strip()
    # Skip: [SHOW:...], ## headers, ---, ━━━, 🎥, [TBC...], [PAUSE], [PLACEHOLDER], blank
    if not stripped:
        continue
    if stripped.startswith('[SHOW:') or stripped.startswith('[TBC') or stripped.startswith('[PAUSE') or stripped.startswith('[PLACEHOLDER'):
        continue
    if stripped.startswith('##') or stripped.startswith('---') or stripped.startswith('━'):
        continue
    if stripped.startswith('🎥'):
        continue
    spoken_lines.append(stripped)

spoken_text = ' '.join(spoken_lines)
words = len(spoken_text.split())

# Known calibration: 153 words in 53 seconds → 173.2 WPM
passage_words = 153
passage_seconds = 53
wpm = (passage_words / passage_seconds) * 60

total_seconds = (words / wpm) * 60
minutes = int(total_seconds // 60)
seconds = int(total_seconds % 60)

print(f'Spoken word count : {words} words')
print(f'Your speaking rate : {wpm:.0f} WPM  (calibrated from 53s sample)')
print(f'Estimated runtime  : {minutes} min {seconds} sec')
print()
# Also show at common rates for comparison
for rate, label in [(128, '128 WPM — slow/deliberate'), (150, '150 WPM — conversational'), (173, 'your measured rate')]:
    t = (words / rate) * 60
    m, s = int(t // 60), int(t % 60)
    print(f'  At {rate} WPM ({label}): {m}:{s:02d}')
