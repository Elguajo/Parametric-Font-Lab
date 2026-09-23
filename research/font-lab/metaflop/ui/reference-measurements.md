# Screenshot/DOM geometry cross-check

The 2976 px wide capture shows a centered ~2000 px content block, corresponding to the 1000 CSS px `#main` rail in upstream SCSS at 2× scale. Main left rail begins near x=488 px; left panel width ~518 px (259 CSS px); gap to glyph preview ~62 px (31 CSS px). Glyph and chart are each ~679 px (339.5 CSS px) with ~62 px gutter. Right rail totals ~1420 px (710 CSS px). Navigation remains aligned above; content begins about 154 px down (77 CSS px). The screenshot confirms design-token proportions rather than supplying independent viewport metadata.

DOM regions: `#navigation`; `#col1 > #menu + #parameter-panel`; `#col2 > #preview-panel > #preview-single + #preview-chart + #preview-typewriter`. SingleFile CSS and upstream SCSS provide actual dimensions. Chart content is static uppercase, lowercase and digits; chooser is under the large glyph. The parameter column extends to the screenshot bottom, so vertical scrolling is page-level. No standalone preset/A-B/script region appears.

Browser rendering of this local SingleFile was blocked by URL policy. Measurements are screenshot estimates backed by CSS source; do not treat them as automated bounding-box output.
