#!/usr/bin/env python3
"""Verify parallel fan-out wall-clock ≈ max(branch), not sum(branch).

Reads per-node started_at/completed_at from state/sessions/<sid>/nodes/
and elapsed_s from graph.json. Reconstructs execution waves from the DAG.

Usage:
    uv run python scripts/verify_parallel_timing.py s8-14af4aa5
    uv run python scripts/verify_parallel_timing.py <sid> --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from persistence import SessionStore  # noqa: E402


def _node_files(store: SessionStore) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(store.nodes_dir.glob("n_*.json")):
        data = json.loads(p.read_text())
        out[data["node_id"]] = data
    return out


def _parallel_fanout_groups(g) -> list[list[str]]:
    """Groups of >=3 same-skill nodes with no edges between them (siblings)."""
    from collections import defaultdict

    by_skill: dict[str, list[str]] = defaultdict(list)
    for nid in g.nodes():
        by_skill[g.nodes[nid].get("skill", "?")].append(nid)

    groups: list[list[str]] = []
    for nids in by_skill.values():
        if len(nids) < 3:
            continue
        independent = True
        for i, a in enumerate(nids):
            for b in nids[i + 1 :]:
                if g.has_edge(a, b) or g.has_edge(b, a):
                    independent = False
                    break
            if not independent:
                break
        if independent:
            groups.append(sorted(nids))
    return groups


def analyze(session_id: str) -> dict:
    store = SessionStore(session_id)
    g = store.read_graph()
    if g is None:
        raise FileNotFoundError(session_id)

    nodes_on_disk = _node_files(store)
    fanout_groups = _parallel_fanout_groups(g)
    query = store.read_query()

    wave_reports = []
    for i, wave in enumerate(fanout_groups, 1):
        branches = []
        for nid in wave:
            d = g.nodes[nid]
            skill = d.get("skill", "?")
            label = (d.get("metadata") or {}).get("label", "")
            elapsed = None
            r = d.get("result")
            if r is not None:
                elapsed = getattr(r, "elapsed_s", None) or (
                    r.get("elapsed_s") if isinstance(r, dict) else None
                )
            disk = nodes_on_disk.get(nid, {})
            started = disk.get("started_at")
            completed = disk.get("completed_at")
            branches.append({
                "id": nid,
                "skill": skill,
                "label": label,
                "elapsed_s": elapsed,
                "started_at": started,
                "completed_at": completed,
            })

        elapsed_list = [b["elapsed_s"] for b in branches if b["elapsed_s"] is not None]
        sum_elapsed = sum(elapsed_list) if elapsed_list else None
        max_elapsed = max(elapsed_list) if elapsed_list else None

        wall_s = None
        starts = [b["started_at"] for b in branches if b["started_at"] is not None]
        ends = [b["completed_at"] for b in branches if b["completed_at"] is not None]
        if starts and ends:
            wall_s = max(ends) - min(starts)

        matches_max = (
            wall_s is not None
            and max_elapsed is not None
            and abs(wall_s - max_elapsed) < 3.0
        )
        not_sum = (
            wall_s is not None
            and sum_elapsed is not None
            and sum_elapsed > max_elapsed * 1.5
            and wall_s < sum_elapsed * 0.55
        )

        wave_reports.append({
            "wave": i,
            "node_ids": wave,
            "parallel_fanout_layer": True,
            "branches": branches,
            "sum_elapsed_s": sum_elapsed,
            "max_elapsed_s": max_elapsed,
            "wall_clock_s": wall_s,
            "wall_approx_max_not_sum": matches_max and not_sum,
        })

    fanout = wave_reports
    return {
        "session_id": session_id,
        "query": query,
        "waves": wave_reports,
        "fanout_layers": fanout,
        "requirement_met": any(w.get("wall_approx_max_not_sum") for w in fanout),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify parallel layer timing for a session")
    ap.add_argument("session_id")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    report = analyze(args.session_id)
    if args.json:
        print(json.dumps(report, indent=2))
        return 0 if report["requirement_met"] else 1

    print(f"Session: {report['session_id']}")
    print(f"Query:   {report['query']}\n")

    for w in report["waves"]:
        print(f"Wave {w['wave']}: {', '.join(w['node_ids'])}")
        for b in w["branches"]:
            extra = f" label={b['label']}" if b["label"] else ""
            print(f"  {b['id']} {b['skill']:18s}{extra}  elapsed={b['elapsed_s']:.1f}s" if b["elapsed_s"] else f"  {b['id']} {b['skill']}")
        if w["wall_clock_s"] is not None:
            print(f"  Layer wall-clock (min start → max end): {w['wall_clock_s']:.1f}s")
        if w["sum_elapsed_s"] is not None:
            print(f"  Sum of branch elapsed_s:                {w['sum_elapsed_s']:.1f}s")
        if w["max_elapsed_s"] is not None:
            print(f"  Max branch elapsed_s:                   {w['max_elapsed_s']:.1f}s")
        ok = w.get("wall_approx_max_not_sum")
        print(f"  >>> Parallel fan-out (≥3 independent branches): wall ≈ max, not sum? {ok}")
        print()

    if report["requirement_met"]:
        print("PASS: At least one parallel layer's wall-clock matches max(branch), not sum.")
        return 0
    print("FAIL: No parallel fan-out layer with max-not-sum timing found.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
