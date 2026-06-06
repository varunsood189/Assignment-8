#!/usr/bin/env bash
# Run Session 8 base queries verbatim (gateway must be up on :8108).
set -euo pipefail
cd "$(dirname "$0")/.."

echo "=== hello ==="
uv run python flow.py "Say hello."

echo "=== A (Shannon) ==="
uv run python flow.py "Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, death date, and three key contributions to information theory."

echo "=== I (London/Paris/Berlin) ==="
uv run python flow.py "Find the populations of London, Paris, Berlin and tell me which two are closest in size."

echo "=== J (graceful fail) ==="
uv run python flow.py "Read /nonexistent/path.txt and tell me what's in it."

echo "=== K (start only — kill with SIGKILL, then: uv run python flow.py --resume <sid>) ==="
uv run python flow.py "For Lagos, Cairo, and Kinshasa, find current populations and growth rates and tell me which is growing fastest."
