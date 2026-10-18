import numpy as np, streamlit as st, streamlit.components.v1 as components
from math import radians, sin, cos, asin, sqrt
from core.privacy import to_unit
from core.federated import sig
from ui.shared import data, fed, current
from ui.components import note, kpi
from ui.media import banner, howto
from ui.alert_console import console

# Simulated placements: (card home city, foreign city where the transaction happened)
SCENES = [
    (dict(city="London", country="UK", lon=-0.13, lat=51.5), dict(city="Lagos", country="Nigeria", lon=3.39, lat=6.45)),
    (dict(city="Mumbai", country="India", lon=72.88, lat=19.08), dict(city="São Paulo", country="Brazil", lon=-46.63, lat=-23.55)),
    (dict(city="New York", country="USA", lon=-74.0, lat=40.71), dict(city="Bucharest", country="Romania", lon=26.1, lat=44.43)),
]

def km(a, b):
    p1, p2 = radians(a["lat"]), radians(b["lat"]); dl = radians(b["lon"] - a["lon"])
    h = sin((p2 - p1) / 2) ** 2 + cos(p1) * cos(p2) * sin(dl / 2) ** 2
    return int(2 * 6371 * asin(sqrt(h)))

banks, test = data(); res = fed(*current())
banner("alerts", "Authorize, block and notify police. Simulation only.", title="Fraud alert console")
howto("How to use the console", [
  "Drag the <b>Alert threshold</b> slider below. Higher means fewer, surer alerts. Lower means more alerts.",
  "Click a <b>city tab</b> on the right panel to switch between flagged transactions.",
  "<b>Press and HOLD</b> each key (Fraud analyst, then Compliance officer) for about one second until its ring fills. Keep the pointer on the key.",
  "When both keys show <b>Authorized</b>, the red button unlocks. Click <b>Shut down transaction and alert police</b>.",
  "Not fraud? Click <b>Dismiss as false positive</b> under the red button."])
note("Simulation only. Nothing is sent to any real police service. A real deployment needs an official legal reporting channel and named, authorized officers.")

thr = st.slider("Alert threshold: only transactions scored above this are flagged (drag left for more alerts)", 0.50, 0.99, 0.80, 0.01,
                help="The score is the federated model's fraud probability, from 0.50 to 0.99.")
w, b = res["weights"], res.get("bias", 0.0)
t = test.assign(score=sig(to_unit(test) @ w + b))
intl = t[t.is_international == 1].sort_values("score", ascending=False)
hits = intl[intl.score >= thr]

c = st.columns(3)
kpi(c[0], "International transactions", f"{len(intl):,}")
kpi(c[1], "Above threshold", f"{len(hits):,}", "top 3 shown below", good=False)
kpi(c[2], "Customer identities shared", "0", "case file carries no PII")

cases = []
for i, (_, r) in enumerate(hits.head(3).iterrows()):
    home, txn = SCENES[i]
    sig_ = [f"Card home {home['country']}, used in {txn['country']}"]
    if r.amount_ratio >= 2: sig_.append(f"Amount {r.amount_ratio:.1f}x the 30-day average")
    if r.device_new: sig_.append("New device")
    if r.merchant_risk >= .6: sig_.append(f"Merchant risk {r.merchant_risk:.2f}")
    if r.velocity_24h >= 4: sig_.append(f"{int(r.velocity_24h)} transactions in 24h")
    cases.append(dict(id=r.txn_id, amount=round(float(r.amount), 2), score=float(r.score), signals=sig_,
                      home=home, txn=txn, km=km(home, txn), ref=f"CF-2026-{r.txn_id[-4:]}",
                      station=f"{txn['city']} police cybercrime desk"))

if cases:
    components.html(console(cases), height=760, scrolling=True)
    st.caption("Cities are simulated placements for the demo. Nothing leaves this page.")
else:
    st.info("No international transaction scores above this threshold. Lower it to see alerts.")
