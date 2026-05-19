from pathlib import Path
path = Path('Driverapp.py')
text = path.read_text(encoding='utf-8')
for i, line in enumerate(text.splitlines(), start=1):
    if i in (220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236):
        print(f'{i}: {line}')
