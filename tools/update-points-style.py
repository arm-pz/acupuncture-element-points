#!/usr/bin/env python3
"""Upgrade points.html styling and micro-interactions."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
target = ROOT / 'points.html'
s = target.read_text(encoding='utf-8')

# Update tokens
s = s.replace(
    ':root{--ground:#10131f;--raise:#171b2a;--raise-2:#1d2233;--ink:#f2f0ea;--ink-2:#9aa4bb;--ink-3:#6c7590;--hair:rgba(242,240,234,.13);',
    ':root{--ground:#0d101d;--raise:#151928;--raise-2:#1e2338;--ink:#f5f3ed;--ink-2:#9ea8bd;--ink-3:#657088;--hair:rgba(245,243,237,.09);--hair-2:rgba(245,243,237,.18);'
)
s = s.replace('--mono:"IBM Plex Mono",ui-monospace,monospace;--ease:cubic-bezier(.22,1,.36,1);color-scheme:dark}',
              '--mono:"IBM Plex Mono",ui-monospace,monospace;--ease:cubic-bezier(.16,1,.3,1);color-scheme:dark}')

# App navigation upgrade to sticky blurred header
old_nav = '''.appnav{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 0;border-bottom:1px solid rgba(242,240,234,.13)}
.appnav .home{display:flex;align-items:baseline;gap:10px;color:#f2f0ea;text-decoration:none;min-width:0}
.appnav .home .han{font:300 19px/1 "Noto Sans SC","PingFang SC",sans-serif}
.appnav .home .t{font:500 11px/1 "Jost",system-ui,sans-serif;letter-spacing:.24em;text-transform:uppercase;color:#9aa4bb;white-space:nowrap}
.appnav ul{display:flex;gap:2px;list-style:none;margin:0;padding:0}
.appnav a.l{display:block;padding:8px 12px;border-radius:999px;font:500 13px/1 "Jost",system-ui,sans-serif;letter-spacing:.02em;color:#9aa4bb;text-decoration:none;transition:color .18s,background .18s}
.appnav a.l:hover{color:#f2f0ea;background:rgba(242,240,234,.06)}
.appnav a.l[aria-current="page"]{color:#10131f;background:#f2f0ea}
.appnav a:focus-visible{outline:2px solid #f2f0ea;outline-offset:2px}'''

new_nav = '''.appnav{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 0;border-bottom:1px solid var(--hair);position:sticky;top:0;z-index:100;background:rgba(13,16,29,.85);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
.appnav .home{display:flex;align-items:baseline;gap:10px;color:var(--ink);text-decoration:none;min-width:0;transition:opacity .16s var(--ease)}
.appnav .home:hover{opacity:.85}
.appnav .home:active{transform:scale(.98)}
.appnav .home .han{font:300 19px/1 "Noto Sans SC","PingFang SC",sans-serif}
.appnav .home .t{font:500 11px/1 "Jost",system-ui,sans-serif;letter-spacing:.24em;text-transform:uppercase;color:var(--ink-2);white-space:nowrap}
.appnav ul{display:flex;gap:2px;list-style:none;margin:0;padding:0}
.appnav a.l{display:block;padding:8px 12px;border-radius:999px;font:500 13px/1 "Jost",system-ui,sans-serif;letter-spacing:.02em;color:var(--ink-2);text-decoration:none;transition:color .16s var(--ease),background .16s var(--ease),transform .12s var(--ease)}
.appnav a.l:hover{color:var(--ink);background:rgba(245,243,237,.06)}
.appnav a.l:active{transform:scale(.96)}
.appnav a.l[aria-current="page"]{color:var(--ground);background:var(--ink);font-weight:600}
.appnav a:focus-visible{outline:2px solid var(--ink);outline-offset:2px}'''

s = s.replace(old_nav, new_nav)

# Controls upgrade
old_controls = '.controls{position:sticky;top:0;z-index:5;background:var(--ground);padding:18px 0 14px;margin-top:22px;border-bottom:1px solid var(--hair);display:flex;flex-direction:column;gap:12px}'
new_controls = '.controls{position:sticky;top:51px;z-index:90;background:rgba(13,16,29,.9);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);padding:16px 0 14px;margin-top:16px;border-bottom:1px solid var(--hair);display:flex;flex-direction:column;gap:12px}'
s = s.replace(old_controls, new_controls)

# Search upgrade
old_search = '''.search{position:relative}
.search input{width:100%;height:46px;padding:0 16px 0 44px;border-radius:12px;border:1px solid var(--hair);background:var(--raise);color:var(--ink);font:400 16px/1 "Jost",system-ui,sans-serif;transition:border-color .18s}
.search input::placeholder{color:var(--ink-3)}
.search input:focus{outline:none;border-color:rgba(242,240,234,.45)}
.search svg{position:absolute;left:15px;top:14px;width:18px;height:18px;color:var(--ink-3)}'''

new_search = '''.search{position:relative}
.search input{width:100%;height:48px;padding:0 16px 0 46px;border-radius:12px;border:1px solid var(--hair);background:var(--raise);color:var(--ink);font:400 15px/1 "Jost",system-ui,sans-serif;box-shadow:inset 0 1px 2px rgba(0,0,0,.25);transition:border-color .16s var(--ease),background .16s var(--ease),box-shadow .16s var(--ease)}
.search input::placeholder{color:var(--ink-3)}
.search input:focus{outline:none;border-color:rgba(245,243,237,.45);background:var(--raise-2);box-shadow:0 0 0 3px rgba(245,243,237,.08),inset 0 1px 2px rgba(0,0,0,.2)}
.search svg{position:absolute;left:16px;top:15px;width:18px;height:18px;color:var(--ink-3);pointer-events:none;transition:color .16s var(--ease)}
.search:focus-within svg{color:var(--ink)}'''

s = s.replace(old_search, new_search)

# Segments upgrade
old_seg = '''.seg{display:inline-flex;flex-wrap:wrap;gap:2px;padding:3px;border-radius:999px;background:var(--raise);border:1px solid var(--hair)}
.seg button{appearance:none;border:0;background:transparent;color:var(--ink-2);font:500 12.5px/1 "Jost",system-ui,sans-serif;padding:8px 12px;border-radius:999px;cursor:pointer;display:inline-flex;align-items:center;gap:7px;transition:color .18s,background .18s}
.seg button:hover{color:var(--ink)}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--ground)}'''

new_seg = '''.seg{display:inline-flex;flex-wrap:wrap;gap:2px;padding:3px;border-radius:999px;background:var(--raise);border:1px solid var(--hair);box-shadow:inset 0 1px 2px rgba(0,0,0,.2)}
.seg button{appearance:none;border:0;background:transparent;color:var(--ink-2);font:500 12.5px/1 "Jost",system-ui,sans-serif;padding:7px 12px;border-radius:999px;cursor:pointer;display:inline-flex;align-items:center;gap:7px;transition:color .15s ease,background .15s ease,transform .12s var(--ease)}
.seg button:hover{color:var(--ink);background:rgba(245,243,237,.05)}
.seg button:active{transform:scale(.95)}
.seg button[aria-pressed="true"]{background:var(--ink);color:var(--ground);box-shadow:0 1px 6px rgba(0,0,0,.35);font-weight:600}'''

s = s.replace(old_seg, new_seg)

# Point rows upgrade
old_pt = '''.pt{display:grid;grid-template-columns:68px minmax(0,1fr) 150px 120px 18px;gap:16px;align-items:center;padding:14px 10px;border-bottom:1px solid var(--hair);color:inherit;text-decoration:none;border-radius:8px;transition:background .18s}
.pt:hover{background:rgba(242,240,234,.04)}
.pt:hover .chev{opacity:1;transform:translateX(2px)}
.code{display:inline-flex;justify-content:center;align-items:center;height:26px;border-radius:4px;background:var(--tint);color:var(--ground);font:500 12.5px/1 var(--mono)}'''

new_pt = '''.pt{display:grid;grid-template-columns:68px minmax(0,1fr) 150px 120px 18px;gap:16px;align-items:center;padding:12px 14px;border:1px solid transparent;border-bottom:1px solid var(--hair);color:inherit;text-decoration:none;border-radius:10px;transition:background .16s var(--ease),border-color .16s var(--ease),transform .14s var(--ease),box-shadow .16s var(--ease)}
.pt:hover{background:var(--raise);border-color:rgba(245,243,237,.08);transform:translateX(3px);box-shadow:0 4px 16px -2px rgba(0,0,0,.35)}
.pt:active{transform:scale(.988) translateX(2px)}
.pt:hover .chev{opacity:1;transform:translateX(3px);color:var(--ink)}
.code{display:inline-flex;justify-content:center;align-items:center;height:26px;border-radius:6px;background:var(--tint);color:var(--ground);font:600 12.5px/1 var(--mono);box-shadow:0 2px 6px rgba(0,0,0,.28);transition:transform .14s var(--ease)}
.pt:hover .code{transform:scale(1.05)}'''

s = s.replace(old_pt, new_pt)

# Mark upgrade
old_mark = 'mark{background:rgba(242,240,234,.18);color:inherit;border-radius:2px}'
new_mark = 'mark{background:rgba(245,243,237,.22);color:var(--ink);border-radius:3px;padding:0 2px}'
s = s.replace(old_mark, new_mark)

target.write_text(s, encoding='utf-8')
print('Updated points.html successfully!')
