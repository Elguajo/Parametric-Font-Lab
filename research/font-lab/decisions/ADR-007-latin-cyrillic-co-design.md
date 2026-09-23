# ADR-007 — Script architecture

Status: Proposed for Phase 1
Date: 2026-09-23

## Context and options

A: Latin first then add Cyrillic via resemblance (fast prototype, high quality debt); B: shared metrics/primitives with script-specific recipes and concurrent release gate (more design effort).

## Evidence

Bespoke T1 source is Latin-only; Russian Cyrillic needs distinct Д/Л/Ж/К/У/Ф/Я/д/л/т/б forms and script spacing.

## Recommendation

B. Author Latin and Russian Cyrillic concurrently, validate with native review.

## Consequences

Positive: consistent cross-script quality. Cost: larger first release. Revisit expanded Slavic variants after V1.
