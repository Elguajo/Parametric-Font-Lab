# Third-party notices

The v1/v2 geometric recipe path uses the tools below. The v3 default also bundles Inter 4.1
font source under SIL OFL 1.1. Its outlines and spacing form PFL Sans; full attribution,
license and source hash are in `vendor/inter/`. No Metaflop or GPL font geometry is included.

| Package | Pinned version | License | Use |
| --- | --- | --- | --- |
| fontmake | 3.11.0 | Apache-2.0 | Compile generated UFO/Designspace into static TTF/OTF |
| fontTools | 4.66.0 | MIT | Font tables and WOFF2 conversion |
| ufoLib2 | 0.18.1 | Apache-2.0 | Write generated UFO source |
| Brotli | 1.1.0 | MIT | WOFF2 compression support |
| Playwright | 1.58.0 | Apache-2.0 | Local browser verification |

The compiler records the resolved `fontTools` version in each build manifest. The full locked
compiler graph is in `requirements.lock`; the glyph recipes
for v1/v2 and their generated outlines are authored in this repository. The v3 project is
`fontlab/project.json` and uses the licensed Inter source.
