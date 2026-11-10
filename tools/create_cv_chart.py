import sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

html_content = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500;600&family=Noto+Sans+SC:wght@300;400;500&display=swap"><title>Conception Vessel — Five Element Points</title>
<style>
:root{
  --ground:#0d101d;--raise:#151928;--raise-2:#1e2338;
  --ink:#f5f3ed;--ink-2:#9ea8bd;--ink-3:#657088;
  --hair:rgba(245,243,237,.09);--hair-2:rgba(245,243,237,.20);
  --wood:#3e885b;--fire:#d94236;--earth:#dca334;--metal:#e2dcce;--water:#3d78cc;
  --accent:#38bdf8;--accent-t:#7dd3fc;--accent-ring:rgba(56,189,248,.36);
  --ease:cubic-bezier(.16,1,.3,1);
  --spring:cubic-bezier(.19,1,.22,1);
  --mono:"IBM Plex Mono",ui-monospace,monospace;
  color-scheme:dark;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--ground);color:var(--ink);font:400 15px/1.5 "Jost",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.page{max-width:1100px;margin:0 auto;padding:0 clamp(16px,3vw,40px) 64px}
.kicker{margin:34px 0 8px;font:500 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-2)}
.badge-pts{display:inline-flex;padding:2px 7px;border-radius:999px;background:rgba(56,189,248,.12);border:1px solid rgba(56,189,248,.3);color:var(--accent-t);font-size:10.5px;letter-spacing:.08em}
h1{margin:0;font-size:clamp(28px,3.4vw,40px);font-weight:500;letter-spacing:-.01em;line-height:1.1}
.lede{margin:10px 0 28px;color:var(--ink-2);max-width:64ch}
.layout{display:grid;grid-template-columns:minmax(0,440px) minmax(0,1fr);gap:clamp(24px,4vw,44px);align-items:start}
.leg{position:relative;padding:14px;border-radius:16px;background:radial-gradient(115% 95% at 50% 12%,#1b233a 0%,#13182b 55%,#0d1120 100%);box-shadow:0 0 0 1px rgba(255,255,255,.07),0 0 0 5px rgba(245,243,237,.02),inset 0 -44px 64px -48px rgba(0,0,0,.8),0 28px 56px -24px rgba(0,0,0,.92);transition:box-shadow .24s var(--ease)}
.leg svg{display:block;width:100%;height:auto;overflow:visible}
#text-labels text{transition:fill .18s var(--ease),transform .18s var(--ease);font-weight:600;cursor:pointer}
#text-labels text.on{fill:var(--accent-t);font-weight:700;filter:drop-shadow(0 0 6px rgba(56,189,248,.7))}
#points circle{fill:#f43f5e;pointer-events:none;transform-box:fill-box;transform-origin:center;transition:transform .22s var(--ease),fill .22s var(--ease),filter .22s var(--ease)}
#points circle.hover{transform:scale(1.35);filter:drop-shadow(0 0 6px rgba(56,189,248,.8))}
#points circle.on{fill:var(--accent-t);transform:scale(1.5);filter:drop-shadow(0 0 8px var(--accent-ring))}
.hit{fill:transparent;cursor:pointer;outline:none}
.hit:focus-visible{stroke:#38bdf8;stroke-width:2}
.ring{fill:none;stroke:var(--accent-t);stroke-width:2.5;opacity:0;pointer-events:none;transform-box:fill-box;transform-origin:center}
.ring.on{opacity:1;animation:ring 2.4s var(--ease) infinite}
@keyframes ring{0%{transform:scale(.6);opacity:.95}70%,100%{transform:scale(1.65);opacity:0}}
.panel{position:sticky;top:20px;background:var(--raise);border:1px solid var(--hair);border-radius:16px;overflow:hidden;box-shadow:0 18px 40px -12px rgba(0,0,0,.68),0 0 0 1px rgba(255,255,255,.03)}
#pt-info{padding:22px 22px 18px;min-height:220px}
#pt-info.enter{animation:enter .22s var(--ease)}
@keyframes enter{from{opacity:0;transform:translateY(6px) scale(.99)}to{opacity:1;transform:none}}
.empty{display:flex;flex-direction:column;justify-content:center;min-height:178px;color:var(--ink-2);font-size:14.5px}
.empty b{display:block;color:var(--ink);font-size:18px;font-weight:500;margin-bottom:4px}
.eyebrow{display:flex;align-items:center;gap:8px;font:600 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--accent-t)}
.eyebrow .sep{width:3px;height:3px;border-radius:50%;background:var(--hair-2)}
.eyebrow .shu{color:var(--ink-2)}
.title{font-size:28px;line-height:1.15;letter-spacing:-.005em;font-weight:500;margin:12px 0 2px}
.en{color:var(--ink-2);font-size:15px}
.tamil-tag{display:inline-block;margin-left:6px;font-weight:500;color:var(--accent-t);font-size:14px}
.pills{display:flex;gap:6px;flex-wrap:wrap;margin:14px 0 0}
.pill{display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 11px;border-radius:999px;background:rgba(245,243,237,.07);font-size:12.5px;font-weight:500;letter-spacing:.02em;color:var(--ink);transition:background-color .15s ease}
.pill i{width:7px;height:7px;border-radius:50%;background:var(--c,var(--ink-3))}
.label{margin:20px 0 5px;font:500 11px/1 var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-2)}
.loc,.cun,.ind{margin:0;font-size:14.5px;line-height:1.55;color:var(--ink)}
.cun a{color:var(--accent-t);text-decoration:none;border-bottom:1px solid var(--accent-ring);padding-bottom:1px;margin-left:4px;white-space:nowrap;transition:border-color .15s ease,color .15s ease}
.cun a:hover{border-color:var(--accent-t)}
.pts{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:4px;padding:6px;margin:0;background:var(--raise-2);border-top:1px solid var(--hair)}
.chip{appearance:none;border:0;background:transparent;border-radius:10px;padding:9px 4px 8px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:4px;color:var(--ink-2);font-family:inherit;transition:background-color .16s ease,color .16s ease,transform .12s var(--ease)}
.chip:hover{background:rgba(245,243,237,.07);color:var(--ink);transform:translateY(-1px)}
.chip .s{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
.chip .c{font:600 12.5px/1 var(--mono);font-variant-numeric:tabular-nums}
.chip i{width:6px;height:6px;border-radius:50%;background:var(--c)}
.chip.on{background:var(--ink);color:var(--ground);box-shadow:0 2px 8px rgba(0,0,0,.35)}
.chip.on .s{color:#3a4156}
.chip:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.chip:active{transform:scale(.95)}
.note a{color:var(--accent-t);text-decoration:none;border-bottom:1px solid var(--accent-ring);transition:border-color .15s ease}
.note a:hover{border-color:var(--accent-t)}
.note{margin:36px 0 0;padding-top:16px;border-top:1px solid var(--hair);font-size:12.5px;line-height:1.6;color:var(--ink-3)}
@media (max-width:760px){
  h1{font-size:28px}
  .lede{margin-bottom:18px}
  .layout{grid-template-columns:1fr;gap:16px}
  .leg{max-width:420px;margin:0 auto;width:100%}
  .panel{position:static}
  #pt-info{min-height:0}
  .empty{min-height:0}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important}
  .ring.on{opacity:.6}
}

/* Appbar */
.appbar{border-bottom:1px solid var(--hair);background:rgba(13,16,29,.85);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);position:sticky;top:0;z-index:100}
.appbar .in{max-width:1100px;margin:0 auto;padding:12px clamp(16px,3vw,40px);display:flex;align-items:center;justify-content:space-between;gap:12px}
.appbar .home{display:flex;align-items:baseline;gap:10px;color:var(--ink);text-decoration:none;min-width:0;transition:opacity .15s ease}
.appbar .home:hover{opacity:.85}
.appbar .home .han{font:300 19px/1 "Noto Sans SC","PingFang SC",sans-serif}
.appbar .home .t{font:500 11px/1 "Jost",system-ui,sans-serif;letter-spacing:.24em;text-transform:uppercase;color:var(--ink-2);white-space:nowrap}
.appbar ul{display:flex;gap:4px;list-style:none;margin:0;padding:0}
.appbar a.l{display:block;padding:7px 13px;border-radius:999px;font:500 13px/1 "Jost",system-ui,sans-serif;letter-spacing:.02em;color:var(--ink-2);text-decoration:none;transition:color .15s ease,background-color .15s ease,transform .12s var(--ease)}
.appbar a.l:hover{color:var(--ink);background:rgba(245,243,237,.07);transform:translateY(-1px)}
.appbar a.l:active{transform:scale(.96)}
.appbar a.l.here{color:var(--ground);background:var(--ink);font-weight:600}
.appbar a:focus-visible,.pager a:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
.pager{display:flex;justify-content:space-between;gap:10px;margin:28px 0 0}
.pager a{display:inline-flex;align-items:center;gap:8px;height:34px;padding:0 15px;border-radius:999px;border:1px solid var(--hair);background:rgba(245,243,237,.03);font:500 13px/1 "Jost",system-ui,sans-serif;letter-spacing:.02em;color:var(--ink-2);text-decoration:none;transition:border-color .15s ease,color .15s ease,background-color .15s ease,transform .12s var(--ease)}
.pager a:hover{border-color:var(--hair-2);color:var(--ink);background:rgba(245,243,237,.07);transform:translateY(-1px)}
.pager a:active{transform:scale(.96)}
.pager i{width:7px;height:7px;border-radius:50%;background:var(--c)}
.pager .up{margin-right:auto}
@media (max-width:700px){
  .appbar .in{flex-wrap:wrap;justify-content:center;row-gap:6px}
  .appbar .home{width:100%;justify-content:center}
  .appbar .home .t{display:none}
  .appbar ul{flex-wrap:wrap;justify-content:center}
  .appbar a.l{padding:7px 10px;font-size:12.5px}
  .pager .nm{display:none}
}

/* Meridian Trajectory & Banner */
.meridian-path-banner{
  margin:22px 0 32px;
  background:linear-gradient(180deg,rgba(20,24,35,0.88) 0%,rgba(14,17,26,0.96) 100%);
  border:1px solid rgba(255,255,255,0.09);
  border-radius:18px;
  overflow:hidden;
  box-shadow:0 16px 40px -12px rgba(0,0,0,0.6),0 0 0 1px rgba(255,255,255,0.03) inset;
  backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);
  transition:border-color .25s ease,box-shadow .25s ease;
}
.meridian-path-banner:hover{
  border-color:rgba(255,255,255,0.16);
  box-shadow:0 20px 48px -12px rgba(0,0,0,0.7),0 0 0 1px rgba(255,255,255,0.06) inset;
}
.mpb-topbar{
  display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 22px;background:rgba(255,255,255,0.025);border-bottom:1px solid var(--hair);flex-wrap:wrap;
}
.mpb-topbar-left{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.mpb-elem-badge{
  display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:999px;font:600 11px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;background:rgba(56,189,248,0.1);border:1px solid rgba(56,189,248,0.25);color:var(--ink);
}
.mpb-elem-dot{width:7px;height:7px;border-radius:50%;background:var(--accent-t);box-shadow:0 0 8px var(--accent-t)}
.mpb-title{font:600 15px/1.2 "Jost",system-ui,sans-serif;letter-spacing:.01em;color:var(--ink)}
.mpb-topbar-right{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.mpb-tag{display:inline-flex;align-items:center;gap:4px;font:500 11.5px/1 var(--mono);letter-spacing:.04em;padding:4px 10px;border-radius:999px;background:rgba(255,255,255,0.04);border:1px solid var(--hair);color:var(--ink-2)}
.mpb-tag strong.num{font-weight:700;color:var(--accent-t)}
.mpb-tag-course{color:var(--ink);background:rgba(255,255,255,0.07)}

.mpb-gateways{
  display:grid;grid-template-columns:1fr auto 1fr;align-items:stretch;gap:18px;padding:22px;background:rgba(0,0,0,0.18);border-bottom:1px solid var(--hair);
}
.gateway-card{
  position:relative;background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);border-radius:14px;padding:18px 20px;display:flex;flex-direction:column;gap:12px;transition:transform .2s ease,border-color .2s ease,background-color .2s ease;
}
.gateway-card:hover{transform:translateY(-2px);border-color:rgba(255,255,255,0.14);background:rgba(255,255,255,0.04)}
.gateway-card.origin{border-left:3px solid var(--accent-t)}
.gateway-card.terminus{border-right:3px solid #f43f5e}
.gw-header{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap}
.gw-role{display:inline-flex;align-items:center;gap:7px;font:600 11px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-2)}
.gw-dot{width:8px;height:8px;border-radius:50%;display:inline-block}
.gw-dot.origin{background:var(--accent-t);box-shadow:0 0 10px var(--accent-t)}
.gw-dot.terminus{background:#f43f5e;box-shadow:0 0 10px #f43f5e}
.gw-landmark{font:500 11px/1.3 var(--mono);letter-spacing:.02em;padding:3px 8px;border-radius:6px;background:rgba(255,255,255,0.05);border:1px solid var(--hair);color:var(--accent-t)}
.gw-identity{display:flex;align-items:center;gap:14px;margin-top:2px}
.gw-code{font:700 24px/1 var(--mono);letter-spacing:.02em;padding:7px 14px;border-radius:10px;background:rgba(245,243,237,0.06);border:1px solid rgba(255,255,255,0.12);color:var(--ink);box-shadow:0 4px 12px rgba(0,0,0,0.35);flex-shrink:0}
.gw-naming{display:flex;flex-direction:column;gap:2px}
.gw-names-row{display:flex;align-items:baseline;gap:8px}
.gw-pinyin{font:600 18px/1.2 "Jost",system-ui,sans-serif;color:var(--ink);letter-spacing:.01em}
.gw-hanzi{font:400 17px/1 "Noto Sans SC","PingFang SC",sans-serif;color:var(--ink-2)}
.gw-trans{font-size:13px;font-style:italic;color:var(--ink-3)}
.gw-loc{display:flex;align-items:flex-start;gap:8px;font-size:13.5px;line-height:1.5;color:var(--ink-2);margin-top:auto}
.gw-loc p{margin:0}
.gw-handoff{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--accent-t);background:rgba(56,189,248,0.08);padding:6px 10px;border-radius:6px;border:1px solid rgba(56,189,248,0.2)}

.gw-conduit{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;padding:0 6px;min-width:110px}
.conduit-line{position:relative;width:100%;height:3px;background:linear-gradient(90deg,var(--accent-t),#f43f5e);border-radius:2px;overflow:visible}
.conduit-arrow{position:absolute;right:-6px;top:50%;transform:translateY(-50%);font:700 14px/1 var(--mono);color:#f43f5e}
.conduit-label{font:600 10.5px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);text-align:center}

.mpb-journey{padding:22px;border-bottom:1px solid var(--hair)}
.mpb-journey-header{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px;flex-wrap:wrap}
.mjh-title-group{display:flex;align-items:center;gap:10px}
.mjh-icon{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:8px;background:rgba(56,189,248,0.12);border:1px solid rgba(56,189,248,0.25);color:var(--accent-t)}
.mjh-title{font:600 14px/1.2 var(--mono);letter-spacing:.06em;text-transform:uppercase;color:var(--ink)}
.mjh-hint{font:400 12.5px/1.2 "Jost",system-ui,sans-serif;color:var(--ink-3)}
.mpb-timeline{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.stage-card{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:8px}
.stage-top{display:flex;align-items:baseline;justify-content:space-between;gap:8px}
.stage-badge{font:700 10px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--accent-t);background:rgba(56,189,248,0.1);padding:3px 6px;border-radius:4px}
.stage-name{font:600 13px/1.2 "Jost",system-ui,sans-serif;color:var(--ink)}
.stage-desc{margin:0;font-size:12.5px;line-height:1.55;color:var(--ink-2)}

.mpb-affinities{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--hair)}
.aff-item{background:rgba(14,17,26,0.96);padding:14px 18px;display:flex;flex-direction:column;gap:4px}
.aff-lbl{font:600 10.5px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3)}
.aff-val{font:500 13px/1.3 "Jost",system-ui,sans-serif;color:var(--ink);display:flex;align-items:center;gap:6px}
.aff-dot{width:6px;height:6px;border-radius:50%;display:inline-block;background:var(--accent-t)}

@media (max-width:960px){
  .mpb-gateways{grid-template-columns:1fr;gap:14px}
  .gw-conduit{flex-direction:row;padding:8px 0}
  .conduit-line{width:60px}
  .mpb-timeline{grid-template-columns:1fr 1fr}
  .mpb-affinities{grid-template-columns:1fr 1fr}
}
@media (max-width:600px){
  .mpb-timeline{grid-template-columns:1fr}
  .mpb-affinities{grid-template-columns:1fr}
  .mpb-topbar{padding:12px 14px}
  .mpb-gateways{padding:14px}
}
</style>
<link rel="icon" type="image/svg+xml" href="favicon.svg">
</head><body>
<header class="appbar"><div class="in"><a class="home" href="index.html" aria-label="Shu Atlas home"><span class="han" lang="zh" aria-hidden="true">五輸</span><span class="t">Shu Atlas</span></a><ul><li><a class="l" href="index.html">Elements</a></li><li><a class="l here" href="channels.html">Channels</a></li><li><a class="l" href="points.html">Points</a></li><li><a class="l" href="learn.html">Learn</a></li><li><a class="l" href="study.html">Study</a></li></ul></div></header>
<main class="page">
<nav class="pager" aria-label="Channels"><a class="up" href="channels.html">‹ Channels Directory</a><a href="bl-meridian-chart.html" aria-label="Channel 12: Bladder"><i style="--c:var(--water)"></i><span class="nm">Bladder</span> ←</a><a href="lung-meridian-chart.html" aria-label="Channel 1: Lung">→ <span class="nm">Lung</span><i style="--c:var(--metal)"></i></a></nav>
<p class="kicker">Extraordinary Vessel · Ren Mai (任脈) · <span class="badge-pts">24 Points</span></p>
<h1>Conception Vessel — Five Element Points</h1>
<p class="lede">Select an element point on the anterior midline, or choose an element below to inspect its anatomical location, cun measurement from the navel pit, and classical therapeutic actions.</p>

<!-- meridian-pathway:start -->
<section class="meridian-path-banner" aria-label="Meridian Trajectory and Waypoint Journey">
  <!-- 1. Top Identity Bar -->
  <div class="mpb-topbar">
    <div class="mpb-topbar-left">
      <span class="mpb-elem-badge"><i class="mpb-elem-dot"></i>Extraordinary Vessel · Ren Mai (任脈)</span>
      <span class="mpb-title">Conception Vessel — Anterior Midline Trajectory</span>
    </div>
    <div class="mpb-topbar-right">
      <span class="mpb-tag"><strong class="num">24</strong> Channel Points</span>
      <span class="mpb-tag"><strong class="num">5</strong> Five Element Points</span>
      <span class="mpb-tag mpb-tag-course">Perineum → Lower Lip (Centripetal Yin)</span>
    </div>
  </div>

  <!-- 2. Dual Gateway Cards -->
  <div class="mpb-gateways">
    <!-- Origin -->
    <div class="gateway-card origin">
      <div class="gw-header">
        <span class="gw-role"><span class="gw-dot origin"></span>VESSEL ORIGIN · 起穴</span>
        <span class="gw-landmark">Perineal Center · Pelvic Floor</span>
      </div>
      <div class="gw-identity">
        <span class="gw-code" style="color:var(--accent-t)">CV1</span>
        <div class="gw-naming">
          <div class="gw-names-row">
            <span class="gw-pinyin">Huiyin</span>
            <span class="gw-hanzi">會陰</span>
          </div>
          <span class="gw-trans">“Meeting of Yin”</span>
        </div>
      </div>
      <div class="gw-loc">
        <span class="gw-loc-icon" aria-hidden="true">📍</span>
        <p>In the center of the perineum, midway between the anus and the posterior scrotal root (men) or posterior labial commissure (women).</p>
      </div>
    </div>

    <!-- Center Transit Vector -->
    <div class="gw-conduit" aria-hidden="true">
      <div class="conduit-line">
        <span class="conduit-arrow">→</span>
      </div>
      <span class="conduit-label">24 Points Total</span>
    </div>

    <!-- Terminus -->
    <div class="gateway-card terminus">
      <div class="gw-header">
        <span class="gw-role"><span class="gw-dot terminus"></span>VESSEL TERMINUS · 止穴</span>
        <span class="gw-landmark">Mentolabial Groove · Chin</span>
      </div>
      <div class="gw-identity">
        <span class="gw-code" style="color:#f43f5e">CV24</span>
        <div class="gw-naming">
          <div class="gw-names-row">
            <span class="gw-pinyin">Chengjiang</span>
            <span class="gw-hanzi">承漿</span>
          </div>
          <span class="gw-trans">“Receiving Fluids”</span>
        </div>
      </div>
      <div class="gw-loc">
        <span class="gw-loc-icon" aria-hidden="true">📍</span>
        <p>In the depression in the center of the mentolabial groove, directly below the midpoint of the lower lip.</p>
      </div>
      <div class="gw-handoff">
        <span class="gw-handoff-icon" aria-hidden="true">⮑</span>
        <span>Internal branches encircle lips, meeting GV28 and ST1 infraorbital region</span>
      </div>
    </div>
  </div>

  <!-- 3. Journey Waypoints -->
  <div class="mpb-journey">
    <div class="mpb-journey-header">
      <div class="mjh-title-group">
        <span class="mjh-icon" aria-hidden="true">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        </span>
        <span class="mjh-title">How It Travels · Anatomical Route Waypoints</span>
      </div>
      <span class="mjh-hint">Sequential course along the anterior median line (Lineae Alba)</span>
    </div>

    <div class="mpb-timeline">
      <div class="stage-card">
        <div class="stage-top">
          <span class="stage-badge">Stage 01</span>
          <span class="stage-name">Pelvic Genesis & Pubic Ascent</span>
        </div>
        <p class="stage-desc">Originates in the lower pelvic cavity (uterus/Bao), emerges superficially at CV1 Huiyin in the perineum, ascends anteriorly through the pubic hair to CV2 Qugu at the superior margin of the pubic symphysis, passing through CV3 Zhongji and CV4 Guanyuan.</p>
      </div>
      <div class="stage-card">
        <div class="stage-top">
          <span class="stage-badge">Stage 02</span>
          <span class="stage-name">Lower Abdominal Element Gates</span>
        </div>
        <p class="stage-desc">Ascends along the lower abdominal midline through vital element points: CV5 Shimen (Fire, 2.5 cun below navel), CV6 Qihai (Water, 1.5 cun below navel), and CV7 Yinjiao (Wood, 1.0 cun below navel), reaching CV8 Shenque in the center of the umbilicus.</p>
      </div>
      <div class="stage-card">
        <div class="stage-top">
          <span class="stage-badge">Stage 03</span>
          <span class="stage-name">Epigastric Cavities & Sternal Course</span>
        </div>
        <p class="stage-desc">Continues upward from the navel pit through CV9 Shuifen (Metal/Air, 1.0 cun above), traverses CV12 Zhongwan, reaches CV13 Shangwan (Earth, 5.0 cun above navel), and ascends the sternal midline across CV17 Danzhong (Pericardium Front-Mu) to the throat.</p>
      </div>
      <div class="stage-card">
        <div class="stage-top">
          <span class="stage-badge">Stage 04</span>
          <span class="stage-name">Laryngeal Ascent & Mentolabial Lip</span>
        </div>
        <p class="stage-desc">Traverses the suprasternal fossa at CV22 Tiantu, climbs through the larynx and hyoid bone at CV23 Lianquan, reaches the chin, and terminates in the mentolabial groove depression at CV24 Chengjiang below the lower lip.</p>
      </div>
    </div>
  </div>

  <!-- 4. Vessel Affinities -->
  <div class="mpb-affinities">
    <div class="aff-item">
      <span class="aff-lbl">Master Confluent Point</span>
      <span class="aff-val"><i class="aff-dot"></i>LU7 (Lieque) coupled w/ KI6</span>
    </div>
    <div class="aff-item">
      <span class="aff-lbl">Vessel Nature</span>
      <span class="aff-val"><i class="aff-dot"></i>Sea of All Yin Channels (陰脈之海)</span>
    </div>
    <div class="aff-item">
      <span class="aff-lbl">Governing Sphere</span>
      <span class="aff-val">Conception, Uterus, Jing & Dantian</span>
    </div>
    <div class="aff-item">
      <span class="aff-lbl">Alarm (Mu) Hub</span>
      <span class="aff-val">Houses 6 Front-Mu Points (LU, PC, HT, ST, SI, BL)</span>
    </div>
  </div>
</section>
<!-- meridian-pathway:end -->

<div class="layout">
<div class="leg">
<svg viewBox="0 0 576 1024" role="group" aria-label="Conception Vessel chart showing its 5 Element Points" version="1.1" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Torso shading gradients -->
    <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#141a2e" stop-opacity="0.8"/>
      <stop offset="30%" stop-color="#1e2642" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#263154" stop-opacity="0.3"/>
      <stop offset="70%" stop-color="#1e2642" stop-opacity="0.5"/>
      <stop offset="100%" stop-color="#141a2e" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="ribGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#475569" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#334155" stop-opacity="0.1"/>
    </linearGradient>
    <linearGradient id="channelGlow" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%" stop-color="#0284c7"/>
      <stop offset="50%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#f43f5e"/>
    </linearGradient>
  </defs>

  <!-- ANATOMICAL TORSO SILHOUETTE & LANDMARKS -->
  <g id="torso-anatomy">
    <!-- Head outline (chin & jaw) -->
    <path d="M 235 90 C 235 60, 341 60, 341 90 C 341 125, 335 155, 305 175 C 295 180, 281 180, 271 175 C 241 155, 235 125, 235 90 Z" fill="#1b233a" stroke="#334155" stroke-width="1.5" opacity="0.6"/>
    <!-- Lips -->
    <path d="M 276 155 Q 288 152 300 155" fill="none" stroke="#64748b" stroke-width="1.8"/>
    <path d="M 279 162 Q 288 165 297 162" fill="none" stroke="#64748b" stroke-width="1.8"/>
    <!-- Mentolabial groove depression -->
    <path d="M 282 170 Q 288 172 294 170" fill="none" stroke="#38bdf8" stroke-width="1.5" opacity="0.8"/>

    <!-- Neck & Trapezius slope -->
    <path d="M 248 168 L 246 220 C 215 230, 160 250, 110 270 L 105 320" fill="none" stroke="#334155" stroke-width="1.8"/>
    <path d="M 328 168 L 330 220 C 361 230, 416 250, 466 270 L 471 320" fill="none" stroke="#334155" stroke-width="1.8"/>

    <!-- Clavicles (Collar bones) -->
    <path d="M 276 258 Q 230 252 135 272" fill="none" stroke="#475569" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M 300 258 Q 346 252 441 272" fill="none" stroke="#475569" stroke-width="2.2" stroke-linecap="round"/>
    <!-- Suprasternal notch (CV22 fossa) -->
    <path d="M 276 256 Q 288 266 300 256" fill="none" stroke="#38bdf8" stroke-width="2"/>

    <!-- Torso lateral body contour -->
    <path d="M 125 320 C 130 380, 140 460, 150 540 C 158 600, 155 650, 145 710 C 138 750, 145 800, 165 850 C 185 895, 210 930, 230 960 L 255 960 C 265 910, 280 890, 288 880 C 296 890, 311 910, 321 960 L 346 960 C 366 930, 391 895, 411 850 C 431 800, 438 750, 431 710 C 421 650, 418 600, 426 540 C 436 460, 446 380, 451 320" fill="url(#bodyGrad)" stroke="#334155" stroke-width="2"/>

    <!-- Sternum bone plate -->
    <path d="M 280 262 L 296 262 L 293 480 L 288 490 L 283 480 Z" fill="#1e293b" stroke="#475569" stroke-width="1.5" opacity="0.6"/>
    <!-- Infrasternal angle (Costal arch / Subcostal margins) -->
    <path d="M 288 490 Q 240 520 185 580" fill="none" stroke="#475569" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M 288 490 Q 336 520 391 580" fill="none" stroke="#475569" stroke-width="2.2" stroke-linecap="round"/>
    
    <!-- Schematic ribs (matching the user's book pages 245-246) -->
    <g opacity="0.35" stroke="#64748b" stroke-width="1.5" fill="none">
      <path d="M 292 340 Q 350 345 425 375"/>
      <path d="M 292 375 Q 350 380 415 415"/>
      <path d="M 292 410 Q 350 418 405 455"/>
      <path d="M 290 445 Q 345 455 395 495"/>
      <path d="M 288 475 Q 340 488 385 535"/>
      <!-- Left ribs -->
      <path d="M 284 340 Q 226 345 151 375"/>
      <path d="M 284 375 Q 226 380 161 415"/>
      <path d="M 284 410 Q 226 418 171 455"/>
      <path d="M 286 445 Q 231 455 181 495"/>
      <path d="M 288 475 Q 236 488 191 535"/>
    </g>

    <!-- Iliac crest & Pelvis outlines (from user book page 244) -->
    <path d="M 152 740 C 180 740, 205 770, 215 810 C 225 850, 245 880, 288 880" fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="4,3" opacity="0.5"/>
    <path d="M 424 740 C 396 740, 371 770, 361 810 C 351 850, 331 880, 288 880" fill="none" stroke="#475569" stroke-width="2" stroke-dasharray="4,3" opacity="0.5"/>
    <!-- Pubic symphysis upper border -->
    <rect x="272" y="876" width="32" height="12" rx="4" fill="#334155" stroke="#64748b" stroke-width="1.5" opacity="0.7"/>

    <!-- Navel Pit / Umbilicus (CV8 Shenque landmark: 0 cun center) -->
    <ellipse cx="288" cy="730" rx="9" ry="11" fill="#0f172a" stroke="#38bdf8" stroke-width="2"/>
    <ellipse cx="288" cy="730" rx="4" ry="5" fill="#38bdf8" opacity="0.8"/>
  </g>

  <!-- CUN MEASUREMENT RULERS (matching book pages 244-246) -->
  <g id="cun-rulers" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#94a3b8;">
    <!-- Upper Cun Ruler: 0 to 8 cun (Navel y=730 to Infrasternal angle y=490) -->
    <line x1="225" y1="730" x2="225" y2="490" stroke="#475569" stroke-width="1.8"/>
    <!-- Ticks -->
    <line x1="220" y1="730" x2="230" y2="730" stroke="#38bdf8" stroke-width="2"/>
    <text x="212" y="734" text-anchor="end" font-weight="600" fill="#38bdf8">0</text>

    <line x1="221" y1="700" x2="229" y2="700" stroke="#e2dcce" stroke-width="1.8"/>
    <text x="212" y="704" text-anchor="end" font-weight="600" fill="#e2dcce">1</text>

    <line x1="223" y1="670" x2="227" y2="670" stroke="#64748b" stroke-width="1.2"/>
    <line x1="223" y1="640" x2="227" y2="640" stroke="#64748b" stroke-width="1.2"/>
    <line x1="221" y1="610" x2="229" y2="610" stroke="#64748b" stroke-width="1.4"/>
    <text x="212" y="614" text-anchor="end">4</text>

    <line x1="221" y1="580" x2="229" y2="580" stroke="#dca334" stroke-width="1.8"/>
    <text x="212" y="584" text-anchor="end" font-weight="600" fill="#dca334">5</text>

    <line x1="223" y1="550" x2="227" y2="550" stroke="#64748b" stroke-width="1.2"/>
    <line x1="223" y1="520" x2="227" y2="520" stroke="#64748b" stroke-width="1.2"/>

    <line x1="220" y1="490" x2="230" y2="490" stroke="#94a3b8" stroke-width="2"/>
    <text x="212" y="494" text-anchor="end" font-weight="600">8</text>
    <text x="200" y="475" text-anchor="end" font-size="9.5" fill="#64748b">8 cun (Sternum)</text>

    <!-- Lower Cun Ruler: 0 to 5 cun (Navel y=730 to Pubic Symphysis y=880) -->
    <line x1="225" y1="730" x2="225" y2="880" stroke="#475569" stroke-width="1.8"/>
    <!-- 1.0 cun below (CV7 Wood) -->
    <line x1="221" y1="760" x2="229" y2="760" stroke="#3e885b" stroke-width="1.8"/>
    <text x="212" y="764" text-anchor="end" font-weight="600" fill="#3e885b">1.0</text>

    <!-- 1.5 cun below (CV6 Water) -->
    <line x1="221" y1="775" x2="229" y2="775" stroke="#3d78cc" stroke-width="1.8"/>
    <text x="212" y="779" text-anchor="end" font-weight="600" fill="#3d78cc">1.5</text>

    <!-- 2.5 cun below (CV5 Fire) -->
    <line x1="221" y1="805" x2="229" y2="805" stroke="#d94236" stroke-width="1.8"/>
    <text x="212" y="809" text-anchor="end" font-weight="600" fill="#d94236">2.5</text>

    <!-- 3.0 & 4.0 cun below -->
    <line x1="223" y1="820" x2="227" y2="820" stroke="#64748b" stroke-width="1.2"/>
    <line x1="223" y1="850" x2="227" y2="850" stroke="#64748b" stroke-width="1.2"/>

    <!-- 5.0 cun below (Pubic bone) -->
    <line x1="220" y1="880" x2="230" y2="880" stroke="#94a3b8" stroke-width="2"/>
    <text x="212" y="884" text-anchor="end" font-weight="600">5.0</text>
    <text x="200" y="898" text-anchor="end" font-size="9.5" fill="#64748b">5 cun (Pubis)</text>
  </g>

  <!-- CONCEPTION VESSEL CHANNEL PATHWAY -->
  <g id="meridian-channel">
    <!-- Glowing background conduit -->
    <line x1="288" y1="910" x2="288" y2="165" stroke="rgba(56,189,248,0.2)" stroke-width="10" stroke-linecap="round"/>
    <!-- Main energetic channel line -->
    <line id="channel" x1="288" y1="910" x2="288" y2="165" stroke="url(#channelGlow)" stroke-width="3.5" stroke-linecap="round"/>
  </g>

  <!-- LANDMARK REFERENCE POINTS (faint dots) -->
  <g id="ref-points" fill="#64748b" opacity="0.65">
    <circle cx="288" cy="910" r="3.5"/><!-- CV1 Huiyin -->
    <text x="275" y="913" text-anchor="end" font-family="'IBM Plex Mono',monospace" font-size="9.5" fill="#64748b">CV1 Huiyin</text>
    <circle cx="288" cy="880" r="3.5"/><!-- CV2 Qugu -->
    <circle cx="288" cy="850" r="3.5"/><!-- CV3 Zhongji -->
    <circle cx="288" cy="820" r="3.5"/><!-- CV4 Guanyuan -->
    <circle cx="288" cy="610" r="3.5"/><!-- CV12 Zhongwan -->
    <text x="300" y="613" text-anchor="start" font-family="'IBM Plex Mono',monospace" font-size="9.5" fill="#64748b">CV12 Zhongwan</text>
    <circle cx="288" cy="410" r="4"/><!-- CV17 Danzhong -->
    <text x="300" y="413" text-anchor="start" font-family="'IBM Plex Mono',monospace" font-size="9.5" fill="#64748b">CV17 Danzhong</text>
    <circle cx="288" cy="260" r="4"/><!-- CV22 Tiantu -->
    <text x="300" y="263" text-anchor="start" font-family="'IBM Plex Mono',monospace" font-size="9.5" fill="#64748b">CV22 Tiantu</text>
    <circle cx="288" cy="170" r="4.5" fill="#f43f5e" opacity="1"/><!-- CV24 Chengjiang -->
    <text x="302" y="174" text-anchor="start" font-family="'IBM Plex Mono',monospace" font-size="10.5" font-weight="600" fill="#f43f5e">CV24 Terminus</text>
  </g>

  <!-- 5 ELEMENT POINTS (CIRCLES) -->
  <g id="points">
    <!-- Earth: CV13 Shangwan (5 cun above navel) -->
    <circle id="p13" cx="288" cy="580" r="8" style="fill:var(--earth);stroke:#0d101d;stroke-width:2;"/>
    <!-- Metal / Air: CV9 Shuifen (1 cun above navel) -->
    <circle id="p9" cx="288" cy="700" r="8" style="fill:var(--metal);stroke:#0d101d;stroke-width:2;"/>
    <!-- Wood: CV7 Yinjiao (1 cun below navel) -->
    <circle id="p7" cx="288" cy="760" r="8" style="fill:var(--wood);stroke:#0d101d;stroke-width:2;"/>
    <!-- Water: CV6 Qihai (1.5 cun below navel) -->
    <circle id="p6" cx="288" cy="775" r="8" style="fill:var(--water);stroke:#0d101d;stroke-width:2;"/>
    <!-- Fire: CV5 Shimen (2.5 cun below navel) -->
    <circle id="p5" cx="288" cy="805" r="8" style="fill:var(--fire);stroke:#0d101d;stroke-width:2;"/>
  </g>

  <!-- CALLOUT LEADER LINES -->
  <g id="callout-lines" style="fill:none;stroke:#64748b;stroke-width:1.2;stroke-dasharray:3,2;">
    <!-- CV13 (Earth) -> Right -->
    <path d="M 296 580 L 375 580"/>
    <!-- CV9 (Air/Metal) -> Right -->
    <path d="M 296 700 L 375 700"/>
    <!-- CV7 (Wood) -> Left (to prevent crowding with CV6) -->
    <path d="M 280 760 L 195 760"/>
    <!-- CV6 (Water) -> Right -->
    <path d="M 296 775 L 375 775"/>
    <!-- CV5 (Fire) -> Left -->
    <path d="M 280 805 L 195 805"/>
  </g>

  <!-- TEXT LABELS -->
  <g id="text-labels" style="font-family:'IBM Plex Mono',monospace;font-size:15px;fill:#cbd5e1;">
    <!-- CV13: Earth / Nilam -->
    <text text-anchor="start" x="382" y="584" data-id="p13">CV13 <tspan font-size="12" fill="var(--earth)">· Earth (நிலம்)</tspan></text>
    <!-- CV9: Air/Metal / Kaatru -->
    <text text-anchor="start" x="382" y="704" data-id="p9">CV9 <tspan font-size="12" fill="var(--metal)">· Metal/Air (காற்று)</tspan></text>
    <!-- CV7: Wood / Maram (Left side) -->
    <text text-anchor="end" x="187" y="764" data-id="p7"><tspan font-size="12" fill="var(--wood)">(மரம்) Wood · </tspan>CV7</text>
    <!-- CV6: Water / Neer -->
    <text text-anchor="start" x="382" y="780" data-id="p6">CV6 <tspan font-size="12" fill="var(--water)">· Water (நீர்)</tspan></text>
    <!-- CV5: Fire / Neruppu (Left side) -->
    <text text-anchor="end" x="187" y="809" data-id="p5"><tspan font-size="12" fill="var(--fire)">(நெருப்பு) Fire · </tspan>CV5</text>
  </g>
</svg>
</div>

<!-- DETAILS PANEL -->
<aside class="panel" aria-label="Point details">
<div id="pt-info" aria-live="polite"><div class="empty"><b>Select an Element Point</b>Choose a point on the midline diagram or use the five element chips below to inspect its cun distance, anatomical location, and clinical indications.</div></div>
<div class="pts" role="group" aria-label="Five Element Points of the Conception Vessel">
  <button type="button" class="chip" data-id="p7" style="--c:var(--wood)"><span class="s">Wood · மரம்</span><span class="c">CV7</span><i></i></button>
  <button type="button" class="chip" data-id="p5" style="--c:var(--fire)"><span class="s">Fire · நெருப்பு</span><span class="c">CV5</span><i></i></button>
  <button type="button" class="chip" data-id="p13" style="--c:var(--earth)"><span class="s">Earth · நிலம்</span><span class="c">CV13</span><i></i></button>
  <button type="button" class="chip" data-id="p9" style="--c:var(--metal)"><span class="s">Air · காற்று</span><span class="c">CV9</span><i></i></button>
  <button type="button" class="chip" data-id="p6" style="--c:var(--water)"><span class="s">Water · நீர்</span><span class="c">CV6</span><i></i></button>
</div>
</aside>
</div>

<p class="note"><b>Note on Element Points:</b> The Five Element points of the Conception Vessel (CV / Ren Mai) are derived from classical Tamil / Indian acupuncture lineages and clinical manuals (e.g., Dr. Anton Jayasuriya & traditional meridian teachings). Governing Vessel (Du / GV) has no element points. Cun measurements are standardized proportional anatomical measurements taken from the center of the navel pit (CV8 Shenque). <a href="learn.html#cun">Learn about proportional cun distances &#8594;</a></p>
</main>

<script>
(function(){
var DATA = {
  "p7": {
    "code": "CV7",
    "pinyin": "Yinjiao",
    "hz": "陰交",
    "en": "Yin Junction",
    "tamil": "மரம் (Maram)",
    "elem": "Wood",
    "shu": "Wood Element Point · மரம்",
    "loc": "On the anterior midline of the lower abdomen, 1.0 cun directly below the center of the navel pit (umbilicus).",
    "cun": "1.0 cun inferior to the center of the umbilicus, 4.0 cun superior to the pubic symphysis.",
    "ind": "Nourishes kidney Yin and regulates menstruation; opens lower burner water passages; treats abdominal distension, irregular menstruation, uterine bleeding, postpartum abdominal colic, and running piglet qi."
  },
  "p5": {
    "code": "CV5",
    "pinyin": "Shimen",
    "hz": "石門",
    "en": "Stone Gate",
    "tamil": "நெருப்பு (Neruppu)",
    "elem": "Fire",
    "shu": "Fire Element Point · நெருப்பு (Front-Mu of Sanjiao)",
    "loc": "On the anterior midline of the lower abdomen, 2.5 cun directly below the center of the navel pit (umbilicus).",
    "cun": "2.5 cun inferior to the center of the umbilicus (midway on the 5-cun line between umbilicus and pubic symphysis).",
    "ind": "Warms and regulates the Fire of the Sanjiao (Triple Burner); regulates the uterus and dispels cold from the lower abdomen; treats amenorrhea, leukorrhea, retention of urine, diarrhea, and edema."
  },
  "p13": {
    "code": "CV13",
    "pinyin": "Shangwan",
    "hz": "上脘",
    "en": "Upper Venter / Upper Cavity",
    "tamil": "நிலம் (Nilam)",
    "elem": "Earth",
    "shu": "Earth Element Point · நிலம்",
    "loc": "On the anterior midline of the epigastrium, 5.0 cun directly above the center of the navel pit (umbilicus).",
    "cun": "5.0 cun superior to the center of the umbilicus (on the 8-cun line between umbilicus and sternocostal angle).",
    "ind": "Harmonizes Stomach and Spleen Earth qi; descends rebellious Stomach qi; treats gastric fullness, nausea, vomiting, acid regurgitation, stomachache, abdominal distension, and indigestion."
  },
  "p9": {
    "code": "CV9",
    "pinyin": "Shuifen",
    "hz": "水分",
    "en": "Water Divide",
    "tamil": "காற்று (Kaatru)",
    "elem": "Metal",
    "shu": "Metal / Air Element Point · காற்று",
    "loc": "On the anterior midline of the upper abdomen, 1.0 cun directly above the center of the navel pit (umbilicus).",
    "cun": "1.0 cun superior to the center of the umbilicus.",
    "ind": "Regulates water metabolism and lung-descending dispersion; harmonizes the intestines and resolves dampness; premier point for edema, abdominal swelling, ascites, borborygmus, and diarrheic disorders."
  },
  "p6": {
    "code": "CV6",
    "pinyin": "Qihai",
    "hz": "氣海",
    "en": "Sea of Qi",
    "tamil": "நீர் (Neer)",
    "elem": "Water",
    "shu": "Water Element Point · நீர் (Lower Dantian Hub)",
    "loc": "On the anterior midline of the lower abdomen, 1.5 cun directly below the center of the navel pit (umbilicus).",
    "cun": "1.5 cun inferior to the center of the umbilicus.",
    "ind": "Fosters and tonifies Original Qi (Yuan Qi); fortifies Kidney essence and Water reservoirs; rescues collapse; treats extreme fatigue, asthma/dyspnea from kidney deficiency, nocturnal emissions, enuresis, and chronic abdominal weakness."
  }
};

var ORDER = ['p7', 'p5', 'p13', 'p9', 'p6'];
var ELEM = {Wood:'var(--wood)', Fire:'var(--fire)', Earth:'var(--earth)', Metal:'var(--metal)', Water:'var(--water)'};
var NS = 'http://www.w3.org/2000/svg';
var panel = document.getElementById('pt-info');
var chips = document.querySelectorAll('.chip');
var labels = document.querySelectorAll('#text-labels text');
var narrow = window.matchMedia('(max-width:760px)');

var ring = document.createElementNS(NS,'circle');
ring.setAttribute('class','ring'); ring.setAttribute('r','16');
document.getElementById('points').parentNode.appendChild(ring);

var hitLayer = document.createElementNS(NS,'g');
document.getElementById('points').parentNode.appendChild(hitLayer);

var current = null;

function select(id, focusChip){
  var d = DATA[id], el = document.getElementById(id);
  if(!d || !el) return;
  current = id;
  document.querySelectorAll('#points circle').forEach(function(c){ c.classList.toggle('on', c === el); });
  hitLayer.querySelectorAll('.hit').forEach(function(h){ h.setAttribute('aria-pressed', h.getAttribute('data-id') === id ? 'true' : 'false'); });
  labels.forEach(function(t){ t.classList.toggle('on', t.getAttribute('data-id') === id); });
  ring.setAttribute('cx', el.getAttribute('cx')); ring.setAttribute('cy', el.getAttribute('cy'));
  ring.classList.remove('on'); void ring.getBBox(); ring.classList.add('on');
  chips.forEach(function(c){ var on = c.getAttribute('data-id') === id; c.classList.toggle('on', on); c.setAttribute('aria-pressed', on ? 'true' : 'false'); if(on && focusChip) c.focus(); });

  panel.innerHTML = '<div class="eyebrow"><span>'+d.code+'</span><span class="sep"></span><span class="shu">'+d.shu+'</span></div>'
    +'<div class="title">'+d.pinyin+' <span style="font-family:Noto Sans SC,sans-serif;font-weight:400;color:var(--ink-2);font-size:24px;">'+d.hz+'</span></div>'
    +'<div class="en">“'+d.en+'” <span class="tamil-tag">'+d.tamil+'</span></div>'
    +'<div class="pills">'
      +'<span class="pill" style="--c:'+ELEM[d.elem]+'"><i></i>'+d.elem+' Element</span>'
      +'<span class="pill">Ren Mai · Yin</span>'
      +'<span class="pill">'+(d.code === 'CV9' || d.code === 'CV13' ? d.cun.split(',')[0].trim() : d.cun.split(',')[0].trim())+'</span>'
    +'</div>'
    +'<p class="label">Location</p><p class="loc">'+d.loc+'</p>'
    +'<p class="label">Cun Measurement</p><p class="cun">'+d.cun+' <a href="learn.html#cun">What is a cun?</a></p>'
    +'<p class="label">Actions & Classical Indications</p><p class="ind">'+d.ind+'</p>';

  panel.classList.remove('enter'); void panel.offsetWidth; panel.classList.add('enter');
  if(narrow.matches && !focusChip) panel.scrollIntoView({block:'nearest',behavior:'smooth'});
}

function xy(id){ var c = document.getElementById(id); return [+c.getAttribute('cx'), +c.getAttribute('cy')]; }

ORDER.forEach(function(id){
  var el = document.getElementById(id), d = DATA[id], p = xy(id), r = 18;
  ORDER.forEach(function(o){ if(o!==id){ var q = xy(o); r = Math.min(r, Math.hypot(p[0]-q[0], p[1]-q[1]) / 2); } });
  var h = document.createElementNS(NS,'circle');
  h.setAttribute('class','hit'); h.setAttribute('cx',p[0]); h.setAttribute('cy',p[1]); h.setAttribute('r',Math.max(r, 12));
  h.setAttribute('data-id',id); h.setAttribute('tabindex','0'); h.setAttribute('role','button');
  h.setAttribute('aria-label', d.code+' '+d.pinyin+', '+d.shu+', '+d.elem);
  h.addEventListener('click', function(){ select(id); });
  h.addEventListener('keydown', function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); select(id); } });
  h.addEventListener('mouseenter', function(){ el.classList.add('hover'); });
  h.addEventListener('mouseleave', function(){ el.classList.remove('hover'); });
  hitLayer.appendChild(h);
});

// Also make the text labels clickable
labels.forEach(function(txt){
  txt.addEventListener('click', function(){
    var id = txt.getAttribute('data-id');
    if(id) select(id);
  });
});

chips.forEach(function(c){
  c.setAttribute('aria-pressed','false');
  c.addEventListener('click', function(){ select(c.getAttribute('data-id')); });
  c.addEventListener('keydown', function(e){
    if(e.key!=='ArrowRight'&&e.key!=='ArrowLeft') return;
    e.preventDefault();
    var i = ORDER.indexOf(current || c.getAttribute('data-id')) + (e.key==='ArrowRight'?1:-1);
    select(ORDER[(i+ORDER.length)%ORDER.length], true);
  });
});

function fromHash(){
  var code = decodeURIComponent(location.hash.slice(1)).toUpperCase();
  for(var k in DATA){ if(DATA[k].code === code){ select(k); return; } }
  // default select Wood point CV7
  select('p7');
}

var _select = select;
select = function(id, focusChip){
  _select(id, focusChip);
  try { history.replaceState(null, '', '#'+DATA[id].code); } catch(e) {}
};

window.addEventListener('hashchange', fromHash);
fromHash();
})();
</script>

<!-- gloss:start -->
<style>
.gl{appearance:none;border:0;background:none;margin:0;padding:0;display:inline;font:inherit;color:inherit;letter-spacing:inherit;text-transform:inherit;text-align:inherit;cursor:help;text-decoration:underline dotted;text-decoration-color:color-mix(in srgb,currentColor 42%,transparent);text-decoration-thickness:1px;text-underline-offset:3px;transition:text-decoration-color .15s}
.gl:focus-visible{outline:2px solid currentColor;outline-offset:2px;border-radius:2px}
.gl[aria-expanded="true"]{text-decoration-color:currentColor}
@media (hover:hover) and (pointer:fine){.gl:hover{text-decoration-color:currentColor}}
.gl-tip{position:fixed;z-index:100;left:0;top:0;width:min(280px,calc(100vw - 24px));padding:12px 14px 13px;border-radius:12px;background:rgba(21,25,40,.96);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);color:#f5f3ed;border:1px solid rgba(245,243,237,.14);box-shadow:0 20px 50px -15px rgba(0,0,0,.85),0 0 0 1px rgba(245,243,237,.06);font:400 13px/1.5 "Jost",system-ui,sans-serif;letter-spacing:.005em;text-align:left;text-transform:none;pointer-events:none;visibility:hidden;opacity:0;transform:translateY(4px);transition:opacity .15s cubic-bezier(.16,1,.3,1),transform .15s cubic-bezier(.16,1,.3,1)}
.gl-tip.on{visibility:visible;opacity:1;transform:none}
.gl-tip.below{transform:translateY(-4px)}
.gl-tip.on.below{transform:none}
.gl-tip-k{display:block;font:500 9.5px/1 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.14em;text-transform:uppercase;color:#8590ab}
.gl-tip-t{display:flex;align-items:baseline;gap:8px;margin-top:7px;font-size:15px;font-weight:600;line-height:1.25}
.gl-tip-t span{font:300 15px/1 "Noto Sans SC","PingFang SC",sans-serif;color:#9ea8bd}
.gl-tip-d{display:block;margin-top:5px;color:#9ea8bd;line-height:1.45}
@media (prefers-reduced-motion:reduce){.gl-tip{transition:none}}
</style>
<script>
(function(){
  'use strict';
  var G = [
    ['Measurement','Cun','寸','A proportional unit for locating points: about the width of the patient’s own thumb, so it scales with the body. Ten fen make one cun.',['cun']],
    ['Measurement','Fen','分','One tenth of a cun.',['fen']],
    ['Measurement','B-cun','','Proportional cun: a body region is divided into a fixed number of cun (e.g. 8 cun between umbilicus and sternum, 5 cun between umbilicus and pubic symphysis).',['B-cun']],
    ['Measurement','F-cun','','Finger cun: measured with the patient’s own fingers. One thumb is 1 cun; four fingers together are 3.',['F-cun']],
    ['Direction','Anterior','','Toward the front of the body. Opposite of posterior.',['anterior']],
    ['Direction','Posterior','','Toward the back of the body. Opposite of anterior.',['posterior']],
    ['Direction','Inferior','','Below; toward the feet.',['inferior']],
    ['Direction','Superior','','Above; toward the head.',['superior']],
    ['Landmark','Umbilicus','神闕','The navel pit (CV8 Shenque), reference 0 landmark for abdominal measurements.',['umbilicus','navel']],
    ['Landmark','Pubic symphysis','曲骨','The cartilaginous joint between the pubic bones; CV2 Qugu sits at its upper border, 5 cun below the navel.',['pubic symphysis']],
    ['Point type','Front-Mu','募穴','Alarm points located on the chest and abdomen where qi of the Zang-Fu organs gathers.',['Front-Mu']],
    ['Extraordinary Vessel','Ren Mai','任脈','Conception Vessel: runs along the anterior midline and governs all Yin meridians.',['Ren Mai','Conception Vessel']]
  ];
  var byAlias = {}, parts = [];
  G.forEach(function(g, i){ g[4].forEach(function(a){ parts.push(a); byAlias[a.toLowerCase()] = i; }); });
  parts.sort(function(a, b){ return b.length - a.length; });
  var RE = new RegExp('(^|[^A-Za-z-])(' + parts.join('|') + ')(?![A-Za-z-])', 'i');
  function lookup(word){
    var w = word.toLowerCase();
    for(var a in byAlias){ if(new RegExp('^(' + a + ')$', 'i').test(w)) return byAlias[a]; }
    return -1;
  }
  var SKIP = 'a,button,b,strong,h1,h2,h3,code,kbd,script,style,svg,.gl,[data-gloss-skip]';
  function wrap(target, seen){
    var walker = document.createTreeWalker(target, NodeFilter.SHOW_TEXT, null), nodes = [], n;
    while((n = walker.nextNode())) nodes.push(n);
    nodes.forEach(function(node){
      var p = node.parentElement;
      if(!p || (p !== target && p.closest(SKIP) && target.contains(p.closest(SKIP)))) return;
      if(p.closest('.gl')) return;
      var text = node.nodeValue, m, frag = null, last = 0, rest = text, offset = 0;
      while((m = RE.exec(rest))){
        var start = offset + m.index + m[1].length, word = m[2], idx = lookup(word);
        offset = start + word.length; rest = text.slice(offset);
        if(idx < 0 || seen[idx]) continue;
        seen[idx] = true;
        frag = frag || document.createDocumentFragment();
        frag.appendChild(document.createTextNode(text.slice(last, start)));
        var b = document.createElement('button');
        b.type = 'button'; b.className = 'gl'; b.dataset.g = idx;
        b.setAttribute('aria-expanded', 'false');
        b.setAttribute('aria-label', word + ': ' + G[idx][3]);
        b.textContent = word;
        frag.appendChild(b);
        last = offset;
      }
      if(frag){ frag.appendChild(document.createTextNode(text.slice(last))); node.parentNode.replaceChild(frag, node); }
    });
  }
  function seenIn(scope){
    var s = {};
    [].forEach.call(scope.querySelectorAll('.gl'), function(b){ s[b.dataset.g] = true; });
    return s;
  }
  function watch(rootSel, targetSel, scopeSel){
    var root = typeof rootSel === 'string' ? document.querySelector(rootSel) : rootSel;
    if(!root) return;
    var mo;
    function run(){
      if(mo) mo.disconnect();
      var seen = new Map();
      [].forEach.call(root.querySelectorAll(targetSel), function(t){
        var scope = (scopeSel && t.closest(scopeSel)) || t;
        if(!seen.has(scope)) seen.set(scope, seenIn(scope));
        wrap(t, seen.get(scope));
      });
      if(mo) mo.observe(root, {childList:true, subtree:true});
    }
    run();
    if('MutationObserver' in window){ mo = new MutationObserver(function(){ run(); }); mo.observe(root, {childList:true, subtree:true}); }
  }
  var tip = document.createElement('div');
  tip.className = 'gl-tip'; tip.setAttribute('role', 'tooltip'); tip.id = 'gl-tip';
  var open = null, timer = 0, lastHide = 0, openedAt = 0;
  function place(el){
    var r = el.getBoundingClientRect(), t = tip.getBoundingClientRect(), gap = 10, pad = 8;
    var x = Math.max(10, Math.min(r.left + r.width/2 - t.width/2, innerWidth - t.width - 10));
    var above = r.top - gap - t.height >= pad;
    var y = above ? r.top - gap - t.height : Math.min(r.bottom + gap, innerHeight - t.height - pad);
    tip.classList.toggle('below', !above);
    tip.style.left = Math.round(x) + 'px'; tip.style.top = Math.round(y) + 'px';
  }
  function show(el){
    var g = G[+el.dataset.g]; if(!g) return;
    clearTimeout(timer);
    if(!tip.parentNode) document.body.appendChild(tip);
    if(open && open !== el){ open.setAttribute('aria-expanded', 'false'); open.removeAttribute('aria-describedby'); }
    open = el; openedAt = Date.now(); el.setAttribute('aria-expanded', 'true'); el.setAttribute('aria-describedby', 'gl-tip');
    tip.innerHTML = '<span class="gl-tip-k"></span><span class="gl-tip-t"></span><span class="gl-tip-d"></span>';
    tip.children[0].textContent = g[0];
    tip.children[1].textContent = g[1];
    if(g[2]){ var hz = document.createElement('span'); hz.lang = 'zh'; hz.textContent = g[2]; tip.children[1].appendChild(hz); }
    tip.children[2].textContent = g[3];
    tip.classList.remove('on'); place(el); void tip.offsetWidth; tip.classList.add('on');
  }
  function hide(){
    clearTimeout(timer);
    if(!open) return;
    open.setAttribute('aria-expanded', 'false'); open.removeAttribute('aria-describedby');
    open = null; tip.classList.remove('on'); lastHide = Date.now();
  }
  function gl(e){ return e.target.closest && e.target.closest('.gl'); }
  document.addEventListener('pointerover', function(e){
    var el = gl(e); if(!el || e.pointerType === 'touch' || open === el) return;
    clearTimeout(timer); timer = setTimeout(function(){ show(el); }, Date.now() - lastHide < 400 ? 0 : 120);
  });
  document.addEventListener('pointerout', function(e){
    var el = gl(e); if(!el || el.contains(e.relatedTarget)) return;
    if(open === el) hide(); else clearTimeout(timer);
  });
  document.addEventListener('focusin', function(e){ var el = gl(e); if(el && open !== el) show(el); });
  document.addEventListener('focusout', function(e){ var el = gl(e); if(el && open === el) hide(); });
  document.addEventListener('click', function(e){
    var el = gl(e); if(!el) return;
    e.preventDefault(); e.stopPropagation();
    if(e.pointerType === 'mouse') return;
    if(open === el && Date.now() - openedAt > 350) hide(); else if(open !== el) show(el);
  }, true);
  document.addEventListener('pointerdown', function(e){ if(open && !gl(e)) hide(); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape' && open) hide(); });
  addEventListener('scroll', hide, true);
  addEventListener('resize', hide);
  window.ShuGloss = {watch: watch, terms: G};
})();
</script>
<!-- gloss:end -->
<script>ShuGloss.watch('#pt-info', '.eyebrow .shu, .loc, .cun', '#pt-info');</script>

<!-- footer:start -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400&display=swap">
<style>
.cf{margin-top:72px;border-top:1px solid var(--hair, rgba(245,243,237,.09));background:var(--ground, #0d101d);color:var(--ink, #f5f3ed);overflow:hidden}
.cf-in{max-width:1100px;margin:0 auto;padding-top:28px;padding-bottom:20px;padding-left:max(clamp(16px,3vw,40px),env(safe-area-inset-left,0px));padding-right:max(clamp(16px,3vw,40px),env(safe-area-inset-right,0px))}
.cf-mark{margin:0;font:400 clamp(44px,9vw,128px)/.82 "Newsreader",Georgia,"Times New Roman",serif;letter-spacing:-.045em;padding-bottom:.18em;text-align:left;white-space:nowrap;color:var(--ink, #f5f3ed)}
.cf-mark b{font-weight:400;color:#ff6a3d}
@media (max-width:700px){.cf{margin-top:48px}}
</style>
<footer class="cf">
  <div class="cf-in"><p class="cf-mark" aria-label="Caffeinity">caffeinity<b>.</b></p></div>
</footer>
<!-- footer:end -->
</body></html>
'''

(ROOT / 'cv-meridian-chart.html').write_text(html_content, encoding='utf-8')
print("Successfully written cv-meridian-chart.html")
