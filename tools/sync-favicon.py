#!/usr/bin/env python3
"""Embed favicon.svg (the yin-yang mark) as the browser-tab icon in every page.

Pages stay self-contained, so the icon is inlined as a data URI between markers. Replaces any
existing <link rel="icon"> on first run.
    python3 tools/sync-favicon.py
"""
import pathlib, re, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
svg = (ROOT / 'favicon.svg').read_text(encoding='utf-8').strip()
uri = 'data:image/svg+xml,' + urllib.parse.quote(svg, safe="/:=' ")
uri = uri.replace(' ', '%20').replace('"', "'")
TAG = f'<!-- favicon:start --><link rel="icon" type="image/svg+xml" href="{uri}"><!-- favicon:end -->'
BLOCK = re.compile(r'<!-- favicon:start -->.*?<!-- favicon:end -->', re.S)
OLD = re.compile(r'<link rel="icon"[^>]*>')
changed = 0
for p in sorted(ROOT.glob('*.html')):
    s = p.read_text(encoding='utf-8')
    if BLOCK.search(s):
        new = BLOCK.sub(lambda m: TAG, s, count=1)
    else:
        s2 = OLD.sub('', s)
        if '</head>' in s2:
            i = s2.index('</head>')
        else:  # index.html is a head-less fragment: put the icon after <title>
            i = s2.index('</title>') + len('</title>')
        new = s2[:i] + TAG + s2[i:]
    if new != s:
        p.write_text(new, encoding='utf-8'); changed += 1
print(f'{changed} page(s) updated')
