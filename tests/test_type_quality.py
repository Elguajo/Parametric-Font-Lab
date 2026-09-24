from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fontlab import recipes_v1
from fontlab.identity import build_id, engine_hash, verified_manifest
from fontlab.recipes import evaluate_project, glyph_signature, load_project, source_hash, with_controls


CORPUS = 'HOAVCSnobdeНОСДЛЖКЯинопбдлеь'


class TypeQualityTests(unittest.TestCase):
    def setUp(self):
        self.project = load_project(Path('fontlab/project-v2.json'))

    def test_v1_projects_keep_their_original_evaluation(self):
        old = load_project(Path('fontlab/project-v1.json'))
        self.assertEqual(evaluate_project(old), recipes_v1.evaluate_project(old))
        self.assertEqual(old['engine']['version'], '1.0')
        self.assertEqual(self.project['engine']['version'], '2.0')

    def test_control_forms_and_bearings_at_endpoints(self):
        cases = [self.project, with_controls(self.project, active_preset='display', **{
            'weight': 124, 'width': 1.08, 'x_height': 520, 'roundness': .9, 'aperture': .72,
            'construction': 'single', 'zero_style': 'slashed',
        })]
        for axis, low, high in [('weight', 40, 160), ('width', .85, 1.15),
                                ('x_height', 460, 540), ('roundness', 0, 1), ('aperture', 0, 1)]:
            cases.extend([with_controls(self.project, **{axis: value}) for value in (low, high)])
        for project in cases:
            with self.subTest(axes=project['axes']):
                glyphs = {chr(glyph['unicode']): glyph for glyph in evaluate_project(project)['glyphs']}
                for character in CORPUS:
                    glyph = glyphs[character]
                    bounds = glyph_signature(glyph)['bounds']
                    left, right = bounds[0], glyph['advance'] - bounds[2]
                    self.assertGreater(left, 20, character)
                    self.assertGreater(right, 20, character)
                    self.assertLess(left, 130, character)
                    self.assertLess(right, 130, character)
                self.assertNotEqual(glyphs['Д']['contours'], glyphs['Л']['contours'])
                self.assertNotEqual(glyphs['b']['contours'], glyphs['ь']['contours'])
                self.assertGreater(glyph_signature(glyphs['b'])['bounds'][3], 690)
                self.assertLess(glyph_signature(glyphs['ь'])['bounds'][3], 560)
                for character in 'Oobdоь':
                    outer, inner = glyphs[character]['contours'][:2] if character not in 'bь' else glyphs[character]['contours'][1:3]
                    outer_bounds = glyph_signature({**glyphs[character], 'contours': [outer]})['bounds']
                    inner_bounds = glyph_signature({**glyphs[character], 'contours': [inner]})['bounds']
                    self.assertGreater(inner_bounds[2] - inner_bounds[0], 60, character)
                    self.assertGreater(inner_bounds[3] - inner_bounds[1], 60, character)
                    self.assertGreater(outer_bounds[2] - outer_bounds[0], inner_bounds[2] - inner_bounds[0])

    def test_engine_change_invalidates_same_json_manifest(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'recipe.py').write_text('old recipe', encoding='utf-8')
            old_revision = engine_hash(root, ('recipe.py',))
            project_hash = source_hash(self.project)
            old_id = build_id(project_hash, old_revision)
            instance = root / old_id
            (instance / 'fonts').mkdir(parents=True)
            (instance / 'proof.html').write_text('proof', encoding='utf-8')
            binary = instance / 'fonts/font.woff2'
            binary.write_bytes(b'compiled old font')
            manifest = {'project': self.project['id'], 'sourceHash': project_hash,
                        'engineHash': old_revision, 'buildId': old_id,
                        'fonts': ['fonts/font.woff2'], 'binaryHashes': {'fonts/font.woff2': sha256(binary.read_bytes()).hexdigest()},
                        'proof': 'proof.html', 'proofHash': sha256(b'proof').hexdigest()}
            (instance / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            self.assertEqual(verified_manifest(self.project, root, old_revision)[0], instance)
            (root / 'recipe.py').write_text('new recipe', encoding='utf-8')
            new_revision = engine_hash(root, ('recipe.py',))
            self.assertNotEqual(old_id, build_id(project_hash, new_revision))
            with self.assertRaisesRegex(ValueError, 'missing or stale'):
                verified_manifest(self.project, root, new_revision)
            binary.write_bytes(b'tampered font')
            with self.assertRaisesRegex(ValueError, 'missing or changed'):
                verified_manifest(self.project, root, old_revision)


if __name__ == '__main__':
    unittest.main()
