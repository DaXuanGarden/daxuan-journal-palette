from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_router():
    path = ROOT / "scripts" / "route_palette.py"
    spec = importlib.util.spec_from_file_location("route_palette", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FastRouterTests(unittest.TestCase):
    def test_builtin_request_returns_one_primary_and_two_alternatives(self) -> None:
        router = load_router()
        result = router.route("五组白底 GO 富集图，东方水墨风格")
        self.assertEqual(result["mode"], "fast-built-in")
        self.assertEqual(result["groups"], 5)
        self.assertEqual(result["background"], "white")
        self.assertEqual(result["primary"]["palette_id"], "ink-mineral-a-sunlit")
        self.assertEqual(len(result["alternatives"]), 2)

    def test_draw_count_defaults_to_five_and_single_card_is_one(self) -> None:
        router = load_router()
        self.assertEqual(router.route("随机抽蓝绿色公共领域作品") ["draw_count"], 5)
        self.assertEqual(router.route("随机抽一张蓝绿色公共领域作品") ["draw_count"], 1)
        self.assertEqual(router.route("随机抽一张蓝绿色公共领域作品")["mode"], "card-draw")

    def test_draw_count_accepts_explicit_counts_up_to_ten(self) -> None:
        router = load_router()
        self.assertEqual(router.route("随机抽十张色彩丰富的公共领域卡片")["draw_count"], 10)
        self.assertEqual(router.route("随机抽 8 张色彩丰富的公共领域卡片")["draw_count"], 8)
        self.assertTrue(router.route("随机抽十张色彩丰富的公共领域卡片")["palette_friendly"])

    def test_plain_image_word_does_not_start_card_draw(self) -> None:
        router = load_router()
        self.assertEqual(router.route("这张图用水墨配色")["mode"], "fast-built-in")

    def test_compact_summary_keeps_primary_and_risk(self) -> None:
        router = load_router()
        summary = router.compact_summary(router.route("五组白底 GO 富集图，东方水墨风格"))
        self.assertIn("主方案：ink-mineral-a-sunlit", summary)
        self.assertIn("备选：hokusai-indigo、botanical-earth", summary)
        self.assertIn("首要风险：", summary)

    def test_candidate_gate_separates_visual_families(self) -> None:
        router = load_router()
        result = router.route("五组白底环形热图")
        diversity = result["candidate_diversity"]
        self.assertTrue(diversity["pass"])
        self.assertEqual(diversity["distinct_families"], 3)
        self.assertGreaterEqual(diversity["observed_min_delta_e"], diversity["minimum_delta_e"])
        self.assertTrue(all(card["distinctness"] in {"primary", "pass"} for card in [result["primary"], *result["alternatives"]]))
        self.assertTrue(any(item["palette_id"] == "dunhuang-mineral" for item in diversity["rejected_candidates"]))

    def test_palette_distance_detects_near_duplicates(self) -> None:
        router = load_router()
        self.assertAlmostEqual(
            router.palette_distance(["#6D98AF"], ["#6D98AF"]),
            0.0,
            places=6,
        )
        self.assertLess(router.palette_distance(["#6D98AF"], ["#6E99B0"]), 1.0)

    def test_route_returns_bounded_human_review_handoff(self) -> None:
        router = load_router()
        result = router.route("五组白底环形热图")
        review = result["human_review"]
        self.assertEqual(review["status"], "awaiting_author")
        self.assertEqual(len(review["questions"]), 3)
        self.assertEqual(review["candidate_ids"], [result["primary"]["palette_id"], *[item["palette_id"] for item in result["alternatives"]]])
        self.assertIn("pause before editing", " ".join(review["guardrails"]))

    def test_circular_keyword_is_not_collapsed_into_sequential(self) -> None:
        router = load_router()
        result = router.route("LDSC 环形热图")
        self.assertEqual(result["figure_type"], "circular")
        self.assertEqual(result["primary"]["palette_id"], "ink-mineral-a-sunlit")

    def test_diverging_request_still_gets_two_alternatives(self) -> None:
        router = load_router()
        result = router.route("正负效应发散图")
        self.assertEqual(result["primary"]["palette_id"], "ink-cinnabar-diverging")
        self.assertEqual(len(result["alternatives"]), 2)

    def test_index_palette_ids_exist_in_registry(self) -> None:
        index = json.loads((ROOT / "assets/palette-gallery/palette-index.json").read_text(encoding="utf-8"))
        registry = json.loads((ROOT / "assets/palette-gallery/palettes.json").read_text(encoding="utf-8"))
        palette_ids = {palette["id"] for palette in registry["palettes"]}
        indexed_ids = {
            palette_id
            for route in index["routes"]
            for palette_id in route["palette_ids"]
        }
        self.assertTrue(indexed_ids <= palette_ids)


if __name__ == "__main__":
    unittest.main()
