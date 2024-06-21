#!/bin/bash
# Get the directory of the current script
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Navigate to the directory containing the script
cd "$SCRIPT_DIR"

# Activate the virtual environment
source .venv/bin/activate

# Run the Python script
python SALTA.py

