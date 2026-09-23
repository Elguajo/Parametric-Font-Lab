# Phase 01 — Geometric/Technical Sans MVP

## Goal
Deliver an original, validated static font design workbench for basic Latin and Russian Cyrillic.

## Context
Phase 0 findings and proposed ADRs: `research/font-lab/final/RESEARCH_REPORT.md`. Full release scope: `research/font-lab/final/mvp-scope.md`.

## In scope
- Phase 1a cross-script vertical slice described in the research report §9.
- Phase 1b full basic Latin + Russian Cyrillic, controlled axes, selected switches, presets/A-B and static export after type quality review.

## Out of scope
- Production variable font release, arbitrary morphing, full Bézier editor and other style engines.

## Tasks
- [x] Implement and verify Phase 1a source/preview/export vertical slice.
- [ ] Author and review complete V1 Latin + Russian Cyrillic glyph repertoire.
- [ ] Add controlled UI, presets/A-B, spacing/kerning and static export validation.

## Acceptance criteria
- [ ] Original recipes generate and preview the agreed repertoire and named variants.
- [ ] Latin/Cyrillic text, metrics, marks and kerning pass script-aware proof review.
- [ ] Deterministic project JSON round-trips; static OTF/TTF/WOFF2 compile and pass table/shape checks.
- [ ] Browser interactions, errors and export work from a clean checkout with pinned dependencies and notices.

## Negative / security cases
- Reject malformed source, invalid axes/switches, incompatible contours and resource-exhausting export requests.
- No third-party font outline import or GPL source reuse.

## Verification
- Follow `.progressive/system/QUALITY_PROTOCOL.md`; focused schema/geometry/build/browser tests plus Latin/Cyrillic specimen review.

## Completion Record
Pending.

## Phase 1a Execution Record — 2026-09-24

Implemented the original eight-glyph vertical slice in `fontlab/project.json`: `H/O/a/0`
and `Н/О/а/о`. The versioned JSON Schema rejects unknown fields, invalid ranges and invalid
switches. The deterministic Python evaluator applies shared `weight`, scopes `counter` to
Latin `O`, and selects a topology-distinct Latin `a` family without changing Cyrillic `а`.

`web/` provides the responsive SVG outline, glyph chart and editable Latin/Cyrillic specimen.
The isolated compiler writes derived UFO and Designspace sources, then static TTF, CFF OTF and
WOFF2 to `build/`; generated artifacts are ignored. `npm test` passed six Python contract and
geometry tests plus a Chrome preview/parity test. `npm run export` passed table, outline and cmap
checks for all eight Unicode mappings with fontTools 4.66.0.

Phase 1 remains active: full basic Latin/Russian Cyrillic repertoire, script proofing,
metrics/kerning, presets and later quality review belong to Phase 1b.
