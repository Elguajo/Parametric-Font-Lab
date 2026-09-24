import { spawnSync } from 'node:child_process';
import { resolve } from 'node:path';

const allowed = new Set(['--project', '--output-dir']);
const forwarded = process.argv.slice(2);
for (let index = 0; index < forwarded.length; index += 2) {
  if (!allowed.has(forwarded[index]) || !forwarded[index + 1]) {
    throw new Error(`expected --project or --output-dir with a value, received ${forwarded[index] || '(nothing)'}`);
  }
}

const python = process.env.PYTHON || resolve('.venv/bin/python');
for (const [command, args] of [
  [python, ['tools/build_font.py', ...forwarded]],
  [process.execPath, ['tests/compiled-font-proof.test.mjs', ...forwarded]],
]) {
  const result = spawnSync(command, args, { stdio: 'inherit' });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status || 1);
}
