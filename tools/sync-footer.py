#!/usr/bin/env python3
"""Copy tools/footer-snippet.html (Caffeinity wordmark and philosophy) into every scrolling page.

Pages stay self-contained. Inserts the footer before </body> on first run, then replaces it between
the footer markers. The home page is a one-screen stage and has no footer.
    python3 tools/sync-footer.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SNIP = (ROOT / 'tools' / 'footer-snippet.html').read_text(encoding='utf-8').strip()
PAGES = ['channels.html', 'points.html', 'learn.html', 'study.html'] + sorted(p.name for p in ROOT.glob('*meridian-chart.html'))
BLOCK = re.compile(r'<!-- footer:start.*?<!-- footer:end -->', re.S)
changed = 0
for name in PAGES:
    p = ROOT / name
    s = p.read_text(encoding='utf-8')
    if BLOCK.search(s):
        new = BLOCK.sub(lambda m: SNIP, s, count=1)
    else:
        i = s.rindex('</body>')
        new = s[:i] + SNIP + '\n' + s[i:]
    if new != s:
        p.write_text(new, encoding='utf-8'); changed += 1
print(f'{changed} page(s) updated')
