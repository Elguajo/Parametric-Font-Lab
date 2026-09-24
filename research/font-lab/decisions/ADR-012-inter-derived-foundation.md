# ADR-012 — Inter-derived readable foundation

Status: Accepted; supersedes ADR-011 for the default product source
Date: 2026-09-24

## Context

The original geometric recipe engine completed technical Phase 02 checks, but its text looked
hand-drawn and visually unacceptable to the product owner. More exception patches would not
establish a coherent typeface. The user requested an Inter-like basis and authorized the change.

## Decision

Use the official Inter 4.1 variable TTF as a pinned, OFL-licensed source for a renamed PFL Sans
family. Retain the original v1/v2 recipe path for saved projects and historical comparison. The
new v3 project has only native `wght` (100–900) and `opsz` (14–32) controls; Text is 400/14 and
Display is 500/32. The browser loads a renamed WOFF2 derived from the same source and gates
proof visibility on an explicit successful FontFace load. Exports instantiate a static TTF and
WOFF2, preserving Inter shaping/spacing tables and carrying a copy of the OFL license.

## Compatibility and consequences

`schemaVersion: 3`/engine `inter-derived` is separate from v1/v2 `technical-sans`. No automatic
migration maps old width, x-height, roundness, aperture or construction settings to Inter. A
v1/v2 saved JSON retains its prior meaning and remains exportable. The default workbench is v3;
the v2 UI remains at `web/legacy.html`. The output is a derivative of Inter, not an original font.
No production variable binary is exported. Product-specific letter changes would require a
separate type-design decision with clear provenance and quality review.

## Source and license

Official release: `https://github.com/rsms/inter/releases/download/v4.1/Inter-4.1.zip`.
The pinned TTF SHA-256, upstream archive hash and OFL attribution are recorded in
`vendor/inter/README.md` and `vendor/inter/LICENSE.txt`.
