# Security — API keys & secrets

## Do not commit

| Path | Purpose |
|------|---------|
| `S8SharedCode/.env` | LLM provider keys, Tavily, Ollama URL (used by gateway + agent) |
| `S8SharedCode/gateway/.env` | Optional duplicate; gateway reads package-root `.env` first |

These paths are listed in `.gitignore`. **Only** `*.env.example` files belong in Git — placeholders with empty values.

## Setup (after clone)

```bash
cp S8SharedCode/.env.example S8SharedCode/.env
# Edit S8SharedCode/.env locally — never push this file
```

## If a key was committed by mistake

1. **Rotate** the exposed key at the provider (Gemini, Groq, OpenRouter, etc.).
2. Remove the file from Git history (`git filter-repo` or BFG) — deleting in a new commit is not enough if the repo was pushed.
3. Confirm `.env` is ignored: `git check-ignore -v S8SharedCode/.env`

## What is safe to commit

- Source code, prompts, tests, scripts
- `*.env.example` templates
- Documentation (`.md`, optional PDFs)
- `uv.lock` files (reproducible installs)

## What stays local

- All of `code/state/sessions/` (run logs, prompts sent, graph snapshots)
- FAISS index + `memory.json`
- `.venv/` directories
