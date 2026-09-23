# Metaflop visual tokens and V1 translation

Extracted from saved CSS and [upstream SCSS](https://github.com/metaflop/metaflop-www/blob/036c26b9f58f1264dba61d3818b7fae6869141e7/assets/stylesheets/_variables.scss). Approximate rendered values may differ by browser/font rasterization.

| Token | Metaflop observed |
|---|---|
| Base / Modulator background | `#f2f2f2` / `#e6ffd7` (panels) |
| Main page / text | white / near black |
| Link / disabled / hover | `#666` / lighter gray / `#f00` |
| Error | `#ab1e1e` |
| Typography | Helvetica/sans-serif, 15 px body, 22.5 px line height; headings 15 px bold; normal text forced lowercase in CSS, preview overrides context |
| Content widths | 1000 px total, left 259, right 710, horizontal gap 31; two preview boxes 339.5 each |
| Vertical spacing | 7 px between boxes; navigation uses 15.5 px vertical padding; group line height 24 px |
| Inputs | numeric width 37 px, height 14 px, 1 px `#ccc9bc` border; select height 14 px; slider row 24 px |
| Panels | squared corners, no shadow; black 1 px rule below legends |
| Icons / focus | Font Awesome ~13 px actions; hover link red; a comprehensive visible keyboard focus style was not found in inspected CSS |

This is a reference inventory, not proposed product branding. Future neutral tokens are in `architecture/ui-tokens-proposal.md`; focus affordances and touch target sizes need redesign.
