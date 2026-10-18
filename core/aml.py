"""Rule-based AML red-flag scanner on a synthetic ledger. Illustrates the typologies; not a production system."""
import numpy as np, pandas as pd

FLAGGED = {"Offshore A", "Offshore B"}      # illustrative placeholders, not an official jurisdiction list
CTR = 10_000                                 # cash reporting threshold used in the demo
FLAG_MIN = 10_000                            # wire size that matters when a flagged jurisdiction is involved
PTS = {"Structuring": 70, "Rapid pass-through": 40, "Fan-in / fan-out": 40, "Circular flow": 45, "Flagged jurisdiction": 20}
pseudo = lambda a: a.startswith(("CASH", "EXT"))

def make_ledger(seed=7):
    r = np.random.default_rng(seed); t0 = pd.Timestamp("2026-09-01"); rows = []
    add = lambda ts, s, d, a, ch="wire", c="US": rows.append((ts, s, d, round(float(a), 2), ch, c))
    accts = [f"ACC{i:03d}" for i in range(1, 61)]
    when = lambda: t0 + pd.Timedelta(minutes=int(r.integers(0, 60 * 24 * 20)))
    for _ in range(500):
        s, d = r.choice(accts, 2, replace=False); add(when(), s, d, r.lognormal(6, .9), r.choice(["wire", "card"]), r.choice(["US", "UK", "DE", "IN", "SG"]))
    for _ in range(60): add(when(), "CASH", r.choice(accts), r.uniform(200, 6000), "cash")
    for k in range(7): add(t0 + pd.Timedelta(days=3, hours=k * 20), "CASH", "SMURF1", r.uniform(9000, 9900), "cash")
    for k in range(3):
        ts = t0 + pd.Timedelta(days=5 + 2 * k); a = 50000 + 1000 * k
        add(ts, "EXT-1", "PASS1", a, "wire", "UK"); add(ts + pd.Timedelta(hours=1), "PASS1", "EXT-2", a * .98, "wire", "Offshore A")
    for k in range(12): add(t0 + pd.Timedelta(days=12, hours=k * 6), f"MULE{k:02d}", "HUB1", r.uniform(800, 1500), "wire", "US")
    add(t0 + pd.Timedelta(days=15), "HUB1", "SHELL1", 11500, "wire", "Offshore B")
    for k, (a, b, x) in enumerate([("RING1", "RING2", 75000), ("RING2", "RING3", 73500), ("RING3", "RING1", 72000)]):
        add(t0 + pd.Timedelta(days=8 + k), a, b, x, "wire", "US")
    for k in range(2): add(t0 + pd.Timedelta(days=16 + k), "EXT-3", "SHELLX", 60000, "wire", "Offshore A")
    df = pd.DataFrame(rows, columns=["ts", "src", "dst", "amount", "channel", "country"]).sort_values("ts").reset_index(drop=True)
    df.insert(0, "txn_id", [f"TX{i:04d}" for i in range(len(df))]); return df

def scan(df):
    fl = []
    flag = lambda acc, rule, detail: fl.append(dict(account=acc, rule=rule, detail=detail, points=PTS[rule]))
    cash = df[(df.channel == "cash") & df.amount.between(.9 * CTR, CTR - 1)]
    for acc, g in cash.groupby("dst"):
        ts = np.sort(g.ts.to_numpy())
        n = max(((ts >= t) & (ts < t + np.timedelta64(7, "D"))).sum() for t in ts)
        if n >= 3: flag(acc, "Structuring", f"{n} cash deposits just under {CTR:,} within 7 days")
    for acc in sorted({a for a in set(df.src) | set(df.dst) if not pseudo(a)}):
        ins, outs = df[df.dst == acc], df[df.src == acc]
        hits = sum(outs[(outs.ts >= i.ts) & (outs.ts <= i.ts + pd.Timedelta(hours=24))].amount.sum() >= .9 * i.amount for i in ins[ins.amount >= 20000].itertuples())
        if hits >= 2: flag(acc, "Rapid pass-through", f"{hits} large inflows forwarded within 24 hours")
        ins = ins.sort_values("ts")
        for t in ins.ts:
            w = ins[(ins.ts >= t) & (ins.ts < t + pd.Timedelta(days=5))]
            if w.src.nunique() >= 8 and outs.amount.sum() >= .8 * w.amount.sum():
                flag(acc, "Fan-in / fan-out", f"{w.src.nunique()} senders in 5 days, then funds forwarded"); break
    e = df[~df.src.map(pseudo)].groupby(["src", "dst"]).amount.sum(); nb = {}
    for (s, d), a in e.items(): nb.setdefault(s, {})[d] = a
    for a, bs in nb.items():
        for b, x in bs.items():
            for c, y in nb.get(b, {}).items():
                z = nb.get(c, {}).get(a)
                if z and a < b and a < c and min(x, y, z) >= 20000 and max(x, y, z) <= 1.15 * min(x, y, z):
                    for acc in (a, b, c): flag(acc, "Circular flow", f"{a} → {b} → {c} → {a} with near-equal amounts")
    for r in df[df.country.isin(FLAGGED) & (df.amount >= FLAG_MIN)].itertuples():
        for acc in (r.src, r.dst):
            if not pseudo(acc): flag(acc, "Flagged jurisdiction", f"Wire of {r.amount:,.0f} involving a flagged jurisdiction")
    if not fl: return pd.DataFrame(), pd.DataFrame()
    f = pd.DataFrame(fl).drop_duplicates(["account", "rule", "detail"])
    s = f.groupby("account").agg(points=("points", "sum"), rules=("rule", lambda x: ", ".join(sorted(set(x))))).reset_index()
    s["score"] = (s.points + np.where(s.rules.str.contains(","), 15, 0)).clip(upper=100)
    s["action"] = np.select([s.score >= 70, s.score >= 40], ["File suspicious activity report; review freeze", "Enhanced due diligence"], "Monitor")
    return f, s.drop(columns="points").sort_values("score", ascending=False).reset_index(drop=True)
