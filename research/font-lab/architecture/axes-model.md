# Axis model (proposed ranges, not established product limits)

Store semantic normalized coordinates separately from OpenType user-space values. `wght`, `wdth`, `opsz` are registered tags; uppercase four-character tags below are proposed custom axes and need naming review. A source-level control is not automatically exported as a variable axis. Continuous export requires compatible contours and metric interpolation at every master. UI normalization can be nonlinear via a documented mapping curve; do not present raw geometric values as uniform perceptual steps.

| Control | Proposed source range / mapping | Scope; affected geometry | Main conflict / VF route |
|---|---|---|---|
| Weight `wght` | 100–900; nonlinear thickness mapping | global stems, joins, spacing | small counters; **V1 variable candidate** |
| Width `wdth` | 75–125%; optical, not affine | global bowl/advances | narrow apertures; Phase 2 candidate |
| X-height `XHGT` | .45–.62 em | global lowercase, marks | cap/ascender; source-only V1 |
| Cap-height `CPHT` | .67–.75 em | global uppercase/marks | vertical metrics; source-only |
| Contrast `CNTR` | 0–1 normalized | style-specific stroke distribution | weight/junctions; defer VF |
| Roundness `ROND` | 0–1 | global curves/corners | compatibility across sharp corners; source-only |
| Superness `SPRN` | .25–1 curve tension | geometric style engine | counter collapse; source-only |
| Aperture `APRT` | 0–1 | global open forms, local override | weight and text size; source-only |
| Terminal angle `TRMA` | -45–45° | style-specific terminal recipes | flat/rounded switch is discrete |
| Taper `TAPR` | 0–1 | joins/terminal stroke | contrast, optical size |
| Optical/Text↔Display `opsz` | 8–72 pt design intent; nonlinear | global apertures, details, spacing | requires curated masters; Phase 2+ |
| Mono amount `MONO` | 0–1 | global widths + redrawn forms | spacing/text reflow; **defer** variable until compatible masters |
| Tech↔Neutral `TECH` | 0–1 | style-engine details | can change topology; source-only, limit range |
| Soft↔Sharp `SOFT` | 0–1 | corners and terminals | terminal construction switch; defer |

For V1 expose a disciplined subset: weight, width, x-height, aperture, roundness and a small curated tech/detail control, with fixed but adjustable optical corrections. Keep `opsz`, contrast and mono architecture-ready but outside initial export guarantee. Local axes use a glyph ID and semantic property (e.g., O.counterOpen) and may inherit/offset a global axis; they do not add global `fvar` axes. Source validation rejects out-of-range or incompatible combinations rather than silently clipping.
