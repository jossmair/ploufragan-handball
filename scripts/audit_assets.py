"""Inventory public PHB assets and flag files with no generated-site reference."""

import argparse
import json
from pathlib import Path
import re

from seo_audit import FILES, ROOT, Page, local_path


TEXT_SOURCES = [ROOT / "build.py", ROOT / "assets" / "site.js"]
TEXT_SOURCES += sorted((ROOT / "data").glob("*.json"))
ASSET_PATTERN = re.compile(r"(?:\.\./)*assets/[A-Za-z0-9_./-]+")
CSS_URL_PATTERN = re.compile(r"url\(\s*['\"]?([^)\"']+)")


def human_size(size):
    units = ("o", "Ko", "Mo", "Go")
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "o" else f"{int(value)} o"
        value /= 1024


def referenced_assets():
    used = set()
    for file in FILES:
        page = Page()
        page.feed(file.read_text(encoding="utf-8"))
        references = list(page.references)
        references += [("resource", page.meta.get(name, "")) for name in ("og:image", "twitter:image")]
        for _, url in references:
            target = local_path(file, url)
            if target and target.is_file() and ROOT / "assets" in target.parents:
                used.add(target)
    for css in (ROOT / "assets").rglob("*.css"):
        for match in CSS_URL_PATTERN.finditer(css.read_text(encoding="utf-8")):
            target = local_path(css, match.group(1))
            if target and target.is_file() and ROOT / "assets" in target.parents:
                used.add(target)
    manifest = ROOT / "manifest.webmanifest"
    if manifest.is_file():
        for icon in json.loads(manifest.read_text(encoding="utf-8")).get("icons", []):
            target = local_path(manifest, icon.get("src", ""))
            if target and target.is_file() and ROOT / "assets" in target.parents:
                used.add(target)
    for source in TEXT_SOURCES:
        if not source.is_file():
            continue
        for value in ASSET_PATTERN.findall(source.read_text(encoding="utf-8")):
            normalized = value.removeprefix("../").split("?", 1)[0]
            target = (ROOT / normalized).resolve()
            if target.is_file() and ROOT / "assets" in target.parents:
                used.add(target)
    return used


def build_report():
    assets = sorted((item for item in (ROOT / "assets").rglob("*") if item.is_file()), key=lambda item: item.stat().st_size, reverse=True)
    used = referenced_assets()
    candidates = [item for item in assets if item.resolve() not in used]
    archived = sorted((item for item in (ROOT / "archive").rglob("*") if item.is_file()), key=lambda item: item.stat().st_size, reverse=True) if (ROOT / "archive").is_dir() else []
    lines = [
        "# Audit des assets",
        "",
        f"- Assets publics : **{len(assets)} fichiers, {human_size(sum(item.stat().st_size for item in assets))}**.",
        f"- Référencés par le site généré ou ses sources : **{len(used)}**.",
        f"- À examiner manuellement : **{len(candidates)}**.",
        f"- Sources graphiques archivées hors publication : **{len(archived)} fichiers, {human_size(sum(item.stat().st_size for item in archived))}**.",
        "",
        "## 20 plus gros assets publics",
        "",
        "| Fichier | Poids |",
        "|---|---:|",
    ]
    lines.extend(f"| `{item.relative_to(ROOT).as_posix()}` | {human_size(item.stat().st_size)} |" for item in assets[:20])
    lines += ["", "## Assets potentiellement inutilisés", "", "Une absence de référence statique ne suffit pas à autoriser une suppression : les sources graphiques et chemins construits dynamiquement doivent être vérifiés manuellement.", ""]
    if candidates:
        lines.extend(f"- `{item.relative_to(ROOT).as_posix()}` — {human_size(item.stat().st_size)}" for item in candidates)
    else:
        lines.append("- Aucun.")
    lines += ["", "## Sources sorties du site public", ""]
    if archived:
        lines.extend(f"- `{item.relative_to(ROOT).as_posix()}` — {human_size(item.stat().st_size)}" for item in archived)
    else:
        lines.append("- Aucune.")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = build_report()
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
