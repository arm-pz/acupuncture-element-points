const http = require('http');
const fs = require('fs');
const path = require('path');
// Channel charts: /lr, /gb … open the V4 chart (the /lr4 … aliases are kept for old links); /lu opens the Lung chart.
const pages = {"/": "index.html", "/lr": "lr-v4-meridian-chart.html", "/lr4": "lr-v4-meridian-chart.html", "/gb": "gb-v4-meridian-chart.html", "/gb4": "gb-v4-meridian-chart.html", "/ht": "ht-v4-meridian-chart.html", "/ht4": "ht-v4-meridian-chart.html", "/si": "si-v4-meridian-chart.html", "/si4": "si-v4-meridian-chart.html", "/pc": "pc-v4-meridian-chart.html", "/pc4": "pc-v4-meridian-chart.html", "/tb": "tb-v4-meridian-chart.html", "/tb4": "tb-v4-meridian-chart.html", "/sp": "sp-v4-meridian-chart.html", "/sp4": "sp-v4-meridian-chart.html", "/st": "st-v4-meridian-chart.html", "/st4": "st-v4-meridian-chart.html", "/lu": "lung-meridian-chart.html", "/li": "li-v4-meridian-chart.html", "/li4": "li-v4-meridian-chart.html", "/ki": "ki-v4-meridian-chart.html", "/ki4": "ki-v4-meridian-chart.html", "/bl": "bl-v4-meridian-chart.html", "/bl4": "bl-v4-meridian-chart.html"};
// The app links between its pages by filename, so serve every routed file, and the
// app's own pages, under their file names as well as their short routes.
Object.assign(pages, { '/channels': 'channels.html', '/points': 'points.html', '/learn': 'learn.html', '/basics': 'basics.html', '/study': 'study.html' });
const files = new Set(Object.values(pages));
http.createServer((req, res) => {
  const url = req.url.split('?')[0];
  const name = pages[url] || (files.has(url.slice(1)) ? url.slice(1) : null);
  if (!name) { res.writeHead(404); res.end('not found: start at /'); return; }
  fs.readFile(path.join(__dirname, name), (e, d) => {
    if (e) { res.writeHead(404); res.end('not found'); }
    else { res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' }); res.end(d); }
  });
}).listen(4174, '127.0.0.1', () => console.log('serving on http://127.0.0.1:4174'));
