# ADR-001 — Metaflop/Bespoke reuse

Status: Proposed for Phase 1
Date: 2026-09-23

## Context and options

A: copy or fork GPL web/Bespoke source into product (fast initial behavior, license and old-pipeline cost); B: use as documented interaction/typography reference and author original source (more initial design work, clean ownership).

## Evidence

GPLv3 web `license`, GPLv3-or-later Bespoke `font.mf` header, server METAFONT pipeline, Latin T1 coverage. See license matrix and engine analysis.

## Recommendation

B. Keep source and visual assets reference-only; no code/glyph tracing.

## Consequences

Positive: licensing and architecture independence. Cost: original recipe/type design effort. Revisit if the product explicitly chooses GPL distribution and can support the legacy pipeline.
