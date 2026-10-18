import streamlit as st
from core.platform_proof import platform_report
from ui.components import note
from ui.media import banner
banner("linuxone", "Live facts from the machine running this app.", title="IBM LinuxONE")
rep = platform_report()
st.markdown("**Live facts from the machine running this app**")
st.json({k: v for k, v in rep.items() if k != "cpu_features"})
if rep["is_s390x"]: st.success("Running on s390x (IBM Z / LinuxONE).")
else: st.info("Not on s390x. This is your laptop. Run the same app on the LinuxONE VM to see the real values.")
st.code("docker build -t aegisnet .\ndocker run -p 8501:8501 aegisnet", language="bash")
note("Secure Execution is only shown as active when the flag above is 1. Do not claim it otherwise.")
