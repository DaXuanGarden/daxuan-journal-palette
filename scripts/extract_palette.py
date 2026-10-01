#!/usr/bin/env python3
"""Extract a reproducible candidate palette from one local image.

Pillow is intentionally optional. The output is a candidate palette with
provenance, not a claim that the image-derived colors are publication-ready.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def rgb_hex(values: tuple[float, float, float]) -> str:
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(value))) for value in values)


def nearest(pixel: tuple[int, int, int], centers: list[tuple[float, float, float]]) -> int:
    return min(
        range(len(centers)),
        key=lambda index: sum((pixel[channel] - centers[index][channel]) ** 2 for channel in range(3)),
    )


def extract_pixels(image_path: Path, max_side: int) -> list[tuple[int, int, int]]:
    try:
        from PIL import Image
    except ImportError as error:
        raise RuntimeError("Pillow is required for image extraction; install it or provide manual colors") from error
    with Image.open(image_path) as image:
        image = image.convert("RGB")
        image.thumbnail((max_side, max_side))
        pixels = image.get_flattened_data() if hasattr(image, "get_flattened_data") else image.getdata()
        return list(pixels)


def kmeans(pixels: list[tuple[int, int, int]], count: int, seed: int, iterations: int = 24) -> list[dict]:
    if not pixels:
        raise ValueError("image contains no pixels")
    rng = random.Random(seed)
    centers = [tuple(float(channel) for channel in pixels[index]) for index in rng.sample(range(len(pixels)), min(count, len(pixels)))]
    while len(centers) < count:
        centers.append(centers[-1])
    assignments = [0] * len(pixels)
    for _ in range(iterations):
        changed = False
        for index, pixel in enumerate(pixels):
            cluster = nearest(pixel, centers)
            if assignments[index] != cluster:
                assignments[index] = cluster
                changed = True
        sums = [[0.0, 0.0, 0.0, 0] for _ in centers]
        for pixel, cluster in zip(pixels, assignments):
            sums[cluster][0] += pixel[0]
            sums[cluster][1] += pixel[1]
            sums[cluster][2] += pixel[2]
            sums[cluster][3] += 1
        for index, (red, green, blue, weight) in enumerate(sums):
            if weight:
                centers[index] = (red / weight, green / weight, blue / weight)
        if not changed:
            break
    clusters = []
    for index, center in enumerate(centers):
        weight = assignments.count(index)
        if weight:
            clusters.append({"hex": rgb_hex(center), "share": round(weight / len(pixels), 6), "pixels": weight})
    clusters.sort(key=lambda item: (-item["pixels"], item["hex"]))
    return clusters


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", type=Path)
    parser.add_argument("--count", type=int, default=5, choices=range(3, 9), metavar="3-8")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-side", type=int, default=120)
    parser.add_argument("--source-url", default="")
    parser.add_argument("--source-title", default="")
    parser.add_argument("--rights", default="unknown")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    pixels = extract_pixels(args.image, args.max_side)
    colors = kmeans(pixels, args.count, args.seed)
    payload = {
        "schema_version": "1.0.0",
        "image": str(args.image),
        "source_url": args.source_url,
        "source_title": args.source_title,
        "rights": args.rights,
        "extraction": {
            "method": "rgb-kmeans",
            "library": "Pillow",
            "seed": args.seed,
            "max_side": args.max_side,
            "pixel_count": len(pixels),
        },
        "colors": colors,
        "status": "candidate-only",
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
