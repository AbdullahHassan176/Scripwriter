import sys
sys.stdout.reconfigure(encoding='utf-8')
path = r'd:\Experimentation\Youtube\Scripwriter\generatedScripts\Male Loneliness Epidemic\male_loneliness_gaming_script.md'
with open(path, encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines, 1):
    if 'Suicide' in line or 'AFSP' in line:
        print(f'L{i}: {repr(line)}')
