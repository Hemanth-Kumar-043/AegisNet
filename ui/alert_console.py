"""Alert console rendered in an isolated iframe (no Streamlit import, no network needed).
Everything is SIMULATED: nothing is ever sent to a real police service."""
import json

HTML = r"""<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500&display=swap');
*{box-sizing:border-box} :root{--ink:#0A1830;--panel:#12264A;--line:#2A4170;--frost:#E8EFFA;--muted:#8FA3C4;--ok:#34D3C0;--warn:#FFB547;--bad:#FF6B6B;--blue:#6EA8FF}
body{margin:0;font-family:'IBM Plex Sans',sans-serif;color:var(--frost);background:transparent}
h4{font-family:'Space Grotesk',sans-serif;margin:0;font-size:1.05rem}
.banner{border-radius:12px;padding:.7rem 1rem;font-family:'Space Grotesk',sans-serif;font-weight:700;display:flex;gap:.6rem;align-items:center;border:1px solid var(--bad);color:var(--bad);background:rgba(255,107,107,.12)}
.banner.alert{animation:flash 1s steps(2,jump-none) infinite}
.banner.ok{border-color:var(--ok);color:var(--ok);background:rgba(52,211,192,.1)}
.banner.off{border-color:var(--line);color:var(--muted);background:rgba(143,163,196,.08)}
@keyframes flash{0%{background:rgba(255,107,107,.28)}100%{background:rgba(255,107,107,.08)}}
.grid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(300px,1fr);gap:14px;margin-top:12px}
@media(max-width:820px){.grid{grid-template-columns:1fr}}
.box:first-child{display:flex;align-items:center}.box{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}
svg text{font-family:'IBM Plex Sans',sans-serif}
#dots circle{fill:#2A4170}
.ring{fill:none;stroke:var(--bad);stroke-width:2;transform-box:fill-box;transform-origin:center;animation:ping 1.8s ease-out infinite}
.ring.r2{animation-delay:.6s}.ring.r3{animation-delay:1.2s}
.ok .ring,.ring.ok{stroke:var(--ok);animation-duration:3s}
@keyframes ping{0%{transform:scale(.3);opacity:.9}100%{transform:scale(3.4);opacity:0}}
.flow{animation:flow 1.2s linear infinite}@keyframes flow{to{stroke-dashoffset:-24}}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}
.tab{background:transparent;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:.3rem .8rem;cursor:pointer;font:inherit;font-size:.85rem;display:flex;gap:6px;align-items:center}
.tab.on{color:var(--frost);border-color:var(--ok)}.tab i{width:8px;height:8px;border-radius:50%;background:var(--bad)}
.tab i.frozen{background:var(--ok)}.tab i.dismissed{background:var(--muted)}
.head{display:flex;gap:14px;align-items:center}
.beacon{flex:0 0 54px;height:54px;border-radius:50%;position:relative;background:#3a1626;border:2px solid var(--bad);overflow:hidden;box-shadow:0 0 0 0 rgba(255,107,107,.6);animation:glow 1.2s ease-out infinite}
.beacon::after{content:"";position:absolute;inset:0;background:conic-gradient(from 0deg,rgba(255,107,107,.95),transparent 35%,transparent 65%,rgba(255,107,107,.95));animation:spin 1s linear infinite}
.beacon.ok{border-color:var(--ok);background:#0f3a3a;animation:none}.beacon.ok::after{animation:none;background:radial-gradient(circle,rgba(52,211,192,.8),transparent 70%)}
.beacon.off{border-color:var(--line);background:#1b2a4a;animation:none}.beacon.off::after{display:none}
@keyframes spin{to{transform:rotate(360deg)}}@keyframes glow{to{box-shadow:0 0 0 16px rgba(255,107,107,0)}}
.rows{display:grid;grid-template-columns:auto 1fr;gap:.3rem 1rem;margin:12px 0;font-size:.92rem}.rows span:nth-child(odd){color:var(--muted)}
.bar{height:8px;border-radius:99px;background:#0A1830;overflow:hidden;margin-top:6px}.bar b{display:block;height:100%;background:linear-gradient(90deg,var(--warn),var(--bad));width:0;transition:width 1s ease-out}
.chips{display:flex;flex-wrap:wrap;gap:6px}.chip{font-size:.78rem;border:1px solid var(--line);border-radius:999px;padding:.15rem .6rem;color:var(--muted)}
.stamp{display:inline-block;border:3px solid var(--ok);color:var(--ok);font-family:'Space Grotesk',sans-serif;font-weight:700;padding:.1rem .6rem;border-radius:6px;transform:rotate(-6deg);animation:stamp .35s cubic-bezier(.2,1.6,.4,1) both}
@keyframes stamp{from{transform:rotate(-6deg) scale(2.4);opacity:0}to{transform:rotate(-6deg) scale(1);opacity:1}}
.keys{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px}
.hold{display:flex;align-items:center;gap:8px;background:#0A1830;color:var(--frost);border:1px solid var(--line);border-radius:12px;padding:8px;cursor:pointer;font:inherit;text-align:left;user-select:none;touch-action:none}
.hold svg{width:38px;height:38px;flex:0 0 38px;transform:rotate(-90deg)}.hold .bg{fill:none;stroke:var(--line);stroke-width:4}
.hold .fg{fill:none;stroke:var(--ok);stroke-width:4;stroke-linecap:round}
.hold small{display:block;color:var(--muted);font-size:.74rem}.hold b{font-size:.85rem}
.hold.holding{border-color:var(--ok)}.hold.done{border-color:var(--ok);background:rgba(52,211,192,.1)}.hold:disabled:not(.done){opacity:.45;cursor:default}
button:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.freeze{width:100%;border-radius:12px;border:1px solid var(--line);background:#0A1830;color:var(--muted);padding:.8rem;font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1rem;cursor:not-allowed}
.freeze.ready{background:var(--bad);color:#1a0a0a;border-color:var(--bad);cursor:pointer;animation:ready 1.4s ease-in-out infinite}
@keyframes ready{50%{box-shadow:0 0 0 6px rgba(255,107,107,.25)}}
.link{background:none;border:0;color:var(--muted);text-decoration:underline;cursor:pointer;font:inherit;font-size:.82rem;padding:.4rem 0}
.log{font-size:.8rem;color:var(--muted);max-height:170px;overflow:auto;margin-top:6px}.log div{padding:2px 0;animation:in .3s both}@keyframes in{from{opacity:0;transform:translateX(-6px)}}
.log em{color:var(--ok);font-style:normal}
pre{background:#0A1830;border:1px solid var(--line);border-radius:10px;padding:8px;font-size:.72rem;color:var(--frost);overflow:auto;margin:6px 0 0}
.top{display:flex;justify-content:space-between;align-items:center;gap:8px}.snd{background:none;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:.2rem .7rem;cursor:pointer;font:inherit;font-size:.78rem}
.hold,.freeze,.link,.snd,.tab{transition:transform .2s cubic-bezier(.2,.9,.3,1.35),box-shadow .2s,border-color .2s,color .2s,background .2s}
.hold:not(:disabled):hover,.hold:not(:disabled):focus-visible{transform:translateY(-3px) scale(1.04);border-color:var(--ok);box-shadow:0 0 18px rgba(52,211,192,.5)}
.freeze.ready:hover{transform:translateY(-3px) scale(1.03);box-shadow:0 0 24px rgba(255,107,107,.65)}
.snd:hover,.tab:hover,.tab:focus-visible{transform:translateY(-2px) scale(1.07);color:#fff;border-color:var(--ok);box-shadow:0 0 14px rgba(52,211,192,.45);outline:none}
.link:hover{color:#fff;transform:scale(1.05)}
.hold svg,.hold span{pointer-events:none}.hold{border-width:1.5px;padding:10px}.hold b{font-size:.95rem}
.steps{display:grid;gap:5px;margin:0 0 10px;padding:9px 11px;border:1px solid var(--line);border-left:3px solid var(--ok);border-radius:0 10px 10px 0;background:rgba(52,211,192,.07);font-size:.82rem;line-height:1.35}
.steps div{display:flex;gap:8px;color:var(--muted)}.steps div b{flex:0 0 18px;height:18px;border-radius:50%;display:grid;place-items:center;background:var(--line);color:var(--frost);font-size:.7rem}
.steps div.now{color:var(--frost)}.steps div.now b{background:var(--ok);color:#0A1830}.steps div.done{opacity:.55;text-decoration:line-through}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
</style>
<div id="banner" class="banner"></div>
<div id="sndhint" class="steps" style="display:none;margin-top:8px">The browser is holding the siren back until you click. Click anywhere on this panel to hear it.</div>
<div class="grid">
 <div class="box"><svg id="map" viewBox="0 0 1000 440" width="100%" role="img" aria-label="World map showing the flagged foreign transaction">
  <g id="grat" stroke="#1d3157" stroke-width=".6"></g><g id="dots"></g><g id="layer"></g></svg></div>
 <div class="box">
  <div class="top"><div class="tabs" id="tabs"></div><button class="snd" id="snd">Sound on</button></div>
  <div id="card"></div><div id="auth"></div><div class="log" id="log"></div>
 </div>
</div>
<script>
const CASES=__CASES__;
const POLY={
 na:[[-168,66],[-156,71],[-125,70],[-95,72],[-80,73],[-62,60],[-55,50],[-67,44],[-76,35],[-81,25],[-97,26],[-97,18],[-87,21],[-83,10],[-78,8],[-90,14],[-105,20],[-112,30],[-118,34],[-124,40],[-125,49],[-135,58],[-150,60],[-165,60]],
 sa:[[-78,8],[-60,10],[-50,0],[-35,-6],[-40,-22],[-48,-28],[-58,-38],[-65,-42],[-68,-52],[-72,-52],[-75,-40],[-71,-20],[-81,-5]],
 eu:[[-10,36],[-9,43],[-2,48],[-5,50],[5,53],[9,57],[5,62],[15,69],[28,71],[40,68],[40,55],[30,45],[28,41],[22,37],[12,38],[8,44],[-1,37]],
 af:[[-17,21],[-10,35],[10,37],[32,31],[43,12],[51,12],[40,-3],[40,-15],[35,-25],[20,-35],[12,-18],[9,-1],[5,5],[-8,4],[-17,14]],
 as:[[40,55],[40,68],[60,70],[100,78],[140,72],[170,66],[160,55],[142,46],[130,35],[122,30],[122,22],[108,20],[106,10],[100,2],[98,15],[92,22],[80,8],[72,20],[67,25],[57,25],[50,30],[40,38],[28,41],[30,48]],
 ar:[[35,30],[43,12],[52,16],[58,22],[56,26],[48,30]],
 au:[[114,-22],[122,-18],[131,-12],[142,-11],[146,-19],[153,-27],[150,-37],[140,-38],[130,-32],[115,-34]],
 gl:[[-55,60],[-20,70],[-20,82],[-60,82],[-70,76]]
};
const W=1000,H=440,X=lon=>(lon+180)/360*W,Y=lat=>(82-lat)/140*H;
const inside=(p,poly)=>{let c=false;for(let i=0,j=poly.length-1;i<poly.length;j=i++){const a=poly[i],b=poly[j];
 if((a[1]>p[1])!=(b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])c=!c}return c};
(function(){let d='',g='';const P=Object.values(POLY);
 for(let lat=80;lat>-58;lat-=3)for(let lon=-180;lon<180;lon+=3)if(P.some(q=>inside([lon,lat],q)))d+=`<circle cx="${X(lon).toFixed(1)}" cy="${Y(lat).toFixed(1)}" r="1.7"/>`;
 for(let lon=-180;lon<=180;lon+=30)g+=`<line x1="${X(lon)}" y1="0" x2="${X(lon)}" y2="${H}"/>`;
 for(let lat=60;lat>=-30;lat-=30)g+=`<line x1="0" y1="${Y(lat)}" x2="${W}" y2="${Y(lat)}"/>`;
 document.getElementById('dots').innerHTML=d;document.getElementById('grat').innerHTML=g})();

const $=s=>document.querySelector(s),RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const S=CASES.map(()=>({a:false,o:false,state:'open',log:[],sent:false}));let cur=0,snd=true,ac=null,sirenNode=null,sirenTimer=0;
const clock=()=>new Date().toLocaleTimeString([], {hour12:false});
function tone(seq){if(!snd)return;try{ctx();let t=ac.currentTime;
 seq.forEach(([f,d])=>{const o=ac.createOscillator(),g=ac.createGain();o.frequency.value=f;g.gain.value=.05;o.connect(g);g.connect(ac.destination);o.start(t);o.stop(t+d);t+=d})}catch(e){}}
const chime=()=>tone([[660,.12],[990,.2]]);
function ctx(){if(!ac){ac=new (window.AudioContext||window.webkitAudioContext)();ac.onstatechange=()=>{if(ac.state==='running')$('#sndhint').style.display='none'}}
 if(ac.state==='suspended')ac.resume().catch(()=>{});return ac}
/* Real siren: sawtooth wail sweeping 560-1240 Hz about once a second, low-passed, moderate level (0.28). Stops on block, dismiss, tab change or after 14 s. */
function startSiren(){if(!snd||sirenNode||S[cur].state!=='open')return;try{const a=ctx(),o=a.createOscillator(),l=a.createOscillator(),lg=a.createGain(),f=a.createBiquadFilter(),g=a.createGain(),t=a.currentTime;
 o.type='sawtooth';o.frequency.value=900;l.type='triangle';l.frequency.value=.9;lg.gain.value=340;l.connect(lg);lg.connect(o.frequency);
 f.type='lowpass';f.frequency.value=2200;g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(.28,t+.25);
 o.connect(f);f.connect(g);g.connect(a.destination);o.start();l.start();sirenNode={o,l,g};
 sirenTimer=setTimeout(stopSiren,14000);setTimeout(()=>{$('#sndhint').style.display=(sirenNode&&ac.state==='suspended')?'block':'none'},400)}catch(e){}}
function stopSiren(){clearTimeout(sirenTimer);$('#sndhint').style.display='none';if(!sirenNode)return;const n=sirenNode;sirenNode=null;
 try{const t=ac.currentTime;n.g.gain.cancelScheduledValues(t);n.g.gain.setValueAtTime(n.g.gain.value,t);n.g.gain.linearRampToValueAtTime(0,t+.2)}catch(e){}
 setTimeout(()=>{try{n.o.stop();n.l.stop()}catch(e){}},300)}
/* "Verified": bright rising four-note chime with a soft sustained final note, played after police are notified and the case is acknowledged. */
function verified(){if(!snd)return;try{const a=ctx(),t0=a.currentTime+.05;
 [[784,0,.18],[988,.12,.18],[1319,.24,.2],[1568,.38,.9]].forEach(([fr,at,d])=>{const o=a.createOscillator(),o2=a.createOscillator(),g=a.createGain();
  o.type='sine';o2.type='triangle';o.frequency.value=fr;o2.frequency.value=fr*2;const st=t0+at;
  g.gain.setValueAtTime(0,st);g.gain.linearRampToValueAtTime(.2,st+.02);g.gain.exponentialRampToValueAtTime(.0008,st+d+.35);
  o.connect(g);o2.connect(g);g.connect(a.destination);o.start(st);o2.start(st);o.stop(st+d+.4);o2.stop(st+d+.4)})}catch(e){}}
function say(i,t){S[i].log.push(`<div>[${clock()}] ${t}</div>`);if(i===cur)renderLog()}

function renderBanner(){const s=S[cur],c=CASES[cur],b=$('#banner');
 if(s.state==='open'){b.className='banner alert';b.innerHTML=`<span>&#9888;</span> Foreign anomaly: ${c.txn.city}, ${c.txn.country}. Authorization needed`}
 else if(s.state==='frozen'){b.className='banner ok';b.innerHTML=`<span>&#10003;</span> Transaction blocked. Report queued for ${c.station} (simulated)`}
 else{b.className='banner off';b.innerHTML='Dismissed as false positive'}}
function renderTabs(){$('#tabs').innerHTML=CASES.map((c,i)=>`<button class="tab ${i===cur?'on':''}" data-i="${i}"><i class="${S[i].state}"></i>${c.txn.city}</button>`).join('')}
function renderCard(){const c=CASES[cur],s=S[cur],cls=s.state==='open'?'':s.state==='frozen'?'ok':'off';
 $('#card').innerHTML=`<div class="head"><div class="beacon ${cls}"></div><div><h4>Transaction ${c.id}</h4><div style="color:var(--muted);font-size:.85rem">Card issued at home in ${c.home.city}, used in ${c.txn.city}</div></div></div>
 <div class="rows"><span>Amount</span><span>$${c.amount.toLocaleString()}</span><span>Distance</span><span>${c.km.toLocaleString()} km from home</span>
 <span>Federated model score</span><span>${(c.score*100).toFixed(1)}%<div class="bar"><b id="sbar"></b></div></span>
 <span>Status</span><span>${s.state==='frozen'?'<span class="stamp">BLOCKED</span>':s.state==='open'?'PENDING at card network':'RELEASED'}</span></div>
 <div class="chips">${c.signals.map(x=>`<span class="chip">${x}</span>`).join('')}</div>`;
 requestAnimationFrame(()=>requestAnimationFrame(()=>{const e=$('#sbar');if(e)e.style.width=(c.score*100)+'%'}))}
function renderAuth(){const s=S[cur],open=s.state==='open',ready=open&&s.a&&s.o;
 const key=(k,n)=>`<button class="hold ${s[k]?'done':''}" data-k="${k}" ${!open||s[k]?'disabled':''}><svg viewBox="0 0 44 44"><circle class="bg" cx="22" cy="22" r="18"/><circle class="fg" cx="22" cy="22" r="18" stroke-dasharray="113.1" stroke-dashoffset="${s[k]?0:113.1}"/></svg><span><b>${n}</b><small>${s[k]?'Authorized':'Hold to authorize'}</small></span></button>`;
 const st1=!(s.a&&s.o)&&open,st2=ready;const stp=(n,t,c)=>`<div class="${c}"><b>${n}</b><span>${t}</span></div>`;
 $('#auth').innerHTML=(open?`<div class="steps">${stp(1,'Press and HOLD each key for about 1 second until its ring fills',st1?'now':'done')}${stp(2,'Both keys must say Authorized',st1?'':'done')}${stp(3,'Click the red button to block the transaction',st2?'now':'')}</div>`:'')+`<div class="keys">${key('a','Fraud analyst')}${key('o','Compliance officer')}</div>
 <button class="freeze ${ready?'ready':''}" id="freeze" ${ready?'':'disabled'}>${s.state==='frozen'?'Transaction blocked':ready?'Shut down transaction and alert police':'Locked: two authorizations needed'}</button>
 ${open?'<button class="link" id="dismiss">Dismiss as false positive</button>':''}`}
function renderLog(){const s=S[cur],c=CASES[cur];let extra='';
 if(s.state==='frozen')extra=`<details open><summary>Case file sent (customer identity withheld)</summary><pre>${JSON.stringify(report(c),null,1)}</pre></details>`;
 $('#log').innerHTML=s.log.join('')+extra}
const report=c=>({case_ref:c.ref,txn_id:c.id,amount_usd:c.amount,model_score:+c.score.toFixed(3),flagged_location:`${c.txn.city}, ${c.txn.country}`,card_home_country:c.home.country,signals:c.signals,
 customer_identity:'withheld until a formal legal request',authorized_by:['fraud_analyst','compliance_officer'],simulation:true});

function arcOf(c){const x1=X(c.home.lon),y1=Y(c.home.lat),x2=X(c.txn.lon),y2=Y(c.txn.lat),d=Math.hypot(x2-x1,y2-y1);
 return `M${x1},${y1} Q${(x1+x2)/2},${Math.min(y1,y2)-d*.18-8} ${x2},${y2}`}
function renderMap(){const c=CASES[cur],s=S[cur],x1=X(c.home.lon),y1=Y(c.home.lat),x2=X(c.txn.lon),y2=Y(c.txn.lat),ok=s.state==='frozen',off=s.state==='dismissed',rc=off?'':ok?'ok':'';
 const rings=off?'':`<circle class="ring ${rc}" cx="${x2}" cy="${y2}" r="12"/><circle class="ring r2 ${rc}" cx="${x2}" cy="${y2}" r="12"/><circle class="ring r3 ${rc}" cx="${x2}" cy="${y2}" r="12"/>`;
 $('#layer').innerHTML=`<path id="arc" d="${arcOf(c)}" fill="none" stroke="${off?'#2A4170':'#FFB547'}" stroke-width="2" stroke-dasharray="6 6" class="${off?'':'flow'}"/>
 <path id="arc2" d="${arcOf(c)}" fill="none" stroke="#34D3C0" stroke-width="3" style="display:${s.sent?'block':'none'}"/>
 <circle cx="${x1}" cy="${y1}" r="6" fill="#34D3C0"/><text x="${x1+10}" y="${y1+16}" fill="#E8EFFA" font-size="13">Card home: ${c.home.city}</text>
 ${rings}<circle cx="${x2}" cy="${y2}" r="7" fill="${ok?'#34D3C0':off?'#8FA3C4':'#FF6B6B'}"/>
 <text x="${x2-10}" y="${y2-16}" fill="#E8EFFA" font-size="13" text-anchor="${x2>800?'end':'start'}">Foreign use: ${c.txn.city}</text>
 <g transform="translate(${x2+16},${y2+4})"><path d="M0,-9 L9,0 L0,9 L-9,0Z" fill="#12264A" stroke="#6EA8FF" stroke-width="2"/><text x="0" y="4" font-size="9" text-anchor="middle" fill="#6EA8FF">P</text></g>
 <text x="${x2+30}" y="${y2+24}" fill="#6EA8FF" font-size="12" text-anchor="${x2>800?'end':'start'}">Police cybercrime desk</text>
 <circle id="pkt" r="6" fill="#34D3C0" style="display:none"/>`}
const renderAll=()=>{renderBanner();renderTabs();renderCard();renderAuth();renderMap();renderLog()};

function dispatch(i){const c=CASES[i];if(RM){S[i].sent=true;if(i===cur)renderMap();return}
 const arc=$('#arc2'),pkt=$('#pkt');if(!arc||i!==cur)return;const len=arc.getTotalLength(),t0=performance.now(),D=1800;arc.style.display='block';pkt.style.display='block';
 arc.style.strokeDasharray=len;const step=n=>{if(cur!==i)return;const p=Math.min(1,(n-t0)/D);arc.style.strokeDashoffset=len*(1-p);const pt=arc.getPointAtLength(len*p);pkt.setAttribute('cx',pt.x);pkt.setAttribute('cy',pt.y);
  if(p<1)requestAnimationFrame(step);else{S[i].sent=true;pkt.style.display='none';arc.style.strokeDasharray='none'}};requestAnimationFrame(step)}
function sign(k){const s=S[cur],n=k==='a'?'Fraud analyst':'Compliance officer';s[k]=true;say(cur,`<em>${n}</em> key accepted`);chime();renderAuth()}
function freeze(){const i=cur,c=CASES[i],s=S[i];if(!(s.a&&s.o)||s.state!=='open')return;s.state='frozen';stopSiren();chime();renderAll();dispatch(i);
 [[0,`Transaction ${c.id} set to <em>BLOCKED</em> at the card network (simulated)`],[500,`Case file ${c.ref} built: customer identity withheld`],[1900,`Report delivered to ${c.station} (simulated)`],[2500,'Acknowledgement received. Case open.']]
 .forEach(([d,t])=>setTimeout(()=>{say(i,t);if(t.indexOf('Acknowledgement')===0)verified()},RM?0:d))}

let hold=null;const D=1100;
function startHold(btn){if(!btn||btn.disabled||hold)return;const k=btn.dataset.k,fg=btn.querySelector('.fg'),t0=performance.now();btn.classList.add('holding');
 hold={btn,fg,raf:0};const tick=n=>{const p=RM?1:Math.min(1,(n-t0)/D);fg.style.strokeDashoffset=113.1*(1-p);if(p>=1){hold=null;sign(k)}else hold.raf=requestAnimationFrame(tick)};hold.raf=requestAnimationFrame(tick)}
function endHold(){if(!hold)return;cancelAnimationFrame(hold.raf);hold.fg.style.strokeDashoffset=113.1;hold.btn.classList.remove('holding');hold=null}
const au=$('#auth');
au.addEventListener('pointerdown',e=>startHold(e.target.closest('.hold')));
au.addEventListener('pointerleave',e=>{if(e.target.classList&&e.target.classList.contains('hold'))endHold()},true);document.addEventListener('pointerup',endHold);document.addEventListener('pointercancel',endHold);
au.addEventListener('contextmenu',e=>e.preventDefault());
au.addEventListener('keydown',e=>{if((e.key===' '||e.key==='Enter')&&e.target.closest('.hold')){e.preventDefault();if(!e.repeat)startHold(e.target.closest('.hold'))}});
au.addEventListener('keyup',e=>{if(e.key===' '||e.key==='Enter')endHold()});
au.addEventListener('click',e=>{if(e.target.closest('#freeze'))freeze();if(e.target.closest('#dismiss')){S[cur].state='dismissed';stopSiren();say(cur,'Alert dismissed by analyst. Transaction released.');renderAll()}});
$('#tabs').addEventListener('click',e=>{const t=e.target.closest('.tab');if(t){endHold();stopSiren();cur=+t.dataset.i;renderAll();startSiren()}});
$('#snd').onclick=()=>{snd=!snd;$('#snd').textContent=snd?'Sound on':'Sound off';if(snd)startSiren();else stopSiren()};
document.addEventListener('pointerdown',()=>{if(ac&&ac.state==='suspended')ac.resume()},true);
CASES.forEach((c,i)=>say(i,`Model flagged ${c.id}: score ${(c.score*100).toFixed(1)}% above threshold`));
renderAll();startSiren();
</script>"""


def console(cases):
    return HTML.replace("__CASES__", json.dumps(cases))
