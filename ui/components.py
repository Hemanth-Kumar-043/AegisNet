import streamlit as st
from .theme import *

def hero():
    st.markdown(f"""<div class="hero"><span class="badge">IBM Z Datathon 2026 · Theme 2: AI Secured</span>
    <h1>Banks catch fraud together without sharing a single customer record.</h1>
    <p>AegisNet trains one fraud model across competing banks. Data is noised on-site, model updates are masked,
    and the final merge runs on IBM LinuxONE (s390x).</p></div>""", unsafe_allow_html=True)

def kpi(col, label, value, delta=None, good=True):
    d = "" if delta is None else f'<div class="d" style="color:{SECURE if good else ALERT}">{delta}</div>'
    col.markdown(f'<div class="kpi"><div class="l">{label}</div><div class="v">{value}</div>{d}</div>', unsafe_allow_html=True)

def note(text): st.markdown(f'<div class="note">{text}</div>', unsafe_allow_html=True)

def style_fig(fig, h=380):
    fig.update_layout(height=h, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans", color=FROST), margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", y=-0.2), colorway=SERIES)
    fig.update_xaxes(gridcolor=LINE, zeroline=False); fig.update_yaxes(gridcolor=LINE, zeroline=False)
    return fig
