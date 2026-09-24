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

Historical completion remains intact. The later type-quality review found additional defects
and a gap between technical proof and readable text; it is a new change request, not a retroactive
rewrite of Phase 1.

## Change request — type quality and trustworthy proof
- [x] Phase 02 — Type-quality foundation — `.progressive/phases/02-type-quality-foundation.md`
- [x] Phase 02a — Inter-derived readable foundation — `.progressive/phases/02a-inter-derived-foundation.md`
- [>] Phase 03 — Product-specific differentiation on the Inter base — `.progressive/phases/03-pfl-sans-differentiation.md`

Phase 02's original v2 result passed its technical checks but was rejected in product review for
visual quality. Phase 02a changed the default source and made v1/v2 legacy paths. The earlier
plan to extend original recipe corrections to all 164 glyphs is superseded; it is not the next
automatic task. A production variable font remains a separate future decision.

Source: `research/font-lab/audits/2026-09-24-type-quality-change-review.md` and
`research/font-lab/decisions/ADR-011-type-quality-source-strategy.md`.
The current default source decision is `research/font-lab/decisions/ADR-012-inter-derived-foundation.md`.

## Deferred change request — workbench workflow and broader Modulator interaction parity
- [ ] After the type-quality change request closes, decide whether the product needs project reopen/save, undo/reset, visual A/B, a user-accessible font-export path, anatomy guidance, sharing, additional parameter families, or multi-family selection.
- [ ] After the workflow decision, decide whether a shared declarative recipe model and Russian usage punctuation are warranted before wider style-engine expansion.

Reason:
The public Modulator interface is a useful interaction reference, but these capabilities materially
expand product scope and validation surface. The audit identified them as valuable follow-up, not
Phase 1 acceptance work. They are intentionally not scheduled before the static type-quality gate.
Sources: https://www.metaflop.com/modulator and
`research/font-lab/audits/2026-09-24-product-technical-audit.md`.
