var ELEM = {Metal:'var(--metal)',Water:'var(--water)',Wood:'var(--wood)',Fire:'var(--fire)',Earth:'var(--earth)'};
var NS = 'http://www.w3.org/2000/svg';
var $ = function(id){ return document.getElementById(id); };
var panel = $('pt-info'), stage = $('stage'), flip = $('flip'), sheet = $('sheet'), grab = $('grab');
var locImg = $('loc-img'), locTag = $('loc-tag'), faceB = locImg.parentNode;
var faceBtns = document.querySelectorAll('.vsw button');
var chips = document.querySelectorAll('.chip');
var labels = document.querySelectorAll('#text-labels text');
var narrow = window.matchMedia('(max-width:760px)');
var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var YY = document.body.getAttribute('data-yy') || '';
var ring = document.createElementNS(NS,'circle');
ring.setAttribute('class','ring'); ring.setAttribute('r','16');
document.getElementById('points').parentNode.appendChild(ring);
var hitLayer = document.createElementNS(NS,'g');
document.getElementById('points').parentNode.appendChild(hitLayer);
var current = null;
function src(code){ var im = IMGS[code]; return im ? (im.indexOf('data:')===0 ? im : 'data:image/jpeg;base64,'+im) : ''; }
// phones: the card shows the channel map on one side and the chosen point's location diagram on the other
function setFace(face){
  var loc = face === 'loc' && current && src(DATA[current].code);
  stage.classList.toggle('loc', !!loc);
  faceB.setAttribute('aria-hidden', loc ? 'false' : 'true');
  faceBtns.forEach(function(b){ b.setAttribute('aria-pressed', (b.getAttribute('data-face') === 'loc') === !!loc ? 'true' : 'false'); });
}
faceBtns.forEach(function(b){ b.addEventListener('click', function(){ setFace(b.getAttribute('data-face')); }); });
function select(id, focusChip, fromChart){
  var d = DATA[id], el = document.getElementById(id);
  current = id;
  document.querySelectorAll('#points circle').forEach(function(c){ c.classList.toggle('on', c === el); });
  hitLayer.querySelectorAll('.hit').forEach(function(h){ h.setAttribute('aria-pressed', h.getAttribute('data-id') === id ? 'true' : 'false'); });
  labels.forEach(function(t){ t.classList.toggle('on', t.textContent.trim() === d.code); });
  ring.setAttribute('cx', el.getAttribute('cx')); ring.setAttribute('cy', el.getAttribute('cy'));
  ring.classList.remove('on'); void ring.getBBox(); ring.classList.add('on');
  chips.forEach(function(c){ var on = c.getAttribute('data-id') === id; c.classList.toggle('on', on); c.setAttribute('aria-pressed', on ? 'true' : 'false'); if(on && focusChip) c.focus(); });
  var shu = d.shu.replace(/ point/g,'');
  var im = src(d.code);
  panel.innerHTML = '<div class="eyebrow"><span>'+d.code+'</span><span class="sep"></span><span class="shu">'+shu+'</span></div>'
    +'<div class="title">'+d.pinyin+'</div><div class="en">'+d.en+'</div>'
    +'<div class="pills"><span class="pill" style="--c:'+ELEM[d.elem]+'"><i></i>'+d.elem+'</span>'+(YY ? '<span class="pill">'+YY+' channel</span>' : '')+'</div>'
    +'<div class="locrow">'+(im ? '<figure><img alt="Location diagram for '+d.code+'" src="'+im+'"></figure>' : '')
    +'<div><p class="label">Location</p><p class="loc">'+d.loc+'</p>'
    +'<p class="label">Cun</p><p class="cun">'+d.cun+'<a href="learn.html#cun">What is a cun?</a></p></div></div>';
  panel.classList.remove('enter'); void panel.offsetWidth; panel.classList.add('enter');
  if(im){ locImg.src = im; locImg.alt = 'Location diagram for '+d.code; locTag.textContent = d.code+' · location'; }
  faceBtns.forEach(function(b){ if(b.getAttribute('data-face') === 'loc') b.disabled = !im; });
  // a tap on the chart turns the card to the diagram; the station buttons keep whichever side is showing
  setFace(fromChart && narrow.matches ? 'loc' : (stage.classList.contains('loc') ? 'loc' : 'map'));
}
// Each dot is drawn in its element's colour and gets an invisible hit circle sized to half the gap
// to its nearest neighbour, so close-set points never steal each other's clicks.
function xy(id){ var c = document.getElementById(id); return [+c.getAttribute('cx'), +c.getAttribute('cy')]; }
ORDER.forEach(function(id){
  var el = document.getElementById(id), d = DATA[id], p = xy(id), r = 18;
  el.style.setProperty('--pc', ELEM[d.elem]);
  ORDER.forEach(function(o){ if(o!==id){ var q = xy(o); r = Math.min(r, Math.hypot(p[0]-q[0], p[1]-q[1]) / 2); } });
  var h = document.createElementNS(NS,'circle');
  h.setAttribute('class','hit'); h.setAttribute('cx',p[0]); h.setAttribute('cy',p[1]); h.setAttribute('r',r);
  h.setAttribute('data-id',id); h.setAttribute('tabindex','0'); h.setAttribute('role','button');
  h.setAttribute('aria-label', d.code+' '+d.pinyin+', '+d.shu+', '+d.elem);
  h.addEventListener('click', function(){ select(id, false, true); });
  h.addEventListener('keydown', function(e){ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); select(id, false, true); } });
  h.addEventListener('mouseenter', function(){ el.classList.add('hover'); });
  h.addEventListener('mouseleave', function(){ el.classList.remove('hover'); });
  hitLayer.appendChild(h);
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
// the sheet: tap the handle or drag it; Escape or a tap on the chart closes it
function setSheet(open){ sheet.classList.toggle('open', open); grab.setAttribute('aria-expanded', open ? 'true' : 'false'); }
var gy = null, dragged = false;
grab.addEventListener('pointerdown', function(e){ gy = e.clientY; dragged = false; });
window.addEventListener('pointerup', function(e){
  if(gy === null) return;
  var dy = e.clientY - gy; gy = null;
  if(Math.abs(dy) > 24){ dragged = true; setSheet(dy < 0); }
});
grab.addEventListener('click', function(){ if(dragged){ dragged = false; return; } setSheet(!sheet.classList.contains('open')); });
document.addEventListener('keydown', function(e){ if(e.key === 'Escape') setSheet(false); });
stage.addEventListener('click', function(){ if(sheet.classList.contains('open')) setSheet(false); });
$('more').addEventListener('toggle', function(){ if(this.open && narrow.matches) setSheet(true); });
// desktop: the plate leans a little toward the pointer
if(!reduced && window.matchMedia('(hover:hover) and (min-width:761px)').matches){
  stage.addEventListener('pointermove', function(e){
    var r = flip.getBoundingClientRect();
    flip.style.setProperty('--ry', (((e.clientX - r.left) / r.width - .5) * 9).toFixed(2)+'deg');
    flip.style.setProperty('--rx', (((e.clientY - r.top) / r.height - .5) * -6).toFixed(2)+'deg');
  });
  stage.addEventListener('pointerleave', function(){ flip.style.setProperty('--ry','0deg'); flip.style.setProperty('--rx','0deg'); });
}
// deep links: chart.html#GB34 opens with that point selected, and selections update the address
function fromHash(){
  var code = decodeURIComponent(location.hash.slice(1)).toUpperCase();
  for(var k in DATA){ if(DATA[k].code === code){ if(k !== current) select(k); return; } }
}
var _select = select;
select = function(id, focusChip, fromChart){
  _select(id, focusChip, fromChart);
  try { history.replaceState(null, '', '#'+DATA[id].code); } catch(e) {}
};
window.addEventListener('hashchange', fromHash);
if(location.hash) fromHash();
