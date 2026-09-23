# Metaflop component inventory

Evidence: saved DOM and [upstream template](https://github.com/metaflop/metaflop-www/blob/036c26b9f58f1264dba61d3818b7fae6869141e7/app/views/modulator.slim), [parameter template](https://github.com/metaflop/metaflop-www/blob/036c26b9f58f1264dba61d3818b7fae6869141e7/app/views/parameter_panel.slim). `state → input → output / dependency` is as exposed by template, not a tested interaction trace.

| Component | State / input → output / dependency | UX and reuse |
|---|---|---|
| Fixed navigation | Selected route → page; external social/about/FAQ links | Preserve orientation, replace branding |
| Font selector | selected metafont → parameter groups, preview glyph repertoire | Keep as future style-engine selector; changing engine may invalidate project parameters |
| Anatomy toggle | on/off → information panel | Useful educational layer, optional V1 |
| Glyph/chart toggle | on/off → preview visibility | Use tabs or responsive split view |
| Parameter group | group legend + mapped parameters → control rows | Strong hierarchy; preserve grouping, improve labels |
| Slider / numeric adjuster | value, range, default; dummy/nerd mode → regenerate preview | Keep both precision and direct manipulation; accessible native controls |
| Reset/random/undo | current values/history → parameter set | Keep; random should use bounded, deterministic seed |
| Glyph preview + chooser | selected glyph → large preview; arrows/list switch glyph | Keep; add local controls and metrics |
| Alphabet chart | glyph cells → overview/selection | Keep, add script and coverage status |
| Typewriter | text preset, size, editable textarea → live specimen | Keep, add language and A/B controls |
| Share | social/mail/copy → parameter URL | Replace with shareable project/preset link after storage model exists |
| Download | OTF or webfont ZIP → server build | Separate validated export profile and status; future variable font |
| Preset/metafont selector | font selector exists, but a separate preset control is not visible in capture | V1 presets should be first-class |

No A/B compare, local glyph parameter inspector, structural switch controls, variable-axis controls, script toggle, or build validation feedback are visible in the captured page.
