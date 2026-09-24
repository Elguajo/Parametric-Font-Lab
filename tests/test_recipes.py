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
        self.assertLess(kerning_value("uni0414", "uni041E"), 0)
        self.assertLess(kerning_value("T", "o"), 0)
        self.assertLess(kerning_value("uni0422", "uni043E"), 0)

    def test_native_proof_recipes_have_distinct_forms_and_expected_width(self):
        glyphs = {glyph["name"]: glyph for glyph in evaluate_project(self.project)["glyphs"]}
        self.assertEqual(glyphs["uni041B"]["advance"], 680)
        self.assertEqual(glyphs["e"]["contours"], glyphs["uni0435"]["contours"])
        for name, generic in (("A", "H"), ("uni0410", "uni041D"), ("K", "H"), ("uni041A", "uni041D"), ("uni0416", "uni041D"), ("uni0431", "uni0430"), ("uni0434", "uni0430"), ("uni043B", "uni0430"), ("uni0442", "uni0430"), ("uni0444", "uni0430"), ("uni0435", "uni0430"), ("uni0451", "uni0430")):
            with self.subTest(name=name):
                self.assertNotEqual(glyphs[name]["contours"], glyphs[generic]["contours"])

    def test_full_repertoire_has_no_generic_fallback_forms(self):
        glyphs = {glyph["name"]: glyph for glyph in evaluate_project(self.project)["glyphs"]}
        reviewed = {
            "uni0021": "uni0026", "uni003F": "uni0026", "uni0040": "uni0026",
            "one": "zero", "two": "three", "eight": "zero", "J": "I", "S": "Z",
            "U": "H", "uni0411": "uni0412", "uni0417": "uni0412", "uni0419": "uni0418",
            "uni0426": "uni0428", "uni042A": "uni042C", "a": "o", "g": "q",
            "uni0432": "uni0431", "uni0437": "uni0442", "uni0439": "uni0438",
            "uni0446": "uni0448", "uni044A": "uni044C",
        }
        names = {glyph["name"] for glyph in glyphs.values()}
        self.assertEqual(len(names), 164)
        for name, unlike in reviewed.items():
            with self.subTest(name=name):
                self.assertIn(name, glyphs)
                self.assertIn(unlike, glyphs)
                self.assertNotEqual(glyphs[name]["contours"], glyphs[unlike]["contours"])
        self.assertEqual(glyphs["acutecomb"]["anchors"]["_top"], (260, 760))
        self.assertEqual(glyphs["dieresiscomb"]["anchors"]["_top"], (260, 760))
        self.assertEqual(glyphs["J"]["advance"], 540)
        self.assertEqual(glyphs["j"]["advance"], 330)
        self.assertEqual(glyphs["r"]["advance"], 420)
        for name, unlike in (("V", "X"), ("Y", "X"), ("W", "uni0428"), ("uni0417", "S"), ("uni0437", "s")):
            self.assertNotEqual(glyphs[name]["contours"], glyphs[unlike]["contours"])

    def test_marks_scale_with_width_and_reverse_rounds_join(self):
        for width in (.85, 1.15):
            glyphs = {glyph["name"]: glyph for glyph in evaluate_project(with_controls(self.project, width=width))["glyphs"]}
            self.assertEqual(glyphs["acutecomb"]["anchors"]["_top"], (260 * width, 760))
            self.assertEqual(glyphs["dieresiscomb"]["anchors"]["_top"], (260 * width, 760))
        for aperture in (0, 1):
            glyphs = {glyph["name"]: glyph for glyph in evaluate_project(with_controls(self.project, aperture=aperture))["glyphs"]}
            for name in ("uni042D", "uni044D"):
                top_bar = glyphs[name]["contours"][1]
                self.assertEqual(max(point[-2] for point in top_bar if point[0] != "Z"), glyphs[name]["advance"] - 80)

    def test_precomposed_and_combining_dieresis_share_attachment_height(self):
        glyphs = {glyph["name"]: glyph for glyph in evaluate_project(self.project)["glyphs"]}
        mark_center = glyphs["dieresiscomb"]["contours"][0][0][-1]
        mark_anchor = glyphs["dieresiscomb"]["anchors"]["_top"]
        for base, precomposed, dot_contour in (("uni0415", "uni0401", 4), ("uni0435", "uni0451", 3)):
            expected_center = glyphs[base]["anchors"]["top"][1] + mark_center - mark_anchor[1]
            self.assertEqual(glyphs[precomposed]["contours"][dot_contour][0][-1], expected_center)

    def test_reviewed_kerning_exceptions_precede_class_pairs(self):
        self.assertEqual(kerning_value("A", "V"), -60)
        self.assertEqual(kerning_value("V", "A"), -60)
        self.assertEqual(kerning_value("T", "O"), -58)
        self.assertEqual(kerning_value("T", "a"), -42)
        self.assertEqual(kerning_value("uni0422", "uni0410"), -54)
        self.assertEqual(kerning_value("uni0422", "uni0430"), -48)

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
