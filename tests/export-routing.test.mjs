import { execFileSync, spawnSync } from 'node:child_process';
import { mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';

const root = resolve('.');
const python = process.env.PYTHON || resolve('.venv/bin/python');
const temporary = await mkdtemp(resolve(tmpdir(), 'pfl-export-routing-'));
const projectPath = resolve(temporary, 'custom-project.json');
const outputDir = resolve(temporary, 'instances');

try {
  const project = JSON.parse(await readFile(resolve('fontlab/project.json'), 'utf8'));
  project.axes.weight = 109;
  project.activePreset = 'custom';
  await writeFile(projectPath, `${JSON.stringify(project, null, 2)}\n`, 'utf8');
  const exported = spawnSync('npm', ['run', 'export', '--', '--project', projectPath, '--output-dir', outputDir], { cwd: root, stdio: 'inherit' });
  if (exported.status !== 0) throw new Error('documented custom-project export failed');
  const proofPath = execFileSync(python, ['tools/verify_compiled_proof.py', '--project', projectPath, '--output-dir', outputDir], { cwd: root, encoding: 'utf8' }).trim();
  const manifest = JSON.parse(await readFile(resolve(proofPath, '../manifest.json'), 'utf8'));
  if (manifest.project !== project.id || !manifest.fonts.some(path => path.endsWith('.woff2'))) throw new Error('custom-project export did not create its selected instance manifest');
  const missing = spawnSync('npm', ['run', 'export', '--', '--project', resolve(temporary, 'missing.json'), '--output-dir', outputDir], { cwd: root, stdio: 'ignore' });
  if (missing.status === 0) throw new Error('missing selected project unexpectedly exported a default instance');
  console.log('custom project routing and missing-project rejection verified');
} finally {
  await rm(temporary, { recursive: true, force: true });
}
