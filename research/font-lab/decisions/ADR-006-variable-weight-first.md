# ADR-006 — Variable font release strategy

Status: Proposed for Phase 1
Date: 2026-09-23

## Context and options

A: expose all source controls as one high-dimensional VF (master explosion, topology risk); B: static V1, curated weight VF after compatible repertoire and metrics; C: no VF ever (misses product goal).

## Evidence

Spike proves one compatible weight axis technically; structural branches changed path count; full Latin/Cyrillic quality is not yet authored.

## Recommendation

B. Static quality first, then weight, width and optical axes with independent gates.

## Consequences

Positive: limits compatibility/QA surface. Cost: later variable delivery. Revisit after full-repertoire master tests.
