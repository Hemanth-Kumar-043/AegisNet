"""Federated averaging (FedAvg) with logistic regression + secure aggregation + local DP."""
import numpy as np
from sklearn.metrics import roc_auc_score, recall_score, precision_score, f1_score
from .data_gen import FEATURES
from .privacy import to_unit, privatize
from .secure_agg import mask_updates

sig = lambda z: 1 / (1 + np.exp(-np.clip(z, -30, 30)))

def local_train(X, y, w, b, epochs=25, lr=0.8, l2=1e-3):
    sw = np.where(y == 1, .5 / max(y.mean(), 1e-3), .5 / (1 - y.mean()))
    for _ in range(epochs):
        g = (sig(X @ w + b) - y) * sw
        w = w - lr * (X.T @ g / len(y) + l2 * w); b = b - lr * g.mean()
    return w, b

def evaluate(X, y, w, b):
    p = sig(X @ w + b); pred = (p > .5).astype(int)
    return dict(auc=roc_auc_score(y, p), recall=recall_score(y, pred),
                precision=precision_score(y, pred, zero_division=0), f1=f1_score(y, pred))

def prepare(banks, epsilon, seed=0):
    return {k: (privatize(to_unit(d), epsilon, seed + i), d.is_fraud.to_numpy()) for i, (k, d) in enumerate(banks.items())}

def run_federation(banks, test, epsilon=5.0, rounds=10, seed=0):
    data = prepare(banks, epsilon, seed)
    Xt, yt = to_unit(test), test.is_fraud.to_numpy()
    d = len(FEATURES); w, b = np.zeros(d), 0.0
    N = sum(len(y) for _, y in data.values())
    hist, sample = [], None
    for r in range(1, rounds + 1):
        ups = []
        for X, y in data.values():
            lw, lb = local_train(X, y, w.copy(), b)
            ups.append(np.append(lw, lb) * len(y) / N)
        masked = mask_updates(ups, seed + r)
        agg = np.sum(masked, axis=0)
        w, b = agg[:-1], agg[-1]
        if r == 1: sample = dict(true=ups, masked=masked, agg=agg, exact=np.sum(ups, axis=0))
        hist.append(dict(round=r, **evaluate(Xt, yt, w, b)))
    local = {}
    for k, (X, y) in data.items():
        lw, lb = local_train(X, y, np.zeros(d), 0.0, epochs=25 * rounds)
        local[k] = evaluate(Xt, yt, lw, lb)
    Xc = np.vstack([to_unit(dd) for dd in banks.values()]); yc = np.concatenate([dd.is_fraud for dd in banks.values()])
    cw, cb = local_train(Xc, yc, np.zeros(d), 0.0, epochs=25 * rounds)
    return dict(history=hist, local=local, central=evaluate(Xt, yt, cw, cb), sample=sample, weights=w, bias=b)

def epsilon_sweep(banks, test, eps_list=(0.5, 1, 2, 5, 10, 20, np.inf)):
    return [dict(epsilon=e, **run_federation(banks, test, e, rounds=8)["history"][-1]) for e in eps_list]
