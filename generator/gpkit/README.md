# The Gradient Path generator

Modules 01, 03, 04, 05 and 06 and the hub are **generated**. Editing the built
HTML directly is lost on the next rebuild.

This pipeline was ephemeral twice and had to be rebuilt from scratch both times,
which is the expensive part of touching this site. It lives here now.

## Rebuild

```bash
cd generator
npm install katex                      # katexify needs a local KaTeX
python3 check.py mod05                 # schema validation, no build
python3 assemble.py mod05 mod05.py 05-statistics.html
python3 katexify.py 05-statistics.html # pre-render $...$ -- no CDN at runtime
python3 build_index.py                 # rebuild the hub from the built pages
```

`gpkit/katex.css` is 261 KB of base64 woff2 and is committed. If it is ever lost,
re-extract it from any built page: it is the FIRST `<style>` block; the second is

## What is where

| file | does |
|---|---|
| `gpkit/figkit.py` | declarative SVG figures, 720 wide, CSS-variable colours |
| `gpkit/build.py` | cards → page shell; owns the two-layer contract |
| `gpkit/prompts.py` | the four-stage tutor prompt, per topic and per tier |
| `gpkit/page.css` `page.js` | extracted verbatim from a built page, then extended |
| `check.py` / `checkfile.py` | the schema validator; run before every build |
| `assemble.py` | collect content → validate → build → fix the entity bug |
| `katexify.py` + `render_math.js` | pre-render all math with a local KaTeX |
| `build_index.py` | the hub; reads each page's own rail so the path cannot drift |
| `retrofit.py` | back-ports real Simple mode onto pages built before it existed |
| `SCHEMA.md` | the card contract handed to content authors |
| `BRIEF.md` | the authoring brief |
| `content/mod05` `mod06` | the card source |
| `research/` | what 2026 interviews actually ask, with sources |

## Three bugs that have each cost a rebuild

1. **`&mdash\;`** — an HTML entity written with a backslash before the semicolon.
   `sed 's/\;/;/g'` is a no-op, because BRE reads `\;` as `;`. Fix in Python, and
   only where `\;` terminates an entity name — a blanket replace also eats
   LaTeX's `\;` thin space inside math. `assemble.py` does it correctly now.
2. **Currency.** `katexify` pairs `$ ... $` across a line, so a stray dollar sign
   finds the next one and renders the prose between them as math — silently,
   because the result is often valid TeX. Write money as `&#36;`. `check.py`
   rejects unbalanced `$` and any `$...$` span that reads like a sentence.
3. **Double-escaped titles.** Card titles already contain `&amp;`, so passing
   them through `html.escape` for the prompt `<pre>` gives `&amp;amp;`.
   `prompts._plain()` strips tags and unescapes before interpolating.
