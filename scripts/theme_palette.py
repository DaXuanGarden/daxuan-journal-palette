#!/usr/bin/env python3
"""Build a theme-aware palette and image-inspiration brief.

This planner connects paper language to visual directions before any image is
drawn or any production figure is edited.  It is deliberately dependency-free
and offline: the returned image queries can be passed to ``draw_art_cards.py``
after the author approves the source and visual direction.

Example::

    python3 scripts/theme_palette.py \
      --title "Sedentary behavior and cardiovascular disease" \
      --fragment "Genetic correlation across cardiovascular outcomes" \
      --figure-meaning "21 outcome rings with signed genetic correlations" \
      --figure-type circular --groups 5 --background white --compact
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parents[0]
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from palette_distance import DEFAULT_MIN_DELTA_E, candidate_distance, palette_colors, palette_family  # noqa: E402


REGISTRY = ROOT / "assets" / "palette-gallery" / "palettes.json"


THEME_RULES: list[dict[str, Any]] = [
    {
        "id": "sedentary_cardiovascular",
        "label": "sedentary behavior and cardiovascular health",
        "terms": (
            "久坐",
            "sedentary",
            "sitting",
            "physical inactivity",
            "cardiovascular",
            "心血管",
            "心脏",
            "cardiac",
            "vascular",
            "动脉",
            "atherosclerosis",
            "动脉粥样硬化",
            "coronary",
            "冠脉",
        ),
        "topic_anchors": ["heart", "vessel", "arterial wall", "circulation"],
        "visual_metaphors": ["flow", "network", "movement", "barrier", "recovery"],
        "image_queries": [
            "heart|anatomy|vascular",
            "movement|walking|figure",
            "water|flow|current",
            "botanical|leaf|vein",
        ],
        "image_rationale": "主题锚点覆盖心脏/血管；流动、步行和叶脉作为久坐—循环的视觉隐喻。",
        "directions": [
            {
                "id": "A",
                "name": "vascular-clinical",
                "label": "血管临床可信度",
                "palette_ids": ["clinical-cool-warm", "hokusai-indigo", "nature-muted"],
                "direction": "冷静蓝灰承载临床可信度，珊瑚只作为有限验证强调。",
                "theme_fit": "最适合主结果图、遗传相关性和多层验证状态。",
                "avoid": ["大面积暖色", "把红色解释为风险方向"],
            },
            {
                "id": "B",
                "name": "circulation-energy",
                "label": "循环与活动能量",
                "palette_ids": ["matisse-flat", "dunhuang-mineral", "editorial-jewel"],
                "direction": "更鲜明的蓝—朱砂—黄组合表达流动、活动和结果层级。",
                "theme_fit": "适合展示久坐与心血管结局之间的整体关系和图形摘要。",
                "avoid": ["用暖色单独编码统计方向", "覆盖所有层的高饱和填充"],
            },
            {
                "id": "C",
                "name": "biological-equilibrium",
                "label": "生物系统平衡",
                "palette_ids": ["tea-earth-botanical", "botanical-earth", "coastal-mineral"],
                "direction": "植物绿、土色和海岸蓝强调组织、代谢和血管系统的平衡。",
                "theme_fit": "适合机制解释、亚临床血管表型和补充图。",
                "avoid": ["绿色表达显著性", "将自然意象写成生物学因果证据"],
            },
        ],
    },
    {
        "id": "generic_scientific_figure",
        "label": "general scientific figure",
        "terms": (),
        "topic_anchors": ["research result", "data structure"],
        "visual_metaphors": ["structure", "contrast", "continuity"],
        "image_queries": ["abstract|geometry|pattern", "water|flow|texture", "botanical|structure|detail"],
        "image_rationale": "未识别到明确疾病主题，使用结构、流动和自然纹理作为中性视觉线索。",
        "directions": [
            {
                "id": "A",
                "name": "editorial-ink",
                "label": "编辑部纸墨",
                "palette_ids": ["ink-mineral-a-sunlit", "ink-paper-literati", "modern-ink-mineral"],
                "direction": "白底中等明度的纸墨和矿物色。",
                "theme_fit": "适合密集分类结果。",
                "avoid": ["浅色小点无描边"],
            },
            {
                "id": "B",
                "name": "print-indigo",
                "label": "版画靛蓝",
                "palette_ids": ["hokusai-indigo", "qinghua-porcelain", "paper-blue-sequential"],
                "direction": "靛蓝和米白形成清晰的版画层次。",
                "theme_fit": "适合空间和流程结构。",
                "avoid": ["相邻蓝色缺少明度差"],
            },
            {
                "id": "C",
                "name": "botanical-earth",
                "label": "草木土色",
                "palette_ids": ["tea-earth-botanical", "botanical-earth", "coastal-mineral"],
                "direction": "草木、土色和海岸蓝形成自然系统感。",
                "theme_fit": "适合机制与生态叙事。",
                "avoid": ["把绿色当作正向含义"],
            },
        ],
    },
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def load_registry() -> dict[str, dict[str, Any]]:
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {str(item["id"]): item for item in payload.get("palettes", [])}


def infer_theme(title: str, fragment: str, figure_meaning: str) -> tuple[dict[str, Any], list[str], list[str]]:
    text = normalize(" ".join((title, fragment, figure_meaning)))
    scored: list[tuple[int, int, dict[str, Any], list[str]]] = []
    for order, rule in enumerate(THEME_RULES):
        hits = [term for term in rule["terms"] if normalize(term) in text]
        scored.append((len(hits), -order, rule, hits))
    scored.sort(reverse=True, key=lambda row: (row[0], row[1]))
    _, _, rule, hits = scored[0]
    if not hits:
        rule = next(item for item in THEME_RULES if item["id"] == "generic_scientific_figure")
    return rule, hits, sorted(set(normalize(term) for term in rule["terms"] if normalize(term) in text))


def choose_directions(
    directions: list[dict[str, Any]], registry: dict[str, dict[str, Any]], min_delta_e: float = DEFAULT_MIN_DELTA_E
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    chosen: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for direction in directions:
        selected_id = None
        selected_distance = None
        for palette_id in direction["palette_ids"]:
            if not palette_colors(palette_id, registry):
                rejected.append({"direction": direction["id"], "palette_id": palette_id, "reason": "missing_registry_palette"})
                continue
            selected_ids = [item["palette_id"] for item in chosen]
            distance = candidate_distance(palette_id, selected_ids, registry) if selected_ids else 0.0
            family = palette_family(palette_id, registry)
            families = {item["visual_family"] for item in chosen}
            if selected_ids and (distance < min_delta_e or family in families):
                rejected.append({
                    "direction": direction["id"],
                    "palette_id": palette_id,
                    "distance_to_selected": round(distance, 2),
                    "reason": "below_minimum_delta_e" if distance < min_delta_e else "same_visual_family",
                })
                continue
            selected_id = palette_id
            selected_distance = distance
            break
        if selected_id is None:
            # The direction is still retained, but the failure is explicit.
            selected_id = direction["palette_ids"][0]
            selected_distance = candidate_distance(selected_id, [item["palette_id"] for item in chosen], registry) if chosen else 0.0
            fallback = True
        else:
            fallback = False
        row = {
            "direction_id": direction["id"],
            "direction_name": direction["name"],
            "label": direction["label"],
            "palette_id": selected_id,
            "visual_family": palette_family(selected_id, registry),
            "distance_to_previous_selected_delta_e": round(selected_distance, 2),
            "distinctness": "pass" if not chosen or selected_distance >= min_delta_e else "warn",
            "direction": direction["direction"],
            "theme_fit": direction["theme_fit"],
            "avoid": direction["avoid"],
            "fallback_used": fallback,
        }
        chosen.append(row)
    pairwise = []
    for left_index, left in enumerate(chosen):
        for right in chosen[left_index + 1 :]:
            pairwise.append(candidate_distance(left["palette_id"], [right["palette_id"]], registry))
    if pairwise:
        observed_min = min(pairwise)
    else:
        observed_min = 0.0
    for row in chosen:
        row["pairwise_min_delta_e"] = round(observed_min, 2)
    return chosen, rejected


def build_theme_brief(
    *,
    title: str,
    fragment: str = "",
    figure_meaning: str = "",
    figure_type: str = "qualitative",
    groups: int = 5,
    background: str = "white",
    min_delta_e: float = DEFAULT_MIN_DELTA_E,
) -> dict[str, Any]:
    if not title.strip():
        raise ValueError("title must not be empty")
    registry = load_registry()
    rule, hits, theme_terms = infer_theme(title, fragment, figure_meaning)
    directions, rejected = choose_directions(rule["directions"], registry, min_delta_e=min_delta_e)
    query = "|".join(rule["image_queries"])
    return {
        "schema_version": "1.0.0",
        "kind": "theme-aware-palette-brief",
        "theme": {
            "id": rule["id"],
            "label": rule["label"],
            "title": title.strip(),
            "fragment": fragment.strip(),
            "figure_meaning": figure_meaning.strip(),
            "matched_terms": hits,
            "theme_terms": theme_terms,
            "topic_anchors": rule["topic_anchors"],
            "visual_metaphors": rule["visual_metaphors"],
        },
        "figure": {
            "type": figure_type,
            "groups": groups,
            "background": background,
        },
        "image_inspiration": {
            "source_policy": "public-domain or author-supplied image only",
            "provider": "The Metropolitan Museum of Art Collection API",
            "search_query": query,
            "search_queries": list(rule["image_queries"]),
            "why_these_queries": rule["image_rationale"],
            "next_step": "先查看候选图片并选择 card_id，再运行 extract_palette.py；图片只提供视觉线索，不承载论文证据。",
            "draw_command": f"python3 scripts/draw_art_cards.py '{query}' --count 5 --seed 20261025 --palette-friendly",
        },
        "directions": directions,
        "candidate_diversity": {
            "strategy": "theme-directed semantic roles plus CIE76/family separation",
            "minimum_delta_e": min_delta_e,
            "observed_min_delta_e": directions[0]["pairwise_min_delta_e"] if directions else 0.0,
            "pass": bool(directions) and all(item["distinctness"] in {"pass", "primary"} for item in directions),
            "rejected_candidates": rejected,
        },
        "provenance": {
            "script": "scripts/theme_palette.py",
            "registry": "assets/palette-gallery/palettes.json",
            "image_source_status": "query-planned; no image downloaded",
        },
        "human_review": {
            "status": "awaiting_author",
            "questions": [
                "A（血管临床可信度）、B（循环与活动能量）、C（生物系统平衡）中，哪种主题方向最符合论文叙事？",
                "图片只作为视觉灵感，是否允许使用 The Met 公共领域卡片？",
                "本轮只提取图片色板，还是同时生成三套真实图形预览？",
            ],
        },
    }


def compact_summary(payload: dict[str, Any]) -> str:
    theme = payload["theme"]
    lines = [
        f"主题：{theme['label']}（{theme['id']}）",
        f"匹配词：{'、'.join(theme['matched_terms']) or '未识别，使用通用科研主题'}",
        f"图像检索：{payload['image_inspiration']['search_query']}",
    ]
    for item in payload["directions"]:
        lines.append(
            f"{item['direction_id']} {item['label']}：{item['palette_id']} / {item['visual_family']} "
            f"（与前序候选最小 ΔE {item['distance_to_previous_selected_delta_e']:.1f}）"
        )
    lines.append("状态：awaiting_author；先选主题方向，再提取图片色板或渲染真实图形")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--fragment", default="")
    parser.add_argument("--figure-meaning", default="")
    parser.add_argument("--figure-type", default="qualitative")
    parser.add_argument("--groups", type=int, default=5)
    parser.add_argument("--background", default="white")
    parser.add_argument("--min-delta-e", type=float, default=DEFAULT_MIN_DELTA_E)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    payload = build_theme_brief(
        title=args.title,
        fragment=args.fragment,
        figure_meaning=args.figure_meaning,
        figure_type=args.figure_type,
        groups=args.groups,
        background=args.background,
        min_delta_e=args.min_delta_e,
    )
    rendered = compact_summary(payload) if args.compact else json.dumps(payload, ensure_ascii=False, indent=2)
    rendered += "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
