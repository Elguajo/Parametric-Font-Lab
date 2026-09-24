# Architecture — Parametric Font Lab

Status: PFL Sans v3 default implemented; original v1/v2 engine retained

## Default path

`fontlab/project.json` is `schemaVersion: 3`, engine `inter-derived` 3.0. It has native `weight`
and `opticalSize` values only. The source is the pinned official Inter 4.1 variable TTF at
`vendor/inter/InterVariable.ttf` (SIL OFL 1.1); a renamed derivative WOFF2 in `web/fonts/`
provides live browser proof. `FontFace.load()` must succeed before chart and specimens appear.
The browser applies `wght` and `opsz` to real font text. The static exporter uses fontTools
`varLib.instancer` to make TTF and WOFF2 with cmap, GPOS and GSUB preserved. The modified family
is named PFL Sans and each export carries `OFL-LICENSE.txt`.

## Legacy path and compatibility

`fontlab/project-v1.json` and `fontlab/project-v2.json` retain the historical `technical-sans`
source semantics, schemas, recipes and compiler. `web/legacy.html` displays the v2 SVG workbench.
Legacy export remains UFO/Designspace → TTF/OTF/WOFF2. v3 does not reinterpret old controls or
silently convert saved projects. The original Phase 1 completion and ADR-011 remain historical.
ADR-012 owns the default source pivot.

## Proof identity

The build ID combines canonical selected-project JSON and a content hash of recipes, compiler,
source TTF, browser preview WOFF2 and dependency lock. `verify_compiled_proof.py` checks that
identity, binary hashes, proof hash and the v3 OFL license hash. Missing, changed or stale assets
fail before the compiled proof is accepted. Browser proof pages explicitly load their WOFF2 and
hide specimens on failure.

## Limits

The v3 export is static; the variable source is used only to pick instances and preview native
axes. This does not validate every weight/optical-size combination or establish original
product-specific glyph design. At weight 900 and 10 px, text is visibly dense; weight 100 is
faint at 10 px. Legacy v2's
five recipe controls still have the source limitations recorded in Phase 02.
