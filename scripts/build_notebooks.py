import json
from pathlib import Path
def _cell(t, s): 
    c = {"cell_type": t, "metadata": {}, "source": s.strip().splitlines(True)}
    if t == "code": c.update(outputs=[], execution_count=None)
    return c
class nbf:
    class v4:
        new_markdown_cell = staticmethod(lambda s: _cell("markdown", s))
        new_code_cell = staticmethod(lambda s: _cell("code", s))
M = lambda s: nbf.v4.new_markdown_cell(s.strip()); C = lambda s: nbf.v4.new_code_cell(s.strip())
HEAD = C("""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path.cwd().parent))   # make core/ importable from notebooks/
import numpy as np, pandas as pd, matplotlib.pyplot as plt
plt.rcParams.update({"figure.facecolor": "#0A1830", "axes.facecolor": "#12264A", "axes.edgecolor": "#2A4170",
    "text.color": "#E8EFFA", "axes.labelcolor": "#E8EFFA", "xtick.color": "#8FA3C4", "ytick.color": "#8FA3C4",
    "axes.prop_cycle": plt.cycler(color=["#34D3C0", "#6EA8FF", "#FFB547", "#B58CFF"]), "axes.grid": True, "grid.color": "#2A4170"})
from core.data_gen import load_all, FEATURES
banks, test = load_all()
""")
nbs = {}
nbs["01_data_and_privacy"] = [
 M("# 1. Data and local differential privacy\nEach bank keeps its own table. Noise is added on the bank's side before any training."),
 HEAD,
 C("pd.concat(banks.values()).groupby(['bank','fraud_type']).size().unstack().fillna(0).astype(int)"),
 M("Each bank mostly sees one fraud pattern. This is why collaboration helps."),
 C("""
from core.privacy import to_unit, privatize
raw = to_unit(banks['Bank A'])
fig, ax = plt.subplots(1, 3, figsize=(13, 3.2))
for a, e in zip(ax, [None, 5, 0.5]):
    a.hist(privatize(raw, e, 1)[:, FEATURES.index('merchant_risk')], bins=40)
    a.set_title('no noise' if e is None else f'epsilon = {e}')
fig.suptitle('merchant_risk as seen by the model'); plt.show()
"""),
]
nbs["02_federated_training"] = [
 M("# 2. Federated training\nFederated averaging across three banks, compared with each bank alone and with an unsafe centralised model."),
 HEAD,
 C("""
from core.federated import run_federation
EPS, ROUNDS = 5, 10
res = run_federation(banks, test, epsilon=EPS, rounds=ROUNDS)
h = pd.DataFrame(res['history']); h.tail(3)
"""),
 C("""
plt.figure(figsize=(9, 4.2)); plt.plot(h['round'], h['auc'], lw=3, label='Federated')
for k, v in res['local'].items(): plt.axhline(v['auc'], ls=':', label=f'{k} alone')
plt.axhline(res['central']['auc'], ls='--', color='#FFB547', label='Centralised (no privacy)')
plt.xlabel('round'); plt.ylabel('test AUC'); plt.legend(); plt.show()
"""),
 M("## Privacy versus accuracy"),
 C("""
from core.federated import epsilon_sweep
s = pd.DataFrame(epsilon_sweep(banks, test)); s['eps'] = s['epsilon'].astype(str)
plt.figure(figsize=(8, 4)); plt.plot(s['eps'], s['auc'], 'o-', label='AUC'); plt.plot(s['eps'], s['recall'], 'o-', label='Recall')
plt.xlabel('epsilon (inf = no noise)'); plt.legend(); plt.show(); s.round(3)
"""),
]
nbs["03_secure_aggregation_and_linuxone_proof"] = [
 M("# 3. Secure aggregation and platform proof\nRun this notebook on the LinuxONE VM and keep the output as evidence."),
 HEAD,
 C("""
from core.federated import run_federation
res = run_federation(banks, test, epsilon=5, rounds=5); s = res['sample']
print('Masks cancel, merged model is exact:', np.allclose(s['agg'], s['exact']))
pd.DataFrame({f'bank{i} true': s['true'][i][:4] for i in range(3)} | {f'bank{i} masked': s['masked'][i][:4] for i in range(3)})
"""),
 M("## What machine is this?"),
 C("""
from core.platform_proof import platform_report, scoring_benchmark
rep = platform_report(); {k: v for k, v in rep.items() if k != 'cpu_features'}
"""),
 M("`secure_execution_guest` is `'1'` only inside a Secure Execution guest. If it is `None`, do not claim Secure Execution."),
 C("""
b = pd.DataFrame(scoring_benchmark(res['weights'], 0.0, len(FEATURES))).round(3); b
"""),
 C("""
plt.figure(figsize=(7, 3.8)); plt.bar(b['batch'].astype(str), b['txns_per_sec'])
plt.yscale('log'); plt.xlabel('batch size'); plt.ylabel('transactions / second'); plt.show()
"""),
]
for name, cells in nbs.items():
    nb = {"cells": cells, "nbformat": 4, "nbformat_minor": 5, "metadata": {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"}}}
    (Path(__file__).resolve().parent.parent / "notebooks" / f"{name}.ipynb").write_text(json.dumps(nb, indent=1))
print("built", list(nbs))
