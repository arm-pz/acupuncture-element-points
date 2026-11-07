#!/usr/bin/env python3
"""Assemble the deployable site into dist/: only the pages and favicon, plus Cloudflare Pages routing.

Source-only files (tools, data, commons, docs, the local dev server) are left out. The short routes
served by shu-serve.js (/lu, /learn, ...) become 200 rewrites in dist/_redirects.
    python3 tools/build-site.py
"""
import pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / 'dist'
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir()

pages = sorted(ROOT.glob('*.html'))
for p in pages:
    shutil.copy2(p, DIST / p.name)
shutil.copy2(ROOT / 'favicon.svg', DIST / 'favicon.svg')

# Routes come from shu-serve.js so the two never drift apart.
js = (ROOT / 'shu-serve.js').read_text(encoding='utf-8')
routes = dict(re.findall(r'"(/[a-z0-9]+)": "([a-z0-9-]+\.html)"', js))
routes.update({'/channels': 'channels.html', '/points': 'points.html', '/learn': 'learn.html',
               '/basics': 'basics.html', '/study': 'study.html'})
lines = []
for route, file in sorted(routes.items()):
    if route == '/' or route[1:] == file[:-5] or not (DIST / file).exists():
        continue
    lines.append(f'{route} /{file[:-5]} 200')  # Pages serves /name for name.html
(DIST / '_redirects').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(f'dist/: {len(pages)} pages, {len(lines)} routes')
