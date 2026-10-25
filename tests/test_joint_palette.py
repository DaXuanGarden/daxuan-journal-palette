from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_joint():
    path = ROOT / "scripts" / "joint_palette_draw.py"
    spec = importlib.util.spec_from_file_location("joint_palette_draw", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class JointPaletteDrawTests(unittest.TestCase):
    def _manifest(self, directory: Path) -> Path:
        payload = {
            "schema_version": "1.0.0",
            "draw_id": "test-draw",
            "cards": [
                {"card_id": "card-01", "title": "red", "extracted_hex": ["#C9474B", "#E7B65A", "#4F7887"]},
                {"card_id": "card-02", "title": "blue", "extracted_hex": ["#315C6B", "#7DAFA8", "#D8B16A"]},
                {"card_id": "card-03", "title": "purple", "extracted_hex": ["#6E4C73", "#BF8FA4", "#E4D8C9"]},
            ],
        }
        path = directory / "cards.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_draw_is_seeded_and_keeps_semantic_layers_separate(self) -> None:
        module = load_joint()
        with tempfile.TemporaryDirectory() as tmp:
            manifest = self._manifest(Path(tmp))
            first = module.draw_joint(manifest, figure="all", groups=3, draw_count=3, seed=11)
            second = module.draw_joint(manifest, figure="all", groups=3, draw_count=3, seed=11)
        self.assertEqual([row["card_id"] for row in first["cards"]], [row["card_id"] for row in second["cards"]])
        self.assertIn("categorical", first["sci_candidates"])
        self.assertIn("heatmap", first["sci_candidates"])
        self.assertIn("circular", first["sci_candidates"])
        self.assertEqual(len(first["matches"]["categorical"]), 3)
        self.assertEqual(len(first["matches"]["heatmap"]), 3)
        self.assertTrue(all(row["sci_palette_id"] for row in first["matches"]["categorical"]))
        self.assertTrue(all("intact" in row["rule"] for row in first["matches"]["heatmap"]))

    def test_preview_writes_a_visible_png_and_html(self) -> None:
        module = load_joint()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self._manifest(root)
            payload = module.draw_joint(manifest, figure="categorical", groups=3, draw_count=2, seed=3)
            png = module.render_preview(payload, root / "preview.png")
            html = module.render_html(payload, root / "index.html")
            self.assertGreater(png.stat().st_size, 1000)
            self.assertIn("Joint palette draw", html.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
