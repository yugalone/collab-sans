#!/usr/bin/env bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "Installing requirements..."
python3 -m pip install -q -r requirements.txt

echo "Building Collab font family..."
python3 generate_collab.py "$@"
