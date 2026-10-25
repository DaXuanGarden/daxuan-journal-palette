# Creation Handoff

## 1. Result

- Skill: daxuan-journal-palette 0.9.0
- Job: 为科研论文图表选择、映射和审查艺术化配色，并输出可复用代码。
- Path: /home/daxuan/.codex/skills/daxuan-journal-palette
- Publication: local only; no repository, release or marketplace publication was requested.

## 2. Reference skills studied

- K-Dense-AI/scientific-agent-skills:scientific-visualization — source https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-visualization; 2026-10-01 skills.sh installs 2.1K and SkillsMP repository stars 46,512. Learned evidence-first figure workflow, semantic palette selection, contrast/gray checks, journal/export constraints and explicit non-claims. Applied to the compact workflow, audit reference and output contract.
- local easyplot — inspected /home/daxuan/.codex/skills/easyplot/SKILL.md, palette library, China recipes and publication QA. Learned named palette recipes, CVD/grayscale diagnostics, retaining a user palette unless approved, and separating curated swatches from claims. Applied to the atlas and audit boundary.
- local nature-figure — inspected design theory and figure contract. Learned claim-first figure architecture, semantic color roles and cross-panel consistency. Applied to Router Rules and the review checklist.
- local journal-ggplot-stylebook — inspected style guide. Learned practical ggplot2 and export conventions. Applied to the R code contract and publication checks.
- jakubkrehel/skills:better-colors — source https://github.com/jakubkrehel/skills/tree/main/skills/better-colors; 2026-10-01 skills.sh installs 24.8K. Learned semantic roles and measuring actual rendered contrast. UI token architecture was intentionally not adopted.

## 3. Absorbed and rejected

- Keep: semantic palettes, fixed mappings across panels, actual-image diagnostics, explicit assumptions, and provenance boundaries.
- Adapt: Chinese/oriental recipes are presented as visual design families, not historical facts; the workflow is lightweight and Chinese-first for GWAS/omics figure authors.
- Reject: UI/brand tokens, copied long palette libraries, automatic journal-compliance claims, and color-only communication of statistical direction.
- Invent: the ink-mineral-a A family, its sunlit white-background variant, a multi-family Chinese-first atlas, and an output contract that always returns HEX plus R/Python mappings and audit status.

## 6. 0.2.0 expansion

- Added `references/style-taxonomy.md`, which maps 18 visual families to figure tasks, category limits, medium risks and starting recipes.
- Extended `references/palette-atlas.md` with literati paper, blue-and-white porcelain, tea-earth botanical, coastal mineral, desert clay, alpine lake, editorial jewel, graphite-copper and impressionist-muted recipes.
- Added style rationale, palette type, provenance and art-specific checks to the routing and output contract.

## 7. 0.3.0 visual and public-release expansion

- Added a JSON-backed palette gallery with 26 cards, interactive HTML filtering, SVG overview, CSV export and grayscale proxies.
- Added a standard-library-only gallery builder so palette updates regenerate all visual outputs deterministically.
- Added MIT LICENSE, GitHub Actions validation and a GitHub public-release reference. The public repository is `https://github.com/DaXuanGarden/daxuan-journal-palette` and release `v0.3.0` is published.

## 8. 0.3.1 artistic-source expansion

- Added `references/artistic-inspiration.md` with source tiers for palette repositories, museum open data, rights/provenance fields and artist-principle-to-figure translations.
- Added six visual translation recipes: atmospheric impressionism, blue/yellow accent, flat geometric colour, field relationships, indigo print grammar and modern ink/mineral.
- Extended the gallery registry and CSV/HTML output with optional inspiration metadata while preserving backwards compatibility for existing palette cards.

## 9. 0.4.0 open-card-draw expansion

- Added `references/card-draw-workflow.md` for public-domain, generated and hybrid card draws, selection-before-extraction, provenance and internalization rules.
- Added `scripts/draw_art_cards.py` for reproducible 3–10 card draws from The Met's paginated public-domain search and object metadata API; v0.5.5 adds palette-friendly colorfulness screening and multi-query candidate pools.
- Added `scripts/extract_palette.py` for optional Pillow-based RGB k-means extraction with seed, source, rights and candidate-only status.
- Added deterministic tests and CI help/compile checks for both scripts. The package still keeps image assets outside the repository by default.

## 10. 0.5.0 fast-router expansion

- Added `palette-index.json` with keyword, figure-type, best-for and risk metadata for fast matching across the 32 built-in palettes.
- Added `scripts/route_palette.py`: ordinary requests return one primary palette and up to two alternatives; explicit card-draw wording returns a draw mode with default count 5 or count 1 for a single-card request.
- Reduced default questions to figure type, group count and background; detailed provenance remains available without expanding the normal response.
- Added router regression tests and kept the full palette atlas as an on-demand reference.

## 0.5.6 SCI palette integration

- Added `scripts/sci_palette_bridge.py` as an explicit-path adapter to the local `sci-color-palettes` package. It keeps Daxuan visual families separate from SCI application scoring and does not duplicate the 184-colour registry.
- Added `references/sci-color-palettes-bridge.md` with field mapping, categorical versus diverging rules, and the three semantic layers used by the current LDSC/Genova/HDL circular heatmap.
- Added bridge tests for application-field routing, `sp.select()` categorical subsets, centred `div-*` ramps and the circular-heatmap contract.
- Added `audit_hex()` so Daxuan or image-extracted candidates can use the same SCI diagnostics without being copied into the SCI registry.
- The recommended workflow is: SCI application gate -> Daxuan semantic/style mapping -> actual-size CVD/grayscale/print review. Automated scores remain diagnostic evidence, not journal certification.

## 0.5.7 joint card-SCI expansion

- Added `scripts/joint_palette_draw.py` to combine a seeded 1–10 card draw with SCI-ranked categorical, diverging-heatmap and circular-layer candidates.
- Added `references/joint-card-sci-workflow.md` to make the separation explicit: image palettes guide mood, intact SCI ramps carry semantic meaning, and cross-layer colour splicing is prohibited.
- Added JSON, PNG and HTML outputs and regression tests; the current 10-card project replay is stored outside the public Skill under the GWAS QA directory.

## 11. 0.8.0 candidate-diversity expansion

- Added `scripts/palette_distance.py`, a dependency-free CIE76/CIELAB screening helper for palette-pair distance.
- Updated `scripts/route_palette.py` to require distinct visual families and a default symmetric mean-nearest `ΔE76 >= 18` for A/B/C candidates; near-duplicates are returned in `rejected_candidates` with reasons.
- Added per-candidate family, distance and distinctness fields plus a machine-readable `candidate_diversity` audit and explicit fallback reporting.
- Added regression tests and documented the gate in the output contract and human-review workflow.

## 12. 0.9.0 theme-aware direction expansion

- Added `scripts/theme_palette.py` to convert a paper title, text fragment and figure meaning into topic anchors, visual metaphors, public-domain image queries and directional A/B/C palette candidates.
- Added explicit sedentary-cardiovascular direction profiles: vascular-clinical, circulation-energy and biological-equilibrium. Each direction has a visual rationale, theme fit and avoid list.
- Added CIE76/family checks to direction selection, an `awaiting_author` handoff, and provenance stating that images are visual cues rather than scientific evidence.
- Added `references/theme-to-palette.md` and regression tests for theme detection, directional separation and generic fallback.

## 4. Advantages and evidence

| Label | Statement | Evidence |
|---|---|---|
| design advantage | The atlas covers qualitative, sequential, diverging and neutral+accent use cases with explicit caveats. | references/palette-atlas.md |
| design advantage | The response contract separates semantic mapping, code, diagnostics, assumptions and evidence limits. | references/output-contract.md |
| validated advantage | Package structure and trigger boundaries are checked by the Qiaomu validator and trigger evaluator. | reports/trigger-eval.json and local validation output |
| hypothesis | Named artistic families may improve hierarchy and reviewability in dense biomedical figures. | Human comparison and provider-backed evidence are missing evidence. |

## 5. Verification and limits

The package is intended for local team reuse and public GitHub distribution. Validation, trigger evaluation and IR export are run after creation. The selected ink-mineral-a palette was manually applied to the insomnia/NAFLD GO-BP figure script as a first use case; this is not an automatic recoloring service. The open card draw is an exploratory input workflow, not an automatic recoloring service. A passing trigger/package check demonstrates routing and package integrity; it does not prove that every HEX combination is color-vision safe, print-safe or preferred by a journal.

Copyright (c) 大轩  
GitHub: https://github.com/DaXuanGarden
