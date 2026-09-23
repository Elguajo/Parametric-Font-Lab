# ADR-010 — Discrete constructions

Status: Proposed for Phase 1
Date: 2026-09-23

## Context and options

A: interpolate mismatched topologies (invalid VF); B: enum-selected recipe families compiled as alternate glyphs/static instances (valid, more sources).

## Evidence

Spike C changes path count across `a` variants; OpenType variable masters require compatible outlines.

## Recommendation

B. Stable enum IDs choose independent compatible families; map selected alternates to GSUB where useful.

## Consequences

Positive: honest topology handling. Cost: per-branch masters and QA. Revisit only if a specific pair can be designed with genuinely compatible contours.
