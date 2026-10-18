import streamlit as st
# aegisnet-noarrow: pyarrow is not available on this s390x VM, so draw tables as plain HTML
try:
    import pyarrow  # noqa: F401
    if getattr(pyarrow, "__aegis_stub__", False):
        raise ImportError
except ImportError:
    import pandas as _pd
    from streamlit.delta_generator import DeltaGenerator as _DG
    def _html_df(self, data, *a, **k):
        d = data if isinstance(data, _pd.DataFrame) else _pd.DataFrame(data)
        h = k.get("height")
        h = h if isinstance(h, int) else 360
        t = d.to_html(index=not k.get("hide_index", False), border=0, classes="aegtbl")
        self.markdown('<style>.aegtbl{width:100%;font-size:.85rem;border-collapse:collapse}'
                      '.aegtbl th,.aegtbl td{padding:4px 10px;text-align:left;border-bottom:1px solid rgba(255,255,255,.12)}</style>'
                      f'<div style="max-height:{h}px;overflow:auto">{t}</div>', unsafe_allow_html=True)
    _DG.dataframe = _html_df                       # col.dataframe(...) / with col: ...
    st.dataframe = lambda data, *a, **k: _html_df(st, data, *a, **k)   # st.dataframe(...)
import re
from ui.styles import inject_css, inject_background, inject_fx, inject_transition
from ui.media import inject_media, brand_title, scroll_handoff
from ui.icons import MATERIAL
from ui.shared import controls

st.set_page_config(page_title="AegisNet", page_icon=MATERIAL["home"], layout="wide")
inject_css(); inject_background(); inject_fx(); inject_media()
nav = st.navigation([
    st.Page("views/home.py", title="Overview", icon=MATERIAL["home"], default=True),
    st.Page("views/federation.py", title="Federation", icon=MATERIAL["federation"]),
    st.Page("views/privacy.py", title="Privacy", icon=MATERIAL["privacy"]),
    st.Page("views/secure.py", title="Secure merge", icon=MATERIAL["secure"]),
    st.Page("views/alerts.py", title="Alerts", icon=MATERIAL["alerts"]),
    st.Page("views/laundering.py", title="Laundering", icon=MATERIAL["laundering"]),
    st.Page("views/data.py", title="Data", icon=MATERIAL["data"]),
    st.Page("views/linuxone.py", title="LinuxONE", icon=MATERIAL["linuxone"]),
], position="top")
controls()  # after st.navigation, so st.page_link can find the registered pages
brand_title()
scroll_handoff()
inject_transition(re.sub(r"\W", "", nav.title) or "home")
nav.run()
