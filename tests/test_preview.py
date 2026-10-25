from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

try:
    import PIL  # noqa: F401
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


ROOT = Path(__file__).resolve().parents[1]


def load_preview():
    path = ROOT / "scripts" / "render_palette_preview.py"
    spec = importlib.util.spec_from_file_location("render_palette_preview", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PalettePreviewTests(unittest.TestCase):
    @unittest.skipUnless(PIL_AVAILABLE, "Pillow is an optional preview dependency")
    def test_preview_writes_five_panel_card_and_manifest(self) -> None:
        preview = load_preview()
        with tempfile.TemporaryDirectory() as tmp:
            result = preview.render_preview(
                ["#6D98AF", "#7DACA3", "#CBA064", "#CE8793", "#A28BAF"],
                tmp,
                title="circular category ring",
            )
            self.assertTrue(Path(result["png"]).is_file())
            self.assertTrue(Path(result["json"]).is_file())
            self.assertEqual(
                result["panels"],
                ["normal", "grayscale", "protanopia", "deuteranopia", "target-size"],
            )
            self.assertEqual(len(result["colors"]), 5)

    @unittest.skipUnless(PIL_AVAILABLE, "Pillow is an optional preview dependency")
    def test_preview_rejects_invalid_hex(self) -> None:
        preview = load_preview()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                preview.render_preview(["not-a-colour"], tmp)


if __name__ == "__main__":
    unittest.main()
