# Type-quality change review — 2026-09-24

## Provenance and boundary

Source: the user's 2026-09-24 screenshots and follow-up request to recheck the comparison with
Metaflop, Fontra, Glyphs, FontLab, Recursive, fontTools and HarfBuzz. The screenshots were supplied
in the conversation, not committed as durable assets. The earlier repository audit is
[`2026-09-24-product-technical-audit.md`](2026-09-24-product-technical-audit.md); its repaired
Phase 1 defects remain historical evidence, not open findings here. Current code evidence below
was read from the 2026-09-24 working tree, including pre-existing uncommitted changes. This is a
product and source-design review, not an independent professional type-design certification.

Primary reference evidence: [Metaflop/Bespoke source](https://github.com/metaflop/metaflop-font-bespoke),
[Metaflop preview FAQ](https://www.metaflop.com/faq),
[Fontra](https://github.com/fontra/fontra),
[Glyphs outline compatibility](https://handbook.glyphsapp.com/interpolation/outline-compatibility/),
[Glyphs spacing](https://glyphsapp.com/learn/spacing),
[FontLab variation model](https://help.fontlab.com/fontlab/7/manual/Variable-Fonts/),
[Recursive process](https://github.com/arrowtype/recursive-minisite/blob/main/process.md),
[fontTools Designspace API](https://github.com/fonttools/fonttools/blob/main/Doc/source/designspaceLib/python.rst),
[HarfBuzz](https://github.com/harfbuzz/harfbuzz), and
[Google Fonts production checks](https://googlefonts.github.io/gf-guide/production.html).

## Corrected diagnosis

An algorithmic font source is viable: Bespoke uses hand-authored glyph-specific programs with
optical adjustments. The local defect is that broad bar/ring recipes, coarse advances and limited
spacing rules do not yet produce a coherent text face across the Latin/Cyrillic repertoire and
control ranges. An all-master rewrite is not a prerequisite for a better static font. Multiple
compatible masters become necessary only for an approved interpolated/variable-font deliverable
or a demonstrated optical need. The adopted rationale is
[`ADR-011`](../decisions/ADR-011-type-quality-source-strategy.md).

## Finding dispositions

| ID | Disposition | Evidence and canonical owner |
| --- | --- | --- |
| Q1: wrong or indistinguishable glyphs | ACCEPTED | `fontlab/recipes.py` `_bars` gives `Д` and `Л` the same construction; lowercase `b` has no ascender and the evaluated `b`/`ь` shapes coincide. Active Phase 02 owns a representative corrected corpus; later repertoire work is in Roadmap. |
| Q2: optical form and text rhythm | ACCEPTED | `_open_round` makes `C/С` from rectangles; `e/е` use a closed ring and bar; `_advance` uses broad width buckets and fixed kerning values. Phase 02 owns the control corpus, sidebearings and text proofs; subsequent Roadmap work owns all 164 glyphs. |
| Q3: preview truth | ACCEPTED | `web/styles.css` hides `.glyph-button svg` even though the chart creates SVG; the visible character label uses the UI font. Source SVG and compiled WOFF2 are different proof paths. Phase 02 owns visible generated glyphs and a clearly identified compiled-font proof. |
| Q4: stale compiled-proof identity | ACCEPTED | `source_hash(project)` hashes project JSON only; `tests/compiled-font-proof.test.mjs` selects a manifest by that hash. A changed recipe may reuse a previous proof. Phase 02 owns build/proof identity and a stale-artifact regression. |
| Q5: parameter semantics | ACCEPTED | `width` scales every X coordinate, affecting vertical stem thickness; `roundness` and `aperture` influence only selected recipes. Phase 02 records effect and quality limits on a control corpus; the next Roadmap slice governs repertoire-wide ranges and control labels. |
| Q6: authored parameter rules plus selective masters | ACCEPTED | Metaflop/Bespoke demonstrates glyph-specific procedural sources; Glyphs/FontLab require compatible masters for interpolation. `ADR-011` owns the chosen source strategy. Phase 02 retains static output while redesigning the control corpus. |
| Q7: production variable font | DEFERRED | Current Designspace has one source and static outputs; a variable deliverable needs an explicit compatible-master decision after static quality. Roadmap owns the later decision, not Phase 02. |
| Q8: Fontra-scale outline editor | REJECTED | A complete Bézier editor changes the product boundary beyond the Brief and does not resolve the current glyph-design defects. Fontra remains a source-model reference; revisit only as a separate product decision. |
| Q9: source and asset reuse | ALREADY_COVERED | The Brief and `research/font-lab/licenses/reuse-policy.md` require original outlines and prohibit transplanting reference code/assets. No copied outlines or new dependency are proposed. |
| Q10: workflow parity | ALREADY_COVERED | Project reopen, undo/reset, visual A/B, user-facing export and broader Metaflop parity already live in the Roadmap deferred change request. |
| Q11: historical Phase 1 completion claim | MERGED | `.progressive/phases/01-technical-sans-mvp.md` and its completion report record technical closure. Their evidence does not establish independent typographic sign-off. Brief, Architecture, Roadmap and the new Phase 02 distinguish completed technical work from new type-quality work without rewriting history. |

## Scope and remaining decisions

The near-term goal is an original readable Geometric/Technical Sans with a trustworthy compiled
proof, initially on representative Latin and Russian Cyrillic forms. Keep rapid source-SVG
interaction, then verify actual compiled text; compilation on every slider event is not required.
Preserve the current project JSON contract during Phase 02. Any later change to saved project
semantics must be versioned with an explicit compatibility/migration decision before release.
Do not promise variable-font binaries, five quality-validated interpolation axes, or professional
certification from the present technical tests.
