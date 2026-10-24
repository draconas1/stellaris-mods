#!/usr/bin/env python3
"""Flatten Stellaris script_documentation logs into one-line-per-entry files.

Output goes to .reference/ (gitignored). Stdlib only.

Usage: tools/ingest_docs.py [docs_dir]
"""
import re
import sys
from pathlib import Path

DEFAULT_DIR = Path.home() / ".local/share/Paradox Interactive/Stellaris/logs/script_documentation"
OUT_DIR = Path(__file__).resolve().parent.parent / ".reference"
STAMP = re.compile(r"^\[\d\d:\d\d:\d\d\]\[[^\]]+\]:\s*")


def entries(text):
    """Blank-line separated blocks, with log timestamp prefixes stripped."""
    for block in re.split(r"\n\s*\n", text):
        lines = [STAMP.sub("", l).rstrip() for l in block.splitlines()]
        lines = [l for l in lines if l.strip() and not l.startswith("==")]
        if lines:
            yield lines


def flatten(lines):
    head, *rest = lines
    return head + " || " + " ".join(l.strip() for l in rest) if rest else head


def convert_blocks(src, dst):
    out = [flatten(b) for b in entries(src.read_text(errors="replace"))
           if " - " in b[0]]
    dst.write_text("\n".join(out) + "\n")
    return len(out)


def convert_modifiers(src, dst):
    out = [l.strip()[2:] for l in src.read_text(errors="replace").splitlines()
           if l.startswith("- ") and ", Category:" in l]
    dst.write_text("\n".join(out) + "\n")
    return len(out)


def main():
    docs = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_DIR
    OUT_DIR.mkdir(exist_ok=True)
    jobs = [("effects", convert_blocks), ("triggers", convert_blocks),
            ("scopes", convert_blocks), ("modifiers", convert_modifiers)]
    for name, fn in jobs:
        src = docs / f"{name}.log"
        if not src.exists():
            print(f"missing {src}")
            continue
        n = fn(src, OUT_DIR / f"{name}.txt")
        print(f"{name}: {n} entries")


if __name__ == "__main__":
    main()
