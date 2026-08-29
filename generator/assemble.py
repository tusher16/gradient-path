#!/usr/bin/env python3
"""assemble.py <content-folder> <config-module> <out.html>"""
import sys, os, importlib.util
import os as _os
ROOT = _os.path.dirname(_os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from gpkit import build
from check import load, check_card

folder, cfgmod, out = sys.argv[1], sys.argv[2], sys.argv[3]
cards = load(folder)

errs, warns, seen = [], [], set()
for c in cards:
    check_card(c, errs, warns, seen)
if errs:
    print(f'{len(errs)} schema errors -- refusing to build')
    for e in errs[:60]:
        print('  ', e)
    sys.exit(1)

spec = importlib.util.spec_from_file_location('cfg', os.path.join(ROOT, cfgmod))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

html = build.page(cards, m.CFG)
import re as _re
# The entity bug -- an agent writing &mdash\; -- but ONLY where \; terminates an
# entity name. A blanket replace also eats LaTeX's \; thin space inside math.
html = _re.sub(r'&([a-zA-Z]+)\\;', r'&\1;', html)
open(out, 'w').write(html)
print(f'wrote {out}  {len(cards)} cards  {len(html)/1e6:.2f} MB')
