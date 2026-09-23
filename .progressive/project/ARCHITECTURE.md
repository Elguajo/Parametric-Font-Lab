# Architecture — Parametric Font Lab

Status: PHASE 1 IN PROGRESS; Phase 1a runtime and static compiler implemented

Phase 1a contains an original deterministic glyph-recipe evaluator, versioned JSON source model,
browser SVG preview and isolated Python compiler for the cross-script `H/O/a/0` and `Н/О/а/о`
slice. Derived UFO and Designspace sources feed fontmake/fontTools for validated static binaries.
Latin and Cyrillic share metrics/primitives but own script-specific recipes and quality tests;
structural variants use separate topology families. Phase 1b extends the repertoire and adds
type-quality, spacing and kerning work.

Trust boundary: project JSON is validated before geometry evaluation; later font uploads require a separate sandbox/size-limit design. Browser preview is provisional; Python export is authoritative. PCK phase state remains in `.progressive/`, not in product JSON.

Research architecture and decision rationale: `research/font-lab/architecture/`, `research/font-lab/decisions/`, and `research/font-lab/final/RESEARCH_REPORT.md`. ADRs are proposed for Phase 1 implementation, not evidence that the system is built.
