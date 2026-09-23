# Spike B — UFO/Designspace static and variable build

Run in disposable environment:

```sh
python3 -m venv /tmp/pfl-research-venv
/tmp/pfl-research-venv/bin/pip install 'fontmake==3.11.0' 'Brotli==1.2.0'
/tmp/pfl-research-venv/bin/python research/font-lab/spikes/variable-build/build.py
```

`build.py` creates two **original CC0** compatible source UFOs (`masters/Light.ufo`, `masters/Bold.ufo`) and `masters/PFLResearch.designspace`; these small sources are committed. Compiled `out/` is ignored. Observed on macOS Python 3.12, fontmake 3.11.0 / fontTools 4.65.0: static Light/Bold TTF + OTF; one Variable TTF (`fvar`, `gvar`, `HVAR`, `MVAR`); static and variable WOFF2. `TTFont` reopened every output; cmap has space/H/O. `fontTools.varLib.instancer` at `wght` 100/140/180 kept H's 12 points and moved a sampled edge from x=520 to 480 to 440, confirming interpolation. Sizes: static TTF 964–1020 B, OTF 1008–1052 B, variable TTF 1300 B, static WOFF2 444–460 B, variable WOFF2 552 B. First run failed at WOFF2 because isolated venv lacked Brotli; installing Brotli fixed it. The final rebuild finished in ~0.75 s locally, not a production latency measure.

The glyphs are geometric rectangles, intentionally unsuitable as a real typeface. This proves tooling compatibility, not outline quality, hinting, Unicode breadth, kerning, variable master compatibility under nonlinear recipes, or production readiness. `fontmake -o variable` emits variable TTF; an OTF variable build would be a separate CFF2 target. License: [`LICENSE.md`](LICENSE.md).
