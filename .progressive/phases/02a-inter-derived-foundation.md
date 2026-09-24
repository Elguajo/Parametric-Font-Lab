# Phase 02a — Inter-derived readable foundation

## Goal
Replace the visually rejected v2 default with a readable Inter-derived source while keeping
saved v1/v2 project meaning and exports intact.

## Acceptance
- Real Latin/Russian glyphs and text in browser chart/specimens, with explicit load failure.
- Native `wght`/`opsz` controls only; JSON v3 isolates the new semantics.
- Static TTF/WOFF2 export from pinned OFL source with license and renamed family.
- Selected-project and engine/source identity reject stale or modified proof artifacts.
- Text/Display and axis endpoints inspected at 10/14/24/72 px, including Д/Л and b/ь.
- Legacy v1/v2 export and v2 browser remain usable.

## Completion Record

Completed 2026-09-24. Full report: `.progressive/completions/02a-inter-derived-foundation.md`.
PFL Sans v3 is the default, using renamed Inter 4.1 outlines and native weight/optical-size
axes. v1/v2 retain their saved semantics and export paths. Browser and compiled WOFF2 proofs
loaded at 10/14/24/72 px for Text/Display and both native axis endpoints; Д/Л and b/ь are
visually distinct. `npm test`, default and v1/v2 exports passed. At 10 px, weight 900 is dense
and weight 100 is faint; neither is the Text preset. See ADR-012 and the full report for evidence
and limits.
