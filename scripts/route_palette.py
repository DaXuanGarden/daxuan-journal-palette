#!/usr/bin/env python3
"""Fast keyword router for the built-in palette atlas.

The router returns compact IDs and reasons. Full recipes stay in palettes.json
and the markdown references, so ordinary requests do not load the whole atlas.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "assets" / "palette-gallery" / "palette-index.json"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def infer_figure_type(text: str) -> str:
    if any(term in text for term in ("发散", "正负", "效应", "相关性", "diverging")):
        return "diverging"
    if any(term in text for term in ("连续", "热图", "强度", "密度", "显著性", "sequential")):
        return "sequential"
    if any(term in text for term in ("主结果", "重点", "中性", "单一强调", "minimal")):
        return "neutral-accent"
    return "qualitative"


def infer_groups(text: str, default: int) -> int:
    match = re.search(r"(\d+)\s*(?:组|类|色|groups?|categories?)", text)
    return int(match.group(1)) if match else default


def infer_background(text: str, default: str) -> str:
    if any(term in text for term in ("深底", "黑底", "dark background")):
        return "dark"
    if any(term in text for term in ("白底", "白色背景", "white background")):
        return "white"
    return default


def draw_requested(text: str) -> bool:
    return any(term in text for term in ("抽卡", "随机抽", "视觉卡片", "公共领域", "生成卡片", "图片提取", "draw card", "image card"))


def requested_draw_count(text: str, default: int) -> int:
    if any(term in text for term in ("一张", "一幅", "单张", "single", "one card")):
        return 1
    return default


def route(request: str, limit: int = 3) -> dict:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    text = normalize(request)
    figure_type = infer_figure_type(text)
    groups = infer_groups(text, index["defaults"]["groups"])
    background = infer_background(text, index["defaults"]["background"])
    scored = []
    for order, route_item in enumerate(index["routes"]):
        hits = [keyword for keyword in route_item["keywords"] if normalize(keyword) in text]
        type_bonus = 2 if figure_type in route_item["figure_types"] else 0
        if groups > 6 and "neutral-accent" in route_item["figure_types"]:
            type_bonus -= 1
        scored.append((len(hits) * 3 + type_bonus, -order, hits, route_item))
    scored.sort(reverse=True, key=lambda item: (item[0], item[1]))
    selected = [item for item in scored if item[0] > 0][:limit]
    if len(selected) < limit:
        selected_keys = {id(item) for item in selected}
        selected.extend(item for item in scored if id(item) not in selected_keys and len(selected) < limit)
    cards = []
    for rank, (_, _, hits, route_item) in enumerate(selected, start=1):
        cards.append({
            "rank": rank,
            "palette_id": route_item["palette_ids"][0],
            "related_palette_ids": route_item["palette_ids"][1:],
            "matched_keywords": hits,
            "best_for": route_item["best_for"],
            "risk": route_item["risk"],
        })
    return {
        "mode": "card-draw" if draw_requested(text) else "fast-built-in",
        "figure_type": figure_type,
        "groups": groups,
        "background": background,
        "primary": cards[0],
        "alternatives": cards[1:],
        "next_questions": ["图表类型？", "大约几组/几类？", "白底还是深底？"],
        "draw_count": requested_draw_count(text, index["defaults"]["draw_cards"]) if draw_requested(text) else 0,
        "provenance": {"index": str(INDEX.relative_to(ROOT)), "full_recipes": "palettes.json", "status": "router-suggestion"},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", nargs="+", help="short Chinese or English palette request")
    parser.add_argument("--limit", type=int, default=3, choices=(1, 2, 3))
    args = parser.parse_args()
    print(json.dumps(route(" ".join(args.request), args.limit), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
