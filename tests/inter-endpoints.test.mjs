import { execFileSync, spawn } from 'node:child_process';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { chromium } from 'playwright';

const root = resolve('.');
const python = process.env.PYTHON || resolve('.venv/bin/python');
const output = resolve('build/inter-endpoints');
await mkdir(output, { recursive: true });
const base = JSON.parse(await readFile(resolve('fontlab/project.json'), 'utf8'));
const cases = [['text', { weight: 400, opticalSize: 14 }], ['display', { weight: 500, opticalSize: 32 }],
  ['weight-min', { weight: 100, opticalSize: 14 }], ['weight-max', { weight: 900, opticalSize: 14 }],
  ['optical-min', { weight: 400, opticalSize: 14 }], ['optical-max', { weight: 400, opticalSize: 32 }]];
const server = spawn(python, ['-m', 'http.server', '8776', '--bind', '127.0.0.1', '--directory', output], { cwd: root, stdio: 'ignore' });
let browser;
const report = [];
try {
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1200, height: 900 } });
  for (const [name, axes] of cases) {
    const project = { ...base, axes, activePreset: name === 'text' || name === 'display' ? name : 'custom' };
    const projectPath = resolve(output, `${name}.json`);
    await writeFile(projectPath, JSON.stringify(project, null, 2) + '\n');
    execFileSync(python, ['tools/build_font.py', '--project', projectPath, '--output-dir', output], { cwd: root });
    const proof = execFileSync(python, ['tools/verify_compiled_proof.py', '--project', projectPath, '--output-dir', output], { cwd: root, encoding: 'utf8' }).trim();
    await page.goto(`http://127.0.0.1:8776/${proof.slice(output.length + 1).replaceAll('\\', '/')}`, { waitUntil: 'networkidle' });
    await page.waitForFunction(() => document.body.dataset.proofState === 'ready');
    const rows = await page.locator('.proof').evaluateAll(elements => elements.map(element => ({ size: getComputedStyle(element).fontSize, visible: !!element.getClientRects().length, text: element.textContent })));
    for (const [index, size] of [10, 14, 24, 72].entries()) if (rows[index]?.size !== `${size}px` || !rows[index].visible || !rows[index].text.includes('ДЛ b ь')) throw new Error(`${name}: invalid ${size}px proof`);
    const screenshot = resolve(output, `${name}.png`);
    await page.screenshot({ path: screenshot, fullPage: true });
    report.push({ name, axes, screenshot, proof });
  }
  await writeFile(resolve(output, 'report.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(`Inter-derived Text/Display and both native axis endpoints loaded at 10/14/24/72 px: ${report.length} cases`);
} finally { await browser?.close(); server.kill(); }
