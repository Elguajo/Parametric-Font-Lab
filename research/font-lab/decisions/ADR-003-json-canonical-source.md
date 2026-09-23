# ADR-003 — Canonical editable source

Status: Proposed for Phase 1
Date: 2026-09-23

## Context and options

A: UFO-first (standard interchange, poor fit for semantic recipe/switch state); B: versioned project JSON plus generated UFO/Designspace (extra generator, human-readable semantic state).

## Evidence

UFO stores contours/components; the local-axis spike has per-glyph and enum state beyond a master UFO. UFO/Designspace build succeeded as derived output.

## Recommendation

B. JSON Schema owns project intent; UFO/Designspace are deterministic build artifacts.

## Consequences

Positive: retains recipes and migrations. Cost: schema/versioning and deterministic generator. Revisit if an editor-native source format proves capable of preserving all semantics.
