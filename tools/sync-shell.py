#!/usr/bin/env python3
"""Copy tools/shell-snippet.html (the app header, the scene backdrop and the view router) into the three app pages.

Elements, Channels and Points are views of one app: whichever of them loads first keeps running and swaps the
other two in without a page load. Pages stay self-contained, so the shell is copied into each. The copy differs
only in which page it names as its own (data-view, data-page and aria-current).
    python3 tools/sync-shell.py           # rewrite the shell blocks
    python3 tools/sync-shell.py --check   # report pages that are out of date, change nothing
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SNIP = (ROOT / 'tools' / 'shell-snippet.html').read_text(encoding='utf-8').strip()
PAGES = {'index': 'index.html', 'channels': 'channels.html', 'points': 'points.html'}
BLOCK = re.compile(r'<!-- shell:start.*?<!-- shell:end -->', re.S)
check = '--check' in sys.argv
stale = []
for key, name in PAGES.items():
    block = (SNIP.replace('data-view="index"', f'data-view="{key}"')
                 .replace('data-page="index"', f'data-page="{key}"')
                 .replace(f'<a class="l" href="{name}">', f'<a class="l" href="{name}" aria-current="page">'))
    p = ROOT / name
    s = p.read_text(encoding='utf-8')
    if not BLOCK.search(s):
        sys.exit(f'{name}: no shell block; add "<!-- shell:start --><!-- shell:end -->" where the header belongs')
    new = BLOCK.sub(lambda m: block, s, count=1)
    if new != s:
        stale.append(name)
        if not check:
            p.write_text(new, encoding='utf-8')
if check:
    if stale:
        sys.exit('out of date: ' + ', '.join(stale) + ' (run python3 tools/sync-shell.py)')
    print('shell blocks are up to date')
else:
    print(f'{len(stale)} page(s) updated')
