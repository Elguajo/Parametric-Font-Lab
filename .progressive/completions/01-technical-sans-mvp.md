# Phase 01 Completion — Geometric/Technical Sans MVP

Status: COMPLETED
Date: 2026-09-24

## Outcome
An original static Technical Sans workbench is complete for ASCII Basic Latin, NBSP, Russian
Cyrillic including `Ё/ё`, and acute/dieresis marks. The browser and compiled TTF/OTF/WOFF2
proofs represent the evaluated source, and selected project JSON exports its corresponding
static instance.

## Delivered
- Bounded original recipe evaluator for 164 mapped glyphs, five axes, O-local counter, and
  `a`/`0` construction switches.
- SVG outline, generated glyph chart, editable specimen, Text/Display presets, source snapshot,
  and downloadable versioned project JSON.
- Deterministic UFO/Designspace → TTF/OTF/WOFF2 compiler with cmap, metrics, GPOS PairPos and
  MarkToBase, contour, and source-hash manifest checks.
- Browser outcome regressions for SVG orientation, generated chart contours, source-anchor mark
  placement, and source/preview parity; export routing regression for custom and absent projects.

## Implementation notes
The browser maps positive-up font coordinates through one shared SVG transform. Combining marks
align both `top` and `_top` source-anchor coordinates. `h` and `n` are structurally and
metrically distinct; `U` is overlap-removed into one compiled outline; `A/А` compile into one
outer outline plus one intentional oppositely wound counter. `npm run export` forwards
`--project` and `--output-dir` to both compilation and WOFF2 browser proof.

## Decisions made
- Retain the bounded original static-workbench direction; do not add broader Modulator workflow
  parity, additional engines, or variable-font compatibility to this phase.
- Treat browser SVG as source-faithful interactive proof and compiled binaries as export truth.
- Retain the 2026-09-24 audit's deferred workflow, spacing, and variable-font work as post-phase
  decisions rather than expanding Phase 1.

## Deviations / technical debt
- The Phase 1 proof review is evidence-based agent review, not external professional type-design
  certification. Future production distribution can commission an independent human review.
- Variable-font masters/compatibility and the deferred workflow request remain unscheduled.

## Problems discovered
The audit exposed direct positive-up coordinates in SVG, a system-font chart, horizontal-only
mark attachment, mechanically identical `h/n`, disconnected `U`, inconsistent `A` component
winding, and npm argument routing that silently compiled the default project. All have focused
regressions now.

## Verification evidence
- `npm test` → 15 Python recipe tests, Chromium workbench proof, and custom-project export
  routing passed.
- `npm run export` → Text TTF/OTF/WOFF2 compiled; compiled WOFF2 loaded and proved at 10, 14,
  24, and 72 px.
- A current Display project (`weight=124`, `width=1.08`, `xHeight=520`, `roundness=.9`,
  `aperture=.72`, single-storey `a`, slashed `0`) compiled to TTF/OTF/WOFF2 and passed the same
  WOFF2 proof.
- An isolated copy completed `npm run setup`, `npm test`, and `npm run export` with pinned
  dependencies; `py_compile`, JavaScript syntax checks, and `git diff --check` passed.
- Source/compiled inspection uses FontTools glyph-set pens; current OpenType references confirm
  non-zero winding and Type 4 MarkToBase semantics.

## Architectural impact
Later work can depend on a versioned project source, source-faithful browser proof, isolated
static export instance directories, and full Latin/Cyrillic static binary validation. Current
architecture: `.progressive/project/ARCHITECTURE.md`.

## Follow-up
- Decide whether to schedule the deferred workflow request or a separate variable-font phase.
