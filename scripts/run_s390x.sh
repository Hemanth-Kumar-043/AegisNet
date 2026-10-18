#!/usr/bin/env bash
# One-shot setup + run for the LinuxONE (Ubuntu s390x) VM. Run from the aegisnet folder:  bash scripts/run_s390x.sh
set -e
cd "$(dirname "$0")/.."
echo "== Machine: $(uname -m) =="
echo "== 1/4 System packages (prebuilt, avoids long compiles) =="
sudo apt-get update
sudo apt-get install -y python3-venv python3-dev python3-numpy python3-scipy python3-sklearn \
  python3-pandas python3-matplotlib python3-plotly python3-pil
echo "== 2/4 Virtual environment that reuses them =="
rm -rf .venv
python3 -m venv .venv --system-site-packages
source .venv/bin/activate
# s390x is big-endian: use pure-Python protobuf and single-thread BLAS to avoid segfaults
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export OPENBLAS_NUM_THREADS=1
pip install --upgrade pip wheel
echo "== 3/4 Streamlit (no pyarrow on s390x) =="
pip install --no-deps "streamlit==1.50.0"
pip install watchdog || true
pip install "altair<6" blinker "cachetools<7" click packaging "protobuf<7" requests tenacity toml \
  typing-extensions gitpython pydeck tornado
PYTHONPATH="$PWD/stubs" python -c "import numpy, scipy, sklearn, pandas, plotly, streamlit; print('imports ok, streamlit', streamlit.__version__)"
echo "== 4/4 Proof numbers, then dashboard =="
python scripts/verify.py
echo "Open http://localhost:8501 on your Mac (SSH tunnel window must stay open). Ctrl+C stops it."
PYTHONPATH="$PWD/stubs${PYTHONPATH:+:$PYTHONPATH}" streamlit run app.py --server.address 127.0.0.1 --server.port 8501
