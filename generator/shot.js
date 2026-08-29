const { chromium } = require('playwright');
(async () => {
  const [file, out, mode, w, h] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: +(w||1280), height: +(h||1400) } });
  await p.goto('file://' + file);
  await p.waitForTimeout(400);
  if (mode) { await p.evaluate(m => window.__setMode(m), mode); await p.waitForTimeout(250); }
  await p.screenshot({ path: out, fullPage: true });
  await b.close();
})();
