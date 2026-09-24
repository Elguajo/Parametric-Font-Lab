# Architecture — Parametric Font Lab

Status: PHASE 1 IN PROGRESS; Phase 1b static workbench and scoped optical corrections are verified, but full-repertoire optical closure remains open

The implemented workbench has an original deterministic glyph-recipe evaluator and versioned JSON
source model for 164 mapped glyphs: ASCII Basic Latin, NBSP, Russian А–Я/а–я including Ё/ё and
combining acute/dieresis. Five bounded source controls, O-local counter and discrete `a`/`0`
branches produce browser SVG previews and derived UFO/Designspace sources. The isolated Python
compiler emits static TTF, CFF OTF and WOFF2, checks cmap/outline tables and requires a GPOS
PairPos kerning lookup. Latin/Cyrillic share primitives while retaining script-qualified metrics,
anchors and kerning groups.

The current browser supports chart/specimen proofing, controlled Text/Display presets, project
download and source-snapshot A/B comparison. It does not implement Modulator's font selection,
full parameter breadth, anatomy/tutorial surface, undo/reset history or share flow; those are
future product work, not present architecture.

Trust boundary: project JSON is validated before geometry evaluation; later font uploads require a separate sandbox/size-limit design. Browser preview is provisional; Python export is authoritative. PCK phase state remains in `.progressive/`, not in product JSON.

Research architecture and decision rationale: `research/font-lab/architecture/`, `research/font-lab/decisions/`, and `research/font-lab/final/RESEARCH_REPORT.md`. ADRs are proposed for Phase 1 implementation, not evidence that the system is built.
