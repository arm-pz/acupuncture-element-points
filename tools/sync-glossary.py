#!/usr/bin/env python3
"""Inline tools/glossary-snippet.html into every page that uses glossary tooltips.

Pages stay self-contained, so the snippet is copied in rather than linked.
Run after editing the snippet:  python3 tools/sync-glossary.py
Each page then calls ShuGloss.watch(...) in its own <script> after the snippet.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SNIP = (ROOT / 'tools' / 'glossary-snippet.html').read_text(encoding='utf-8').strip()
PAGES = ['learn.html', 'study.html', 'lung-meridian-chart.html'] + sorted(p.name for p in ROOT.glob('*-v4-meridian-chart.html'))
BLOCK = re.compile(r'<!-- gloss:start.*?<!-- gloss:end -->', re.S)

changed = 0
for name in PAGES:
    path = ROOT / name
    s = path.read_text(encoding='utf-8')
    if BLOCK.search(s):
        new = BLOCK.sub(lambda m: SNIP, s, count=1)
    else:
        sys.exit(f'{name}: no gloss markers; add the snippet once by hand before </body>')
    if new != s:
        path.write_text(new, encoding='utf-8'); changed += 1
print(f'{changed} page(s) updated')
