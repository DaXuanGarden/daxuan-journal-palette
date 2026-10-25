#!/usr/bin/env python3
"""Join visual card draws with SCI palette candidates.

The image-derived palette is treated as an inspiration cue.  The returned
SCI palette remains the publication candidate for the requested figure
semantic, so this tool never splices unrelated ramps into one scale.

Typical use::

    python3 scripts/joint_palette_draw.py \
      --cards-json cards/colorful_cards_v2_with_palettes.json \
      --figure all --groups 5 --draw-count 10 \
      --output-dir qa/joint_palette_draw --seed 20261025
"""

from __future__ import annotations

import argparse
import colorsys
import html
import importlib.util
import json
import random
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sci_palette_bridge import (  # noqa: E402
    audit_hex,
    categorical_recommendations,
    circular_heatmap_recommendation,
    diverging_recommendations,
    load_sci,
)


FIGURE_CHOICES = ("categorical", "heatmap", "circular", "all")


def _resolve_path(value: str | None, base: Path) -> Path | None:
    if not value:
        return None
    candidate = Path(value).expanduser()
    return candidate if candidate.is_absolute() else (base / candidate).resolve()


def _read_palette_file(path: Path | None) -> list[str]:
    if path is None or not path.is_file():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [str(item["hex"]).upper() for item in payload.get("colors", []) if item.get("hex")]


def load_cards(path: str | Path) -> list[dict[str, Any]]:
    """Load cards and normalize image/palette paths without downloading files."""
    manifest = Path(path).expanduser().resolve()
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    cards: list[dict[str, Any]] = []
    for index, raw in enumerate(payload.get("cards", []), start=1):
        card = dict(raw)
        card["card_id"] = card.get("card_id") or f"card-{index:02d}"
        palette = [str(value).upper() for value in card.get("extracted_hex", []) if value]
        palette_path = _resolve_path(card.get("palette_file"), manifest.parent)
        if not palette:
            palette = _read_palette_file(palette_path)
        if not palette:
            continue
        card["extracted_hex"] = palette
        image_path = _resolve_path(card.get("local_image") or card.get("image"), manifest.parent)
        card["local_image"] = str(image_path) if image_path else ""
        card["palette_file"] = str(palette_path) if palette_path else ""
        cards.append(card)
    if not cards:
        raise ValueError(f"no cards with extracted_hex/palette_file found in {manifest}")
    return cards


def _hue_label(colours: list[str]) -> str:
    """Return a short visual cue label for the card preview."""
    rgb = []
    for colour in colours:
        value = colour.lstrip("#")
        if len(value) != 6:
            continue
        rgb.append(tuple(int(value[i : i + 2], 16) / 255 for i in (0, 2, 4)))
    if not rgb:
        return "unclassified"
    hues = []
    for red, green, blue in rgb:
        hue, saturation, value = colorsys.rgb_to_hsv(red, green, blue)
        if saturation > 0.16 and value > 0.15:
            hues.append(hue * 360)
    if not hues:
        return "neutral / mineral"
    mean = sum(hues) / len(hues)
    labels = (
        (15, "red / cinnabar"),
        (45, "ochre / amber"),
        (75, "yellow / olive"),
        (165, "green / jade"),
        (205, "cyan / glacier"),
        (255, "blue / indigo"),
        (305, "violet / lilac"),
        (360, "rose / burgundy"),
    )
    for upper, label in labels:
        if mean < upper:
            return label
    return labels[-1][1]


def _palette_distance(sp, left: list[str], right: list[str]) -> float:
    """Mean nearest-colour CIE76 distance; lower means closer visual cue."""
    values = [float(sp.delta_e(a, b)) for a in left for b in right]
    if not values:
        return 100.0
    nearest = [min(float(sp.delta_e(a, b)) for b in right) for a in left]
    return sum(nearest) / len(nearest)


def _compact_categorical(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row["id"],
        "name_en": row.get("name_en"),
        "name_zh": row.get("name_zh"),
        "hex": list(row.get("hex", [])),
        "selected_hex": list(row.get("selected_hex", [])),
        "field": row.get("field"),
        "score": row.get("score"),
        "fits": row.get("fits"),
        "why": row.get("why", ""),
        "selected_audit": row.get("selected_audit", {}),
    }


def _compact_diverging(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row["id"],
        "name_en": row.get("name_en"),
        "name_zh": row.get("name_zh"),
        "hex": list(row.get("hex", [])),
        "selected_hex": list(row.get("selected_hex", [])),
        "centre_index_zero_based": row.get("centre_index_zero_based"),
        "centre_hex": row.get("centre_hex"),
        "rank_metrics": row.get("rank_metrics", {}),
        "selected_audit": row.get("selected_audit", {}),
    }


def _candidate_match(sp, art_hex: list[str], candidate_hex: list[str], quality_prior: float) -> dict[str, float]:
    distance = _palette_distance(sp, art_hex, candidate_hex)
    visual_match = max(0.0, 100.0 - min(100.0, distance))
    # Quality is a gate/order signal; once candidates come from the SCI
    # shortlist, visual proximity carries most of the matching weight so a
    # ten-card draw remains useful for comparison instead of collapsing to one
    # palette for every card.
    score = 0.05 * quality_prior + 0.95 * (visual_match / 100.0)
    return {
        "mean_delta_e": round(distance, 2),
        "visual_match": round(visual_match, 2),
        "joint_score": round(score, 4),
    }


def _rank_matches(
    cards: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    *,
    diverging: bool = False,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """Match each visual card to a semantic SCI candidate without mixing ramps."""
    if not candidates:
        return []
    rows = []
    for card in cards:
        ranked = []
        for rank, candidate in enumerate(candidates):
            selected = candidate.get("selected_hex") or candidate.get("hex", [])
            quality_prior = 1.0 - (rank / max(1, len(candidates) - 1))
            metrics = _candidate_match(load_sci(), card["extracted_hex"], selected, quality_prior)
            ranked.append((metrics["joint_score"], candidate, metrics))
        ranked.sort(key=lambda item: item[0], reverse=True)
        _, winner, metrics = ranked[0]
        rows.append({
            "card_id": card["card_id"],
            "visual_cue": _hue_label(card["extracted_hex"]),
            "sci_palette_id": winner["id"],
            "sci_hex": list(winner.get("selected_hex") or winner.get("hex", [])),
            "match": metrics,
            "rule": (
                "card palette is inspiration; use the intact SCI diverging ramp for signed values"
                if diverging
                else "card palette is inspiration; use the intact SCI categorical ramp for groups"
            ),
        })
    return rows[:limit]


def _make_sci_bundle(figure: str, groups: int) -> dict[str, Any]:
    try:
        categorical = categorical_recommendations(field="database", n=groups, require_fit=True, candidate_limit=12)
        diverging = diverging_recommendations(n=7)
    except FileNotFoundError as error:
        return {
            "categorical": [],
            "heatmap": [],
            "provenance": {
                "sci_status": "unavailable",
                "fallback": "daxuan-atlas",
                "fallback_reason": str(error),
                "validation": "SCI diagnostics unavailable; visual-card inspiration is retained without semantic SCI ranking",
            },
        }
    bundle: dict[str, Any] = {
        "categorical": [_compact_categorical(row) for row in categorical["recommendations"][:12]],
        "heatmap": [_compact_diverging(row) for row in diverging["recommendations"][:12]],
        "provenance": {
            "categorical_field": "database",
            "categorical_rule": "sp.suggest_for + sp.select; preserve original ramp members",
            "heatmap_rule": "diverging family + sp.ramp; centre remains index 3",
            "validation": "SCI diagnostics are evidence for screening, not journal certification",
        },
    }
    if figure in ("circular", "all"):
        try:
            circular = circular_heatmap_recommendation(categories=groups)
            bundle["circular"] = {
                "figure": circular["figure"],
                "background": circular["background"],
                "layers": circular["semantic_layers"],
                "policy": circular["policy"],
            }
        except FileNotFoundError as error:
            bundle["circular"] = {
                "sci_status": "unavailable",
                "fallback": "daxuan-atlas",
                "fallback_reason": str(error),
            }
    return bundle


def draw_joint(cards_path: str | Path, *, figure: str = "all", groups: int = 5, draw_count: int = 10, seed: int = 20261025) -> dict[str, Any]:
    cards = load_cards(cards_path)
    if draw_count < 1 or draw_count > len(cards):
        raise ValueError(f"draw_count must be between 1 and {len(cards)}")
    rng = random.Random(seed)
    drawn = rng.sample(cards, draw_count)
    for index, card in enumerate(drawn, start=1):
        card["draw_rank"] = index
        try:
            card["art_audit"] = audit_hex(card["extracted_hex"])
        except FileNotFoundError as error:
            card["art_audit"] = {
                "status": "unavailable",
                "reason": str(error),
                "hex": list(card["extracted_hex"]),
            }
        card["visual_cue"] = _hue_label(card["extracted_hex"])
    sci = _make_sci_bundle(figure, groups)
    matches: dict[str, list[dict[str, Any]]] = {}
    if figure in ("categorical", "circular", "all"):
        matches["categorical"] = _rank_matches(drawn, sci["categorical"], limit=draw_count)
    if figure in ("heatmap", "circular", "all"):
        matches["heatmap"] = _rank_matches(drawn, sci["heatmap"], diverging=True, limit=draw_count)
    return {
        "schema_version": "1.0.0",
        "mode": "joint-card-sci",
        "seed": seed,
        "draw_count": draw_count,
        "cards_json": str(Path(cards_path).expanduser().resolve()),
        "request": {"figure": figure, "groups": groups, "background": "white"},
        "cards": drawn,
        "sci_candidates": sci,
        "matches": matches,
        "policy": [
            "visual cards open a style direction; they are not a publication guarantee",
            "use one intact SCI ramp per semantic layer; never splice categorical and diverging colours",
            "render and audit the final figure at its target size before selection",
        ],
        "provenance": {
            "draw_seed": seed,
            "image_cards": "local card manifest; source/rights metadata retained in cards_json",
            "sci_adapter": "scripts/sci_palette_bridge.py",
            "audit": "SCI CIE76/CVD/luminance/white-background diagnostics",
        },
    }


def _font(size: int):
    try:
        from PIL import ImageFont
        for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
            if Path(path).is_file():
                return ImageFont.truetype(path, size=size)
        return ImageFont.load_default()
    except ImportError as error:
        raise RuntimeError("Pillow is required to render the joint preview") from error


def _swatch(draw, x: int, y: int, w: int, h: int, colours: list[str], *, labels: bool = False) -> None:
    if not colours:
        return
    width = max(1, int(w / len(colours)))
    small = _font(max(10, min(14, h // 3)))
    for index, colour in enumerate(colours):
        left = x + index * width
        right = x + (index + 1) * width if index < len(colours) - 1 else x + w
        draw.rectangle((left, y, right, y + h), fill=colour, outline="#FFFFFF", width=1)
        if labels and right - left > 52:
            draw.text((left + 4, y + h + 3), colour, fill="#263238", font=small)


def render_preview(payload: dict[str, Any], output: str | Path) -> Path:
    """Render a combined card + SCI candidate contact sheet with Pillow."""
    try:
        from PIL import Image, ImageDraw, ImageOps
    except ImportError as error:
        raise RuntimeError("Pillow is required for --preview") from error
    out = Path(output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    width, height = 3000, 2080
    image = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(image)
    title = _font(42)
    heading = _font(28)
    body = _font(20)
    small = _font(16)
    draw.text((70, 42), "Joint palette draw · visual cards × SCI semantic candidates", fill="#263238", font=title)
    draw.text((70, 100), f"seed={payload['seed']}  ·  figure={payload['request']['figure']}  ·  groups={payload['request']['groups']}", fill="#6B7280", font=body)
    left_x, left_w = 70, 1390
    right_x, right_w = 1530, 1400
    draw.line((left_x + left_w + 30, 150, left_x + left_w + 30, height - 100), fill="#D8DEE4", width=2)
    draw.text((left_x, 155), "A  Visual card draw (inspiration)", fill="#263238", font=heading)
    draw.text((right_x, 155), "B  SCI candidates (semantic output)", fill="#263238", font=heading)
    match_by_card: dict[str, dict[str, str]] = {}
    for kind, rows in payload.get("matches", {}).items():
        for row in rows:
            match_by_card.setdefault(row["card_id"], {})[kind] = row["sci_palette_id"]
    card_w, card_h = 665, 305
    for idx, card in enumerate(payload["cards"]):
        col, row = idx % 2, idx // 2
        x = left_x + col * (card_w + 35)
        y = 205 + row * (card_h + 22)
        draw.rounded_rectangle((x, y, x + card_w, y + card_h), radius=12, fill="#FAFBFC", outline="#D8DEE4", width=2)
        local = Path(card.get("local_image", ""))
        thumb_box = (x + 14, y + 14, x + card_w - 14, y + 168)
        if local.is_file():
            try:
                with Image.open(local) as source:
                    thumb = ImageOps.fit(source.convert("RGB"), (thumb_box[2] - thumb_box[0], thumb_box[3] - thumb_box[1]), method=Image.Resampling.LANCZOS)
                image.paste(thumb, (thumb_box[0], thumb_box[1]))
            except Exception:
                draw.rectangle(thumb_box, fill="#EEF1F3")
        else:
            draw.rectangle(thumb_box, fill="#EEF1F3")
        label = f"{card['card_id']}  #{card['draw_rank']}  {card.get('title', 'untitled')[:46]}"
        draw.text((x + 16, y + 181), label, fill="#263238", font=body)
        draw.text((x + 16, y + 208), f"cue: {card['visual_cue']}  ·  richness: {card.get('colorfulness', {}).get('score', 'n/a')}", fill="#6B7280", font=small)
        _swatch(draw, x + 16, y + 240, card_w - 32, 30, card["extracted_hex"][:6], labels=False)
        linked = match_by_card.get(card["card_id"], {})
        links = "  ·  ".join(f"{key} → {value}" for key, value in linked.items()) or "no semantic match requested"
        draw.text((x + 16, y + 278), links[:82], fill="#263238", font=small)
    y0 = 205
    sections = [("Categorical blocks", payload["sci_candidates"].get("categorical", []), "database field; intact qualitative ramp"), ("Signed heatmap", payload["sci_candidates"].get("heatmap", []), "diverging ramp; centre is zero")]
    if "circular" in payload["sci_candidates"]:
        layers = payload["sci_candidates"]["circular"]["layers"]
        sections.append(("Circular heatmap", [], "category ring + signed heat ring + neutral validation ring"))
    for section_index, (label, rows, note) in enumerate(sections):
        y = y0 + section_index * 560
        draw.rounded_rectangle((right_x, y, right_x + right_w, y + 510), radius=12, fill="#FAFBFC", outline="#D8DEE4", width=2)
        draw.text((right_x + 22, y + 18), label, fill="#263238", font=heading)
        draw.text((right_x + 22, y + 55), note, fill="#6B7280", font=small)
        if rows:
            row_h = 76
            for i, rowdata in enumerate(rows[:5]):
                yy = y + 88 + i * row_h
                draw.text((right_x + 22, yy + 12), f"{i + 1}. {rowdata['id']}", fill="#263238", font=body)
                _swatch(draw, right_x + 380, yy + 8, 610, 34, rowdata.get("selected_hex") or rowdata.get("hex", []))
                quality = rowdata.get("score")
                if quality is None:
                    quality = rowdata.get("rank_metrics", {}).get("min5_delta_e", "-")
                draw.text((right_x + 1015, yy + 12), f"quality {quality}", fill="#6B7280", font=small)
        else:
            circular_layers = payload["sci_candidates"]["circular"]["layers"]
            layer_y = y + 98
            for layer in circular_layers:
                draw.text((right_x + 25, layer_y), layer["layer"], fill="#263238", font=body)
                if layer.get("recommendations"):
                    first = layer["recommendations"][0]
                    colours = first.get("selected_hex") or first.get("hex") or []
                    _swatch(draw, right_x + 510, layer_y - 3, 620, 30, colours)
                    draw.text((right_x + 1160, layer_y), str(first.get("id", "neutral-accent")), fill="#6B7280", font=small)
                else:
                    draw.rectangle((right_x + 510, layer_y - 3, right_x + 1130, layer_y + 27), fill="#B8BEC4")
                    draw.text((right_x + 1160, layer_y), "gray + one accent", fill="#6B7280", font=small)
                layer_y += 95
        draw.text((right_x + 22, y + 462), "Card colours guide mood; SCI colours carry semantic meaning and audit evidence.", fill="#6B7280", font=small)
    draw.text((70, height - 62), "Diagnostic preview only · inspect the final figure at target size · no cross-layer colour splicing", fill="#6B7280", font=small)
    image.save(out, dpi=(180, 180))
    return out


def render_html(payload: dict[str, Any], output: str | Path) -> Path:
    """Write a small self-contained HTML index for the combined result."""
    out = Path(output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for card in payload["cards"]:
        swatches = "".join(f'<span class="swatch" style="background:{html.escape(c)}" title="{html.escape(c)}"></span>' for c in card["extracted_hex"])
        image = html.escape(card.get("local_image", ""))
        rows.append(f'<article><h3>{html.escape(card["card_id"])} · {html.escape(str(card.get("title", "untitled")))}</h3><img src="{image}" alt=""><p>{html.escape(card["visual_cue"])}</p><div>{swatches}</div></article>')
    candidate_blocks = []
    for kind, title in (("categorical", "Categorical blocks"), ("heatmap", "Signed heatmap")):
        items = payload["sci_candidates"].get(kind, [])
        item_html = []
        for item in items:
            swatches = "".join(
                f'<span class="swatch" style="background:{html.escape(c)}"></span>'
                for c in (item.get("selected_hex") or item.get("hex", []))
            )
            item_html.append(f'<li><b>{html.escape(item["id"])}</b> <span class="swatches">{swatches}</span></li>')
        body = "".join(item_html)
        candidate_blocks.append(f"<section><h2>{title}</h2><ul>{body}</ul></section>")
    page = f"""<!doctype html><meta charset='utf-8'><title>Joint palette draw</title><style>body{{font:16px system-ui,sans-serif;color:#263238;max-width:1400px;margin:2rem auto}}.cards{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}}article,section{{border:1px solid #d8dee4;border-radius:10px;padding:1rem;background:#fafbfc}}img{{width:100%;height:150px;object-fit:cover}}.swatch{{display:inline-block;width:34px;height:18px;margin-right:2px;border:1px solid #fff}}li{{margin:.6rem 0}}h1,h2,h3{{font-weight:600}}</style><h1>Joint palette draw</h1><p>seed={payload['seed']} · figure={payload['request']['figure']} · groups={payload['request']['groups']}</p><div class='cards'>{''.join(rows)}</div>{''.join(candidate_blocks)}"""
    out.write_text(page, encoding="utf-8")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cards-json", required=True, type=Path)
    parser.add_argument("--figure", choices=FIGURE_CHOICES, default="all")
    parser.add_argument("--groups", type=int, default=5)
    parser.add_argument("--draw-count", type=int, default=10, metavar="1-10")
    parser.add_argument("--seed", type=int, default=20261025)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--no-preview", action="store_true")
    args = parser.parse_args()
    payload = draw_joint(args.cards_json, figure=args.figure, groups=args.groups, draw_count=args.draw_count, seed=args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "joint_palette_draw.json"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not args.no_preview:
        render_preview(payload, args.output_dir / "joint_palette_preview.png")
        render_html(payload, args.output_dir / "index.html")
    print(json.dumps({"json": str(json_path), "preview": str(args.output_dir / 'joint_palette_preview.png'), "html": str(args.output_dir / 'index.html')}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
