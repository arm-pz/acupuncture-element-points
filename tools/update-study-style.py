#!/usr/bin/env python3
"""Upgrade study.html styling and tactile interactions."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
target = ROOT / 'study.html'
s = target.read_text(encoding='utf-8')

# Update variables
s = s.replace('--ground:#10131f;--raise:#171b2a;--raise-2:#1d2233;--ink:#f2f0ea;--ink-2:#9aa4bb;--ink-3:#6c7590;--hair:rgba(242,240,234,.13);',
              '--ground:#0d101d;--raise:#151928;--raise-2:#1e2338;--ink:#f5f3ed;--ink-2:#9ea8bd;--ink-3:#657088;--hair:rgba(245,243,237,.09);--hair-2:rgba(245,243,237,.20);')

s = s.replace('--mono:"IBM Plex Mono",ui-monospace,monospace;--ease:cubic-bezier(.22,1,.36,1);',
              '--mono:"IBM Plex Mono",ui-monospace,monospace;--ease:cubic-bezier(.16,1,.3,1);')

# Card upgrade
old_card = '.card{margin:22px 0 60px;background:var(--raise);border:1px solid var(--hair);border-radius:18px;padding:clamp(20px,4vw,36px);max-width:760px;box-shadow:0 20px 50px -24px rgba(0,0,0,.6)}'
new_card = '.card{margin:22px 0 60px;background:var(--raise);border:1px solid var(--hair);border-radius:20px;padding:clamp(22px,4vw,40px);max-width:780px;box-shadow:0 24px 60px -20px rgba(0,0,0,.75),0 0 0 1px rgba(255,255,255,.03);transition:box-shadow .2s var(--ease)}'
s = s.replace(old_card, new_card)

# Options upgrade
old_opt = '.opt{appearance:none;text-align:left;display:flex;align-items:center;gap:12px;min-height:56px;padding:12px 16px;border-radius:12px;border:1px solid var(--hair);background:var(--raise-2);color:var(--ink);font:500 16px/1.25 "Jost",system-ui,sans-serif;cursor:pointer;transition:border-color .18s,background .18s,transform .12s}'
new_opt = '.opt{appearance:none;text-align:left;display:flex;align-items:center;gap:14px;min-height:58px;padding:14px 18px;border-radius:14px;border:1px solid var(--hair);background:var(--raise-2);color:var(--ink);font:500 16px/1.25 "Jost",system-ui,sans-serif;cursor:pointer;transition:border-color .15s ease,background-color .15s ease,transform .12s var(--ease),box-shadow .15s ease}'
s = s.replace(old_opt, new_opt)

old_opt_hover = '.opt:hover:not(:disabled){border-color:rgba(242,240,234,.4)}'
new_opt_hover = '.opt:hover:not(:disabled){border-color:rgba(245,243,237,.35);background:rgba(245,243,237,.05);transform:translateY(-1px)}'
s = s.replace(old_opt_hover, new_opt_hover)

old_opt_active = '.opt:active:not(:disabled){transform:scale(.985)}'
new_opt_active = '.opt:active:not(:disabled){transform:scale(.96)}'
s = s.replace(old_opt_active, new_opt_active)

old_right = '.opt.right{border-color:#83c7a3;background:rgba(131,199,163,.14)}'
new_right = '.opt.right{border-color:#83c7a3;background:rgba(131,199,163,.18);box-shadow:0 0 16px rgba(131,199,163,.25)}'
s = s.replace(old_right, new_right)

old_wrong = '.opt.wrong{border-color:#f2968a;background:rgba(242,150,138,.12)}'
new_wrong = '.opt.wrong{border-color:#f2968a;background:rgba(242,150,138,.15);box-shadow:0 0 14px rgba(242,150,138,.2)}'
s = s.replace(old_wrong, new_wrong)

old_btn = '.btn{display:inline-flex;align-items:center;gap:8px;height:42px;padding:0 18px;border-radius:999px;border:1px solid var(--hair);background:transparent;color:var(--ink);font:500 14px/1 "Jost",system-ui,sans-serif;text-decoration:none;cursor:pointer}'
new_btn = '.btn{display:inline-flex;align-items:center;gap:8px;height:42px;padding:0 20px;border-radius:999px;border:1px solid var(--hair);background:transparent;color:var(--ink);font:500 14px/1 "Jost",system-ui,sans-serif;text-decoration:none;cursor:pointer;transition:all .15s var(--ease)}\n.btn:active{transform:scale(.96)}'
s = s.replace(old_btn, new_btn)

# Upgrade appnav in study.html to sticky blur
old_nav = '.appnav{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 0;border-bottom:1px solid rgba(242,240,234,.13)}'
new_nav = '.appnav{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:12px 0;border-bottom:1px solid var(--hair);position:sticky;top:0;z-index:100;background:rgba(13,16,29,.85);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px)}'
s = s.replace(old_nav, new_nav)

target.write_text(s, encoding='utf-8')
print('Updated study.html successfully!')
