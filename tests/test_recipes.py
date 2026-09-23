from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from fontlab.recipes import GLYPH_DEFINITIONS, ProjectValidationError, evaluate_project, kerning_value, load_project, source_hash, validate_glyph, with_controls


class Phase1bRecipeTests(unittest.TestCase):
    def setUp(self): self.project = load_project()

    def test_repertoire_has_full_basic_latin_russian_and_marks(self):
        cmap = {glyph["unicode"] for glyph in GLYPH_DEFINITIONS}
        self.assertTrue(set(range(0x20, 0x7F)).issubset(cmap))
        self.assertIn(0xA0, cmap)
        self.assertTrue(set(range(0x410, 0x430)).issubset(cmap))
        self.assertTrue(set(range(0x430, 0x450)).issubset(cmap))
        self.assertTrue({0x401, 0x451, 0x301, 0x308}.issubset(cmap))

    def test_all_recipes_are_closed_at_safe_axis_corners(self):
        for weight in (40, 160):
            for width in (.85, 1.15):
                with self.subTest(weight=weight, width=width):
                    glyphs = evaluate_project(with_controls(self.project, weight=weight, width=width))["glyphs"]
                    self.assertEqual(len(glyphs), 164)
                    self.assertTrue(all(glyph["advance"] >= 0 for glyph in glyphs))
                    self.assertTrue(all(contour[0][0] == "M" and contour[-1] == ("Z",) for glyph in glyphs for contour in glyph["contours"]))

    def test_control_scopes_and_structural_switches(self):
        base = evaluate_project(self.project)["glyphs"]
        changed = evaluate_project(with_controls(self.project, counter=.6))["glyphs"]
        names = [before["name"] for before, after in zip(base, changed) if before["contours"] != after["contours"]]
        self.assertEqual(names, ["O"])
        single = evaluate_project(with_controls(self.project, construction="single"))["glyphs"]
        self.assertNotEqual(next(g for g in base if g["name"] == "a")["contours"], next(g for g in single if g["name"] == "a")["contours"])
        slashed = evaluate_project(with_controls(self.project, zero_style="slashed"))["glyphs"]
        self.assertNotEqual(next(g for g in base if g["name"] == "zero")["contours"], next(g for g in slashed if g["name"] == "zero")["contours"])
        open_forms = evaluate_project(with_controls(self.project, aperture=.1))["glyphs"]
        self.assertNotEqual(next(g for g in base if g["name"] == "C")["contours"], next(g for g in open_forms if g["name"] == "C")["contours"])

    def test_metrics_anchors_and_script_kerning(self):
        glyphs = {glyph["name"]: glyph for glyph in evaluate_project(self.project)["glyphs"]}
        self.assertEqual(glyphs["acutecomb"]["advance"], 0)
        self.assertIn("top", glyphs["uni0401"]["anchors"])
        self.assertLess(kerning_value("A", "O"), 0)
        self.assertLess(kerning_value("uni0414", "uni041e"), 0)
        self.assertLess(kerning_value("T", "o"), 0)
        self.assertLess(kerning_value("uni0422", "uni043e"), 0)

    def test_round_trip_and_rejects_invalid_source(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "project.json"
            path.write_text(json.dumps(self.project, ensure_ascii=False, sort_keys=True), encoding="utf-8")
            self.assertEqual(source_hash(self.project), source_hash(load_project(path)))
        invalid = deepcopy(self.project); invalid["axes"]["width"] = 2
        with self.assertRaises(ProjectValidationError): evaluate_project(invalid)
        invalid = deepcopy(self.project); invalid["glyphs"] = {"repertoire": "anything"}
        with self.assertRaises(ProjectValidationError): evaluate_project(invalid)
        with self.assertRaises(ProjectValidationError):
            validate_glyph({"name": "probe", "advance": 500, "metricsClass": "latin", "contours": [[("M", 0, 0), ("L", 100, 100), ("L", 0, 100), ("L", 100, 0), ("Z",)]]})


if __name__ == "__main__": unittest.main()
