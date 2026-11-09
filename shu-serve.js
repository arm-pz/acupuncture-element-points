const http = require('http');
const fs = require('fs');
const path = require('path');

// Channel charts: /lr, /gb … open the official meridian chart (/lr4 … aliases and *-v4-* file aliases are kept for legacy links); /lu opens the Lung chart.
const pages = {
  "/": "index.html",
  "/lr": "lr-meridian-chart.html", "/lr4": "lr-meridian-chart.html", "/lr-v4-meridian-chart.html": "lr-meridian-chart.html",
  "/gb": "gb-meridian-chart.html", "/gb4": "gb-meridian-chart.html", "/gb-v4-meridian-chart.html": "gb-meridian-chart.html",
  "/ht": "ht-meridian-chart.html", "/ht4": "ht-meridian-chart.html", "/ht-v4-meridian-chart.html": "ht-meridian-chart.html",
  "/si": "si-meridian-chart.html", "/si4": "si-meridian-chart.html", "/si-v4-meridian-chart.html": "si-meridian-chart.html",
  "/pc": "pc-meridian-chart.html", "/pc4": "pc-meridian-chart.html", "/pc-v4-meridian-chart.html": "pc-meridian-chart.html",
  "/tb": "tb-meridian-chart.html", "/tb4": "tb-meridian-chart.html", "/tb-v4-meridian-chart.html": "tb-meridian-chart.html",
  "/sp": "sp-meridian-chart.html", "/sp4": "sp-meridian-chart.html", "/sp-v4-meridian-chart.html": "sp-meridian-chart.html",
  "/st": "st-meridian-chart.html", "/st4": "st-meridian-chart.html", "/st-v4-meridian-chart.html": "st-meridian-chart.html",
  "/lu": "lung-meridian-chart.html", "/lu-meridian-chart.html": "lung-meridian-chart.html",
  "/li": "li-meridian-chart.html", "/li4": "li-meridian-chart.html", "/li-v4-meridian-chart.html": "li-meridian-chart.html",
  "/ki": "ki-meridian-chart.html", "/ki4": "ki-meridian-chart.html", "/ki-v4-meridian-chart.html": "ki-meridian-chart.html",
  "/bl": "bl-meridian-chart.html", "/bl4": "bl-meridian-chart.html", "/bl-v4-meridian-chart.html": "bl-meridian-chart.html"
};

// The app links between its pages by filename, so serve every routed file, and the
// app's own pages, under their file names as well as their short routes.
Object.assign(pages, {
  '/channels': 'channels.html',
  '/points': 'points.html',
  '/learn': 'learn.html',
  '/basics': 'basics.html',
  '/study': 'study.html'
});

const files = new Set(Object.values(pages));

http.createServer((req, res) => {
  const url = req.url.split('?')[0];
  const name = pages[url] || (files.has(url.slice(1)) ? url.slice(1) : null);
  if (!name) {
    res.writeHead(404);
    res.end('not found: start at /');
    return;
  }
  fs.readFile(path.join(__dirname, name), (e, d) => {
    if (e) {
      res.writeHead(404);
      res.end('not found');
    } else {
      res.writeHead(200, {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'no-store'
      });
      res.end(d);
    }
  });
}).listen(4174, '127.0.0.1', () => console.log('serving on http://127.0.0.1:4174'));
