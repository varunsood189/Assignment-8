# Run results (2026-06-06)

Recent end-to-end runs from `./scripts/run_assignment.sh`. Session folders live locally at `S8SharedCode/code/state/sessions/<id>/` (gitignored). Regenerate DAG HTML:

```bash
cd S8SharedCode/code
uv run python visualize_graph.py <session_id> --open
uv run python replay.py <session_id>
```

---

## Summary

| Part | Script | Session | Outcome |
|------|--------|---------|---------|
| **1 hello** | `1 hello` | `s8-2eeced31` | **OK** — `Hello!` |
| **1 A** | `1 A` | `s8-19951deb` | **OK** — Shannon birth/death dates + 3 IT contributions |
| **1 I** | `1 I` | `s8-302aedc3` | **OK** — London 9.8M, Paris 11.3M, Berlin 3.8M; closest: London & Paris (Δ 1.5M). Recovery planner after sandbox fail. |
| **1 J** | `1 J` | `s8-0336aa12` | **OK** — graceful fail on missing file |
| **1 K** | `1 K` | `s8-f38508c4` | **OK** — Lagos 21.0M (3.9%), Cairo 20.5M (2.5%), Kinshasa 15.0M (**4.1%** fastest) |
| **2** | `2` | `s8-d9949021` | **OK** — 3× researcher ∥ + verify **PASS** (wall ≈ max branch) |
| **3 pass** | `3 pass` | `s8-1435de01` | **OK** — critic pass, sum **42** |
| **3 fail** | `3 fail` | `s8-de2d675a` | **OK** — `↪ critic-fail recovery` ×2, final sum **42** (one critic hit 503 transient) |
| **4** | `4` | `s8-9cc4458b` | **Weak** — no population figures in research scrape |
| **5** | `5` | `s8-1f8e3788` | **OK** — Madrid 3.5M, Rome 2.9M, Lisbon 576k; closest: Madrid & Rome (Δ 607k) |

---

## Part 1 — base queries

### hello — `s8-2eeced31`

```
FINAL: Hello!
```

Graph: `planner` → `formatter`

---

### A (Claude Shannon) — `s8-19951deb`

```
FINAL: Claude Shannon was born on April 30, 1916, and passed away on February 24, 2001.
Three key contributions to information theory:
1. Foundational 1948 paper "A Mathematical Theory of Communication"
2. Information entropy
3. Logical operations via relays/switches (digital circuits)
```

Graph: `planner` → `researcher` → `distiller` → `formatter`

---

### I (London / Paris / Berlin) — `s8-302aedc3`

First attempt (`s8-0b6c0ec4`) could not extract populations from a single researcher pass. Second run recovered via planner after `sandbox_executor` failed, then fanned out to **3× researcher** + coder.

```
FINAL:
  London:  9,800,000
  Paris:  11,300,000
  Berlin:  3,800,000
  Closest pair: London & Paris (difference 1,500,000)
```

Notable log line: `↪ recovery (upstream_failure): planner node n:6 queued for n:5`

---

### J (graceful fail) — `s8-0336aa12`

```
FINAL: Cannot read /nonexistent/path.txt — file does not exist (no crash).
```

Graph: `planner` → `formatter`

---

### K (Lagos / Cairo / Kinshasa)

| Session | Note |
|---------|------|
| `s8-31c12207` | Started for interrupt/resume demo; stopped with Ctrl+C during distiller layer |
| `s8-f38508c4` | Completed run (full graph through coder + sandbox) |

```
FINAL:
  Lagos:     21.0 million @ 3.9% growth
  Cairo:     20.5 million @ 2.5% growth
  Kinshasa:  15.0 million @ 4.1% growth  ← fastest
```

Resume after SIGKILL: `./scripts/run_assignment.sh resume s8-31c12207`

---

## Part 2 — parallel fan-out — `s8-d9949021`

Query: CRISPR + mRNA vaccine + photovoltaic (three Wikipedia URLs).

```
FINAL: CRISPR … adaptive immunity / gene editing. mRNA vaccines … protein + immune response.
       Photovoltaic … photons excite electrons in semiconductor. CRISPR and mRNA most related to medicine.
```

**Timing verify (PASS):**

| Wave | Nodes | Wall-clock | Max branch |
|------|-------|------------|------------|
| 1 | 3× researcher | 37.0s | 37.0s |
| 2 | 3× summariser | 10.7s | 10.7s |

---

## Part 3 — critic — `s8-1435de01` / `s8-de2d675a`

**Pass:** coder → critic (pass) → sandbox → formatter → **42**

**Fail + recovery:** critic threshold **50** (wrong on purpose); log shows:

```
↪ critic-fail recovery: planner node n:8 for n:2
↪ critic-fail recovery: planner node n:13 for n:9
```

Final answer still **42**. One recovery-path critic hit `503 Service Unavailable` (transient; skipped re-plan).

---

## Part 4 — coder + sandbox — `s8-9cc4458b`

```
FINAL: Population data for London, Paris, and Berlin was not found in the provided research results.
```

Use **`s8-302aedc3`** (Part 1 I) as the stronger query-I example with coder + sandbox + recovery.

---

## Part 5 — comparator — `s8-1f8e3788`

```
FINAL:
  Madrid:  3,506,730
  Rome:    2,900,000
  Lisbon:    575,739
  Closest pair: Madrid & Rome (difference 606,730)
```

Graph includes **3× researcher** (parallel) → coder → **comparator** → formatter + sandbox.

---

## Tests

```bash
cd S8SharedCode/code && uv run pytest tests/test_recovery.py
# Expected: 22 passed
```
