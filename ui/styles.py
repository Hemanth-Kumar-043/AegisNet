import streamlit as st
from .theme import *

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=IBM+Plex+Sans:wght@400;500&family=IBM+Plex+Mono:wght@400&display=swap');
html, body, [class*="css"], .stApp {{ font-family:'IBM Plex Sans',sans-serif; color:{FROST}; }}
.stApp {{ background: radial-gradient(1200px 500px at 85% -10%, #17356b 0%, {INK} 60%); }}
h1,h2,h3 {{ font-family:'Space Grotesk',sans-serif !important; letter-spacing:-0.02em; color:{FROST}; }}
section[data-testid="stSidebar"] {{ background:{PANEL}; border-right:1px solid {LINE}; }}
.hero {{ padding:2.2rem 0 1.4rem; max-width:62rem; }}
.hero h1 {{ font-size:3.1rem; line-height:1.05; margin:0 0 .6rem; }}
.hero p {{ font-size:1.12rem; color:{MUTED}; max-width:44rem; line-height:1.55; margin:0; }}
.badge {{ display:inline-block; font-size:.82rem; padding:.3rem .75rem; border:1px solid {SECURE}; color:{SECURE};
  border-radius:999px; margin-bottom:1rem; }}
.kpi {{ background:{PANEL}; border:1px solid {LINE}; border-radius:14px; padding:1.1rem 1.25rem; }}
.kpi .v {{ font-family:'Space Grotesk'; font-size:2.1rem; font-weight:700; }}
.kpi .l {{ color:{MUTED}; font-size:.9rem; }}
.kpi .d {{ font-size:.85rem; margin-top:.2rem; }}
.note {{ border-left:3px solid {WARN}; background:#1b2a4a; padding:.8rem 1rem; border-radius:0 10px 10px 0;
  color:{FROST}; font-size:.95rem; }}
.mono {{ font-family:'IBM Plex Mono',monospace; font-size:.85rem; color:{MUTED}; }}
button[data-baseweb="tab"] {{ font-family:'Space Grotesk'; font-size:1rem; }}
div[data-testid="stDataFrame"] {{ border:1px solid {LINE}; border-radius:12px; }}
@media (prefers-reduced-motion: no-preference) {{ .hero {{ animation: rise .6s ease-out both; }}
  @keyframes rise {{ from {{opacity:0; transform:translateY(10px)}} to {{opacity:1; transform:none}} }} }}
</style>
"""
def inject_css(): st.markdown(CSS, unsafe_allow_html=True)

BG = f"""
<style>
.stApp::before {{ content:""; position:fixed; inset:0; z-index:0; pointer-events:none;
  background-image: linear-gradient(rgba(52,211,192,.07) 1px, transparent 1px), linear-gradient(90deg, rgba(52,211,192,.07) 1px, transparent 1px);
  background-size:52px 52px; animation: drift 26s linear infinite;
  -webkit-mask-image: radial-gradient(ellipse 80% 70% at 50% 25%, #000 25%, transparent 80%); mask-image: radial-gradient(ellipse 80% 70% at 50% 25%, #000 25%, transparent 80%); }}
.stApp::after {{ content:""; position:fixed; inset:-20%; z-index:0; pointer-events:none; filter: blur(70px); opacity:.5;
  background: radial-gradient(420px 320px at 20% 30%, rgba(52,211,192,.35), transparent 70%), radial-gradient(500px 360px at 80% 20%, rgba(110,168,255,.35), transparent 70%), radial-gradient(380px 300px at 60% 85%, rgba(181,140,255,.25), transparent 70%);
  animation: float 22s ease-in-out infinite alternate; }}
[data-testid="stAppViewContainer"] {{ position:relative; z-index:1; background:transparent; }}
[data-testid="stHeader"] {{ background:transparent; }}
@keyframes drift {{ to {{ background-position:52px 52px, 52px 52px; }} }}
@keyframes float {{ from {{ transform:translate(-3%,-2%) scale(1); }} to {{ transform:translate(4%,3%) scale(1.12); }} }}
@media (prefers-reduced-motion: reduce) {{ .stApp::before, .stApp::after {{ animation:none; }} }}
</style>
"""
def inject_background(): st.markdown(BG, unsafe_allow_html=True)


_SEL = ['[data-testid="stTopNavLink"]', '[data-testid="stSidebarNavLink"]', 'header a[href]', '.stButton button',
        '.stDownloadButton button', 'button[data-baseweb="tab"]']
_SEL += ['[data-testid="stPageLink-NavLink"]', '[data-testid="stBaseButton-secondary"]', '[data-testid="stBaseButton-primary"]', 'a[data-testid="stBaseLinkButton-secondary"]']
_ALL = ", ".join(_SEL); _HOV = ", ".join(x + ":hover" for x in _SEL) + ", " + ", ".join(x + ":focus-visible" for x in _SEL)
FX = f"""
<style>
{_ALL} {{ border-radius:10px; transition: transform .22s cubic-bezier(.2,.9,.3,1.35), box-shadow .22s ease, background-color .22s ease, color .22s ease !important; }}
{_HOV} {{ transform: translateY(-4px) scale(1.08); background-color: rgba(52,211,192,.14) !important; color:#fff !important;
  box-shadow: 0 0 0 1px {SECURE}, 0 0 18px rgba(52,211,192,.55), 0 10px 26px rgba(52,211,192,.28); }}
@media (prefers-reduced-motion: reduce) {{ {_HOV} {{ transform:none; }} }}
</style>
"""
EXTRA = f"""
<style>
.stButton button, .stDownloadButton button {{ border:1.5px solid {SECURE} !important; background:rgba(52,211,192,.10) !important; font-weight:600; padding:.55rem 1.3rem; cursor:pointer; }}
.stButton button:active, .stDownloadButton button:active, [data-testid="stPageLink-NavLink"]:active {{ transform:translateY(0) scale(.97) !important; }}
[data-testid="stTopNavLink"], header a[href] {{ font-size:1.02rem !important; font-weight:600 !important; padding:.5rem .9rem !important; }}
[data-testid="stTopNavLink"] svg, [data-testid="stTopNavLink"] span[data-testid="stIconMaterial"] {{ font-size:1.5rem !important; color:{SECURE}; }}
[data-testid="stSidebar"] [data-testid="stSlider"] [role="slider"] {{ width:22px; height:22px; box-shadow:0 0 0 4px rgba(52,211,192,.28); }}
[data-testid="stSlider"] [role="slider"]:hover {{ box-shadow:0 0 0 7px rgba(52,211,192,.4); transform:scale(1.15); }}
</style>"""
def inject_fx(): st.markdown(FX + EXTRA, unsafe_allow_html=True)

def inject_transition(slug):
    """Fade-in and rise on page change. The animation name changes per page, which restarts the animation."""
    st.markdown(f"""<style>
@keyframes veil_{slug} {{ 0% {{opacity:1}} 30% {{opacity:1}} 100% {{opacity:0}} }}
@keyframes rise_{slug} {{ 0% {{opacity:0; transform:translateY(26px)}} 35% {{opacity:0; transform:translateY(26px)}} 100% {{opacity:1; transform:none}} }}
@keyframes sweep {{ from {{transform:translateX(-90px)}} to {{transform:translateX(90px)}} }}
.pgveil {{ position:fixed; inset:0; z-index:999999; pointer-events:none; background:{INK}; opacity:0; animation:veil_{slug} 1s ease-out both;
  display:flex; align-items:center; justify-content:center; }}
.pgveil::after {{ content:""; width:150px; height:3px; border-radius:3px; background:linear-gradient(90deg,transparent,{SECURE},transparent); animation:sweep .9s ease-in-out; }}
[data-testid="stMainBlockContainer"], .block-container {{ animation:rise_{slug} .95s cubic-bezier(.2,.8,.2,1) both; }}
@media (prefers-reduced-motion: reduce) {{ .pgveil {{display:none}} [data-testid="stMainBlockContainer"], .block-container {{animation:none}} }}
</style><div class="pgveil"></div>""", unsafe_allow_html=True)
