# Parametric Font Lab — Phase 0 research report

Date: 2026-09-23. Authoritative brief: [RESEARCH_SPEC](../../../.progressive/phases/00-research/RESEARCH_SPEC.md). [Machine summary](research-summary.json) and [source manifest](../sources/repositories.json). **Phase 0 is research only; no production Font Lab was built.**

## 1. Executive summary

The project currently has a PCK workflow scaffold and two supplied Metaflop references, but no product runtime. The best feasible direction is an **original Geometric/Technical Sans grammar** with Latin and Russian Cyrillic authored together; a versioned JSON source project; deterministic glyph recipes; generated UFO/Designspace; Python fontmake/fontTools compilation; responsive browser preview. Three disposable spikes prove the basic geometry-state separation, browser outline rendering and two-master static/variable/WOFF2 toolchain. They do not prove typographic quality or full-script compatibility.

## 2. Metaflop findings

The 2026-09-23 SingleFile and 2976×1656 screenshot show Bespoke in a fixed centered tool: Modulator/Parameters left, Glyph+Chart right, Typewriter below. Source SCSS confirms 1000 px content, 259/710 px columns, 31 px gutter and a fixed top nav. Saved DOM exposes **16** controls; official Bespoke page says 14, a copy/source discrepancy. [`reverse-spec`](../metaflop/reverse-spec/layout.md), [parameter table](../metaflop/reverse-spec/parameters.md), [engine analysis](../metaflop/parameters/engine-analysis.md).

Preserve grouped numeric/sliders, immediate glyph/chart/typewriter feedback, reset/undo and shareable state. Redesign fixed width, small targets, hidden precision mode and weak focus affordance; add script/local/switch/quality states. The local SingleFile browser URL was blocked by browser security policy; static DOM/CSS source and PNG provided the evidence. Exact drag/debounce/keyboard behavior remains unconfirmed, rather than guessed.

## 3. Engine and reuse decision

The official Ruby/Sinatra app rewrites `font.mf` and runs a server METAFONT → mf2outline/FontForge pipeline; preview is a generated base64 OTF. Bespoke has global numeric controls, hand-authored glyph files, optical rules, Latin T1 repertoire, class kerning/ligatures; inspected source has no Cyrillic, UFO/Designspace, compatible masters, local axes or structural-switch UI. A single recipe skeleton cannot cover all style families or arbitrary font morphing. [`limitations`](../metaflop/parameters/limitations.md).

[Comparison matrix](../engines/comparison-matrix.md) assigns roles: Fontra and Recursive as architecture references; opentype.js for outline inspection; native CSS text (HarfBuzz later if exact shaping is required) for specimen; fontTools/fontmake for build. Folent's arbitrary contour matching is visual experimentation, not safe font compilation. Fontc is a plausible future compiler alternative, with no V1 reason to add Rust infrastructure.

[Recursive's five-axis design](../engines/recursive-reference.md) used a historically reported 24 source fonts; its authored Mono/Sans transition is evidence for deferring PFL mono until compatible, quality-reviewed masters exist.

## 4. Licenses

[Primary-file matrix](../licenses/license-matrix.md) and [reuse policy](../licenses/reuse-policy.md) separate web code, Bespoke source and generated output. Metaflop web and Bespoke source are GPLv3-labeled; site assets have no blanket grant established. Webfont packages include GPLv3 and OFL texts; that does not license PFL code. FontTools/opentype.js are MIT, fontmake/fontc/Coldtype Apache 2, HarfBuzz Old MIT-style, Recursive font OFL 1.1. UFO spec prose has no root license file verified. Use original outlines; do not copy GPL recipes/CSS or import commercial fonts.

## 5. Proposed architecture

`StyleEngine → GlyphRecipe/grammar → global axes + local overrides + switch branch → script module → optical/metrics/kerning → compatible UFO masters + Designspace → fontmake/fontTools → validated binaries`. The [data model](../architecture/data-model.md) keeps versioned JSON canonical. [Glyph grammar](../architecture/glyph-grammar.md), [axes](../architecture/axes-model.md), [switches](../architecture/structural-switches.md), [scripts](../architecture/script-system.md), [spacing](../architecture/spacing-kerning.md), [pipeline](../architecture/build-pipeline.md), [PCK placement](../architecture/pck-integration.md) and [UI IA](../architecture/ui-information-architecture.md) detail interfaces and gates. Structural branches do not interpolate with one another.

## 6. Spike evidence

- [Browser](../spikes/browser-outline/README.md): Chromium + opentype.js parsed 4-glyph original TTF in 6 ms; SVG path/text/width visual update worked in one run; no page errors. Timing is not a full-font benchmark.
- [Build](../spikes/variable-build/README.md): two original compatible UFO masters + Designspace built static OTF/TTF, variable TTF and WOFF2; reopen verified tables and cmap. Brotli was a required extra.
- [Local/switch](../spikes/local-axis/README.md): global H weight, local O counter and discrete `a` branch produced distinct cases; topology differed across switch branch, as expected.

## 7. MVP and PCK

[V1 scope](mvp-scope.md) reduces ten candidate controls to five global controls and two first switches; Latin and Russian Cyrillic, static export, chart/specimen, presets/A-B remain release targets. Variable weight moves to Phase 2 after all glyph masters and metrics pass. [Roadmap](roadmap.md). PCK audit found no reusable runtime/UI; use its router, skills, phase state, templates and audit tools rather than create parallel governance. Current `PROJECT_BRIEF` and `ARCHITECTURE` remain uninitialized until Phase 1 product initialization.

## 8. Risks and open questions

Highest risks: typographic quality at axis extremes, Cyrillic design quality, compatible variable contours, spacing/kerning, GPL/asset boundaries and later untrusted-font parsing. [Risk register](risk-register.md). Open decisions for Phase 1 implementation: exact safe axis curves after type proofs; responsive app framework only after vertical-slice needs; hosted job/storage transport only when a deployment target exists; per-language Cyrillic variants after native review. These do not block starting the narrow vertical slice.

## 9. Exact next implementation task

**Phase 1a: build a minimal original cross-script vertical slice.** Create a versioned JSON Schema and deterministic recipe evaluator for H/O/a/0 plus Н/О/а/о, with global weight, O counter-local override and one `a` construction switch. Create a responsive browser page showing glyph outline, chart and editable Latin/Cyrillic specimen with numeric/slider controls. Generate static UFO → Designspace → TTF/OTF/WOFF2 through an isolated Python command. Add tests for serialization, glyph contour validity, browser/server parity, static table/cmap output and text preview; include dependency notices and PCK phase tracking. Do not import Metaflop/Recursive outlines or implement full font, hosted storage or multi-engine framework in this task. Acceptance: all named glyphs render and export from original recipes, the local override affects only O, switch variants remain discrete, Cyrillic specimen maps to Cyrillic glyph IDs, and build tests pass from a clean checkout.
