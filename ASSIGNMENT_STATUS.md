# Running the project

Quick reference for setup and the five example workflows. Session output is written locally under `S8SharedCode/code/state/sessions/` (gitignored).

**Docs:** [PROJECT_GUIDE.pdf](PROJECT_GUIDE.pdf) · [docs/PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md)

---

## Setup

Two terminals: gateway on port **8108** + agent in `code/`.

```bash
cd S8SharedCode
cp .env.example .env    # edit locally — never commit .env
cd gateway && uv sync && cd ..
cd code && uv sync && cd ..
cd code && uv run playwright install chromium
ollama pull nomic-embed-text
```

**Terminal 1 — gateway**

```bash
cd S8SharedCode/gateway && uv run main.py
```

**Terminal 2 — agent**

```bash
cd S8SharedCode/code
```

---

## Run scripts

```bash
./scripts/run_assignment.sh 1 hello
./scripts/run_assignment.sh 1 A
./scripts/run_assignment.sh 1 I
./scripts/run_assignment.sh 1 J
./scripts/run_assignment.sh 1 K
./scripts/run_assignment.sh 2          # parallel fan-out
./scripts/run_assignment.sh 3 pass
./scripts/run_assignment.sh 3 fail
./scripts/run_assignment.sh 4
./scripts/run_assignment.sh 5
./scripts/run_assignment.sh resume s8-<session_id>
./scripts/run_assignment.sh --help
```

**Query K (interrupt + resume):** start with `1 K`, SIGKILL mid-run, then `./scripts/run_assignment.sh resume <session_id>`.

---

## Inspect a run

```bash
uv run python replay.py <session_id>
uv run python visualize_graph.py <session_id> --open
uv run python scripts/verify_parallel_timing.py <session_id>   # Part 2 timing check
```

---

## Tests

```bash
cd S8SharedCode/code
uv run pytest tests/test_recovery.py
```

---

## Part reference

| Part | Script | Notes |
|------|--------|-------|
| 1 | `run_assignment.sh 1 …` | hello, Shannon fetch, populations, graceful fail, resume |
| 2 | `run_assignment.sh 2` | [PARALLEL_FANOUT.md](S8SharedCode/code/PARALLEL_FANOUT.md) |
| 3 | `run_assignment.sh 3` | [CRITIC_VERDICT.md](S8SharedCode/code/CRITIC_VERDICT.md) |
| 4 | `run_assignment.sh 4` | Coder + sandbox (query I) |
| 5 | `run_assignment.sh 5` | Comparator skill |

**Example session outputs:** [docs/RUN_LOGS.md](../docs/RUN_LOGS.md) · [docs/RUN_RESULTS.md](../docs/RUN_RESULTS.md)

---

## Regenerate PDF docs

```bash
cd S8SharedCode/code
uv run --with fpdf2 python ../../generate_pdf.py ../../docs/PROJECT_GUIDE.md ../../PROJECT_GUIDE.pdf
uv run --with fpdf2 python ../../generate_pdf.py ../../README.md ../../CODE_EXPLANATION.pdf
```

Optional local session catalog (not tracked in git):

```bash
python3 generate_sessions_report.py
uv run --with fpdf2 python generate_pdf.py docs/SESSIONS_CATALOG.md SESSIONS_CATALOG.pdf
```
