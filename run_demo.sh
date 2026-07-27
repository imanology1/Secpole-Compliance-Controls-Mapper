#!/usr/bin/env bash
# Start the Secpol audit simulation: seeded FastAPI backend + Next.js frontend.
# Usage: ./run_demo.sh   (Ctrl-C stops both)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "==> Installing Python deps"
pip install -r requirements.txt >/dev/null

echo "==> Starting API on http://localhost:8000  (seed: Meridian Financial Services)"
uvicorn api.main:app --reload --port 8000 &
API_PID=$!

cleanup() {
  echo; echo "==> Stopping..."
  kill "$API_PID" 2>/dev/null || true
  [ -n "${FE_PID:-}" ] && kill "$FE_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo "==> Installing frontend deps (first run only)"
cd "$ROOT/frontend"
[ -d node_modules ] || npm install

echo "==> Starting frontend on http://localhost:3000"
npm run dev &
FE_PID=$!

echo
echo "======================================================================"
echo " Secpol audit sim is up:"
echo "   API docs:   http://localhost:8000/docs"
echo "   Company:    http://localhost:8000/api/company"
echo "   Dashboard:  http://localhost:3000"
echo " Reset seed at any time:  curl -X POST http://localhost:8000/api/reseed"
echo "======================================================================"
wait
