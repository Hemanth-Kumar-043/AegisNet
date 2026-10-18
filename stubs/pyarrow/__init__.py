# Stand-in for pyarrow on machines where it cannot be installed (s390x). Lets Streamlit start; real Arrow features are unavailable.
import sys as _sys, types as _types
__aegis_stub__ = True
__version__ = "0.0.1"  # deliberately ancient so pandas ignores this stand-in
_cache = {}
class _Base:
    def __init__(self, *a, **k):
        raise RuntimeError("pyarrow is not available on this machine")
def _make(name):
    if name not in _cache:
        _cache[name] = type(name, (_Base,), {})
    return _cache[name]
def __getattr__(name):
    if name.startswith("__"):
        raise AttributeError(name)
    return _make(name)
def _sub(n):
    m = _types.ModuleType("pyarrow." + n)
    m.__path__ = []
    m.__aegis_stub__ = True
    def _ga(name, _n=n):
        if name.startswith("__"):
            raise AttributeError(name)
        return _make(_n + "." + name)
    m.__getattr__ = _ga
    _sys.modules["pyarrow." + n] = m
    globals()[n] = m
for _n in ("lib", "types", "compute", "parquet", "ipc", "feather"):
    _sub(_n)
