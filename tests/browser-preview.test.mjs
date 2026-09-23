import { execFileSync, spawn } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { chromium } from 'playwright';

const python = process.env.PYTHON || resolve('.venv/bin/python');
const scratch = mkdtempSync(join(tmpdir(), 'pfl-phase1a-'));
const server = spawn(python, ['-m', 'http.server', '8765', '--bind', '127.0.0.1'], { cwd: resolve('.'), stdio: 'ignore' });
let browser;

function pythonSignature(weight, counter, construction) {
  const program = 'import json,sys; from fontlab.recipes import load_project,parity_signature,with_controls; p=with_controls(load_project(),weight=float(sys.argv[1]),counter=float(sys.argv[2]),construction=sys.argv[3]); print(json.dumps(parity_signature(p),ensure_ascii=False))';
  return JSON.parse(execFileSync(python, ['-c', program, String(weight), String(counter), construction], { encoding: 'utf8' }));
}

try {
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 850 }, acceptDownloads: true });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('http://127.0.0.1:8765/web/', { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.pfl?.signature);
  const actual = await page.evaluate(() => window.pfl.signature());
  if (JSON.stringify(actual) !== JSON.stringify(pythonSignature(88, 1, 'double'))) throw new Error('default browser evaluator differs from Python');
  if (await page.locator('.glyph-button').count() !== 8) throw new Error('glyph chart is incomplete');

  await page.locator('#specimen').fill('Н О а о H O a 0');
  const specimenIds = await page.locator('#specimen-preview svg').evaluateAll(elements => elements.map(element => element.dataset.glyphId));
  const expectedIds = ['cyrillic-en', 'cyrillic-o', 'cyrillic-a', 'cyrillic-small-o', 'latin-H', 'latin-O', 'latin-a', 'latin-zero'];
  if (JSON.stringify(specimenIds) !== JSON.stringify(expectedIds)) throw new Error(`wrong specimen glyph IDs: ${specimenIds}`);

  await page.locator('[data-glyph="O"]').click();
  const centerHit = await page.evaluate(() => {
    const group = document.querySelector('#outline g');
    const point = new DOMPoint(340, 350).matrixTransform(group.getScreenCTM());
    return document.elementFromPoint(point.x, point.y)?.tagName.toLowerCase();
  });
  if (centerHit === 'path') throw new Error('Latin O counter is filled in the SVG preview');

  await page.locator('#weight-number').fill('200');
  if (!await page.locator('#download-project').isDisabled()) throw new Error('invalid numeric weight is exportable');
  await page.locator('#weight-number').fill('120');
  await page.locator('#counter-number').fill('0.63');
  if (await page.locator('#counter').inputValue() !== '0.63') throw new Error('numeric counter did not sync the slider');
  await page.locator('#counter-number').fill('0.6');
  await page.locator('#construction').selectOption('single');
  const customized = await page.evaluate(() => window.pfl.signature());
  if (JSON.stringify(customized) !== JSON.stringify(pythonSignature(120, 0.6, 'single'))) throw new Error('custom browser evaluator differs from Python');
  if (await page.locator('#weight').inputValue() !== '120') throw new Error('numeric control did not sync the slider');

  const downloadPromise = page.waitForEvent('download');
  await page.locator('#download-project').click();
  const download = await downloadPromise;
  const projectPath = join(scratch, 'project.json');
  await download.saveAs(projectPath);
  const project = JSON.parse(readFileSync(projectPath, 'utf8'));
  if (project.axes.weight !== 120 || project.localOverrides.O.counter !== 0.6 || project.switches.aConstruction !== 'single') {
    throw new Error('downloaded project does not contain the preview controls');
  }

  const outputDir = join(scratch, 'build');
  mkdirSync(outputDir);
  writeFileSync(join(outputDir, 'keep.txt'), 'unrelated generated work');
  const manifest = JSON.parse(execFileSync(python, ['tools/build_font.py', '--project', projectPath, '--output-dir', outputDir], { encoding: 'utf8' }));
  const instance = join(outputDir, manifest.sourceHash);
  if (manifest.fonts.length !== 3 || !manifest.fonts.every(path => existsSync(join(instance, path)))) throw new Error('static output set is incomplete');
  if (!existsSync(join(outputDir, 'keep.txt'))) throw new Error('compiler deleted unrelated build output');
  const checkBinary = `
import json,sys
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.pointInsidePen import PointInsidePen
from ufoLib2 import Font
root=Path(sys.argv[1]); manifest=json.loads((root/'manifest.json').read_text())
assert len(Font.open(root/manifest['ufo'])['a'].contours)==4
for relative in manifest['fonts']:
    font=TTFont(root/relative)
    assert font['name'].getDebugName(6)==manifest['instanceName']
    assert font['OS/2'].usWeightClass==633
    glyphset=font.getGlyphSet()
    for point, expected in [((340,340), False), ((180,340), True)]:
        pen=PointInsidePen(glyphset, point); glyphset['O'].draw(pen)
        assert pen.getResult()==expected, (relative, point)
`;
  execFileSync(python, ['-c', checkBinary, instance]);
  if (errors.length) throw new Error(`browser errors: ${errors.join('; ')}`);

  mkdirSync('test-results', { recursive: true });
  await page.screenshot({ path: 'test-results/browser-preview-proof.png', fullPage: true });
  await page.locator('#specimen').fill('Ж');
  const unsupportedMessage = await page.locator('#preview-error').textContent();
  if (!unsupportedMessage.includes('Ж')) throw new Error('unsupported specimen characters are hidden without feedback');
  await page.setViewportSize({ width: 375, height: 800 });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
  if (overflow) throw new Error('mobile viewport has horizontal overflow');
  console.log('browser counters, glyph IDs, numeric controls, custom-project round-trip and static export verified');
} finally {
  await browser?.close();
  server.kill();
  rmSync(scratch, { recursive: true, force: true });
}
