# Third-party notices

Phase 1a depends on the following tools only for compilation and browser verification. No
third-party font outlines, font sources, or UI assets are bundled or used as recipe input.

| Package | Pinned version | License | Use |
| --- | --- | --- | --- |
| fontmake | 3.11.0 | Apache-2.0 | Compile generated UFO/Designspace into static TTF/OTF |
| fontTools | 4.66.0 | MIT | Font tables and WOFF2 conversion |
| ufoLib2 | 0.18.1 | Apache-2.0 | Write generated UFO source |
| Brotli | 1.1.0 | MIT | WOFF2 compression support |
| Playwright | 1.58.0 | Apache-2.0 | Local browser verification |

The compiler records the resolved `fontTools` version in each build manifest. The full locked
compiler graph is in `requirements.lock`; the glyph recipes
in `fontlab/project.json` and their generated outlines are authored in this repository.
