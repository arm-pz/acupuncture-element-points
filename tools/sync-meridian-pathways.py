#!/usr/bin/env python3
"""Sync meridian trajectory, start/end locations, and point counts into all 12 chart pages."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = json.loads((ROOT / 'data' / 'points.json').read_text(encoding='utf-8'))
CHANNELS = {c['file']: c for c in DOC['channels']}

BLOCK = re.compile(r'<!-- meridian-pathway:start -->.*?<!-- meridian-pathway:end -->\n*', re.S)

def make_banner(c):
    start_pt = c['startPoint']
    end_pt = c['endPoint']
    start_sub = start_pt.split()[0]
    end_sub = end_pt.split()[0]
    organs_str = ', '.join(c.get('organs', []))
    
    html = f'''<!-- meridian-pathway:start -->
<section class="meridian-path-banner" aria-label="Meridian Trajectory and Points">
  <div class="mpb-grid">
    <div class="mpb-stat"><span class="mpb-label">Total Points</span><span class="mpb-val">{c['pointsCount']} <span class="mpb-sub">(5 Shu)</span></span></div>
    <div class="mpb-stat"><span class="mpb-label">Course</span><span class="mpb-val">{c['course']}</span></div>
    <div class="mpb-stat"><span class="mpb-label">Origin (Start)</span><span class="mpb-val">{c['startPoint']}</span></div>
    <div class="mpb-stat"><span class="mpb-label">Terminus (End)</span><span class="mpb-val">{c['endPoint']}</span></div>
  </div>
  <details class="mpb-details" open>
    <summary>
      <span class="mpb-sum-icon" aria-hidden="true">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
      </span>
      <span class="mpb-sum-title">Meridian Pathway &amp; Travel</span>
      <span class="mpb-sum-tag">{c['pointsCount']} Points Total</span>
    </summary>
    <div class="mpb-body">
      <div class="mpb-route-row">
        <span class="mpb-route-badge">Start</span>
        <span class="mpb-route-point">{c['startPoint']}</span>
        <span class="mpb-route-loc">{c['startLoc']}</span>
      </div>
      <div class="mpb-route-row">
        <span class="mpb-route-badge">End</span>
        <span class="mpb-route-point">{c['endPoint']}</span>
        <span class="mpb-route-loc">{c['endLoc']}</span>
      </div>
      <div class="mpb-desc">
        <p class="mpb-desc-lead"><strong>How it travels:</strong> {c['pathway']}</p>
        <p class="mpb-organs"><strong>Internal organ connections:</strong> {organs_str}</p>
      </div>
    </div>
  </details>
</section>
<!-- meridian-pathway:end -->
'''
    return html

count = 0
for filename, c in CHANNELS.items():
    path = ROOT / filename
    if not path.exists():
        print(f"Skipping missing file: {filename}")
        continue
    txt = path.read_text(encoding='utf-8')
    
    # 1. Update kicker with points badge
    # Base pattern matches <p class="kicker">...</p>
    def update_kicker(m):
        raw = m.group(1)
        # strip any existing badge-pts
        clean = re.sub(r'\s*·?\s*<span class="badge-pts">.*?</span>', '', raw).strip()
        return f'<p class="kicker">{clean} · <span class="badge-pts">{c["pointsCount"]} Points</span></p>'
        
    txt = re.sub(r'<p class="kicker">(.*?)</p>', update_kicker, txt, count=1)
    
    # 2. Insert or replace banner before <div class="layout">
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
        print(f"Updated {filename} with meridian pathway and {c['pointsCount']} points")

print(f"Synced meridian pathways to {count} chart pages.")
