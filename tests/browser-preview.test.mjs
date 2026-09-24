import { execFileSync, spawn } from 'node:child_process';
import { chromium } from 'playwright';
import { resolve } from 'node:path';

const python = process.env.PYTHON || resolve('.venv/bin/python');
const server = spawn(python, ['-m', 'http.server', '8765', '--bind', '127.0.0.1'], { cwd: resolve('.'), stdio: 'ignore' });
let browser;
try {
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 850 }, acceptDownloads: true });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('http://127.0.0.1:8765/web/', { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.pfl?.glyphs?.length === 164);
  if (await page.locator('.glyph-button').count() !== 164) throw new Error('full Phase 1b chart is incomplete');
  if (await page.locator('.glyph-button svg.chart-glyph').count() !== 164 || await page.locator('.glyph-button svg.chart-glyph path').count() !== 164) throw new Error('glyph chart does not render every generated outline as SVG');
  if (await page.locator('[data-glyph="A"] svg.chart-glyph path').getAttribute('d') !== await page.locator('#outline path').getAttribute('d')) throw new Error('glyph chart outline differs from the current generated A outline');
  const upright = await page.evaluate(() => {
    const matrix = document.querySelector('#outline g').getScreenCTM();
    const baseline = new DOMPoint(0, 0).matrixTransform(matrix);
    const capHeight = new DOMPoint(0, 700).matrixTransform(matrix);
    return capHeight.y < baseline.y;
  });
  if (!upright) throw new Error('font-space cap height renders below the baseline in the SVG preview');
  if (await page.locator('#weight-number').inputValue() !== '88') throw new Error('initial numeric control is not synchronized with source state');
  const sourceGlyphs = JSON.parse(execFileSync(python, ['-c', "import json; from fontlab.recipes import evaluate_project, load_project; print(json.dumps([{k: g[k] for k in ('name', 'advance', 'contours', 'anchors')} for g in evaluate_project(load_project())['glyphs']]))"], { cwd: resolve('.'), encoding: 'utf8' }));
  const previewGlyphs = await page.evaluate(() => window.pfl.glyphs.map(g => {
    const rendered = window.pfl.evalGlyph(g);
    return { name: rendered.name, advance: rendered.advance, contours: rendered.contours, anchors: rendered.anchors };
  }));
  const paritySignature = glyphs => JSON.stringify(glyphs, (_key, value) => typeof value === 'number' ? Number(value.toFixed(6)) : value);
  if (paritySignature(previewGlyphs) !== paritySignature(sourceGlyphs)) {
    const mismatch = previewGlyphs.findIndex((glyph, index) => paritySignature(glyph) !== paritySignature(sourceGlyphs[index]));
    throw new Error(`browser preview contours, advances, or recipe branches differ from source at ${sourceGlyphs[mismatch]?.name || mismatch}`);
  }
  await page.locator('#weight').evaluate(element => { element.value = '100'; element.dispatchEvent(new Event('input', { bubbles: true })); });
  if (await page.locator('#weight-number').inputValue() !== '100') throw new Error('slider input does not synchronize its numeric companion');
  await page.locator('#weight-number').fill('110');
  if (await page.locator('#weight').inputValue() !== '110') throw new Error('numeric input does not synchronize its slider companion');
  const allBasicLatin = String.fromCodePoint(...Array.from({ length: 95 }, (_, index) => 32 + index));
  await page.locator('#specimen').fill(`${allBasicLatin}\nАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ\nабвгдеёжзийклмнопрстуфхцчшщъыьэюя`);
  if (await page.locator('#preview-error').textContent()) throw new Error('full Latin/Cyrillic proof has unsupported characters');
  await page.locator('#specimen').fill('AVATAR СТРОКА АВНОРСХ ДЛЖКУФЯ бдлтф ёж AА eе 0123456789');
  if (await page.locator('#preview-error').textContent()) throw new Error('covered Latin/Cyrillic proof has unsupported characters');
  for (const size of ['10 px', '14 px', '24 px', '72 px']) {
    await page.getByRole('button', { name: size }).click();
    if (await page.locator('.glyph').count() === 0) throw new Error(`proof did not render at ${size}`);
  }
  const advances = await page.locator('.glyph').evaluateAll(elements => elements.slice(0, 12).map(element => Number.parseFloat(getComputedStyle(element).width)));
  if (!(Math.max(...advances) > Math.min(...advances))) throw new Error('proof normalizes glyph advances instead of showing source spacing');
  await page.locator('#specimen').fill('To То');
  const exceptionKerning = await page.locator('.glyph').evaluateAll(elements => elements.map(element => element.style.marginLeft));
  if (exceptionKerning[1] !== '-3.024px' || exceptionKerning[4] !== '-3.456px') throw new Error(`preview exception kerning differs from source: ${exceptionKerning}`);
  await page.locator('#specimen').fill('AV VA TO Ta ТА Та То');
  const reviewedKerning = await page.locator('.glyph').evaluateAll(elements => elements.map(element => element.style.marginLeft));
  const expectedKerning = new Map([[1, '-4.32px'], [4, '-4.32px'], [7, '-4.176px'], [10, '-3.024px'], [13, '-3.888px'], [16, '-3.456px'], [19, '-3.456px']]);
  for (const [index, value] of expectedKerning) if (reviewedKerning[index] !== value) throw new Error(`preview kerning at glyph ${index} differs from source: ${reviewedKerning}`);
  for (const glyphName of ['B', 'uni0412', 'uni042F']) {
    await page.locator(`[data-glyph="${glyphName}"]`).click();
    const before = await page.locator('#outline path').getAttribute('d');
    await page.locator('#roundness-number').fill('0.2');
    const after = await page.locator('#outline path').getAttribute('d');
    if (before !== after) throw new Error(`${glyphName} preview outline must retain its source-fixed roundness`);
  }
  await page.locator('#preset').selectOption('display');
  if (await page.locator('#zero-style').inputValue() !== 'slashed') throw new Error('display preset did not control the zero switch');
  if (await page.locator('#weight').inputValue() !== '124' || await page.locator('#weight-number').inputValue() !== '124') throw new Error('preset does not synchronize paired weight controls');
  const displayProject = await page.evaluate(() => window.pfl.currentProject());
  const displaySourceGlyphs = JSON.parse(execFileSync(python, ['-c', "import json, sys; from fontlab.recipes import evaluate_project; project=json.load(sys.stdin); print(json.dumps([{k: g[k] for k in ('name', 'advance', 'contours', 'anchors')} for g in evaluate_project(project)['glyphs']]))"], { cwd: resolve('.'), input: JSON.stringify(displayProject), encoding: 'utf8' }));
  const displayPreviewGlyphs = await page.evaluate(() => window.pfl.glyphs.map(g => {
    const rendered = window.pfl.evalGlyph(g);
    return { name: rendered.name, advance: rendered.advance, contours: rendered.contours, anchors: rendered.anchors };
  }));
  if (paritySignature(displayPreviewGlyphs) !== paritySignature(displaySourceGlyphs)) throw new Error('display preset preview differs from source');
  await page.locator('#compare').click();
  await page.locator('#weight-number').fill('110');
  await page.locator('#compare').click();
  if (!(await page.locator('#compare-status').textContent()).includes('differ')) throw new Error('A/B state did not report changed source');
  const downloadPromise = page.waitForEvent('download');
  await page.locator('#download-project').click();
  const download = await downloadPromise;
  if (!download.suggestedFilename().includes('phase-1b')) throw new Error('downloaded project is not versioned as Phase 1b');
  await page.locator('#specimen').fill('Ж');
  if (await page.locator('#preview-error').textContent()) throw new Error('Cyrillic Ж is absent from preview');
  await page.locator('#specimen').fill('А́ ё');
  await page.waitForFunction(() => document.querySelectorAll('#specimen-preview .glyph').length === 5);
  const markAttachments = await page.locator('#specimen-preview .glyph').evaluateAll(elements => [[0, 1], [3, 4]].map(([baseIndex, markIndex]) => {
    const glyphFor = element => window.pfl.evalGlyph(window.pfl.glyphs.find(glyph => glyph.id === element.dataset.glyphId));
    const pointFor = (element, anchor) => new DOMPoint(...anchor).matrixTransform(element.querySelector('g').getScreenCTM());
    const base = glyphFor(elements[baseIndex]);
    const mark = glyphFor(elements[markIndex]);
    const basePoint = pointFor(elements[baseIndex], base.anchors.top);
    const markPoint = pointFor(elements[markIndex], mark.anchors._top);
    return { dx: Math.abs(basePoint.x - markPoint.x), dy: Math.abs(basePoint.y - markPoint.y) };
  }));
  for (const attachment of markAttachments) if (attachment.dx > .1 || attachment.dy > .1) throw new Error(`combining mark does not use both source anchor coordinates: ${JSON.stringify(attachment)}`);
  await page.setViewportSize({ width: 375, height: 800 });
  if (await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)) throw new Error('mobile viewport has horizontal overflow');
  if (errors.length) throw new Error(`browser errors: ${errors.join('; ')}`);
  console.log('full chart, script proof, presets/A-B, controls and download verified');
} finally { await browser?.close(); server.kill(); }
