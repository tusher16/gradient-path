"""Declarative SVG figures for Gradient Path. Canvas is always 720 wide.

A card supplies fig={'kind': ..., ...}. Colours are CSS variables so every
figure re-themes with the page. Tones:
  sig   pink   -- what moves / where the error is / the thing that goes wrong
  mem   teal   -- what survives / the honest estimate / the move that works
  plain        -- currentColor
  mute         -- currentColor at low opacity
"""
from xml.sax.saxutils import escape

W = 720
MONO = "'IBM Plex Mono', ui-monospace, monospace"

TONE = {
    'sig':   'var(--signal)',
    'mem':   'var(--memory)',
    'plain': 'currentColor',
    'mute':  'currentColor',
}
TONE_OP = {'sig': 1.0, 'mem': 1.0, 'plain': 0.85, 'mute': 0.5}


def _c(tone):
    return TONE.get(tone, 'currentColor')


def _f(v):
    return f"{float(v):.1f}"


# ---------------------------------------------------------------- primitives
def text(x, y, s, size=12, anchor='middle', tone='plain', weight='400',
         op=None, track=None, rot=None):
    if op is None:
        op = TONE_OP.get(tone, 0.85)
    a = (f'<text x="{_f(x)}" y="{_f(y)}" font-size="{size}" text-anchor="{anchor}" '
         f'fill="{_c(tone)}" font-weight="{weight}" opacity="{op:.2f}"')
    if track:
        a += f' letter-spacing="{track}"'
    if rot is not None:
        a += f' transform="rotate({rot} {_f(x)} {_f(y)})"'
    return a + f'>{escape(str(s))}</text>'


def cap(x, y, s, tone='plain', anchor='middle', size=10.5, op=0.60, rot=None):
    """Small uppercase tracked label."""
    return text(x, y, str(s).upper(), size=size, anchor=anchor, tone=tone,
                op=op, track='1.2', rot=rot)


def rect(x, y, w, h, tone='plain', fill=False, op=None, r=3, sw=1.1, dash=None):
    out = []
    if fill:
        out.append(f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" '
                   f'rx="{r}" fill="{_c(tone)}" opacity="{op if op is not None else 0.18:.2f}"/>')
    d = f' stroke-dasharray="{dash}"' if dash else ''
    out.append(f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" rx="{r}" '
               f'fill="none" stroke="{_c(tone)}" stroke-width="{sw}" opacity="0.45"{d}/>')
    return ''.join(out)


def line(x1, y1, x2, y2, tone='plain', sw=1.1, dash=None, arrow=False, op=0.45):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    m = ''
    if arrow:
        m = f' marker-end="url(#ar-{ {"sig":"sig","mem":"mem"}.get(tone,"fg") })"'
    return (f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" '
            f'stroke="{_c(tone)}" stroke-width="{sw}" opacity="{op:.2f}"{d}{m}/>')


def path(d, tone='plain', sw=1.6, fill='none', op=0.9, dash=None):
    ds = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<path d="{d}" fill="{fill}" stroke="{_c(tone)}" stroke-width="{sw}" '
            f'opacity="{op:.2f}" stroke-linejoin="round" stroke-linecap="round"{ds}/>')


def dot(x, y, r=3.2, tone='plain', op=0.9):
    return f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{r}" fill="{_c(tone)}" opacity="{op:.2f}"/>'


def ring(x, y, r=4, tone='plain', sw=1.4, op=0.9):
    return (f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{r}" fill="none" '
            f'stroke="{_c(tone)}" stroke-width="{sw}" opacity="{op:.2f}"/>')


def svg(body, h, label):
    return (f'<svg viewBox="0 0 {W} {int(h)}" role="img" aria-label="{escape(label)}" '
            f'font-family="{MONO}" font-size="13">{body}</svg>')


def _wrap(s, n):
    words, out, cur = str(s).split(), [], ''
    for w in words:
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur); cur = w
        else:
            cur = (cur + ' ' + w).strip()
    if cur:
        out.append(cur)
    return out


# ------------------------------------------------------------------- kinds
def k_pipeline(f):
    """Boxes left to right with arrows. steps=[{t, sub, tone}]"""
    steps = f['steps']
    n = len(steps)
    top = 44 if f.get('head') else 26
    bh = f.get('bh', 62)
    gap = 26
    bw = (W - 68 - gap * (n - 1)) / n
    y = top + 14
    b = []
    if f.get('head'):
        b.append(cap(34, 20, f['head'][0], tone='sig', anchor='start', op=0.9, size=11))
        if len(f['head']) > 1:
            b.append(cap(686, 20, f['head'][1], tone='mem', anchor='end', op=0.85, size=11))
    for i, s in enumerate(steps):
        x = 34 + i * (bw + gap)
        tone = s.get('tone', 'plain')
        b.append(rect(x, y, bw, bh, tone=tone, fill=tone in ('sig', 'mem'),
                      op=0.14, dash=s.get('dash')))
        lines = _wrap(s['t'], max(10, int(bw / 7.4)))
        ty = y + bh / 2 - (len(lines) - 1) * 7 - (5 if s.get('sub') else -1)
        for j, ln in enumerate(lines):
            b.append(text(x + bw / 2, ty + j * 14, ln, size=11.5, tone=tone, weight='600'))
        if s.get('sub'):
            b.append(text(x + bw / 2, ty + len(lines) * 14 + 3, s['sub'], size=10,
                          tone=tone, op=0.62))
        if i < n - 1:
            ar = steps[i].get('arrow', 'plain')
            b.append(line(x + bw + 5, y + bh / 2, x + bw + gap - 6, y + bh / 2,
                          tone=ar, sw=1.3, arrow=True, op=0.6))
    h = y + bh + 22
    if f.get('foot'):
        b.append(text(360, h + 10, f['foot'], size=10.5, tone='plain', op=0.6))
        h += 22
    return ''.join(b), h


def k_grid(f):
    """A 2x2 (or n x m) decision table. cells=[[{t,sub,tone,fill}]] row-major."""
    cells = f['cells']
    rows, cols = len(cells), len(cells[0])
    top = 44 if f.get('head') else 30
    lx, ly = 223, top + 45
    cw, ch = (615 - 223) / cols, 68
    b = []
    if f.get('head'):
        b.append(cap(34, 20, f['head'][0], tone='sig', anchor='start', op=0.9, size=11))
        if len(f['head']) > 1:
            b.append(cap(686, 20, f['head'][1], tone='mem', anchor='end', op=0.85, size=11))
    if f.get('xlab'):
        b.append(cap(419, top - 8, f['xlab'], op=0.6))
    if f.get('ylab'):
        b.append(cap(36, ly + rows * ch / 2, f['ylab'], op=0.6, rot=-90))
    for j, c in enumerate(f.get('cols', [])):
        b.append(text(lx + j * cw + cw / 2, ly - 7, c, size=11, weight='600', op=0.75))
    for i, r in enumerate(f.get('rows', [])):
        b.append(text(lx - 9, ly + i * ch + ch / 2 + 4, r, size=11, anchor='end',
                      weight='600', op=0.75))
    for i in range(rows):
        for j in range(cols):
            c = cells[i][j]
            tone = c.get('tone', 'plain')
            x, y = lx + j * cw, ly + i * ch
            b.append(rect(x, y, cw, ch, tone=tone, fill=c.get('fill', False), op=0.18))
            b.append(text(x + cw / 2, y + 32, c['t'], size=12, tone=tone, weight='600', op=1.0))
            if c.get('sub'):
                b.append(text(x + cw / 2, y + 47, c['sub'], size=10, tone=tone, op=0.6))
    h = ly + rows * ch + 24
    if f.get('foot'):
        b.append(text(360, h + 12, f['foot'], size=10.5, op=0.6))
        h += 26
    return ''.join(b), h


def k_plot(f):
    """Curves on axes. curves=[{pts:[(x,y)..] in data units, tone, label, dash}]"""
    x0, x1 = f.get('xr', (0, 1))
    y0, y1 = f.get('yr', (0, 1))
    L, R, T, B = 78, 660, (46 if f.get('head') else 28), 0
    ph = f.get('ph', 190)
    bot = T + ph
    b = []
    if f.get('head'):
        b.append(cap(34, 20, f['head'][0], tone='sig', anchor='start', op=0.9, size=11))
        if len(f['head']) > 1:
            b.append(cap(686, 20, f['head'][1], tone='mem', anchor='end', op=0.85, size=11))

    def px(v):
        return L + (v - x0) / (x1 - x0) * (R - L)

    def py(v):
        return bot - (v - y0) / (y1 - y0) * ph

    b.append(line(L, bot, R, bot, sw=1.1, op=0.4))
    b.append(line(L, T, L, bot, sw=1.1, op=0.4))
    for gx, gl in f.get('xticks', []):
        b.append(line(px(gx), bot, px(gx), bot + 4, sw=1, op=0.4))
        b.append(text(px(gx), bot + 18, gl, size=10, op=0.6))
    for gy, gl in f.get('yticks', []):
        b.append(line(L - 4, py(gy), L, py(gy), sw=1, op=0.4))
        b.append(text(L - 9, py(gy) + 3.5, gl, size=10, anchor='end', op=0.6))
    for g in f.get('vlines', []):
        b.append(line(px(g['x']), T, px(g['x']), bot, tone=g.get('tone', 'plain'),
                      dash='4 4', sw=1.2, op=0.5))
        if g.get('label'):
            b.append(text(px(g['x']), T - 6, g['label'], size=10,
                          tone=g.get('tone', 'plain'), op=0.85, weight='600'))
    for g in f.get('hlines', []):
        b.append(line(L, py(g['y']), R, py(g['y']), tone=g.get('tone', 'plain'),
                      dash='4 4', sw=1.2, op=0.5))
        if g.get('label'):
            b.append(text(R, py(g['y']) - 6, g['label'], size=10, anchor='end',
                          tone=g.get('tone', 'plain'), op=0.85, weight='600'))
    for g in f.get('bands', []):
        xa, xb = px(g['x0']), px(g['x1'])
        b.append(f'<rect x="{_f(xa)}" y="{_f(T)}" width="{_f(xb-xa)}" height="{_f(ph)}" '
                 f'fill="{_c(g.get("tone","mem"))}" opacity="{g.get("op",0.10):.2f}"/>')
        if g.get('label'):
            b.append(text((xa + xb) / 2, T + 14, g['label'], size=10,
                          tone=g.get('tone', 'mem'), op=0.9, weight='600'))
    for c in f['curves']:
        pts = c['pts']
        if c.get('fill'):
            d = 'M' + f'{px(pts[0][0]):.1f} {bot:.1f}'
            d += ' L' + ' L'.join(f'{px(a):.1f} {py(bb):.1f}' for a, bb in pts)
            d += f' L{px(pts[-1][0]):.1f} {bot:.1f} Z'
            b.append(f'<path d="{d}" fill="{_c(c.get("tone","plain"))}" opacity="0.13"/>')
        d = 'M' + ' L'.join(f'{px(a):.1f} {py(bb):.1f}' for a, bb in pts)
        b.append(path(d, tone=c.get('tone', 'plain'), sw=c.get('sw', 1.8),
                      dash=c.get('dash'), op=0.95))
        if c.get('label'):
            lx_, ly_ = pts[c.get('lat', -1)]
            b.append(text(px(lx_) + c.get('dx', 8), py(ly_) + c.get('dy', -6),
                          c['label'], size=10.5, anchor=c.get('la', 'start'),
                          tone=c.get('tone', 'plain'), weight='600', op=0.95))
    for p in f.get('marks', []):
        b.append(dot(px(p['x']), py(p['y']), r=p.get('r', 3.6), tone=p.get('tone', 'sig')))
        if p.get('label'):
            b.append(text(px(p['x']) + p.get('dx', 8), py(p['y']) + p.get('dy', -8),
                          p['label'], size=10, anchor=p.get('la', 'start'),
                          tone=p.get('tone', 'sig'), weight='600', op=0.95))
    if f.get('xlab'):
        b.append(cap(370, bot + 38, f['xlab'], op=0.6))
    if f.get('ylab'):
        b.append(cap(30, T + ph / 2, f['ylab'], op=0.6, rot=-90))
    h = bot + (52 if f.get('xlab') else 34)
    if f.get('foot'):
        b.append(text(360, h + 8, f['foot'], size=10.5, op=0.6))
        h += 24
    return ''.join(b), h


def k_bars(f):
    """Horizontal labelled bars. bars=[{label, v, tone, note}] with vmax."""
    bars = f['bars']
    vmax = f.get('vmax') or max(b['v'] for b in bars) * 1.12
    top = 44 if f.get('head') else 26
    lw = f.get('lw', 168)
    bx, bw = 34 + lw, W - 68 - lw - 96
    bh, gap = f.get('bh', 26), 12
    b = []
    if f.get('head'):
        b.append(cap(34, 20, f['head'][0], tone='sig', anchor='start', op=0.9, size=11))
        if len(f['head']) > 1:
            b.append(cap(686, 20, f['head'][1], tone='mem', anchor='end', op=0.85, size=11))
    for i, s in enumerate(bars):
        y = top + i * (bh + gap)
        tone = s.get('tone', 'plain')
        w = max(2.0, s['v'] / vmax * bw)
        b.append(text(34 + lw - 12, y + bh / 2 + 4, s['label'], size=11, anchor='end',
                      op=0.8, weight='600'))
        b.append(f'<rect x="{_f(bx)}" y="{_f(y)}" width="{_f(bw)}" height="{_f(bh)}" rx="3" '
                 f'fill="currentColor" opacity="0.05"/>')
        b.append(f'<rect x="{_f(bx)}" y="{_f(y)}" width="{_f(w)}" height="{_f(bh)}" rx="3" '
                 f'fill="{_c(tone)}" opacity="{0.72 if tone!="plain" else 0.30:.2f}"/>')
        if s.get('note'):
            b.append(text(bx + bw + 10, y + bh / 2 + 4, s['note'], size=10.5, anchor='start',
                          tone=tone, op=0.85, weight='600'))
    h = top + len(bars) * (bh + gap) + 10
    if f.get('xlab'):
        b.append(cap(bx + bw / 2, h + 8, f['xlab'], op=0.6))
        h += 22
    if f.get('foot'):
        b.append(text(360, h + 10, f['foot'], size=10.5, op=0.6))
        h += 24
    return ''.join(b), h


def k_scatter(f):
    """Points in two groups plus optional boundary path. groups=[{pts,tone,label}]"""
    x0, x1 = f.get('xr', (0, 1))
    y0, y1 = f.get('yr', (0, 1))
    L, R = 78, 640
    T = 46 if f.get('head') else 28
    ph = f.get('ph', 200)
    bot = T + ph
    b = []
    if f.get('head'):
        b.append(cap(34, 20, f['head'][0], tone='sig', anchor='start', op=0.9, size=11))
        if len(f['head']) > 1:
            b.append(cap(686, 20, f['head'][1], tone='mem', anchor='end', op=0.85, size=11))

    def px(v): return L + (v - x0) / (x1 - x0) * (R - L)
    def py(v): return bot - (v - y0) / (y1 - y0) * ph

    b.append(line(L, bot, R, bot, sw=1.1, op=0.4))
    b.append(line(L, T, L, bot, sw=1.1, op=0.4))
    for g in f.get('regions', []):
        b.append(f'<rect x="{_f(px(g["x0"]))}" y="{_f(py(g["y1"]))}" '
                 f'width="{_f(px(g["x1"])-px(g["x0"]))}" height="{_f(py(g["y0"])-py(g["y1"]))}" '
                 f'fill="{_c(g.get("tone","mem"))}" opacity="{g.get("op",0.09):.2f}"/>')
    for g in f['groups']:
        for (a, c) in g['pts']:
            if g.get('hollow'):
                b.append(ring(px(a), py(c), r=g.get('r', 3.4), tone=g.get('tone', 'plain'), sw=1.3))
            else:
                b.append(dot(px(a), py(c), r=g.get('r', 3.4), tone=g.get('tone', 'plain'),
                             op=g.get('op', 0.85)))
        if g.get('label'):
            b.append(text(px(g['lx']), py(g['ly']), g['label'], size=10.5,
                          tone=g.get('tone', 'plain'), weight='600', op=0.95,
                          anchor=g.get('la', 'start')))
    for c in f.get('curves', []):
        d = 'M' + ' L'.join(f'{px(a):.1f} {py(bb):.1f}' for a, bb in c['pts'])
        b.append(path(d, tone=c.get('tone', 'sig'), sw=c.get('sw', 1.8), dash=c.get('dash')))
        if c.get('label'):
            lx_, ly_ = c['pts'][c.get('lat', -1)]
            b.append(text(px(lx_) + c.get('dx', 8), py(ly_) + c.get('dy', -6), c['label'],
                          size=10.5, tone=c.get('tone', 'sig'), weight='600',
                          anchor=c.get('la', 'start')))
    for gy, gl in f.get('yticks', []):
        b.append(text(L - 9, py(gy) + 3.5, gl, size=10, anchor='end', op=0.6))
    for gx, gl in f.get('xticks', []):
        b.append(text(px(gx), bot + 18, gl, size=10, op=0.6))
    if f.get('xlab'):
        b.append(cap(360, bot + 38, f['xlab'], op=0.6))
    if f.get('ylab'):
        b.append(cap(30, T + ph / 2, f['ylab'], op=0.6, rot=-90))
    h = bot + (52 if f.get('xlab') else 32)
    if f.get('foot'):
        b.append(text(360, h + 8, f['foot'], size=10.5, op=0.6))
        h += 24
    return ''.join(b), h


def k_stack(f):
    """A single horizontal budget bar split into segments. segs=[{t,v,tone}]"""
    segs = f['segs']
    tot = sum(s['v'] for s in segs)
    top = 46 if f.get('head') else 30
    bx, bw, bh = 34, W - 68, f.get('bh', 46)
    b = []
    if f.get('head'):
        b.append(cap(34, 20, f['head'][0], tone='sig', anchor='start', op=0.9, size=11))
        if len(f['head']) > 1:
            b.append(cap(686, 20, f['head'][1], tone='mem', anchor='end', op=0.85, size=11))
    x = bx
    labels = []
    for s in segs:
        w = s['v'] / tot * bw
        tone = s.get('tone', 'plain')
        b.append(f'<rect x="{_f(x)}" y="{_f(top)}" width="{_f(w)}" height="{_f(bh)}" '
                 f'fill="{_c(tone)}" opacity="{s.get("op", 0.68 if tone!="plain" else 0.22):.2f}"/>')
        b.append(f'<rect x="{_f(x)}" y="{_f(top)}" width="{_f(w)}" height="{_f(bh)}" '
                 f'fill="none" stroke="var(--surface)" stroke-width="1.5"/>')
        if w > 46:
            b.append(text(x + w / 2, top + bh / 2 + 4, s.get('inner', ''), size=11,
                          tone='plain', op=0.0))
        labels.append((x + w / 2, s['t'], s.get('sub'), tone, w))
        x += w
    ty = top + bh + 20
    alt = 0
    for (cx, t, sub, tone, w) in labels:
        yy = ty + (0 if w > 90 else (alt % 2) * 26)
        b.append(text(cx, yy, t, size=10.5, tone=tone, weight='600', op=0.95))
        if sub:
            b.append(text(cx, yy + 13, sub, size=9.5, tone=tone, op=0.6))
        if w <= 90:
            b.append(line(cx, top + bh + 2, cx, yy - 10, tone=tone, sw=1, op=0.35))
            alt += 1
    h = ty + 46
    if f.get('foot'):
        b.append(text(360, h, f['foot'], size=10.5, op=0.6))
        h += 22
    return ''.join(b), h


def k_blocks(f):
    """Free-form labelled boxes on a coarse grid, with connectors.
    boxes=[{x,y,w,h,t,sub,tone,fill}] in svg units; links=[{a,b,tone,label,dash,side}]
    a/b are indices into boxes."""
    boxes = f['boxes']
    b = []
    top = 0
    if f.get('head'):
        b.append(cap(34, 20, f['head'][0], tone='sig', anchor='start', op=0.9, size=11))
        if len(f['head']) > 1:
            b.append(cap(686, 20, f['head'][1], tone='mem', anchor='end', op=0.85, size=11))
    for lk in f.get('links', []):
        A, B = boxes[lk['a']], boxes[lk['b']]
        side = lk.get('side', 'auto')
        ax, ay = A['x'] + A['w'], A['y'] + A['h'] / 2
        bx_, by = B['x'], B['y'] + B['h'] / 2
        if side == 'down':
            ax, ay = A['x'] + A['w'] / 2, A['y'] + A['h']
            bx_, by = B['x'] + B['w'] / 2, B['y']
        elif side == 'up':
            ax, ay = A['x'] + A['w'] / 2, A['y']
            bx_, by = B['x'] + B['w'] / 2, B['y'] + B['h']
        elif side == 'left':
            ax, ay = A['x'], A['y'] + A['h'] / 2
            bx_, by = B['x'] + B['w'], B['y'] + B['h'] / 2
        b.append(line(ax, ay, bx_, by, tone=lk.get('tone', 'plain'), sw=1.3,
                      arrow=True, op=0.55, dash=lk.get('dash')))
        if lk.get('label'):
            b.append(text((ax + bx_) / 2, (ay + by) / 2 - 6, lk['label'], size=9.5,
                          tone=lk.get('tone', 'plain'), op=0.8, weight='600'))
    for bx0 in boxes:
        tone = bx0.get('tone', 'plain')
        b.append(rect(bx0['x'], bx0['y'], bx0['w'], bx0['h'], tone=tone,
                      fill=bx0.get('fill', tone in ('sig', 'mem')), op=0.14,
                      dash=bx0.get('dash')))
        lines = _wrap(bx0['t'], max(9, int(bx0['w'] / 7.2)))
        cy = bx0['y'] + bx0['h'] / 2 - (len(lines) - 1) * 7 - (5 if bx0.get('sub') else -1)
        for i, ln in enumerate(lines):
            b.append(text(bx0['x'] + bx0['w'] / 2, cy + i * 14, ln, size=11.5, tone=tone,
                          weight='600'))
        if bx0.get('sub'):
            b.append(text(bx0['x'] + bx0['w'] / 2, cy + len(lines) * 14 + 3, bx0['sub'],
                          size=9.5, tone=tone, op=0.62))
    for lb in f.get('labels', []):
        b.append(cap(lb['x'], lb['y'], lb['t'], tone=lb.get('tone', 'plain'),
                     anchor=lb.get('a', 'middle'), op=lb.get('op', 0.6)))
    h = f.get('h', max(bx0['y'] + bx0['h'] for bx0 in boxes) + 24)
    if f.get('foot'):
        b.append(text(360, h - 6, f['foot'], size=10.5, op=0.6))
    return ''.join(b), h


def k_tree(f):
    """A decision tree / hierarchy. nodes=[{id,x,y,t,sub,tone}], edges=[{a,b,label}]"""
    nodes = {n['id']: n for n in f['nodes']}
    b = []
    if f.get('head'):
        b.append(cap(34, 20, f['head'][0], tone='sig', anchor='start', op=0.9, size=11))
        if len(f['head']) > 1:
            b.append(cap(686, 20, f['head'][1], tone='mem', anchor='end', op=0.85, size=11))
    NW, NH = f.get('nw', 132), f.get('nh', 42)
    for e in f.get('edges', []):
        A, B = nodes[e['a']], nodes[e['b']]
        b.append(line(A['x'], A['y'] + NH / 2, B['x'], B['y'] - NH / 2,
                      tone=e.get('tone', 'plain'), sw=1.2, op=0.45, arrow=True,
                      dash=e.get('dash')))
        if e.get('label'):
            mx, my = (A['x'] + B['x']) / 2, (A['y'] + NH / 2 + B['y'] - NH / 2) / 2
            b.append(text(mx + e.get('dx', 0), my + 3, e['label'], size=9.5,
                          tone=e.get('tone', 'plain'), op=0.8, weight='600'))
    for n in f['nodes']:
        tone = n.get('tone', 'plain')
        w = n.get('w', NW)
        b.append(rect(n['x'] - w / 2, n['y'] - NH / 2, w, NH, tone=tone,
                      fill=tone in ('sig', 'mem'), op=0.14))
        b.append(text(n['x'], n['y'] + (0 if not n.get('sub') else -4), n['t'], size=11.5,
                      tone=tone, weight='600'))
        if n.get('sub'):
            b.append(text(n['x'], n['y'] + 11, n['sub'], size=9.5, tone=tone, op=0.62))
    h = f.get('h', max(n['y'] for n in f['nodes']) + NH / 2 + 26)
    if f.get('foot'):
        b.append(text(360, h - 8, f['foot'], size=10.5, op=0.6))
    return ''.join(b), h


def k_loop(f):
    """A cycle of boxes with a return arrow. steps=[{t,sub,tone}]"""
    steps = f['steps']
    n = len(steps)
    top = 46 if f.get('head') else 30
    bh = 56
    gap = 22
    bw = (W - 68 - gap * (n - 1)) / n
    y = top
    b = []
    if f.get('head'):
        b.append(cap(34, 20, f['head'][0], tone='sig', anchor='start', op=0.9, size=11))
        if len(f['head']) > 1:
            b.append(cap(686, 20, f['head'][1], tone='mem', anchor='end', op=0.85, size=11))
    for i, s in enumerate(steps):
        x = 34 + i * (bw + gap)
        tone = s.get('tone', 'plain')
        b.append(rect(x, y, bw, bh, tone=tone, fill=tone in ('sig', 'mem'), op=0.14))
        lines = _wrap(s['t'], max(9, int(bw / 7.2)))
        cy = y + bh / 2 - (len(lines) - 1) * 7 - (5 if s.get('sub') else -1)
        for j, ln in enumerate(lines):
            b.append(text(x + bw / 2, cy + j * 14, ln, size=11.5, tone=tone, weight='600'))
        if s.get('sub'):
            b.append(text(x + bw / 2, cy + len(lines) * 14 + 3, s['sub'], size=9.5,
                          tone=tone, op=0.62))
        if i < n - 1:
            b.append(line(x + bw + 4, y + bh / 2, x + bw + gap - 7, y + bh / 2,
                          sw=1.3, arrow=True, op=0.55))
    ry = y + bh + 30
    lx_, rx = 34 + bw / 2, 34 + (n - 1) * (bw + gap) + bw / 2
    d = (f'M{rx:.1f} {y+bh:.1f} L{rx:.1f} {ry:.1f} L{lx_:.1f} {ry:.1f} L{lx_:.1f} {y+bh+7:.1f}')
    b.append(f'<path d="{d}" fill="none" stroke="{_c(f.get("loop_tone","mem"))}" '
             f'stroke-width="1.3" opacity="0.55" stroke-dasharray="5 4" '
             f'marker-end="url(#ar-{ {"sig":"sig","mem":"mem"}.get(f.get("loop_tone","mem"),"fg") })"/>')
    if f.get('loop_label'):
        b.append(text(360, ry - 7, f['loop_label'], size=10.5,
                      tone=f.get('loop_tone', 'mem'), weight='600', op=0.9))
    h = ry + 26
    if f.get('foot'):
        b.append(text(360, h - 4, f['foot'], size=10.5, op=0.6))
        h += 12
    return ''.join(b), h


def k_compare(f):
    """Two labelled columns side by side, each with a small nested figure."""
    left, right = f['left'], f['right']
    b = []
    b.append(cap(190, 20, left['t'], tone=left.get('tone', 'sig'), op=0.9, size=11))
    b.append(cap(530, 20, right['t'], tone=right.get('tone', 'mem'), op=0.9, size=11))
    b.append(line(360, 32, 360, f.get('h', 240) - 26, dash='4 5', sw=1, op=0.25))
    h = 40
    for side, xoff, spec in ((left, 0, left), (right, 360, right)):
        for i, ln in enumerate(spec.get('lines', [])):
            b.append(text(xoff + 180, 52 + i * 22, ln, size=11.5,
                          tone=spec.get('tone', 'plain'), op=0.9 if i == 0 else 0.7,
                          weight='600' if i == 0 else '400'))
        h = max(h, 52 + len(spec.get('lines', [])) * 22 + 16)
    if f.get('foot'):
        b.append(text(360, h + 8, f['foot'], size=10.5, op=0.6))
        h += 26
    return ''.join(b), h


def k_panels(f):
    """Two or three nested figures side by side, each with a caption."""
    ps = f['panels']
    n = len(ps)
    b = []
    inner_w = W
    scale = (W - 68 - 22 * (n - 1)) / n / W
    y0 = 40 if f.get('head') else 22
    if f.get('head'):
        b.append(cap(34, 20, f['head'][0], tone='sig', anchor='start', op=0.9, size=11))
        if len(f['head']) > 1:
            b.append(cap(686, 20, f['head'][1], tone='mem', anchor='end', op=0.85, size=11))
    hmax = 0
    for i, p in enumerate(ps):
        body, ph = render_body(p['fig'])
        x = 34 + i * ((W - 68 - 22 * (n - 1)) / n + 22)
        b.append(f'<g transform="translate({x:.1f} {y0:.1f}) scale({scale:.4f})">{body}</g>')
        hh = ph * scale
        b.append(text(x + (W - 68 - 22 * (n - 1)) / n / 2, y0 + hh + 16, p['t'], size=11,
                      tone=p.get('tone', 'plain'), weight='600', op=0.9))
        if p.get('sub'):
            b.append(text(x + (W - 68 - 22 * (n - 1)) / n / 2, y0 + hh + 31, p['sub'],
                          size=9.5, tone=p.get('tone', 'plain'), op=0.62))
        hmax = max(hmax, hh + (46 if p.get('sub') else 30))
    h = y0 + hmax + 10
    if f.get('foot'):
        b.append(text(360, h, f['foot'], size=10.5, op=0.6))
        h += 22
    return ''.join(b), h


KINDS = {
    'pipeline': k_pipeline, 'grid': k_grid, 'plot': k_plot, 'bars': k_bars,
    'scatter': k_scatter, 'stack': k_stack, 'blocks': k_blocks, 'tree': k_tree,
    'loop': k_loop, 'compare': k_compare, 'panels': k_panels,
}


def render_body(f):
    kind = f['kind']
    if kind not in KINDS:
        raise ValueError(f'unknown figure kind: {kind}')
    return KINDS[kind](f)


def render(f):
    body, h = render_body(f)
    return svg(body, h, f.get('alt', 'diagram'))
