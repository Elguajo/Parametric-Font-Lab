# Product and technical audit — 2026-09-24

## Verdict and scope

Retain the bounded original Technical Sans engine and static compiler direction. The repository is a working engineering prototype, not yet a usable Metaflop replacement or production-quality text font. Correctness blockers remain before qualified optical sign-off; that sign-off is not the only missing work.

Inspected current working tree including pre-existing uncommitted changes, compiled project context, web UI, recipe evaluator, compiler, tests, README, and primary reference websites. Ran local tests, export, browser observations and targeted reproductions. No implementation changes, deployment, external upload, or delegated review. This is not independent professional type-design certification.

Comparison criteria: visible preview fidelity; complete edit/save/reopen/export workflow; meaningful parameter scope; script/type quality; maintainability and validation.

## Reference comparison

| Reference | Relevant mechanism | Local implication |
| --- | --- | --- |
| [Metaflop Modulator](https://www.metaflop.com/modulator) | Parameter families, glyph/chart/typewriter, font selection, undo/reset, font downloads | The local five-axis single-family scope is intentional, but correct glyph previews and usable output are baseline workflow needs. Public interface inspected; remote downloads were not exercised. |
| [Recursive](https://www.recursive.design/) | Five coordinated variable axes, named instances, compatible construction alternatives | Power depends on coherent, reviewed design space, not slider count. Recursive is a finished font family, not a general parametric editor; do not infer its variable compatibility for local recipes. |
| [Glyphr Studio](https://www.glyphrstudio.com/) | Browser font-design product | Useful adjacent editor reference, not evidence that a full outline editor belongs in this MVP. No detailed runtime comparison performed. |

## 1. P1 — Preview does not faithfully show the generated font

Evidence: `web/app.js:26,29,35`, `web/styles.css:24` and local `build/audit-workbench.png`.

- Font-space positive-up coordinates are inserted directly into positive-down SVG coordinates without a Y transform. The selected A and specimen are vertically inverted in the running UI.
- Chart buttons use `textContent` instead of evaluated outlines. Browser measured 164 buttons, zero SVGs, and computed Arial font. This is a character picker, not a generated-font chart.
- Mark positioning adjusts horizontal margins only. Lowercase decomposed diaeresis receives no source-anchor vertical translation; observed `ё` and `е + U+0308` have different vertical mark positions.

Recommendation: one explicit font-to-SVG coordinate transform shared by outline, chart and specimen; source-based X/Y mark placement; rendered orientation and mark regressions. Keep SVG for immediate outline interaction and use compiled font text as the final proof. This is a bounded repair with moderate rendering risk. Replacing the entire renderer now would cost more and is not required.

## 2. P1 — Actual recipe defects remain behind green checks

Evidence: `fontlab/recipes.py:68,78,179,211`, `build/compiled-phase-1b-proof.png`.

- Evaluated h and n have identical contours and identical advance 540.
- U has stem spans 300–700 and 0–170, leaving a 130-unit gap on both sides at default settings.
- A has oppositely wound overlapping filled components: signed areas approximately -65712, -65712, +30272. White cutouts at bar/diagonal joins are visible in the compiled WOFF2 proof. Solid component union and counter winding need an explicit convention.
- Many constructions remain literal modular forms. Their suitability for UI/body text is unproven; a deliberately modular display face is a possible product direction but should not silently replace the stated text-quality goal.

Recommendation: first repair objective identity/connectivity/winding defects across related glyph families, then get a qualified Latin/Russian type designer to review compiled Text and Display proofs. Review both small text and large details across parameter extremes. Retain the current engine; expanding repertoire or adding style engines now multiplies repair cost. Effort is substantial for quality closure; targeted objective fixes are smaller and lower risk than a wholesale rewrite.

## 3. P1 — Custom-export command silently ignores the selected project

Evidence: `package.json:10`, `README.md:463`, `tests/compiled-font-proof.test.mjs:13`.

Reproduction: `npm run export -- --project /tmp/pfl-audit-deliberately-missing.json` returned success and compiled default source hash `fca7a8a9414ffd4a7fd79f972c03d877b82cb5ce444da939d4ca3aaf6853f891`. npm appends arguments to the final Node proof command, not the Python compiler; the proof ignores the arguments and also resolves only the default project.

Recommendation: one export entry point forwarding project and output directory to both compiler and proof. Verify a changed project produces its own manifest and actual chosen outlines, and a missing project fails. Small change, high benefit, low architectural risk. Direct Python invocation is a temporary workaround but does not solve the browser workflow.

## 4. P2 — Product claims exceed the usable workflow

Evidence: `web/app.js:37`, `web/index.html:29`, README, current project architecture and handoff.

- A/B captures JSON and reports equal/different; there is no visual A/B or restore/switch operation.
- Project JSON can be downloaded but not reopened in the editor. No reload persistence, undo/reset, or browser font export exists.
- Current browser tests verify A/B status wording and download filename, not a user recovering work or comparing designs.
- README contains an older research-only status and ambitious planned checklist alongside implemented instructions. The prior handoff described external optical sign-off as the sole blocker.

Recommendation: distinguish implemented, prototype-only, and planned behavior. After correctness repairs, deliver save/reopen, undo/reset, visual A/B, and a user-accessible export path. These are workflow foundations for a nondeveloper, even with one family and five axes. Sharing, accounts, multiple engines and a full anatomy tutorial can remain deferred. Workflow work is moderate effort; hosted compilation needs a separate operational/security design before exposure.

## Architecture and validation risks

- Glyph grammar is hand duplicated in Python and densely compressed JavaScript. Existing parity tests are valuable but prove agreement, not correctness. Prefer a shared declarative recipe representation or generated evaluator after bounded fixes; do not start a framework rewrite solely to change code style.
- Width currently scales all X coordinates, including stroke thickness. Treat independence of width/weight as a design question and review compensation before expanding ranges.
- Kerning constants do not adapt to axes. This is a credible type-quality risk, not proof that every current pair is wrong.
- Self-intersection validation records line segments but skips cubic intersections. Do not describe it as exhaustive outline validation.
- Russian letter coverage is not complete practical Russian typography: em dash, Russian quotes and numero sign are outside the current mapped set. Add a usage-driven punctuation set after basic correctness.

## Observed validation

- `npm test`: passed 14 Python tests and existing Chromium workbench tests.
- `npm run export`: passed TTF/OTF/WOFF2 compilation, current table/metric/GPOS checks and Chromium compiled WOFF2 proof.
- Additional 32 endpoint combinations of weight/xHeight/roundness/aperture/O counter passed current evaluator validation. This is not exhaustive optical or curve-intersection validation.
- Runtime screenshot confirms inverted previews; DOM confirms chart uses system text.
- Targeted Python reproduction confirms h/n identity, U gaps and opposite winding in A.
- Deliberately missing custom-project export incorrectly succeeds, confirming the command-routing defect.

Existing tests do not justify a production quality claim. In particular, the compiled proof verifies unchanged text and selected kerning values; a screenshot is saved but not automatically judged for shape correctness.

## Recommended sequence

1. Repair preview coordinate/mark/chart fidelity, glyph identity/connectivity/winding and custom export routing with outcome-based regressions. Keep Phase 1 open.
2. Review compiled Text/Display type quality with a qualified script-aware reviewer; correct verified spacing/forms across safe ranges.
3. Complete nondeveloper workflow: save/reopen, undo/reset, visual comparison, usable export and clear parameter guidance. Reconcile README and acceptance wording with actual behavior.
4. Only after that consider additional meaningful controls, compatible variable masters and further style engines. Do not confuse a parameterized generator with a variable-font binary.

No decision to broaden scope or replace architecture was made by this audit.
