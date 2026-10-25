#!/usr/bin/env python3
"""Small, dependency-free colour-distance helpers for candidate routing.

The fast router must be able to reject near-duplicate palette cards without
loading the optional SCI audit stack.  The implementation uses CIE76 in
CIELAB, with a symmetric mean-nearest-colour distance for palette pairs.  It
is a screening signal for candidate diversity, not a substitute for the
publication audit performed by :mod:`sci_palette_bridge`.
"""

from __future__ import annotations

import math
from typing import Iterable, Mapping, Sequence


DEFAULT_MIN_DELTA_E = 18.0


def _srgb_to_linear(channel: float) -> float:
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def hex_to_lab(value: str) -> tuple[float, float, float]:
    """Convert a six-digit sRGB hex colour to CIELAB (D65).

    The function intentionally accepts only full six-digit colours.  Palette
    registry entries use that format, and rejecting malformed values is safer
    than silently inventing a candidate-distance result.
    """

    text = str(value).strip().lstrip("#")
    if len(text) != 6:
        raise ValueError(f"expected a six-digit hex colour, got {value!r}")
    try:
        red, green, blue = (int(text[index : index + 2], 16) / 255.0 for index in (0, 2, 4))
    except ValueError as exc:
        raise ValueError(f"invalid hex colour {value!r}") from exc
    red, green, blue = (_srgb_to_linear(channel) for channel in (red, green, blue))

    # sRGB/D65 to XYZ, scaled to the conventional 0..100 range.
    x = (0.4124564 * red + 0.3575761 * green + 0.1804375 * blue) * 100.0
    y = (0.2126729 * red + 0.7151522 * green + 0.0721750 * blue) * 100.0
    z = (0.0193339 * red + 0.1191920 * green + 0.9503041 * blue) * 100.0
    reference = (95.047, 100.0, 108.883)

    def f(ratio: float) -> float:
        delta = 6.0 / 29.0
        return ratio ** (1.0 / 3.0) if ratio > delta**3 else ratio / (3.0 * delta**2) + 4.0 / 29.0

    fx, fy, fz = (f(value / ref) for value, ref in zip((x, y, z), reference))
    return (116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz))


def delta_e76(left: str, right: str) -> float:
    """Return Euclidean CIE76 distance between two hex colours."""

    first = hex_to_lab(left)
    second = hex_to_lab(right)
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(first, second)))


def _mean_nearest(left: Sequence[str], right: Sequence[str]) -> float:
    if not left or not right:
        return 100.0
    return sum(min(delta_e76(colour, other) for other in right) for colour in left) / len(left)


def palette_distance(left: Sequence[str], right: Sequence[str]) -> float:
    """Return a symmetric mean-nearest CIE76 distance for two palettes."""

    return (_mean_nearest(left, right) + _mean_nearest(right, left)) / 2.0


def palette_family(palette_id: str, registry: Mapping[str, Mapping[str, object]]) -> str:
    """Return a registry family, with the palette ID as a safe fallback."""

    palette = registry.get(palette_id, {})
    return str(palette.get("family") or palette_id)


def palette_colors(palette_id: str, registry: Mapping[str, Mapping[str, object]]) -> list[str]:
    palette = registry.get(palette_id, {})
    values = palette.get("colors", [])
    return [str(value) for value in values if value]


def candidate_distance(
    palette_id: str,
    selected_ids: Iterable[str],
    registry: Mapping[str, Mapping[str, object]],
) -> float:
    """Return the nearest selected-palette distance for one candidate."""

    colours = palette_colors(palette_id, registry)
    selected = [palette_colors(item, registry) for item in selected_ids]
    selected = [values for values in selected if values]
    if not colours or not selected:
        return 100.0
    return min(palette_distance(colours, values) for values in selected)
