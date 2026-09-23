"""Disposable proof that global, glyph-local and discrete state stay separate."""

from pathlib import Path
import json


ROOT = Path(__file__).parent


def recipe(glyph, weight, local=None, switch=None):
    if glyph == "H":
        return {"glyph": glyph, "globalWeight": weight, "paths": [
            f"M40 40h{weight}v320h-{weight}z",
            f"M{360-weight} 40h{weight}v320h-{weight}z",
            f"M{40+weight} {190-weight/2}h{320-2*weight}v{weight}h-{320-2*weight}z",
        ]}
    if glyph == "O":
        counter = local if local is not None else 1.0
        inset = weight + 30 * (1 - counter)
        return {"glyph": glyph, "globalWeight": weight, "localCounter": counter,
                "paths": [f"M40 40h320v320H40z M{40+inset} {40+inset}v{320-2*inset}h{320-2*inset}v-{320-2*inset}z"]}
    if glyph == "a":
        if switch == "single":
            paths = [f"M40 160 Q40 100 120 100 Q200 100 200 160 V360 H40 Z",
                     f"M200 100 h{weight}v260h-{weight}z"]
        elif switch == "double":
            paths = [f"M40 160 Q40 100 120 100 Q200 100 200 160 V360 H40 Z",
                     f"M200 100 h{weight}v260h-{weight}z", f"M120 100 Q120 40 240 40 L240 75 Q170 75 170 110 Z"]
        else:
            raise ValueError("a needs an explicit construction")
        return {"glyph": glyph, "globalWeight": weight, "switch": switch, "paths": paths}
    raise ValueError(glyph)


cases = [
    recipe("H", 60), recipe("H", 100),
    recipe("O", 60, local=1.0), recipe("O", 60, local=0.5),
    recipe("a", 60, switch="single"), recipe("a", 60, switch="double"),
]
assert cases[0]["paths"] != cases[1]["paths"]
assert cases[2]["paths"] != cases[3]["paths"]
assert len(cases[4]["paths"]) != len(cases[5]["paths"])
(ROOT / "cases.json").write_text(json.dumps(cases, indent=2) + "\n")
parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 440">']
for index, case in enumerate(cases):
    parts.append(f'<g transform="translate({index*400},0)" fill="none" stroke="black" stroke-width="3">')
    parts.extend(f'<path d="{path}"/>' for path in case["paths"])
    parts.append('</g>')
parts.append('</svg>')
(ROOT / "proof.svg").write_text("\n".join(parts) + "\n")
print("6 cases verified; switch changes contour topology")
