#!/usr/bin/env python3
"""Build and upgrade channels.html with interactive transit explorer capabilities."""
import json
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# 1. Load point data
with open(ROOT / 'data' / 'points.json', encoding='utf-8') as f:
    points_data = json.load(f)

points_dict = {p['code']: p for p in points_data['points']}
channel_meta = {
    'LR': {'limb': 'foot', 'yy': 'yin', 'el': 'wood', 'name': 'Liver', 'hz': '足厥陰肝經', 'file': 'lr-v4-meridian-chart.html'},
    'GB': {'limb': 'foot', 'yy': 'yang', 'el': 'wood', 'name': 'Gallbladder', 'hz': '足少陽膽經', 'file': 'gb-v4-meridian-chart.html'},
    'HT': {'limb': 'hand', 'yy': 'yin', 'el': 'fire', 'name': 'Heart', 'hz': '手少陰心經', 'file': 'ht-v4-meridian-chart.html'},
    'SI': {'limb': 'hand', 'yy': 'yang', 'el': 'fire', 'name': 'Small Intestine', 'hz': '手太陽小腸經', 'file': 'si-v4-meridian-chart.html'},
    'PC': {'limb': 'hand', 'yy': 'yin', 'el': 'fire', 'name': 'Pericardium', 'hz': '手厥陰心包經', 'file': 'pc-v4-meridian-chart.html'},
    'TB': {'limb': 'hand', 'yy': 'yang', 'el': 'fire', 'name': 'Triple Burner', 'hz': '手少陽三焦經', 'file': 'tb-v4-meridian-chart.html'},
    'SP': {'limb': 'foot', 'yy': 'yin', 'el': 'earth', 'name': 'Spleen', 'hz': '足太陰脾經', 'file': 'sp-v4-meridian-chart.html'},
    'ST': {'limb': 'foot', 'yy': 'yang', 'el': 'earth', 'name': 'Stomach', 'hz': '足陽明胃經', 'file': 'st-v4-meridian-chart.html'},
    'LU': {'limb': 'hand', 'yy': 'yin', 'el': 'metal', 'name': 'Lung', 'hz': '手太陰肺經', 'file': 'lung-meridian-chart.html'},
    'LI': {'limb': 'hand', 'yy': 'yang', 'el': 'metal', 'name': 'Large Intestine', 'hz': '手陽明大腸經', 'file': 'li-v4-meridian-chart.html'},
    'KI': {'limb': 'foot', 'yy': 'yin', 'el': 'water', 'name': 'Kidney', 'hz': '足少陰腎經', 'file': 'ki-v4-meridian-chart.html'},
    'BL': {'limb': 'foot', 'yy': 'yang', 'el': 'water', 'name': 'Bladder', 'hz': '足太陽膀胱經', 'file': 'bl-v4-meridian-chart.html'}
}

# Read original channels.html to extract fonts
orig_html = (ROOT / 'channels.html').read_text(encoding='utf-8')
font_end = orig_html.find(':root')
font_block = orig_html[:font_end]

# Read footer snippet
footer_snippet = (ROOT / 'tools' / 'footer-snippet.html').read_text(encoding='utf-8').strip()

# Build compact points JSON for client-side inspector
clean_points = {}
for code, p in points_dict.items():
    ch_info = channel_meta.get(p['ch'], {})
    clean_points[code] = {
        'code': p['code'],
        'ch': p['ch'],
        'chName': ch_info.get('name', ''),
        'hz': p.get('hz', ''),
        'py': p.get('py', ''),
        'en': p.get('en', ''),
        'shu': p.get('shu', ''),
        'elem': p.get('elem', ''),
        'yy': ch_info.get('yy', ''),
        'limb': ch_info.get('limb', ''),
        'loc': p.get('loc', ''),
        'note': p.get('note', ''),
        'file': ch_info.get('file', '')
    }

points_json_str = json.dumps(clean_points, ensure_ascii=False)

# Build Routes HTML
channels_order = ['LR', 'GB', 'HT', 'SI', 'PC', 'TB', 'SP', 'ST', 'LU', 'LI', 'KI', 'BL']
routes_html = []

for idx, ch in enumerate(channels_order):
    meta = channel_meta[ch]
    ch_pts = [p for p in points_data['points'] if p['ch'] == ch]
    ch_pts.sort(key=lambda x: x['rank'])
    
    yin_class = " is-yin" if meta['yy'] == 'yin' else ""
    el_class = f"ph-{meta['el']}"
    limb_class = f"is-{meta['limb']}"
    
    stations_markup = []
    for p in ch_pts:
        p_el = p['elem'].lower()
        stations_markup.append(
            f'<a class="station ph-{p_el}" href="{meta["file"]}#{p["code"]}" data-code="{p["code"]}" data-rank="{p["rank"]}" aria-label="{p["code"]} {p.get("py","")} ({p.get("shu","")}, {p.get("elem","")})">'
            f'<span class="sr-only">{p.get("shu","")}: </span>'
            f'<span class="code">{p["code"]}</span>'
            f'<span class="node" aria-hidden="true"></span>'
            f'<span class="tick" aria-hidden="true"></span>'
            f'<span class="phase">{p.get("elem","")}</span>'
            f'</a>'
        )
    stations_str = "".join(stations_markup)
    
    route_div = f'''<div class="route {el_class}{yin_class} {limb_class}" data-ch="{ch}" data-el="{meta['el']}" data-yy="{meta['yy'].lower()}" data-limb="{meta['limb']}" style="--i:{idx}">
  <div class="terminus">
    <a class="link" href="{meta['file']}" aria-label="Open the {meta['name']} ({ch}) chart — {meta['yy']} {meta['el'].title()} channel">
      <span class="badge">{ch}</span>
      <span class="ident">
        <span class="name">{meta['name']}</span>
        <span class="meta">{meta['yy']} · {meta['el'].title()} · <span class="han" lang="zh-Hant">{meta['hz']}</span></span>
      </span>
    </a>
  </div>
  <div class="field">
    <span class="bend" aria-hidden="true"><svg viewBox="0 0 22 28" preserveAspectRatio="none"><path class="bend-yin" d="M1 7L22 28"/><path class="bend-yang" d="M1 7L22 28"/></svg></span>
    <span class="track" aria-hidden="true"></span>
    <span class="stations">{stations_str}</span>
  </div>
  <span class="chev" aria-hidden="true"><svg viewBox="0 0 8 14" aria-hidden="true"><path d="M1 1l6 6-6 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg></span>
</div>'''
    routes_html.append(route_div)

all_routes_str = "\n".join(routes_html)

# CSS Styles
styles = f'''{font_block}:root{{
  --ground:#0d101d;
  --raise:#151928;
  --raise-2:#1e2338;
  --ink:#f5f3ed;
  --ink-2:#9ea8bd;
  --ink-3:#657088;
  --hair:rgba(245,243,237,.09);
  --hair-2:rgba(245,243,237,.18);
  --row:60px;
  --term:clamp(230px,21vw,292px);
  --chev:30px;
  --pad:clamp(16px,3vw,48px);
  --mono:"Plex Mono",ui-monospace,monospace;
  --ease:cubic-bezier(.16,1,.3,1);
}}
.ph-wood{{--deep:#3e7d5a;--tint:#83c7a3;--glow:rgba(131,199,163,.28)}}
.ph-fire{{--deep:#d23b2e;--tint:#f2968a;--glow:rgba(242,150,138,.28)}}
.ph-earth{{--deep:#d99a2b;--tint:#e8c273;--glow:rgba(232,194,115,.28)}}
.ph-metal{{--deep:#dfd9cb;--tint:#f5f3ed;--glow:rgba(245,243,237,.28)}}
.ph-water{{--deep:#3c6fbd;--tint:#93b8f0;--glow:rgba(147,184,240,.28)}}

*{{box-sizing:border-box}}
html{{background:var(--ground);color-scheme:dark;scrollbar-color:#3a4257 var(--ground);scrollbar-width:thin}}
body{{margin:0;background:var(--ground);color:var(--ink);font-family:"Jost",system-ui,sans-serif;font-weight:400;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}}
::selection{{background:rgba(245,243,237,.24);color:var(--ink)}}
:focus-visible{{outline:2px solid var(--ink);outline-offset:2px}}
a{{color:inherit}}
.sr-only{{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}}
.wrap{{max-width:1440px;margin:0 auto;padding:0 var(--pad)}}

/* App Navigation */
.appnav{{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 0;border-bottom:1px solid var(--hair);position:sticky;top:0;z-index:100;background:rgba(13,16,29,.85);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}}
.appnav .home{{display:flex;align-items:baseline;gap:10px;color:var(--ink);text-decoration:none;min-width:0;transition:opacity .16s var(--ease)}}
.appnav .home:hover{{opacity:.85}}
.appnav .home:active{{transform:scale(.98)}}
.appnav .home .han{{font:300 19px/1 "Noto Sans SC","PingFang SC",sans-serif}}
.appnav .home .t{{font:500 11px/1 "Jost",system-ui,sans-serif;letter-spacing:.24em;text-transform:uppercase;color:var(--ink-2);white-space:nowrap}}
.appnav ul{{display:flex;gap:2px;list-style:none;margin:0;padding:0}}
.appnav a.l{{display:block;padding:8px 12px;border-radius:999px;font:500 13px/1 "Jost",system-ui,sans-serif;letter-spacing:.02em;color:var(--ink-2);text-decoration:none;transition:color .16s var(--ease),background .16s var(--ease),transform .12s var(--ease)}}
.appnav a.l:hover{{color:var(--ink);background:rgba(245,243,237,.06)}}
.appnav a.l:active{{transform:scale(.96)}}
.appnav a.l[aria-current="page"]{{color:var(--ground);background:var(--ink);font-weight:600}}
@media (max-width:700px){{
  .appnav{{flex-wrap:wrap;justify-content:center;row-gap:6px}}
  .appnav .home{{width:100%;justify-content:center}}
  .appnav .home .t{{display:none}}
  .appnav ul{{flex-wrap:wrap;justify-content:center}}
  .appnav a.l{{padding:8px 9px;font-size:12.5px}}
}}

/* Masthead */
.masthead{{display:flex;align-items:flex-start;justify-content:space-between;gap:32px;padding:28px 0 20px;border-bottom:1px solid var(--hair)}}
.mark{{display:block;width:88px;height:14px;margin-bottom:12px}}
.brand h1{{margin:0;font-size:clamp(24px,2.4vw,32px);font-weight:500;letter-spacing:.18em;text-transform:uppercase;line-height:1;display:flex;align-items:baseline;gap:12px}}
.brand h1 .han{{font-family:"Classic","Songti SC","Noto Sans SC","SimSun",serif;font-size:14px;font-weight:500;letter-spacing:.08em;color:var(--ink-2)}}
.tagline{{margin:8px 0 0;font-size:14px;letter-spacing:.015em;color:var(--ink-2)}}
.key{{display:flex;flex-direction:column;align-items:flex-end;gap:10px;padding-top:4px}}
.key-label{{font:500 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3)}}
.phases{{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:6px 14px;margin:0;padding:0;list-style:none}}
.phases li{{display:flex;align-items:center;gap:7px;font:500 11px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-2);cursor:pointer;padding:3px 6px;border-radius:6px;transition:background .15s var(--ease),color .15s var(--ease)}}
.phases li:hover{{background:rgba(245,243,237,.06);color:var(--ink)}}
.phases .sw{{width:16px;height:4px;border-radius:2px;background:var(--deep);box-shadow:0 0 6px var(--glow)}}
.polarity{{display:flex;align-items:center;gap:16px;margin:0;font:500 11px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-2)}}
.polarity span{{display:flex;align-items:center;gap:7px}}
.pl{{width:24px;height:5px;position:relative;background:var(--ink);border-radius:1px}}
.pl-yin::after{{content:"";position:absolute;left:0;right:0;top:1.75px;height:1.5px;background:var(--ground)}}

/* Controls Panel */
.controls-panel{{margin:20px 0 16px;padding:16px 18px;background:var(--raise);border:1px solid var(--hair);border-radius:16px;box-shadow:0 4px 20px -4px rgba(0,0,0,.35);display:flex;flex-direction:column;gap:14px}}
.search-wrap{{position:relative;display:flex;align-items:center}}
.search-icon{{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:18px;height:18px;color:var(--ink-3);pointer-events:none;transition:color .16s var(--ease)}}
.search-wrap input{{width:100%;height:46px;padding:0 140px 0 44px;border-radius:12px;border:1px solid var(--hair);background:var(--raise-2);color:var(--ink);font:400 15px/1 "Jost",system-ui,sans-serif;box-shadow:inset 0 1px 2px rgba(0,0,0,.25);transition:border-color .16s var(--ease),background .16s var(--ease),box-shadow .16s var(--ease)}}
.search-wrap input::placeholder{{color:var(--ink-3)}}
.search-wrap input:focus{{outline:none;border-color:rgba(245,243,237,.45);background:#1a2033;box-shadow:0 0 0 3px rgba(245,243,237,.08),inset 0 1px 2px rgba(0,0,0,.2)}}
.search-wrap:focus-within .search-icon{{color:var(--ink)}}
.count-badge{{position:absolute;right:14px;top:50%;transform:translateY(-50%);font:500 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);pointer-events:none;background:var(--raise);padding:4px 8px;border-radius:6px;border:1px solid var(--hair);white-space:nowrap}}
.clear-search-btn{{position:absolute;right:150px;top:50%;transform:translateY(-50%);appearance:none;border:0;background:transparent;color:var(--ink-3);cursor:pointer;font:500 11.5px/1 var(--mono);padding:4px 6px;border-radius:4px;display:none}}
.clear-search-btn:hover{{color:var(--ink)}}

.filter-row{{display:flex;flex-wrap:wrap;align-items:center;gap:12px 20px}}
.filter-group{{display:flex;align-items:center;gap:8px}}
.filter-lbl{{font:500 10.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);flex:none}}
.seg{{display:inline-flex;flex-wrap:wrap;gap:2px;padding:3px;border-radius:999px;background:var(--raise-2);border:1px solid var(--hair)}}
.seg button{{appearance:none;border:0;background:transparent;color:var(--ink-2);font:500 12px/1 "Jost",system-ui,sans-serif;padding:6px 12px;border-radius:999px;cursor:pointer;display:inline-flex;align-items:center;gap:6px;transition:color .15s ease,background-color .15s ease,transform .12s var(--ease)}}
.seg button:hover{{color:var(--ink);background:rgba(245,243,237,.05)}}
.seg button:active{{transform:scale(.95)}}
.seg button[aria-pressed="true"]{{background:var(--ink);color:var(--ground);box-shadow:0 1px 6px rgba(0,0,0,.35);font-weight:600}}
.seg button .dot{{width:7px;height:7px;border-radius:50%;background:var(--deep);display:inline-block}}

/* Column Header */
.colhead{{position:sticky;top:50px;z-index:20;background:rgba(13,16,29,.92);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);display:grid;grid-template-columns:var(--term) minmax(0,1fr) var(--chev);align-items:end;padding:12px 8px 10px;border-bottom:1px solid var(--hair)}}
.term-head{{font:500 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3)}}
.colgrid{{display:grid;grid-template-columns:repeat(5,1fr);gap:4px}}
.shu-col-btn{{appearance:none;border:1px solid transparent;background:transparent;padding:6px 4px;border-radius:8px;cursor:pointer;display:flex;align-items:baseline;justify-content:center;gap:7px;color:var(--ink-2);transition:all .16s var(--ease)}}
.shu-col-btn:hover{{background:rgba(245,243,237,.05);color:var(--ink);border-color:var(--hair)}}
.shu-col-btn:active{{transform:scale(.97)}}
.shu-col-btn[aria-pressed="true"]{{background:var(--raise-2);color:var(--ink);border-color:var(--hair-2);box-shadow:0 2px 8px rgba(0,0,0,.3)}}
.shu-en{{font:500 11px/1 var(--mono);letter-spacing:.15em;text-transform:uppercase}}
.shu-han{{font-family:"Classic","Noto Sans SC","Songti SC",serif;font-size:13px;font-weight:500;color:var(--ink);opacity:.85}}

/* Harmonic Drawer Banner */
.col-drawer{{margin:8px 0 14px;padding:12px 18px;background:var(--raise);border:1px solid var(--hair-2);border-radius:12px;box-shadow:0 8px 24px -6px rgba(0,0,0,.45);display:none;animation:fadeSlide .2s var(--ease) both}}
.col-drawer.open{{display:block}}
.col-drawer-in{{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px}}
.col-drawer-left{{display:flex;align-items:center;gap:14px;min-width:0;flex:1}}
.col-drawer-badge{{display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 10px;border-radius:6px;background:var(--ink);color:var(--ground);font:600 12px/1 var(--mono);letter-spacing:.04em;flex:none}}
.col-drawer-desc{{margin:0;font-size:13.5px;line-height:1.45;color:var(--ink-2);flex:1}}
.col-drawer-desc b{{color:var(--ink);font-weight:500}}
.col-drawer-close{{appearance:none;border:0;background:rgba(245,243,237,.06);color:var(--ink-2);padding:5px 10px;border-radius:6px;font:500 11.5px/1 "Jost",system-ui,sans-serif;cursor:pointer;transition:all .15s var(--ease)}}
.col-drawer-close:hover{{background:rgba(245,243,237,.12);color:var(--ink)}}

/* Routes & Map */
.map{{padding-bottom:12px}}
.route{{position:relative;display:grid;grid-template-columns:var(--term) minmax(0,1fr) var(--chev);align-items:stretch;min-height:var(--row);border-radius:12px;padding:0 8px;transition:background-color .16s ease,transform .15s var(--ease),opacity .18s ease,filter .18s ease}}
.route + .route{{border-top:1px solid var(--hair)}}
.route:hover{{background:rgba(245,243,237,.04);transform:translateX(3px)}}
.route:active{{transform:scale(0.995)}}
.route[hidden]{{display:none}}
.route.dimmed{{opacity:.22;filter:grayscale(.3)}}

.map:has(.route:hover) .route:not(:hover){{opacity:.45}}
.map:has(.station:hover) .route:not(:has(.station:hover)){{opacity:.25}}

.terminus{{display:flex;align-items:center;padding-right:16px;min-width:0;position:relative}}
.link{{display:flex;align-items:center;gap:12px;width:100%;height:100%;padding:8px 0;text-decoration:none}}
.badge{{display:inline-flex;align-items:center;justify-content:center;flex:none;min-width:46px;height:26px;padding:0 6px;border-radius:6px;background:var(--tint);color:var(--ground);font-family:var(--mono);font-size:12.5px;font-weight:600;letter-spacing:.04em;box-shadow:0 2px 6px rgba(0,0,0,.3);transition:transform .15s var(--ease)}}
.route:hover .badge{{transform:scale(1.06)}}
.ident{{display:flex;flex-direction:column;min-width:0}}
.name{{font-size:16.5px;font-weight:500;line-height:1.15;letter-spacing:.005em;color:var(--ink);white-space:nowrap}}
.meta{{font-size:11px;line-height:1.4;color:var(--ink-2);white-space:nowrap;margin-top:2px}}
.meta .han{{font-family:"Classic","Songti SC","Noto Sans SC",serif;font-size:11.5px;font-weight:500;letter-spacing:.02em}}

.field{{position:relative;min-width:0}}
.stations{{position:absolute;inset:0;display:grid;grid-template-columns:repeat(5,1fr);z-index:10;pointer-events:none}}
.station{{position:relative;min-width:0;display:block;height:100%;text-decoration:none;pointer-events:auto;transition:transform .15s var(--ease)}}

.code{{position:absolute;left:0;right:0;top:4px;text-align:center;font-family:var(--mono);font-size:11px;line-height:1.2;letter-spacing:.02em;color:var(--ink);transition:transform .15s var(--ease),color .15s ease,filter .15s ease}}
.tick{{position:absolute;left:50%;top:19px;width:3px;height:18px;margin-left:-1.5px;background:var(--deep);transition:transform .15s var(--ease),filter .15s ease}}
.phase{{position:absolute;left:0;right:0;top:41px;text-align:center;font:500 10.5px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--tint);transition:transform .15s var(--ease)}}

/* Transit Station Node (Dot on the line) */
.node{{position:absolute;left:50%;top:24.5px;width:7px;height:7px;margin-left:-3.5px;border-radius:50%;background:var(--ground);border:2px solid var(--tint);box-shadow:0 0 0 1px rgba(0,0,0,.5);z-index:4;transition:transform .16s var(--ease),background .16s var(--ease),box-shadow .16s var(--ease)}}
.route.is-yin .node{{top:24px}}

.station:hover .code{{transform:translateY(-2px) scale(1.18);color:var(--tint);font-weight:600;filter:drop-shadow(0 0 6px var(--glow))}}
.station:hover .node{{transform:scale(1.7);background:var(--tint);box-shadow:0 0 10px var(--glow),0 0 0 1px var(--ground)}}
.station:hover .tick{{transform:scaleY(1.3);filter:drop-shadow(0 0 6px var(--glow))}}
.station:focus-visible{{outline:none}}
.station:focus-visible .node{{transform:scale(1.8);background:var(--tint);box-shadow:0 0 0 2px var(--ink)}}

/* Station Search Match & Column Active Highlights */
.station.match .code{{color:#fff;font-weight:700;transform:translateY(-2px) scale(1.2);filter:drop-shadow(0 0 8px var(--tint))}}
.station.match .node{{transform:scale(2);background:var(--tint);box-shadow:0 0 12px var(--tint);animation:matchPulse 1.4s infinite alternate ease-in-out}}
.station.col-active .code{{color:var(--tint);font-weight:600;transform:translateY(-1px) scale(1.12)}}
.station.col-active .node{{transform:scale(1.5);background:var(--tint);box-shadow:0 0 8px var(--glow)}}
.station.col-active::before{{content:"";position:absolute;inset:2px 4px;background:rgba(245,243,237,.035);border-radius:6px;pointer-events:none}}

@keyframes matchPulse{{from{{transform:scale(1.8);box-shadow:0 0 8px var(--tint)}}to{{transform:scale(2.3);box-shadow:0 0 16px var(--tint)}}}}

/* Tracks */
.track{{position:absolute;left:22px;right:10%;top:26.5px;height:3px;background:var(--deep);transform-origin:left center;animation:draw .65s var(--ease) both;animation-delay:calc(var(--i) * 40ms);z-index:1;overflow:hidden}}
.route.is-yin .track{{top:25.5px;height:5px}}
.route.is-yin .track::after{{content:"";position:absolute;left:0;right:0;top:1.5px;height:2px;background:var(--ground)}}

/* Qi Pulse Wave on hover */
.route:hover .track::before{{content:"";position:absolute;top:0;left:-60%;width:60%;height:100%;background:linear-gradient(90deg,transparent,var(--tint),transparent);animation:qiFlow 1.6s cubic-bezier(.4,0,.2,1) infinite}}
@keyframes qiFlow{{0%{{transform:translateX(0)}}100%{{transform:translateX(350%)}}}}

.bend{{position:absolute;left:0;top:0;width:22px;height:28px;z-index:1}}
.bend svg{{display:block;width:22px;height:28px;overflow:visible;animation:fade .4s ease both;animation-delay:calc(var(--i) * 40ms)}}
.bend-yin,.bend-yang{{fill:none;stroke-linecap:butt}}
.bend-yin{{display:none}}
.bend-yang{{stroke:var(--deep);stroke-width:3}}
.route.is-yin .bend-yang{{display:none}}
.route.is-yin .bend-yin{{display:block;stroke:var(--deep);stroke-width:5}}
.route.is-yin .bend::after{{content:"";position:absolute;left:0;top:7px;width:30px;height:2px;background:var(--ground);transform:rotate(45deg);transform-origin:left top;pointer-events:none}}

.chev{{display:flex;align-items:center;justify-content:center;color:var(--ink);opacity:.3;transition:opacity .18s ease,transform .18s ease}}
.chev svg{{width:8px;height:14px}}
.route:hover .chev{{opacity:1;transform:translateX(2px)}}

@keyframes draw{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes fadeSlide{{from{{opacity:0;transform:translateY(-6px)}}to{{opacity:1;transform:none}}}}

/* Floating Station Inspector Popover */
.station-popover{{position:fixed;z-index:120;left:0;top:0;width:min(320px,calc(100vw - 28px));padding:16px 18px 14px;border-radius:14px;background:rgba(21,25,40,.96);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);color:var(--ink);border:1px solid rgba(245,243,237,.16);box-shadow:0 24px 60px -15px rgba(0,0,0,.85),0 0 0 1px rgba(245,243,237,.06);font:400 13px/1.5 "Jost",system-ui,sans-serif;letter-spacing:.005em;pointer-events:none;visibility:hidden;opacity:0;transform:translateY(6px) scale(.98);transition:opacity .16s var(--ease),transform .16s var(--ease)}}
.station-popover.on{{visibility:visible;opacity:1;pointer-events:auto;transform:none}}
.station-popover.below{{transform:translateY(-6px) scale(.98)}}
.station-popover.on.below{{transform:none}}

.sp-top{{display:flex;align-items:baseline;justify-content:space-between;gap:8px;border-bottom:1px solid var(--hair);padding-bottom:10px}}
.sp-left{{display:flex;align-items:baseline;gap:8px}}
.sp-code{{display:inline-flex;align-items:center;justify-content:center;padding:2px 8px;border-radius:5px;background:var(--tint);color:var(--ground);font:600 12px/1 var(--mono)}}
.sp-hz{{font-family:"Classic","Songti SC","Noto Sans SC",serif;font-size:16px;font-weight:500;color:var(--ink)}}
.sp-py{{font:500 12px/1 var(--mono);color:var(--ink-2)}}
.sp-en{{font-size:12px;color:var(--ink-3);font-style:italic}}

.sp-badges{{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}}
.sp-badge{{display:inline-flex;align-items:center;gap:5px;padding:3px 8px;border-radius:6px;background:var(--raise-2);border:1px solid var(--hair);font:500 11px/1 var(--mono);letter-spacing:.02em;color:var(--ink-2)}}
.sp-dot{{width:6px;height:6px;border-radius:50%;display:inline-block}}

.sp-note{{margin:8px 0 0;font-size:12px;line-height:1.45;color:var(--tint)}}
.sp-loc{{margin:8px 0 0;padding-top:8px;border-top:1px solid var(--hair);font-size:12px;line-height:1.5;color:var(--ink-2)}}
.sp-loc-lbl{{display:block;font:500 9.5px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);margin-bottom:3px}}

.sp-foot{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:12px;padding-top:10px;border-top:1px solid var(--hair)}}
.sp-hint{{font:500 10.5px/1 var(--mono);color:var(--ink-3);letter-spacing:.02em}}
.sp-cta{{display:inline-flex;align-items:center;gap:5px;color:var(--ink);font-weight:500;font-size:12px;text-decoration:none;border-bottom:1px solid var(--hair);padding-bottom:1px;transition:border-color .15s ease}}
.sp-cta:hover{{border-color:var(--ink)}}

/* Footer Notes */
.notes{{margin-top:34px;border-top:1px solid var(--hair);padding:22px 0 40px;max-width:88ch}}
.notes p{{margin:0 0 10px;font-size:12px;line-height:1.7;color:var(--ink-2)}}
.notes p:last-child{{margin-bottom:0}}
.notes .arr{{opacity:.55;margin:0 2px}}
.notes .po{{color:var(--tint);letter-spacing:.01em}}
.notes .lb{{color:var(--ink);letter-spacing:.06em;font-weight:500}}
.notes .sep{{padding:0 6px;opacity:.6}}
.cycle{{display:inline}}

@media (max-width:820px){{
  .masthead{{flex-direction:column;gap:20px;padding:22px 0 16px}}
  .key{{align-items:flex-start;padding-top:0}}
  .phases{{justify-content:flex-start;gap:4px 9px}}
  .polarity{{gap:12px}}
  .colhead{{position:sticky;top:0;grid-template-columns:1fr;padding:10px 0 8px}}
  .term-head{{display:none}}
  .route{{grid-template-columns:1fr;padding:10px 0 8px}}
  .terminus{{padding-right:0}}
  .field{{height:54px;margin-top:8px}}
  .track{{left:0;top:23.5px}}
  .route.is-yin .track{{top:22.5px}}
  .bend{{display:none}}
  .chev{{display:none}}
  .code{{top:1px}}
  .tick{{top:16px}}
  .phase{{top:37px}}
  .node{{top:21.5px}}
  .route.is-yin .node{{top:21px}}
}}
@media (prefers-reduced-motion:reduce){{
  *,*::before,*::after{{animation:none!important;transition:none!important}}
}}
</style>
'''

# JavaScript Engine
js_script = f'''<script>
(function(){{
  'use strict';
  var P = {points_json_str};
  
  var state = {{
    el: '',
    yy: '',
    limb: '',
    q: '',
    col: null
  }};
  
  var routes = document.querySelectorAll('.map .route');
  var matchCounter = document.getElementById('match-counter');
  var searchInput = document.getElementById('q');
  var clearBtn = document.getElementById('clear-search');
  var colBtns = document.querySelectorAll('.shu-col-btn');
  var colDrawer = document.getElementById('col-drawer');
  var cdBadge = document.getElementById('cd-badge');
  var cdDesc = document.getElementById('cd-desc');
  var cdClose = document.getElementById('cd-close');
  
  var SHU_INFO = [
    {{
      title: 'Jing-Well · 井',
      desc: '<b>Where Qi emerges</b> like water welling from a spring (nail corners). Indicated for fullness below the heart, acute mental-emotional distress, and reviving consciousness.'
    }},
    {{
      title: 'Ying-Spring · 滎',
      desc: '<b>Where Qi trickles</b> like a small mountain stream (web margins). Indicated for heat in the body, fever, facial redness, and clearing seasonal pathogens.'
    }},
    {{
      title: 'Shu-Stream · 輸',
      desc: '<b>Where Qi pours</b> like a broad river (knuckles & metatarsals). Indicated for heaviness of the body, swollen joints, and damp-bi pain. <i>On Yin channels, Shu-Stream is also the Yuan-Source (原) point.</i>'
    }},
    {{
      title: 'Jing-River · 經',
      desc: '<b>Where Qi flows</b> deep and swiftly (forearms & calves). Indicated for cough, asthma, chills and alternating fever, and vocal disorders.'
    }},
    {{
      title: 'He-Sea · 合',
      desc: '<b>Where Qi unites</b> and plunges inward like a river into the ocean (elbows & knees). Indicated for counterflow Qi, stomach disease, diarrhea, and disorders of the Fu organs.'
    }}
  ];
  
  function updateFilter(){{
    var q = state.q.trim().toLowerCase();
    var visibleRoutes = 0;
    var matchedStationsCount = 0;
    
    // Clear matches
    document.querySelectorAll('.station.match').forEach(function(s){{ s.classList.remove('match'); }});
    
    routes.forEach(function(r){{
      var ch = r.getAttribute('data-ch');
      var el = r.getAttribute('data-el');
      var yy = r.getAttribute('data-yy');
      var limb = r.getAttribute('data-limb');
      
      var matchEl = !state.el || el === state.el;
      var matchYy = !state.yy || yy === state.yy;
      var matchLimb = !state.limb || limb === state.limb;
      
      var matchSearch = true;
      if(q){{
        var stations = r.querySelectorAll('.station');
        var chHasMatch = false;
        stations.forEach(function(st){{
          var code = st.getAttribute('data-code');
          var p = P[code];
          if(!p) return;
          var hay = [p.code, p.py, p.hz, p.en, p.shu, p.elem, p.chName, p.loc, p.note, p.yy, p.limb].join(' ').toLowerCase();
          if(hay.indexOf(q) >= 0 || hay.replace(/\\s/g,'').indexOf(q.replace(/\\s/g,'')) >= 0){{
            st.classList.add('match');
            chHasMatch = true;
            matchedStationsCount++;
          }}
        }});
        matchSearch = chHasMatch;
      }}
      
      var on = matchEl && matchYy && matchLimb && matchSearch;
      r.hidden = !on;
      if(on) visibleRoutes++;
    }});
    
    if(matchCounter){{
      if(q){{
        matchCounter.textContent = visibleRoutes + ' channels (' + matchedStationsCount + ' pts)';
      }} else {{
        matchCounter.textContent = visibleRoutes === 12 ? 'All 12 channels' : visibleRoutes + ' / 12 channels';
      }}
    }}
    
    if(clearBtn){{
      clearBtn.style.display = (q || state.el || state.yy || state.limb) ? 'block' : 'none';
    }}
  }}
  
  // Wire Segment Buttons
  function wireSeg(containerId, stateKey){{
    var box = document.getElementById(containerId);
    if(!box) return;
    box.addEventListener('click', function(e){{
      var b = e.target.closest('button');
      if(!b) return;
      var val = b.getAttribute('data-' + (stateKey === 'el' ? 'el' : stateKey === 'yy' ? 'yy' : 'limb'));
      state[stateKey] = val || '';
      box.querySelectorAll('button').forEach(function(x){{
        x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
      }});
      updateFilter();
      if(stateKey === 'el') syncUrl(state.el);
    }});
  }}
  
  wireSeg('f-el', 'el');
  wireSeg('f-yy', 'yy');
  wireSeg('f-limb', 'limb');
  
  // Wire Search
  if(searchInput){{
    var stTimer;
    searchInput.addEventListener('input', function(){{
      clearTimeout(stTimer);
      stTimer = setTimeout(function(){{
        state.q = searchInput.value;
        updateFilter();
      }}, 50);
    }});
  }}
  
  if(clearBtn){{
    clearBtn.addEventListener('click', function(){{
      state.q = '';
      state.el = '';
      state.yy = '';
      state.limb = '';
      if(searchInput) searchInput.value = '';
      document.querySelectorAll('.seg button').forEach(function(b){{
        var isAll = !b.getAttribute('data-el') && !b.getAttribute('data-yy') && !b.getAttribute('data-limb');
        b.setAttribute('aria-pressed', isAll ? 'true' : 'false');
      }});
      updateFilter();
      syncUrl('');
    }});
  }}
  
  // Column Harmony Drawer
  colBtns.forEach(function(btn){{
    btn.addEventListener('click', function(){{
      var rank = btn.getAttribute('data-rank');
      if(state.col === rank){{
        // Close
        state.col = null;
        colBtns.forEach(function(b){{ b.setAttribute('aria-pressed', 'false'); }});
        colDrawer.classList.remove('open');
        document.querySelectorAll('.station.col-active').forEach(function(s){{ s.classList.remove('col-active'); }});
      }} else {{
        state.col = rank;
        colBtns.forEach(function(b){{ b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); }});
        var info = SHU_INFO[+rank];
        cdBadge.innerHTML = info.title;
        cdDesc.innerHTML = info.desc;
        colDrawer.classList.add('open');
        
        document.querySelectorAll('.station').forEach(function(s){{
          s.classList.toggle('col-active', s.getAttribute('data-rank') === rank);
        }});
      }}
    }});
  }});
  
  if(cdClose){{
    cdClose.addEventListener('click', function(){{
      state.col = null;
      colBtns.forEach(function(b){{ b.setAttribute('aria-pressed', 'false'); }});
      colDrawer.classList.remove('open');
      document.querySelectorAll('.station.col-active').forEach(function(s){{ s.classList.remove('col-active'); }});
    }});
  }}
  
  // Station Popover Inspector
  var popover = document.getElementById('station-popover');
  var spCode = document.getElementById('sp-code');
  var spHz = document.getElementById('sp-hz');
  var spPy = document.getElementById('sp-py');
  var spEn = document.getElementById('sp-en');
  var spShu = document.getElementById('sp-shu');
  var spElemName = document.getElementById('sp-elem-name');
  var spCh = document.getElementById('sp-ch');
  var spNote = document.getElementById('sp-note');
  var spLocT = document.getElementById('sp-loc-t');
  var spCta = document.getElementById('sp-cta');
  
  var popoverTimer = 0, activeStation = null;
  
  function placePopover(target){{
    if(!popover) return;
    var r = target.getBoundingClientRect();
    var p = popover.getBoundingClientRect();
    var gap = 12;
    
    var x = Math.max(12, Math.min(r.left + r.width/2 - p.width/2, window.innerWidth - p.width - 12));
    var above = r.top - gap - p.height >= 10;
    var y = above ? (r.top - gap - p.height) : (r.bottom + gap);
    y = Math.max(10, Math.min(y, window.innerHeight - p.height - 10));
    
    popover.classList.toggle('below', !above);
    popover.style.left = Math.round(x) + 'px';
    popover.style.top = Math.round(y) + 'px';
  }}
  
  function showPopover(st){{
    var code = st.getAttribute('data-code');
    var p = P[code];
    if(!p || !popover) return;
    
    clearTimeout(popoverTimer);
    activeStation = st;
    
    spCode.textContent = p.code;
    spCode.className = 'sp-code ph-' + p.elem.toLowerCase();
    spHz.textContent = p.hz;
    spPy.textContent = p.py;
    spEn.textContent = p.en ? '“' + p.en + '”' : '';
    spShu.textContent = p.shu;
    spElemName.textContent = p.elem;
    spCh.textContent = p.chName + ' · ' + p.yy;
    spNote.textContent = p.note || '';
    spLocT.textContent = p.loc;
    spCta.href = p.file + '#' + p.code;
    spCta.textContent = 'Inspect ' + p.code + ' on Chart →';
    
    var dot = popover.querySelector('.sp-dot');
    if(dot) dot.style.background = 'var(--' + p.elem.toLowerCase() + ')';
    
    popover.classList.remove('on');
    placePopover(st);
    void popover.offsetWidth;
    popover.classList.add('on');
    popover.setAttribute('aria-hidden', 'false');
  }}
  
  function hidePopover(){{
    clearTimeout(popoverTimer);
    if(!popover) return;
    popover.classList.remove('on');
    popover.setAttribute('aria-hidden', 'true');
    activeStation = null;
  }}
  
  document.addEventListener('pointerover', function(e){{
    var st = e.target.closest('.station');
    if(st){{
      clearTimeout(popoverTimer);
      showPopover(st);
    }} else if(popover && !popover.contains(e.target)){{
      clearTimeout(popoverTimer);
      popoverTimer = setTimeout(hidePopover, 140);
    }}
  }});
  
  document.addEventListener('focusin', function(e){{
    var st = e.target.closest('.station');
    if(st) showPopover(st);
  }});
  
  document.addEventListener('focusout', function(e){{
    var st = e.target.closest('.station');
    if(st && (!popover || !popover.contains(e.relatedTarget))){{
      hidePopover();
    }}
  }});
  
  // Clicking anywhere outside hides popover
  document.addEventListener('pointerdown', function(e){{
    if(popover && !popover.contains(e.target) && !e.target.closest('.station')){{
      hidePopover();
    }}
  }});
  
  // Keyboard Shortcuts
  document.addEventListener('keydown', function(e){{
    if(e.key === 'Escape'){{
      hidePopover();
      if(state.col){{
        state.col = null;
        colBtns.forEach(function(b){{ b.setAttribute('aria-pressed', 'false'); }});
        colDrawer.classList.remove('open');
        document.querySelectorAll('.station.col-active').forEach(function(s){{ s.classList.remove('col-active'); }});
      }}
    }} else if(e.key === '/' && document.activeElement !== searchInput){{
      if(searchInput){{
        e.preventDefault();
        searchInput.focus();
      }}
    }}
  }});
  
  // URL Hash & Search Params Deep Linking
  function syncUrl(el){{
    try {{ history.replaceState(null, '', el ? '#'+el : location.pathname.split('/').pop()); }} catch(e) {{}}
  }}
  function fromUrl(){{
    var params = new URLSearchParams(location.search);
    var hash = location.hash.replace(/^#/, '');
    
    var el = params.get('el') || (/^(wood|fire|earth|metal|water)$/.test(hash) ? hash : '');
    var yy = params.get('yy') || '';
    var limb = params.get('limb') || '';
    var q = params.get('q') || '';
    var rank = params.get('rank') || '';
    
    if(el) state.el = el;
    if(yy) state.yy = yy;
    if(limb) state.limb = limb;
    if(q){{
      state.q = q;
      if(searchInput) searchInput.value = q;
    }}
    
    ['el', 'yy', 'limb'].forEach(function(k){{
      var box = document.getElementById('f-' + k);
      if(box && state[k]){{
        box.querySelectorAll('button').forEach(function(b){{
          b.setAttribute('aria-pressed', b.getAttribute('data-' + k) === state[k] ? 'true' : 'false');
        }});
      }}
    }});
    
    if(rank !== '' && +rank >= 0 && +rank <= 4){{
      var btn = document.querySelector('.shu-col-btn[data-rank="' + rank + '"]');
      if(btn) btn.click();
    }}
    
    updateFilter();
  }}
  
  window.addEventListener('hashchange', fromUrl);
  fromUrl();
  updateFilter();
}})();
</script>'''

# Combine full document
new_html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#0d101d">
<title>Channels · Shu Atlas</title>
<meta name="description" content="An interactive transit atlas of the five Shu points across the twelve primary channels — twelve routes, sixty stations, one click to each chart.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500&display=swap">
<style>
{styles}
<!-- favicon:start --><link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg%20xmlns=%22http://www.w3.org/2000/svg%22%20viewBox=%220%200%2032%2032%22%3E%3Crect%20width=%2232%22%20height=%2232%22%20rx=%227%22%20fill=%22%2310131f%22/%3E%3Ccircle%20cx=%2216%22%20cy=%2216%22%20r=%2212.5%22%20fill=%22%23f2f0ea%22%20stroke=%22%23f2f0ea%22%20stroke-width=%221.2%22/%3E%3Cpath%20d=%22M16%203.5a12.5%2012.5%200%200%201%200%2025a6.25%206.25%200%200%201%200-12.5a6.25%206.25%200%200%200%200-12.5z%22%20fill=%22%2310131f%22/%3E%3Ccircle%20cx=%2216%22%20cy=%229.75%22%20r=%222%22%20fill=%22%2310131f%22/%3E%3Ccircle%20cx=%2216%22%20cy=%2222.25%22%20r=%222%22%20fill=%22%23f2f0ea%22/%3E%3C/svg%3E"><!-- favicon:end -->
</head>
<body>
<div class="wrap">
<nav class="appnav" aria-label="Shu Atlas">
  <a class="home" href="index.html" aria-label="Shu Atlas home">
    <span class="han" lang="zh" aria-hidden="true">五輸</span>
    <span class="t">Shu Atlas</span>
  </a>
  <ul>
    <li><a class="l" href="index.html">Elements</a></li>
    <li><a class="l" href="channels.html" aria-current="page">Channels</a></li>
    <li><a class="l" href="points.html">Points</a></li>
    <li><a class="l" href="learn.html">Learn</a></li>
    <li><a class="l" href="study.html">Study</a></li>
  </ul>
</nav>

<header class="masthead">
  <div class="brand">
    <svg class="mark" viewBox="0 0 88 14" aria-hidden="true">
      <path d="M0 7h88" stroke="#f5f3ed" stroke-opacity=".38" stroke-width="1.5"/>
      <path d="M8 2v10" stroke="#3e7d5a" stroke-width="2.5"/>
      <path d="M26 2v10" stroke="#d23b2e" stroke-width="2.5"/>
      <path d="M44 2v10" stroke="#d99a2b" stroke-width="2.5"/>
      <path d="M62 2v10" stroke="#f5f3ed" stroke-width="2.5"/>
      <path d="M80 2v10" stroke="#3c6fbd" stroke-width="2.5"/>
    </svg>
    <h1>Five Shu <span class="han" lang="zh-Hant">五輸</span></h1>
    <p class="tagline">Interactive transit atlas of the twelve primary channels</p>
  </div>
  <div class="key">
    <span class="key-label">Phase inks</span>
    <ul class="phases">
      <li class="ph-wood" onclick="document.querySelector('#f-el button[data-el=\\'wood\\']').click()"><span class="sw" aria-hidden="true"></span>Wood</li>
      <li class="ph-fire" onclick="document.querySelector('#f-el button[data-el=\\'fire\\']').click()"><span class="sw" aria-hidden="true"></span>Fire</li>
      <li class="ph-earth" onclick="document.querySelector('#f-el button[data-el=\\'earth\\']').click()"><span class="sw" aria-hidden="true"></span>Earth</li>
      <li class="ph-metal" onclick="document.querySelector('#f-el button[data-el=\\'metal\\']').click()"><span class="sw" aria-hidden="true"></span>Metal</li>
      <li class="ph-water" onclick="document.querySelector('#f-el button[data-el=\\'water\\']').click()"><span class="sw" aria-hidden="true"></span>Water</li>
    </ul>
    <p class="polarity"><span><span class="pl" aria-hidden="true"></span>yang (Fu)</span><span><span class="pl pl-yin" aria-hidden="true"></span>yin (Zang)</span></p>
  </div>
</header>

<div class="controls-panel">
  <div class="search-wrap">
    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
    <input type="search" id="q" placeholder="Filter by code, name, category, or symptom (e.g. ST36, knee, source, Zusanli)..." autocomplete="off" spellcheck="false" aria-label="Search channels and points">
    <button type="button" class="clear-search-btn" id="clear-search" aria-label="Clear all filters">✕ Clear</button>
    <span class="count-badge" id="match-counter">All 12 channels</span>
  </div>
  <div class="filter-row">
    <div class="filter-group">
      <span class="filter-lbl">Element</span>
      <div class="seg" id="f-el" role="group" aria-label="Filter by element">
        <button type="button" data-el="" aria-pressed="true">All</button>
        <button type="button" class="ph-wood" data-el="wood"><span class="dot"></span>Wood</button>
        <button type="button" class="ph-fire" data-el="fire"><span class="dot"></span>Fire</button>
        <button type="button" class="ph-earth" data-el="earth"><span class="dot"></span>Earth</button>
        <button type="button" class="ph-metal" data-el="metal"><span class="dot"></span>Metal</button>
        <button type="button" class="ph-water" data-el="water"><span class="dot"></span>Water</button>
      </div>
    </div>
    <div class="filter-group">
      <span class="filter-lbl">Polarity</span>
      <div class="seg" id="f-yy" role="group" aria-label="Filter by polarity">
        <button type="button" data-yy="" aria-pressed="true">All</button>
        <button type="button" data-yy="yin">Yin (Zang 脏)</button>
        <button type="button" data-yy="yang">Yang (Fu 腑)</button>
      </div>
    </div>
    <div class="filter-group">
      <span class="filter-lbl">Limb</span>
      <div class="seg" id="f-limb" role="group" aria-label="Filter by limb">
        <button type="button" data-limb="" aria-pressed="true">All</button>
        <button type="button" data-limb="hand">Hand (Arm 手)</button>
        <button type="button" data-limb="foot">Foot (Leg 足)</button>
      </div>
    </div>
  </div>
</div>

<div class="colhead" id="colhead">
  <span class="term-head">Channel · terminus</span>
  <div class="colgrid" role="group" aria-label="Five Shu categories">
    <button type="button" class="shu-col-btn" data-rank="0" aria-label="Highlight Jing-Well points">
      <span class="shu-en">Well</span><span class="shu-han" lang="zh-Hant">井</span>
    </button>
    <button type="button" class="shu-col-btn" data-rank="1" aria-label="Highlight Ying-Spring points">
      <span class="shu-en">Spring</span><span class="shu-han" lang="zh-Hant">滎</span>
    </button>
    <button type="button" class="shu-col-btn" data-rank="2" aria-label="Highlight Shu-Stream points">
      <span class="shu-en">Stream</span><span class="shu-han" lang="zh-Hant">輸</span>
    </button>
    <button type="button" class="shu-col-btn" data-rank="3" aria-label="Highlight Jing-River points">
      <span class="shu-en">River</span><span class="shu-han" lang="zh-Hant">經</span>
    </button>
    <button type="button" class="shu-col-btn" data-rank="4" aria-label="Highlight He-Sea points">
      <span class="shu-en">Sea</span><span class="shu-han" lang="zh-Hant">合</span>
    </button>
  </div>
  <span></span>
</div>

<div class="col-drawer" id="col-drawer" aria-live="polite">
  <div class="col-drawer-in">
    <div class="col-drawer-left">
      <span class="col-drawer-badge" id="cd-badge">Jing-Well · 井</span>
      <p class="col-drawer-desc" id="cd-desc">Where Qi emerges like water from a mountain spring.</p>
    </div>
    <button type="button" class="col-drawer-close" id="cd-close" aria-label="Close harmonic drawer">✕ Close</button>
  </div>
</div>

<main class="map">
{all_routes_str}
</main>

<div class="station-popover" id="station-popover" role="dialog" aria-hidden="true">
  <div class="sp-in">
    <div class="sp-top">
      <div class="sp-left">
        <span class="sp-code" id="sp-code">ST36</span>
        <span class="sp-hz" id="sp-hz">足三里</span>
        <span class="sp-py" id="sp-py">Zusanli</span>
      </div>
      <span class="sp-en" id="sp-en">“Leg Three Li”</span>
    </div>
    <div class="sp-badges">
      <span class="sp-badge" id="sp-shu">He-Sea · 合</span>
      <span class="sp-badge"><span class="sp-dot"></span><span id="sp-elem-name">Earth</span></span>
      <span class="sp-badge" id="sp-ch">Stomach · Yang</span>
    </div>
    <p class="sp-note" id="sp-note">He-Sea point</p>
    <div class="sp-loc">
      <span class="sp-loc-lbl">Landmark</span>
      <p id="sp-loc-t">3 cun below ST35, one finger-breadth lateral to the anterior crest of the tibia.</p>
    </div>
    <div class="sp-foot">
      <span class="sp-hint">Click point to jump</span>
      <a class="sp-cta" id="sp-cta" href="#">Inspect on Chart →</a>
    </div>
  </div>
</div>

<footer class="notes">
  <p class="cycles"><span class="cycle"><span class="lb">Yin</span> runs <span class="ph-wood po">Wood</span> <span class="arr">→</span> <span class="ph-fire po">Fire</span> <span class="arr">→</span> <span class="ph-earth po">Earth</span> <span class="arr">→</span> <span class="ph-metal po">Metal</span> <span class="arr">→</span> <span class="ph-water po">Water</span></span><span class="sep" aria-hidden="true">·</span><span class="cycle"><span class="lb">Yang</span> runs <span class="ph-metal po">Metal</span> <span class="arr">→</span> <span class="ph-water po">Water</span> <span class="arr">→</span> <span class="ph-wood po">Wood</span> <span class="arr">→</span> <span class="ph-fire po">Fire</span> <span class="arr">→</span> <span class="ph-earth po">Earth</span>.</span> <span class="tail">Both cycles skip the Luo-Connecting and Xi-Cleft points.</span></p>
  <p>Every route runs Well → Sea, from the digits to just below the elbow or knee. The eight interactive overlay channels are LI, HT, SP, ST, LR, GB, KI and BL; LU, SI, PC and TB open the earlier chart format.</p>
  <p>Point categories were checked against the classical 五輸穴 tables and nalaayan.com’s per-point badges. Point-location charts are user-supplied; licensing review is pending before any public release.</p>
</footer>
</div>

{js_script}

{footer_snippet}
</body>
</html>
'''

(ROOT / 'channels.html').write_text(new_html, encoding='utf-8')
print("Successfully generated upgraded channels.html with deep linking and harmonic drawer!")
