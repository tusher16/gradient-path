#!/usr/bin/env python3
"""Validate ONE card file in isolation: python3 checkfile.py <path.py>"""
import sys, importlib.util
import os as _os
ROOT = _os.path.dirname(_os.path.abspath(__file__))
sys.path.insert(0, ROOT)
from check import check_card

p = sys.argv[1]
spec = importlib.util.spec_from_file_location('m', p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
errs, warns, seen = [], [], set()
for c in m.CARDS:
    check_card(c, errs, warns, seen)
print(f'{p}: {len(m.CARDS)} cards | {len(errs)} errors | {len(warns)} warnings')
for x in warns: print('  warn ', x)
for x in errs:  print('  ERROR', x)
sys.exit(1 if errs else 0)
