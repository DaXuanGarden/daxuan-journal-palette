#!/usr/bin/env python3
"""Create and update a human-in-the-loop palette review brief.

The palette engine proposes constrained candidates; the author chooses the
direction. This script keeps that handoff machine-readable so a later render
can explain which preference caused a palette or layout change.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


QUESTION_OPTIONS = {
    "visual_direction": [
        {"id": "keep", "label": "保持当前气质", "description": "只修复可读性或局部冲突。"},
        {"id": "airy", "label": "更轻盈明亮", "description": "提高白底上的明度和留白感。"},
        {"id": "colorful", "label": "更丰富鲜明", "description": "提高色彩区分度，但仍保留语义层。"},
        {"id": "warmer", "label": "更温暖", "description": "增加暖色倾向，保留中性和方向编码。"},
        {"id": "cooler", "label": "更冷静", "description": "增加蓝紫或青灰倾向，避免沉重。"},
    ],
    "priority": [
        {"id": "balanced", "label": "均衡", "description": "在审美、可读性和语义之间折中。"},
        {"id": "readability", "label": "可读性优先", "description": "优先保证灰度、CVD、缩印和标签清晰。"},
        {"id": "aesthetics", "label": "审美优先", "description": "优先保持作者选择的视觉气质，再修复硬伤。"},
        {"id": "print", "label": "打印/CVD 优先", "description": "优先保证黑白打印和色觉差异下仍可读。"},
    ],
    "edit_scope": [
        {"id": "palette_only", "label": "只改配色", "description": "锁定几何、标签、图例和数据。"},
        {"id": "palette_legend", "label": "配色加图例", "description": "允许同步调整图例顺序、距离和说明。"},
        {"id": "full_figure", "label": "整图打磨", "description": "允许调整配色、图例、标签和几何细节。"},
    ],
}


def build_review_questions(
    *, figure_type: str = "qualitative", groups: int = 5, background: str = "white"
) -> list[dict[str, Any]]:
    """Return at most three author questions for a palette iteration."""
    return [
        {
            "id": "visual_direction",
            "kind": "single_choice",
            "question": f"这张 {figure_type} 图（约 {groups} 类，{background} 背景）下一轮最想往哪个方向改？",
            "options": deepcopy(QUESTION_OPTIONS["visual_direction"]),
            "recommended": "keep",
        },
        {
            "id": "priority",
            "kind": "single_choice",
            "question": "这一轮最重要的评价标准是什么？",
            "options": deepcopy(QUESTION_OPTIONS["priority"]),
            "recommended": "balanced",
        },
        {
            "id": "edit_scope",
            "kind": "single_choice",
            "question": "允许本轮改动到哪一层？",
            "options": deepcopy(QUESTION_OPTIONS["edit_scope"]),
            "recommended": "palette_only",
        },
    ]


def _feedback_constraints(feedback: str) -> list[dict[str, str]]:
    """Translate common author feedback into explicit constraints."""
    text = feedback.strip().lower()
    constraints: list[dict[str, str]] = []
    rules = [
        (("绿色", "green", "发绿"), "avoid_hues", "green", "作者明确排斥绿色倾向"),
        (("太暗", "黑", "沉重", "dark", "heavy"), "lightness_target", "airy", "作者要求提高明度"),
        (("太灰", "灰灰", "gray", "grey"), "chroma_target", "moderate", "作者要求增加可辨识度"),
        (("鲜艳", "多彩", "丰富", "colorful", "vivid"), "chroma_target", "colorful", "作者希望色彩更丰富"),
        (("暖", "warm"), "preserve_cues", "warm", "作者希望保留暖色线索"),
        (("冷", "cool"), "preserve_cues", "cool", "作者希望保留冷色线索"),
    ]
    for tokens, key, value, reason in rules:
        if any(token in text for token in tokens):
            constraints.append({"key": key, "value": value, "reason": reason})
    return constraints


def create_review_brief(
    *,
    request: str,
    candidates: list[str],
    figure_type: str = "qualitative",
    groups: int = 5,
    background: str = "white",
) -> dict[str, Any]:
    if not request.strip():
        raise ValueError("request must not be empty")
    if not candidates:
        raise ValueError("at least one candidate palette id is required")
    return {
        "schema_version": "1.0",
        "kind": "author-review-brief",
        "status": "awaiting_author",
        "request": request.strip(),
        "figure": {
            "type": figure_type,
            "groups": groups,
            "background": background,
        },
        "candidate_ids": list(dict.fromkeys(candidates)),
        "questions": build_review_questions(
            figure_type=figure_type, groups=groups, background=background
        ),
        "guardrails": [
            "keep data values and semantic layer assignments fixed unless the author explicitly changes them",
            "show candidates with identical geometry and export settings before comparing palettes",
            "translate free-text feedback into preference_constraints and preserve rejected candidates",
            "pause before changing a production figure until the author selects a direction",
        ],
        "decision_log": [],
        "provenance": {
            "script": "scripts/author_review.py",
            "purpose": "human-in-the-loop palette iteration",
        },
    }


def record_review(
    brief: dict[str, Any],
    *,
    selection: str | None = None,
    feedback: str = "",
    answers: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Append one author decision without mutating the input object."""
    updated = deepcopy(brief)
    candidates = set(updated.get("candidate_ids", []))
    if selection and selection not in candidates:
        raise ValueError(f"selection {selection!r} is not one of candidate_ids")
    answers = answers or {}
    constraints = _feedback_constraints(feedback)
    event = {
        "recorded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "selection": selection,
        "answers": dict(answers),
        "feedback": feedback.strip(),
        "preference_constraints": constraints,
    }
    updated.setdefault("decision_log", []).append(event)
    if selection and not feedback.strip():
        updated["status"] = "direction_selected"
    elif feedback.strip():
        updated["status"] = "revision_requested"
    else:
        updated["status"] = "needs_clarification"
    updated["active_constraints"] = constraints
    return updated


def _write_or_print(payload: dict[str, Any], output: Path | None) -> None:
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="create an author review brief")
    create.add_argument("--request", required=True)
    create.add_argument("--candidate", action="append", required=True)
    create.add_argument("--figure-type", default="qualitative")
    create.add_argument("--groups", type=int, default=5)
    create.add_argument("--background", default="white")
    create.add_argument("--output", type=Path)

    record = sub.add_parser("record", help="record one author selection or feedback")
    record.add_argument("--brief", type=Path, required=True)
    record.add_argument("--selection")
    record.add_argument("--feedback", default="")
    record.add_argument("--answer", action="append", default=[], help="question_id=value")
    record.add_argument("--output", type=Path)

    args = parser.parse_args()
    if args.command == "create":
        payload = create_review_brief(
            request=args.request,
            candidates=args.candidate,
            figure_type=args.figure_type,
            groups=args.groups,
            background=args.background,
        )
        _write_or_print(payload, args.output)
        return

    brief = json.loads(args.brief.read_text(encoding="utf-8"))
    answers: dict[str, str] = {}
    for raw in args.answer:
        if "=" not in raw:
            raise SystemExit(f"invalid --answer {raw!r}; use question_id=value")
        key, value = raw.split("=", 1)
        answers[key] = value
    payload = record_review(
        brief,
        selection=args.selection,
        feedback=args.feedback,
        answers=answers,
    )
    _write_or_print(payload, args.output)


if __name__ == "__main__":
    main()
