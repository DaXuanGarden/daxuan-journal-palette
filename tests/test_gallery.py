from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GALLERY = ROOT / "assets" / "palette-gallery"


class PaletteGalleryTests(unittest.TestCase):
    def test_registry_has_unique_valid_palettes(self) -> None:
        payload = json.loads((GALLERY / "palettes.json").read_text(encoding="utf-8"))
        palettes = payload["palettes"]
        ids = [palette["id"] for palette in palettes]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertGreaterEqual(len(palettes), 20)
        for palette in palettes:
            self.assertEqual(len(palette["colors"]), len(palette["names"]))
            for colour in palette["colors"]:
                self.assertRegex(colour, r"^#[0-9A-Fa-f]{6}$")

    def test_generated_gallery_outputs_are_present(self) -> None:
        for name in ("index.html", "palette-atlas.svg", "palettes.csv", "manifest.json"):
            path = GALLERY / name
            self.assertTrue(path.is_file(), name)
            self.assertGreater(path.stat().st_size, 0, name)

    def test_gallery_contains_each_registry_id(self) -> None:
        payload = json.loads((GALLERY / "palettes.json").read_text(encoding="utf-8"))
        html = (GALLERY / "index.html").read_text(encoding="utf-8")
        svg = (GALLERY / "palette-atlas.svg").read_text(encoding="utf-8")
        for palette in payload["palettes"]:
            self.assertIn(palette["id"], html)
            self.assertIn(palette["id"], svg)


if __name__ == "__main__":
    unittest.main()
