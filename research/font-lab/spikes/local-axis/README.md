# Spike C — global, local and structural state

Run `python3 research/font-lab/spikes/local-axis/probe.py`. It writes six original SVG/JSON cases and asserts three independent changes: global weight alters H, local counter width alters only O, and the `a` single/double construction switch changes path count. Observed: `6 cases verified; switch changes contour topology`.

This supports a data model with project axes, per-glyph overrides, and enum construction variants. `proof.svg` is illustrative only: it is not a valid font, and the double-storey `a` is a topology marker rather than a typographically correct design. The structural branch must compile as a separate topology family or alternate glyph; do not interpolate it inside one variable master set. The original experimental shapes are CC0 under the same test-asset policy as Spike B.
