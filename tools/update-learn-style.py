#!/usr/bin/env python3
"""Upgrade learn.html styling and interactions."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
target = ROOT / 'learn.html'
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
.appnav a.l{display:block;padding:8px 12px;border-radius:999px;font:500 13px/1 "Jost",system-ui,sans-serif;letter-spacing:.02em;color:#9aa4bb;text-decoration:none;transition:color .18s var(--ease),background .18s var(--ease),transform .12s var(--ease)}
.appnav a.l:active{transform:scale(.97)}
.appnav a.l[aria-current="page"]{color:#10131f;background:#f2f0ea}
@media (hover:hover) and (pointer:fine){.appnav a.l:hover{color:#f2f0ea;background:rgba(242,240,234,.06)}}
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

# Rail upgrade
old_rail = '''.rail{position:sticky;top:18px;padding-top:2px}
.rail .rt{display:flex;justify-content:space-between;gap:10px;margin:0 0 12px;font:500 10px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
.rail .part{margin:17px 0 5px;font:500 9.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
.rail ol{list-style:none;margin:0;padding:0;display:grid;gap:1px}
.rail a{display:flex;align-items:baseline;gap:9px;padding:7px 8px;border-radius:8px;color:var(--ink-2);text-decoration:none;font-size:13px;line-height:1.3;transition:background .16s var(--ease),color .16s var(--ease)}
.rail a .n{flex:none;font:500 10px/1.5 var(--mono);letter-spacing:.04em;color:var(--ink-3)}
.rail a.active{background:rgba(242,240,234,.055);color:var(--ink)}'''

new_rail = '''.rail{position:sticky;top:66px;padding-top:2px}
.rail .rt{display:flex;justify-content:space-between;gap:10px;margin:0 0 12px;font:500 10px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
.rail .part{margin:17px 0 5px;font:500 9.5px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
.rail ol{list-style:none;margin:0;padding:0;display:grid;gap:2px}
.rail a{display:flex;align-items:baseline;gap:9px;padding:7px 10px;border-radius:8px;color:var(--ink-2);text-decoration:none;font-size:13px;line-height:1.3;transition:background .16s var(--ease),color .16s var(--ease),transform .14s var(--ease)}
.rail a .n{flex:none;font:500 10px/1.5 var(--mono);letter-spacing:.04em;color:var(--ink-3);transition:color .16s var(--ease)}
.rail a.active{background:rgba(245,243,237,.08);color:var(--ink);box-shadow:inset 2px 0 0 var(--ink)}
@media (hover:hover) and (pointer:fine){.rail a:hover{background:rgba(245,243,237,.05);color:var(--ink);transform:translateX(2px)}}'''

s = s.replace(old_rail, new_rail)

# Card upgrades
old_take = '.take{display:grid;grid-template-columns:auto minmax(0,1fr);gap:12px;align-items:start;background:var(--raise);border:1px solid var(--hair);border-radius:14px;padding:15px 16px;margin:20px 0 0}'
new_take = '.take{display:grid;grid-template-columns:auto minmax(0,1fr);gap:12px;align-items:start;background:var(--raise);border:1px solid var(--hair);border-radius:14px;padding:16px 18px;margin:20px 0 0;box-shadow:0 4px 18px -4px rgba(0,0,0,.35)}'
s = s.replace(old_take, new_take)

old_practice = '.practice{margin:20px 0 0;padding:16px 17px 15px;background:var(--raise);border:1px solid var(--hair);border-radius:14px}'
new_practice = '.practice{margin:20px 0 0;padding:18px 20px 16px;background:var(--raise);border:1px solid var(--hair);border-radius:14px;box-shadow:0 4px 18px -4px rgba(0,0,0,.35)}'
s = s.replace(old_practice, new_practice)

old_five = '.five article{background:var(--raise);border:1px solid var(--hair);border-radius:14px;padding:14px 13px 13px;display:flex;flex-direction:column}'
new_five = '.five article{background:var(--raise);border:1px solid var(--hair);border-radius:14px;padding:14px 13px 13px;display:flex;flex-direction:column;box-shadow:0 4px 18px -4px rgba(0,0,0,.3);transition:transform .18s var(--ease),border-color .18s var(--ease),box-shadow .18s var(--ease)}\n.five article:hover{transform:translateY(-2px);border-color:rgba(245,243,237,.18);box-shadow:0 8px 24px -4px rgba(0,0,0,.45)}'
s = s.replace(old_five, new_five)

old_names = '.names article{background:var(--raise);border:1px solid var(--hair);border-radius:14px;padding:15px;display:flex;flex-direction:column}'
new_names = '.names article{background:var(--raise);border:1px solid var(--hair);border-radius:14px;padding:15px;display:flex;flex-direction:column;box-shadow:0 4px 18px -4px rgba(0,0,0,.3);transition:transform .18s var(--ease),border-color .18s var(--ease),box-shadow .18s var(--ease)}\n.names article:hover{transform:translateY(-2px);border-color:rgba(245,243,237,.18);box-shadow:0 8px 24px -4px rgba(0,0,0,.45)}'
s = s.replace(old_names, new_names)

old_tablewrap = '.tablewrap{overflow-x:auto;margin:16px 0 0;border:1px solid var(--hair);border-radius:14px;background:var(--raise);-webkit-overflow-scrolling:touch}'
new_tablewrap = '.tablewrap{overflow-x:auto;margin:16px 0 0;border:1px solid var(--hair);border-radius:14px;background:var(--raise);box-shadow:0 4px 20px -4px rgba(0,0,0,.35);-webkit-overflow-scrolling:touch}'
s = s.replace(old_tablewrap, new_tablewrap)

old_work = '.work{background:var(--raise);border:1px solid var(--hair);border-radius:16px;padding:18px 18px 16px}'
new_work = '.work{background:var(--raise);border:1px solid var(--hair);border-radius:16px;padding:18px 18px 16px;box-shadow:0 4px 18px -4px rgba(0,0,0,.35)}'
s = s.replace(old_work, new_work)

old_btn = '.done-btn{display:inline-flex;align-items:center;gap:9px;height:38px;padding:0 15px;border-radius:999px;border:1px solid var(--hair);background:transparent;color:var(--ink);font:500 12.5px/1 "Jost",system-ui,sans-serif;cursor:pointer;transition:background .18s var(--ease),color .18s var(--ease),border-color .18s var(--ease),transform .12s var(--ease)}'
new_btn = '.done-btn{display:inline-flex;align-items:center;gap:9px;height:38px;padding:0 15px;border-radius:999px;border:1px solid var(--hair);background:transparent;color:var(--ink);font:500 12.5px/1 "Jost",system-ui,sans-serif;cursor:pointer;transition:all .16s var(--ease)}\n.done-btn:hover{background:rgba(245,243,237,.06);border-color:rgba(245,243,237,.25)}\n.done-btn:active{transform:scale(.95)}'
s = s.replace(old_btn, new_btn)

target.write_text(s, encoding='utf-8')
print('Updated learn.html successfully!')
