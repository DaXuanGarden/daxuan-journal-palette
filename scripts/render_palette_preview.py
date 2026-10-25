#!/usr/bin/env python3
"""Render a small, dependency-light palette QA card.

The preview is intentionally figure-agnostic: it shows the same swatches under
normal vision, grayscale, two common CVD simulations, and a reduced-size panel.
It is a screening aid, not a journal or accessibility certification.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:  # pragma: no cover - exercised by the CLI environment
    raise SystemExit("Pillow is required: pip install Pillow") from exc


ROOT = Path(__file__).resolve().parents[1]

# Matrices are compact sRGB screening transforms. The final figure still needs
# review at its intended size and export format.
CVD_MATRICES = {
    "protanopia": ((0.56667, 0.43333, 0.0), (0.55833, 0.44167, 0.0), (0.0, 0.24167, 0.75833)),
    "deuteranopia": ((0.625, 0.375, 0.0), (0.7, 0.3, 0.0), (0.0, 0.3, 0.7)),
}


def parse_hex(value: str) -> tuple[int, int, int]:
    token = value.strip().lstrip("#")
    if len(token) != 6 or any(char not in "0123456789abcdefABCDEF" for char in token):
        raise ValueError(f"invalid HEX colour: {value!r}")
    return tuple(int(token[index : index + 2], 16) for index in (0, 2, 4))


def as_hex(rgb: Iterable[int]) -> str:
    return "#" + "".join(f"{max(0, min(255, int(value))):02X}" for value in rgb)


def transform(rgb: tuple[int, int, int], matrix: tuple[tuple[float, ...], ...]) -> tuple[int, int, int]:
    return tuple(round(sum(weight * channel for weight, channel in zip(row, rgb))) for row in matrix)  # type: ignore[return-value]


def luminance(rgb: tuple[int, int, int]) -> int:
    return round(0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2])


def render_preview(
    colours: list[str],
    output_dir: str | Path,
    *,
    title: str = "Palette preview",
    width: int = 1200,
    height: int = 720,
) -> dict:
    if not colours:
        raise ValueError("at least one colour is required")
    rgb_values = [parse_hex(value) for value in colours]
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()
    panel_w = width // 3
    panel_h = height // 2
    panels = {
        "normal": rgb_values,
        "grayscale": [(luminance(rgb),) * 3 for rgb in rgb_values],
        "protanopia": [transform(rgb, CVD_MATRICES["protanopia"]) for rgb in rgb_values],
        "deuteranopia": [transform(rgb, CVD_MATRICES["deuteranopia"]) for rgb in rgb_values],
    }
    # The target-size panel is a reduced-size proof, not a second colour transform.
    panel_order = ["normal", "grayscale", "protanopia", "deuteranopia", "target-size"]
    swatch_gap = 8
    for panel_index, panel_name in enumerate(panel_order):
        # With three columns the canvas remains readable while the fifth panel
        # gives the author a visible small-size proof before final export.
        px = (panel_index % 3) * panel_w
        py = (panel_index // 3) * panel_h
        draw.rectangle((px, py, px + panel_w - 1, py + panel_h - 1), outline="#D8D8D8")
        draw.text((px + 18, py + 14), f"{title} · {panel_name}", fill="#222222", font=font)
        values = panels["normal"] if panel_name == "target-size" else panels[panel_name]
        available_w = panel_w - 36
        swatch_w = max(18, (available_w - swatch_gap * (len(values) - 1)) // len(values))
        top = py + (78 if panel_name == "target-size" else 58)
        bottom = py + (panel_h - 56 if panel_name == "target-size" else panel_h - 34)
        if panel_name == "target-size":
            top += 8
            bottom = top + max(22, (bottom - top) // 2)
        for index, rgb in enumerate(values):
            left = px + 18 + index * (swatch_w + swatch_gap)
            right = min(px + panel_w - 18, left + swatch_w)
            draw.rectangle((left, top, right, bottom), fill=tuple(rgb), outline="#777777")
            label = colours[index].upper()
            draw.text((left, bottom + 9), label, fill="#222222", font=font)
    png_path = out / "palette_preview.png"
    canvas.save(png_path, dpi=(300, 300))
    manifest = {
        "schema_version": "1.0",
        "title": title,
        "colors": [value.upper() if value.startswith("#") else f"#{value.upper()}" for value in colours],
        "panels": panel_order,
        "target_size_proof": "2x2 swatch card; inspect again at final figure dimensions",
        "audit_status": "screening_only",
        "provenance": {
            "script": "scripts/render_palette_preview.py",
            "rule": "same semantic colors across normal, grayscale and CVD panels",
        },
    }
    json_path = out / "palette_preview.json"
    json_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["png"] = str(png_path)
    manifest["json"] = str(json_path)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--colors", nargs="+", required=True, help="HEX colours in semantic display order")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--title", default="Palette preview")
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--height", type=int, default=720)
    args = parser.parse_args()
    result = render_preview(args.colors, args.output_dir, title=args.title, width=args.width, height=args.height)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
