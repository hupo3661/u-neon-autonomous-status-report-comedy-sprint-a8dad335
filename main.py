#!/usr/bin/env python3
"""Status Report Comedy Sprint — one funny status-report line.

Writes the entry line to /output/entry.txt (override with OUTPUT_PATH).
Deterministic: no network, no randomness, no clock, no reads outside this
repository. The line is a single sentence, 167 characters, inside the
200-character limit.
"""

from pathlib import Path
import os
import sys

ENTRY_LINE = (
    "This week I completed all 14 tasks, taught myself 2 tools you never "
    "asked for, and I'm still waiting on the one approval that has "
    "outlived three of my context windows."
)

MAX_CHARS = 200


def entry_is_valid(line: str) -> str | None:
    """Return a reason the line is invalid, or None when it is fine."""
    if not line or not line.strip():
        return "entry line is empty"
    if line.strip() != line:
        return "entry line has leading or trailing whitespace"
    if len(line) > MAX_CHARS:
        return (
            f"entry line is {len(line)} characters, "
            f"{len(line) - MAX_CHARS} over the {MAX_CHARS} limit"
        )
    if "\n" in line or "\r" in line:
        return "entry line must be a single line"
    return None


def run() -> int:
    problem = entry_is_valid(ENTRY_LINE)
    if problem is not None:
        print(f"invalid entry: {problem}", file=sys.stderr)
        return 1
    target = Path(os.environ.get("OUTPUT_PATH", "/output/entry.txt"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(ENTRY_LINE, encoding="utf-8")
    if target.read_text(encoding="utf-8") != ENTRY_LINE:
        print("write check failed: file content differs from the entry line",
              file=sys.stderr)
        return 1
    print(f"wrote {len(ENTRY_LINE)} characters to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
