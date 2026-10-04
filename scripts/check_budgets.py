"""Budgets de taille stables pour détecter les régressions en production."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

BUDGETS = {
    "CSS navigation": (ASSETS / "navigation.css", 6_000),
    "JavaScript navigation": (ASSETS / "navigation.js", 4_000),
    "Vidéo Galerie": (ASSETS / "videos" / "galerie-animation.mp4", 500_000),
    "CSS commun": (ASSETS / "site.min.css", 166_000),
    "JavaScript commun": (ASSETS / "site.min.js", 24_000),
    "Vidéo accueil": (ASSETS / "blog" / "intro.mp4", 3_200_000),
    "Vidéo Résultats": (ASSETS / "blog" / "blog-logo-orbit.mp4", 5_700_000),
    "Vidéo Blog": (ASSETS / "blog" / "blog-ploufy-reading.mp4", 2_200_000),
    "Vidéo Entraînements": (ASSETS / "videos" / "entrainements-animation.mp4", 4_500_000),
    "Vidéo Boutique": (ASSETS / "videos" / "boutique-animation.mp4", 2_100_000),
}
# Added the 194-photo summer camp album and eight locally hosted videos.
TOTAL_ASSETS_BUDGET = 181_000_000
GALLERY_ORIGINALS = ASSETS / "galeries" / "seniors-1-pays-de-dinan-2026" / "originals"
GALLERY_ORIGINALS_BUDGET = 330_000_000


def main():
    errors = []
    for label, (path, maximum) in BUDGETS.items():
        if not path.is_file():
            errors.append(f"{label}: fichier absent ({path.relative_to(ROOT)})")
            continue
        size = path.stat().st_size
        print(f"{label}: {size:,} / {maximum:,} octets")
        if size > maximum:
            errors.append(f"{label}: budget dépassé de {size - maximum:,} octets")

    total = sum(
        path.stat().st_size for path in ASSETS.rglob("*")
        if path.is_file() and GALLERY_ORIGINALS not in path.parents
    )
    print(f"Assets publics: {total:,} / {TOTAL_ASSETS_BUDGET:,} octets")
    if total > TOTAL_ASSETS_BUDGET:
        errors.append(f"Assets publics: budget dépassé de {total - TOTAL_ASSETS_BUDGET:,} octets")

    originals = list(GALLERY_ORIGINALS.glob("*")) if GALLERY_ORIGINALS.is_dir() else []
    originals_size = sum(path.stat().st_size for path in originals if path.is_file())
    print(f"Originaux galerie: {len(originals)} fichiers, {originals_size:,} / {GALLERY_ORIGINALS_BUDGET:,} octets")
    if len(originals) != 164:
        errors.append(f"Originaux galerie: 164 fichiers attendus, {len(originals)} trouvés")
    if originals_size > GALLERY_ORIGINALS_BUDGET:
        errors.append(f"Originaux galerie: budget dépassé de {originals_size - GALLERY_ORIGINALS_BUDGET:,} octets")

    for error in errors:
        print("ERROR", error)
    if not errors:
        print("PASS : budgets de poids respectés")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
