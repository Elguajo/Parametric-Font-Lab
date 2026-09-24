# Phase 02a Completion — Inter-derived readable foundation

Status: COMPLETED
Date: 2026-09-24

## Outcome
The default face is now PFL Sans, a renamed Inter 4.1 derivative with readable Latin and
Russian forms and spacing. The original geometric recipe engine remains available for v1/v2.

## Delivered
- v3 project/schema with native weight and optical-size controls, browser WOFF2 chart and text proof.
- Static TTF/WOFF2 compiler with pinned source, renamed family, license copy and selected-project manifest.
- Preserved v1/v2 JSON files, schemas, export path and legacy browser workbench.

## Implementation notes
The official Inter 4.1 TTF is pinned by SHA-256; source and license are in `vendor/inter/`.
The live preview is a renamed WOFF2 from that source. The static compiler instantiates both
native axes and preserves OpenType shaping tables. The identity hash covers both source and
preview font bytes. A failed FontFace load hides browser specimens; the compiled proof has the
same gate.

## Decisions made
- ADR-012 supersedes ADR-011 for the default product source. No automatic v1/v2 → v3 migration.

## Deviations / technical debt
- Weight 900 at 10 px is dense and weight 100 at 10 px is faint; Text preset stays at 400/14.
  No production variable binary.
- No claim of original PFL glyph authorship in v3; downstream custom forms need separate design work.

## Problems discovered
The v2 control corpus passed structural tests but was rejected visually by the product owner.
The correction changes the underlying type source instead of adding more geometric exceptions.

## Verification evidence
- `npm test` → 22 Python tests, new v3 Chromium workbench regression, legacy v2 browser regression,
  and custom-project export routing passed.
- `npm run export` → v3 static TTF/WOFF2 compiled; selected WOFF2 loaded with GPOS behavior and
  visible Latin/Russian control strings at 10/14/24/72 px; missing WOFF2 hid the proof.
- `node tests/inter-endpoints.test.mjs` → six Text/Display/native-axis endpoint cases compiled,
  loaded and screenshotted at 10/14/24/72 px. `build/inter-endpoints/report.json` records paths.
- `npm run export -- --project fontlab/project-v1.json` and the same v2 command → both legacy
  TTF/OTF/WOFF2 exports and browser compiled proofs passed.
- Visual review of Text, Display and weight-900 compiled screenshots → Д/Л and b/ь are distinct;
  weight 900 at 10 px is visibly dense. Weight-100 proof is visibly faint at 10 px.
- `python3 -m py_compile`, `node --check`, `git diff --check` → passed. PCK runtime audit →
  PASS with 0 errors and 12 pre-existing skill-collision warnings.

## Architectural impact
Later work may rely on a readable OFL source and honest v3 preview/export. Existing projects
are not reinterpreted. Architecture and ADR-012 own the source/compatibility contract.

## Follow-up
Scope product-specific differentiation on the Inter base separately; do not assume the
original 164-glyph custom-design plan still applies.
