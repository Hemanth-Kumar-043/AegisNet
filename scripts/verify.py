"""Prints the project's key claims as plain numbers. No UI needed."""
import sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
from core.data_gen import load_all
from core.federated import run_federation
banks, test = load_all()
print("\nSTEP 1 - Each bank's private data (never combined):")
for k, d in banks.items():
    t = d[d.is_fraud == 1].fraud_type.value_counts(); print(f"  {k}: {len(d)} rows, {d.is_fraud.mean():.1%} fraud, mostly '{t.index[0]}'")
r = run_federation(banks, test, epsilon=5, rounds=10)
print("\nSTEP 2 - Fraud detection score (AUC, 0.5 = guessing, 1.0 = perfect), tested on unseen data:")
for k, v in r["local"].items(): print(f"  {k} trained alone     : {v['auc']:.3f}")
print(f"  ALL banks, federated    : {r['history'][-1]['auc']:.3f}   <- our system, raw data never shared")
print(f"  Pooled data, no privacy : {r['central']['auc']:.3f}   <- unsafe upper limit")
s = r["sample"]
print("\nSTEP 3 - What the server receives from Bank A (first 3 numbers):")
print("  real update  :", np.round(s["true"][0][:3], 3)); print("  masked update:", np.round(s["masked"][0][:3], 3), "<- looks like noise")
print("  masks cancel, merged model exact:", np.allclose(s["agg"], s["exact"]))
