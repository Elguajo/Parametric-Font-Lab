# Original Geometric/Technical Sans glyph grammar (proposal)

A recipe graph resolves global axes, glyph-local overrides and a named construction before drawing. Primitives share metrics, but each glyph owns optical corrections. Reusing a primitive does **not** imply all glyphs share one skeleton. Store contours with stable point IDs and winding/order for each interpolation family; fail compatibility checks before variable export. Source inspiration is typographic technique, not copied Metaflop formulas.

| Primitive | Inputs and constraints | Optical rule | Candidate glyphs |
|---|---|---|---|
| Stem | thickness, angle, endpoints; minimum counter | overshoot/ink trap at join | H, I, n, Н, П |
| Crossbar | height, thickness, attachment; stay within bowl | overshoot into stem | A, H, Е, А, Н |
| Bowl | width, height, curvature, stroke map; closed orientation | side flattening | O, B, P, Ф, о |
| Counter | inset shape, minimum area; opposite winding | widen optically at heavy weight | O, a, e, Ф, а |
| Arch | spring, crown, stem joins | flatten top | n, h, п, и |
| Shoulder | projection, inflection | soften inner join | r, m, г |
| Spine | bend, tension, endpoints | weight at turns | S, s, З, з |
| Diagonal | angle, thickness, intersections | junction thinning | A, V, Ж, К |
| Leg | origin, slope, landing | preserve white triangle | R, Я, К |
| Tail | attach, direction, length | exit thinning | Q, g, У |
| Terminal | angle, cut/rounded type | compensate apparent length | C, G, c, с |
| Aperture | opening angle, throat | minimum opening under weight | c, e, G, с, э |
| Join | miter/round/ink trap, overlap | remove darkness | k, R, Ж, ж |
| Spur | size, location, branch | overshoot relative to curve | G, б |
| Overshoot zone | baseline/cap/x-height/descender | curve-specific extension | O, o, Ф, ф |

Generation order: metrics → named construction → components → local axis resolution → constraint solver → optical correction → contour normalization → spacing. Component recipes are semantic source, not necessarily UFO components after expansion; flatten before compilation when master transforms differ. Test minimum counters, self-intersections, point order and black/white balance at axis corners. A small quality corpus across Latin and Cyrillic is required before scaling repertoire.
