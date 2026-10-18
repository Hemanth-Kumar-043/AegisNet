import streamlit as st
from core.data_gen import load_all
from core.federated import run_federation, epsilon_sweep

@st.cache_data
def data(): return load_all()
@st.cache_data
def fed(eps, rounds): return run_federation(*data(), epsilon=eps, rounds=rounds)
@st.cache_data
def sweep(): return epsilon_sweep(*data())

def controls():
    from ui.media import sidebar_nav
    with st.sidebar:
        sidebar_nav()
        st.divider()
        st.markdown("### Privacy controls")
        st.caption("These two sliders change every page. Drag the round handle, or click anywhere on the bar. Arrow keys also work.")
        st.select_slider("Privacy budget ε (left = more private, right = more accurate)", [0.5, 1, 2, 5, 10, 20], value=5, key="eps",
                         help="Smaller ε adds more noise to each bank's data before training. 0.5 is strongest privacy, 20 is the weakest.")
        st.slider("Federated rounds (how many times the banks merge)", 3, 20, 10, key="rounds",
                  help="Each round the banks train locally, then the masked updates are merged. More rounds usually means a better model.")
        st.caption("ε is applied to each feature on the bank's own data before training. Labels are not noised.")
def current(): return st.session_state.get("eps", 5), st.session_state.get("rounds", 10)
