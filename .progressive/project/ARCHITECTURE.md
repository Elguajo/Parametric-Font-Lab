# Architecture — Parametric Font Lab

Status: PROPOSED FROM PHASE 0; no production runtime exists

The repository currently contains PCK governance and research assets only. Phase 1 is proposed to create an original deterministic glyph-recipe evaluator, versioned JSON source model, browser preview and isolated Python compiler. Derived UFO masters and Designspace feed fontmake/fontTools for validated binaries. Latin and Cyrillic share metrics/primitives but own script-specific recipes and quality tests; structural variants use separate topology families.

Trust boundary: project JSON is validated before geometry evaluation; later font uploads require a separate sandbox/size-limit design. Browser preview is provisional; Python export is authoritative. PCK phase state remains in `.progressive/`, not in product JSON.

Research architecture and decision rationale: `research/font-lab/architecture/`, `research/font-lab/decisions/`, and `research/font-lab/final/RESEARCH_REPORT.md`. ADRs are proposed for Phase 1 implementation, not evidence that the system is built.
