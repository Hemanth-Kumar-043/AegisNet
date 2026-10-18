#!/usr/bin/env bash
# Mac/Linux one-command launcher: makes a venv, installs, runs the checks, starts the dashboard.
set -e
cd "$(dirname "$0")/.."
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip && pip install -r requirements.txt
python scripts/verify.py
streamlit run app.py
