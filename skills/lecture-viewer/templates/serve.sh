#!/bin/bash
# Launch local server for the Lecture Viewer.
# Required because file:// blocks iframe cross-origin access.
# Usage: cd to the lecture directory, then run ./viewer/serve.sh

DIR="$(cd "$(dirname "$0")/.." && pwd)"
PORT=8080

command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 not found. Install Python 3 first."; exit 1; }

echo "Serving lecture at http://localhost:$PORT/viewer/index.html"
echo "Press Ctrl+C to stop."
cd "$DIR" && python3 -m http.server $PORT
