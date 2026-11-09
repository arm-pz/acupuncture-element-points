#!/usr/bin/env python3
"""Apply tools/chart.css to every chart page, so the twelve charts share the app shell.

Replaces each chart's first <style> block, loads the same fonts as the app pages and marks
Channels as the current section in the app bar. Re-run after editing tools/chart.css:
    python3 tools/sync-chart-style.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = (ROOT / 'tools' / 'chart.css').read_text(encoding='utf-8').strip()
FONTS = 'https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&family=IBM+Plex+Mono:wght@500&family=Noto+Sans+SC:wght@300&display=swap'
PAGES = sorted(p.name for p in ROOT.glob('*meridian-chart.html'))
changed = 0
for name in PAGES:
    p = ROOT / name
    s = p.read_text(encoding='utf-8')
    new = re.sub(r'<style>.*?</style>', lambda m: '<style>\n' + CSS + '\n</style>', s, count=1, flags=re.S)
    new = re.sub(r'https://fonts\.googleapis\.com/css2\?[^"]+', FONTS, new, count=1)
    new = new.replace('<a class="l" href="channels.html">', '<a class="l here" href="channels.html">', 1) if 'class="l here"' not in new else new
    if new != s:
        p.write_text(new, encoding='utf-8'); changed += 1
print(f'{changed} page(s) updated')
