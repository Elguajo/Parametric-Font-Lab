import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { resolve } from 'node:path';

const server = spawn('python3', ['-m', 'http.server', '8765', '--bind', '127.0.0.1'], {
  cwd: resolve('..'), stdio: 'ignore',
});
let browser;
try {
  browser = await chromium.launch({
    headless: true,
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  });
  const page = await browser.newPage({ viewport: { width: 900, height: 700 } });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('http://127.0.0.1:8765/browser-outline/');
  await page.waitForFunction(() => window.pflProbe?.renders > 0);
  const before = await page.locator('#outline path').getAttribute('d');
  await page.locator('#text').fill('OH');
  const changedText = await page.locator('#outline path').getAttribute('d');
  await page.locator('#width').evaluate(el => {
    el.value = '1.20';
    el.dispatchEvent(new Event('input', { bubbles: true }));
  });
  const transform = await page.locator('#outline path').getAttribute('transform');
  if (before === changedText || transform !== 'scale(1.2 1)' || errors.length) {
    throw new Error(JSON.stringify({ before, changedText, transform, errors }));
  }
  const metrics = await page.evaluate(() => window.pflProbe);
  await page.screenshot({ path: 'proof.png' });
  console.log(JSON.stringify({ ...metrics, textPathChanged: true, transform, errors }));
} finally {
  await browser?.close();
  server.kill();
}
