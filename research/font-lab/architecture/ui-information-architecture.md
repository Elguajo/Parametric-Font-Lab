# Font Lab V1 information architecture

Top bar: project title/status, presets, compare A/B, export. Left parameter rail: Global, Glyph, Optical, Spacing, Advanced (some collapsed). Center: persistent Glyph Inspector or Live Specimen. Right: searchable chart with Latin/Cyrillic filter, coverage and metrics. Bottom resizable specimen: editable text, size, script/language, A/B compare. On narrow screens, chart and controls become tabs/drawers while specimen stays visible.

Primary loop: choose glyph or text → change a grouped control with slider or numeric input → see draft outline/text immediately → compare or undo → validate and export. Selecting a glyph reveals **local** overrides and construction switches without changing global settings. Keyboard access, focus indicators, value units and invalid-range messages are explicit. Loading states distinguish fast preview from server compilation. Presets are immutable snapshots; A/B compares source hashes, not just screenshots. Export dialog states repertoire, selected switch set, formats, variable-axis support and build diagnostics.

Metaflop's `parameters → glyph/chart → typewriter` spatial model remains, but its fixed 1000 px layout, tiny controls and hidden precision mode need redesign. No full Bézier editor in V1.
