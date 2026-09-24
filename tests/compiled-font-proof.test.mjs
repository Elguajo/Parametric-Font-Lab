import { readFile } from 'node:fs/promises';
import { execFile, spawn } from 'node:child_process';
import { resolve } from 'node:path';
import { promisify } from 'node:util';
import { chromium } from 'playwright';

const root = resolve('.');
const python = process.env.PYTHON || resolve('.venv/bin/python');
const proof = 'АВНОРСХ ДЛЖКУФЯ\nбдлтф ёж AА eе\nAO AV VA TO Ta To АО ТА Та То';
const execFileAsync = promisify(execFile);

async function compiledWoff2() {
  const { stdout } = await execFileAsync(python, ['-c', 'from fontlab.recipes import load_project, source_hash; print(source_hash(load_project()))'], { cwd: root });
  const sourceHash = stdout.trim();
  const manifest = JSON.parse(await readFile(resolve('build', sourceHash, 'manifest.json'), 'utf8'));
  if (manifest.project !== 'pfl-technical-sans-phase-1b' || manifest.sourceHash !== sourceHash) throw new Error('compiled Phase 1b manifest does not match the exported source');
  const font = manifest.fonts.find(path => path.endsWith('.woff2'));
  if (!font) throw new Error('compiled Phase 1b WOFF2 is absent; run npm run export first');
  return `/build/${sourceHash}/${font}`;
}

const server = spawn(python, ['-m', 'http.server', '8767', '--bind', '127.0.0.1'], { cwd: root, stdio: 'ignore' });
let browser;
try {
  const fontUrl = await compiledWoff2();
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 850 } });
  const responses = [];
  page.on('response', response => { if (response.url().endsWith('.woff2')) responses.push(response.status()); });
  await page.goto('http://127.0.0.1:8767/web/', { waitUntil: 'networkidle' });
  await page.setContent(`<!doctype html><style>@font-face{font-family:PFLCompiled;src:url('${fontUrl}') format('woff2')}body{font-family:PFLCompiled;font-kerning:normal}.proof{white-space:pre-wrap}</style><div class="proof">${proof}</div>`);
  await page.waitForFunction(() => document.fonts.status === 'loaded' && document.fonts.check('10px PFLCompiled'));
  if (!responses.includes(200)) throw new Error('browser did not load the compiled WOFF2');
  for (const size of [10, 14, 24, 72]) {
    await page.locator('.proof').evaluate((element, value) => { element.style.fontSize = `${value}px`; }, size);
    if ((await page.locator('.proof').innerText()) !== proof) throw new Error(`compiled proof text changed at ${size}px`);
  }
  const kerning = await page.evaluate(() => {
    const measure = (text, kerning) => {
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      context.font = '72px PFLCompiled';
      context.fontKerning = kerning;
      return context.measureText(text).width;
    };
    return Object.fromEntries([
      ['AO', 5.184], ['AV', 4.32], ['VA', 4.32], ['TO', 4.176], ['Ta', 3.024], ['To', 3.024],
      ['АО', 4.752], ['ТА', 3.888], ['Та', 3.456], ['То', 3.456],
    ].map(([pair, expected]) => [pair, { expected, actual: measure(pair, 'none') - measure(pair, 'normal') }]));
  });
  for (const [pair, { expected, actual }] of Object.entries(kerning)) if (Math.abs(actual - expected) > .01) throw new Error(`compiled GPOS kerning for ${pair} differs from source: ${actual}, expected ${expected}`);
  await page.screenshot({ path: resolve('build/compiled-phase-1b-proof.png'), fullPage: true });
  console.log('compiled WOFF2 loaded; 10/14/24/72 px Latin/Cyrillic proof and GPOS kerning verified');
} finally {
  await browser?.close();
  server.kill();
}
