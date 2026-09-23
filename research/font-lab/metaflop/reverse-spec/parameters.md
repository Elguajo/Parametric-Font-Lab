# Bespoke parameter model in captured Modulator

Evidence: saved input values, [`font.mf`](https://github.com/metaflop/metaflop-font-bespoke/blob/35a9ff885fd3bb4e503b31910f347125df7d978a/font.mf) range comments and [`modulator.js`](https://github.com/metaflop/metaflop-www/blob/036c26b9f58f1264dba61d3818b7fae6869141e7/assets/javascripts/modulator.js). Values are METAFONT source units or ratios, **not** equivalent to future OpenType axis coordinates. JS configures slider step `0.01`; nerd buttons use 0.01/0.1. Linear UI slider range is observed, but visual response is generally nonlinear due to geometry and constraints. All exposed values act globally in Bespoke; none is a glyph-local user control.

| Internal / label | Min–default–max | Meaning / affected parts / conflict |
|---|---|---|
| `u#` / unit width | .75–1.4–2 pt | base horizontal unit, overall proportions and spacing; interacts with pen width |
| `px#` / pen width | .1–.9–1 pt | stroke thickness, counters; high end closes apertures |
| `cap#` / cap height | .75–.9–1 × box | uppercase height, bar and overshoot alignment |
| `bar` / bar height | .25–.5–.75 | crossbar fraction of cap height |
| `asc#` / asc. height | .75–.95–1.25 × box | ascender top; accent collision risk |
| `des#` / desc. height | .25–.3–.75 × box | descender depth and line metrics |
| `mean#` / x-height | .5–.65–1 × cap | lowercase height; top collision at extremes |
| `incx` / horiz. increase | 0–0–.75 | horizontal stroke expansion; joins/counters |
| `incy` / vert. increase | 0–0–.75 | vertical expansion; joins/counters |
| `cont` / contrast | 1–1.1–2 | stroke contrast/positioning; with weight risks pinching |
| `superness` / superness | .25–.74–1 | curve control, round-to-squarer shape response |
| `slant` / slanting | -.75–0–.75 | global transform; spacing/overhang changes |
| `apert` / aperture | 0–.6–.75 | opening in relevant lowercase forms; may close at low value |
| `corner#` / corner | 0–1–1.5 pt | corner treatment, join form |
| `o#` / overshoot | 0–.1–1 pt | curved top/bottom beyond baseline/cap; limit by size |
| `taper` / taper | 0–.5–1 | tapered joins/terminals; interacts with contrast |

Dependency: `mean#` is expressed relative to `cap#`; `barheight#` derives from `bar*cap#`; other derived metrics live in `fontbase.mf`. `sidebearing` is hidden and toggled for OTF export. Official Bespoke page says 14 parameters, but captured DOM and current `font.mf` expose 16; record this as source/copy drift, not an inferred missing control. Captured defaults match the source; the visible UI shows no local axis or construction switch.
