# Phase 00 Completion — Research

Status: COMPLETED
Date: 2026-09-23

## Outcome
Research baseline and a concrete Phase 1a implementation task are ready; no production Font Lab exists yet. Main report: `research/font-lab/final/RESEARCH_REPORT.md`. Definition of Done audit: `research/font-lab/final/definition-of-done.md`.

## Delivered
- Immutable Metaflop SingleFile/screenshot reference analysis; official web and Bespoke source analysis.
- 15-repository source/license manifest, engine comparison, reuse policy.
- Glyph, axis, switch, Latin/Cyrillic, metrics, UI, data and PCK integration proposals plus ten proposed ADRs.
- Disposable browser, variable font build and local-axis/structural switch spikes.
- MVP, product roadmap, risks, report and machine-readable summary.

## Implementation notes
The repository had no product runtime, package manager or CI. The proposed architecture keeps versioned JSON as semantic source and derives UFO/Designspace for fontmake/fontTools. Browser preview and Python export need parity tests. Research dependencies and public source clones stayed outside product runtime; generated binaries and `node_modules` are ignored.

## Decisions made
See `research/font-lab/decisions/ADR-001`–`ADR-010` (Phase 1 proposals): original source instead of Metaflop GPL code; browser preview/Python compiler split; JSON canonical model; fontmake/fontTools; opentype.js outline inspector; variable weight after static quality; Latin/Cyrillic co-design; authored mono later; local overrides; topology-separated switches.

## Deviations / technical debt
Browser URL policy blocked direct rendering of the local SingleFile; static DOM/CSS, official JS and screenshot supplied the reverse-spec. The UFO spec repository did not expose a root LICENSE; no prose/assets are copied. Full-font quality, native Cyrillic review and whole-repertoire variable compatibility remain Phase 1/2 work.

## Problems discovered
The previous ROADMAP spec path was stale (`.progressive/project/phases/...`) and its standalone `Status:` lines were not discoverable by PCK `context_compile.py`; phase bullets now point to `.progressive/phases/` and preserve the section goals. The official Bespoke marketing page says 14 parameters while captured source/UI expose 16. WOFF2 required Brotli in the isolated spike venv.

## Verification evidence
- `npm run verify` in `research/font-lab/spikes/browser-outline/` → Chromium parsed original font (~6 ms), rendered SVG and live text, applied 1.2 width visual transform, zero page errors.
- `/tmp/pfl-research-venv/bin/python research/font-lab/spikes/variable-build/build.py` → static OTF/TTF, variable TTF and WOFF2; all reopened via `TTFont`; fvar/gvar present; intermediate instancing changed H geometry.
- `python3 research/font-lab/spikes/local-axis/probe.py` → six cases verified, switch changes contour topology.
- `python3 .progressive/tools/audit.py` → pass with 12 pre-existing global/project skill-name collision warnings; `routing_integrity.py` → pass.
- `python3 .progressive/tools/context_compile.py --output /tmp/pfl-phase1-context.md` → active Phase 1 and previous Phase 0 Completion Record both included.
- Required research files and ten ADRs counted; JSON/Python syntax passed, 45 research Markdown docs had zero broken relative links, and the summary matched 15 pinned repositories/16 parameters/10 ADRs.

## Architectural impact
Phase 1 can rely on toolchain feasibility and a sourced proposal, not on a complete font or proven production performance. Canonical current/proposed shape: `.progressive/project/ARCHITECTURE.md`; detailed choices: research ADRs.

## Follow-up
Execute Phase 1a vertical slice from research report §9, then progress toward the V1 Latin + Russian Cyrillic release gate in `.progressive/phases/01-technical-sans-mvp.md`.
