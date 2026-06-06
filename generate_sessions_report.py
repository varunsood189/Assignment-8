#!/usr/bin/env python3
"""Scan state/sessions and write docs/SESSIONS_CATALOG.md."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent
SESSIONS_ROOT = ROOT / "S8SharedCode" / "code" / "state" / "sessions"
OUTPUT_MD = ROOT / "docs" / "SESSIONS_CATALOG.md"

KEY_SESSIONS: dict[str, str] = {
    "s8-7f8a75bf": "Part 1 / hello",
    "s8-5c7b354b": "Part 1 / A (Shannon)",
    "s8-30cc4b2c": "Part 1 / I + Part 4 coder",
    "s8-ea8e55ff": "Part 1 / J",
    "s8-65c8069d": "Part 1 / K (interrupt)",
    "s8-453bce58": "Part 2 / parallel fan-out",
    "s8-14af4aa5": "Part 2 / alternate (4 cities)",
    "s8-4fd467a0": "Part 3 / critic pass",
    "s8-418393c0": "Part 3 / critic fail + recovery",
    "s8-a6972d7c": "Part 5 / comparator",
    "s8-1dc4d047": "Part 5 / comparator (first run)",
}


def _truncate(text: str, n: int) -> str:
    text = " ".join(text.split())
    if len(text) <= n:
        return text
    return text[: n - 1] + "..."


def _load_graph(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _skills_from_graph(g: dict) -> list[str]:
    skills = []
    for node in g.get("nodes", []):
        s = node.get("skill")
        if s and s not in skills:
            skills.append(s)
    return skills


def _dag_shape(g: dict) -> str:
    """Topological-ish chain from planner following first successor edge."""
    nodes = {n["id"]: n for n in g.get("nodes", []) if "id" in n}
    if not nodes:
        return "?"
    edges = [(e["source"], e["target"]) for e in g.get("edges", []) if "source" in e]
    succ: dict[str, list[str]] = {}
    for u, v in edges:
        succ.setdefault(u, []).append(v)
    start = next((nid for nid, d in nodes.items() if d.get("skill") == "planner"), None)
    if not start:
        start = next(iter(nodes))
    parts = []
    seen = set()
    q = [start]
    while q and len(parts) < 12:
        nid = q.pop(0)
        if nid in seen or nid not in nodes:
            continue
        seen.add(nid)
        skill = nodes[nid].get("skill", "?")
        label = (nodes[nid].get("metadata") or {}).get("label")
        parts.append(f"{skill}({label})" if label else skill)
        for child in succ.get(nid, []):
            if child not in seen:
                q.append(child)
    return " -> ".join(parts) if parts else ", ".join(_skills_from_graph(g))


def _final_answer(g: dict) -> str:
    for node in g.get("nodes", []):
        if node.get("skill") != "formatter":
            continue
        result = node.get("result")
        if not result:
            continue
        if isinstance(result, dict):
            out = result.get("output") or {}
            fa = out.get("final_answer")
            if isinstance(fa, str) and fa.strip():
                return fa.strip()
    for node in reversed(g.get("nodes", [])):
        result = node.get("result")
        if not isinstance(result, dict):
            continue
        out = result.get("output")
        if isinstance(out, dict) and out:
            return json.dumps(out, default=str)[:500]
    return "(no final answer captured)"


def _session_mtime(sid_dir: Path) -> float:
    gp = sid_dir / "graph.json"
    if gp.exists():
        return gp.stat().st_mtime
    return sid_dir.stat().st_mtime


def collect_sessions() -> list[dict]:
    rows = []
    if not SESSIONS_ROOT.exists():
        return rows
    for sid_dir in sorted(SESSIONS_ROOT.iterdir()):
        if not sid_dir.is_dir() or not sid_dir.name.startswith("s8-"):
            continue
        sid = sid_dir.name
        query_path = sid_dir / "query.txt"
        query = query_path.read_text(encoding="utf-8").strip() if query_path.exists() else ""
        g = _load_graph(sid_dir / "graph.json")
        skills = _skills_from_graph(g) if g else []
        node_count = len(g.get("nodes", [])) if g else 0
        shape = _dag_shape(g) if g else "?"
        final = _final_answer(g) if g else ""
        rows.append({
            "id": sid,
            "tag": KEY_SESSIONS.get(sid, ""),
            "query": query,
            "skills": ", ".join(skills),
            "nodes": node_count,
            "shape": shape,
            "final": final,
            "mtime": _session_mtime(sid_dir),
        })
    rows.sort(key=lambda r: r["mtime"], reverse=True)
    return rows


def render_markdown(rows: list[dict]) -> str:
    lines = [
        "# Session 8 — Sessions Catalog",
        "",
        "Auto-generated catalog of all persisted runs under `S8SharedCode/code/state/sessions/`.",
        "",
        f"**Total sessions:** {len(rows)}",
        "",
        "---",
        "",
        "## Key assignment sessions",
        "",
    ]
    key_rows = [r for r in rows if r["tag"]]
    key_order = list(KEY_SESSIONS.keys())
    key_rows.sort(key=lambda r: key_order.index(r["id"]) if r["id"] in key_order else 999)

    for r in key_rows:
        lines.append(f"### {r['id']} — {r['tag']}")
        lines.append("")
        lines.append(f"**Query:** {r['query']}")
        lines.append("")
        lines.append(f"**Skills:** {r['skills']}")
        lines.append("")
        lines.append(f"**Nodes:** {r['nodes']} | **Shape:** {r['shape']}")
        lines.append("")
        lines.append("**Final answer:**")
        lines.append("")
        for fa_line in r["final"].splitlines() or [r["final"]]:
            lines.append(f"> {fa_line}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.extend([
        "## All sessions (newest first)",
        "",
        "| Session | Tag | Nodes | Skills | Query (short) |",
        "|---------|-----|-------|--------|---------------|",
    ])
    for r in rows:
        qshort = _truncate(r["query"], 80).replace("|", "/")
        tag = r["tag"] or "-"
        skills_short = _truncate(r["skills"], 40).replace("|", "/")
        lines.append(f"| {r['id']} | {tag} | {r['nodes']} | {skills_short} | {qshort} |")

    lines.extend([
        "",
        "---",
        "",
        "## Appendix — DAG shape and final answer (truncated)",
        "",
    ])
    other = [r for r in rows if not r["tag"]]
    for r in other:
        lines.append(f"### {r['id']}")
        lines.append("")
        lines.append(f"- **Query:** {_truncate(r['query'], 300)}")
        lines.append(f"- **Shape:** {_truncate(r['shape'], 200)}")
        lines.append(f"- **Final:** {_truncate(r['final'], 250)}")
        lines.append("")

    skill_counts = Counter()
    for r in rows:
        for s in r["skills"].split(", "):
            if s:
                skill_counts[s] += 1
    lines.extend([
        "---",
        "",
        "## Skill usage across all sessions",
        "",
        "| Skill | Sessions |",
        "|-------|----------|",
    ])
    for skill, count in skill_counts.most_common():
        lines.append(f"| {skill} | {count} |")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    rows = collect_sessions()
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text(render_markdown(rows), encoding="utf-8")
    print(f"Wrote {OUTPUT_MD} ({len(rows)} sessions)")


if __name__ == "__main__":
    main()
