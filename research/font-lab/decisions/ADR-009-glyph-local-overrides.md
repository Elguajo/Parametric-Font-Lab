# ADR-009 — Local parameter semantics

Status: Proposed for Phase 1
Date: 2026-09-23

## Context and options

A: every local change becomes a global OpenType axis (axis proliferation); B: glyph-local semantic override resolved before generating masters (predictable, no fvar explosion).

## Evidence

Spike C changes only O counter while H is stable; Fontra documents local axes but its GPL editor is reference-only.

## Recommendation

B. LocalAxis stores glyph ID, inherited source axis and validated override.

## Consequences

Positive: precise glyph control. Cost: exports need recompute affected glyph/spacing. Revisit if future format offers standardized local variation semantics.
