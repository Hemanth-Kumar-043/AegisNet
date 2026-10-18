"""Synthetic multi-bank transaction generator (no real PII). Each bank has a different
fraud rate and spending profile -> non-IID data, like real institutions."""
import numpy as np, pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FEATURES = ["amount", "account_age_days", "txn_hour", "merchant_risk", "velocity_24h",
            "geo_distance_km", "is_international", "device_new", "avg_amount_30d", "amount_ratio"]
PROFILES = {   # mix = share of [account-takeover, cross-border, card-testing] fraud each bank mostly sees
    "Bank A": dict(n=4000, fraud=0.08, amt=60, seed=1, mix=(.8, .1, .1)),   # retail
    "Bank B": dict(n=4000, fraud=0.10, amt=90, seed=2, mix=(.1, .8, .1)),   # cards
    "Bank C": dict(n=4000, fraud=0.12, amt=45, seed=3, mix=(.1, .1, .8)),   # digital-first
}

def make_bank(name, n, fraud, amt, seed, mix=(1/3, 1/3, 1/3)):
    r = np.random.default_rng(seed)
    y = (r.random(n) < fraud).astype(int)
    t = np.where(y == 1, r.choice(3, n, p=mix), -1)            # fraud type, -1 = legit
    f0, f1, f2 = t == 0, t == 1, t == 2                         # which features each fraud type distorts
    amount = np.where(f0, r.lognormal(np.log(amt * 5), .9, n), r.lognormal(np.log(amt), .8, n))
    avg = r.lognormal(np.log(amt), .5, n)
    df = pd.DataFrame({
        "txn_id": [f"{name[-1]}{i:06d}" for i in range(n)],
        "bank": name,
        "amount": amount.round(2),
        "account_age_days": np.where(f0, r.exponential(90, n), r.exponential(900, n)).clip(1, 5000).round(),
        "txn_hour": np.where(f2, r.choice([0, 1, 2, 3, 4, 22, 23], n), r.integers(6, 23, n)),
        "merchant_risk": np.where(f1, r.beta(5, 2, n), r.beta(2, 5, n)).round(3),
        "velocity_24h": np.where(f2, r.poisson(7, n), r.poisson(1.5, n)),
        "geo_distance_km": np.where(f1, r.exponential(1200, n), r.exponential(60, n)).round(1),
        "is_international": np.where(f1, r.random(n) < .75, r.random(n) < .05).astype(int),
        "device_new": np.where(f0, r.random(n) < .80, r.random(n) < .08).astype(int),
        "avg_amount_30d": avg.round(2),
    })
    df["amount_ratio"] = (df.amount / df.avg_amount_30d).round(3)
    flip = r.random(n) < .02
    df["is_fraud"] = np.where(flip, 1 - y, y)
    df["fraud_type"] = np.where(t < 0, "none", np.array(["account_takeover", "cross_border", "card_testing"])[np.clip(t, 0, 2)])
    return df

def generate_all(save=True):
    banks = {k: make_bank(k, **v) for k, v in PROFILES.items()}
    test = make_bank("Test", 4000, .10, 65, 99)
    if save:
        DATA_DIR.mkdir(exist_ok=True)
        for k, d in banks.items(): d.to_csv(DATA_DIR / f"{k.lower().replace(' ', '_')}.csv", index=False)
        test.to_csv(DATA_DIR / "global_holdout_test.csv", index=False)
    return banks, test

def load_all():
    files = {k: DATA_DIR / f"{k.lower().replace(' ', '_')}.csv" for k in PROFILES}
    if all(p.exists() for p in files.values()) and (DATA_DIR / "global_holdout_test.csv").exists():
        return {k: pd.read_csv(p) for k, p in files.items()}, pd.read_csv(DATA_DIR / "global_holdout_test.csv")
    return generate_all()
