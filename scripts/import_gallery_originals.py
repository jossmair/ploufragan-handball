"""Importe les originaux Piwigo d'une galerie depuis les archives fournies."""

import argparse
import json
import re
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "galeries.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("archives", nargs="+", type=Path)
    parser.add_argument("--album", default="seniors-1-pays-de-dinan-2026")
    args = parser.parse_args()

    galleries = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    album = next(item for item in galleries if item["slug"] == args.album)
    output = ROOT / "assets" / "galeries" / args.album / "originals"
    output.mkdir(parents=True, exist_ok=True)

    members = {}
    archives = []
    for archive_path in args.archives:
        archive = zipfile.ZipFile(archive_path)
        archives.append(archive)
        for info in archive.infolist():
            match = re.match(r"(\d+)_", Path(info.filename).name)
            if match and not info.is_dir():
                members[int(match.group(1))] = (archive, info)

    imported = 0
    total_size = 0
    try:
        for index, photo in enumerate(album["photos"], start=1):
            match = re.search(r"[?&]id=(\d+)", photo["original_url"])
            if not match:
                raise ValueError(f"Identifiant Piwigo absent pour la photo {index}")
            photo_id = int(match.group(1))
            if photo_id not in members:
                raise FileNotFoundError(f"Original Piwigo {photo_id} absent des archives")
            archive, info = members[photo_id]
            suffix = Path(info.filename).suffix.lower()
            filename = "animation.gif" if suffix == ".gif" else f"photo-{index}.jpg"
            destination = output / filename
            with archive.open(info) as source, destination.open("wb") as target:
                shutil.copyfileobj(source, target)
            photo["original_url"] = f"/assets/galeries/{args.album}/originals/{filename}"
            photo["original_name"] = (
                "PHB-SM1-Pays-de-Dinan-2026-animation.gif"
                if suffix == ".gif"
                else f"PHB-SM1-Pays-de-Dinan-2026-photo-{index:03d}.jpg"
            )
            imported += 1
            total_size += destination.stat().st_size
    finally:
        for archive in archives:
            archive.close()

    DATA_PATH.write_text(
        json.dumps(galleries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"{imported} originaux importés ({total_size:,} octets) dans {output}")


if __name__ == "__main__":
    main()
