#!/usr/bin/env python3
"""Upgrade channels.html styling and tactile interactions."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
target = ROOT / 'channels.html'
s = target.read_text(encoding='utf-8')

# Update variables
s = s.replace('--ground:#10131f;', '--ground:#0d101d;')
s = s.replace('--ink:#f2f0ea;', '--ink:#f5f3ed;')
s = s.replace('--ink-2:#9aa4bb;', '--ink-2:#9ea8bd;')
s = s.replace('--hair:rgba(242,240,234,.13);', '--hair:rgba(245,243,237,.09);')

# Upgrade route styling
old_route = '.route{position:relative;display:grid;grid-template-columns:var(--term) minmax(0,1fr) var(--chev);align-items:stretch;min-height:var(--row);transition:background .18s ease,opacity .18s ease}'
new_route = '.route{position:relative;display:grid;grid-template-columns:var(--term) minmax(0,1fr) var(--chev);align-items:stretch;min-height:var(--row);border-radius:10px;padding:0 8px;transition:background-color .16s ease,transform .14s cubic-bezier(.16,1,.3,1),opacity .18s ease}'
s = s.replace(old_route, new_route)

# Upgrade route hover and active
old_hover = '.route:hover{background:rgba(242,240,234,.038)}'
new_hover = '.route:hover{background:rgba(245,243,237,.04);transform:translateX(3px)}\n.route:active{transform:scale(0.995)}'
s = s.replace(old_hover, new_hover)

# Upgrade station hover
old_station = '.station{position:relative;min-width:0}'
new_station = '.station{position:relative;min-width:0;transition:transform .15s cubic-bezier(.16,1,.3,1)}\n.station:hover .code{transform:translateY(-1px) scale(1.15);color:var(--tint);font-weight:600;filter:drop-shadow(0 0 5px var(--tint))}\n.station:hover .tick{transform:scaleY(1.25);filter:drop-shadow(0 0 5px var(--deep))}'
s = s.replace(old_station, new_station)

old_code = '.code{position:absolute;left:0;right:0;top:4px;text-align:center;font-family:var(--mono);font-size:11px;line-height:1.2;letter-spacing:.02em;color:var(--ink)}'
new_code = '.code{position:absolute;left:0;right:0;top:4px;text-align:center;font-family:var(--mono);font-size:11px;line-height:1.2;letter-spacing:.02em;color:var(--ink);transition:transform .15s cubic-bezier(.16,1,.3,1),color .15s ease,filter .15s ease}'
s = s.replace(old_code, new_code)

old_tick = '.tick{position:absolute;left:50%;top:19px;width:3px;height:18px;margin-left:-1.5px;background:var(--deep)}'
new_tick = '.tick{position:absolute;left:50%;top:19px;width:3px;height:18px;margin-left:-1.5px;background:var(--deep);transition:transform .15s cubic-bezier(.16,1,.3,1),filter .15s ease}'
s = s.replace(old_tick, new_tick)

# Upgrade badge
old_badge = '.badge{display:inline-flex;align-items:center;justify-content:center;flex:none;min-width:46px;height:26px;padding:0 6px;border-radius:3px;background:var(--tint);color:var(--ground);font-family:var(--mono);font-size:12.5px;letter-spacing:.04em}'
new_badge = '.badge{display:inline-flex;align-items:center;justify-content:center;flex:none;min-width:46px;height:26px;padding:0 6px;border-radius:6px;background:var(--tint);color:var(--ground);font-family:var(--mono);font-size:12.5px;font-weight:600;letter-spacing:.04em;box-shadow:0 2px 6px rgba(0,0,0,.3);transition:transform .15s cubic-bezier(.16,1,.3,1)}\n.route:hover .badge{transform:scale(1.05)}'
s = s.replace(old_badge, new_badge)

# Upgrade filter button
old_btn = '.filter button{appearance:none;border:0;background:transparent;color:var(--ink-2);font:500 12.5px/1 "Jost",system-ui,sans-serif;padding:8px 12px;border-radius:999px;cursor:pointer;display:inline-flex;align-items:center;gap:7px;transition:color .18s,background .18s}'
new_btn = '.filter button{appearance:none;border:0;background:transparent;color:var(--ink-2);font:500 12.5px/1 "Jost",system-ui,sans-serif;padding:8px 14px;border-radius:999px;cursor:pointer;display:inline-flex;align-items:center;gap:7px;transition:color .15s ease,background-color .15s ease,transform .12s cubic-bezier(.16,1,.3,1)}\n.filter button:hover{color:var(--ink);background:rgba(245,243,237,.06);transform:translateY(-1px)}\n.filter button:active{transform:scale(.95)}\n.filter button[aria-pressed="true"]{background:var(--ink);color:var(--ground);box-shadow:0 2px 8px rgba(0,0,0,.35);font-weight:600}'
s = s.replace(old_btn, new_btn)

# Upgrade colhead
old_colhead = '.colhead{display:grid;grid-template-columns:var(--term) minmax(0,1fr) var(--chev);align-items:end;padding:12px 0 9px;border-bottom:1px solid rgba(242,240,234,.26)}'
new_colhead = '.colhead{position:sticky;top:52px;z-index:8;background:rgba(13,16,29,.9);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);display:grid;grid-template-columns:var(--term) minmax(0,1fr) var(--chev);align-items:end;padding:12px 8px 9px;border-bottom:1px solid var(--hair)}'
s = s.replace(old_colhead, new_colhead)

target.write_text(s, encoding='utf-8')
print('Updated channels.html successfully!')
