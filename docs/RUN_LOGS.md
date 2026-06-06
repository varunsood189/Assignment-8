# Run logs (2026-06-06)

Terminal output from `./scripts/run_assignment.sh` (gateway on `:8108`). MCP/Crawl4AI noise omitted; **session id**, **node timings**, **recovery lines**, and **FINAL** kept verbatim where useful.

Inspect locally: `cd S8SharedCode/code && uv run python replay.py <session_id>`

---

## Summary

| Part | Session | Result |
|------|---------|--------|
| 1 hello | `s8-2eeced31` | OK |
| 1 A | `s8-19951deb` | OK |
| 1 I (retry) | `s8-302aedc3` | OK + recovery |
| 1 J | `s8-0336aa12` | OK |
| 1 K (interrupt) | `s8-31c12207` | Ctrl+C mid-run |
| 1 K (complete) | `s8-f38508c4` | OK |
| 2 | `s8-d9949021` | OK + timing PASS |
| 3 pass | `s8-1435de01` | OK |
| 3 fail | `s8-de2d675a` | OK + critic recovery |
| 4 | `s8-9cc4458b` | Weak |
| 5 | `s8-1f8e3788` | OK |

---

## Part 1 — hello — `s8-2eeced31`

```text
./scripts/run_assignment.sh 1 hello

session s8-2eeced31  ─  query: Say hello.
[n:1] planner            complete (3.6s)
[n:2] formatter          complete (2.1s)

FINAL: Hello!
```

---

## Part 1 — A (Claude Shannon) — `s8-19951deb`

```text
./scripts/run_assignment.sh 1 A

session s8-19951deb  ─  query: Fetch https://en.wikipedia.org/wiki/Claude_Shannon ...
[FETCH] https://en.wikipedia.org/wiki/Claude_Shannon  ✓
[n:1] planner            complete (3.6s)
[n:2] researcher         complete (19.9s)
[n:3] distiller          complete (3.1s)
[n:4] formatter          complete (4.2s)

FINAL: Claude Shannon was born on April 30, 1916, and passed away on February 24, 2001.
His three key contributions to information theory are:
1. Foundational 1948 paper "A Mathematical Theory of Communication"
2. Information entropy
3. Logical operations via relays/switches (digital circuits)
```

---

## Part 1 — I (London / Paris / Berlin) — `s8-302aedc3`

First attempt `s8-0b6c0ec4` failed to extract populations (single researcher). Second run recovered:

```text
./scripts/run_assignment.sh 1 I

session s8-302aedc3  ─  query: Find the populations of London, Paris, Berlin ...
[n:1] planner            complete (3.2s)
[n:2] researcher         complete (13.3s)
[n:3] coder              complete (3.5s)
[n:4] formatter          complete (3.7s)
[n:5] sandbox_executor   failed   (0.1s)
  ↪ recovery (upstream_failure): planner node n:6 queued for n:5
[n:6] planner            complete (4.5s)
[n:7] researcher         complete (72.0s)
[n:8] researcher         complete (24.1s)
[n:9] researcher         complete (27.6s)
[n:10] coder              complete (3.2s)
[n:11] formatter          complete (3.4s)
[n:12] sandbox_executor   complete (0.1s)

FINAL: The populations of the cities are:
*   London:  9,800,000
*   Paris:  11,300,000
*   Berlin:  3,800,000
The two cities closest in population size are London and Paris, with a difference of 1,500,000.
```

---

## Part 1 — J (graceful fail) — `s8-0336aa12`

```text
./scripts/run_assignment.sh 1 J

session s8-0336aa12  ─  query: Read /nonexistent/path.txt and tell me what's in it.
[n:1] planner            complete (3.8s)
[n:2] formatter          complete (3.8s)

FINAL: I am sorry, but I cannot read the file /nonexistent/path.txt because it does not exist.
```

---

## Part 1 — K (Lagos / Cairo / Kinshasa)

**Interrupted run** — `s8-31c12207` (Ctrl+C during distiller layer after 3× researcher):

```text
./scripts/run_assignment.sh 1 K

session s8-31c12207  ─  query: For Lagos, Cairo, and Kinshasa, find current populations ...
[n:2] researcher         complete (32.3s)
[n:3] researcher         complete (20.2s)
[n:4] researcher         complete (62.6s)
[n:12] distiller          complete (11.2s)
[n:13] distiller          complete (3.5s)
[n:14] distiller          complete (7.3s)
^C KeyboardInterrupt

# Resume:
./scripts/run_assignment.sh resume s8-31c12207
```

**Completed run** — `s8-f38508c4`:

```text
session s8-f38508c4  ─  query: For Lagos, Cairo, and Kinshasa, find current populations ...
[n:2] researcher         complete (76.5s)
[n:3] researcher         complete (31.9s)
[n:4] researcher         complete (44.4s)
[n:5] distiller          complete (9.3s)
[n:6] distiller          complete (1.2s)
[n:7] distiller          complete (5.0s)
[n:8] coder              complete (5.0s)
[n:9] formatter          complete (3.3s)
[n:10] sandbox_executor   complete (0.1s)

FINAL:
*   Lagos:     Population = 21.0 million, Growth Rate = 3.9%
*   Cairo:     Population = 20.5 million, Growth Rate = 2.5%
*   Kinshasa:  Population = 15.0 million, Growth Rate = 4.1%
The fastest growing city is Kinshasa with a growth rate of 4.1%.
```

---

## Part 2 — parallel fan-out — `s8-d9949021`

```text
./scripts/run_assignment.sh 2

session s8-d9949021  ─  query: Run three parallel research branches: CRISPR / mRNA / photovoltaic ...
[n:1] planner            complete (4.4s)
[n:2] researcher         complete (29.4s)
[n:3] researcher         complete (37.0s)
[n:4] researcher         complete (20.0s)
[n:5] summariser         complete (6.8s)
[n:6] summariser         complete (2.8s)
[n:7] summariser         complete (10.7s)
[n:8] comparator         complete (181.7s)
[n:9] formatter          complete (3.9s)

FINAL: CRISPR is a system found in prokaryotes ... mRNA vaccines work by instructing cells ...
       Solar cells convert light into electricity ... CRISPR and mRNA vaccines are most related to medicine.

Wave 1: n:2, n:3, n:4
  Layer wall-clock: 37.0s   Max branch: 37.0s   Sum: 86.4s   → wall ≈ max? True
Wave 2: n:5, n:6, n:7
  Layer wall-clock: 10.7s   Max branch: 10.7s   Sum: 20.3s   → wall ≈ max? True

PASS: At least one parallel layer's wall-clock matches max(branch), not sum.
DAG: state/sessions/s8-d9949021/graph_view.html
```

---

## Part 3 — critic pass — `s8-1435de01`

```text
./scripts/run_assignment.sh 3 pass

session s8-1435de01  ─  query: Use Python to compute 23 plus 19 ... explicit critic ...
[n:1] planner            complete (3.9s)
[n:2] coder              complete (4.0s)
[n:3] critic             complete (0.9s)
[n:5] sandbox_executor   complete (0.0s)
[n:4] formatter          complete (2.5s)

FINAL: The sum of 23 and 19 is 42.
```

---

## Part 3 — critic fail + recovery — `s8-de2d675a`

```text
./scripts/run_assignment.sh 3 fail

session s8-de2d675a  ─  query: ... critic that fails unless sum equals 50 (true answer is 42) ...
[n:1] planner            complete (3.9s)
[n:2] coder              complete (7.7s)
[n:3] critic             complete (1.1s)
  ↪ critic-fail recovery: planner node n:8 for n:2
[n:8] planner            complete (4.7s)
[n:9] coder              complete (4.3s)
[n:10] critic             complete (0.9s)
  ↪ critic-fail recovery: planner node n:13 for n:9
[n:13] planner            complete (3.1s)
[n:14] coder              complete (4.7s)
[n:15] critic             failed   (0.0s)  err=503 Service Unavailable
  ↪ n:15 failed (transient, skill=critic): transient gateway error; gateway retry exhausted, not re-planning
[n:17] sandbox_executor   complete (0.0s)

FINAL: The sum of 23 plus 19 is 42.
```

---

## Part 4 — coder + sandbox — `s8-9cc4458b`

```text
./scripts/run_assignment.sh 4

session s8-9cc4458b  ─  query: Find the populations of London, Paris, Berlin ...
[n:1] planner            complete (4.0s)
[n:2] researcher         complete (19.9s)
[n:3] coder              complete (5.1s)
[n:4] formatter          complete (2.0s)
[n:5] sandbox_executor   complete (0.1s)

FINAL: Population data for London, Paris, and Berlin was not found in the provided research results.
```

Use **`s8-302aedc3`** (Part 1 I) as the stronger coder + sandbox example.

---

## Part 5 — comparator — `s8-1f8e3788`

```text
./scripts/run_assignment.sh 5

session s8-1f8e3788  ─  query: Find the populations of Madrid, Rome, and Lisbon, compare them ...
[n:1] planner            complete (4.7s)
[n:2] researcher         complete (33.9s)
[n:3] researcher         complete (62.3s)
[n:4] researcher         complete (51.3s)
[n:5] coder              complete (5.2s)
[n:6] comparator         complete (1.6s)
[n:7] formatter          complete (3.8s)
[n:8] sandbox_executor   complete (0.0s)

FINAL:
*   Madrid:  3,506,730
*   Rome:    2,900,000
*   Lisbon:    575,739
Madrid and Rome are the closest in population size, with a difference of 606,730.
```

---

## Tests

```bash
cd S8SharedCode/code && uv run pytest tests/test_recovery.py -q
# 22 passed
```
