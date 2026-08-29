const { chromium } = require('playwright');
const fs = require('fs');
const PAGES = ['index.html','01-linear-algebra.html','blind75nightlyreview.html',
  '03-machine-learning.html','04-llms.html','05-statistics.html','06-system-design.html'];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  let fail = 0;
  for (const f of PAGES) {
    const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
    const errs = [];
    p.on('pageerror', e => errs.push(String(e).slice(0,140)));
    p.on('console', m => { const t=m.text(); if (m.type()==='error' && !/ERR_TUNNEL|fonts.g/.test(t)) errs.push('console: '+t.slice(0,140)); });
    await p.goto('file:///tmp/gp/site/' + f);
    await p.waitForTimeout(500);
    const r = await p.evaluate(() => {
      const out = { cards: document.querySelectorAll('.card').length,
                    rail: document.querySelectorAll('[data-rail]').length,
                    switches: document.querySelectorAll('.modeswitch').length,
                    techOnly: document.querySelectorAll('.tech-only').length,
                    upshift: document.querySelectorAll('.upshift').length,
                    badHref: [] };
      document.querySelectorAll('a[href$=".html"]').forEach(a => {
        out.badHref.push(a.getAttribute('href'));
      });
      out.badHref = [...new Set(out.badHref)];
      return out;
    });
    // measure the two modes
    let heights = null;
    if (r.switches > 0) {
      const h = async m => { await p.evaluate(x => window.__setMode(x), m);
                             await p.waitForTimeout(200);
                             return p.evaluate(() => document.body.scrollHeight); };
      const simple = await h('simple'), tech = await h('tech');
      heights = { simple, tech, shrink: (100*(1 - simple/tech)).toFixed(1) + '%' };
      // and confirm the switch persists
      await p.evaluate(x => window.__setMode(x), 'simple');
    }
    const ok = errs.length === 0;
    if (!ok) fail++;
    console.log(`${ok?'OK  ':'FAIL'} ${f.padEnd(28)} cards=${String(r.cards).padStart(3)} rail=${String(r.rail).padStart(3)} switches=${r.switches} tech-only=${String(r.techOnly).padStart(3)} upshift=${String(r.upshift).padStart(3)}` +
      (heights ? `  simple=${heights.simple}px tech=${heights.tech}px (-${heights.shrink})` : ''));
    if (errs.length) errs.slice(0,3).forEach(e => console.log('      !', e));
    for (const h2 of r.badHref) if (!fs.existsSync('/tmp/gp/site/' + h2)) { console.log('      ! dead link:', h2); fail++; }
    await p.close();
  }
  console.log(fail ? `\n${fail} FAILURES` : '\nall pages clean');
  await b.close();
})();
