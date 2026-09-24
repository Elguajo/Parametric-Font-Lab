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
  const sourceHash = execFileSync(python, ['-c', 'import sys; from pathlib import Path; from fontlab.recipes import load_project, source_hash; print(source_hash(load_project(Path(sys.argv[1]))))', projectPath], { cwd: root, encoding: 'utf8' }).trim();
  const manifest = JSON.parse(await readFile(resolve(outputDir, sourceHash, 'manifest.json'), 'utf8'));
  if (manifest.sourceHash !== sourceHash || !manifest.fonts.some(path => path.endsWith('.woff2'))) throw new Error('custom-project export did not create its selected instance manifest');
  const missing = spawnSync('npm', ['run', 'export', '--', '--project', resolve(temporary, 'missing.json'), '--output-dir', outputDir], { cwd: root, stdio: 'ignore' });
  if (missing.status === 0) throw new Error('missing selected project unexpectedly exported a default instance');
  console.log('custom project routing and missing-project rejection verified');
} finally {
  await rm(temporary, { recursive: true, force: true });
}
