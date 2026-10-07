"""Regenerate Gallery hub previews with Pillow; not required by the CI site build."""
from pathlib import Path
import hashlib
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
previews = ROOT / 'assets/gallery-previews'
previews.mkdir(exist_ok=True)
youth = json.loads((DATA / 'youth_galleries.json').read_text(encoding='utf-8'))
albums = json.loads((DATA / 'galeries.json').read_text(encoding='utf-8'))
covers = [f"assets/{slug}/gallery/{youth[slug]['photos'][0]['file']}" for slug in ('u13-filles','u13-garcons','u15-filles','u18-garcons','u11-mixte')]
covers += [album['cover'] for album in albums]
covers += ['assets/stage-ete/photo-003.webp']
manifest = {}
for source in dict.fromkeys(covers):
    stem = hashlib.sha1(source.encode()).hexdigest()[:10]
    variants = {}
    with Image.open(ROOT / source) as original:
        for width in (480, 960):
            image = original.convert('RGB')
            image.thumbnail((width, 10000), Image.Resampling.LANCZOS)
            output = previews / f'{stem}-{width}.webp'
            image.save(output, 'WEBP', quality=78, method=6)
            variants[str(width)] = {'src': output.relative_to(ROOT).as_posix(), 'width':image.width, 'height':image.height}
    manifest[source] = variants
(DATA / 'gallery_previews.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
print(f'{len(manifest)} covers generated; original album images preserved.')
