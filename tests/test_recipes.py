from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from fontlab.recipes import (
    PROJECT_PATH,
    ProjectValidationError,
    evaluate_project,
    load_project,
    parity_signature,
    source_hash,
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

    def test_all_original_phase_1a_glyphs_have_closed_contours(self):
        rendered = evaluate_project(self.project)["glyphs"]
        self.assertEqual([glyph["name"] for glyph in rendered], ["H", "O", "a", "zero", "uni041D", "uni041E", "uni0430", "uni043E"])
        for glyph in rendered:
            self.assertGreater(glyph["advance"], 0)
            self.assertTrue(all(contour[0][0] == "M" and contour[-1] == ("Z",) for contour in glyph["contours"]))

    def test_weight_is_shared_by_all_recipes(self):
        lighter = parity_signature(with_controls(self.project, weight=50))
        heavier = parity_signature(with_controls(self.project, weight=140))
        self.assertNotEqual(lighter, heavier)

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
        invalid["unexpected"] = True
        with self.assertRaises(ProjectValidationError):
            evaluate_project(invalid)


if __name__ == "__main__":
    unittest.main()
