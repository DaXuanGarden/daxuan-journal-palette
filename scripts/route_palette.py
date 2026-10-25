#!/usr/bin/env python3
"""Fast keyword router for the built-in palette atlas.

The router returns compact IDs and reasons. Full recipes stay in palettes.json
and the markdown references, so ordinary requests do not load the whole atlas.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from palette_distance import (  # noqa: E402
    DEFAULT_MIN_DELTA_E,
    candidate_distance,
    palette_colors,
    palette_distance,
    palette_family,
)


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "assets" / "palette-gallery" / "palette-index.json"
REGISTRY = ROOT / "assets" / "palette-gallery" / "palettes.json"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def infer_figure_type(text: str) -> str:
    if any(term in text for term in ("环形", "圆环", "环图", "circular", "circumferential")):
        return "circular"
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


def palette_rich_requested(text: str) -> bool:
    return any(term in text for term in ("色彩丰富", "多彩", "高饱和", "鲜艳", "不要灰", "colorful", "vivid", "saturated"))


def requested_draw_count(text: str, default: int) -> int:
    if any(term in text for term in ("一张", "一幅", "单张", "single", "one card")):
        return 1
    number_map = {"两": 2, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    match = re.search(r"(10|[2-9]|[两二三四五六七八九十])\s*(?:张|幅|个)?[^0-9]{0,12}(?:卡片|卡|cards?)", text)
    if match:
        token = match.group(1)
        return min(10, int(token) if token.isdigit() else number_map[token])
    return default


def build_human_review_contract(cards: list[dict]) -> dict:
    """Return a bounded author handoff before any production figure edit."""
    return {
        "mode": "author-select-before-render",
        "status": "awaiting_author",
        "candidate_ids": [card["palette_id"] for card in cards],
        "questions": [
            {
                "id": "visual_direction",
                "question": "下一轮更想保持当前气质、变亮、变鲜明、变暖还是变冷静？",
                "options": ["keep", "airy", "colorful", "warmer", "cooler"],
            },
            {
                "id": "priority",
                "question": "这一轮优先审美、可读性、均衡，还是打印/CVD？",
                "options": ["balanced", "readability", "aesthetics", "print"],
            },
            {
                "id": "edit_scope",
                "question": "本轮只改配色，还是允许同步改图例/整图细节？",
                "options": ["palette_only", "palette_legend", "full_figure"],
            },
        ],
        "guardrails": [
            "keep data and semantic assignments fixed",
            "compare candidates with identical geometry and export settings",
            "only present alternatives that pass the visual-distance and family-diversity gate",
            "pause before editing a production figure",
            "record selection and free-text feedback as preference constraints",
        ],
        "decision_log": [],
        "provenance": {"contract": "scripts/author_review.py", "status": "router-handoff"},
    }


def select_diverse_candidates(
    scored: list[tuple[int, int, list[str], dict]],
    registry: dict[str, dict],
    limit: int,
    *,
    min_delta_e: float = DEFAULT_MIN_DELTA_E,
) -> dict:
    """Select scored routes while separating visual families.

    A route can contain several close variants from one family.  Showing all
    of them as A/B/C creates a false sense of choice, so alternatives are
    accepted only when they belong to a new family and are at least
    ``min_delta_e`` away from every already-selected palette.  If the route
    index cannot supply enough distinct choices, the least-similar remaining
    choices are returned with an explicit fallback warning.
    """

    chosen: list[tuple[int, int, list[str], dict]] = []
    rejected: list[dict] = []
    fallback_candidates: list[dict] = []
    seen_ids: set[str] = set()

    def candidate_id(item: tuple[int, int, list[str], dict]) -> str:
        return str(item[3].get("palette_ids", [""])[0])

    def candidate_info(item: tuple[int, int, list[str], dict], reason: str, distance: float | None) -> dict:
        pid = candidate_id(item)
        return {
            "palette_id": pid,
            "family": palette_family(pid, registry),
            "distance_to_selected": round(distance, 2) if distance is not None else None,
            "reason": reason,
        }

    for item in scored:
        if len(chosen) >= limit:
            break
        pid = candidate_id(item)
        if not pid or pid in seen_ids or not palette_colors(pid, registry):
            continue
        if not chosen:
            chosen.append(item)
            seen_ids.add(pid)
            continue

        selected_ids = [candidate_id(selected) for selected in chosen]
        distance = candidate_distance(pid, selected_ids, registry)
        family = palette_family(pid, registry)
        selected_families = {palette_family(selected_id, registry) for selected_id in selected_ids}
        reasons = []
        if family in selected_families:
            reasons.append("same_visual_family")
        if distance < min_delta_e:
            reasons.append("below_minimum_delta_e")
        if reasons:
            rejected.append(candidate_info(item, "+".join(reasons), distance))
            continue
        chosen.append(item)
        seen_ids.add(pid)

    # A sparse route index should not silently return fewer cards.  Fill any
    # remaining slots with the most separated choices and make the fallback
    # visible to the author in the returned audit.
    fallback_used = False
    while len(chosen) < limit:
        remaining = [item for item in scored if candidate_id(item) not in seen_ids and palette_colors(candidate_id(item), registry)]
        if not remaining:
            break
        if not chosen:
            item = remaining[0]
            distance = None
        else:
            item = max(
                remaining,
                key=lambda candidate: candidate_distance(
                    candidate_id(candidate), [candidate_id(selected) for selected in chosen], registry
                ),
            )
            distance = candidate_distance(candidate_id(item), [candidate_id(selected) for selected in chosen], registry)
        fallback_candidates.append(candidate_info(item, "fallback_after_diversity_pool_exhausted", distance))
        chosen.append(item)
        seen_ids.add(candidate_id(item))
        fallback_used = True

    return {
        "selected": chosen,
        "rejected": rejected,
        "fallback_candidates": fallback_candidates,
        "fallback_used": fallback_used,
        "minimum_delta_e": min_delta_e,
    }


def route(request: str, limit: int = 3) -> dict:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    registry_payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry = {str(item["id"]): item for item in registry_payload.get("palettes", [])}
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
    candidate_pool = [item for item in scored if item[0] > 0]
    # A circular figure is usually layer-aware: its category ring needs a
    # qualitative family even when the request also contains "heatmap". If no
    # explicit style keyword was supplied, do not let the heatmap keyword route
    # the whole figure to a sequential ramp.
    semantic_keywords = {"热图", "连续", "强度", "密度", "显著性", "sequential", "相关性", "正负", "发散", "效应", "diverging"}
    explicit_style_hit = any(
        hit not in semantic_keywords for item in scored for hit in item[2]
    )
    if figure_type == "circular" and not explicit_style_hit:
        candidate_pool = [item for item in scored if "qualitative" in item[3]["figure_types"]]
    if len(candidate_pool) < limit:
        selected_keys = {id(item) for item in candidate_pool}
        candidate_pool.extend(item for item in scored if id(item) not in selected_keys)
    selection = select_diverse_candidates(candidate_pool, registry, limit)
    selected = selection["selected"]
    cards = []
    primary_id = str(selected[0][3]["palette_ids"][0]) if selected else ""
    selected_ids = [str(item[3]["palette_ids"][0]) for item in selected]
    selected_families = [palette_family(pid, registry) for pid in selected_ids]
    for rank, (_, _, hits, route_item) in enumerate(selected, start=1):
        palette_id = str(route_item["palette_ids"][0])
        distance = 0.0 if rank == 1 else candidate_distance(palette_id, [primary_id], registry)
        cards.append({
            "rank": rank,
            "palette_id": palette_id,
            "visual_family": palette_family(palette_id, registry),
            "distance_from_primary_delta_e": round(distance, 2),
            "distinctness": "primary" if rank == 1 else ("pass" if distance >= selection["minimum_delta_e"] else "warn"),
            "related_palette_ids": route_item["palette_ids"][1:],
            "matched_keywords": hits,
            "best_for": route_item["best_for"],
            "risk": route_item["risk"],
        })
    pairwise_distances = []
    for pair_index, left_id in enumerate(selected_ids):
        for right_id in selected_ids[pair_index + 1 :]:
            pairwise_distances.append(candidate_distance(left_id, [right_id], registry))
    observed_min = min(pairwise_distances) if pairwise_distances else 0.0
    diversity = {
        "strategy": "CIE76 symmetric mean-nearest palette distance plus visual-family separation",
        "minimum_delta_e": selection["minimum_delta_e"],
        "observed_min_delta_e": round(observed_min, 2),
        "distinct_families": len(set(selected_families)),
        "families": selected_families,
        "pass": bool(len(selected) <= 1 or observed_min >= selection["minimum_delta_e"]),
        "fallback_used": selection["fallback_used"],
        "rejected_candidates": selection["rejected"],
        "fallback_candidates": selection["fallback_candidates"],
    }
    return {
        "mode": "card-draw" if draw_requested(text) else "fast-built-in",
        "figure_type": figure_type,
        "groups": groups,
        "background": background,
        "primary": cards[0],
        "alternatives": cards[1:],
        "candidate_diversity": diversity,
        "rejected_candidates": selection["rejected"],
        "next_questions": ["图表类型？", "大约几组/几类？", "白底还是深底？"],
        "human_review": build_human_review_contract(cards),
        "draw_count": requested_draw_count(text, index["defaults"]["draw_cards"]) if draw_requested(text) else 0,
        "palette_friendly": palette_rich_requested(text) if draw_requested(text) else False,
        "provenance": {"index": str(INDEX.relative_to(ROOT)), "full_recipes": "palettes.json", "status": "router-suggestion"},
    }


def compact_summary(result: dict) -> str:
    """Render the fast lane as a short human-readable handoff."""
    alternatives = result["alternatives"]
    alternative_ids = "、".join(item["palette_id"] for item in alternatives) or "无"
    lines = [
        f"模式：{result['mode']}",
        f"主方案：{result['primary']['palette_id']}",
        f"备选：{alternative_ids}",
        f"类型：{result['figure_type']}；组数：{result['groups']}；背景：{result['background']}",
        f"首要风险：{result['primary']['risk']}",
        f"候选多样性：{result['candidate_diversity']['observed_min_delta_e']:.1f} ΔE（阈值 {result['candidate_diversity']['minimum_delta_e']:.1f}；{'通过' if result['candidate_diversity']['pass'] else '需复核'}）",
        "下一步：图表类型、组数、白底/深底",
        "作者审阅：先选择视觉方向、优先级和改动范围，再进入下一轮渲染",
    ]
    if result["draw_count"]:
        lines.append(f"抽卡数量：{result['draw_count']} 张")
        if result.get("palette_friendly"):
            lines.append("抽卡筛选：色彩丰富度筛选（排除主要灰度/低饱和候选）")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", nargs="+", help="short Chinese or English palette request")
    parser.add_argument("--limit", type=int, default=3, choices=(1, 2, 3))
    parser.add_argument("--compact", action="store_true", help="print a short human-readable summary")
    args = parser.parse_args()
    result = route(" ".join(args.request), args.limit)
    if args.compact:
        print(compact_summary(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
