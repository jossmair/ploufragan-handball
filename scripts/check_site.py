"""Check generated HTML references to local files."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
missing = []
for page in root.glob("*.html"):
    html = page.read_text(encoding="utf-8")
    for target in re.findall(r'(?:src|href)="([^"#?]+)', html):
        if re.match(r"^[a-z]+:", target):
            continue
        if not (root / target).exists():
            missing.append((page.name, target))

print(f"Pages: {len(list(root.glob('*.html')))}")
print(f"Références locales manquantes: {len(missing)}")
for page_name, target in missing:
    print(f"- {page_name}: {target}")
raise SystemExit(bool(missing))
