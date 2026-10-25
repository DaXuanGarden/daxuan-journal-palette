from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_theme():
    path = ROOT / "scripts" / "theme_palette.py"
    spec = importlib.util.spec_from_file_location("theme_palette", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ThemePaletteTests(unittest.TestCase):
    def test_cardiovascular_theme_builds_three_directional_candidates(self) -> None:
        module = load_theme()
        payload = module.build_theme_brief(
            title="久坐行为与心血管疾病的遗传相关性",
            fragment="We evaluate sedentary behavior across cardiovascular outcomes.",
            figure_meaning="21 outcome rings with signed genetic correlations",
            figure_type="circular",
            groups=5,
            background="white",
        )
        self.assertEqual(payload["theme"]["id"], "sedentary_cardiovascular")
        self.assertEqual([item["direction_id"] for item in payload["directions"]], ["A", "B", "C"])
        self.assertEqual([item["palette_id"] for item in payload["directions"]], [
            "clinical-cool-warm",
            "matisse-flat",
            "tea-earth-botanical",
        ])
        self.assertTrue(payload["candidate_diversity"]["pass"])
        self.assertGreaterEqual(payload["candidate_diversity"]["observed_min_delta_e"], 18.0)
        self.assertIn("heart|anatomy|vascular", payload["image_inspiration"]["search_queries"])
        json.dumps(payload, ensure_ascii=False)

    def test_generic_theme_keeps_directional_separation(self) -> None:
        module = load_theme()
        payload = module.build_theme_brief(title="A scientific result figure")
        self.assertEqual(payload["theme"]["id"], "generic_scientific_figure")
        self.assertEqual(len(payload["directions"]), 3)
        self.assertTrue(payload["candidate_diversity"]["pass"])
        self.assertEqual(payload["human_review"]["status"], "awaiting_author")

    def test_title_is_required(self) -> None:
        module = load_theme()
        with self.assertRaises(ValueError):
            module.build_theme_brief(title="")


if __name__ == "__main__":
    unittest.main()
