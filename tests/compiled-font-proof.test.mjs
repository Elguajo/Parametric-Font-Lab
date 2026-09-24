import { execFile } from 'node:child_process';
import { spawn } from 'node:child_process';
import { dirname, relative, resolve, sep } from 'node:path';
import { readFile } from 'node:fs/promises';
import { promisify } from 'node:util';
import { chromium } from 'playwright';

const root = resolve('.');
const python = process.env.PYTHON || resolve('.venv/bin/python');
const execFileAsync = promisify(execFile);
const options = { project: resolve('fontlab/project.json'), outputDir: resolve('build') };
for (let index = 2; index < process.argv.length; index += 1) {
  const option = process.argv[index];
  const key = option === '--project' ? 'project' : option === '--output-dir' ? 'outputDir' : null;
  if (!key || !process.argv[index + 1]) throw new Error(`expected --project or --output-dir with a value, received ${option}`);
  options[key] = resolve(process.argv[index + 1]);
  index += 1;
}

// Verification reads the current recipe/compiler bytes and rejects missing, stale or
// modified binaries before Chromium is allowed to render a specimen.
const { stdout } = await execFileAsync(python, ['tools/verify_compiled_proof.py', '--project', options.project, '--output-dir', options.outputDir], { cwd: root });
const proofPath = stdout.trim();
const project = JSON.parse(await readFile(options.project, 'utf8'));
let expectedPairs = null;
if (project.schemaVersion !== 3) {
  const { stdout: pairOutput } = await execFileAsync(python, ['-c', 'import json,sys; from pathlib import Path; from fontlab.recipes import GLYPH_DEFINITIONS,evaluate_project,kerning_value,load_project; names={chr(g["unicode"]):g["name"] for g in GLYPH_DEFINITIONS}; p=evaluate_project(load_project(Path(sys.argv[1])))["kerning"]; print(json.dumps({s:kerning_value(*(names[c] for c in s),p)*-.072 for s in ("AO","AV","VA","TO","Ta","To","АО","ТА","Та","То")}))', options.project], { cwd: root });
  expectedPairs = JSON.parse(pairOutput);
}
const proofUrl = `/${relative(dirname(options.outputDir), proofPath).split(sep).join('/')}`;
const server = spawn(python, ['-m', 'http.server', '8767', '--bind', '127.0.0.1', '--directory', dirname(options.outputDir)], { cwd: root, stdio: 'ignore' });
let browser;
try {
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 850 } });
  const responses = [];
  page.on('response', response => { if (response.url().endsWith('.woff2')) responses.push(response.status()); });
  await page.goto(`http://127.0.0.1:8767${proofUrl}`, { waitUntil: 'networkidle' });
  await page.waitForFunction(() => document.body.dataset.proofState === 'ready');
  if (!responses.includes(200)) throw new Error('browser did not load the selected compiled WOFF2');
  const rows = await page.locator('.proof').evaluateAll(elements => elements.map(element => ({
    size: getComputedStyle(element).fontSize,
    family: getComputedStyle(element).fontFamily,
    visible: !!element.getClientRects().length,
    text: element.textContent,
  })));
  for (const [index, size] of [10, 14, 24, 72].entries()) {
    const row = rows[index];
    if (row.size !== `${size}px` || row.family !== 'PFLCompiled' || !row.visible || !row.text.includes('ДЛ') || !row.text.includes('bone')) {
      throw new Error(`compiled proof row is invalid at ${size}px: ${JSON.stringify(row)}`);
    }
  }
  if (await page.evaluate(() => ![...document.fonts].some(face => face.family === 'PFLCompiled' && face.status === 'loaded'))) throw new Error('PFLCompiled FontFace is absent');
  const kerning = await page.evaluate(pairs => {
    const measure = (text, kerning) => {
      const context = document.createElement('canvas').getContext('2d');
      context.font = '72px PFLCompiled';
      context.fontKerning = kerning;
      return context.measureText(text).width;
    };
    return Object.fromEntries(Object.entries(pairs).map(([pair, expected]) => [pair, { expected, actual: measure(pair, 'none') - measure(pair, 'normal') }]));
  }, expectedPairs || { AV: null, To: null, 'ДО': null });
  if (expectedPairs) {
    for (const [pair, { expected, actual }] of Object.entries(kerning)) if (Math.abs(actual - expected) > .01) throw new Error(`compiled GPOS kerning for ${pair} differs from source: ${actual}, expected ${expected}`);
  } else if (Object.values(kerning).every(({ actual }) => Math.abs(actual) < .01)) {
    throw new Error('Inter-derived compiled font has no observable pair kerning');
  }
  await page.screenshot({ path: resolve(project.schemaVersion === 3 ? 'build/compiled-pfl-sans-proof.png' : 'build/compiled-phase-02-proof.png'), fullPage: true });
  const failedContext = await browser.newContext();
  await failedContext.route('**/*.woff2', route => route.abort());
  const failedPage = await failedContext.newPage();
  await failedPage.goto(`http://127.0.0.1:8767${proofUrl}`);
  await failedPage.waitForFunction(() => document.body.dataset.proofState === 'error');
  if (await failedPage.locator('.proof').first().isVisible()) throw new Error('missing WOFF2 silently fell back to another font');
  await failedContext.close();
  console.log('selected compiled WOFF2 loaded; 10/14/24/72 px Latin/Cyrillic proof and GPOS kerning verified');
} finally {
  await browser?.close();
  server.kill();
}
