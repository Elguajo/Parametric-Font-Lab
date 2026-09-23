# ADR-004 — Compiler pipeline

Status: Proposed for Phase 1
Date: 2026-09-23

## Context and options

A: retain METAFONT/mf2outline/FontForge (existing concept, GPL/compatibility issues); B: fontmake/ufo2ft/fontTools (proven UFO/Designspace static+VF); C: fontc Rust (active alternative, extra stack).

## Evidence

Two-master spike emitted static OTF/TTF, variable TTF and WOFF2 via fontmake/fontTools; primary docs describe supported formats.

## Recommendation

B, pinned in isolated Python environment with validation gates.

## Consequences

Positive: mature interoperable pipeline and permissive library licenses. Cost: Python worker and dependency pinning. Revisit if fontc demonstrates concrete quality/performance benefit.
