#!/usr/bin/env python3
"""Migrate all references from *-v4-meridian-chart.html to *-meridian-chart.html."""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Files to update
TARGET_FILES = [
    'channels.html',
    'points.html',
    'study.html',
    'learn.html',
    'index.html',
    'README.md',
    'shu-serve.js',
    'lung-meridian-chart.html',
    'tools/sync-chart-style.py',
    'tools/sync-footer.py',
    'tools/sync-glossary.py',
    'tools/sync-points.py',
    'tools/upgrade-channels.py',
    'tools/build-site.py'
]

# Add all meridian chart files
for p in ROOT.glob('*-meridian-chart.html'):
    if p.name not in TARGET_FILES:
        TARGET_FILES.append(p.name)

count = 0
for rel in TARGET_FILES:
    p = ROOT / rel
    if not p.exists():
        continue
    content = p.read_text(encoding='utf-8')
    new_content = content
    
    # Replace [xx]-v4-meridian-chart.html with [xx]-meridian-chart.html
    new_content = re.sub(r'([a-z]{2})-v4-meridian-chart\.html', r'\1-meridian-chart.html', new_content)
    
    # Specific tool glob updates: '*-v4-meridian-chart.html' -> '*-meridian-chart.html'
    new_content = new_content.replace("*-v4-meridian-chart.html", "*-meridian-chart.html")
    
    # In README.md: update text mentions of V4
    if rel == 'README.md':
        new_content = new_content.replace("The twelve chart pages are the V4 pages plus Lung; the older V1–V3 charts were removed", "The twelve chart pages are the official meridian charts")
    
    if new_content != content:
        p.write_text(new_content, encoding='utf-8')
        count += 1
        print(f"Updated references in {rel}")

print(f"Migration completed. {count} files updated.")
