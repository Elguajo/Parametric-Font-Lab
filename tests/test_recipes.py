from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from fontlab.recipes import (
    GLYPH_DEFINITIONS,
    SCHEMA_PATH,
    ProjectValidationError,
    evaluate_project,
    load_project,
    parity_signature,
    source_hash,
    validate_glyph,
    with_controls,
)


class RecipeTests(unittest.TestCase):
    def setUp(self):
        self.project = load_project()

    def test_json_serialization_is_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "project.json"
            path.write_text(json.dumps(self.project, ensure_ascii=False, sort_keys=True), encoding="utf-8")
            self.assertEqual(source_hash(self.project), source_hash(load_project(path)))

    def test_schema_repertoire_matches_runtime_contract(self):
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["glyphs"]["const"], GLYPH_DEFINITIONS)

    def test_all_original_phase_1a_glyphs_have_closed_contours(self):
        rendered = evaluate_project(self.project)["glyphs"]
        self.assertEqual([glyph["name"] for glyph in rendered], ["H", "O", "a", "zero", "uni041D", "uni041E", "uni0430", "uni043E"])
        for glyph in rendered:
            self.assertGreater(glyph["advance"], 0)
            self.assertTrue(all(contour[0][0] == "M" and contour[-1] == ("Z",) for contour in glyph["contours"]))

    def test_weight_is_shared_by_all_recipes(self):
        lighter = parity_signature(with_controls(self.project, weight=50))
        heavier = parity_signature(with_controls(self.project, weight=140))
        for before, after in zip(lighter, heavier):
            with self.subTest(glyph=before["name"]):
                self.assertNotEqual(before["outline"], after["outline"])

    def test_local_counter_override_changes_only_latin_o(self):
        normal = parity_signature(self.project)
        changed = parity_signature(with_controls(self.project, counter=0.6))
        changed_names = [before["name"] for before, after in zip(normal, changed) if before != after]
        self.assertEqual(changed_names, ["O"])

    def test_a_switch_is_discrete_and_latin_scoped(self):
        single = parity_signature(with_controls(self.project, construction="single"))
        double = parity_signature(with_controls(self.project, construction="double"))
        changed = [before["name"] for before, after in zip(single, double) if before != after]
        self.assertEqual(changed, ["a"])
        self.assertNotEqual(single[2]["contours"], double[2]["contours"])

    def test_rejects_invalid_control_and_unknown_fields(self):
        invalid = deepcopy(self.project)
        invalid["axes"]["weight"] = 200
        with self.assertRaises(ProjectValidationError):
            evaluate_project(invalid)
        invalid = deepcopy(self.project)
        invalid["axes"]["weight"] = 10 ** 1000
        with self.assertRaises(ProjectValidationError):
            evaluate_project(invalid)
        invalid = deepcopy(self.project)
        invalid["unexpected"] = True
        with self.assertRaises(ProjectValidationError):
            evaluate_project(invalid)

    def test_rejects_wrong_glyph_identity_and_mapping(self):
        changes = [
            (4, "unicode", 0x041F),
            (0, "recipe", "zero"),
            (1, "id", "latin-H"),
            (1, "id", ""),
            (1, "script", "Cyrl"),
        ]
        for index, field, value in changes:
            with self.subTest(field=field, value=value):
                invalid = deepcopy(self.project)
                invalid["glyphs"][index][field] = value
                with self.assertRaises(ProjectValidationError):
                    evaluate_project(invalid)

    def test_rejects_invalid_source_types_and_oversized_file(self):
        invalid = deepcopy(self.project)
        invalid["schemaVersion"] = True
        with self.assertRaises(ProjectValidationError):
            evaluate_project(invalid)
        invalid = deepcopy(self.project)
        invalid["switches"]["aConstruction"] = []
        with self.assertRaises(ProjectValidationError):
            evaluate_project(invalid)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.json"
            path.write_text(" " * 65537, encoding="utf-8")
            with self.assertRaises(ProjectValidationError):
                load_project(path)

    def test_rejects_self_intersection(self):
        bowtie = {"name": "probe", "advance": 500, "contours": [
            [("M", 0, 0), ("L", 100, 100), ("L", 0, 100), ("L", 100, 0), ("Z",)]
        ]}
        with self.assertRaises(ProjectValidationError):
            validate_glyph(bowtie)
        curved = {"name": "probe", "advance": 500, "contours": [
            [("M", 0, 0), ("C", 100, 0, 100, 100, 0, 100), ("L", 100, 50), ("L", 0, 50), ("Z",)]
        ]}
        with self.assertRaises(ProjectValidationError):
            validate_glyph(curved)

    def test_all_authored_contours_are_valid_at_axis_bounds(self):
        for weight in (40, 88, 160):
            for construction in ("single", "double"):
                with self.subTest(weight=weight, construction=construction):
                    self.assertEqual(len(evaluate_project(with_controls(self.project, weight=weight, construction=construction))["glyphs"]), 8)


if __name__ == "__main__":
    unittest.main()
