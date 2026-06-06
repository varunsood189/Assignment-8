#!/usr/bin/env bash
# Session 8 assignment runs (gateway on :8108 required).
#
# Usage:
#   ./scripts/run_assignment.sh [part] [sub]
#
# Parts:
#   1 [hello|A|I|J|K]   base queries (no sub = all five)
#   2                   parallel fan-out
#   3 [pass|fail]       critic (no sub = both)
#   4                   coder + sandbox
#   5                   comparator skill
#   resume <sid>        resume interrupted session (query K)
#   all                 everything + pytest
#
# Examples:
#   ./scripts/run_assignment.sh 1 hello
#   ./scripts/run_assignment.sh 1 A
#   ./scripts/run_assignment.sh 3 pass
#   ./scripts/run_assignment.sh 3 fail
#   ./scripts/run_assignment.sh resume s8-65c8069d
set -euo pipefail
cd "$(dirname "$0")/.."

PART="${1:-all}"
SUB="${2:-}"

usage() {
  cat <<'EOF'
Usage: ./scripts/run_assignment.sh [part] [sub]

  1 [hello|A|I|J|K]   base queries (omit sub to run all)
  2                   parallel fan-out
  3 [pass|fail]       critic verdict (omit sub to run both)
  4                   coder + sandbox
  5                   comparator
  resume SESSION_ID  resume interrupted run after SIGKILL
  all                 all parts + pytest

Examples:
  ./scripts/run_assignment.sh 1 hello
  ./scripts/run_assignment.sh 1 A
  ./scripts/run_assignment.sh 1 I
  ./scripts/run_assignment.sh 1 J
  ./scripts/run_assignment.sh 1 K
  ./scripts/run_assignment.sh 3 pass
  ./scripts/run_assignment.sh 3 fail
  ./scripts/run_assignment.sh resume s8-65c8069d
EOF
}

run_1_hello() {
  echo "=== Part 1 / hello ==="
  uv run python flow.py "Say hello."
}

run_1_A() {
  echo "=== Part 1 / A (Shannon) ==="
  uv run python flow.py "Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, death date, and three key contributions to information theory."
}

run_1_I() {
  echo "=== Part 1 / I (London/Paris/Berlin + coder) ==="
  uv run python flow.py "Find the populations of London, Paris, Berlin and tell me which two are closest in size."
}

run_1_J() {
  echo "=== Part 1 / J (graceful fail) ==="
  uv run python flow.py "Read /nonexistent/path.txt and tell me what's in it."
}

run_1_K() {
  echo "=== Part 1 / K (start — SIGKILL this run, then: ./scripts/run_assignment.sh resume SESSION_ID) ==="
  uv run python flow.py "For Lagos, Cairo, and Kinshasa, find current populations and growth rates and tell me which is growing fastest."
}

run_resume() {
  local sid="${1:?usage: ./scripts/run_assignment.sh resume s8-SESSION_ID}"
  echo "=== Resume session $sid ==="
  uv run python flow.py --resume "$sid"
}

run_part_1() {
  local which="${1:-all}"
  echo "════════════════════════════════════════════════════════════════"
  echo "Part 1 — Base queries"
  echo "════════════════════════════════════════════════════════════════"
  case "$(echo "$which" | tr '[:lower:]' '[:upper:]')" in
    HELLO) run_1_hello ;;
    A)     run_1_A ;;
    I)     run_1_I ;;
    J)     run_1_J ;;
    K)     run_1_K ;;
    ALL)
      run_1_hello
      run_1_A
      run_1_I
      run_1_J
      run_1_K
      ;;
    *)
      echo "Unknown Part 1 query: $which"
      echo "Valid: hello, A, I, J, K"
      exit 1
      ;;
  esac
}

run_part_2() {
  local part2_query
  part2_query='Run three parallel research branches: (1) From https://en.wikipedia.org/wiki/CRISPR — one sentence on what CRISPR is. (2) From https://en.wikipedia.org/wiki/MRNA_vaccine — one sentence on how mRNA vaccines work. (3) From https://en.wikipedia.org/wiki/Photovoltaic_effect — one sentence on how solar cells convert light. Then merge the three answers and say which two topics are most related to medicine.'
  echo "════════════════════════════════════════════════════════════════"
  echo "Part 2 — Parallel fan-out (3 independent Wikipedia branches)"
  echo "════════════════════════════════════════════════════════════════"
  uv run python flow.py "$part2_query"
  SID=$(ls -t state/sessions | head -1)
  echo ""
  echo "Part 2 session: $SID"
  uv run python scripts/verify_parallel_timing.py "$SID" || true
  uv run python visualize_graph.py "$SID"
  echo "DAG: state/sessions/$SID/graph_view.html"
}

run_3_pass() {
  echo "=== Part 3 / Critic PASS ==="
  uv run python flow.py "Use Python to compute 23 plus 19. The coder must emit JSON {\"sum\": <integer>}. Use an explicit critic node to verify the sum is arithmetically correct before the formatter answers."
}

run_3_fail() {
  echo "=== Part 3 / Critic FAIL + planner recovery ==="
  uv run python flow.py "Use Python to compute 23 plus 19. The coder must emit JSON {\"sum\": <integer>}. Use an explicit critic that fails unless sum equals 50 (the true answer is 42). After critic-fail recovery, formatter must state the correct sum 42."
}

run_part_3() {
  local which="${1:-all}"
  echo "════════════════════════════════════════════════════════════════"
  echo "Part 3 — Critic pass + fail + recovery"
  echo "See CRITIC_VERDICT.md"
  echo "════════════════════════════════════════════════════════════════"
  case "$(echo "$which" | tr '[:upper:]' '[:lower:]')" in
    pass) run_3_pass ;;
    fail) run_3_fail ;;
    all)
      run_3_pass
      run_3_fail
      ;;
    *)
      echo "Unknown Part 3 subcommand: $which"
      echo "Valid: pass, fail"
      exit 1
      ;;
  esac
}

run_part_4() {
  echo "════════════════════════════════════════════════════════════════"
  echo "Part 4 — Coder + SandboxExecutor (query I)"
  echo "════════════════════════════════════════════════════════════════"
  uv run python flow.py "Find the populations of London, Paris, Berlin and tell me which two are closest in size."
}

run_part_5() {
  echo "════════════════════════════════════════════════════════════════"
  echo "Part 5 — New skill: comparator"
  echo "════════════════════════════════════════════════════════════════"
  uv run python flow.py "Find the populations of Madrid, Rome, and Lisbon, compare them, and tell me which two are closest in size."
}

case "$PART" in
  1) run_part_1 "${SUB:-all}" ;;
  2)
    if [[ -n "$SUB" ]]; then
      echo "Part 2 has no subcommands."
      usage
      exit 1
    fi
    run_part_2
    ;;
  3) run_part_3 "${SUB:-all}" ;;
  4)
    if [[ -n "$SUB" ]]; then
      echo "Part 4 has no subcommands."
      usage
      exit 1
    fi
    run_part_4
    ;;
  5)
    if [[ -n "$SUB" ]]; then
      echo "Part 5 has no subcommands."
      usage
      exit 1
    fi
    run_part_5
    ;;
  resume)
    if [[ -z "$SUB" ]]; then
      echo "Missing session id."
      usage
      exit 1
    fi
    run_resume "$SUB"
    ;;
  all)
    if [[ -n "$SUB" ]]; then
      echo "Use: ./scripts/run_assignment.sh all   # no second argument"
      exit 1
    fi
    run_part_1 all
    run_part_2
    run_part_3 all
    run_part_4
    run_part_5
    echo ""
    echo "Regression:"
    uv run pytest tests/test_recovery.py -q
    ;;
  -h|--help|help) usage ;;
  *)
    usage
    exit 1
    ;;
esac
# End of script — do not paste terminal output below this line.
