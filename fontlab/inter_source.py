"""Version 3 projects backed by the pinned Inter 4.1 source font."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "vendor/inter/InterVariable.ttf"
SOURCE_SHA256 = "4989b125924991b90d05b2d16e0e388c48f7d5bb8b30539bbf9c755278d0ccaf"
CONTROL_TEXT = "H O A V C S n o b d e | Н О С Д Л Ж К Я и н о п б д л е ь\nbone done | нос сон дно поле дело | AV VA AO АО ДО ДЛ b ь"
PRESETS = {"text": {"weight": 400, "opticalSize": 14}, "display": {"weight": 500, "opticalSize": 32}}


def load_project(path: Path) -> dict:
    raw = path.read_bytes()
    if len(raw) > 65536:
        raise ValueError("v3 project exceeds 65536 bytes")
    project = json.loads(raw.decode("utf-8"))
    if not isinstance(project, dict) or set(project) != {"schemaVersion", "id", "name", "engine", "axes", "activePreset"}:
        raise ValueError("v3 project has missing or unsupported fields")
    if project["schemaVersion"] != 3 or project["engine"] != {"id": "inter-derived", "version": "3.0"}:
        raise ValueError("v3 project has an unsupported schema or engine")
    if not isinstance(project["id"], str) or not 1 <= len(project["id"]) <= 80 or not all(c in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in project["id"]):
        raise ValueError("v3 project id must be lowercase letters, digits, or hyphens")
    if not isinstance(project["name"], str) or not 1 <= len(project["name"]) <= 100:
        raise ValueError("v3 project name is required")
    if project["activePreset"] not in ("text", "display", "custom"):
        raise ValueError("unsupported v3 preset")
    axes = project["axes"]
    if not isinstance(axes, dict) or set(axes) != {"weight", "opticalSize"}:
        raise ValueError("v3 supports only weight and opticalSize")
    for key, low, high in (("weight", 100, 900), ("opticalSize", 14, 32)):
        value = axes[key]
        if isinstance(value, bool) or not isinstance(value, (float, int)) or not low <= value <= high:
            raise ValueError(f"v3 {key} must be between {low} and {high}")
    return project


def rename_font(font) -> None:
    """Give the modified outlines a distinct family while retaining OFL attribution."""
    for record in font["name"].names:
        if record.nameID in (0, 7, 8, 9, 11, 12, 13, 14):
            continue
        original = record.toUnicode()
        if "Inter" not in original:
            continue
        replacement = original.replace("Inter", "PFLSans" if record.nameID in (3, 6, 25) or record.nameID >= 259 else "PFL Sans")
        record.string = replacement.encode("utf-16-be") if record.isUnicode() else replacement.encode("latin-1", errors="replace")
