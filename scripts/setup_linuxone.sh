#!/usr/bin/env bash
# Run ON the LinuxONE VM. Installs the ML stack and starts JupyterLab bound to localhost only.
set -e
sudo apt-get update && sudo apt-get install -y python3-venv python3-dev build-essential gfortran libopenblas-dev || true
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt jupyterlab ipykernel matplotlib
python -m ipykernel install --user --name aegisnet --display-name "AegisNet (s390x)"
jupyter lab --no-browser --ip=127.0.0.1 --port=8888
# From your laptop:  ssh -L 8888:localhost:8888 <user>@<linuxone-host>   then open http://localhost:8888
