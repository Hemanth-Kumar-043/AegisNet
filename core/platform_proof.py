"""Reads real facts from the machine it runs on, so claims in the demo are evidence-backed."""
import platform, os, time, numpy as np
from pathlib import Path

def _read(p):
    try: return Path(p).read_text().strip()
    except Exception: return None

def platform_report():
    cpu = _read("/proc/cpuinfo") or ""
    feats = next((l.split(":", 1)[1].split() for l in cpu.splitlines() if l.startswith("features")), [])
    return {
        "machine": platform.machine(),
        "is_s390x": platform.machine() == "s390x",
        "os": platform.platform(),
        "cpus": os.cpu_count(),
        "secure_execution_guest": _read("/sys/firmware/uv/prot_virt_guest"),   # "1" inside a Secure Execution guest
        "vector_facility": "vx" in feats,
        "crypto_msa": [f for f in feats if f.startswith("msa")],
        "cpu_features": feats,
    }

def scoring_benchmark(w, b, n_features, batch_sizes=(1, 100, 10_000, 1_000_000), reps=20):
    """Latency/throughput of scoring transactions with the trained federated model."""
    rows = []
    for n in batch_sizes:
        X = np.random.default_rng(0).random((n, n_features)); t = []
        for _ in range(reps):
            s = time.perf_counter(); 1 / (1 + np.exp(-(X @ w + b))); t.append(time.perf_counter() - s)
        t = np.array(t)
        rows.append(dict(batch=n, p50_ms=np.percentile(t, 50) * 1e3, p99_ms=np.percentile(t, 99) * 1e3,
                         txns_per_sec=n / np.median(t)))
    return rows
