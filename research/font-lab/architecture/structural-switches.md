# Structural switches

A switch selects a named, separately authored recipe family. Each choice has its own compatible master topology; the switch is serialized as an enum and mapped to alternate glyphs/OpenType stylistic sets where appropriate. Do not interpolate across branches by adding/removing contours in an OpenType variable axis. Maintain common advance/anchors when possible, then re-run spacing and kerning per choice.

| Glyph | Choices / risk |
|---|---|
| Latin `a`, `g` | single / double storey; radically different counter/ear topology |
| `4` | open / closed apex; contour count and interior white |
| `0` | plain / slashed / dotted; overlay and collision, `zero` feature candidate |
| `Q` | internal/external/short tail; bowl/tail join and descent |
| `R` | straight/curved leg; branch darkness and advance |
| `1` | foot/no foot; number alignment |
| `G` | spur/no spur/short spur; aperture |
| terminal family | flat / angled / rounded; may alter contour topology |

Cyrillic: `Д` and `д` (legs/base), `Л` and `л` (triangular vs curved left entry), `Ж`/`ж` (diagonal junction), `К`/`к` (arm/leg junction), `У` (diagonal/tail), `Ф`/`ф` (center stem/bowl), `Я` (leg and bowl), `т` (m-like vs t-like form), `б` (head/spur). These are design exploration targets, not automatic Latin substitutions. Confirm language-specific variants with Cyrillic typographic review; `locl` where a form is language dependent, `ssXX` for user-selectable alternates.

V1 author `a` single/double and `0` plain/slashed only after script baseline works. Remaining listed switches stay in the schema and roadmap, not a promise of immediate glyph coverage. Verification matrix: each switch × min/default/max weight × script specimen → contour validity, counter area, advance, kerning, and expected alternate mapping.
