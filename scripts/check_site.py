"""Check generated HTML references to local files."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
missing = []
for page in root.rglob("*.html"):
    html = page.read_text(encoding="utf-8")
    for target in re.findall(r'(?:src|href)="([^"#?]+)', html):
        if re.match(r"^[a-z]+:", target):
            continue
        if not (page.parent / target).exists():
            missing.append((page.relative_to(root), target))

print(f"Pages: {len(list(root.rglob('*.html')))}")
print(f"Références locales manquantes: {len(missing)}")
for page_name, target in missing:
    print(f"- {page_name}: {target}")
raise SystemExit(bool(missing))
