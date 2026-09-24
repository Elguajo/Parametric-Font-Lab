# Phase 02 — Type-quality foundation

## Goal
Produce a trustworthy generated/compiled proof and an original, readable Text design on a
representative Latin and Russian Cyrillic corpus before extending type-quality work to 164 glyphs.

## Context
Phase 1 completed the technical static workbench. New findings Q1–Q6 are disposed in
`research/font-lab/audits/2026-09-24-type-quality-change-review.md`; source-design rationale is
`research/font-lab/decisions/ADR-011-type-quality-source-strategy.md`. Read the Phase 1 compact
Completion Record for the prior export and browser guarantees.

## In scope
- Make the chart visibly display current generated glyphs and identify the compiled-font text
  proof separately from the immediate source-SVG preview.
- Bind compiled proof identity to both selected project data and the generating engine revision;
  reject or rebuild a stale output rather than reporting it as current.
- Redesign a control corpus of structural families: `H O A V C S n o b d e` and
  `Н О С Д Л Ж К Я и н о п б д л е ь`. Use original glyph-specific contours and optical rules.
- Establish per-glyph sidebearings and control-corpus spacing before kerning; test representative
  Russian and Latin words at Text/Display presets and the current safe control endpoints.
- Record current parameter effects and a versioned project-compatibility plan before any change
  to saved JSON semantics.

## Out of scope
- Full 164-glyph optical closure, production variable fonts, all-axis master production, an
  outline editor, new font dependencies and broader workbench workflow parity.

## Tasks
- [x] Correct chart visibility and distinguish fast SVG proof from compiled text; add behavior
  checks that observe visible generated shapes and the selected compiled font.
- [x] Prevent stale compiled proof reuse after source-engine changes, with an outcome-based
  regression covering changed recipes and unchanged project JSON.
- [x] Design and evaluate the control corpus, including distinct `Д/Л` and `b/ь`, ascenders,
  open forms, optical joins and surviving counters at control extremes.
- [x] Tune the control corpus's sidebearings, then kerning; inspect mixed Latin/Russian text and
  document remaining defects for Phase 03.
- [x] Decide how any necessary new source semantics preserve or migrate existing project JSON
  before implementing a breaking change.

## Acceptance criteria
- [x] The chart visibly renders current evaluated contours; a compiled-font specimen loads the
  binary generated from the exact selected project and current engine revision.
- [x] A stale binary cannot pass the compiled proof when recipe code changes without JSON change.
- [x] Control glyphs are distinguishable and structurally valid across Text/Display and tested
  control endpoints; `Д` differs from `Л`, `b` from `ь`, and lowercase ascenders have intended
  height. Open bowls and joins remain readable in the compiled proof.
- [x] Documented Latin and Russian control strings have reviewed sidebearings and spacing at
  10/14/24/72 px; remaining quality problems are recorded rather than marked complete.
- [x] Existing v1 project JSON keeps its documented meaning or has an explicitly approved,
  versioned migration before new semantics are shipped.

## Negative / security cases
- A missing or stale compiled artifact must fail explicitly; no silent fallback to system font
  may be counted as a successful generated-font proof.
- Do not import reference font outlines or GPL editor/source routines.

## Verification
- Follow `.progressive/system/QUALITY_PROTOCOL.md` with focused recipe/identity/spacing tests,
  browser computed-style or rendered-shape assertions, stale-artifact reproduction, and actual
  compiled TTF/OTF/WOFF2 proof. Capture control strings and glyph details at 10/14/24/72 px for
  Text/Display and axis endpoints; record a script-aware optical review and open defects.
- Run the relevant existing `npm test`, `npm run export`, syntax and diff checks after changes.

## Completion Record

Completed 2026-09-24. Phase 1's historical completion was left unchanged.

### Source and compatibility

The default project is now `schemaVersion: 2`, engine `2.0`, with separate v2 metrics and
kerning profile names. The same five axes and ranges remain; the control corpus has new geometry,
per-glyph bearings, and retuned diagonal/round kerning. Existing v1 JSON still routes to the
preserved `fontlab/recipes_v1.py` evaluator and v1 profile values; a reference v1 file and schema
remain in `fontlab/`. There is no automatic conversion. Both v1 and v2 exports were compiled and
loaded in the browser. New geometry did not silently reinterpret old saved projects.

### Proof identity and negative cases

The browser chart displays evaluated SVG paths; its computed display and nonzero rendered size
were checked. The workbench labels live SVG separately from the exported compiled proof.
`npm run export` writes `proof.html` with a WOFF2 FontFace load gate. The selected project's
canonical JSON hash and a content hash of recipe/compiler/lock files determine a build ID. The
manifest records both, plus SHA-256 hashes of all font binaries and the proof page.
`verify_compiled_proof.py` rejects missing, changed, or stale files. A focused regression kept
project JSON fixed, changed recipe bytes, and observed rejection of the old instance. A browser
check blocked WOFF2 loading and observed an explicit error with the proof rows hidden.

### Control-corpus review

Original control contours were added for open C/С and e/е, smooth S, Latin n shoulder,
ascender-height b/d, wider lower counters, distinct Д/Л constructions, and Cyrillic б/ь.
The text corpus is `bone done | нос сон дно поле дело`; the proof also shows `AV VA AO АО ДО ДЛ b ь`
and the exact control glyph list. In the final compiled screenshots the two Д/Л structures and
b/ь ascender distinction are visible at Text/Display and the tested endpoints. The updated n
shoulder and S turn no longer show the join defects found during review. Source endpoint tests
check positive bearings, distinct contours, ascender heights, and inner counter dimensions.
The compiler verifies these glyph distinctions and heights in each TTF/OTF/WOFF2 instance.

Bearings on the evaluated Text control corpus range from 34 to 72 units on each side; Display
ranges from 36 to 78 units. After v2 kerning, example horizontal outline gaps in Text are
`AO 50`, `AV 25`, `АО 53`, `ДО 50`, `ДЛ 82`, `bo 109`, `on 117`, `по 117` units. These become
0.25–1.17 px at 10 px and 1.8–8.4 px at 72 px. The corresponding Display pair gaps remain
positive. The 10/14/24/72 px WOFF2 screenshots were reviewed for Text, Display, and each
individual min/max axis endpoint; the strings remain separated and the named control glyphs
remain distinguishable. `build/phase-02-endpoints/report.json` and sibling PNGs are reproducible
local evidence from `node tests/control-endpoints.test.mjs`.

### Verification and remaining limits

Observed passing: `npm test` (18 Python tests, browser SVG/source parity, selected-project export),
`npm run export` for v2 and the preserved v1 project, and the 12-case endpoint compilation and
browser WOFF2 load check. Python/JavaScript syntax and `git diff --check` passed. The generated
Designspace is still single-source and static. At weight 160, 10 px text is dense even though
control counters remain open; production text tuning across axis combinations remains open.
Other letters outside the named control set, including the remaining mapped punctuation and
Cyrillic forms, have not received optical closure. Width still scales vertical stroke thickness,
and roundness/aperture affect selected recipes rather than the full repertoire. Those issues are
Phase 03 work, not Phase 02 completion claims. No external type-design certification was obtained.

## Subsequent product review

On 2026-09-24 the product owner rejected the visual result as too hand-drawn and asked for an
Inter-based foundation. The technical checks above remain historical observations about v2;
they no longer establish acceptance of v2 as the default readable typeface. The corrective v3
work and its evidence are in `02a-inter-derived-foundation.md` and ADR-012.
