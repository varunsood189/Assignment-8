# Session 8 — Submission Package

**Course:** EAG V3 — Session 8 (Multi-Agent DAG Orchestration)  
**Repo:** [Assignment 8 README](./README.md) (architecture + evidence log)  
**Code:** `S8SharedCode/`

## Links (fill before submitting)

| Item | Value |
|------|--------|
| **GitHub / repo README** | _paste course submission URL to this repo_ |
| **YouTube demo** | _paste unlisted/public video URL here_ |
| **Student name** | _your name_ |

## Deliverables checklist

| # | Requirement | Status | Primary evidence |
|---|-------------|--------|------------------|
| 1 | Five base queries (hello, A, I, J, K) | Done | See [Evidence log](./README.md#assignment-evidence-log) |
| 2 | Custom parallel fan-out (≥3 concurrent researchers) | Run `./scripts/run_assignment.sh 2` | _session after run_ |
| 3 | Critic pass + fail + planner recovery | `./scripts/run_assignment.sh 3` | Pass `s8-4fd467a0`, fail `s8-418393c0` — [CRITIC_VERDICT.md](S8SharedCode/code/CRITIC_VERDICT.md) |
| 4 | Coder prompt + sandbox chain | Done | `prompts/coder.md`, `s8-30cc4b2c` |
| 5 | One new skill (no `flow.py` change) | Done | `comparator` — `s8-1dc4d047` |
| 6 | Recovery tests | Done | `22 passed` — `tests/test_recovery.py` |
| 7 | YouTube walkthrough | **Pending** | Use [demo script](#demo-recording-script) below |

## Session ID quick reference

### Base queries (verbatim)

```bash
cd S8SharedCode/code

uv run python flow.py "Say hello."
# → s8-7f8a75bf (logged)

uv run python flow.py "Fetch https://en.wikipedia.org/wiki/Claude_Shannon and tell me his birth date, death date, and three key contributions to information theory."

uv run python flow.py "Find the populations of London, Paris, Berlin and tell me which two are closest in size."

uv run python flow.py "Read /nonexistent/path.txt and tell me what's in it."

# K: start, SIGKILL mid-run, then:
uv run python flow.py --resume <sid>
```

Logged sessions: hello `s8-7f8a75bf`, A `s8-dc7d6377`, I `s8-30cc4b2c`, J `s8-ea8e55ff`, K interrupt `s8-65c8069d`.

### Part 2 — Parallel fan-out (3 Wikipedia branches)

```bash
cd S8SharedCode/code
./scripts/run_assignment.sh 2
```

Or verbatim:

```bash
uv run python flow.py "Run three parallel research branches: (1) From https://en.wikipedia.org/wiki/CRISPR — one sentence on what CRISPR is. (2) From https://en.wikipedia.org/wiki/MRNA_vaccine — one sentence on how mRNA vaccines work. (3) From https://en.wikipedia.org/wiki/Photovoltaic_effect — one sentence on how solar cells convert light. Then merge the three answers and say which two topics are most related to medicine."
```

Session: _paste `s8-*` after run_.  
Verify: `uv run python scripts/verify_parallel_timing.py <sid>`

Alternate (4 cities, already logged): `s8-14af4aa5`.

### Comparator (new skill)

```bash
uv run python flow.py "Find the populations of Madrid, Rome, and Lisbon, compare them, and tell me which two are closest in size."
```

Sessions: `s8-1dc4d047` (first), **`s8-a6972d7c`** (re-run with population figures + recovery splice).

### Part 3 — Critic (Ada Lovelace / distiller / auto-critic)

```bash
cd S8SharedCode/code
./scripts/run_assignment.sh 3
```

**Pass:** supported `birth_year` + `death_year` only — see [CRITIC_VERDICT.md](S8SharedCode/code/CRITIC_VERDICT.md).

**Fail + recovery:** mandatory unsupported `fields_medal_year` → critic fail → planner splice.

## Inspect runs

```bash
uv run python replay.py <session_id>
uv run python visualize_graph.py <session_id> --open
# HTML: state/sessions/<sid>/graph_view.html
```

## Demo recording script

Record in this order (~12 min):

1. Two terminals: `gateway/` → `uv run main.py`; `code/` → `uv sync` once.
2. `flow.py "Say hello."` — show session folder.
3. Open `prompts/coder.md` — show JSON contract; run query **I** or show `s8-30cc4b2c` graph.
4. Flash five base session IDs from `state/sessions/` (or re-run one live).
5. `./scripts/run_assignment.sh 2` then `visualize_graph.py <sid> --open` — parallel layer.
6. Critic pass + fail sessions; mention recovery log lines on fail run.
7. `agent_config.yaml` + `comparator.md` + comparator graph.
8. `uv run pytest tests/test_recovery.py`.

## Regression

```bash
cd S8SharedCode/code && uv run pytest tests/test_recovery.py
```

Expected: **22 passed**.

## Notes for graders

- Orchestrator [`flow.py`](S8SharedCode/code/flow.py) was not modified for the assignment scope.
- Supporting fixes: `skills.py`, `mcp_runner.py`, planner/researcher/critic prompts (documented in repo history).
- Playwright Chromium required for `fetch_url`: `cd code && uv run playwright install chromium`.
