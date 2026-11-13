#!/usr/bin/env python3
"""Keep the twelve channel pages on one layout and one script.

Each page keeps its own plate, point data and diagrams. This tool gives every page the same frame
around them: the to-scale channel line, the plate card that turns to the point's location diagram,
the details panel (a sheet on phones) holding the route and relations, the shared script from
tools/chart-app.js, and the element's scene behind the page (painters taken from
tools/shell-snippet.html, so the ring and the charts paint the same picture).

The first run restructures a page; later runs only refresh the generated blocks. Run it after
editing tools/chart-app.js, the scene painters, or channel facts in data/points.json:
    python3 tools/sync-chart-app.py          (--check reports stale pages without writing)
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = json.loads((ROOT / 'data' / 'points.json').read_text(encoding='utf-8'))
CHANNELS = {c['file']: c for c in DOC['channels']}
APP = (ROOT / 'tools' / 'chart-app.js').read_text(encoding='utf-8').strip()
SHELL = (ROOT / 'tools' / 'shell-snippet.html').read_text(encoding='utf-8')
PAINT = SHELL[SHELL.index('/* ---------- procedural scenes'):SHELL.index('/* ---------- app shell')].strip()
KEYS = ['wood', 'fire', 'earth', 'metal', 'water']

def num(code):
    return int(re.sub(r'\D', '', code))

def place(landmark):
    """The part of a landmark that names where on the body it is, e.g. '4th Toe' from 'Lateral Nail Angle · 4th Toe'."""
    parts = [x.strip() for x in landmark.split('·')]
    named = [x for x in parts if not re.search(r'Nail Angle|Cun|Line$|^Apex$', x)]
    return (named or parts)[0]

def line(c):
    """The whole channel on one line, with the five Shu points at their true positions."""
    n = c['pointsCount']
    start, end = c['startDetails'], c['endDetails']
    shu = sorted((p for p in DOC['points'] if p['ch'] == c['abbr']), key=lambda p: num(p['code']))
    ticks = ''.join(
        f'<i style="left:{(num(p["code"]) - 1) / (n - 1) * 100:.1f}%;--c:var(--{p["elem"].lower()})" title="{p["code"]} · {p["shu"]}"></i>'
        for p in shu)
    course = re.sub(r'\s*\(.*\)$', '', c['course'])
    a, b = place(start['landmark']), place(end['landmark'])
    label = f'The whole {c["name"]} channel, {start["code"]} to {end["code"]}, {n} points, with its five Shu points marked'
    return ('<!-- chartline:start · generated from data/points.json by tools/sync-chart-app.py; edit there -->\n'
            f'<div class="cline" role="img" aria-label="{label}">'
            f'<div class="cl-track"><b style="left:0"></b><b style="left:100%"></b>{ticks}</div>'
            f'<div class="cl-lab"><span><b>{start["code"]}</b> · {a}</span><em>{n} points · {course}</em><span>{b} · <b>{end["code"]}</b></span></div>'
            '</div>\n<!-- chartline:end -->')

def scene(c):
    key = c['elem'].lower()
    return ('<!-- chartscene:start · painters copied from tools/shell-snippet.html by tools/sync-chart-app.py; edit there -->\n'
            '<script>\n(function(){\n' + PAINT + '\n'
            f"var key='{key}',el=document.getElementById('cscene');\n"
            "function show(){try{el.style.setProperty('--scene','url('+renderScene(key," + str(101 + KEYS.index(key) * 37) + ")+')');el.classList.add('on')}catch(e){}}\n"
            "var idle=window.requestIdleCallback||function(f){return setTimeout(f,60)};\n"
            "if(document.readyState==='complete')idle(show);else window.addEventListener('load',function(){idle(show)});\n"
            '})();\n</script>\n<!-- chartscene:end -->')

STAGE_HEAD = ('<div class="stage" id="stage">\n'
              '<div class="vsw" role="group" aria-label="Chart view"><button type="button" data-face="map" aria-pressed="true">Channel map</button>'
              '<button type="button" data-face="loc" aria-pressed="false" disabled>Point location</button></div>\n'
              '<div class="flip" id="flip">\n<div class="leg">')
STAGE_TAIL = ('<span class="ftag">Channel map · not to scale</span>\n</div>\n'
              '<div class="face-b" aria-hidden="true"><img id="loc-img" alt=""><span class="ftag" id="loc-tag"></span></div>\n'
              '</div>\n</div>')
EMPTY = '<div class="empty"><b>Select a point</b>Tap a dot on the chart or a station above for its location, cun measure and diagram.</div>'

def migrate(s, c):
    """One-time restructure of a page that still has the old layout."""
    banner = re.search(r'<!-- meridian-pathway:start -->.*?<!-- meridian-pathway:end -->\n?', s, re.S)
    s = s.replace(banner.group(0), '', 1)
    m = re.search(r'<div class="layout">\n<div class="leg">(.*?</svg>)\n</div>\n<aside class="panel" aria-label="Point details">\n'
                  r'<div id="pt-info" aria-live="polite">.*?</div></div>\n(<div class="pts".*?</div>)\n</aside>\n</div>\n(<p class="note">.*?</p>)', s, re.S)
    if not m:
        raise SystemExit('unexpected layout: ' + c['file'])
    summary = f'{c["startDetails"]["code"]} → {c["endDetails"]["code"]} · {len(c.get("stages", [])) or 1} stages'
    new = ('<div class="layout">\n' + STAGE_HEAD + m.group(1) + '\n' + STAGE_TAIL + '\n'
           '<aside class="panel" id="sheet" aria-label="Point details">\n'
           '<button type="button" class="grab" id="grab" aria-expanded="false" aria-controls="sheet-body"><i></i><span class="sr">Show or hide the full details</span></button>\n'
           '<div class="sheet-body" id="sheet-body">\n' + m.group(2) + '\n'
           '<div id="pt-info" aria-live="polite">' + EMPTY + '</div>\n'
           f'<details class="more" id="more"><summary><span>Route and relations</span><small>{summary}</small></summary>\n'
           + banner.group(0).rstrip('\n') + '\n</details>\n' + m.group(3) + '\n</div>\n</aside>\n</div>')
    s = s[:m.start()] + new + s[m.end():]
    s = re.sub(r'<h1>(.+?) (Meridian — Five Shu Points)</h1>', r'<h1>\1 <span class="h1x">\2</span></h1>', s, count=1)
    s = re.sub(r'(<p class="lede">.*?</p>)', lambda k: k.group(1) + '\n<!-- chartline:start --><!-- chartline:end -->', s, count=1, flags=re.S)
    i = s.index('var ELEM = ')
    j = s.index('})();\n</script>', i)
    s = s[:i] + '/* chartapp:start */\n/* chartapp:end */\n' + s[j:]
    j = s.index('</script>', i) + len('</script>')
    s = s[:j] + '\n<!-- chartscene:start --><!-- chartscene:end -->' + s[j:]
    s = s.replace('<main class="page">', '<div class="cscene" id="cscene" aria-hidden="true"></div>\n<main class="page" data-chartapp="1">', 1)
    return s

def sync(s, c):
    if 'data-chartapp' not in s:
        s = migrate(s, c)
    s = re.sub(r'<body[^>]*>', f'<body class="chart" data-el="{c["elem"].lower()}" data-yy="{c["yy"]}">', s, count=1)
    s = re.sub(r'<!-- chartline:start.*?<!-- chartline:end -->', lambda m: line(c), s, count=1, flags=re.S)
    s = re.sub(r'/\* chartapp:start.*?/\* chartapp:end \*/', lambda m: '/* chartapp:start · generated from tools/chart-app.js by tools/sync-chart-app.py; edit there */\n' + APP + '\n/* chartapp:end */', s, count=1, flags=re.S)
    s = re.sub(r'<!-- chartscene:start.*?<!-- chartscene:end -->', lambda m: scene(c), s, count=1, flags=re.S)
    return s

def main():
    check = '--check' in sys.argv
    stale = []
    for name, c in CHANNELS.items():
        p = ROOT / name
        if not p.exists():
            continue
        s = p.read_text(encoding='utf-8')
        new = sync(s, c)
        if new != s:
            stale.append(name)
            if not check:
                p.write_text(new, encoding='utf-8')
    if check:
        print('stale: ' + ', '.join(stale) if stale else 'chart pages are up to date')
        sys.exit(1 if stale else 0)
    print(f'{len(stale)} page(s) updated')

if __name__ == '__main__':
    main()
