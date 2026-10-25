from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_review():
    path = ROOT / "scripts" / "author_review.py"
    spec = importlib.util.spec_from_file_location("author_review", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuthorReviewTests(unittest.TestCase):
    def test_brief_asks_three_bounded_questions_and_stops(self) -> None:
        review = load_review()
        brief = review.create_review_brief(
            request="改进当前 LDSC 环形热图配色",
            candidates=["ink-mineral-a-sunlit", "div-plum-blue"],
            figure_type="circular",
            groups=5,
        )
        self.assertEqual(brief["status"], "awaiting_author")
        self.assertEqual(len(brief["questions"]), 3)
        self.assertIn("pause before changing", " ".join(brief["guardrails"]))

    def test_feedback_becomes_constraints_and_preserves_log(self) -> None:
        review = load_review()
        brief = review.create_review_brief(
            request="palette iteration", candidates=["a", "b"]
        )
        updated = review.record_review(
            brief,
            selection="a",
            feedback="不要绿色，太暗，希望更丰富",
            answers={"priority": "readability"},
        )
        self.assertEqual(updated["status"], "revision_requested")
        self.assertEqual(len(updated["decision_log"]), 1)
        pairs = {(row["key"], row["value"]) for row in updated["active_constraints"]}
        self.assertIn(("avoid_hues", "green"), pairs)
        self.assertIn(("lightness_target", "airy"), pairs)
        self.assertIn(("chroma_target", "colorful"), pairs)
        self.assertEqual(brief["decision_log"], [])

    def test_selection_must_be_one_of_present_candidates(self) -> None:
        review = load_review()
        brief = review.create_review_brief(request="x", candidates=["a"])
        with self.assertRaises(ValueError):
            review.record_review(brief, selection="missing")


if __name__ == "__main__":
    unittest.main()
