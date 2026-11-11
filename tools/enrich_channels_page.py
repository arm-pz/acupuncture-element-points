#!/usr/bin/env python3
"""Enrich channels.html with total points count and start-to-end pathway indications."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = json.loads((ROOT / 'data' / 'points.json').read_text(encoding='utf-8'))
CHANNELS = {c['abbr']: c for c in DOC['channels']}

SHORT_TERMINI = {
    "LU": ("LU1 Chest", "LU11 Thumb"),
    "LI": ("LI1 Index", "LI20 Nose"),
    "ST": ("ST1 Eye", "ST45 2nd Toe"),
    "SP": ("SP1 Toe", "SP21 Ribcage"),
    "HT": ("HT1 Axilla", "HT9 Little Finger"),
    "SI": ("SI1 Finger", "SI19 Ear"),
    "BL": ("BL1 Inner Eye", "BL67 5th Toe"),
    "KI": ("KI1 Sole", "KI27 Clavicle"),
    "PC": ("PC1 Chest", "PC9 Mid Finger"),
    "TB": ("TB1 Ring Finger", "TB23 Eyebrow"),
    "GB": ("GB1 Outer Eye", "GB44 4th Toe"),
    "LR": ("LR1 Great Toe", "LR14 Ribcage")
}

channels_html_path = ROOT / 'channels.html'
html = channels_html_path.read_text(encoding='utf-8')

# 1. Update each route's terminus ident
for abbr, c in CHANNELS.items():
    start_sh, end_sh = SHORT_TERMINI[abbr]
    pts = c['pointsCount']
    
    # Target regex for this channel's terminus
    # <div class="route ... data-ch="XX" ...>
    # ... <span class="name">Name</span>
    # ... <span class="meta">...</span>
    pattern = rf'(data-ch="{abbr}"[^>]*>.*?<div class="terminus">.*?<span class="name">)(.*?)(</span>\s*<span class="meta">)(.*?)(</span>)'
    
    def repl(m):
        prefix = m.group(1)
        name_raw = re.sub(r'<span class="pts-tag">.*?</span>', '', m.group(2)).strip()
        mid = m.group(3)
        meta_raw = m.group(4)
        suffix = m.group(5)
        
        # Build enriched name and peek
        new_name = f'{name_raw} <span class="pts-tag">{pts} pts</span>'
        peek = f'<span class="route-peek" title="Origin: {c["startPoint"]} → Terminus: {c["endPoint"]}">{start_sh} → {end_sh}</span>'
        return f'{prefix}{new_name}{mid}{meta_raw}{suffix}\n        {peek}'

    # Check if route-peek already exists to avoid duplication
    if f'data-ch="{abbr}"' in html:
        # First clean any previous route-peek in this channel
        html = re.sub(rf'(data-ch="{abbr}"[^>]*>.*?<div class="terminus">.*?)\s*<span class="route-peek".*?</span>', r'\1', html, flags=re.S)
        html = re.sub(pattern, repl, html, count=1, flags=re.S)

# 2. Add CSS styles if not present
CSS = '''
/* Meridian Point Count Badge & Start-to-End Route Peek */
.name .pts-tag {
  display: inline-block;
  margin-left: 6px;
  padding: 1px 6px;
  border-radius: 999px;
  font: 500 10.5px/1.3 var(--mono);
  letter-spacing: .03em;
  color: var(--accent-t, #c89e52);
  background: rgba(245, 243, 237, 0.08);
  border: 1px solid var(--hair);
  vertical-align: middle;
}
.route-peek {
  display: block;
  font: 400 10.5px/1.35 var(--mono);
  letter-spacing: .02em;
  color: var(--ink-2);
  margin-top: 3px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  opacity: .85;
}
.route:hover .route-peek {
  opacity: 1;
  color: var(--ink);
}
@media (max-width: 600px) {
  .name .pts-tag {
    font-size: 9.5px;
    padding: 0 5px;
    margin-left: 4px;
  }
  .route-peek {
    font-size: 9.5px;
  }
}
'''

if '.name .pts-tag' not in html:
    html = html.replace('</style>', CSS + '\n</style>', 1)

channels_html_path.write_text(html, encoding='utf-8')
print("Successfully enriched channels.html with point badges and route peeks!")
