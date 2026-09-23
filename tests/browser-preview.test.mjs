import { spawn } from 'node:child_process';
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
  await page.locator('#specimen').fill('AVATAR СТРОКА АВНОРСХ ДЛЖКУФЯ бдлтф ёж AА eе 0123456789');
  if (await page.locator('#preview-error').textContent()) throw new Error('covered Latin/Cyrillic proof has unsupported characters');
  await page.locator('#preset').selectOption('display');
  if (await page.locator('#zero-style').inputValue() !== 'slashed') throw new Error('display preset did not control the zero switch');
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
  await page.setViewportSize({ width: 375, height: 800 });
  if (await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth)) throw new Error('mobile viewport has horizontal overflow');
  if (errors.length) throw new Error(`browser errors: ${errors.join('; ')}`);
  console.log('full chart, script proof, presets/A-B, controls and download verified');
} finally { await browser?.close(); server.kill(); }
