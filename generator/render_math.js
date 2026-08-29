// Reads {"items":[{"t":"...","display":bool}]} on stdin, writes rendered HTML.
const katex = require('katex');
let raw = '';
process.stdin.on('data', d => raw += d);
process.stdin.on('end', () => {
  const inp = JSON.parse(raw);
  const out = inp.items.map(it => {
    try {
      return { ok: true, html: katex.renderToString(it.t, {
        displayMode: it.display, throwOnError: true, strict: false, output: 'html' }) };
    } catch (e) {
      return { ok: false, err: String(e.message || e), src: it.t };
    }
  });
  process.stdout.write(JSON.stringify({ out }));
});
