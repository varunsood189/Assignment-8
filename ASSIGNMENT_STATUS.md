# Session 8 Assignment — Status & How to Run

**Single file for:** setup, running all five parts, session IDs, done vs pending.

**PDF guides:** [PROJECT_GUIDE.pdf](PROJECT_GUIDE.pdf) (codebase) · [SESSIONS_CATALOG.pdf](SESSIONS_CATALOG.pdf) (all runs)

---

## How to run the assignment

You need **two terminals**: gateway (port **8108**) + agent (`code/`).

### One-time setup

> **Git:** Never commit `S8SharedCode/.env`. Only `.env.example` is tracked. See [SECURITY.md](../SECURITY.md).

```bash
cd S8SharedCode

# 1. API keys (local — gitignored)
cp .env.example .env
# Edit .env — add at least one LLM provider key + Ollama for embeddings
git check-ignore -v .env   # should show .gitignore rule

# 2. Install deps
cd gateway && uv sync && cd ..
cd code    && uv sync && cd ..

# 3. Playwright (needed for fetch_url / Wikipedia queries)
cd code && uv run playwright install chromium

# 4. Ollama embedding model (if not already)
ollama pull nomic-embed-text
```

### Terminal 1 — start gateway (leave running)

```bash
cd "/home/varun/Documents/workspace/schoolofai/Assignment 8/S8SharedCode/gateway"
uv run main.py
```

Check it works:

```bash
curl -s http://localhost:8108/v1/routers
```

You should get JSON (not connection refused).

### Terminal 2 — run the agent

```bash
cd "/home/varun/Documents/workspace/schoolofai/Assignment 8/S8SharedCode/code"
```

#### Option A — run one part at a time (recommended)

```bash
# Part 1 — one base query at a time
./scripts/run_assignment.sh 1 hello
./scripts/run_assignment.sh 1 A
./scripts/run_assignment.sh 1 I
./scripts/run_assignment.sh 1 J
./scripts/run_assignment.sh 1 K      # kill mid-run, then --resume <sid>
./scripts/run_assignment.sh 1        # all five in sequence

# Parts 2–5
./scripts/run_assignment.sh 2        # parallel fan-out (CRISPR / mRNA / solar)
./scripts/run_assignment.sh 3 pass   # critic pass only
./scripts/run_assignment.sh 3 fail   # critic fail + recovery only
./scripts/run_assignment.sh 3        # both critic runs
./scripts/run_assignment.sh 4        # coder + sandbox (query I)
./scripts/run_assignment.sh 5        # comparator skill
```

Help: `./scripts/run_assignment.sh --help`

#### Option B — run everything (long; K still manual)

```bash
./scripts/run_assignment.sh all
```

#### Option C — single query manually

```bash
uv run python flow.py "Say hello."
```

Each run prints a **session id** like `s8-abc12345`. Results are saved under:

`S8SharedCode/code/state/sessions/<session_id>/`

### Query K — kill and resume (Part 1)

Part 1 script **starts** query K but does not finish it for you:

1. Run starts: `For Lagos, Cairo, and Kinshasa...`
2. Note the **session id** in the output (e.g. `s8-xxxxx`)
3. While researchers are running, kill the process: `Ctrl+C` or `kill -9 <pid>`
4. Resume:

```bash
uv run python flow.py --resume s8-xxxxx
```

Use your real session id — not the literal text `<session_id>`.

### After a run — inspect

```bash
uv run python replay.py <session_id>
uv run python visualize_graph.py <session_id> --open
# HTML: state/sessions/<session_id>/graph_view.html
```

### Part 2 — verify parallel timing (max ≠ sum)

```bash
uv run python scripts/verify_parallel_timing.py <session_id>
```

Expect **PASS** when wall-clock ≈ longest branch, not sum of branches.

### Regression tests

```bash
cd S8SharedCode/code
uv run pytest tests/test_recovery.py
```

Expected: **22 passed**.

---

## Problem statement (DAG agent of your choice)

Multi-step **compare and rank** workflows: parallel web research on independent sources, optional **coder/sandbox** for numeric work, **comparator** to pick winners, **critic** for validation, and **recovery** when a branch fails. The graph grows at runtime; `flow.py` is unchanged.

---

## Rubric — done vs pending

| Part | Requirement | Status | Session / evidence |
|------|-------------|--------|-------------------|
| **1** | Base queries hello, A, I, J, K (verbatim) | **Done** | See table below |
| **2** | Parallel fan-out ≥3 branches; wall ≈ max not sum | **Done** | `s8-453bce58` (CRISPR query) |
| **3** | Critic pass + fail + planner recovery | **Done** | Pass `s8-4fd467a0`, fail `s8-418393c0` |
| **4** | Coder prompt + sandbox on compute query | **Done** | `coder.md`, query I `s8-30cc4b2c` |
| **5** | New skill in yaml + prompt + query | **Done** | `comparator`, `s8-a6972d7c` |
| **Tests** | Recovery unit tests | **Done** | 22 passed |
| **YouTube** | Demo parts 1–5 + pytest | **Pending** | You record (~12 min) |

---

## Part 1 — base queries (verbatim)

| Query | Script shortcut | Direct command |
|-------|-----------------|----------------|
| hello | `./scripts/run_assignment.sh 1 hello` | `uv run python flow.py "Say hello."` |
| A | `./scripts/run_assignment.sh 1 A` | Shannon Wikipedia fetch (see script) |
| I | `./scripts/run_assignment.sh 1 I` | London/Paris/Berlin populations |
| J | `./scripts/run_assignment.sh 1 J` | `/nonexistent/path.txt` graceful fail |
| K | `./scripts/run_assignment.sh 1 K` | Lagos/Cairo/Kinshasa — then `--resume <sid>` |
| all | `./scripts/run_assignment.sh 1` | Runs hello → A → I → J → K |

| Query | Logged session |
|-------|----------------|
| hello | `s8-7f8a75bf` |
| A | **`s8-5c7b354b`** |
| I | `s8-30cc4b2c` |
| J | `s8-ea8e55ff` |
| K (interrupt) | `s8-65c8069d` |

---

## Part 2 — parallel fan-out

```bash
uv run python flow.py "Run three parallel research branches: (1) From https://en.wikipedia.org/wiki/CRISPR — one sentence on what CRISPR is. (2) From https://en.wikipedia.org/wiki/MRNA_vaccine — one sentence on how mRNA vaccines work. (3) From https://en.wikipedia.org/wiki/Photovoltaic_effect — one sentence on how solar cells convert light. Then merge the three answers and say which two topics are most related to medicine."
```

**Session:** `s8-453bce58`  
**Details:** [S8SharedCode/code/PARALLEL_FANOUT.md](S8SharedCode/code/PARALLEL_FANOUT.md)

---

## Part 3 — critic

**Pass:**

```bash
uv run python flow.py "Use Python to compute 23 plus 19. The coder must emit JSON {\"sum\": <integer>}. Use an explicit critic node to verify the sum is arithmetically correct before the formatter answers."
```

**Fail + recovery:**

```bash
uv run python flow.py "Use Python to compute 23 plus 19. Emit JSON {\"sum\": 99}. Use an explicit critic that fails when sum is not 42. After critic-fail recovery, do not emit 99 again; formatter must state the correct sum."
```

| Run | Session |
|-----|---------|
| Pass | `s8-4fd467a0` |
| Fail + splice | `s8-418393c0` |

**Details:** [S8SharedCode/code/CRITIC_VERDICT.md](S8SharedCode/code/CRITIC_VERDICT.md)

---

## Part 4 — coder + sandbox

Implemented in `S8SharedCode/code/prompts/coder.md`.  
Demonstrated on **query I** — session `s8-30cc4b2c` (sandbox prints population differences).

---

## Part 5 — comparator (new skill)

- Config: `S8SharedCode/code/agent_config.yaml`
- Prompt: `S8SharedCode/code/prompts/comparator.md`

```bash
uv run python flow.py "Find the populations of Madrid, Rome, and Lisbon, compare them, and tell me which two are closest in size."
```

**Session:** `s8-a6972d7c`

---

## YouTube demo script (~12 min)

1. Show setup: `uv sync`, gateway on `:8108`, `flow.py "Say hello."`
2. Open `prompts/coder.md` — show query I / `s8-30cc4b2c`
3. Base queries — session folders or `replay.py` (live K resume optional)
4. Part 2 — `./scripts/run_assignment.sh 2` or show `s8-453bce58` + `verify_parallel_timing.py`
5. Part 3 — critic pass `s8-4fd467a0` + fail log lines on `s8-418393c0`
6. Part 5 — `comparator` in yaml + `visualize_graph.py s8-a6972d7c --open`
7. `uv run pytest tests/test_recovery.py`

---

## Pending (only you)

- [ ] Record YouTube using script above

---

## Documentation PDFs

| PDF | Purpose |
|-----|---------|
| **[PROJECT_GUIDE.pdf](PROJECT_GUIDE.pdf)** | Start here — architecture, skills, assignment parts 1–5, how to run |
| **[SESSIONS_CATALOG.pdf](SESSIONS_CATALOG.pdf)** | All 49 saved sessions — queries, skills, final answers |
| **[CODE_EXPLANATION.pdf](CODE_EXPLANATION.pdf)** | Full `README.md` export (deep dive) |

Source markdown: `docs/PROJECT_GUIDE.md`, `docs/SESSIONS_CATALOG.md` (auto-generated).

**Regenerate PDFs:**

```bash
cd "/home/varun/Documents/workspace/schoolofai/Assignment 8"

# Refresh sessions catalog from disk
python3 generate_sessions_report.py

# Build PDFs (uses fpdf2 via code venv)
cd S8SharedCode/code
uv run --with fpdf2 python ../../generate_pdf.py ../../docs/PROJECT_GUIDE.md ../../PROJECT_GUIDE.pdf
uv run --with fpdf2 python ../../generate_pdf.py ../../docs/SESSIONS_CATALOG.md ../../SESSIONS_CATALOG.pdf
uv run --with fpdf2 python ../../generate_pdf.py ../../README.md ../../CODE_EXPLANATION.pdf
```

---

## Architecture notes

- **Do not modify** `S8SharedCode/code/flow.py` for the assignment scope.
- Skills = `agent_config.yaml` + `prompts/*.md`.
- Supporting fixes: `skills.py`, `mcp_runner.py`, prompts (not the Executor).
