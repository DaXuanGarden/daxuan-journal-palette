# Prior-Art Research

- Researched at: 2026-10-01
- Queries: scientific journal figure color palettes publication; ggplot publication palette color vision deficiency accessibility; Chinese ink wash palette scientific visualization; Nature Cell journal figure color style
- Catalogs: skills.sh, SkillsMP, GitHub source review
- Rating evidence: unavailable; installs and repository stars are adoption/attention signals, not ratings or correctness
- Unified candidate record: [prior-art-candidates.json](prior-art-candidates.json)

| Candidate | Relevance | skills.sh installs | SkillsMP repo stars | Quality/trust evidence | Adopt | Reject | License |
|---|---|---:|---:|---|---|---|---|
| K-Dense-AI/scientific-agent-skills:scientific-visualization | Evidence-first scientific figure workflow | 2.1K | 46,512 | Canonical GitHub source inspected; source review only | Semantic palette selection, journal/export checks, provenance, non-claims | Broad scope and heavier workflow than this focused palette task | Source license needs to be checked before redistribution; only principles adopted |
| local easyplot | Palette recipes and publication QA | local | local | Installed source inspected | Exact HEX recipes, CVD/grayscale checks, China/oriental palette families, retain user palette | Do not copy its full library or assume its audit certifies a figure | Local package; referenced, not vendored |
| local nature-figure | Claim-first figure architecture | local | local | Installed source inspected | Semantic roles, one neutral/signal/accent family, cross-panel consistency, journal dimensions | Nature-specific framing is not a universal journal rule | Local package; referenced, not vendored |
| local journal-ggplot-stylebook | R figure and export conventions | local | local | Installed source inspected | R/ggplot2 mapping and export-oriented review | Stylebook examples do not prove accessibility or acceptance | Local package; referenced, not vendored |
| jakubkrehel/skills:better-colors | Named palette/ramp and measured contrast principles | 24.8K | not returned | Canonical GitHub source inspected; UI-focused | Semantic roles and actual rendered contrast measurement | UI token architecture and product-brand assumptions | Source license needs to be checked before redistribution; only principles adopted |

## Original contribution

This package connects a Chinese-first artistic palette atlas to a strict scientific output contract: every recommendation keeps semantic group order, provides exact R/Python mappings, and separates visual design from accessibility diagnostics and publication claims. The ink-mineral-a family records the user's selected A direction; the sunlit variant raises luminance for dense white-background figures without presenting it as historical or journal-official color.

## What we learned from each candidate

- scientific-visualization: use an evidence-first sequence, specify journal/export constraints, and preserve provenance. Applied in SKILL.md, accessibility-and-print.md, and the output contract.
- easyplot: maintain named recipes, support Chinese/oriental visual families, and treat CVD/grayscale as diagnostics. Applied in palette-atlas.md and the audit boundary.
- nature-figure: define colors by figure semantics and keep them stable across panels. Applied in Router Rules and output-contract.md.
- journal-ggplot-stylebook: provide practical ggplot2 mappings and publication-oriented export checks. Applied in the R example and review checklist.
- better-colors: measure actual rendered contrast and use semantic roles. Applied as a principle; UI-specific token systems were not carried over.

## Created skill advantages

- Design advantage: a single atlas covers qualitative, sequential, diverging and neutral+accent use cases with explicit caveats.
- Design advantage: the output contract forces the response to distinguish semantic mapping, HEX, code, audit evidence and assumptions.
- Validated advantage: local package structure and all trigger cases are validated by the Qiaomu scripts; this supports routing/package integrity, not visual superiority.
- Hypothesis: named artistic families plus a consistent semantic mapping should make dense biomedical figures easier to review; provider-backed comparison and human figure-panel testing are missing evidence.

## Deliberate rejection

- UI/branding color systems were rejected because they optimize interaction states or brand recall, not scientific figure semantics.
- Large copied palette libraries were rejected to keep the package maintainable and to avoid treating source swatches as official cultural or journal standards.
- Automatic journal-compliance claims were rejected because no journal review or printed proof exists.

## Missing evidence

- No human comparison of the styles on the insomnia/NAFLD figure has been run.
- No provider-backed or journal-editor review is available.
- No physical print proof, color-profile conversion or formal WCAG-style audit of every atlas combination has been performed.
- Candidate rating/review fields were not available in the inspected catalogs.
