"""Compile a static, renamed OFL instance from the pinned Inter 4.1 source."""

from __future__ import annotations

from datetime import datetime, timezone
from hashlib import sha256
from html import escape
import json
from pathlib import Path
from shutil import copyfile
import sys

from fontTools import __version__ as fonttools_version
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

from fontlab.identity import build_id, engine_hash
from fontlab.inter_source import CONTROL_TEXT, ROOT, SOURCE, SOURCE_SHA256, rename_font
from fontlab.recipes import source_hash


def _set_name(font: TTFont, name_id: int, value: str) -> None:
    font["name"].setName(value, name_id, 3, 1, 0x409)
    font["name"].setName(value, name_id, 1, 0, 0)


def _validate_font(path: Path) -> None:
    font = TTFont(path)
    if "fvar" in font or not {"glyf", "GPOS", "GSUB", "cmap", "name"}.issubset(font.keys()):
        raise RuntimeError(f"{path.name}: static font or shaping tables are invalid")
    cmap = font.getBestCmap()
    for character in CONTROL_TEXT.replace(" ", "").replace("\n", ""):
        if ord(character) not in cmap:
            raise RuntimeError(f"{path.name}: missing {character}")
    shapes = []
    for character in "ДЛbь":
        pen = RecordingPen()
        font.getGlyphSet()[cmap[ord(character)]].draw(pen)
        shapes.append(pen.value)
    if shapes[0] == shapes[1] or shapes[2] == shapes[3]:
        raise RuntimeError(f"{path.name}: ambiguous control outlines")
    names = {record.toUnicode() for record in font["name"].names if record.nameID in (1, 4, 6)}
    if not any("PFL Sans" in name for name in names) or any("Inter" in name for name in names):
        raise RuntimeError(f"{path.name}: derivative family was not renamed")


def build_inter_font(project: dict, output_dir: Path) -> None:
    if sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise RuntimeError("pinned Inter 4.1 source differs from the recorded SHA-256")
    project_hash = source_hash(project)
    revision = engine_hash()
    identity = build_id(project_hash, revision)
    instance = output_dir / identity
    fonts = instance / "fonts"
    fonts.mkdir(parents=True, exist_ok=True)
    license_path = instance / "OFL-LICENSE.txt"
    copyfile(ROOT / "vendor/inter/LICENSE.txt", license_path)
    weight = project["axes"]["weight"]
    optical_size = project["axes"]["opticalSize"]
    font = instantiateVariableFont(TTFont(SOURCE), {"wght": weight, "opsz": optical_size}, inplace=True)
    rename_font(font)
    style = f"W{weight:g} O{optical_size:g}"
    _set_name(font, 1, "PFL Sans")
    _set_name(font, 2, style)
    _set_name(font, 3, f"PFL-Sans-{identity[:12]}")
    _set_name(font, 4, f"PFL Sans {style}")
    _set_name(font, 6, f"PFLSans-{identity[:12]}")
    _set_name(font, 16, "PFL Sans")
    _set_name(font, 17, style)
    instance_name = f"PFLSans-{identity[:12]}"
    ttf_path = fonts / f"{instance_name}.ttf"
    font.save(ttf_path)
    font.flavor = "woff2"
    woff2_path = fonts / f"{instance_name}.woff2"
    font.save(woff2_path)
    for path in (ttf_path, woff2_path):
        _validate_font(path)
    rows = "".join(f'<div class="proof" style="font-size:{size}px"><span class="size">{size} px</span>{escape(CONTROL_TEXT)}</div>' for size in (10, 14, 24, 72))
    proof_html = f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>PFL Sans compiled proof {identity[:12]}</title>
<style>body{{font-family:Arial,sans-serif;margin:24px}}.proof{{white-space:pre-wrap;line-height:1.45;margin:18px 0;display:none}}.size{{display:block;font:12px Arial;color:#555}}body[data-proof-state="ready"] .proof{{display:block;font-family:PFLCompiled;font-synthesis:none}}#status[data-error]{{color:#b5121b}}</style>
<h1>Compiled font proof</h1><p>Project: {escape(project['id'])} · Source: {project_hash[:16]} · Engine: {revision[:16]} · {escape(style)}</p>
<p id="status" role="status">Loading compiled WOFF2…</p>{rows}
<script>const face=new FontFace('PFLCompiled','url(./fonts/{woff2_path.name}) format("woff2")');
face.load().then(font=>{{document.fonts.add(font);document.body.dataset.proofState='ready';document.getElementById('status').textContent='Compiled WOFF2 loaded';}}).catch(error=>{{document.body.dataset.proofState='error';let status=document.getElementById('status');status.dataset.error='';status.textContent='Compiled font failed to load: '+error.message;}});</script></html>'''
    (instance / "proof.html").write_text(proof_html, encoding="utf-8")
    paths = (ttf_path, woff2_path)
    manifest = {
        "project": project["id"], "sourceHash": project_hash, "engineHash": revision,
        "buildId": identity, "instanceName": instance_name,
        "source": {"name": "Inter 4.1", "sha256": SOURCE_SHA256, "license": "SIL OFL 1.1", "path": "vendor/inter/LICENSE.txt"},
        "licenseFile": license_path.name, "licenseHash": sha256(license_path.read_bytes()).hexdigest(),
        "compiler": {"fontTools": fonttools_version, "python": sys.version.split()[0]},
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "fonts": [str(path.relative_to(instance)) for path in paths],
        "binaryHashes": {str(path.relative_to(instance)): sha256(path.read_bytes()).hexdigest() for path in paths},
        "proof": "proof.html", "proofHash": sha256(proof_html.encode("utf-8")).hexdigest(),
    }
    (instance / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
