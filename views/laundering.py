import pandas as pd, streamlit as st, streamlit.components.v1 as components
from core.aml import make_ledger, scan, CTR
from core.aml_cases import CASES
from ui.laundering_map import laundering_map
from ui.components import note, kpi
from ui.media import banner, howto

@st.cache_data
def scanned(seed): df = make_ledger(seed); f, s = scan(df); return df, f, s

banner("laundering", "Six real cases, replayed hop by hop, plus how to stop them.", title="Money laundering lab")
note("Educational. Cases are simplified from public reports (court filings, US Senate, regulators, journalists). Routes are illustrative reconstructions, not exact transaction records. Not legal advice.")
t1, t2, t3, t4 = st.tabs(["Historic cases", "Spot it and stop it", "Live scanner", "Where AegisNet fits"])

with t1:
    howto("How to use the map", ["Click a <b>case name</b> above the map. The route plays by itself.",
      "Colors: <b style='color:#FFB547'>amber</b> placement, <b style='color:#6EA8FF'>blue</b> layering, <b style='color:#34D3C0'>teal</b> integration.",
      "Click any <b>numbered hop</b> in the right list to jump to it, or press <b>Replay route</b> to watch again."])
    components.html(laundering_map(CASES), height=800, scrolling=True)

with t2:
    a, b, c = st.columns(3)
    a.markdown("#### Placement\nDirty cash first enters the system: deposits, casinos, cash-heavy shops.\n\n**Look for:** cash just under reporting limits, deposits that do not fit the business.")
    b.markdown("#### Layering\nMoney is moved around to hide its origin: shells, wires, many banks and countries.\n\n**Look for:** money in and straight out, circular transfers, many senders to one exit.")
    c.markdown("#### Integration\nThe money returns looking clean: property, art, businesses, loans.\n\n**Look for:** assets far above known income, unexplained wealth, shell-owned property.")
    st.markdown("### Red flags and the control that catches each")
    st.markdown("""
| Red flag | Why it matters | Control that catches it |
|---|---|---|
| Cash deposits just under the reporting limit | Splitting cash to dodge reports (structuring) | Add up cash across days and branches, then file a report |
| Money in and straight out | The account is a pipe | Velocity and in/out ratio rules |
| Many senders, one receiver, one exit | A collection point for a network of mules | Fan-in / fan-out graph rules |
| Circular transfers | Money goes round to look legitimate | Cycle detection on the transfer graph |
| Shell companies with no real business | Hides who really owns the money | Beneficial-ownership checks and registries |
| Volume far above the business size | The Danske Estonia pattern | Peer-group baselines, branch risk limits |
| Politically exposed person involved | Corruption proceeds (1MDB pattern) | PEP screening, enhanced due diligence, source-of-funds proof |
| Unclear purpose or flagged jurisdictions | Secrecy is the goal | Country risk scoring, require supporting documents |
| Alerts piling up unreviewed | The HSBC lesson: detection without action | Staffing, review deadlines, independent testing |
""")
    st.markdown("### A program that stops it")
    st.markdown("""
1. **Know your customer** and the real owner behind every company, at onboarding and again when behavior changes.
2. **Risk-rate** customers, products and countries, and scrutinize the high-risk ones more.
3. **Monitor every transaction** with rules plus machine learning, and keep the thresholds low enough to flag *any inclination*.
4. **Triage fast.** Every flag gets a score and an action: monitor, enhanced due diligence, or a suspicious activity report. Never tip off the customer.
5. **Block with authorization.** Freezing needs two named approvers, as on the Alerts page.
6. **Screen** against sanctions and politically exposed person lists, and vet correspondent banks.
7. **Train staff, protect whistleblowers, and test independently.** Several cases above had warnings that were ignored.
8. **Share typologies** between institutions where the law allows, because no single bank sees the whole chain.
""")

with t3:
    st.markdown("A synthetic ledger with 8 planted laundering accounts hidden among ordinary traffic. The scanner applies the rules from the previous tab.")
    df, f, s = scanned(7)
    k = st.columns(4)
    kpi(k[0], "Transactions scanned", f"{len(df):,}"); kpi(k[1], "Accounts flagged", f"{len(s)}", "of 8 planted", good=True)
    kpi(k[2], "Need a report", f"{(s.score >= 70).sum()}", "score 70 or more", good=False); kpi(k[3], "Cash limit used", f"{CTR:,}")
    st.dataframe(s.rename(columns={"account": "Account", "rules": "Rules fired", "score": "Risk score", "action": "Recommended action"}), height=300)
    acc = st.selectbox("Inspect an account", s.account)
    why = f[f.account == acc][["rule", "detail"]]; st.dataframe(why, hide_index=True)
    st.dataframe(df[(df.src == acc) | (df.dst == acc)].drop(columns="txn_id").tail(12), hide_index=True)
    st.caption("Rules are deliberately simple and the jurisdictions are placeholders. Real systems add machine learning, customer history and human investigators.")

with t4:
    st.markdown("""
Every case on the map has the same shape: **the chain crosses several banks and borders, but each bank sees only its own hop.**
Danske saw the Estonian branch, a correspondent bank saw the dollar leg, and nobody saw the whole route.

AegisNet's idea carries over directly. Banks cannot pool customer data, but they can train a shared model on **noised local data**
and merge **masked updates**, so the group learns patterns of layering that no single bank can see.

What exists today and what does not:
- **Built:** federated fraud detection with differential privacy and simulated secure aggregation (card fraud).
- **This page:** rule-based laundering scanner and historic case maps. It does not use the federated model yet.
- **Next step:** add graph features (fan-in, fan-out, cycles, hop counts) to each bank's local features, train the same federated model on laundering labels, and share only masked updates.
""")
