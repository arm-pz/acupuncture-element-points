# Evidence: app shell (Elements, Channels and Points as one app)

Date: 2026-11-11. Branch: feature/app-shell. Run against the local server (node shu-serve.js).

```
$ python3 tools/sync-shell.py --check
shell blocks are up to date
$ python3 tools/sync-points.py --check
all pages match data/points.json
$ python3 tools/build-site.py
.build/worker.js: 20 pages, 62 routes, 2742 KiB
$ python3 tests/test_playwright_e2e.py http://127.0.0.1:4174
==================================================
 Running Playwright E2E Suite against: http://127.0.0.1:4174
==================================================
[PASS] Home Page Five Elements Hub (/): Status: 200, 5 discs rendered, CTA visible (2345ms)
[PASS] Channels 12 Routes & 60 Stations (/channels): 12 routes and 60 stations rendered (924ms)
[PASS] Station Inspector Popover (ST36 Hover): Popover active with details: 'ST36'
[PASS] Live Search Filter ('knee'): Search active: 1 highlighted station nodes, counter: '1 CHANNELS (1 PTS)'
[PASS] Faceted Filtering (Hand Yin Channels): Correctly isolated exactly 3 Hand Yin channels: ['HT', 'PC', 'LU']
[PASS] Harmonic Column View & Drawer: Stream column activated with harmonic drawer: 'Shu-Stream · 輸'
[PASS] Points Directory Search & Table (/points): Directory rendered 60 points with live filtering (719ms)
[PASS] Learn Curriculum & Glossary (/learn): Loaded modules with left rail curriculum (849ms)
[PASS] Active Recall Study Deck (/study): Quiz deck loaded with active recall interactions (545ms)
[PASS] Meridian Anatomy Chart (/lu): SVG anatomy rendered with 12 circles (687ms)
[PASS] Lung Gateway Cards & 4-Stage Waypoints: Verified premium Origin (LU1 Zhongfu), Terminus (LU11 Shaoshang), 4-stage waypoints
[PASS] Renamed LI Meridian Chart (20 Points & Gateway Cards): li-meridian-chart.html loads with 20 points, LI1 start, LI20 end
[PASS] Renamed Bladder Meridian Chart (67 Points & Gateway Cards): bl-meridian-chart.html loads with 67 points, BL1 start, BL67 end
[PASS] Legacy Aliases Compatibility: Both li-v4 and bl-v4 legacy URLs served with 200 OK
[PASS] Channels Page Enriched Badges & Peeks: All 12 channels display point count pills and start->end route peeks
[PASS] Mobile Viewport Banner Responsiveness: Banner displays cleanly on 390x844 mobile viewport
[PASS] Mobile Homepage Responsiveness: Homepage renders mobile layout with viewport tag, .phone styling and 5 elements
[PASS] Conception Vessel Chart (/cv): CV chart rendered with 5 element points, anatomy, and Nalaayan diagram images
[PASS] CV Hidden from Channels Directory: CV channel successfully hidden from Channels directory while primary 12 channels remain clean
[PASS] App Shell In-Place Views: Elements, Channels and Points swap with no reload; filter, search, ring and Back all hold
[PASS] App Shell Deep Link: A /points deep link reaches the ring and Channels in place
[PASS] App Shell Fixed Header: Brand and tabs sit at the same position on Elements, Channels and Points

==================================================
 Playwright Test Summary: 22 PASSED, 0 FAILED out of 22 tests
==================================================
```

Also checked by hand: 1280, 390 and 320 px wide with no sideways scroll; home view pixel-compared with the live site (only the header position differs); index.html opened from disk falls back to plain links.
