import streamlit as st
from ui.shared import data
from ui.media import banner
banks, test = data()
banner("data", "Synthetic transactions. No names, card numbers or addresses.")
st.markdown("Synthetic transactions. There are no names, card numbers or addresses in this data.")
import pandas as pd
st.dataframe(pd.concat(banks.values()).sample(200, random_state=1), height=380)
st.download_button("Download test set (CSV)", test.to_csv(index=False), "global_holdout_test.csv")
