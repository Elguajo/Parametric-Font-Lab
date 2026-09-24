from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen

from fontlab.identity import build_id, engine_hash, verified_manifest
from fontlab.inter_source import SOURCE, SOURCE_SHA256, load_project
from fontlab.recipes import source_hash


class InterSourceTests(unittest.TestCase):
    def setUp(self):
        self.project = load_project(Path('fontlab/project.json'))

    def test_pinned_source_and_native_axes(self):
        self.assertEqual(sha256(SOURCE.read_bytes()).hexdigest(), SOURCE_SHA256)
        font = TTFont(SOURCE)
        self.assertEqual({axis.axisTag: (axis.minValue, axis.maxValue) for axis in font['fvar'].axes}, {'opsz': (14, 32), 'wght': (100, 900)})
        cmap = font.getBestCmap()
        for char in 'ДЛbьbone doneнос сон дно поле делоЁё':
            self.assertIn(ord(char), cmap)

    def test_browser_font_has_same_control_outlines_as_source(self):
        source = TTFont(SOURCE)
        preview = TTFont('web/fonts/PFLSansVariable.woff2')
        self.assertEqual(source.getBestCmap(), preview.getBestCmap())
        self.assertEqual([(axis.axisTag, axis.minValue, axis.maxValue) for axis in source['fvar'].axes],
                         [(axis.axisTag, axis.minValue, axis.maxValue) for axis in preview['fvar'].axes])
        for char in 'ДЛbьАВео':
            glyph = source.getBestCmap()[ord(char)]
            source_pen, preview_pen = RecordingPen(), RecordingPen()
            source.getGlyphSet()[glyph].draw(source_pen)
            preview.getGlyphSet()[glyph].draw(preview_pen)
            self.assertEqual(source_pen.value, preview_pen.value, glyph)

    def test_v3_does_not_reinterpret_v2_controls(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'project.json'
            project = deepcopy(self.project)
            project['axes']['width'] = 1.1
            path.write_text(json.dumps(project), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'only weight and opticalSize'):
                load_project(path)
            project = deepcopy(self.project)
            project['axes']['weight'] = 901
            path.write_text(json.dumps(project), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'between 100 and 900'):
                load_project(path)

    def test_engine_identity_changes_when_source_changes(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'source.ttf').write_bytes(b'first font')
            first = engine_hash(root, ('source.ttf',))
            project_hash = source_hash(self.project)
            old_build = build_id(project_hash, first)
            instance = root / old_build
            (instance / 'fonts').mkdir(parents=True)
            (instance / 'proof.html').write_text('proof', encoding='utf-8')
            binary = instance / 'fonts' / 'font.woff2'
            binary.write_bytes(b'old compiled font')
            manifest = {'project': self.project['id'], 'sourceHash': project_hash, 'engineHash': first, 'buildId': old_build,
                        'fonts': ['fonts/font.woff2'], 'binaryHashes': {'fonts/font.woff2': sha256(binary.read_bytes()).hexdigest()},
                        'proof': 'proof.html', 'proofHash': sha256(b'proof').hexdigest()}
            (instance / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
            self.assertEqual(verified_manifest(self.project, root, first)[0], instance)
            (root / 'source.ttf').write_bytes(b'changed font')
            second = engine_hash(root, ('source.ttf',))
            self.assertNotEqual(first, second)
            with self.assertRaisesRegex(ValueError, 'missing or stale'):
                verified_manifest(self.project, root, second)


if __name__ == '__main__':
    unittest.main()
