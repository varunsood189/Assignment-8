#!/usr/bin/env python3
"""Convert markdown to PDF using fpdf2.

Usage:
    uv run python generate_pdf.py
    uv run python generate_pdf.py docs/PROJECT_GUIDE.md PROJECT_GUIDE.pdf
    uv run python generate_pdf.py README.md CODE_EXPLANATION.pdf
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from fpdf import FPDF

ROOT = Path(__file__).parent
DEFAULT_INPUT = ROOT / "README.md"
DEFAULT_OUTPUT = ROOT / "CODE_EXPLANATION.pdf"
DEFAULT_TITLE = "Assignment 8 - Multi-Agent Growing-Graph Orchestrator"


class DocPDF(FPDF):
    def __init__(self, header_title: str = DEFAULT_TITLE):
        super().__init__()
        self._header_title = header_title

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, sanitize(self._header_title), align="C")
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def sanitize(text: str) -> str:
    """Replace unicode chars that core Helvetica fonts cannot render."""
    replacements = {
        "\u2014": "-",
        "\u2013": "-",
        "\u2192": "->",
        "\u2190": "<-",
        "\u2026": "...",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2500": "-",
        "\u2502": "|",
        "\u251c": "+",
        "\u2514": "+",
        "\u250c": "+",
        "\u2510": "+",
        "\u2534": "+",
        "\u252c": "+",
        "\u2022": "-",
        "\u2264": "<=",
        "\u2265": ">=",
        "\u00d7": "x",
        "\u2501": "=",
        "\u2550": "=",
        "\u2551": "|",
        "\u2554": "+",
        "\u2557": "+",
        "\u255a": "+",
        "\u255d": "+",
        "\u2560": "+",
        "\u2563": "+",
        "\u2566": "+",
        "\u2569": "+",
        "\u256c": "+",
        "\u2193": "v",
        "\u2191": "^",
        "\u250a": "|",
        "\u2518": "+",
        "\u251c": "+",
        "\u2524": "+",
        "\u252c": "+",
        "\u2534": "+",
        "\u253c": "+",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def write_wrapped(pdf: DocPDF, text: str, size: int = 10, style: str = "", indent: int = 0):
    pdf.set_font("Helvetica", style, size)
    pdf.set_text_color(30, 30, 30)
    effective_w = pdf.w - pdf.l_margin - pdf.r_margin - indent
    pdf.set_x(pdf.l_margin + indent)
    pdf.multi_cell(effective_w, size * 0.45, sanitize(text))
    pdf.ln(2)


def render_markdown(pdf: DocPDF, md: str) -> None:
    lines = md.splitlines()
    in_code = False
    code_buf: list[str] = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # fenced code block
        if line.strip().startswith("```"):
            if in_code:
                pdf.set_font("Courier", "", 8)
                pdf.set_fill_color(245, 245, 245)
                block = "\n".join(code_buf)
                for cl in block.splitlines():
                    pdf.set_x(pdf.l_margin)
                    pdf.multi_cell(0, 4.5, sanitize(cl), fill=True)
                pdf.ln(3)
                code_buf = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_buf.append(line)
            i += 1
            continue

        stripped = line.strip()

        if stripped == "---":
            pdf.ln(2)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
            pdf.ln(4)
            i += 1
            continue

        if stripped.startswith("# "):
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 18)
            pdf.set_text_color(20, 60, 120)
            pdf.multi_cell(0, 10, sanitize(re.sub(r"\*\*(.+?)\*\*", r"\1", stripped[2:])))
            pdf.ln(2)
            i += 1
            continue

        if stripped.startswith("## "):
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(30, 80, 140)
            pdf.multi_cell(0, 8, sanitize(stripped[3:]))
            pdf.ln(1)
            i += 1
            continue

        if stripped.startswith("### "):
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(50, 50, 50)
            pdf.multi_cell(0, 7, sanitize(stripped[4:]))
            pdf.ln(1)
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+\|", lines[i + 1].strip()):
            # table header
            headers = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2  # skip separator
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / max(len(headers), 1)
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_fill_color(230, 240, 250)
            for h in headers:
                pdf.cell(col_w, 6, sanitize(h)[:40], border=1, fill=True)
            pdf.ln()
            pdf.set_font("Helvetica", "", 8)
            for row in rows:
                for cell in row:
                    pdf.cell(col_w, 6, sanitize(cell)[:50], border=1)
                pdf.ln()
            pdf.ln(3)
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            write_wrapped(pdf, "  * " + stripped[2:], size=10, indent=4)
            i += 1
            continue

        m = re.match(r"^(\d+)\.\s+(.*)", stripped)
        if m:
            write_wrapped(pdf, f"  {m.group(1)}. {m.group(2)}", size=10, indent=4)
            i += 1
            continue

        if stripped.startswith("*") and stripped.endswith("*") and not stripped.startswith("**"):
            write_wrapped(pdf, stripped.strip("*"), size=10, style="I")
            i += 1
            continue

        if stripped == "":
            pdf.ln(2)
            i += 1
            continue

        # inline bold strip (simple)
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", stripped)
        text = re.sub(r"`(.+?)`", r"\1", text)
        write_wrapped(pdf, text, size=10)
        i += 1


def markdown_to_pdf(md_path: Path, out_path: Path, *, title: str | None = None) -> None:
    if not md_path.exists():
        raise FileNotFoundError(md_path)
    md = md_path.read_text(encoding="utf-8")
    header = title or md_path.stem.replace("_", " ")
    pdf = DocPDF(header_title=header)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_margins(18, 18, 18)
    render_markdown(pdf, md)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(out_path))
    print(f"Wrote {out_path} ({out_path.stat().st_size // 1024} KB)")


def main() -> None:
    ap = argparse.ArgumentParser(description="Convert markdown to PDF (fpdf2)")
    ap.add_argument("input", nargs="?", default=str(DEFAULT_INPUT), help="Input .md file")
    ap.add_argument("output", nargs="?", default=str(DEFAULT_OUTPUT), help="Output .pdf file")
    ap.add_argument("--title", help="PDF header title (default: input stem)")
    args = ap.parse_args()
    try:
        markdown_to_pdf(Path(args.input), Path(args.output), title=args.title)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
