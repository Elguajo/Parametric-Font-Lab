# Phase 01 — Geometric/Technical Sans MVP

## Goal
Deliver an original, validated static font design workbench for basic Latin and Russian Cyrillic.

## Context
Phase 0 findings and proposed ADRs: `research/font-lab/final/RESEARCH_REPORT.md`. Full release scope: `research/font-lab/final/mvp-scope.md`.

## In scope
- Phase 1a cross-script vertical slice described in the research report §9.
- Phase 1b full basic Latin + Russian Cyrillic, controlled axes, selected switches, presets/A-B and static export after type quality review.
- Correct the accepted evidence from `research/font-lab/audits/2026-09-24-product-technical-audit.md`: faithful SVG outline/chart/specimen proofing, the verified `h`/`n`, `U`, and `A` recipe/contour defects, and selected-project export routing.

## Out of scope
- Production variable font release, arbitrary morphing, full Bézier editor and other style engines.

## Tasks
- [x] Implement and verify Phase 1a source/preview/export vertical slice.
- [x] Author and review complete V1 Latin + Russian Cyrillic glyph repertoire.
- [x] Add controlled UI, presets/A-B, spacing/kerning and static export validation.
- [x] Repair audit findings 1–3 and add outcome-based regressions for browser rendering, recipes and selected-project export.

## Acceptance criteria
- [x] Original recipes generate and preview the agreed repertoire and named variants.
- [x] Latin/Cyrillic text, metrics, marks and kerning pass script-aware proof review.
- [x] Deterministic project JSON round-trips; static OTF/TTF/WOFF2 compile and pass table/shape checks.
- [x] Browser interactions, errors and export work from a clean checkout with pinned dependencies and notices.
- [x] The browser outline, chart and specimen represent the current source in the correct coordinate system; combining marks use both source anchor coordinates.
- [x] `h`/`n` are distinct, `U` has connected stems, and `A` has intentional, valid component winding/joins in the compiled proof.
- [x] The documented selected-project export invocation compiles that project and fails for an absent or invalid project.

## Negative / security cases
- Reject malformed source, invalid axes/switches, incompatible contours and resource-exhausting export requests.
- No third-party font outline import or GPL source reuse.

## Verification
- Follow `.progressive/system/QUALITY_PROTOCOL.md`; focused schema/geometry/build/browser tests plus Latin/Cyrillic specimen review.
- For audit findings 1–3, use rendered browser assertions plus compiled-font proof, recipe topology/contour assertions and a non-default project-export integration test. Passing source-preview parity alone is insufficient.

## Completion Record
Status: COMPLETED 2026-09-24.

Final report: `.progressive/completions/01-technical-sans-mvp.md`.

Outcome: original 164-glyph Latin/Cyrillic static Technical Sans workbench with source-faithful
browser proof and selected-project TTF/OTF/WOFF2 export.

Validation: current and isolated-checkout `npm test`/`npm run export`, Text and Display WOFF2
proofs at 10/14/24/72 px, Python/JavaScript syntax checks, and diff check passed.

Decision / technical debt: bounded static direction closes Phase 1; variable masters and deferred
workflow work are post-phase decisions. The proof review is evidence-based agent review, not
external professional type-design certification.

Handoff: no next implementation phase is scheduled; use the deferred Roadmap request to choose
future work.

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

## Phase 1b Scoped Native Optical Review — 2026-09-24

Compiled TTF/OTF/WOFF2 and browser proofs were inspected at 10, 14, 24 and 72 px with
`АВНОРСХ`, `ДЛЖКУФЯ`, `бдлтф`, `ёж`, `AА`, `eе`, and Latin/Cyrillic kerning pairs.
The review found that `А` had an E-like construction, `К/Ж` collapsed to X-like forms,
`В/Я` and `б/д/л/т/ф` used unsuitable generic constructions, and cap `Л` was
erroneously narrow. Cyrillic `е` was visibly inconsistent with Latin `e`; both now use
the same round skeleton, with `ё` adding its diaeresis. A local variable shadowing
`roundness` in the Cyrillic lowercase recipes also produced malformed compiled curves;
it is fixed.

The browser proof now shows source advances rather than normalizing every glyph to a
fixed width, applies the same representative pair values as the source, offers 10/14/24/72
px proof sizes, and has no unsupported default specimen character. The compiler now checks
all cmap names and advances against source and verifies `A/O=-72`, `Д/О=-66`, `T/o=-42`,
and `Т/о=-48` from compiled GPOS. A browser export proof loads the generated WOFF2 and
checks all four sizes and active kerning.

Observed: six Python tests, recipe-preview browser test, Python syntax check, diff check,
and full static export all passed. This is not Phase 1 closure: the full chart still has
unreviewed generic fallback recipes outside this targeted proof, so its full-repertoire
type-quality acceptance criterion remains open. No Modulator-parity work was started.

## Phase 1b Review-Fix Verification — 2026-09-24

Independent review found and the follow-up fixed three preview/export-proof defects: exact
`T/o` and `Т/о` kerning exceptions now precede their class rules; `B/В/Я` use their
source-fixed `.8` roundness in browser outlines; and compiled-browser proof resolves the
manifest from the exact current project source hash rather than scanning `build/`. Browser
regression checks both exception margins and verifies that the three fixed-roundness outlines
do not change when the UI `roundness` control changes. `npm run test`, `npm run export`,
Python syntax validation and `git diff --check` passed after the fixes.

## Change-adoption note — 2026-09-24

The public Modulator interface was reassessed as an interaction reference
(`https://www.metaflop.com/modulator`). Its parameter breadth, anatomy/help surface, undo/reset,
sharing and family selection are not implemented in this phase. The original, bounded static
workbench direction is retained; any broader parity work is deferred in `ROADMAP.md` until Phase 1
type quality is closed.

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

## Phase 1b Full-Repertoire Recipe Review — 2026-09-24

Reviewed all 95 ASCII Basic Latin positions, NBSP, and Russian Cyrillic
`А–Я/а–я` including `Ё/ё` from the original local recipes. The old generic
rectangle/bar fallback is now unreachable: punctuation, digits, every Latin and
Cyrillic letter, and marks have explicit recipe branches; an unreviewed branch
raises rather than silently producing a fallback form. The pass also corrected
the narrow `J/j/r` advances, positioned mark anchors at the mark centre, added
`Й/й` construction, and added explicit Latin/Cyrillic diagonal-pair exceptions
alongside the existing class pairs.

Browser geometry is now checked against all 164 Python-evaluated glyphs (outline
coordinates and advances, rounded only for floating-point transport). The
compiled TTF/OTF/WOFF2 check validates `A/O`, `A/V`, `V/A`, `T/O`, `T/a`,
`T/o`, `А/О`, `Т/А`, `Т/а`, and `Т/о`; the WOFF2 browser proof measures the
same GPOS values at 72 px. Observed: eight Python tests, full-repertoire browser
proof at 10/14/24/72 px, complete static export, Python syntax validation, and
`git diff --check` passed.

This is not Phase 1 closure. The generated proof is structurally complete and
source-parity-safe, but its literal modular forms and joins still require a
qualified optical/type-design judgment before the criterion that Latin/Cyrillic
text and marks *pass* a script-aware proof review can be marked complete.

## Phase 1b Independent Implementation Review — 2026-09-24

An independent GPT-6 Sol high-reasoning review found and the follow-up corrected
Latin `V/Y/W` forms that had collapsed into `X`/`Ш`, Cyrillic `З/з` that copied
Latin `S/s`, disconnected reverse-open `Э/э`, width-drifting mark anchors, and
inconsistent precomposed/decomposed diaeresis heights. The browser now keeps
range/number control pairs synchronized and attaches combining marks to the
previous base anchor instead of allocating them as ordinary spacing glyphs.

New regressions prove distinct forms, reverse-round joins at aperture limits,
mark-anchor scaling at width limits, precomposed/decomposed diaeresis alignment,
paired-control synchronization, mark placement, and display-preset source→preview
parity. The compiler now requires GPOS MarkToBase lookup type 4 in every static
output. Observed: `npm run test` (10 Python plus browser tests), `npm run export`,
`py_compile`, `node --check web/app.js`, and `git diff --check` passed.

## Phase 1b Optical Recipe Pass — 2026-09-24

An independent GPT-6 Sol high-reasoning implementation pass turned the remaining
mechanically testable optical findings into original recipe corrections. Round and
open Latin/Cyrillic forms now overshoot flat alignments (`O/О/Q/0`, `o/о/e/е/ё`
and related open forms); open-form terminals overlap their stems at safe weight and
x-height limits, and their excessive right sidebearings were reduced before adding
any new kerning. `F/I/M/Z/Г` now have distinct constructions rather than inherited
near-neighbour skeletons. Bowl–stem joins in `P/R/Р/Ь/Я` and `b/d/p/q/р/ь` overlap
at the weight extremes while preserving counters.

New recipe regressions cover optical bounds, structural distinction, open-form
spacing and terminal overlap, and bowl–stem joins/counters at the axis limits.
The compiler verifies that exported TTF/OTF/WOFF2 preserve the required overshoot
bounds for representative round/open forms; browser source→preview parity continues
to cover all 164 glyphs. Observed: `npm run test` (14 Python tests plus Chrome
proof), `npm run export` (compiled TTF/OTF/WOFF2 bounds/cmap/advance/GPOS and
WOFF2 proof at 10/14/24/72 px), `py_compile`, `node --check web/app.js`, and
`git diff --check` passed.

This remains a bounded technical optical pass, not qualified type-design sign-off.
Phase 1 stays open for a human/qualified script-aware review of the compiled proofs;
no new kerning pairs, axes, imported outlines, or Modulator-parity work were added.

## Phase 1b Full Compiled Proof Recheck — 2026-09-24

The current uncommitted original-recipe/parity/compiler/test changes were rechecked without
modifying or committing the worktree. `npm run test` passed all 14 Python recipe tests and the
Chrome chart/workbench proof. `npm run export` rebuilt the Text TTF/OTF/WOFF2, verified
tables/optical bounds/cmap/advances/GPOS, and loaded its WOFF2 in Chrome at 10/14/24/72 px.
`py_compile`, `node --check web/app.js`, and `git diff --check` also passed.

An isolated copy of the current source (excluding `.git`, `.venv`, `node_modules`, and `build`)
passed the documented README path: `npm run setup`, `npm test`, and `npm run export`. The
browser test exercised the workbench chart, Text/Display presets, paired controls, A/B,
combining-mark placement, mobile layout, and versioned JSON download.

For the required full compiled proof, both the Text project
`fca7a8a9414ffd4a7fd79f972c03d877b82cb5ce444da939d4ca3aaf6853f891` and the actual Display
preset values (`weight=124`, `width=1.08`, `xHeight=520`, `roundness=.9`, `aperture=.72`,
single-storey `a`, slashed `0`) were compiled to isolated TTF/OTF/WOFF2 instances. In Chrome,
each WOFF2 returned HTTP 200 and rendered all 95 Basic Latin positions, NBSP, every Russian
uppercase/lowercase mapping, targeted round/open/join families, `AV/VA/TO/Ta/To`,
`АО/ТА/Та/То`, and precomposed/decomposed acute/diaeresis at 10, 14, 24, and 72 px. The proof
text was unchanged at every size and had non-zero layouts (1408 px width; 75/105/180/630 px
height). At 72 px, measured GPOS reductions were respectively `AO=5.184`, `AV=4.32`,
`VA=4.32`, `TO=4.176`, `Ta=3.024`, `To=3.024`, `АО=4.752`, `ТА=3.888`, `Та=3.456`, and
`То=3.456` px in both instances. Local visual proof captures are in ignored `build/`.

Phase 1 remains IN PROGRESS. These are reproducibility, parity, compiler, rendering and
mechanical optical observations; they do not constitute the required independent qualified
script-aware optical/type-design sign-off. No subjective redesign was made without that review.

## Audit Adoption — 2026-09-24

Source: `research/font-lab/audits/2026-09-24-product-technical-audit.md`.

- `ACCEPTED`: findings 1–3 — browser-proof fidelity; named `h`/`n`, `U` and `A` recipe defects; selected-project export routing. These are Phase 1 work.
- `ALREADY COVERED`: qualified script-aware proof review and static binary validation remain Phase 1 gates.
- `DEFERRED`: project reopen/save, visual A/B, undo/reset, user-accessible export, broader Modulator parity, shared recipe representation, axis-aware spacing/kerning and Russian usage punctuation. The deferred roadmap change request owns them after Phase 1.

No implementation or consequential architecture decision occurred in this adoption.

## Browser Preview Fidelity Repair — 2026-09-24

Corrected only the audit's browser-proof fidelity finding. The outline, generated glyph
chart, and specimen now share an explicit font-space-to-SVG transform that maps positive-up
font coordinates into SVG's positive-down screen space. The chart renders the current
evaluated contour in an SVG for each of the 164 mapped glyphs, while retaining its character
label for selection. The specimen carries evaluated source anchors and places combining marks
by both anchor coordinates: horizontal layout aligns `top.x` to `_top.x`; a vertical SVG
translation aligns `top.y` to `_top.y`.

Observed validation: the Chromium regression checks 164 chart SVG outlines, source/current
chart parity, upright cap-height versus baseline, source-anchor parity for Text and Display,
and actual screen-space X/Y coincidence for acute and diaeresis attachments. `npm test` passed
14 Python tests plus the browser suite; `npm run export` completed TTF/OTF/WOFF2 compilation
and compiled WOFF2 proof; `node --check`, `py_compile`, and `git diff --check` passed.

Phase 1 remains in progress. This record does not repair the separate `h`/`n`, `U`, `A`, or
selected-project export-routing findings, and it is not typographic quality sign-off.

## Audit Recipe and Export Corrections — 2026-09-24

Completed the remaining accepted objective audit findings. Latin `h` now has an ascender and a
distinct advance from `n`; `n` remains x-height based. The upper and lower `U` stems overlap,
so compilation removes them into one connected outline. `A` and Cyrillic `А` now give the
crossbar the same solid winding as their diagonal strokes; compilation retains one intentional
counter with opposite winding rather than an accidental cutout at a join.

`npm run export` now uses a local launcher that forwards `--project` and `--output-dir` to both
the Python compiler and the compiled-WOFF2 proof. The new integration regression exports a
valid non-default project into its own source-hash directory, proves that WOFF2 in Chromium,
and confirms a missing selected project fails instead of compiling the default source.

Observed validation: `npm test` passed 15 Python tests, Chromium browser proof, and custom
export-routing integration; `npm run export` passed TTF/OTF/WOFF2 compilation and WOFF2 proof.
Compiler validation now requires compiled `h`/`n` distinction, one connected `U` outline, and
an outer `A` outline plus one oppositely wound intentional counter. `py_compile`, JavaScript
syntax checks, and `git diff --check` passed.

Phase 1 remains in progress pending the independent qualified script-aware optical/type-design
review. These mechanical corrections are not typographic quality sign-off.
