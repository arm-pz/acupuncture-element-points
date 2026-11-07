#!/usr/bin/env python3
"""Upgrade glossary-snippet.html tooltip styling."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
snip = ROOT / 'tools' / 'glossary-snippet.html'
content = snip.read_text(encoding='utf-8')

old_part = content[content.find('.gl-tip{'):content.find('</style>')]
new_part = '''.gl-tip{position:fixed;z-index:100;left:0;top:0;width:min(280px,calc(100vw - 24px));padding:12px 14px 13px;border-radius:12px;background:rgba(21,25,40,.96);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);color:#f5f3ed;border:1px solid rgba(245,243,237,.14);box-shadow:0 20px 50px -15px rgba(0,0,0,.85),0 0 0 1px rgba(245,243,237,.06);font:400 13px/1.5 "Jost",system-ui,sans-serif;letter-spacing:.005em;text-align:left;text-transform:none;pointer-events:none;visibility:hidden;opacity:0;transform:translateY(4px);transition:opacity .15s cubic-bezier(.16,1,.3,1),transform .15s cubic-bezier(.16,1,.3,1)}
.gl-tip.on{visibility:visible;opacity:1;transform:none}
.gl-tip.below{transform:translateY(-4px)}
.gl-tip.on.below{transform:none}
.gl-tip-k{display:block;font:500 9.5px/1 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;color:#8590ab}
.gl-tip-t{display:flex;align-items:baseline;gap:8px;margin-top:7px;font-size:15px;font-weight:600;line-height:1.25}
.gl-tip-t span{font:300 15px/1 "Noto Sans SC","PingFang SC",sans-serif;color:#9ea8bd}
.gl-tip-d{display:block;margin-top:5px;color:#9ea8bd;line-height:1.45}
@media (prefers-reduced-motion:reduce){.gl-tip{transition:none}}
'''

snip.write_text(content.replace(old_part, new_part), encoding='utf-8')
print('Updated glossary snippet successfully!')
