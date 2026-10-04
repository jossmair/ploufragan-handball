"""Guard displayed image formats, dimensions and gallery loading at each build."""
from pathlib import Path
import sys

from seo_audit import FILES, ROOT, Page, local_path

# This existing animation is preserved; new heavy GIFs should use video instead.
ANIMATED_EXCEPTIONS = {"assets/galeries/seniors-1-pays-de-dinan-2026/animation.gif"}


def main():
    errors = set()
    checked = set()
    for file in FILES:
        page = Page()
        page.feed(file.read_text(encoding="utf-8"))
        for image in page.images:
            src = image.get("src")
            if not src:
                continue  # Dynamic lightbox images have no resource until opened.
            target = local_path(file, src)
            if not target or not target.is_file():
                continue  # Missing resources are already rejected by check_site.
            relative = target.relative_to(ROOT).as_posix()
            checked.add(relative)
            try:
                if int(image.get("width", 0)) <= 0 or int(image.get("height", 0)) <= 0:
                    raise ValueError
            except ValueError:
                errors.add(f"{file.name}: missing/invalid dimensions: {src}")
            if relative in ANIMATED_EXCEPTIONS:
                continue
            size = target.stat().st_size
            if target.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"} and size > 300_000:
                errors.add(f"Heavy raster must use WebP/AVIF or video: {relative} ({size} bytes)")
            if target.suffix.lower() in {".webp", ".avif"} and size > 600_000:
                errors.add(f"Displayed image exceeds 600 KB: {relative} ({size} bytes)")
            gallery = "/gallery/" in relative or "/galeries/" in relative or "/thumbs/" in relative
            # The first visible album image remains eager to preserve its LCP.
            if gallery and image.get("loading") != "lazy" and image.get("fetchpriority") != "high":
                errors.add(f"{file.name}: gallery image must load lazily: {src}")
    for error in sorted(errors):
        print("ERROR", error)
    print(f"Media guard: {len(checked)} displayed image files, {len(errors)} errors.")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
