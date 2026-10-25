from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from functools import wraps


ROOT = Path(__file__).resolve().parents[1]


def load_bridge():
    path = ROOT / "scripts" / "sci_palette_bridge.py"
    spec = importlib.util.spec_from_file_location("sci_palette_bridge", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def requires_sci(test):
    @wraps(test)
    def wrapped(self, *args, **kwargs):
        bridge = load_bridge()
        if bridge.discover_sci_root() is None:
            self.skipTest("sci-color-palettes is an optional local dependency")
        return test(self, *args, **kwargs)

    return wrapped


class SciBridgeTests(unittest.TestCase):
    def test_field_aliases_and_inference(self) -> None:
        bridge = load_bridge()
        self.assertEqual(bridge.normalize_field("数据库"), "database")
        self.assertEqual(bridge.infer_field(figure_type="GWAS heatmap"), "basic")
        self.assertEqual(bridge.infer_field(groups=8), "database")

    @requires_sci
    def test_categorical_selection_preserves_real_ramp_members(self) -> None:
        bridge = load_bridge()
        result = bridge.categorical_recommendations(field="database", n=5)
        self.assertEqual(result["kind"], "categorical")
        self.assertGreaterEqual(len(result["recommendations"]), 1)
        row = result["recommendations"][0]
        self.assertEqual(len(row["selected_hex"]), 5)
        self.assertTrue(set(row["selected_hex"]) <= set(row["hex"]))
        self.assertTrue(row["fits"])
        self.assertIn("selected_audit", row)
        self.assertIn("cvd", row["selected_audit"])

    @requires_sci
    def test_arbitrary_palette_can_be_audited_without_registry_mutation(self) -> None:
        bridge = load_bridge()
        result = bridge.audit_hex(["#123456", "#D95F59", "#E6AB02"])
        self.assertEqual(result["n"], 3)
        self.assertEqual(len(result["hex"]), 3)
        self.assertIn("deuteranopia", result["cvd"])
        self.assertIn("contrast_on_white", result)

    @requires_sci
    def test_diverging_ramp_has_original_centre(self) -> None:
        bridge = load_bridge()
        result = bridge.diverging_recommendations(n=7)
        self.assertGreaterEqual(len(result["recommendations"]), 1)
        row = result["recommendations"][0]
        self.assertEqual(row["centre_index_zero_based"], 3)
        self.assertEqual(row["centre_hex"], row["hex"][3])
        self.assertEqual(len(row["selected_hex"]), 7)

    @requires_sci
    def test_current_circular_heatmap_contract_separates_layers(self) -> None:
        bridge = load_bridge()
        result = bridge.circular_heatmap_recommendation(
            categories=5,
            avoid_hues=["green"],
            lightness_target="airy",
            chroma_target="moderate",
            preserve_cues=["yellow/olive"],
        )
        layers = {layer["layer"]: layer for layer in result["semantic_layers"]}
        self.assertIn("outcome_category_ring", layers)
        self.assertIn("signed_ldsc_heat_ring", layers)
        self.assertIn("validation_ring", layers)
        self.assertEqual(layers["outcome_category_ring"]["field"], "database")
        self.assertEqual(layers["signed_ldsc_heat_ring"]["kind"], "diverging")
        self.assertEqual(result["preference_constraints"]["avoid_hues"], ["green"])
        self.assertEqual(result["preference_constraints"]["chroma_target"], "moderate")
        self.assertTrue(layers["signed_ldsc_heat_ring"]["rejected_candidates"])
        self.assertIn("never splice", " ".join(result["policy"]))

    def test_sci_root_discovery_and_optional_fallback_are_actionable(self) -> None:
        bridge = load_bridge()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts" / "sci_palettes").mkdir(parents=True)
            self.assertEqual(bridge.discover_sci_root(root), root.resolve())
            missing = root / "missing"
            result = bridge.circular_heatmap_fallback(
                categories=5,
                reason="test",
                avoid_hues=["green"],
                lightness_target="airy",
                chroma_target="moderate",
                preserve_cues=["yellow/olive"],
            )
            self.assertEqual(result["sci_status"], "unavailable")
            self.assertEqual(result["fallback"], "daxuan-atlas")
            self.assertEqual(result["preference_constraints"]["avoid_hues"], ["green"])
            self.assertEqual(result["preference_constraints"]["lightness_target"], "airy")
            with self.assertRaises(FileNotFoundError) as context:
                bridge.load_sci(missing)
            self.assertIn("SCI_COLOR_PALETTES_ROOT", str(context.exception))

    def test_non_circular_missing_sci_has_machine_readable_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "sci_palette_bridge.py"),
                    "--figure",
                    "categorical",
                    "--sci-root",
                    str(Path(tmp) / "missing"),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(completed.stdout)
            self.assertEqual(payload["sci_status"], "unavailable")
            self.assertEqual(payload["fallback"], "daxuan-atlas")


if __name__ == "__main__":
    unittest.main()
