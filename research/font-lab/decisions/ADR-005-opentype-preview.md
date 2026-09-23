# ADR-005 — Browser outline parser

Status: Proposed for Phase 1
Date: 2026-09-23

## Context and options

A: native CSS only (best text shaping, no contour inspector); B: opentype.js path parser plus native CSS text (inspector and specimen); C: HarfBuzz WASM for all preview (correct shaping, larger integration).

## Evidence

Browser spike used opentype.js 2.0.0 to render SVG contours and native font face to render text; upstream API documents variable instances.

## Recommendation

B. Add HarfBuzz only for exact shaping proof when CSS is insufficient.

## Consequences

Positive: simple responsive inspector. Cost: distinguish path preview from shaped text; parse untrusted files only after security design. Revisit for complex script/feature debugging.
