const http = require('http');
const fs = require('fs');
const path = require('path');
const pages = { '/': 'index.html', '/lu': 'lung-meridian-chart.html', '/li': 'li-meridian-chart.html', '/li2': 'li-v2-meridian-chart.html', '/li3': 'li-v3-meridian-chart.html', '/li4': 'li-v4-meridian-chart.html', '/ht': 'ht-meridian-chart.html', '/ht2': 'ht-v2-meridian-chart.html', '/sp2': 'sp-v2-meridian-chart.html', '/sp3': 'sp-v3-meridian-chart.html', '/st2': 'st-v2-meridian-chart.html', '/st3': 'st-v3-meridian-chart.html', '/bl2': 'bl-v2-meridian-chart.html', '/bl3': 'bl-v3-meridian-chart.html', '/ki2': 'ki-v2-meridian-chart.html', '/ki3': 'ki-v3-meridian-chart.html', '/gb2': 'gb-v2-meridian-chart.html', '/gb3': 'gb-v3-meridian-chart.html', '/lr2': 'lr-v2-meridian-chart.html', '/lr3': 'lr-v3-meridian-chart.html', '/si': 'si-meridian-chart.html', '/pc': 'pc-meridian-chart.html', '/tb': 'tb-meridian-chart.html' };
http.createServer((req, res) => {
  const url = req.url.split('?')[0];
  const name = pages[url] || (url === '/index.html' ? 'index.html' : null);
  if (!name) { res.writeHead(404); res.end('use /lu, /li or /ht'); return; }
  fs.readFile(path.join(__dirname, name), (e, d) => {
    if (e) { res.writeHead(404); res.end('not found'); }
    else { res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' }); res.end(d); }
  });
}).listen(4174, '127.0.0.1', () => console.log('serving on http://127.0.0.1:4174'));
