"""Normalize partner artwork onto a safe white canvas without cropping content."""
from pathlib import Path

from PIL import Image, ImageChops, ImageFilter


for path in sorted(Path("assets/partenaires").glob("*.webp")):
    source = Image.open(path).convert("RGB")
    white = Image.new("RGB", source.size, "white")
    difference = ImageChops.difference(source, white).convert("L")
    mask = difference.point(lambda value: 255 if value > 14 else 0).filter(ImageFilter.MaxFilter(3))
    box = mask.getbbox()
    if box:
        left, top, right, bottom = box
        left = max(0, left - 2)
        top = max(0, top - 2)
        right = min(source.width, right + 2)
        bottom = min(source.height, bottom + 2)
        source = source.crop((left, top, right, bottom))

    # Keep a slim safety edge so the artwork can use the full white tile.
    # The previous 12% inset made already-small square marks look like thumbnails.
    padding_x = max(3, round(source.width * 0.035))
    padding_y = max(3, round(source.height * 0.035))
    canvas = Image.new("RGB", (source.width + padding_x * 2, source.height + padding_y * 2), "white")
    canvas.paste(source, (padding_x, padding_y))
    canvas.save(path, "WEBP", quality=94, method=6)
