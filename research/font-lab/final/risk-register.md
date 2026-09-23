# Risk register

P/I = probability/impact for the proposed first product release (L/M/H). Validation named here is required before declaring a risk retired.

| Risk | P/I | Mitigation | Validation |
|---|---|---|---|
| Geometry complexity | H/H | small grammar, explicit recipe ownership, curate axis ranges | representative glyph matrix across scripts |
| Self-intersections/counter collapse | H/H | constraints and minimum white-area checks | contour scanner + raster proof at corners |
| Master interpolation incompatibility | H/H | stable point IDs/order, branch topology families | fontmake/varLib compile every axis corner |
| Variable font constraints | M/H | weight first, defer structural switches | inspect fvar/gvar/HVAR, instantiate and shape |
| Kerning complexity | H/M | classes plus exceptions, no universal auto claims | shaped pair corpus at widths/weights |
| Cyrillic quality | H/H | authored Cyrillic module + native review from first milestone | Russian specimen and language review |
| Browser performance | M/M | Worker, per-glyph cache, source hash, throttle commits | 100+ glyph/long text benchmarks on target hardware |
| Font parsing security | M/H | no upload V1, later sandbox/size/table caps | malformed font fuzz corpus and resource tests |
| GPL/copyleft contamination | M/H | source-reference only, notice gate | code provenance and dependency/license audit |
| Derivative-font licensing | M/H | original outlines, no commercial morph/import | asset manifest review before release |
| Scope explosion | H/H | five V1 controls, two switches, phase gates | accepted scope checklist per phase |
| Typographic quality at extreme sliders | H/H | design-safe range, curated masters/optical rules | text/display proof at min/default/max |
| Browser/server preview divergence | M/H | versioned semantics + parity corpus | compare paths/metrics from both evaluators |
| Export resource exhaustion | M/H | isolated jobs/time/memory limits and cleanup | stress/time-out tests in hosted stage |
| Missing font notices/metadata | M/M | deterministic export manifest and license template | inspect `name`, OS/2, notices and package contents |

No risk is declared retired by tiny spikes. The build spike lowers toolchain feasibility risk only.
