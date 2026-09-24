# ADR-011 — Type-quality source strategy

Status: Historical; superseded for the default product source by ADR-012 after owner review
Date: 2026-09-24

## Context

The completed static workbench exports 164 mapped characters, but its broad geometric recipes
still produce distinguishability and text-rhythm defects. The research audit and later comparison
are consolidated in [`type-quality-change-review.md`](../audits/2026-09-24-type-quality-change-review.md).
The current Designspace contains one source and does not represent an interpolated family.

## Options considered

- Keep patching generic bars/rings: low initial disruption, but glyph-specific corrections and
  spacing would remain exceptions to an unsuitable common skeleton.
- Replace the entire source with authored multi-master outlines: enables interpolation, but
  incurs compatibility work before the static text face is designed or approved.
- Author original glyph-specific parametric contours and optical/spacing rules, adding
  compatible masters selectively after a demonstrated need and separate variable-font decision.

## Decision

Use the third approach. First establish a coherent static Text design on a representative
Latin/Cyrillic corpus, with glyph-specific forms, sidebearings, kerning and optical corrections.
Retain the current Python fontmake/fontTools static build path and quick browser-source preview;
check the compiled font separately as the export truth. Only add compatible masters for axes
whose quality is demonstrated, and only schedule a variable-font deliverable after the explicit
decision already required by the Project Brief. Discrete construction alternatives remain
separate recipe families unless their outlines are proven compatible.

## Consequences

The source evaluator and browser proof must stay geometrically aligned. Existing saved project
JSON must not silently change meaning; version or migrate its semantics before any breaking
change. Early work focuses on a small control corpus, then expands to all 164 mapped glyphs.
The policy of original outlines and reference-only GPL editor/source material remains in force.
