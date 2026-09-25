"""Stable size budgets intended to catch large production regressions."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

BUDGETS = {
    "CSS commun": (ASSETS / "site.css", 160_000),
    "JavaScript commun": (ASSETS / "site.js", 30_000),
    "Vidéo accueil": (ASSETS / "blog" / "intro.mp4", 3_200_000),
    "Vidéo Résultats": (ASSETS / "blog" / "blog-logo-orbit.mp4", 5_700_000),
    "Vidéo Blog": (ASSETS / "blog" / "blog-ploufy-reading.mp4", 2_200_000),
    "Vidéo Entraînements": (ASSETS / "videos" / "entrainements-animation.mp4", 4_500_000),
}
TOTAL_ASSETS_BUDGET = 38_000_000


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
    total = sum(path.stat().st_size for path in ASSETS.rglob("*") if path.is_file())
    print(f"Assets publics: {total:,} / {TOTAL_ASSETS_BUDGET:,} octets")
    if total > TOTAL_ASSETS_BUDGET:
        errors.append(f"Assets publics: budget dépassé de {total - TOTAL_ASSETS_BUDGET:,} octets")
    for error in errors:
        print("ERROR", error)
    if not errors:
        print("PASS : budgets de poids respectés")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
