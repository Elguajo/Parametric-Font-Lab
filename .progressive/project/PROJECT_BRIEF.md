# Project Brief — Parametric Font Lab

Status: Phase 1 historical technical MVP complete; Inter-derived readable foundation complete;
product-specific differentiation is the next scoped phase.

## Outcome

Provide a browser font workbench with a genuinely readable Latin/Russian baseline, honest live
preview and trustworthy static export. The current default is PFL Sans, a renamed derivative of
Inter 4.1 under SIL OFL 1.1. Metaflop Modulator remains an interaction reference.

## Current release

The v3 workbench displays actual font glyphs and mixed Latin/Russian text. It exposes native
weight and optical-size controls, Text/Display presets, a downloadable versioned project and
static TTF/WOFF2 export. The original 164-glyph geometric recipe workbench remains available
for v1/v2 saved projects but is not the default readable face. No migration maps its five
controls to Inter. A production variable-font binary, original custom type design across all
164 signs and broad Modulator workflow features remain separate future decisions.

## Constraints

Preserve v1/v2 JSON semantics, license and attribute third-party outlines, and never present a
fallback system font as a successful proof. The release proof is the selected project's compiled
binary at 10/14/24/72 px. The default v3 source decision is ADR-012; ADR-011 remains historical
for the original recipe phase.
