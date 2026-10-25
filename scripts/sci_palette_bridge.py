#!/usr/bin/env python3
"""Bridge Daxuan Journal Palette to the local sci-color-palettes library.

The two skills keep different responsibilities:

* Daxuan supplies visual families, semantic roles and figure-specific layout.
* sci-color-palettes supplies application gates and accessibility diagnostics.

This adapter deliberately does not copy the 184 SCI colours into the Daxuan
registry. It loads the local SCI package by an explicit path, returns a small
auditable recommendation, and preserves the original ramp order.
"""

from __future__ import annotations

import argparse
import colorsys
import importlib
import json
import os
import sys
from pathlib import Path
from typing import Any


# No developer-specific path is embedded.  Public installs can use the
# environment variable or place sibling checkouts next to this Skill.
DEFAULT_SCI_ROOT: Path | None = None
FIELD_ALIASES = {
    "clinical": "clinical",
    "临床": "clinical",
    "临床研究": "clinical",
    "survival": "clinical",
    "生存": "clinical",
    "database": "database",
    "数据库": "database",
    "队列": "database",
    "registry": "database",
    "cohort": "database",
    "多中心": "database",
    "basic": "basic",
    "基础": "basic",
    "基础科研": "basic",
    "omics": "basic",
    "组学": "basic",
    "gwas": "basic",
    "general": "general",
    "通用": "general",
    "跨学科": "general",
}


def _candidate_sci_roots(root: str | os.PathLike[str] | None = None) -> list[Path]:
    """Return explicit, environment and sibling checkout candidates in order."""
    candidates: list[Path] = []
    if root:
        # An explicit path is an assertion. Do not silently use a different
        # checkout when the caller is testing or debugging a missing path.
        candidates.append(Path(root).expanduser())
    else:
        env_root = os.environ.get("SCI_COLOR_PALETTES_ROOT")
        if env_root:
            candidates.append(Path(env_root).expanduser())
        # Public installs may place both skills next to one another. This avoids
        # requiring the developer's /home path while keeping the local checkout fast.
        candidates.append(Path(__file__).resolve().parents[1].parent / "sci-color-palettes")
        if DEFAULT_SCI_ROOT is not None:
            candidates.append(DEFAULT_SCI_ROOT)
    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if str(resolved) not in seen:
            unique.append(resolved)
            seen.add(str(resolved))
    return unique


def discover_sci_root(root: str | os.PathLike[str] | None = None) -> Path | None:
    """Find a local sci-color-palettes checkout, or return ``None``.

    The SCI adapter is optional. Daxuan-only routing must remain usable when the
    external library is not installed, so discovery is explicit and side-effect
    free rather than raising during import.
    """
    for candidate in _candidate_sci_roots(root):
        if (candidate / "scripts" / "sci_palettes").is_dir():
            return candidate
    return None


def _sci_root(root: str | os.PathLike[str] | None = None) -> Path:
    discovered = discover_sci_root(root)
    return discovered if discovered is not None else _candidate_sci_roots(root)[0]


def load_sci(root: str | os.PathLike[str] | None = None):
    """Import sci_palettes without requiring a system-wide installation."""
    package_root = discover_sci_root(root)
    if package_root is None:
        requested = str(root) if root else "SCI_COLOR_PALETTES_ROOT"
        raise FileNotFoundError(
            "sci-color-palettes is optional but unavailable. Install or expose a "
            f"checkout via {requested} or SCI_COLOR_PALETTES_ROOT; "
            "Daxuan-only routing remains available."
        )
    scripts = package_root / "scripts"
    path = str(scripts)
    if path not in sys.path:
        sys.path.insert(0, path)
    return importlib.import_module("sci_palettes")


def normalize_field(field: str) -> str:
    key = str(field).strip().lower()
    if key in FIELD_ALIASES:
        return FIELD_ALIASES[key]
    raise ValueError(
        f"unknown SCI application field {field!r}; use clinical/database/basic/general"
    )


def infer_field(
    *,
    semantic: str | None = None,
    figure_type: str | None = None,
    groups: int | None = None,
    keywords: str = "",
) -> str:
    """Map a Daxuan figure request to the SCI application profile.

    This is a routing suggestion, not a claim about the scientific domain.
    Explicit ``semantic`` wins; otherwise density and keywords determine the
    profile. Diverging/sequential layers are handled separately below.
    """
    if semantic:
        return normalize_field(semantic)
    text = f"{figure_type or ''} {keywords}".lower()
    if any(term in text for term in ("临床", "clinical", "survival", "forest", "生存")):
        return "clinical"
    if any(term in text for term in ("数据库", "database", "cohort", "registry", "队列", "multi-cohort")):
        return "database"
    if groups is not None and groups >= 7:
        return "database"
    if any(term in text for term in ("gwas", "omics", "组学", "基础", "basic")):
        return "basic"
    return "general"


def _hue_family(hex_colour: str) -> str:
    """Coarse hue family used only for explicit user exclusions."""
    value = hex_colour.lstrip("#")
    if len(value) != 6:
        return "unknown"
    rgb = tuple(int(value[i : i + 2], 16) / 255 for i in (0, 2, 4))
    hue, saturation, _ = colorsys.rgb_to_hsv(*rgb)
    degrees = hue * 360
    if saturation < 0.12:
        return "neutral"
    if degrees < 35 or degrees >= 340:
        return "red"
    if degrees < 70:
        return "yellow"
    if degrees < 170:
        return "green"
    if degrees < 255:
        return "blue"
    if degrees < 300:
        return "purple"
    return "red"


def _contains_avoided_hue(colours: list[str], avoid_hues: list[str] | None) -> bool:
    if not avoid_hues:
        return False
    requested = {str(item).strip().lower() for item in avoid_hues}
    return any(_hue_family(colour) in requested for colour in colours)


def _record(sp, palette_id: str, field: str | None = None) -> dict[str, Any]:
    info = sp.get(palette_id)
    application = sp.applications(palette_id)
    result: dict[str, Any] = {
        "id": palette_id,
        "name_zh": info.get("name_zh"),
        "name_en": info.get("name_en"),
        "family": info.get("family", "anchor"),
        "base": info.get("base", palette_id),
        "derived": bool(info.get("derived", False)),
        "hex": list(sp.palette(palette_id)),
        "application": application,
        "audit": sp.check(palette_id),
    }
    if field:
        key = normalize_field(field)
        result["field"] = key
        result["score"] = application["scores"][key]
        result["fits"] = bool(application["fit"][key])
        result["metrics"] = application["metrics"]
    return result


def audit_hex(
    colours: list[str],
    *,
    sci_root: str | os.PathLike[str] | None = None,
    hard_pair_delta_e: float = 12.0,
) -> dict[str, Any]:
    """Audit an arbitrary Daxuan or extracted palette with SCI diagnostics.

    ``sci_palettes.check`` accepts registered palette ids. This small wrapper
    applies the same underlying colour maths to a user-supplied list, so a
    Daxuan recipe or an extracted card palette can be audited without adding it
    to the SCI registry.
    """
    if not colours:
        raise ValueError("colours must contain at least one hex colour")
    sp = load_sci(sci_root)
    values = list(sp.as_hex(colours))
    pairs = []
    for i, left in enumerate(values):
        for j in range(i + 1, len(values)):
            distance = float(sp.delta_e(left, values[j]))
            if distance < hard_pair_delta_e:
                pairs.append({"a": left, "b": values[j], "delta_e": round(distance, 1)})
    cvd = {}
    for label, matrix in (
        ("protanopia", sp.PROTANOPIA),
        ("deuteranopia", sp.DEUTERANOPIA),
        ("tritanopia", sp.TRITANOPIA),
        ("achromatopsia", sp.ACHROMATOPSIA),
    ):
        transformed = sp.simulate_cvd(values, matrix)
        distances = [
            float(sp.delta_e(transformed[i], transformed[j]))
            for i in range(len(transformed))
            for j in range(i + 1, len(transformed))
        ]
        cvd[label] = {
            "min_delta_e": round(min(distances), 1) if distances else None,
            "simulated_hex": transformed,
        }
    luminances = [float(sp.luminance(colour)) for colour in values]
    contrast = [float(sp.contrast_ratio(colour, "#FFFFFF")) for colour in values]
    return {
        "hex": values,
        "n": len(values),
        "hard_pairs": pairs,
        "cvd": cvd,
        "lightness_span": round(max(luminances) - min(luminances), 3),
        "contrast_on_white": {
            "min": round(min(contrast), 2),
            "max": round(max(contrast), 2),
            "aa_or_better": sum(value >= 4.5 for value in contrast),
            "aaa": sum(value >= 7.0 for value in contrast),
        },
        "notes": [
            "diagnostic only; evaluate the rendered figure at its final size",
            "pale members should remain fills/bands rather than small text",
        ],
    }


def categorical_recommendations(
    *,
    field: str | None = None,
    n: int = 5,
    require_fit: bool = True,
    candidate_limit: int | None = None,
    sci_root: str | os.PathLike[str] | None = None,
) -> dict[str, Any]:
    """Return SCI-ranked categorical ramps and a safe subset for ``n`` groups.

    ``candidate_limit`` widens the ranked pool while keeping ``selected_hex``
    at exactly ``n`` colours.  It is useful for visual card matching: the
    application gate remains upstream, while visual proximity can distinguish
    several publication-eligible candidates.
    """
    if n < 1:
        raise ValueError("n must be positive")
    profile = normalize_field(field or "general")
    sp = load_sci(sci_root)
    ranked = sp.suggest_for(profile, n=max(5, candidate_limit or n), require_fit=require_fit)
    if not ranked and require_fit:
        ranked = sp.suggest_for(profile, n=max(5, candidate_limit or n), require_fit=False)
    rows = []
    for item in ranked:
        pid = item["id"]
        record = _record(sp, pid, profile)
        record["selected_hex"] = list(sp.select(record["hex"], n))
        record["selected_audit"] = audit_hex(record["selected_hex"], sci_root=sci_root)
        record["selection_rule"] = "sci_palettes.select: preserve original ramp members"
        record["why"] = item.get("why", "")
        rows.append(record)
    return {
        "kind": "categorical",
        "field": profile,
        "n_groups": n,
        "require_fit": require_fit,
        "recommendations": rows,
        "provenance": {
            "adapter": "daxuan-journal-palette/scripts/sci_palette_bridge.py",
            "sci_root": str(_sci_root(sci_root)),
            "rule": "rank with sp.suggest_for; choose categorical members with sp.select",
        },
    }


def diverging_recommendations(
    *,
    n: int = 5,
    avoid_hues: list[str] | None = None,
    sci_root: str | os.PathLike[str] | None = None,
) -> dict[str, Any]:
    """Return diverging ramps for signed effects; index 3 is always the centre."""
    sp = load_sci(sci_root)
    ids = sp.family("diverging", sort_by_score=False)
    rows = []
    rejected = []
    for pid in ids:
        record = _record(sp, pid)
        colours = record["hex"]
        if len(colours) != 7:
            continue
        if _contains_avoided_hue(colours, avoid_hues):
            rejected.append({"id": pid, "reason": "contains avoided hue", "avoid_hues": avoid_hues})
            continue
        record["centre_index_zero_based"] = 3
        record["centre_hex"] = colours[3]
        record["selected_hex"] = list(sp.ramp(colours, n, keep_ends=True))
        record["selected_audit"] = audit_hex(record["selected_hex"], sci_root=sci_root)
        metrics = record["application"]["metrics"]
        record["rank_metrics"] = {
            "cvd_min_deuteranopia": record["audit"]["cvd"]["deuteranopia"]["min_delta_e"],
            "cvd5_deuteranopia": metrics["cvd5"],
            "min5_delta_e": metrics["min5"],
            "lightness_span8": metrics["span8"],
        }
        record["selection_rule"] = (
            "sci_palettes.ramp for continuous signed values; preserve the pale centre"
        )
        rows.append(record)
    rows.sort(
        key=lambda row: (
            -row["rank_metrics"]["cvd_min_deuteranopia"],
            -row["application"]["metrics"]["min5"],
            -row["application"]["metrics"]["span8"],
        )
    )
    return {
        "kind": "diverging",
        "n_values": n,
        "avoid_hues": avoid_hues or [],
        "recommendations": rows,
        "rejected_candidates": rejected,
        "provenance": {
            "adapter": "daxuan-journal-palette/scripts/sci_palette_bridge.py",
            "sci_root": str(_sci_root(sci_root)),
            "rule": "use sp.ramp for continuous data; centre is original index 3 of 7",
        },
    }


def circular_heatmap_recommendation(
    *,
    categories: int = 5,
    avoid_hues: list[str] | None = None,
    lightness_target: str = "balanced",
    chroma_target: str = "moderate",
    preserve_cues: list[str] | None = None,
    sci_root: str | os.PathLike[str] | None = None,
) -> dict[str, Any]:
    """Recommendation contract for the current 5-category circular heatmap.

    The outer category ring and signed LDSC heat ring are different semantic
    layers. They are kept as two self-contained ramps; colours are never mixed
    between the categorical and diverging scales.
    """
    categorical = categorical_recommendations(
        field="database", n=categories, require_fit=True, sci_root=sci_root
    )
    diverging = diverging_recommendations(
        n=7, avoid_hues=avoid_hues, sci_root=sci_root
    )
    return {
        "figure": "LDSC/Genova/HDL circular genetic-correlation heatmap",
        "background": "#FFFFFF",
        "preference_constraints": {
            "avoid_hues": avoid_hues or [],
            "lightness_target": lightness_target,
            "chroma_target": chroma_target,
            "preserve_cues": preserve_cues or [],
            "scope": "signed_ldsc_heat_ring",
        },
        "semantic_layers": [
            {
                "layer": "outcome_category_ring",
                "kind": "categorical",
                "field": "database",
                "reason": "five outcome categories need hue and pairwise separation",
                "recommendations": categorical["recommendations"][:5],
            },
            {
                "layer": "signed_ldsc_heat_ring",
                "kind": "diverging",
                "reason": "genetic correlation is signed and has a meaningful zero midpoint",
                "recommendations": diverging["recommendations"][:5],
                "rejected_candidates": diverging["rejected_candidates"],
            },
            {
                "layer": "validation_ring",
                "kind": "neutral-accent",
                "reason": "HDL/Genova validation is a status cue, so keep neutral gray plus one accent",
                "rule": "do not encode validation status using the heatmap scale",
            },
        ],
        "policy": [
            "one ramp per semantic layer; never splice members from unrelated ramps",
            "preserve category order across panels and legend",
            "pale SCI members are fills/bands only; use dark members for text and outlines",
            "retain labels/geometry/markers because color is not the sole evidence cue",
            "run sp.report or sp.check again after the final figure is rendered",
        ],
        "provenance": {
            "adapter": "daxuan-journal-palette/scripts/sci_palette_bridge.py",
            "sci_root": str(_sci_root(sci_root)),
            "daxuan_role": "style family, semantic mapping and final figure audit",
            "sci_role": "application ranking and accessibility diagnostics",
        },
    }


def circular_heatmap_fallback(
    *,
    categories: int = 5,
    reason: str = "sci-color-palettes unavailable",
    avoid_hues: list[str] | None = None,
    lightness_target: str = "balanced",
    chroma_target: str = "moderate",
    preserve_cues: list[str] | None = None,
) -> dict[str, Any]:
    """Return a usable Daxuan-only contract when the optional SCI library is absent."""
    return {
        "figure": "LDSC/Genova/HDL circular genetic-correlation heatmap",
        "background": "#FFFFFF",
        "sci_status": "unavailable",
        "fallback": "daxuan-atlas",
        "fallback_reason": reason,
        "preference_constraints": {
            "avoid_hues": avoid_hues or [],
            "lightness_target": lightness_target,
            "chroma_target": chroma_target,
            "preserve_cues": preserve_cues or [],
        },
        "semantic_layers": [
            {
                "layer": "outcome_category_ring",
                "kind": "categorical",
                "groups": categories,
                "palette_source": "daxuan-atlas",
            },
            {
                "layer": "signed_ldsc_heat_ring",
                "kind": "diverging",
                "palette_source": "daxuan-atlas",
                "zero_policy": "retain a central midpoint",
            },
            {
                "layer": "validation_ring",
                "kind": "neutral-accent",
                "rule": "neutral plus one accent; independent of the heatmap scale",
            },
        ],
        "policy": [
            "SCI diagnostics are unavailable; render the Daxuan preview and mark the audit as pending",
            "never splice members from unrelated ramps",
        ],
    }


def _main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--field", default="database", help="clinical/database/basic/general or Chinese alias")
    parser.add_argument("--groups", type=int, default=5)
    parser.add_argument("--figure", choices=("categorical", "diverging", "circular"), default="circular")
    parser.add_argument("--n-values", type=int, default=7)
    parser.add_argument("--avoid-hue", action="append", default=[], help="exclude a hue family from the signed heat ring; repeatable")
    parser.add_argument("--lightness-target", default="balanced", choices=("airy", "balanced", "ink-heavy"))
    parser.add_argument("--chroma-target", default="moderate", choices=("muted", "moderate", "colorful"))
    parser.add_argument("--preserve-cue", action="append", default=[], help="visual cue to retain, e.g. yellow/olive")
    parser.add_argument("--sci-root", type=Path)
    args = parser.parse_args()
    try:
        if args.figure == "categorical":
            result = categorical_recommendations(
                field=args.field, n=args.groups, sci_root=args.sci_root
            )
        elif args.figure == "diverging":
            result = diverging_recommendations(
                n=args.n_values, avoid_hues=args.avoid_hue, sci_root=args.sci_root
            )
        else:
            result = circular_heatmap_recommendation(
                categories=args.groups,
                avoid_hues=args.avoid_hue,
                lightness_target=args.lightness_target,
                chroma_target=args.chroma_target,
                preserve_cues=args.preserve_cue,
                sci_root=args.sci_root,
            )
    except FileNotFoundError as error:
        # The optional SCI package must never make a Daxuan-only command
        # unusable. Keep the returned object machine-readable for all figure
        # modes, while preserving a richer layer contract for circular figures.
        if args.figure == "circular":
            result = circular_heatmap_fallback(
                categories=args.groups,
                avoid_hues=args.avoid_hue,
                lightness_target=args.lightness_target,
                chroma_target=args.chroma_target,
                preserve_cues=args.preserve_cue,
                reason=str(error),
            )
        else:
            result = {
                "kind": args.figure,
                "sci_status": "unavailable",
                "fallback": "daxuan-atlas",
                "fallback_reason": str(error),
                "recommendations": [],
            }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _main()
