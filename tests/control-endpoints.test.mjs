import { execFileSync, spawn } from 'node:child_process';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { chromium } from 'playwright';

const root = resolve('.');
const python = process.env.PYTHON || resolve('.venv/bin/python');
const output = resolve('build/phase-02-endpoints');
await mkdir(output, { recursive: true });
const base = JSON.parse(await readFile(resolve('fontlab/project-v2.json'), 'utf8'));
const cases = [{ name: 'text', project: base }];
const display = structuredClone(base);
display.activePreset = 'display';
Object.assign(display.axes, { weight: 124, width: 1.08, xHeight: 520, roundness: .9, aperture: .72 });
Object.assign(display.switches, { aConstruction: 'single', zeroStyle: 'slashed' });
cases.push({ name: 'display', project: display });
for (const [axis, low, high] of [['weight', 40, 160], ['width', .85, 1.15], ['xHeight', 460, 540], ['roundness', 0, 1], ['aperture', 0, 1]]) {
  for (const [suffix, value] of [['min', low], ['max', high]]) {
    const project = structuredClone(base);
    project.axes[axis] = value;
    project.activePreset = 'custom';
    cases.push({ name: `${axis}-${suffix}`, project });
  }
}
const server = spawn(python, ['-m', 'http.server', '8773', '--bind', '127.0.0.1', '--directory', output], { cwd: root, stdio: 'ignore' });
let browser;
const report = [];
try {
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
  for (const item of cases) {
    const projectPath = resolve(output, `${item.name}.json`);
    await writeFile(projectPath, `${JSON.stringify(item.project, null, 2)}\n`);
    execFileSync(python, ['tools/build_font.py', '--project', projectPath, '--output-dir', output], { cwd: root, stdio: ['ignore', 'pipe', 'pipe'] });
    const proofPath = execFileSync(python, ['tools/verify_compiled_proof.py', '--project', projectPath, '--output-dir', output], { cwd: root, encoding: 'utf8' }).trim();
    const instance = proofPath.slice(output.length + 1).replace('/proof.html', '');
    const requests = [];
    page.on('response', response => { if (response.url().endsWith('.woff2')) requests.push(response.status()); });
    await page.goto(`http://127.0.0.1:8773/${instance}/proof.html`, { waitUntil: 'networkidle' });
    await page.waitForFunction(() => document.body.dataset.proofState === 'ready');
    if (!requests.includes(200)) throw new Error(`${item.name}: compiled WOFF2 was not loaded`);
    const details = await page.locator('.proof').evaluateAll(rows => rows.map(row => ({
      size: getComputedStyle(row).fontSize,
      family: getComputedStyle(row).fontFamily,
      visible: !!row.getClientRects().length,
      text: row.textContent,
    })));
    for (const [index, size] of [10, 14, 24, 72].entries()) {
      if (details[index].size !== `${size}px` || details[index].family !== 'PFLCompiled' || !details[index].visible || !details[index].text.includes('ДЛ')) {
        throw new Error(`${item.name}: invalid ${size}px compiled proof`);
      }
    }
    const screenshot = resolve(output, `${item.name}.png`);
    await page.screenshot({ path: screenshot, fullPage: true });
    report.push({ case: item.name, engine: item.project.engine.version, axes: item.project.axes, build: instance, screenshot });
  }
  await writeFile(resolve(output, 'report.json'), `${JSON.stringify(report, null, 2)}\n`);
  console.log(`Compiled TTF/OTF/WOFF2 and loaded WOFF2 at 10/14/24/72 px for ${report.length} Text/Display/endpoint cases`);
} finally {
  await browser?.close();
  server.kill();
}
