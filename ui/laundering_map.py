"""Hop-by-hop money-laundering route map, rendered in an isolated iframe (offline, no network)."""
import json
from .worldmap import POLY

HTML = r"""<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500&display=swap');
*{box-sizing:border-box}:root{--panel:#12264A;--line:#2A4170;--frost:#E8EFFA;--muted:#8FA3C4;--p:#FFB547;--l:#6EA8FF;--i:#34D3C0}
body{margin:0;font-family:'IBM Plex Sans',sans-serif;color:var(--frost);background:transparent}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}
.tab{background:transparent;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:.4rem .95rem;cursor:pointer;font:inherit;transition:transform .2s cubic-bezier(.2,.9,.3,1.3),box-shadow .2s,color .2s,border-color .2s}
.tab:hover,.tab:focus-visible{transform:translateY(-3px) scale(1.07);color:#fff;border-color:var(--i);box-shadow:0 0 16px rgba(52,211,192,.5);outline:none}
.tab.on{color:var(--frost);border-color:var(--i);background:rgba(52,211,192,.1)}
.grid{display:grid;grid-template-columns:minmax(0,1.55fr) minmax(300px,1fr);gap:14px}@media(max-width:860px){.grid{grid-template-columns:1fr}}
.box:first-child{align-self:start}.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}
#side{max-height:690px;overflow:auto}
h4{font-family:'Space Grotesk',sans-serif,sans-serif;margin:0 0 2px;font-size:1.25rem}.era{color:var(--muted);font-size:.85rem}.hl{margin:.6rem 0;line-height:1.5}
.ctl{display:flex;gap:14px;align-items:center;flex-wrap:wrap;margin-top:8px;font-size:.82rem;color:var(--muted)}
.ctl button{background:#0A1830;color:var(--frost);border:1px solid var(--line);border-radius:999px;padding:.35rem .9rem;cursor:pointer;font:inherit;transition:transform .2s,box-shadow .2s}
.ctl button:hover{transform:translateY(-2px) scale(1.06);box-shadow:0 0 14px rgba(52,211,192,.5);border-color:var(--i)}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:5px}
.hop{display:flex;gap:10px;padding:8px;border:1px solid transparent;border-radius:10px;cursor:pointer;opacity:.4;transition:opacity .3s,background .3s;font-size:.88rem;line-height:1.4}
.hop.on{opacity:1}.hop.cur{background:rgba(110,168,255,.1);border-color:var(--line)}.hop b{flex:0 0 22px;height:22px;border-radius:50%;display:grid;place-items:center;color:#0A1830;font-size:.75rem}
.hop small{display:block;color:var(--muted);font-size:.74rem}
.sec{margin-top:12px;font-size:.88rem;line-height:1.5}.sec h5{margin:0 0 4px;font-size:.85rem;color:var(--muted);font-weight:500}
.chips{display:flex;flex-wrap:wrap;gap:6px}.chip{border:1px solid #6b3a47;color:#ffb3b3;border-radius:999px;padding:.15rem .6rem;font-size:.78rem}
.ring{fill:none;stroke-width:2;transform-box:fill-box;transform-origin:center;animation:ping 1.2s ease-out}
@keyframes ping{0%{transform:scale(.3);opacity:1}100%{transform:scale(3.4);opacity:0}}
.pop{transform-box:fill-box;transform-origin:center;animation:pop .4s cubic-bezier(.2,1.6,.4,1) both}@keyframes pop{from{transform:scale(0)}}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
<div class="tabs" id="tabs"></div>
<div class="grid"><div class="box"><svg id="map" viewBox="0 0 1000 440" width="100%" role="img" aria-label="Map of the laundering route"><path id="land" fill="none" stroke="#2A4170" stroke-linecap="round" vector-effect="non-scaling-stroke" stroke-width="2.6"/><g id="layer"></g></svg>
 <div class="ctl"><button id="play">Replay route</button><span><i class="dot" style="background:var(--p)"></i>Placement: cash enters</span><span><i class="dot" style="background:var(--l)"></i>Layering: hidden through hops</span><span><i class="dot" style="background:var(--i)"></i>Integration: comes out clean</span></div></div>
 <div class="box" id="side"></div></div>
<script>
const CASES=__CASES__,POLY=__POLY__,W=1000,H=440,X=o=>(o+180)/360*W,Y=a=>(82-a)/140*H,COL={placement:'#FFB547',layering:'#6EA8FF',integration:'#34D3C0'};
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches,$=s=>document.querySelector(s),sleep=ms=>new Promise(r=>setTimeout(r,RM?0:ms));
const inside=(p,q)=>{let c=false;for(let i=0,j=q.length-1;i<q.length;j=i++){const a=q[i],b=q[j];if((a[1]>p[1])!=(b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])c=!c}return c};
(function(){const P=Object.values(POLY);let d='';for(let la=80;la>-58;la-=1.5)for(let lo=-180;lo<180;lo+=1.5)if(P.some(q=>inside([lo,la],q)))d+=`M${X(lo).toFixed(1)} ${Y(la).toFixed(1)}h0`;$('#land').setAttribute('d',d)})();
let cur=0,shown=0,tok=0,vb=[0,0,W,H];
function fit(c){const xs=c.nodes.map(n=>X(n.lon)),ys=c.nodes.map(n=>Y(n.lat));let w=Math.min(W,Math.max(Math.max(...xs)-Math.min(...xs)+260,420)),h=w*H/W;
 if(Math.max(...ys)-Math.min(...ys)+140>h){h=Math.min(H,Math.max(...ys)-Math.min(...ys)+140);w=h*W/H}
 const cx=(Math.min(...xs)+Math.max(...xs))/2,cy=(Math.min(...ys)+Math.max(...ys))/2;return[Math.min(Math.max(cx-w/2,0),W-w),Math.min(Math.max(cy-h/2,0),H-h),w,h]}
const node=(c,n)=>c.nodes.find(o=>o.n===n),arc=(c,h)=>{const a=node(c,h.a),b=node(c,h.b),x1=X(a.lon),y1=Y(a.lat),x2=X(b.lon),y2=Y(b.lat),d=Math.hypot(x2-x1,y2-y1);
 return `M${x1},${y1} Q${(x1+x2)/2},${Math.min(y1,y2)-d*.22-6} ${x2},${y2}`};
const below=(c,n,x,y,fs)=>c.nodes.some(o=>o!==n&&Math.abs(X(o.lon)-x)<fs*6&&Math.abs(Y(o.lat)-y)<fs*1.5&&Y(o.lat)<y);
function layer(anim){const c=CASES[cur],u=vb[2]/1000,fs=vb[2]/55,reached=new Set();c.hops.slice(0,shown).forEach(h=>{reached.add(h.a);reached.add(h.b)});
 if(anim)reached.add(anim.a),reached.add(anim.b);let g='';
 c.hops.slice(0,shown).forEach(h=>{if(h.a!==h.b)g+=`<path d="${arc(c,h)}" fill="none" stroke="${COL[h.stage]}" stroke-width="${3*u}" opacity=".85"/>`});
 c.nodes.forEach(n=>{const x=X(n.lon),y=Y(n.lat),on=reached.has(n.n),r=on?6*u:4*u,st=c.hops.find(h=>h.b===n.n||h.a===n.n),col=on?COL[(c.hops.filter(h=>h.a===n.n||h.b===n.n).pop()||st).stage]:'#5b6f94';
  g+=`<circle cx="${x}" cy="${y}" r="${r}" fill="${col}" ${on?'class="pop"':''}/><text x="${x>vb[0]+vb[2]*.75?x-9*u:x+9*u}" y="${below(c,n,x,y,fs)?y+fs*1.1+6*u:y-8*u}" fill="${on?'#E8EFFA':'#8FA3C4'}" font-size="${fs}" text-anchor="${x>vb[0]+vb[2]*.75?'end':'start'}" font-weight="500">${n.n}</text>`});
 $('#layer').innerHTML=g+'<g id="anim"></g>'}
function side(){const c=CASES[cur];$('#side').innerHTML=`<h4>${c.name}</h4><div class="era">${c.era}</div><div class="hl">${c.headline}</div>
 ${c.hops.map((h,i)=>`<div class="hop ${i<shown?'on':''} ${i===shown-1?'cur':''}" data-i="${i}"><b style="background:${COL[h.stage]}">${i+1}</b><div>${h.t}<small>${h.a===h.b?h.a:h.a+' to '+h.b} · ${h.stage}</small></div></div>`).join('')}
 <div class="sec"><h5>Red flags that were there</h5><div class="chips">${c.flags.map(f=>`<span class="chip">${f}</span>`).join('')}</div></div>
 <div class="sec"><h5>What happened</h5>${c.outcome}</div><div class="sec"><h5>Lesson</h5>${c.lesson}</div>`}
function tabs(){$('#tabs').innerHTML=CASES.map((c,i)=>`<button class="tab ${i===cur?'on':''}" data-i="${i}">${c.name}</button>`).join('')}
async function runHop(h,my){const c=CASES[cur],a=node(c,h.a),u=vb[2]/1000,col=COL[h.stage],x=X(a.lon),y=Y(a.lat);layer(h);const A=$('#anim');
 if(h.a===h.b){A.innerHTML=[0,1,2].map(k=>`<circle class="ring" style="animation-delay:${k*.3}s" cx="${x}" cy="${y}" r="${12*u}" stroke="${col}"/>`).join('');await sleep(1300);return}
 A.innerHTML=`<path id="ap" d="${arc(c,h)}" fill="none" stroke="${col}" stroke-width="${3*u}"/><circle id="pk" r="${7*u}" fill="${col}"/>`;
 const p=$('#ap'),L=p.getTotalLength(),t0=performance.now(),D=RM?1:1300;p.style.strokeDasharray=L;
 await new Promise(res=>{const f=n=>{if(my!==tok)return res();const q=Math.min(1,(n-t0)/D);p.style.strokeDashoffset=L*(1-q);const pt=p.getPointAtLength(L*q);$('#pk').setAttribute('cx',pt.x);$('#pk').setAttribute('cy',pt.y);q<1?requestAnimationFrame(f):res()};requestAnimationFrame(f)})}
async function play(){const my=++tok,c=CASES[cur];shown=0;layer();side();await sleep(400);
 for(let i=0;i<c.hops.length;i++){if(my!==tok)return;await runHop(c.hops[i],my);if(my!==tok)return;shown=i+1;layer();side();await sleep(300)}}
function open(i){cur=i;tok++;vb=fit(CASES[cur]);$('#map').setAttribute('viewBox',vb.join(' '));tabs();play()}
$('#tabs').addEventListener('click',e=>{const t=e.target.closest('.tab');if(t)open(+t.dataset.i)});
$('#play').onclick=()=>play();
$('#side').addEventListener('click',e=>{const h=e.target.closest('.hop');if(h){tok++;shown=+h.dataset.i+1;layer();side()}});
open(0);
</script>"""


def laundering_map(cases):
    return HTML.replace("__CASES__", json.dumps(cases)).replace("__POLY__", json.dumps(POLY))
