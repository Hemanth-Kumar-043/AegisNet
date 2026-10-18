import numpy as np, pandas as pd, streamlit as st
from core.data_gen import FEATURES
from ui.shared import data, fed, current
from ui.components import kpi
from ui.media import banner, howto
banks, _ = data(); res = fed(*current()); smp = res["sample"]
banner("secure", "Banks send masked numbers. Only the sum is ever revealed.")
st.markdown("Banks send **masked** updates. The masks cancel in the sum, so the server learns the merged model and nothing about any one bank.")
names = list(banks)
df = pd.DataFrame({f"{n} real": smp["true"][i][:5] for i, n in enumerate(names)} | {f"{n} masked": smp["masked"][i][:5] for i, n in enumerate(names)}, index=FEATURES[:5]).round(3)
st.dataframe(df)
ok = np.allclose(smp["agg"], smp["exact"])
kpi(st.columns(3)[0], "Merged model equals exact sum", "Yes" if ok else "No", "masks cancelled" if ok else "check masking", ok)

st.caption("Masks here are simulated in one process. A production system adds key agreement between banks and recovery when a bank drops out.")
