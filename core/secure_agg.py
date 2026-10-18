"""Pairwise-mask secure aggregation: each bank adds random masks that cancel in the sum,
so the aggregator only ever sees masked vectors but recovers the exact total."""
import numpy as np

def mask_updates(updates, seed=0):
    r = np.random.default_rng(seed)
    masked = [u.astype(float).copy() for u in updates]
    for i in range(len(updates)):
        for j in range(i + 1, len(updates)):
            m = r.normal(0, 5, updates[i].shape)
            masked[i] += m; masked[j] -= m
    return masked
