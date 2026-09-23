"""Deterministic, original outline recipes for the Phase 1a slice.

Coordinates are font units.  A contour is a closed sequence of move/line/cubic commands;
the evaluator deliberately has no dependency on a font editor or a third-party font source.
"""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
import math
from pathlib import Path
import re
from typing import Any

from fontTools.misc.bezierTools import curveCurveIntersections, curveLineIntersections, splitCubicAtT
from fontTools.pens.areaPen import AreaPen


ROOT = Path(__file__).resolve().parent
PROJECT_PATH = ROOT / "project.json"
SCHEMA_PATH = ROOT / "project.schema.json"
MAX_SOURCE_BYTES = 65536
KAPPA = 0.5522847498307936
WEIGHT_RANGE = (40.0, 160.0)
COUNTER_RANGE = (0.5, 1.5)
VALID_A_CONSTRUCTIONS = {"single", "double"}
GLYPH_DEFINITIONS = [
    {"id": "latin-H", "name": "H", "recipe": "cap-h", "script": "Latn", "unicode": 72},
    {"id": "latin-O", "name": "O", "recipe": "cap-o", "script": "Latn", "unicode": 79},
    {"id": "latin-a", "name": "a", "recipe": "latin-a", "script": "Latn", "unicode": 97},
    {"id": "latin-zero", "name": "zero", "recipe": "zero", "script": "Latn", "unicode": 48},
    {"id": "cyrillic-en", "name": "uni041D", "recipe": "cap-h", "script": "Cyrl", "unicode": 1053},
    {"id": "cyrillic-o", "name": "uni041E", "recipe": "cap-o", "script": "Cyrl", "unicode": 1054},
    {"id": "cyrillic-a", "name": "uni0430", "recipe": "cyrillic-a", "script": "Cyrl", "unicode": 1072},
    {"id": "cyrillic-small-o", "name": "uni043E", "recipe": "small-o", "script": "Cyrl", "unicode": 1086},
]


class ProjectValidationError(ValueError):
    """A project document is outside the intentionally small Phase 1a contract."""


def load_project(path: Path | None = None) -> dict[str, Any]:
    with (path or PROJECT_PATH).open("rb") as source:
        raw = source.read(MAX_SOURCE_BYTES + 1)
    if len(raw) > MAX_SOURCE_BYTES:
        raise ProjectValidationError(f"project exceeds {MAX_SOURCE_BYTES} bytes")
    try:
        project = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ProjectValidationError(f"malformed UTF-8 JSON: {error}") from error
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
    if type(project.get("schemaVersion")) is not int or project["schemaVersion"] != 1:
        raise ProjectValidationError("unsupported schemaVersion")
    if not isinstance(project["id"], str) or re.fullmatch(r"[a-z0-9-]{1,80}", project["id"]) is None:
        raise ProjectValidationError("project id must be 1..80 lowercase letters, digits or hyphens")
    if not isinstance(project["name"], str) or not 1 <= len(project["name"]) <= 100:
        raise ProjectValidationError("project name must be 1..100 characters")
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
    if not isinstance(switches["aConstruction"], str) or switches["aConstruction"] not in VALID_A_CONSTRUCTIONS:
        raise ProjectValidationError("aConstruction must be single or double")
    glyphs = project["glyphs"]
    if glyphs != GLYPH_DEFINITIONS:
        raise ProjectValidationError("glyph IDs, names, Unicode, scripts and recipes must match the Phase 1a repertoire")


def _only_keys(value: Any, expected: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != expected:
        raise ProjectValidationError(f"{label} fields must be exactly {sorted(expected)}")


def _range(value: Any, limits: tuple[float, float], label: str) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not limits[0] <= value <= limits[1] or not math.isfinite(value):
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
        pen = AreaPen()
        segments = []
        start = endpoints[0]
        previous = start
        pen.moveTo(start)
        for command in contour[1:]:
            operation = command[0]
            if operation == "L" and len(command) == 3:
                end = (command[1], command[2])
                pen.lineTo(end)
                segments.append((previous, end))
                previous = end
            elif operation == "C" and len(command) == 7:
                controls = ((command[1], command[2]), (command[3], command[4]))
                end = (command[5], command[6])
                pen.curveTo(*controls, end)
                segments.append((previous, *controls, end))
                previous = end
            elif operation == "Z" and command == ("Z",):
                pen.closePath()
                if previous != start:
                    segments.append((previous, start))
            else:
                raise ProjectValidationError(f"{glyph['name']}: invalid contour command")
        if not math.isfinite(pen.value) or abs(pen.value) < 1e-6:
            raise ProjectValidationError(f"{glyph['name']}: contour has zero area")
        for index, segment in enumerate(segments):
            if segment[0] == segment[-1] and len(segment) == 2:
                raise ProjectValidationError(f"{glyph['name']}: zero-length segment")
            if len(segment) == 4:
                halves = splitCubicAtT(*segment, 0.5)
                # fontTools may report the shared midpoint with ~1e-4 parameter drift.
                if any(hit.t1 < 1 - 1e-3 and hit.t2 > 1e-3 for hit in curveCurveIntersections(*halves)):
                    raise ProjectValidationError(f"{glyph['name']}: self-intersecting cubic")
            for other_index in range(index + 2, len(segments)):
                if index == 0 and other_index == len(segments) - 1:
                    continue  # The first and closing segments meet at the start point.
                if _segments_intersect(segment, segments[other_index]):
                    raise ProjectValidationError(f"{glyph['name']}: self-intersecting contour")


def _segments_intersect(first: tuple, second: tuple) -> bool:
    if len(first) == 4 and len(second) == 4:
        return bool(curveCurveIntersections(first, second))
    if len(first) == 4:
        return bool(curveLineIntersections(first, second))
    if len(second) == 4:
        return bool(curveLineIntersections(second, first))
    a, b = first
    c, d = second

    def cross(p: tuple, q: tuple, r: tuple) -> float:
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

    def on_segment(p: tuple, q: tuple, r: tuple) -> bool:
        return min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1])

    turns = (cross(a, b, c), cross(a, b, d), cross(c, d, a), cross(c, d, b))
    if turns[0] * turns[1] < 0 and turns[2] * turns[3] < 0:
        return True
    return any(abs(turn) < 1e-8 and on_segment(*points) for turn, points in zip(turns, ((a, c, b), (a, d, b), (c, a, d), (c, b, d))))


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
