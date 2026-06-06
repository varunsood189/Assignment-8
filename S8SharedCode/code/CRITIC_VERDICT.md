# Part 3 — Critic verdict (pass + fail + recovery)

The **Critic has no tools**. It reads `UPSTREAM_OUTPUT` and `INPUTS` only — no web, no sandbox execution.

**Property verified:** a **numeric claim in coder JSON** matches the computation described in `USER_QUERY` (arithmetic check the model can do in-prompt).

**Path:** `coder` → **explicit `critic`** → `formatter` (Planner must insert critic; see `prompts/planner.md`).

---

## Pass run

```bash
cd S8SharedCode/code

uv run python flow.py "Use Python to compute 23 plus 19. The coder must emit JSON {\"sum\": <integer>}. Use an explicit critic node to verify the sum is arithmetically correct before the formatter answers."
```

**Expect:** `coder` → `critic` (`verdict: pass`) → `formatter` with sum **42**.

**Logged session:** `s8-4fd467a0`

---

## Fail + recovery run

Critic is given a **wrong threshold** (50); coder correctly emits 42; critic fails; recovery replans.

```bash
uv run python flow.py "Use Python to compute 23 plus 19. The coder must emit JSON {\"sum\": <integer>}. Use an explicit critic that fails unless sum equals 50 (the true answer is 42). After critic-fail recovery, formatter must state the correct sum 42."
```

**Why not “emit sum 99”?** The coder usually computes the correct arithmetic anyway, so critic passes and recovery never runs. A wrong **critic threshold** (50) reliably produces `verdict: fail` when coder outputs 42.

**Logged session:** `s8-418393c0` (older 99-query run); re-run with query above for fresh evidence.

**Expect:**

1. First `critic` → `verdict: fail` (42 ≠ 50)
2. Log: `↪ critic-fail recovery: planner node n:…`
3. Recovery path → user-facing answer with **42**

---

## Inspect

```bash
uv run python replay.py <session_id>
grep -l verdict state/sessions/<sid>/nodes/*.json | head
uv run python visualize_graph.py <sid> --open
```

---

## One-shot

```bash
./scripts/run_assignment.sh 3
```
