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

    def test_plain_image_word_does_not_start_card_draw(self) -> None:
        router = load_router()
        self.assertEqual(router.route("这张图用水墨配色")["mode"], "fast-built-in")

    def test_compact_summary_keeps_primary_and_risk(self) -> None:
        router = load_router()
        summary = router.compact_summary(router.route("五组白底 GO 富集图，东方水墨风格"))
        self.assertIn("主方案：ink-mineral-a-sunlit", summary)
        self.assertIn("备选：dunhuang-mineral、hokusai-indigo", summary)
        self.assertIn("首要风险：", summary)

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
