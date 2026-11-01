#!/usr/bin/env python3
"""Copy the point data in data/points.json into every page that shows it.

data/points.json is the single source for the sixty Shu points. Pages stay
self-contained, so this script writes the data into them:

  * script blocks between  /* points:start NAME ... */  and  /* points:end */
      P     study.html, points.html   flat list of all sixty points
      CH    study.html                the twelve channels
      DATA  chart pages (*-v4 + Lung) that channel's five points
      FILE  index.html                channel -> chart file and name; element -> channels
      HOR   index.html                channel -> horary point
  * HTML elements in learn.html tagged  data-pt="CODE" data-f="FIELD"
      py (pinyin), elem (dot + element), loc (location), horary (category line)

Usage:  python3 tools/sync-points.py          write the pages
        python3 tools/sync-points.py --check  exit 1 if any page is out of date
"""
import html, json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = json.loads((ROOT / 'data' / 'points.json').read_text(encoding='utf-8'))
CHANNELS = DOC['channels']
POINTS = DOC['points']
CH = {c['abbr']: c for c in CHANNELS}
PT = {p['code']: p for p in POINTS}

SHU = ['Jing-Well', 'Ying-Spring', 'Shu-Stream', 'Jing-River', 'He-Sea']
SEQ = {'Yin': ['Wood', 'Fire', 'Earth', 'Metal', 'Water'],
       'Yang': ['Metal', 'Water', 'Wood', 'Fire', 'Earth']}


def validate():
    errors = []
    for c in CHANNELS:
        pts = sorted((p for p in POINTS if p['ch'] == c['abbr']), key=lambda p: p['rank'])
        if [p['rank'] for p in pts] != [0, 1, 2, 3, 4]:
            errors.append(f"{c['abbr']}: needs exactly one point per station, got ranks {[p['rank'] for p in pts]}")
            continue
        for p in pts:
            if p['shu'] != SHU[p['rank']]:
                errors.append(f"{p['code']}: station {p['rank']} must be {SHU[p['rank']]}, not {p['shu']}")
            if p['elem'] != SEQ[c['yy']][p['rank']]:
                errors.append(f"{p['code']}: a {c['yy']} {p['shu']} carries {SEQ[c['yy']][p['rank']]}, not {p['elem']}")
            for k in ('py', 'hz', 'en', 'note', 'loc'):
                if not p.get(k):
                    errors.append(f"{p['code']}: missing {k}")
        if sum(p['elem'] == c['elem'] for p in pts) != 1:
            errors.append(f"{c['abbr']}: needs exactly one horary point")
    if errors:
        sys.exit('data/points.json is invalid:\n  ' + '\n  '.join(errors))


def js(v):
    return json.dumps(v, ensure_ascii=False)


def by_channel(abbr):
    return sorted((p for p in POINTS if p['ch'] == abbr), key=lambda p: p['rank'])


def flat(p):
    c = CH[p['ch']]
    return {'code': p['code'], 'py': p['py'], 'hz': p['hz'], 'en': p['en'], 'shu': p['shu'], 'rank': p['rank'],
            'note': p['note'], 'elem': p['elem'], 'loc': p['loc'], 'ch': c['abbr'], 'chName': c['name'],
            'chElem': c['elem'], 'yy': c['yy'], 'file': c['file']}


def gen_P(page):
    return 'var P = ' + js([flat(p) for c in CHANNELS for p in by_channel(c['abbr'])]) + ';'


def gen_CH(page):
    return 'var CH = ' + js([{k: c[k] for k in ('key', 'file', 'name', 'abbr', 'elem', 'yy')} for c in CHANNELS]) + ';'


def gen_DATA(page):
    chans = [c for c in CHANNELS if c['file'] == page]
    if len(chans) != 1:
        sys.exit(f'{page}: no single channel in data/points.json has this file')
    rows = []
    for p in by_channel(chans[0]['abbr']):
        d = {'code': p['code'], 'pinyin': p['py'], 'en': p['en'], 'shu': p['note'], 'elem': p['elem'], 'loc': p['loc']}
        if p.get('cun'):
            d['cun'] = p['cun']
        rows.append(' ' + js('p' + re.sub(r'\D', '', p['code'])) + ': ' + js(d))
    return 'var DATA = {\n' + ',\n'.join(rows) + '\n};'


def gen_FILE(page):
    elch = {}
    for c in CHANNELS:
        elch.setdefault(c['elem'], []).append(c['abbr'])
    return ('const FILE=' + js({c['abbr']: c['file'] for c in CHANNELS})
            + ',NAME=' + js({c['abbr']: c['name'] for c in CHANNELS})
            + ',ELCH=' + js(elch) + ';')


def gen_HOR(page):
    hor = {}
    for c in CHANNELS:
        p = next(p for p in by_channel(c['abbr']) if p['elem'] == c['elem'])
        hor[c['abbr']] = [p['code'], p['py']]
    return 'const HOR=' + json.dumps(hor, ensure_ascii=False, separators=(',', ':')) + ';'


GEN = {'P': gen_P, 'CH': gen_CH, 'DATA': gen_DATA, 'FILE': gen_FILE, 'HOR': gen_HOR}
BLOCK = re.compile(r'(/\* points:start (\w+)[^*]*\*/\n)(.*?)(\n/\* points:end \*/)', re.S)


def fill_blocks(page, s):
    def one(m):
        if m.group(2) not in GEN:
            sys.exit(f'{page}: unknown block {m.group(2)}')
        return m.group(1) + GEN[m.group(2)](page) + m.group(4)
    return BLOCK.sub(one, s)


def learn_value(code, field):
    p = PT.get(code) or sys.exit(f'learn.html: unknown point {code}')
    if field == 'py':
        return html.escape(p['py'])
    if field == 'loc':
        return html.escape(p['loc'])
    if field == 'elem':
        return f'<i class="dot" style="--c:var(--t-{p["elem"].lower()})"></i>{p["elem"]}'
    if field == 'horary':
        if p['elem'] != CH[p['ch']]['elem']:
            sys.exit(f'learn.html: {code} is tagged horary but is not its channel\'s horary point')
        return f'<b>{p["shu"]}</b> · {p["elem"]} · horary'
    sys.exit(f'learn.html: unknown field {field}')


TAGGED = re.compile(r'(<(\w+)\b[^>]*\bdata-pt="(\w+)" data-f="(\w+)"[^>]*>)(.*?)(</\2>)', re.S)


def fill_tagged(page, s):
    return TAGGED.sub(lambda m: m.group(1) + learn_value(m.group(3), m.group(4)) + m.group(6), s)


def main():
    validate()
    check = '--check' in sys.argv
    pages = sorted({c['file'] for c in CHANNELS} | {'study.html', 'points.html', 'index.html', 'learn.html'})
    stale = []
    for name in pages:
        path = ROOT / name
        s = path.read_text(encoding='utf-8')
        new = fill_tagged(name, fill_blocks(name, s))
        if new != s:
            stale.append(name)
            if not check:
                path.write_text(new, encoding='utf-8')
    if check:
        if stale:
            sys.exit('out of date: ' + ', '.join(stale) + '\nrun: python3 tools/sync-points.py')
        print('all pages match data/points.json')
    else:
        print(f'{len(stale)} page(s) updated')


if __name__ == '__main__':
    main()
