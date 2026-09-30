"""Inventory public PHB assets and monitor the deployed site payload."""

import argparse
import json
from pathlib import Path
import re
import sys

try:
    from .seo_audit import FILES, ROOT, Page, local_path
except ImportError:
    from seo_audit import FILES, ROOT, Page, local_path


DEFAULT_MAX_SITE_BYTES = 400 * 1024 * 1024
TEXT_SOURCES = [ROOT / "build.py", ROOT / "assets" / "site.js"]
TEXT_SOURCES += sorted((ROOT / "data").glob("*.json"))
ASSET_PATTERN = re.compile(r"(?:\.\./)*assets/[A-Za-z0-9_./-]+")
CSS_URL_PATTERN = re.compile(r"url\(\s*['\"]?([^)\"']+)")
PUBLIC_ROOT_PATTERNS = ("*.html", "*.txt", "*.xml", "*.webmanifest", "CNAME", ".nojekyll")
PUBLIC_DIRECTORIES = ("articles", "galeries", "assets")


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


def files_in(directory):
    if not directory.is_dir():
        return []
    return [item for item in directory.rglob("*") if item.is_file()]


def public_site_files(site_root=None):
    if site_root:
        resolved = site_root if site_root.is_absolute() else ROOT / site_root
        if not resolved.is_dir():
            raise FileNotFoundError(f"Dossier de site publié introuvable : {resolved}")
        return files_in(resolved), f"dossier `{resolved.name}`"

    public = set()
    for pattern in PUBLIC_ROOT_PATTERNS:
        public.update(item for item in ROOT.glob(pattern) if item.is_file())
    for directory_name in PUBLIC_DIRECTORIES:
        public.update(files_in(ROOT / directory_name))
    return sorted(public), "simulation du paquet GitHub Pages"


def gallery_rows():
    rows = []
    senior_root = ROOT / "assets" / "galeries"
    if senior_root.is_dir():
        for gallery in sorted(item for item in senior_root.iterdir() if item.is_dir()):
            originals = files_in(gallery / "originals")
            thumbs = files_in(gallery / "thumbs")
            excluded = {item.resolve() for item in originals + thumbs}
            display = [item for item in files_in(gallery) if item.resolve() not in excluded]
            rows.append((gallery.name, display, thumbs, originals))

    for gallery in sorted((ROOT / "assets").glob("*/gallery")):
        thumbs = files_in(gallery / "thumbs")
        thumb_paths = {item.resolve() for item in thumbs}
        display = [item for item in files_in(gallery) if item.resolve() not in thumb_paths]
        rows.append((gallery.parent.name, display, thumbs, []))
    return rows


def count_and_size(files):
    return len(files), sum(item.stat().st_size for item in files)


def build_report(site_root=None, max_site_bytes=DEFAULT_MAX_SITE_BYTES):
    assets = sorted(files_in(ROOT / "assets"), key=lambda item: item.stat().st_size, reverse=True)
    used = referenced_assets()
    candidates = [item for item in assets if item.resolve() not in used]
    archived = sorted(files_in(ROOT / "archive"), key=lambda item: item.stat().st_size, reverse=True)
    site_files, site_source = public_site_files(site_root)
    site_size = sum(item.stat().st_size for item in site_files)
    remaining = max_site_bytes - site_size
    status = "OK" if remaining >= 0 else "DÉPASSÉ"
    gallery_data = gallery_rows()
    all_originals = [item for _, _, _, originals in gallery_data for item in originals]

    lines = [
        "# Audit des assets",
        "",
        "## Poids du site publié",
        "",
        f"- Source du calcul : **{site_source}**.",
        f"- Paquet public : **{len(site_files)} fichiers, {human_size(site_size)}**.",
        f"- Plafond surveillé : **{human_size(max_site_bytes)}** — **{status}**.",
        f"- Marge restante : **{human_size(max(remaining, 0))}**.",
        "",
        "## Galeries et originaux HD",
        "",
        "| Galerie | Images web | Miniatures | Originaux HD | Total |",
        "|---|---:|---:|---:|---:|",
    ]
    for label, display, thumbs, originals in gallery_data:
        display_count, display_size = count_and_size(display)
        thumb_count, thumb_size = count_and_size(thumbs)
        original_count, original_size = count_and_size(originals)
        total_size = display_size + thumb_size + original_size
        lines.append(
            f"| `{label}` | {display_count} · {human_size(display_size)} | "
            f"{thumb_count} · {human_size(thumb_size)} | {original_count} · {human_size(original_size)} | "
            f"{human_size(total_size)} |"
        )
    original_count, original_size = count_and_size(all_originals)
    lines += [
        "",
        f"- Total des originaux HD publiés : **{original_count} fichiers, {human_size(original_size)}**.",
        "- Les cartes du hub Galerie réutilisent ces fichiers existants ; elles ne créent aucune copie.",
        "",
        "## Inventaire général",
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
    lines += [
        "",
        "## Assets potentiellement inutilisés",
        "",
        "Une absence de référence statique ne suffit pas à autoriser une suppression : les sources graphiques et chemins construits dynamiquement doivent être vérifiés manuellement.",
        "",
    ]
    if candidates:
        lines.extend(f"- `{item.relative_to(ROOT).as_posix()}` — {human_size(item.stat().st_size)}" for item in candidates)
    else:
        lines.append("- Aucun.")
    lines += ["", "## Sources sorties du site public", ""]
    if archived:
        lines.extend(f"- `{item.relative_to(ROOT).as_posix()}` — {human_size(item.stat().st_size)}" for item in archived)
    else:
        lines.append("- Aucune.")
    return "\n".join(lines) + "\n", site_size <= max_site_bytes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--site-root", type=Path)
    parser.add_argument("--max-site-bytes", type=int, default=DEFAULT_MAX_SITE_BYTES)
    args = parser.parse_args()
    report, within_budget = build_report(args.site_root, args.max_site_bytes)
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(report, encoding="utf-8")
    print(report)
    if not within_budget:
        print("Le paquet public dépasse le plafond configuré.", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
