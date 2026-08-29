#!/usr/bin/env python3
"""Schema validator. Run before build; run again on the built HTML.

The rules exist because each of them has already cost a rebuild:
  - the simple layer must contain NO math notation at all, or the switch
    is decoration
  - a drill answer must open with a bolded verdict, or it reads as an essay
  - a bare & breaks XML well-formedness inside a figure
  - '&mdash\;' (backslash before the semicolon) is not fixable with sed
"""
import sys, os, re, importlib.util, xml.etree.ElementTree as ET
import os as _os
ROOT = _os.path.dirname(_os.path.abspath(__file__))

sys.path.insert(0, ROOT)
from gpkit import figkit

REQ = ['id', 'tier', 'title', 'kicker', 'simple', 'analogy', 'tech', 'fig',
       'caption', 'when', 'trap', 'real', 'drills', 'anchor', 'chips', 'followup']
TIERS = {'foundation', 'core', 'advanced', 'production'}

# notation that must never appear in the simple layer
MATHY = re.compile(r'[$\\^_×÷≈≥≤≠∑∏∫√±∞θμσλβαπΣΔ∈∀∃⊕⊗]|\b[A-Za-z]\s*=\s*[^ ]|\bP\(|\bE\[|\blog\b|\bsqrt\b|O\(')
ENT_BUG = re.compile(r'&[a-zA-Z]+\\;')   # a LITERAL backslash before the semicolon
BARE_AMP = re.compile(r'&(?!#?\w+;)')
KEBAB = re.compile(r'^[a-z0-9]+(-[a-z0-9]+)*$')
# katexify pairs $ ... $ on a line. A stray currency sign therefore pairs with
# the next one and renders the PROSE BETWEEN THEM as math -- silently, because
# the result is often valid TeX. Two tells: an odd number of $ in a field, and
# an extracted span that reads like a sentence rather than an expression.
INLINE_SPAN = re.compile(r'(?<!\$)\$([^$\n]+?)\$(?!\$)')
WORDY = re.compile(r'\b[A-Za-z]{3,}\b')
TEXY = re.compile(r'[\\^_{}=<>+]|\\times|\\frac')


def math_smells_like_prose(s):
    """True when a $...$ span is probably two currency signs that found each other."""
    for m in INLINE_SPAN.finditer(s):
        span = m.group(1)
        if TEXY.search(span):
            continue
        if len(WORDY.findall(span)) >= 4:
            return span
    return None


def texts(v, out):
    if isinstance(v, str):
        out.append(v)
    elif isinstance(v, dict):
        for k, x in v.items():
            texts(x, out)
    elif isinstance(v, (list, tuple)):
        for x in v:
            texts(x, out)
    return out


def flat(v):
    return ' '.join(v) if isinstance(v, (list, tuple)) else str(v)


def check_card(c, errs, warns, seen):
    cid = c.get('id', '?')

    def e(m):
        errs.append(f'[{cid}] {m}')

    def w(m):
        warns.append(f'[{cid}] {m}')

    for f in REQ:
        if f not in c or c[f] in (None, '', [], {}):
            e(f'missing required field: {f}')
    if not KEBAB.match(cid):
        e('id is not kebab-case')
    if cid in seen:
        e('duplicate id')
    seen.add(cid)
    if c.get('tier') not in TIERS:
        e(f'bad tier: {c.get("tier")}')

    # --- the simple layer must be genuinely simple
    for field in ('simple', 'analogy', 'simple_extra', 'trap_simple'):
        if c.get(field):
            s = flat(c[field])
            m = MATHY.search(s)
            if m:
                e(f'{field} contains math notation: ...{s[max(0,m.start()-40):m.start()+30]}...')
    fs = c.get('anchor', {}).get('formula_simple')
    if fs and MATHY.search(fs):
        e('anchor.formula_simple contains math notation')

    # --- drills
    ds = c.get('drills', [])
    if len(ds) != 3:
        e(f'expected exactly 3 drills, found {len(ds)}')
    for i, d in enumerate(ds):
        for k in ('q', 'a', 'a_simple'):
            if not d.get(k):
                e(f'drill {i+1} missing {k}')
        if d.get('a') and not d['a'].lstrip().startswith('<b>'):
            e(f'drill {i+1} technical answer does not open with a bolded verdict')
        if d.get('a_simple'):
            if not d['a_simple'].lstrip().startswith('<b>'):
                e(f'drill {i+1} simple answer does not open with a bolded verdict')
            m = MATHY.search(d['a_simple'])
            if m:
                e(f'drill {i+1} simple answer contains math notation: '
                  f'...{d["a_simple"][max(0,m.start()-40):m.start()+30]}...')

    # --- the anchor
    a = c.get('anchor', {})
    if not a.get('formula'):
        e('anchor.formula missing')
    if len(a.get('bullets', [])) < 2:
        e('anchor needs at least 2 bullets')

    if len(c.get('when', [])) < 3:
        w('fewer than 3 "you reach for it when" bullets')
    if len(c.get('chips', [])) < 3:
        w('fewer than 3 unlock chips')

    # --- entity hygiene, everywhere
    for s in texts(c, []):
        if ENT_BUG.search(s):
            e(r'HTML entity written as &name\; -- fix in python with .replace("\;",";")')
        if s.count('$') % 2:
            e(f'unbalanced $ in a field -- katexify will pair it with the next one: '
              f'...{s[:90]}...')
        bad = math_smells_like_prose(s)
        if bad:
            e(f'a $...$ span reads as prose, not math -- write currency as &#36;: '
              f'...{bad[:70]}...')
        for m in BARE_AMP.finditer(s):
            frag = s[max(0, m.start() - 30):m.start() + 30]
            if '$' in frag:
                continue
            e(f'bare & (write &amp;): ...{frag}...')

    # --- the figure has to render and be well-formed
    if c.get('fig'):
        try:
            svg = figkit.render(c['fig'])
            ET.fromstring(svg)
        except Exception as ex:
            e(f'figure failed: {type(ex).__name__}: {ex}')

    # --- production-quality content rules
    if c.get('real') and re.search(r'used in (ML|AI|many) applications', c['real'], re.I):
        e('real-world block is generic filler')
    if c.get('real') and not re.search(r'\d', c.get('real', '')):
        w('real-world block carries no number')


def load(folder):
    cards = []
    d = os.path.join(ROOT, 'content', folder)
    for fn in sorted(os.listdir(d)):
        if not fn.endswith('.py'):
            continue
        spec = importlib.util.spec_from_file_location(fn[:-3], os.path.join(d, fn))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        cards += m.CARDS
    return cards


def main():
    folder = sys.argv[1]
    cards = load(folder)
    errs, warns, seen = [], [], set()
    for c in cards:
        check_card(c, errs, warns, seen)
    order = ['foundation', 'core', 'advanced', 'production']
    idx = [order.index(c['tier']) for c in cards if c['tier'] in order]
    if idx != sorted(idx):
        errs.append('cards are not in tier order foundation -> core -> advanced -> production')
    print(f'{len(cards)} cards  |  {len(errs)} errors  |  {len(warns)} warnings')
    for x in warns:
        print('  warn ', x)
    for x in errs:
        print('  ERROR', x)
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())
