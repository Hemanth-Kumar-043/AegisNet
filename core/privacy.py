"""Local differential privacy: features are clipped to public bounds, scaled to [0,1],
then Laplace noise with scale 1/epsilon is added BEFORE data is used for training."""
import numpy as np
from .data_gen import FEATURES

LOG = {"amount", "avg_amount_30d", "geo_distance_km", "account_age_days"}
BOUNDS = {"amount": (0, 10), "account_age_days": (0, 8.6), "txn_hour": (0, 23), "merchant_risk": (0, 1),
          "velocity_24h": (0, 20), "geo_distance_km": (0, 9), "is_international": (0, 1),
          "device_new": (0, 1), "avg_amount_30d": (0, 10), "amount_ratio": (0, 10)}

def to_unit(df):
    X = np.zeros((len(df), len(FEATURES)))
    for j, c in enumerate(FEATURES):
        v = np.log1p(df[c].to_numpy(float)) if c in LOG else df[c].to_numpy(float)
        lo, hi = BOUNDS[c]
        X[:, j] = (np.clip(v, lo, hi) - lo) / (hi - lo)
    return X

def privatize(X, epsilon, seed=0):
    if epsilon is None or np.isinf(epsilon): return X
    return X + np.random.default_rng(seed).laplace(0, 1.0 / epsilon, X.shape)
