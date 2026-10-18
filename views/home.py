import streamlit as st, streamlit.components.v1 as components
from ui.html_blocks import hero_diagram, slider
from ui.components import kpi
from ui.media import home_banner, home_tiles, howto, zero_downtime
from ui.shared import fed, current
eps, rounds = current(); res = fed(eps, rounds); last = res["history"][-1]; best = max(v["auc"] for v in res["local"].values())
home_banner("IBM Z Datathon 2026 · Theme 2: AI Secured", "Banks catch fraud together without sharing a single customer record.",
  "AegisNet trains one fraud model across competing banks. Data is noised on-site, model updates are masked, and the final merge runs on IBM LinuxONE (s390x).")
st.markdown("### The idea in one picture")
components.html(hero_diagram(), height=330)
home_tiles()
c = st.columns(4)
kpi(c[0], "Shared model AUC", f"{last['auc']:.3f}", f"+{last['auc']-best:.3f} vs best single bank")
kpi(c[1], "Fraud caught", f"{last['recall']:.0%}", f"precision {last['precision']:.0%}")
kpi(c[2], "Records leaving banks", "0", "only masked updates travel")
kpi(c[3], "Privacy budget", f"ε = {eps}", "noise on every feature")
zero_downtime()
st.markdown("### How it works")
st.caption("Swipe, click the dots, or use the arrows.")
components.html(slider(), height=360)
