# ADR-002 — Geometry execution boundary

Status: Proposed for Phase 1
Date: 2026-09-23

## Context and options

A: all geometry on server (one implementation, network latency); B: browser Worker preview plus Python server compilation from versioned source (responsive, parity burden); C: all build in browser (offline, difficult isolated font toolchain).

## Evidence

Metaflop server OTF preview has 10 s timeout; browser spike parsed and rendered a tiny original font; fontmake Python build spike works.

## Recommendation

B. Browser handles provisional glyph preview; Python compiles authoritative exports.

## Consequences

Positive: direct manipulation and mature compiler. Cost: browser/server parity corpus and shared semantics. Revisit after representative performance/quality measurements.
