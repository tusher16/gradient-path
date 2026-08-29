#!/usr/bin/env python3
"""Pre-render every $...$ and $$...$$ with a local KaTeX so the page has no
CDN dependency and math renders offline. Anything inside <pre> is skipped --
the tutor prompts are plain text and must stay plain text."""
import sys, os, re, json, subprocess, html as H
import os as _os
ROOT = _os.path.dirname(_os.path.abspath(__file__))

SEG = re.compile(r'(<pre\b.*?</pre>)', re.S)
DISPLAY = re.compile(r'\$\$(.+?)\$\$', re.S)
INLINE = re.compile(r'(?<!\$)\$([^$\n]+?)\$(?!\$)')


def render_all(items):
    p = subprocess.run(['node', os.path.join(ROOT, 'render_math.js')],
                       input=json.dumps({'items': items}), capture_output=True, text=True)
    if p.returncode != 0:
        print(p.stderr[:2000]); sys.exit(1)
    return json.loads(p.stdout)['out']


def main():
    path = sys.argv[1]
    s = open(path).read()
    parts = SEG.split(s)

    items, slots = [], []
    for i, part in enumerate(parts):
        if i % 2 == 1:            # inside <pre>, leave alone
            continue
        def grab(m, display):
            tex = H.unescape(m.group(1))     # &lt; inside math is a parse error
            items.append({'t': tex, 'display': display})
            slots.append((i, len(items) - 1))
            return f'\x00{len(items)-1}\x00'
        parts[i] = DISPLAY.sub(lambda m: grab(m, True), part)
        parts[i] = INLINE.sub(lambda m: grab(m, False), parts[i])

    if not items:
        print('no math found'); return
    out = render_all(items)
    bad = [(o.get('src'), o.get('err')) for o in out if not o['ok']]
    if bad:
        print(f'{len(bad)} KaTeX failures:')
        for src, err in bad[:20]:
            print('  ', repr(src)[:120], '->', str(err)[:160])
        sys.exit(1)

    def fill(m):
        return out[int(m.group(1))]['html']
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r'\x00(\d+)\x00', fill, parts[i])

    open(path, 'w').write(''.join(parts))
    print(f'katexified {path}: {len(items)} expressions')


if __name__ == '__main__':
    main()
