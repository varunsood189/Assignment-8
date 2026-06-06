#!/usr/bin/env python3
"""Render a Session 8 run as an interactive HTML DAG.

Usage:
    uv run python visualize_graph.py <session_id>
    uv run python visualize_graph.py <session_id> --open
    uv run python visualize_graph.py --list

Writes: state/sessions/<sid>/graph_view.html
"""

from __future__ import annotations

import argparse
import json
import sys
import webbrowser
from pathlib import Path

import networkx as nx

from persistence import SessionStore, list_sessions

ROOT = Path(__file__).parent
STATUS_COLORS = {
    "complete": "#22c55e",
    "running": "#3b82f6",
    "pending": "#94a3b8",
    "failed": "#ef4444",
    "skipped": "#f59e0b",
}

SKILL_COLORS = {
    "planner": "#8b5cf6",
    "researcher": "#0ea5e9",
    "retriever": "#06b6d4",
    "distiller": "#14b8a6",
    "summariser": "#64748b",
    "comparator": "#f97316",
    "critic": "#e11d48",
    "formatter": "#10b981",
    "coder": "#6366f1",
    "sandbox_executor": "#a855f7",
}


def _load_graph(store: SessionStore) -> nx.DiGraph:
    g = store.read_graph()
    if g is None:
        raise FileNotFoundError(f"No graph.json for session {store.session_id}")
    return g


def _infer_edges(g: nx.DiGraph) -> list[tuple[str, str, str]]:
    """Build edge list from explicit edges + input references (n:...)."""
    seen: set[tuple[str, str]] = set()
    out: list[tuple[str, str, str]] = []

    def add(u: str, v: str, kind: str) -> None:
        if u == v or not u or not v:
            return
        key = (u, v)
        if key in seen:
            return
        seen.add(key)
        out.append((u, v, kind))

    for u, v in g.edges():
        add(u, v, "exec")

    for nid, data in g.nodes(data=True):
        for inp in data.get("inputs") or []:
            if isinstance(inp, str) and inp.startswith("n:") and inp in g.nodes:
                add(inp, nid, "input")
            elif inp == "USER_QUERY":
                add("__USER__", nid, "query")

    return out


def _node_label(nid: str, data: dict) -> str:
    skill = data.get("skill", "?")
    label = (data.get("metadata") or {}).get("label")
    line1 = f"{nid}\\n{skill}"
    if label:
        line1 += f"\\n({label})"
    result = data.get("result")
    if result is not None:
        elapsed = getattr(result, "elapsed_s", None) or (result.get("elapsed_s") if isinstance(result, dict) else None)
        if elapsed is not None:
            line1 += f"\\n{elapsed:.1f}s"
    return line1


def _build_payload(store: SessionStore, g: nx.DiGraph) -> dict:
    query = store.read_query() or ""
    nodes = []
    for nid, data in g.nodes(data=True):
        skill = data.get("skill", "?")
        status = data.get("status", "pending")
        result = data.get("result")
        err = ""
        if result is not None:
            err = getattr(result, "error", None) or (result.get("error") if isinstance(result, dict) else "") or ""
        nodes.append({
            "id": nid,
            "label": _node_label(nid, data),
            "skill": skill,
            "status": status,
            "color": STATUS_COLORS.get(status, "#94a3b8"),
            "border": SKILL_COLORS.get(skill, "#475569"),
            "title": json.dumps({
                "skill": skill,
                "status": status,
                "inputs": data.get("inputs"),
                "metadata": data.get("metadata"),
                "error": err[:200] if err else None,
            }, indent=2),
        })

    edges = [{"from": u, "to": v, "kind": k} for u, v, k in _infer_edges(g)]
    return {"session_id": store.session_id, "query": query, "nodes": nodes, "edges": edges}


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>S8 DAG — __SESSION__</title>
  <script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; font-family: system-ui, sans-serif; background: #0f172a; color: #e2e8f0; }
    header { padding: 12px 16px; background: #1e293b; border-bottom: 1px solid #334155; }
    header h1 { margin: 0 0 6px; font-size: 1.1rem; }
    header p { margin: 0; font-size: 0.85rem; color: #94a3b8; max-width: 900px; }
    #graph { width: 100%; height: calc(100vh - 120px); background: #0f172a; }
    .legend { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; font-size: 0.75rem; }
    .legend span { display: inline-flex; align-items: center; gap: 4px; }
    .dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
    .toolbar { margin-top: 8px; }
    button { background: #334155; color: #e2e8f0; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer; margin-right: 6px; }
    button:hover { background: #475569; }
  </style>
</head>
<body>
  <header>
    <h1>Session __SESSION__</h1>
    <p><strong>Query:</strong> __QUERY_ESC__</p>
    <div class="legend">
      <span><i class="dot" style="background:#22c55e"></i> complete</span>
      <span><i class="dot" style="background:#3b82f6"></i> running</span>
      <span><i class="dot" style="background:#94a3b8"></i> pending</span>
      <span><i class="dot" style="background:#ef4444"></i> failed</span>
      <span><i class="dot" style="background:#f59e0b"></i> skipped</span>
      <span style="margin-left:12px">Border color = skill type</span>
    </div>
    <div class="toolbar">
      <button type="button" onclick="network.fit()">Fit view</button>
      <button type="button" onclick="layoutHierarchical()">Hierarchical layout</button>
      <button type="button" onclick="layoutPhysics()">Physics layout</button>
    </div>
  </header>
  <div id="graph"></div>
  <script>
    const payload = __PAYLOAD__;
    const nodes = new vis.DataSet(payload.nodes.map(n => ({
      id: n.id,
      label: n.label,
      title: n.title,
      color: { background: n.color, border: n.border, highlight: { background: n.color, border: '#fff' } },
      borderWidth: 2,
      font: { color: '#f8fafc', size: 12, face: 'monospace' },
      shape: n.id === '__USER__' ? 'ellipse' : 'box',
    })));
    const edges = new vis.DataSet(payload.edges.map((e, i) => ({
      id: 'e' + i,
      from: e.from,
      to: e.to,
      arrows: 'to',
      color: e.kind === 'query' ? { color: '#64748b' } : { color: '#94a3b8' },
      dashes: e.kind === 'input',
    })));
    const container = document.getElementById('graph');
    const data = { nodes, edges };
    const options = {
      layout: {
        hierarchical: {
          enabled: true,
          direction: 'UD',
          sortMethod: 'directed',
          levelSeparation: 100,
          nodeSpacing: 140,
        }
      },
      physics: { enabled: false },
      interaction: { hover: true, tooltipDelay: 100, navigationButtons: true },
    };
    const network = new vis.Network(container, data, options);
    function layoutHierarchical() {
      network.setOptions({ layout: { hierarchical: { enabled: true, direction: 'UD' } }, physics: { enabled: false } });
    }
    function layoutPhysics() {
      network.setOptions({ layout: { hierarchical: { enabled: false } }, physics: { enabled: true, stabilization: { iterations: 120 } } });
    }
    window.network = network;
    network.on('click', p => {
      if (p.nodes.length) console.log('Node', p.nodes[0], nodes.get(p.nodes[0]));
    });
  </script>
</body>
</html>
"""


def render_html(payload: dict) -> str:
    q = payload["query"].replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    if len(q) > 500:
        q = q[:500] + "…"
    return (
        HTML_TEMPLATE.replace("__SESSION__", payload["session_id"])
        .replace("__QUERY_ESC__", q)
        .replace("__PAYLOAD__", json.dumps(payload))
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Visualize S8 session DAG as HTML")
    ap.add_argument("session_id", nargs="?", help="Session id (e.g. s8-1dc4d047)")
    ap.add_argument("--open", action="store_true", help="Open in default browser")
    ap.add_argument("--list", action="store_true", help="List available sessions")
    ap.add_argument("-o", "--output", help="Output HTML path (default: session dir/graph_view.html)")
    args = ap.parse_args()

    if args.list:
        for sid in list_sessions():
            print(sid)
        return 0

    if not args.session_id:
        ap.print_help()
        return 1

    store = SessionStore(args.session_id)
    g = _load_graph(store)
    payload = _build_payload(store, g)

    if "__USER__" not in g.nodes:
        payload["nodes"].insert(0, {
            "id": "__USER__",
            "label": "USER_QUERY",
            "skill": "user",
            "status": "complete",
            "color": "#334155",
            "border": "#64748b",
            "title": payload["query"][:500],
        })

    out_path = Path(args.output) if args.output else store.dir / "graph_view.html"
    out_path.write_text(render_html(payload), encoding="utf-8")
    print(f"Wrote {out_path}")
    print(f"  nodes: {len(payload['nodes'])}  edges: {len(payload['edges'])}")

    if args.open:
        webbrowser.open(out_path.as_uri())

    return 0


if __name__ == "__main__":
    sys.exit(main())
