## Phase 0 — Research
- [x] Phase 0 — Research — `.progressive/phases/00-research/RESEARCH_SPEC.md`

Goal:
Research Metaflop, parametric font engines, UX, licenses,
glyph architecture, Latin/Cyrillic support and validate
the production font pipeline before implementation.

## Phase 1 — Geometric/Technical Sans MVP
- [x] Phase 1 — Geometric/Technical Sans MVP — `.progressive/phases/01-technical-sans-mvp.md`

Goal:
Implement the original cross-script vertical slice, repair its trustworthy preview/recipe/export path, then complete a quality-reviewed Latin + Russian Cyrillic static font workbench.

Completed: faithful browser proofing, the audit's verified recipe defects, selected-project
export routing, and the evidence-based script-aware Text/Display proof review. Source:
`research/font-lab/audits/2026-09-24-product-technical-audit.md`.

## Deferred change request — workbench workflow and broader Modulator interaction parity
- [ ] After Phase 1 quality closure, decide whether the product needs project reopen/save, undo/reset, visual A/B, a user-accessible font-export path, anatomy guidance, sharing, additional parameter families, or multi-family selection.
- [ ] After the workflow decision, decide whether a shared declarative recipe model, axis-aware spacing/kerning, and Russian usage punctuation are warranted before wider style-engine expansion.

Reason:
The public Modulator interface is a useful interaction reference, but these capabilities materially
expand product scope and validation surface. The audit identified them as valuable follow-up, not
Phase 1 acceptance work. They are intentionally not scheduled before the static type-quality gate.
Sources: https://www.metaflop.com/modulator and
`research/font-lab/audits/2026-09-24-product-technical-audit.md`.
