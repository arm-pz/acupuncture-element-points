# Evidence: one scene from the ring to a point (redesign/one-forest)

Date: 2026-11-13. Branch: redesign/one-forest. Run against the local server (node shu-serve.js), Chromium via Playwright 1.63.

```
$ python3 tools/sync-shell.py --check
shell blocks are up to date
$ python3 tools/sync-chart-app.py --check
chart pages are up to date
$ python3 tools/sync-points.py --check
all pages match data/points.json
$ python3 tools/build-site.py
.build/worker.js: 20 pages, 62 routes, 3035 KiB
$ python3 tests/test_playwright_e2e.py http://127.0.0.1:4174
==================================================
 Running Playwright E2E Suite against: http://127.0.0.1:4174
==================================================
[PASS] Home Page Five Elements Hub (/): Status: 200, 5 discs rendered, CTA visible (2050ms)
[PASS] Channels 12 Routes & 60 Stations (/channels): 12 routes and 60 stations rendered (850ms)
[PASS] Station Inspector Popover (ST36 Hover): Popover active with details: 'ST36'
[PASS] Live Search Filter ('knee'): Search active: 1 highlighted station nodes, counter: '1 CHANNELS (1 PTS)'
[PASS] Faceted Filtering (Hand Yin Channels): Correctly isolated exactly 3 Hand Yin channels: ['HT', 'PC', 'LU']
[PASS] Harmonic Column View & Drawer: Stream column activated with harmonic drawer: 'Shu-Stream · 輸'
[PASS] Points Directory Search & Table (/points): Directory rendered 60 points with live filtering (733ms)
[PASS] Learn Curriculum & Glossary (/learn): Loaded modules with left rail curriculum (833ms)
[PASS] Active Recall Study Deck (/study): Quiz deck loaded with active recall interactions (526ms)
[PASS] Meridian Anatomy Chart (/lu): SVG anatomy rendered with 12 circles (526ms)
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
[PASS] Channel Page Phone Layout: Plate on first screen, card turns to the GB34 diagram and back, location text in view, sheet opens
[PASS] Channel Page Desktop Layout: Diagram sits beside its location; all 12 charts carry the line, 5 points and folded route block
[PASS] Phone Dock, Ring Labels, Weather and Scene: Dock at the bottom, labels on the ring, weather drawn, scene carried into Channels

==================================================
 Playwright Test Summary: 25 PASSED, 0 FAILED out of 25 tests
==================================================
```

The suite was run three times after the last change (this run and two before it), 25 of 25 each time. An earlier revision failed "App Shell In-Place Views" about one run in two: the parallax moved the title block, so the Explore button kept drifting and the ring auto-advanced before the click landed. The title no longer moves; a six-run repro of that path then held Fire every time.

Also checked by hand in the browser: Gallbladder, Lung, Stomach and Kidney charts at 390x844, 375x667, 360x600 (the short-screen flow layout) and 1440x900; the ring, Channels, Points and Learn at 390x844 and 1440x900. The plate SVG, the point diagrams (IMGS) and the point data (DATA) in all twelve charts were compared with main and are byte-identical. The Conception Vessel page, data/ and commons/ are unchanged.

Not tested: real devices (gyroscope parallax, iOS Safari sheet and dock), and the deployed Worker.
