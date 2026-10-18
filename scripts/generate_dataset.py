import sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core.data_gen import generate_all
banks, test = generate_all()
print({k: (len(v), round(v.is_fraud.mean(), 3)) for k, v in banks.items()}, "test:", len(test))
