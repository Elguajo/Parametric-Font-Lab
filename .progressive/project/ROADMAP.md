## Phase 0 — Research
- [x] Phase 0 — Research — `.progressive/phases/00-research/RESEARCH_SPEC.md`

Goal:
Research Metaflop, parametric font engines, UX, licenses,
glyph architecture, Latin/Cyrillic support and validate
the production font pipeline before implementation.

## Phase 1 — Geometric/Technical Sans MVP
- [>] Phase 1 — Geometric/Technical Sans MVP — `.progressive/phases/01-technical-sans-mvp.md`

Goal:
Implement the original cross-script vertical slice, then complete a quality-reviewed Latin + Russian Cyrillic static font workbench.

## Deferred change request — broader Modulator interaction parity
- [ ] After Phase 1 quality closure, decide whether the product needs anatomy guidance, undo/reset history, sharing, additional parameter families, or multi-family selection.

Reason:
The public Modulator interface is a useful interaction reference, but these capabilities materially
expand product scope and validation surface. They are intentionally not scheduled before the static
type-quality gate. Source: https://www.metaflop.com/modulator
