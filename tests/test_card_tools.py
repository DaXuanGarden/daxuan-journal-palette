from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str):
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CardToolTests(unittest.TestCase):
    def test_kmeans_returns_deterministic_hex_candidates(self) -> None:
        module = load_script("extract_palette.py")
        pixels = [(220, 40, 40)] * 12 + [(40, 70, 220)] * 8 + [(240, 220, 80)] * 4
        first = module.kmeans(pixels, count=3, seed=7)
        second = module.kmeans(pixels, count=3, seed=7)
        self.assertEqual(first, second)
        self.assertEqual({entry["hex"] for entry in first}, {"#DC2828", "#2846DC", "#F0DC50"})
        self.assertAlmostEqual(sum(entry["share"] for entry in first), 1.0, places=5)

    def test_draw_cards_preserves_source_and_selection_metadata(self) -> None:
        module = load_script("draw_art_cards.py")

        def fake_fetch(url: str) -> dict:
            if "/search?" in url:
                return {"total": 3, "objectIDs": [101, 102, 103]}
            object_id = int(url.rsplit("/", 1)[-1])
            return {
                "objectID": object_id,
                "isPublicDomain": True,
                "primaryImageSmall": f"https://images.example/{object_id}.jpg",
                "objectURL": f"https://museum.example/{object_id}",
                "title": f"Work {object_id}",
                "artistDisplayName": "Test artist",
            }

        module.fetch_json = fake_fetch
        payload = module.draw_cards("blue", count=3, seed=2, download_dir=None)
        self.assertEqual(payload["count"], 3)
        self.assertEqual([card["card_id"] for card in payload["cards"]], ["card-01", "card-02", "card-03"])
        self.assertTrue(all(card["rights"].startswith("public-domain") for card in payload["cards"]))
        json.dumps(payload, ensure_ascii=False)

    def test_colorfulness_screen_separates_colorful_and_grayscale_pixels(self) -> None:
        module = load_script("draw_art_cards.py")
        colorful = module.colorfulness_from_pixels(
            [(220, 30, 40)] * 8 + [(30, 100, 220)] * 8 + [(235, 190, 30)] * 8
        )
        grayscale = module.colorfulness_from_pixels(
            [(220, 220, 220)] * 8 + [(100, 100, 100)] * 8 + [(30, 30, 30)] * 8
        )
        self.assertGreater(colorful["score"], grayscale["score"])
        self.assertGreater(colorful["hue_coverage"], 0)
        self.assertEqual(grayscale["hue_coverage"], 0)

    def test_palette_friendly_draw_records_screen_metadata(self) -> None:
        module = load_script("draw_art_cards.py")

        def fake_fetch(url: str) -> dict:
            if "/search?" in url:
                return {"total": 3, "objectIDs": [101, 102, 103]}
            object_id = int(url.rsplit("/", 1)[-1])
            return {
                "objectID": object_id,
                "isPublicDomain": True,
                "primaryImageSmall": f"https://images.example/{object_id}.jpg",
                "objectURL": f"https://museum.example/{object_id}",
                "title": f"Work {object_id}",
                "artistDisplayName": "Test artist",
            }

        module.fetch_json = fake_fetch
        module.screen_record_colorfulness = lambda record, **_: {
            **record,
            "colorfulness": {"score": 0.5},
        }
        payload = module.draw_cards(
            "colorful",
            count=3,
            seed=2,
            download_dir=None,
            palette_friendly=True,
            min_colorfulness=0.22,
        )
        self.assertTrue(payload["screen"]["palette_friendly"])
        self.assertEqual(payload["screen"]["min_colorfulness"], 0.22)
        self.assertEqual(payload["count"], 3)
        self.assertTrue(all("colorfulness" in card for card in payload["cards"]))


if __name__ == "__main__":
    unittest.main()
