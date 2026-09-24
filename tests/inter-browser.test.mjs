import { spawn } from 'node:child_process';
import { resolve } from 'node:path';
import { chromium } from 'playwright';

const root = resolve('.');
const python = process.env.PYTHON || resolve('.venv/bin/python');
const server = spawn(python, ['-m', 'http.server', '8775', '--bind', '127.0.0.1'], { cwd: root, stdio: 'ignore' });
let browser;
try {
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 850 }, acceptDownloads: true });
  const responses = [];
  page.on('response', response => { if (response.url().endsWith('PFLSansVariable.woff2')) responses.push(response.status()); });
  await page.goto('http://127.0.0.1:8775/web/', { waitUntil: 'networkidle' });
  await page.waitForFunction(() => document.body.dataset.fontState === 'ready');
  if (!responses.includes(200) || !await page.evaluate(() => document.fonts.check('400 14px PFLSansPreview', 'ДЛbь'))) throw new Error('actual preview WOFF2 was not loaded');
  if (await page.locator('.glyph-button').count() < 150) throw new Error('real font chart is incomplete');
  await page.locator('.glyph-button[data-character="Л"]').click();
  if (await page.locator('#selected-glyph').textContent() !== 'Л') throw new Error('selected glyph did not update');
  for (const [preset, weight, opticalSize] of [['text', '400', '14'], ['display', '500', '32']]) {
    await page.locator('#preset').selectOption(preset);
    const actual = await page.locator('.proof-text').first().evaluate(element => ({ family: getComputedStyle(element).fontFamily, variation: getComputedStyle(element).fontVariationSettings }));
    if (await page.locator('#weight').inputValue() !== weight || await page.locator('#opticalSize').inputValue() !== opticalSize || !actual.family.includes('PFLSansPreview') || !actual.variation.includes(`"wght" ${weight}`) || !actual.variation.includes(`"opsz" ${opticalSize}`)) throw new Error(`${preset} uses incorrect native axes`);
  }
  await page.locator('#weight').fill('650');
  if (await page.locator('#preset').inputValue() !== 'custom') throw new Error('manual axis edit did not create custom project');
  const proofSizes = await page.locator('.proof-text').evaluateAll(rows => rows.map(row => getComputedStyle(row).fontSize));
  if (JSON.stringify(proofSizes) !== JSON.stringify(['10px', '14px', '24px', '72px'])) throw new Error('required proof sizes are missing');
  const downloadPromise = page.waitForEvent('download'); await page.locator('#download-project').click();
  if (!(await downloadPromise).suggestedFilename().includes('v3')) throw new Error('project download is not versioned');
  await page.screenshot({ path: resolve('build/inter-browser.png'), fullPage: true });
  await page.setViewportSize({ width: 375, height: 800 });
  if (await page.evaluate(() => document.documentElement.scrollWidth > innerWidth)) throw new Error('mobile viewport overflows');
  const blocked = await browser.newContext(); await blocked.route('**/PFLSansVariable.woff2', route => route.abort());
  const errorPage = await blocked.newPage(); await errorPage.goto('http://127.0.0.1:8775/web/');
  await errorPage.waitForFunction(() => document.body.dataset.fontState === 'error');
  if (await errorPage.locator('.proof-list').isVisible()) throw new Error('missing font silently displays fallback specimen');
  await blocked.close();
  console.log('Inter-derived preview, chart, native axes, project download and missing-font gate verified');
} finally { await browser?.close(); server.kill(); }
