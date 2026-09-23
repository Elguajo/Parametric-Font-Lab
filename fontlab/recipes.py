"""Deterministic, original outline recipes for the Phase 1a slice.

Coordinates are font units.  A contour is a closed sequence of move/line/cubic commands;
the evaluator deliberately has no dependency on a font editor or a third-party font source.
"""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
PROJECT_PATH = ROOT / "project.json"
SCHEMA_PATH = ROOT / "project.schema.json"
KAPPA = 0.5522847498307936
WEIGHT_RANGE = (40.0, 160.0)
COUNTER_RANGE = (0.5, 1.5)
VALID_A_CONSTRUCTIONS = {"single", "double"}


class ProjectValidationError(ValueError):
    """A project document is outside the intentionally small Phase 1a contract."""


def load_project(path: Path | None = None) -> dict[str, Any]:
    with (path or PROJECT_PATH).open(encoding="utf-8") as source:
        project = json.load(source)
    validate_project(project)
    return project


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def source_hash(project: dict[str, Any]) -> str:
    return sha256(canonical_json(project).encode("utf-8")).hexdigest()


def validate_project(project: Any) -> None:
    """Validate the schema-owned fields without accepting forward fields implicitly."""
    if not isinstance(project, dict):
        raise ProjectValidationError("project must be an object")
    required = {"schemaVersion", "id", "name", "engine", "axes", "localOverrides", "switches", "glyphs"}
    _only_keys(project, required, "project")
    if project.get("schemaVersion") != 1:
        raise ProjectValidationError("unsupported schemaVersion")
    if not isinstance(project["id"], str) or not project["id"]:
        raise ProjectValidationError("project id must be a non-empty string")
    if not isinstance(project["name"], str) or not project["name"]:
        raise ProjectValidationError("project name must be a non-empty string")
    engine = project["engine"]
    if engine != {"id": "technical-sans", "version": "1.0"}:
        raise ProjectValidationError("unsupported engine")
    axes = project["axes"]
    _only_keys(axes, {"weight"}, "axes")
    _range(axes["weight"], WEIGHT_RANGE, "weight")
    overrides = project["localOverrides"]
    _only_keys(overrides, {"O"}, "localOverrides")
    _only_keys(overrides["O"], {"counter"}, "localOverrides.O")
    _range(overrides["O"]["counter"], COUNTER_RANGE, "localOverrides.O.counter")
    switches = project["switches"]
    _only_keys(switches, {"aConstruction"}, "switches")
    if switches["aConstruction"] not in VALID_A_CONSTRUCTIONS:
        raise ProjectValidationError("aConstruction must be single or double")
    glyphs = project["glyphs"]
    if not isinstance(glyphs, list) or len(glyphs) != 8:
        raise ProjectValidationError("Phase 1a requires exactly eight glyphs")
    expected = {"H", "O", "a", "zero", "uni041D", "uni041E", "uni0430", "uni043E"}
    names, unicodes = set(), set()
    for glyph in glyphs:
        _only_keys(glyph, {"id", "name", "unicode", "script", "recipe"}, "glyph")
        if glyph["name"] in names or glyph["unicode"] in unicodes:
            raise ProjectValidationError("glyph names and Unicode values must be unique")
        if glyph["script"] not in {"Latn", "Cyrl"}:
            raise ProjectValidationError("unsupported script")
        names.add(glyph["name"])
        unicodes.add(glyph["unicode"])
    if names != expected:
        raise ProjectValidationError("glyph repertoire differs from Phase 1a")


def _only_keys(value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        raise ProjectValidationError(f"{label} fields must be exactly {sorted(expected)}")


def _range(value: Any, limits: tuple[float, float], label: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not limits[0] <= value <= limits[1]:
        raise ProjectValidationError(f"{label} must be within {limits[0]}..{limits[1]}")


def rectangle(x0: float, y0: float, x1: float, y1: float, reverse: bool = False) -> list[tuple]:
    points = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    if reverse:
        points.reverse()
    return [("M", *points[0]), *(("L", *point) for point in points[1:]), ("Z",)]


def oval(cx: float, cy: float, rx: float, ry: float, reverse: bool = False) -> list[tuple]:
    if rx <= 0 or ry <= 0:
        raise ProjectValidationError("counter collapsed")
    commands = [
        ("M", cx + rx, cy),
        ("C", cx + rx, cy + KAPPA * ry, cx + KAPPA * rx, cy + ry, cx, cy + ry),
        ("C", cx - KAPPA * rx, cy + ry, cx - rx, cy + KAPPA * ry, cx - rx, cy),
        ("C", cx - rx, cy - KAPPA * ry, cx - KAPPA * rx, cy - ry, cx, cy - ry),
        ("C", cx + KAPPA * rx, cy - ry, cx + rx, cy - KAPPA * ry, cx + rx, cy),
        ("Z",),
    ]
    if not reverse:
        return commands
    # Reverse cubic topology while retaining the same closed, original ellipse geometry.
    anchors = [(cx + rx, cy), (cx, cy - ry), (cx - rx, cy), (cx, cy + ry), (cx + rx, cy)]
    return [
        ("M", *anchors[0]),
        ("C", cx + rx, cy - KAPPA * ry, cx + KAPPA * rx, cy - ry, *anchors[1]),
        ("C", cx - KAPPA * rx, cy - ry, cx - rx, cy - KAPPA * ry, *anchors[2]),
        ("C", cx - rx, cy + KAPPA * ry, cx - KAPPA * rx, cy + ry, *anchors[3]),
        ("C", cx + KAPPA * rx, cy + ry, cx + rx, cy + KAPPA * ry, *anchors[4]),
        ("Z",),
    ]


def ring(cx: float, cy: float, rx: float, ry: float, inset: float) -> list[list[tuple]]:
    return [oval(cx, cy, rx, ry), oval(cx, cy, rx - inset, ry - inset, reverse=True)]


def evaluate_project(project: dict[str, Any]) -> dict[str, Any]:
    validate_project(project)
    weight = float(project["axes"]["weight"])
    result = []
    for definition in project["glyphs"]:
        contours, width = _recipe(definition, weight, project)
        glyph = {**definition, "advance": width, "contours": contours}
        validate_glyph(glyph)
        result.append(glyph)
    return {"sourceHash": source_hash(project), "glyphs": result}


def _recipe(definition: dict[str, Any], weight: float, project: dict[str, Any]) -> tuple[list[list[tuple]], int]:
    recipe = definition["recipe"]
    if recipe == "cap-h":
        return [
            rectangle(70, 0, 70 + weight, 700),
            rectangle(610 - weight, 0, 610, 700),
            rectangle(70 + weight, 318 - weight / 2, 610 - weight, 318 + weight / 2),
        ], 680
    if recipe == "cap-o":
        # The counter override is intentionally scoped to the Latin O glyph ID only.
        counter = project["localOverrides"]["O"]["counter"] if definition["name"] == "O" else 1.0
        inset = weight + 24 * (1 - counter)
        return ring(340, 350, 270, 360, inset), 680
    if recipe == "zero":
        return ring(340, 350, 235, 350, weight + 8), 680
    if recipe == "small-o":
        return ring(270, 250, 205, 250, weight), 540
    if recipe == "latin-a":
        if project["switches"]["aConstruction"] == "single":
            return _single_storey_a(weight), 540
        return _double_storey_a(weight), 540
    if recipe == "cyrillic-a":
        # Cyrillic keeps its own authored recipe and does not inherit the Latin construction switch.
        return _cyrillic_a(weight), 540
    raise ProjectValidationError(f"unknown recipe {recipe}")


def _single_storey_a(weight: float) -> list[list[tuple]]:
    return [
        *ring(255, 245, 185, 245, weight),
        rectangle(440 - weight, 0, 440, 510),
        rectangle(310, 0, 440, weight),
    ]


def _double_storey_a(weight: float) -> list[list[tuple]]:
    return [
        *ring(250, 185, 175, 185, weight),
        *ring(250, 405, 185, 185, weight),
        rectangle(425 - weight, 0, 425, 520),
        rectangle(265, 288, 425 - weight / 2, 288 + weight),
    ]


def _cyrillic_a(weight: float) -> list[list[tuple]]:
    return [
        *ring(260, 190, 180, 190, weight),
        *ring(260, 400, 180, 180, weight),
        rectangle(430 - weight, 0, 430, 510),
        rectangle(270, 285, 430 - weight / 2, 285 + weight),
    ]


def validate_glyph(glyph: dict[str, Any]) -> None:
    if glyph["advance"] <= 0:
        raise ProjectValidationError(f"{glyph['name']}: non-positive advance")
    for contour in glyph["contours"]:
        if len(contour) < 4 or contour[0][0] != "M" or contour[-1] != ("Z",):
            raise ProjectValidationError(f"{glyph['name']}: contour is not closed")
        endpoints = [(command[-2], command[-1]) for command in contour if command[0] in {"M", "L", "C"}]
        if len(set(endpoints)) < 3:
            raise ProjectValidationError(f"{glyph['name']}: contour has too few points")


def glyph_signature(glyph: dict[str, Any]) -> dict[str, Any]:
    points = [
        (command[-2], command[-1])
        for contour in glyph["contours"]
        for command in contour
        if command[0] in {"M", "L", "C"}
    ]
    return {
        "name": glyph["name"],
        "advance": glyph["advance"],
        "contours": len(glyph["contours"]),
        "bounds": [round(min(x for x, _ in points), 4), round(min(y for _, y in points), 4), round(max(x for x, _ in points), 4), round(max(y for _, y in points), 4)],
        "outline": "|".join(svg_path(contour) for contour in glyph["contours"]),
    }


def parity_signature(project: dict[str, Any]) -> list[dict[str, Any]]:
    return [glyph_signature(glyph) for glyph in evaluate_project(project)["glyphs"]]


def svg_path(contour: list[tuple]) -> str:
    return " ".join(command[0] if command[0] == "Z" else f"{command[0]} " + " ".join(_fmt(value) for value in command[1:]) for command in contour)


def _fmt(value: float) -> str:
    return f"{value:.4f}".rstrip("0").rstrip(".")


def with_controls(project: dict[str, Any], *, weight: float | None = None, counter: float | None = None, construction: str | None = None) -> dict[str, Any]:
    copy = deepcopy(project)
    if weight is not None:
        copy["axes"]["weight"] = weight
    if counter is not None:
        copy["localOverrides"]["O"]["counter"] = counter
    if construction is not None:
        copy["switches"]["aConstruction"] = construction
    validate_project(copy)
    return copy
