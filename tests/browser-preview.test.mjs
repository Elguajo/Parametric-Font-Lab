import { execFileSync, spawn } from 'node:child_process';
import { resolve } from 'node:path';
import { chromium } from 'playwright';

const python = process.env.PYTHON || resolve('.venv/bin/python');
const server = spawn(python, ['-m', 'http.server', '8765', '--bind', '127.0.0.1'], { cwd: 'web', stdio: 'ignore' });
let browser;
try {
  const expected = JSON.parse(execFileSync(python, ['-c', "import json; from fontlab.recipes import load_project, parity_signature; print(json.dumps(parity_signature(load_project()), ensure_ascii=False))"], { encoding: 'utf8' }));
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 850 } });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('http://127.0.0.1:8765', { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.pfl?.signature);
  const actual = await page.evaluate(() => window.pfl.signature());
  if (JSON.stringify(actual) !== JSON.stringify(expected)) throw new Error('browser evaluator differs from Python evaluator');
  if (await page.locator('.glyph-button').count() !== 8) throw new Error('glyph chart does not contain the Phase 1a repertoire');
  await page.locator('#specimen').fill('Н О а о H O a 0');
  if (await page.locator('#specimen-preview svg').count() !== 8) throw new Error('specimen did not map all Latin/Cyrillic glyphs');
  const beforeO = await page.evaluate(() => window.pfl.signature());
  await page.locator('#counter').evaluate(element => { element.value = '0.60'; element.dispatchEvent(new Event('input', { bubbles: true })); });
  const afterO = await page.evaluate(() => window.pfl.signature());
  const counterChanges = beforeO.filter((item, index) => JSON.stringify(item) !== JSON.stringify(afterO[index])).map(item => item.name);
  if (JSON.stringify(counterChanges) !== JSON.stringify(['O'])) throw new Error(`local O scope failed: ${counterChanges}`);
  await page.locator('#construction').selectOption('single');
  const single = await page.evaluate(() => window.pfl.signature());
  const switchChanges = afterO.filter((item, index) => JSON.stringify(item) !== JSON.stringify(single[index])).map(item => item.name);
  if (JSON.stringify(switchChanges) !== JSON.stringify(['a'])) throw new Error(`a switch scope failed: ${switchChanges}`);
  if (errors.length) throw new Error(`browser errors: ${errors.join('; ')}`);
  await page.screenshot({ path: 'build/browser-preview-proof.png', fullPage: true });
  console.log('browser preview, Latin/Cyrillic mapping, evaluator parity, and local/discrete controls verified');
} finally {
  await browser?.close();
  server.kill();
}
