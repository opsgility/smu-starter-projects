#!/bin/bash
cd /workspace
pip install -r requirements.txt -q 2>&1 | tail -3
echo "Environment ready. Run: python main.py"
