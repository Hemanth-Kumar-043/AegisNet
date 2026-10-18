import pandas as pd, streamlit as st, plotly.graph_objects as go
from ui.shared import data, fed, current
from ui.components import note, style_fig
from ui.theme import *
from ui.media import banner, howto
banks, _ = data(); eps, rounds = current(); res = fed(eps, rounds)
banner("federation", "One shared model against every bank working alone.")
howto("How to read this page", ["The <b>teal line</b> is the shared model. Each round the banks merge, it climbs.","The <b>dotted lines</b> are single banks on their own. Where the teal line sits above them, sharing helped.","Change <b>rounds</b> or <b>privacy</b> in the left sidebar and the chart updates."])
h = pd.DataFrame(res["history"]); fig = go.Figure()
fig.add_scatter(x=h["round"], y=h["auc"], name="Federated (all banks)", line=dict(color=SECURE, width=4))
for i, (k, v) in enumerate(res["local"].items()):
    fig.add_hline(y=v["auc"], line=dict(color=SERIES[i + 1], dash="dot"), annotation_text=f"{k} alone", annotation_font_color=MUTED)
fig.add_hline(y=res["central"]["auc"], line=dict(color=WARN, dash="dash"), annotation_text="Pooled, no privacy (unsafe ceiling)", annotation_position="bottom right")
fig.update_layout(title="Test AUC by round", xaxis_title="Round", yaxis_title="AUC")
st.plotly_chart(style_fig(fig, 420))
note("Each bank mostly sees one fraud pattern. Alone it misses the other two. The shared model learns all three.")
mix = pd.concat(banks.values()).query("fraud_type!='none'").groupby(["bank", "fraud_type"]).size().unstack().fillna(0)
st.plotly_chart(style_fig(go.Figure([go.Bar(name=c, x=mix.index, y=mix[c]) for c in mix.columns]).update_layout(barmode="stack", title="Fraud patterns each bank sees"), 300))
