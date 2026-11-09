#!/usr/bin/env python3
"""Sync high-effort meridian trajectory gateway cards and waypoint journeys into all 12 chart pages."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = json.loads((ROOT / 'data' / 'points.json').read_text(encoding='utf-8'))
CHANNELS = {c['file']: c for c in DOC['channels']}

BLOCK = re.compile(r'<!-- meridian-pathway:start -->.*?<!-- meridian-pathway:end -->\n*', re.S)

def make_banner(c):
    abbr = c['abbr']
    elem = c['elem']
    elem_lower = elem.lower()
    yy = c['yy']
    pts_count = c['pointsCount']
    course = c['course']
    tide = c.get('tide', '')
    
    start = c.get('startDetails', {
        'code': c['startPoint'].split()[0],
        'py': c['startPoint'].split()[1] if len(c['startPoint'].split()) > 1 else '',
        'hz': '',
        'en': '',
        'landmark': 'Channel Origin',
        'loc': c['startLoc']
    })
    
    end = c.get('endDetails', {
        'code': c['endPoint'].split()[0],
        'py': c['endPoint'].split()[1] if len(c['endPoint'].split()) > 1 else '',
        'hz': '',
        'en': '',
        'landmark': 'Channel Terminus',
        'loc': c['endLoc'],
        'handoff': ''
    })
    
    stages = c.get('stages', [
        {
            'num': '01',
            'title': 'Anatomical Course & Waypoints',
            'desc': c['pathway']
        }
    ])
    
    organs = c.get('organAffinities', {
        'primary': f"{c['name']} ({c['yy']})",
        'paired': 'Paired Channel Partner',
        'tissues': 'Muscles & Sinews'
    })
    
    # Handoff HTML for Terminus
    handoff_html = ''
    if end.get('handoff'):
        handoff_html = f'''
      <div class="gw-handoff">
        <span class="gw-handoff-icon" aria-hidden="true">⮑</span>
        <span>{end['handoff']}</span>
      </div>'''

    # Build Stage Cards
    stage_cards = []
    for s in stages:
        stage_cards.append(f'''      <div class="stage-card">
        <div class="stage-top">
          <span class="stage-badge">Stage {s['num']}</span>
          <span class="stage-name">{s['title']}</span>
        </div>
        <p class="stage-desc">{s['desc']}</p>
      </div>''')
    stages_html = '\n'.join(stage_cards)

    html = f'''<!-- meridian-pathway:start -->
<section class="meridian-path-banner" aria-label="Meridian Trajectory, Gateway Termini and Waypoint Journey" style="--c:var(--{elem_lower})">
  <!-- 1. Top Identity Bar -->
  <div class="mpb-topbar">
    <div class="mpb-topbar-left">
      <span class="mpb-elem-badge"><i class="mpb-elem-dot" style="--c:var(--{elem_lower})"></i>{elem} · {yy}</span>
      <span class="mpb-title">{c['name']} Meridian — Anatomical Trajectory</span>
    </div>
    <div class="mpb-topbar-right">
      <span class="mpb-tag"><strong class="num">{pts_count}</strong> Primary Points</span>
      <span class="mpb-tag">5 Five-Shu Points</span>
      <span class="mpb-tag mpb-tag-course">{course}</span>
    </div>
  </div>

  <!-- 2. Dual Gateway Cards (Origin & Terminus) with Visual Transit Conduit -->
  <div class="mpb-gateways">
    <!-- Origin Station Card -->
    <div class="gateway-card origin" style="border-left-color:var(--{elem_lower})">
      <div class="gw-header">
        <span class="gw-role"><span class="gw-dot origin" style="background:var(--{elem_lower});box-shadow:0 0 10px var(--{elem_lower})"></span>CHANNEL ORIGIN · 起穴</span>
        <span class="gw-landmark">{start['landmark']}</span>
      </div>
      <div class="gw-identity">
        <span class="gw-code" style="color:var(--{elem_lower})">{start['code']}</span>
        <div class="gw-naming">
          <div class="gw-names-row">
            <span class="gw-pinyin">{start['py']}</span>
            <span class="gw-hanzi">{start['hz']}</span>
          </div>
          <span class="gw-trans">“{start['en']}”</span>
        </div>
      </div>
      <div class="gw-loc">
        <span class="gw-loc-icon" aria-hidden="true">📍</span>
        <p>{start['loc']}</p>
      </div>
    </div>

    <!-- Center Transit Vector -->
    <div class="gw-conduit" aria-hidden="true">
      <div class="conduit-line" style="background:linear-gradient(90deg, var(--{elem_lower}), var(--accent-t))">
        <span class="conduit-pulse" style="background:var(--accent-t)"></span>
        <span class="conduit-arrow" style="color:var(--accent-t)">→</span>
      </div>
      <span class="conduit-label">{pts_count} Points Total</span>
    </div>

    <!-- Terminus Station Card -->
    <div class="gateway-card terminus" style="border-right-color:var(--accent-t)">
      <div class="gw-header">
        <span class="gw-role"><span class="gw-dot terminus"></span>CHANNEL TERMINUS · 止穴</span>
        <span class="gw-landmark">{end['landmark']}</span>
      </div>
      <div class="gw-identity">
        <span class="gw-code" style="color:var(--accent-t)">{end['code']}</span>
        <div class="gw-naming">
          <div class="gw-names-row">
            <span class="gw-pinyin">{end['py']}</span>
            <span class="gw-hanzi">{end['hz']}</span>
          </div>
          <span class="gw-trans">“{end['en']}”</span>
        </div>
      </div>
      <div class="gw-loc">
        <span class="gw-loc-icon" aria-hidden="true">📍</span>
        <p>{end['loc']}</p>
      </div>{handoff_html}
    </div>
  </div>

  <!-- 3. Journey Waypoints: How It Travels (Stage-by-Stage Milestone Route) -->
  <div class="mpb-journey">
    <div class="mpb-journey-header">
      <div class="mjh-title-group">
        <span class="mjh-icon" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        </span>
        <span class="mjh-title">How It Travels · Anatomical Route Waypoints</span>
      </div>
      <span class="mjh-hint">Sequential course from Origin to Terminus</span>
    </div>

    <div class="mpb-timeline">
{stages_html}
    </div>
  </div>

  <!-- 4. Organ Affinities & Circadian Tide Ribbon -->
  <div class="mpb-affinities">
    <div class="aff-item">
      <span class="aff-lbl">Primary Organ</span>
      <span class="aff-val"><i class="aff-dot primary"></i>{organs['primary']}</span>
    </div>
    <div class="aff-item">
      <span class="aff-lbl">Paired Organ</span>
      <span class="aff-val"><i class="aff-dot paired" style="background:var(--{elem_lower})"></i>{organs['paired']}</span>
    </div>
    <div class="aff-item">
      <span class="aff-lbl">Associated Tissues</span>
      <span class="aff-val">{organs['tissues']}</span>
    </div>
    <div class="aff-item">
      <span class="aff-lbl">Circadian Peak Tide</span>
      <span class="aff-val aff-val-mono">{tide}</span>
    </div>
  </div>
</section>
<!-- meridian-pathway:end -->
'''
    return html

count = 0
for filename, c in CHANNELS.items():
    path = ROOT / filename
    if not path.exists():
        continue
    txt = path.read_text(encoding='utf-8')
    banner = make_banner(c)
    
    if BLOCK.search(txt):
        new_txt = BLOCK.sub(banner, txt, count=1)
    else:
        layout_idx = txt.find('<div class="layout">')
        if layout_idx == -1:
            print(f"Error: could not find <div class=\"layout\"> in {filename}")
            continue
        new_txt = txt[:layout_idx] + banner + txt[layout_idx:]
        
    if new_txt != txt:
        path.write_text(new_txt, encoding='utf-8')
        count += 1
        print(f"Updated {filename} with premium gateway cards and multi-stage waypoints")

print(f"Synced premium meridian pathways to {count} chart pages.")
