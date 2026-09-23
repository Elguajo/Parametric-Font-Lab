"""Disposable, original-outline UFO/Designspace compilation experiment."""

from pathlib import Path
import subprocess
import sys

from fontTools.designspaceLib import AxisDescriptor, DesignSpaceDocument, SourceDescriptor
from fontTools.ttLib import TTFont
from ufoLib2 import Font


ROOT = Path(__file__).parent
OUT = ROOT / "out"
SOURCES = ROOT / "masters"
OUT.mkdir(exist_ok=True)
SOURCES.mkdir(exist_ok=True)


def rectangle(pen, x0, y0, x1, y1, reverse=False):
    points = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    if reverse:
        points.reverse()
    pen.moveTo(points[0])
    for point in points[1:]:
        pen.lineTo(point)
    pen.closePath()


def make_master(weight, name):
    font = Font()
    font.info.familyName = "PFL Research Original"
    font.info.styleName = name
    font.info.unitsPerEm = 1000
    font.info.ascender = 800
    font.info.descender = -200
    font.info.capHeight = 700
    font.info.xHeight = 500
    font.info.openTypeOS2WeightClass = weight
    missing = font.newGlyph(".notdef")
    missing.width = 600
    rectangle(missing.getPen(), 60, 0, 540, 700)
    space = font.newGlyph("space")
    space.width = 300
    space.unicodes = [32]
    glyph = font.newGlyph("H")
    glyph.width = 680
    glyph.unicodes = [72]
    pen = glyph.getPen()
    rectangle(pen, 60, 0, 60 + weight, 700)
    rectangle(pen, 620 - weight, 0, 620, 700)
    rectangle(pen, 60 + weight, 310, 620 - weight, 310 + weight)
    glyph = font.newGlyph("O")
    glyph.width = 680
    glyph.unicodes = [79]
    pen = glyph.getPen()
    rectangle(pen, 60, 0, 620, 700)
    rectangle(pen, 60 + weight, weight, 620 - weight, 700 - weight, reverse=True)
    path = SOURCES / f"{name}.ufo"
    font.save(path, overwrite=True)
    return path


masters = [(100, "Light"), (180, "Bold")]
document = DesignSpaceDocument()
axis = AxisDescriptor()
axis.name = "Weight"
axis.tag = "wght"
axis.minimum = 100
axis.default = 100
axis.maximum = 180
document.addAxis(axis)
for weight, name in masters:
    path = make_master(weight, name)
    source = SourceDescriptor()
    source.name = name
    source.path = str(path.resolve())
    source.familyName = "PFL Research Original"
    source.styleName = name
    source.location = {"Weight": weight}
    if name == "Light":
        source.copyInfo = True
        source.copyLib = True
        source.copyGroups = True
        source.copyFeatures = True
    document.addSource(source)
designspace = SOURCES / "PFLResearch.designspace"
document.write(designspace)

for output in ("ttf", "otf", "variable"):
    subprocess.run(
        [sys.executable, "-m", "fontmake", "-m", str(designspace), "-o", output, "--output-dir", str(OUT / output)],
        check=True,
    )

for path in [*(OUT / "ttf").glob("*.ttf"), *(OUT / "variable").glob("*.ttf")]:
    font = TTFont(path)
    font.flavor = "woff2"
    font.save(path.with_suffix(".woff2"))
    print("woff2", path.name, list(font.keys()))
