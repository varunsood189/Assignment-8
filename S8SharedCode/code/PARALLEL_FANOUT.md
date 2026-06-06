# Part 2 — Parallel fan-out (non–city query)

Assignment requirement: **≥3 independent sub-tasks**, Planner emits **concurrent** nodes, wall-clock of the parallel layer ≈ **max(branch)**, not **sum**.

## Recommended query (three Wikipedia URLs — not populations)

Each bullet is an independent `researcher` branch (`fetch_url` on a fixed URL). No city names.

```bash
cd S8SharedCode/code

uv run python flow.py "Run three parallel research branches: (1) From https://en.wikipedia.org/wiki/CRISPR — one sentence on what CRISPR is. (2) From https://en.wikipedia.org/wiki/MRNA_vaccine — one sentence on how mRNA vaccines work. (3) From https://en.wikipedia.org/wiki/Photovoltaic_effect — one sentence on how solar cells convert light. Then merge the three answers and say which two topics are most related to medicine."
```

**Expected DAG shape:**

```text
planner
  ├─ researcher (CRISPR URL)
  ├─ researcher (mRNA URL)
  └─ researcher (photovoltaic URL)   ← 3 concurrent siblings
        ↓ (barrier)
  distiller or summariser → formatter
```

Planner rule in `prompts/planner.md`: explicit URL → `researcher`; multiple items → **one node per item**, not one mega-node.

---

## Alternatives (also non-city)

### Nobel years (three people)

```bash
uv run python flow.py "In three parallel branches, find the year each person won the Nobel Prize in Physics: Marie Curie, Richard Feynman, and Subrahmanyan Chandrasekhar. Then say which two prizes were closest in time."
```

### Three algorithms (compute layer)

```bash
uv run python flow.py "Research worst-case time complexity for binary search, merge sort, and quicksort in three separate branches, then use Python to print which two algorithms share the same Big-O class."
```

Expect: 3× `researcher` ∥ → `coder` → `sandbox_executor` → `formatter`.

### Three papers in local corpus (retriever fan-out)

```bash
uv run python flow.py "From the indexed papers, in three parallel retriever branches, pull the main architectural claim from: (1) attention is all you need, (2) BERT, (3) GPT-3. Then summarize how the three differ."
```

Only works if FAISS index has those chunks; clear stale memory if the planner mis-routes.

---

## Verify max vs sum (after a run)

Replace `<sid>` with the session id printed by `flow.py`.

```bash
uv run python visualize_graph.py <sid> --open
uv run python scripts/verify_parallel_timing.py <sid>
```

**PASS** means layer wall-clock ≈ longest branch, and much less than the sum of all branch times.

**On video:** show terminal lines for the parallel batch, e.g. three `[n:x] researcher complete (Xs)` with different seconds, then run the verify script.

---

## Course note

The Tokyo/Delhi/Shanghai run (`s8-14af4aa5`) already satisfies part 2. Use **this** query if you want a cleaner story that is not population/city trivia.
