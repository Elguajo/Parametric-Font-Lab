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

## Phase 1b Execution Record — 2026-09-24

Implemented the bounded `basic-latin-russian-v1` source repertoire: all 95 ASCII Basic
Latin positions, NBSP, Russian А–Я/а–я including Ё/ё, and combining acute/dieresis
marks (164 mapped glyphs total).  Every shape is evaluated from original local recipe
code; no external outline, font, or SVG source is read.  The source validator keeps the
repertoire selector, five safe axes (`weight`, `width`, `xHeight`, `roundness`,
`aperture`), O-local counter and the `a`/`0` construction switches bounded.

Recipe output now carries script-aware metric classes and top/bottom mark anchors.  The
derived UFO persists Latin/Cyrillic UFO3 kerning groups and representative class/exception
pairs, which compile to a GPOS PairPos lookup.  The browser chart/specimen covers the full
repertoire, editable Latin/Cyrillic proof text, controlled Text/Display presets and a
source-snapshot A/B comparison; downloaded JSON retains all selected controls.

Observed verification: five Python source/coverage/axis/metrics/kerning tests, a Chrome
browser proof at desktop and 375 px, `py_compile`, `git diff --check`, and a full static
UFO → Designspace → TTF/OTF/WOFF2 export passed.  The compiler validates every expected
cmap/name mapping and requires a GPOS pair-kerning lookup in each compiled output.

Phase 1 remains active for a native-language optical/type-design review and any corrective
spacing work it identifies; variable-font compatibility remains Phase 2 work.

## Phase 1a Review Closure — 2026-09-24

The follow-up review fixed the SVG counter fill: each glyph now uses one nonzero-winding path,
matching the exported contours. Browser controls load the canonical project JSON; numeric and
slider inputs remain in sync, and the page downloads a versioned project with the chosen values.
The Python compiler accepts that file with `--project`, names each static instance by its source
hash, and writes only its own instance directory without clearing unrelated `build/` contents.

The JSON Schema and runtime validator now enforce the exact eight-glyph ID/Unicode/script/recipe
contract. Input size is capped at 64 KiB, compiler subprocesses time out, and generated contours
are checked for zero area and self-intersection before compilation. `npm test` passed 11 Python
tests and the Chrome round-trip test, including customized project → UFO/Designspace →
TTF/OTF/WOFF2, binary outlines/cmap, Cyrillic glyph IDs and a 375 px viewport. `npm run export`,
syntax checks, dependency checks and `git diff --check` passed. Type quality and the full
Latin/Cyrillic repertoire remain Phase 1b work.
