#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "TESSDATA_PREFIX=/opt/homebrew/share/tessdata" > .env
echo "[✔] Setup completed!"