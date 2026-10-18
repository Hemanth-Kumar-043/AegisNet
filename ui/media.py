"""Image banners, big overview tiles, sidebar navigation and how-to panels.
Images live in ./static and are served by Streamlit (server.enableStaticServing = true), at /app/static/<file>."""
import streamlit as st
from .icons import icon, MATERIAL
from .theme import *

S = "/app/static"
IMAGES = {"hero": "hero.jpg", "top": "tile_top.jpg", "blue": "tile_blue.jpg", "logo": "tile_logo.jpg", "mid": "tile_mid.jpg",
          "stage": "stage.jpg", "ztile": "ztile.jpg", "portrait": "portrait.jpg"}

# key, page file, label, one-line description, tile image
PAGES = [
    ("home", "views/home.py", "Overview", "Start here: the idea, the numbers and every lab.", "hero"),
    ("federation", "views/federation.py", "Federation", "See one shared model beat every bank working alone.", "top"),
    ("privacy", "views/privacy.py", "Privacy", "Slide the privacy budget and watch what noise costs.", "blue"),
    ("secure", "views/secure.py", "Secure merge", "Masked updates that cancel out in the sum.", "logo"),
    ("alerts", "views/alerts.py", "Alerts", "Fraud console: authorize, block, notify police (simulated).", "stage"),
    ("laundering", "views/laundering.py", "Laundering", "Replay six famous laundering routes hop by hop.", "mid"),
    ("data", "views/data.py", "Data", "Browse the synthetic transactions. No personal data.", "ztile"),
    ("linuxone", "views/linuxone.py", "LinuxONE", "Live proof of the machine this app runs on.", "portrait"),
]
BYKEY = {p[0]: p for p in PAGES}

import base64 as _b64
from pathlib import Path as _Path
_STATIC = _Path(__file__).resolve().parent.parent / "static"

def _uri(name):
    """Embed the image in the CSS itself so it shows on any host (no static-file serving needed)."""
    try:
        return "data:image/jpeg;base64," + _b64.b64encode((_STATIC / name).read_bytes()).decode()
    except OSError:
        return f"{S}/{name}"   # fall back to static serving

CSS = "<style>" + "".join(f".im-{k}{{background-image:url({_uri(v)});}}" for k, v in IMAGES.items()) + f"""
/* ---------- image banner (hover = slow magnify, like a console store page) ---------- */
.pb {{ position:relative; overflow:hidden; border-radius:18px; border:1px solid {LINE}; margin:0 0 1.2rem; min-height:150px;
  display:flex; align-items:center; box-shadow:0 12px 40px rgba(0,0,0,.35); isolation:isolate; }}
.pb .bg {{ position:absolute; inset:0; z-index:-2; background-size:cover; background-position:center; transform:scale(1.02);
  transition:transform 1.4s cubic-bezier(.2,.7,.2,1), filter .6s ease; filter:saturate(1.05); }}
.pb::after {{ content:""; position:absolute; inset:0; z-index:-1;
  background:linear-gradient(90deg, rgba(10,24,48,.96) 0%, rgba(10,24,48,.80) 42%, rgba(10,24,48,.15) 100%); }}
.pb:hover .bg {{ transform:scale(1.14); filter:saturate(1.25) brightness(1.12); }}
.pb .in {{ padding:1.5rem 1.8rem; max-width:46rem; display:flex; gap:1.1rem; align-items:center; }}
.pb .ic {{ flex:0 0 auto; width:66px; height:66px; border-radius:18px; display:grid; place-items:center; color:{SECURE};
  background:rgba(52,211,192,.12); border:1px solid rgba(52,211,192,.55); box-shadow:0 0 22px rgba(52,211,192,.25); transition:transform .3s cubic-bezier(.2,.9,.3,1.4); }}
.pb:hover .ic {{ transform:scale(1.12) rotate(-4deg); }}
.pb h2 {{ margin:0 0 .25rem; font-size:2rem; padding:0; }} .pb p {{ margin:0; color:#c5d3ec; font-size:1.02rem; line-height:1.5; }}
.pb.big {{ min-height:360px; }} .pb.big .in {{ padding:2.4rem 2.4rem; display:block; max-width:44rem; }}
.pb.big h1 {{ font-size:3.1rem; line-height:1.05; margin:0 0 .8rem; }} .pb.big p {{ font-size:1.15rem; }}
.pb.big .bg {{ background-position:right center; }}
.pb.big::after {{ background:linear-gradient(90deg, rgba(10,24,48,.97) 0%, rgba(10,24,48,.78) 45%, rgba(10,24,48,0) 78%); }}
.pb .hint {{ position:absolute; right:14px; bottom:10px; font-size:.72rem; color:#9db4d8; letter-spacing:.04em; opacity:.8; }}

/* ---------- big overview tiles ---------- */
.tile {{ position:relative; overflow:hidden; border-radius:18px; border:1px solid {LINE}; height:250px; isolation:isolate;
  display:flex; flex-direction:column; justify-content:flex-end; padding:1.1rem 1.2rem; margin-bottom:.55rem; cursor:pointer;
  transition:transform .35s cubic-bezier(.2,.9,.3,1.25), box-shadow .35s ease, border-color .35s ease; }}
.tile .bg {{ position:absolute; inset:0; z-index:-2; background-size:cover; background-position:center; transition:transform 1s cubic-bezier(.2,.7,.2,1), filter .5s ease; }}
.tile::after {{ content:""; position:absolute; inset:0; z-index:-1; background:linear-gradient(180deg, rgba(10,24,48,.15) 0%, rgba(10,24,48,.92) 82%); }}
.tile:hover {{ transform:translateY(-8px) scale(1.035); border-color:{SECURE}; box-shadow:0 0 0 1px {SECURE}, 0 18px 46px rgba(52,211,192,.30); }}
.tile:hover .bg {{ transform:scale(1.22); filter:brightness(1.25) saturate(1.2); }}
.tile .ti {{ position:absolute; top:1rem; left:1.2rem; width:64px; height:64px; border-radius:18px; display:grid; place-items:center; color:{SECURE};
  background:rgba(10,24,48,.62); border:1px solid rgba(52,211,192,.6); backdrop-filter:blur(6px); transition:transform .35s cubic-bezier(.2,.9,.3,1.5), background .3s; }}
.tile:hover .ti {{ transform:scale(1.16) rotate(-5deg); background:rgba(52,211,192,.25); color:#fff; }}
.tile h3 {{ margin:0 0 .2rem; font-size:1.5rem; }} .tile p {{ margin:0; color:#c5d3ec; font-size:.95rem; line-height:1.4; }}
.tile .go {{ position:absolute; top:1.3rem; right:1.2rem; font-size:.78rem; color:{SECURE}; opacity:0; transform:translateX(-8px); transition:all .3s; letter-spacing:.06em; }}
.tile:hover .go {{ opacity:1; transform:none; }}
.tile.guide {{ cursor:default; background:{PANEL}; justify-content:flex-start; }} .tile.guide::after {{ display:none; }}
.tile.guide:hover {{ transform:none; box-shadow:none; border-color:{LINE}; }}
.tile.guide ol {{ margin:.4rem 0 0; padding-left:1.2rem; color:#c5d3ec; font-size:.95rem; line-height:1.65; }}

/* page_link under each tile becomes a big obvious button */
[data-testid="stPageLink-NavLink"] {{ width:100%; border:1px solid {LINE}; background:{PANEL}; border-radius:12px; padding:.7rem 1rem !important; font-weight:600; }}
[data-testid="stPageLink-NavLink"] p {{ font-size:1.02rem; }}
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {{ padding:.75rem .9rem !important; margin-bottom:.35rem; }}
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] p {{ font-size:1.05rem; }}
[data-testid="stPageLink-NavLink"][aria-current="page"] {{ border-color:{SECURE}; background:rgba(52,211,192,.12); }}

/* ---------- brand title ---------- */
.brand {{ display:flex; align-items:center; gap:1rem; margin:.2rem 0 1.1rem; }}
.brand .mark {{ width:54px; height:54px; display:grid; place-items:center; color:{SECURE};
  clip-path:polygon(25% 0,100% 0,100% 75%,75% 100%,0 100%,0 25%); background:rgba(52,211,192,.14); box-shadow:inset 0 0 0 1px {SECURE}; }}
.brand .name {{ font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:2.5rem; letter-spacing:.34em; line-height:1; color:#fff; text-transform:uppercase;
  text-shadow:0 0 22px rgba(52,211,192,.35); }}
.brand .name i {{ font-style:normal; color:{SECURE}; }}
.brand .rule {{ flex:1; height:2px; min-width:40px; background:linear-gradient(90deg,{SECURE},rgba(52,211,192,0)); clip-path:polygon(0 0,100% 0,96% 100%,0 100%); }}
.brand .tag {{ font-family:'IBM Plex Mono',monospace; font-size:.74rem; color:{MUTED}; letter-spacing:.22em; text-transform:uppercase; white-space:nowrap; }}
@media (max-width:760px) {{ .brand .name {{ font-size:1.6rem; letter-spacing:.2em; }} .brand .tag {{ display:none; }} }}

/* ---------- ZeroDowntime band ---------- */
.zd {{ position:relative; margin:2.2rem 0 1.8rem; padding:1.7rem 2rem; overflow:hidden; background:linear-gradient(100deg,#0c1d3c 0%,#12264A 55%,#0c1d3c 100%);
  clip-path:polygon(0 0,calc(100% - 38px) 0,100% 38px,100% 100%,38px 100%,0 calc(100% - 38px)); box-shadow:inset 0 0 0 1px {LINE}; }}
.zd::before {{ content:""; position:absolute; inset:0; background:repeating-linear-gradient(115deg,transparent 0 22px,rgba(52,211,192,.05) 22px 24px); pointer-events:none; }}
.zd::after {{ content:""; position:absolute; top:0; bottom:0; width:120px; left:-160px; background:linear-gradient(100deg,transparent,rgba(52,211,192,.28),transparent);
  transform:skewX(-20deg); animation:zdsweep 5.5s ease-in-out infinite; pointer-events:none; }}
@keyframes zdsweep {{ 0%,55% {{ left:-160px; }} 100% {{ left:110%; }} }}
.zd .word {{ position:relative; text-align:center; font-family:'Space Grotesk',sans-serif; font-weight:700; text-transform:uppercase; transform:skewX(-10deg);
  padding:0 8%; font-size:clamp(2rem,6.4vw,5rem); line-height:1; letter-spacing:.06em; }}
.zd .a {{ color:#fff; text-shadow:0 0 28px rgba(52,211,192,.45); }}
.zd .b {{ color:transparent; -webkit-text-stroke:2px {SECURE}; }}
.zd .blade {{ position:absolute; top:50%; height:3px; width:7%; background:{SECURE}; transform:skewX(-35deg); box-shadow:0 0 14px rgba(52,211,192,.8); }}
.zd .blade.l {{ left:1.2rem; }} .zd .blade.r {{ right:1.2rem; }}
.zd .blade.l::after,.zd .blade.r::after {{ content:""; position:absolute; left:0; right:35%; top:-9px; height:3px; background:rgba(52,211,192,.45); }}
.zd .blade.l::before,.zd .blade.r::before {{ content:""; position:absolute; left:0; right:65%; top:9px; height:3px; background:rgba(52,211,192,.3); }}
.zd:hover .b {{ color:rgba(52,211,192,.18); }}
.zd .b {{ transition:color .4s ease; }}
@media (prefers-reduced-motion: reduce) {{ .zd::after {{ animation:none; }} }}

/* ---------- top menu hands over to the sidebar on scroll ---------- */
.aegis-topnav, [data-testid^="stTopNav"] {{ transition:opacity .35s ease, transform .35s cubic-bezier(.2,.8,.2,1); }}
html.aegis-scrolled .aegis-topnav, html.aegis-scrolled [data-testid^="stTopNav"] {{ opacity:0; transform:translateY(-16px); pointer-events:none; }}
.st-key-aegisnav {{ max-height:0; opacity:0; overflow:hidden; transform:translateX(-26px); pointer-events:none;
  transition:max-height .5s ease, opacity .4s ease .08s, transform .5s cubic-bezier(.2,.8,.2,1); }}
html.aegis-scrolled .st-key-aegisnav {{ max-height:900px; opacity:1; transform:none; pointer-events:auto; }}
@media (prefers-reduced-motion: reduce) {{ .aegis-topnav, .st-key-aegisnav {{ transition:none; }} }}

/* ---------- how-to panel ---------- */
.howto {{ border:1px solid {LINE}; border-left:4px solid {SECURE}; background:linear-gradient(90deg, rgba(52,211,192,.10), rgba(18,38,74,.9)); border-radius:0 14px 14px 0;
  padding:.9rem 1.2rem 1rem; margin:.4rem 0 1rem; }}
.howto h4 {{ margin:0 0 .5rem; font-family:'Space Grotesk',sans-serif; font-size:1.02rem; color:{SECURE}; letter-spacing:.02em; text-transform:uppercase; }}
.howto ol {{ list-style:none; counter-reset:s; margin:0; padding:0; display:grid; gap:.45rem; }}
.howto li {{ counter-increment:s; display:flex; gap:.7rem; align-items:flex-start; font-size:.97rem; line-height:1.45; color:{FROST}; }}
.howto li::before {{ content:counter(s); flex:0 0 1.55rem; height:1.55rem; border-radius:50%; display:grid; place-items:center; font-weight:700; font-size:.85rem;
  color:#0A1830; background:{SECURE}; }}
.howto b {{ color:#fff; }}
@media (prefers-reduced-motion: reduce) {{ .pb .bg, .tile .bg, .tile, .pb .ic, .tile .ti {{ transition:none; }} .pb:hover .bg, .tile:hover .bg {{ transform:none; }} .tile:hover {{ transform:none; }} }}
</style>"""


def inject_media(): st.markdown(CSS, unsafe_allow_html=True)


def banner(key, sub=None, title=None, img=None, hint=True):
    _, _, label, desc, im = BYKEY[key]
    st.markdown(f'<div class="pb"><div class="bg im-{img or im}"></div><div class="in"><div class="ic">{icon(key, 38)}</div>'
                f'<div><h2>{title or label}</h2><p>{sub or desc}</p></div></div></div>', unsafe_allow_html=True)


def home_banner(badge, headline, text):
    st.markdown(f'<div class="pb big"><div class="bg im-hero"></div><div class="in"><span class="badge">{badge}</span>'
                f'<h1>{headline}</h1><p>{text}</p></div><span class="hint">Hover the image to zoom in</span></div>', unsafe_allow_html=True)


def howto(title, steps):
    li = "".join(f"<li><span>{s}</span></li>" for s in steps)
    st.markdown(f'<div class="howto"><h4>{title}</h4><ol>{li}</ol></div>', unsafe_allow_html=True)


def home_tiles():
    """Large clickable tiles for every page except Overview, plus a short guide tile."""
    items = [p for p in PAGES if p[0] != "home"]
    st.markdown("### Open a lab")
    st.caption("Click a tile's button to open that page. The same shortcuts are in the left sidebar and the top menu.")
    for row in range(0, len(items), 4):
        cols = st.columns(4)
        for col, (k, path, label, desc, im) in zip(cols, items[row:row + 4]):
            col.markdown(f'<div class="tile"><div class="bg im-{im}"></div><div class="ti">{icon(k, 36)}</div><span class="go">OPEN</span>'
                         f'<h3>{label}</h3><p>{desc}</p></div>', unsafe_allow_html=True)
            col.page_link(path, label=f"Open {label}", icon=MATERIAL[k])
    # fill the last row with a guide tile
    if len(items) % 4:
        cols = st.columns(4)
        cols[len(items) % 4].markdown(
            '<div class="tile guide"><h3>How to move around</h3><ol><li>Pick a tile or use the sidebar.</li>'
            '<li>Set <b>privacy</b> and <b>rounds</b> in the sidebar.</li><li>Hover anything that glows: it is clickable.</li></ol></div>',
            unsafe_allow_html=True)


def sidebar_nav():
    """Hidden at the top of a page; slides in when the reader scrolls down (see scroll_handoff)."""
    with st.container(key="aegisnav"):
        st.markdown("### Pages")
        st.caption("The top menu moves here when you scroll down.")
        for k, path, label, desc, im in PAGES:
            st.page_link(path, label=label, icon=MATERIAL[k])


def brand_title():
    st.markdown(f'<div class="brand"><div class="mark">{icon("home", 32, stroke=3.2)}</div><div class="name">Aegis<i>Net</i></div><div class="rule"></div>'
                '<div class="tag">Federated fraud defence</div></div>', unsafe_allow_html=True)


def zero_downtime():
    st.markdown('<div class="zd"><span class="blade l"></span><div class="word"><span class="a">Zero</span><span class="b">Downtime</span></div><span class="blade r"></span></div>',
                unsafe_allow_html=True)


_JS = r"""
(function(){
  var P=window.parent; if(!P||P.__aegisScroll) return;
  var D=P.document, s=D.createElement('script');
  s.textContent='('+function(){
    window.__aegisScroll=1; var root=document.documentElement, opened=false;
    function mark(){ var L=[].slice.call(document.querySelectorAll('[data-testid="stTopNavLink"]')); if(!L.length) return;
      L.forEach(function(a){ a.classList.add('aegis-topnav'); });
      var anc=[]; for(var n=L[0]; n; n=n.parentElement) anc.push(n);
      var lca=anc.filter(function(x){ return L.every(function(l){ return x.contains(l); }); })[0];
      if(lca && lca.tagName!=='HEADER' && lca!==document.body && lca.getAttribute('data-testid')!=='stHeader') lca.classList.add('aegis-topnav');
      [].forEach.call(document.querySelectorAll('header button'), function(b){ if(/^\s*more\s*$/i.test(b.textContent||'')) (b.closest('[data-testid*="Popover"]')||b).classList.add('aegis-topnav'); }); }
    function expandSidebar(){ var b=document.querySelector('[data-testid="stExpandSidebarButton"],[data-testid="collapsedControl"] button,[data-testid="stSidebarCollapsedControl"] button'); if(b) b.click(); }
    function set(y){ var on=y>120; if(on!==root.classList.contains('aegis-scrolled')){ root.classList.toggle('aegis-scrolled',on); if(on&&!opened){opened=true; setTimeout(expandSidebar,150);} if(!on)opened=false; } }
    document.addEventListener('scroll',function(e){ var t=e.target, y=0;
      if(t===document||t===document.documentElement||t===document.body) y=window.scrollY;
      else if(t&&t.matches&&t.matches('[data-testid="stMain"],section.main,[data-testid="stAppViewContainer"],.main')) y=t.scrollTop; else return;
      mark(); set(y); },true);
    setInterval(mark,700); mark();
  }.toString()+')()';
  D.head.appendChild(s);
})();
"""


def scroll_handoff():
    import streamlit.components.v1 as components
    components.html(f"<script>{_JS}</script>", height=0)
