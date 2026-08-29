"""Renders card dicts into the Gradient Path page shell.

The two-layer contract
----------------------
Simple mode is not a swapped paragraph. Everything marked .tech-only is
absent from the flow in simple mode: the math slab, the code block, the
interview-grade drill answers and the technical trap. Simple mode carries
its own equivalents so the card still ends in a decision -- it is a
different card, not a truncated one.
"""
import os, re, json, html
from . import figkit, prompts

HERE = os.path.dirname(__file__)
# a path curving from signal pink up into memory teal -- inline, so the page
# still has zero image requests
FAVICON = ('data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2032%2032%22%3E%3Cdefs%3E%3ClinearGradient%20id%3D%22g%22%20x1%3D%220%22%20y1%3D%221%22%20x2%3D%221%22%20y2%3D%220%22%3E%3Cstop%20offset%3D%220%22%20stop-color%3D%22%23C11E5C%22%2F%3E%3Cstop%20offset%3D%221%22%20stop-color%3D%22%230C7A70%22%2F%3E%3C%2FlinearGradient%3E%3C%2Fdefs%3E%3Crect%20width%3D%2232%22%20height%3D%2232%22%20rx%3D%227%22%20fill%3D%22%23131C1A%22%2F%3E%3Cpath%20d%3D%22M8%2025C8%2015%2024%2017%2024%207%22%20fill%3D%22none%22%20stroke%3D%22url%28%23g%29%22%20stroke-width%3D%224.5%22%20stroke-linecap%3D%22round%22%2F%3E%3C%2Fsvg%3E')

TIER_CLASS = {'foundation': 't-foundation', 'core': 't-core',
              'advanced': 't-advanced', 'production': 't-production'}


def _p(s, cls='prose'):
    return f'<p class="{cls}">{s}</p>'


def _paras(s, cls='prose'):
    """A field may be one string or a list of paragraphs."""
    if isinstance(s, (list, tuple)):
        return ''.join(_p(x, cls) for x in s)
    return _p(s, cls)


def _lbl(t, cost=None):
    c = f' <span class="cost">{cost}</span>' if cost else ''
    return f'<h3 class="lbl">{t}{c}</h3>'


# ------------------------------------------------------------------ blocks
def fig_block(c):
    if not c.get('fig'):
        return ''
    svg = figkit.render(c['fig'])
    cap_t = c.get('caption', '')
    cap_s = c.get('caption_simple') or cap_t
    swipe = ' <span class="swipe">Swipe the picture sideways to see all of it.</span>'
    caps = f'<figcaption class="simple-only">{cap_s}{swipe}</figcaption>'
    capt = f'<figcaption class="tech-only">{cap_t}{swipe}</figcaption>'
    if cap_s == cap_t:
        caps, capt = f'<figcaption>{cap_t}{swipe}</figcaption>', ''
    return f'<figure class="fig"><div class="fig-scroll">{svg}</div>{caps}{capt}</figure>'


def say_block(c):
    simple = _paras(c['simple'], 'prose lede')
    if c.get('analogy'):
        simple += _p(c['analogy'], 'prose analogy')
    if c.get('simple_extra'):
        simple += _paras(c['simple_extra'], 'prose sm')
    tech = _paras(c['tech'], 'prose lede')
    if c.get('tech_note'):
        tech += _paras(c['tech_note'], 'prose sm')
    return (f'<div class="say"><div class="say-simple simple-only">{simple}</div>'
            f'<div class="say-tech tech-only">{tech}</div></div>')


def when_trap(c):
    when = ''.join(f'<li>{x}</li>' for x in c['when'])
    trap_t = c['trap']
    trap_s = c.get('trap_simple') or trap_t
    tr = (f'<p class="prose sm trap simple-only">{trap_s}</p>'
          f'<p class="prose sm trap tech-only">{trap_t}</p>')
    if trap_s == trap_t:
        tr = f'<p class="prose sm trap">{trap_t}</p>'
    return ('<div class="split">'
            f'<section class="blk">{_lbl(c.get("when_label","You reach for it when"))}'
            f'<ul class="when">{when}</ul></section>'
            f'<section class="blk">{_lbl("The trap")}{tr}</section></div>')


def nums_block(c):
    if not c.get('nums'):
        return ''
    li = ''.join(
        f'<li><span class="n-k">{n["k"]}</span><span class="n-v">{n["v"]}</span>'
        f'<span class="n-s">{n["s"]}</span></li>' for n in c['nums'])
    return (f'<section class="blk">{_lbl(c.get("nums_label","The numbers you say out loud"))}'
            f'<ul class="nums">{li}</ul></section>')


def ask_block(c):
    if not c.get('ask'):
        return ''
    li = ''.join(f'<li><q>{a["q"]}</q><span>{a["a"]}</span></li>' for a in c['ask'])
    return (f'<section class="blk">{_lbl("Ask these before you draw anything", c.get("ask_cost"))}'
            f'<ul class="ask">{li}</ul></section>')


def estimate_block(c):
    if not c.get('estimate'):
        return ''
    e = c['estimate']
    rows = ''.join(
        f'<tr class="{"tot" if r.get("tot") else ""}"><td class="e-l">{r["l"]}</td>'
        f'<td class="e-w">{r.get("w","")}</td><td class="e-r">{r["r"]}</td></tr>'
        for r in e['rows'])
    note = f'<p class="prose sm">{e["note"]}</p>' if e.get('note') else ''
    return (f'<section class="blk">{_lbl(e.get("label","The arithmetic, out loud"), e.get("cost"))}'
            f'<div class="estimate"><table>{rows}</table></div>{note}</section>')


def tradeoff_block(c):
    if not c.get('tradeoffs'):
        return ''
    li = ''.join(f'<li><span class="t-k">{t["k"]}</span><span class="t-v">{t["v"]}</span></li>'
                 for t in c['tradeoffs'])
    return (f'<section class="blk">{_lbl(c.get("tradeoff_label","The tradeoffs, and what you say")) }'
            f'<ul class="tradeoffs">{li}</ul></section>')


def math_block(c):
    if not c.get('math'):
        return ''
    m = c['math']
    note = f'<span class="note">{m["note"]}</span>' if m.get('note') else ''
    return (f'<section class="blk tech-only">{_lbl("The math", m.get("cost"))}'
            f'<div class="slab">$${m["tex"]}$${note}</div></section>')


def code_block(c):
    if not c.get('code'):
        return ''
    k = c['code']
    return (f'<section class="blk tech-only">{_lbl(k.get("label","In code"), k.get("cost"))}'
            f'<div class="codewrap"><pre><code>{k["src"]}</code></pre></div></section>')


def real_block(c):
    return (f'<section class="blk">{_lbl(c.get("real_label","Where this bites in production"))}'
            f'<p class="prose sm real">{c["real"]}</p></section>')


def drill_block(c):
    ds = c['drills']
    out = []
    for i, d in enumerate(ds):
        a_t = f'<div class="ans ans-tech tech-only">{d["a"]}</div>'
        a_s = f'<div class="ans ans-simple simple-only">{d["a_simple"]}</div>'
        out.append(f'<details><summary data-q="{i+1}">{d["q"]}</summary>{a_s}{a_t}</details>')
    return (f'<section class="blk">{_lbl("Interview drill", f"{len(ds)} questions &middot; click to reveal")}'
            f'<div class="drill">{"".join(out)}</div></section>')


def verdict_block(c):
    if not c.get('verdict'):
        return ''
    v = c['verdict']
    return (f'<section class="blk">{_lbl("No-hire answer vs strong answer")}'
            f'<div class="verdicts"><div class="vno"><h4>No hire</h4><p>{v["no"]}</p></div>'
            f'<div class="vyes"><h4>Strong</h4><p>{v["yes"]}</p></div></div></section>')


def anchor_block(c):
    a = c['anchor']
    bl = ''.join(f'<li>{x}</li>' for x in a['bullets'])
    f_t = f'<div class="anchor-formula tech-only">{a["formula"]}</div>'
    f_s = f'<div class="anchor-formula anchor-plain simple-only">{a.get("formula_simple", a["formula"])}</div>'
    return (f'<section class="anchor">{_lbl("Say this back tomorrow")}{f_s}{f_t}'
            f'<ul>{bl}</ul></section>')


def chips_block(c):
    li = ''.join(f'<li>{x}</li>' for x in c['chips'])
    return f'<section class="blk">{_lbl("Unlocks")}<ul class="chips">{li}</ul></section>'


def upshift_block(c):
    """Simple mode only: name exactly what is being withheld and hand over
    the one control that reveals it. Without this the switch is invisible."""
    got = []
    if c.get('math'):
        got.append('the formula')
    if c.get('code'):
        got.append('the code')
    got.append('the interview-grade answers')
    if len(got) > 1:
        listed = ', '.join(got[:-1]) + ' and ' + got[-1]
    else:
        listed = got[0]
    return ('<div class="upshift simple-only">'
            f'<p>You are reading the plain version. <b>{listed[0].upper()+listed[1:]}</b> '
            'are one switch away, on this same card.</p>'
            '<button type="button" class="tolevel" data-to="tech">Show the precise version</button>'
            '</div>')


def practice_block(c, cfg, nxt):
    p = prompts.topic_prompt(c, cfg, nxt)
    pid = 'p-' + c['id']
    return ('<section class="practice"><div class="practice-head">'
            f'{_lbl("Practise anywhere, with any chatbot")}'
            f'<button type="button" class="copy" data-target="{pid}">Copy the prompt</button></div>'
            '<p class="prose sm">Paste this into ChatGPT, Gemini or Claude. It teaches the concept, '
            'makes you say it back before it moves on, walks the examples, then quizzes you one '
            'question at a time and scores you.</p>'
            '<details><summary>Read it first</summary>'
            f'<pre class="prompt" id="{pid}">{html.escape(p)}</pre></details></section>')


def status_block(c):
    return (f'<div class="statusbar" data-for="{c["id"]}"><span class="lbl">Tonight I feel</span>'
            '<button type="button" data-s="new">New to me</button>'
            '<button type="button" data-s="fuzzy">Fuzzy</button>'
            '<button type="button" data-s="solid">Solid</button></div>')


def card_html(c, n, cfg, nxt):
    tc = TIER_CLASS[c['tier']]
    parts = [
        f'<header class="card-head"><p class="eyebrow"><span class="num">{n:02d}</span>'
        f'<span class="tier {tc}">{c["tier"]}</span></p><h2>{c["title"]}</h2>'
        f'<p class="kicker">{c["kicker"]}</p></header>',
        say_block(c),
        fig_block(c),
        ask_block(c),
        nums_block(c),
        when_trap(c),
        estimate_block(c),
        math_block(c),
        code_block(c),
        tradeoff_block(c),
        real_block(c),
        drill_block(c),
        verdict_block(c),
        anchor_block(c),
        chips_block(c),
        upshift_block(c),
        practice_block(c, cfg, nxt),
        status_block(c),
    ]
    return f'<article class="card" id="{c["id"]}">' + ''.join(parts) + '</article>'


def tierhead_html(key, cards, cfg):
    t = cfg['tiers'][key]
    p = prompts.tier_prompt(key, cards, cfg)
    pid = f'p-tier-{key}'
    return (f'<section class="tierhead" id="tier-{key}">'
            f'<p class="eyebrow"><span class="tier {TIER_CLASS[key]}">{t["name"].upper()}</span> '
            f'&middot; {len(cards)} topics</p><h2>{t["title"]}</h2>'
            f'<p class="prose">{t["blurb"]}</p>'
            '<div class="practice" style="background:var(--surface)"><div class="practice-head">'
            f'{_lbl("Practise this whole block with a chatbot")}'
            f'<button type="button" class="copy" data-target="{pid}">Copy the block prompt</button></div>'
            '<p class="prose sm">One prompt for every topic in this block, in order. Good for a '
            'commute or a long queue &mdash; say "continue" next time and it picks up where you '
            'stopped.</p><details><summary>Read it first</summary>'
            f'<pre class="prompt" id="{pid}">{html.escape(p)}</pre></details></div></section>')


def rail_html(cards, cfg):
    out = []
    seen = None
    for i, c in enumerate(cards):
        if c['tier'] != seen:
            seen = c['tier']
            out.append(f'<li class="rail-tier">{cfg["tiers"][seen]["name"]}</li>')
        out.append(f'<li><a href="#{c["id"]}" data-rail="{c["id"]}"><span class="dot"></span>'
                   f'<span class="rn">{i+1:02d}</span><span class="rt">{c["title"]}</span></a></li>')
    mode = ('<div class="rail-mode"><h2 class="lbl">Reading at</h2>'
            '<div class="modeswitch" role="group" aria-label="Explanation depth">'
            '<button type="button" data-mode="simple" aria-pressed="true">Simple</button>'
            '<button type="button" data-mode="tech" aria-pressed="false">Technical</button></div>'
            '<span class="depth" id="depth"></span></div>')
    return (f'<nav class="rail" aria-label="All topics">{mode}<ul>{"".join(out)}</ul></nav>')


ARROW_DEFS = """
<svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute;color:var(--ink)">
 <defs>
  <marker id="ar-fg" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto">
    <path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker>
  <marker id="ar-sig" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto">
    <path d="M0 0 L10 5 L0 10 z" fill="var(--signal)"/></marker>
  <marker id="ar-mem" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto">
    <path d="M0 0 L10 5 L0 10 z" fill="var(--memory)"/></marker>
 </defs>
</svg>
"""


def page(cards, cfg):
    katex_css = open(os.path.join(HERE, 'katex.css')).read()
    page_css = open(os.path.join(HERE, 'page.css')).read()
    js = open(os.path.join(HERE, 'page.js')).read()
    js = js.replace('__IDS__', json.dumps([c['id'] for c in cards]))
    js = js.replace('__KEY__', cfg['key'])

    order = ['foundation', 'core', 'advanced', 'production']
    body = []
    n = 0
    for tk in order:
        group = [c for c in cards if c['tier'] == tk]
        if not group:
            continue
        body.append(tierhead_html(tk, group, cfg))
        for c in group:
            n += 1
            i = cards.index(c)
            nxt = cards[i + 1]['title'] if i + 1 < len(cards) else None
            body.append(card_html(c, n, cfg, nxt))

    return (
        "<!doctype html><html lang=\"en\"><head><meta charset='utf-8'>\n"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>\n"
        f"<title>{cfg['title']}</title>\n"
        '<link rel="icon" href="' + FAVICON + '">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:'
        'opsz,wght@12..96,500;12..96,700;12..96,800&family=IBM+Plex+Mono:wght@400;600;700&'
        'family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap">\n'
        f'<style>{katex_css}</style>\n<style>{page_css}</style></head><body>\n'
        + ARROW_DEFS +
        '<div class="top"><div class="top-in">'
        '<a class="backlink" href="index.html">&larr; Gradient Path</a>'
        f'<div class="masthead"><div><p class="eyebrow">Module {cfg["num"]} &middot; Nightly review</p>'
        f'<h1>{cfg["h1"]}</h1><p class="deck">{cfg["deck"]}</p></div>'
        '<aside class="howto"><h2 class="lbl">Ten minutes before bed</h2><ol>'
        + ''.join(f'<li>{x}</li>' for x in cfg['howto']) +
        '</ol></aside></div>'
        '<div class="legend">'
        f'<p><span class="swatch sw-sig"></span><span><b class="sig-t">Pink</b> &mdash; {cfg["legend_sig"]}</span></p>'
        f'<p><span class="swatch sw-mem"></span><span><b class="mem-t">Teal</b> &mdash; {cfg["legend_mem"]}</span></p>'
        '</div>'
        '<div class="controls"><div class="modeswitch" role="group" aria-label="Explanation depth">'
        '<button type="button" data-mode="simple" aria-pressed="true">Explain simply</button>'
        '<button type="button" data-mode="tech" aria-pressed="false">Full technical</button></div>'
        '<button class="btn" type="button" id="pick">Pick tonight&rsquo;s topic</button>'
        '<button class="btn ghost" type="button" id="theme">Dark / light</button>'
        f'<span class="meter" id="meter">0 of {len(cards)} solid</span></div>'
        '</div></div>'
        '<div class="shell">' + rail_html(cards, cfg) +
        '<main class="stack">' + ''.join(body) + '</main></div>'
        f'<footer class="foot"><p>{cfg["footer"]}</p>'
        '<p><a href="index.html">&larr; Back to Gradient Path</a></p></footer>'
        f'<script>{js}</script></body></html>'
    )
