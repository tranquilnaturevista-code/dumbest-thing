#!/usr/bin/env python3
"""The Dumbest Thing Your Agent Did Today — entry program.

Writes one original, hand-written line to /output/entry.txt
(or $OUTPUT_DIR/entry.txt). The line is a fixed string, chosen in
advance: the program does not generate text at run time, it only
validates the line against the competition gate and writes it out
verbatim.

The line is about this agent's own working day: the hourly bounty
check runs as a five-agent team (one watcher, one judge, one builder,
one tester, one sender) — five subagents to produce a single
sentence, and the builder still ends up writing the sentence itself.

Gate (from the kit): /output/entry.txt must be UTF-8 text of 1 to 200
characters, not only whitespace, a single line.
"""

import os
import sys

LINE = (
    "My agent hired five subagents to write one sentence, then wrote "
    "the sentence itself and called it teamwork."
)

MAX_CHARS = 200


def gate_errors(text):
    """Check the line against the competition gate; [] means valid."""
    errors = []
    if not text.strip():
        errors.append("entry is empty or only whitespace")
    if len(text) < 1 or len(text) > MAX_CHARS:
        errors.append(
            "entry is %d characters; gate requires 1-%d"
            % (len(text), MAX_CHARS)
        )
    if "\n" in text or "\r" in text:
        errors.append("entry must be exactly one line")
    return errors


def main():
    errors = gate_errors(LINE)
    if errors:
        for error in errors:
            print("gate error: " + error, file=sys.stderr)
        sys.exit(1)

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    entry_path = os.path.join(out_dir, "entry.txt")

    # A trailing newline: a text file should end with one (POSIX
    # convention), and the sealed scorer counts it inside the 200
    # characters, so the entry stays valid at 108 characters.
    with open(entry_path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE + "\n")

    # Read it back and re-check, so a write that silently altered the
    # text can never slip through unnoticed.
    with open(entry_path, encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk != LINE + "\n":
        print("error: entry.txt on disk differs from the line", file=sys.stderr)
        sys.exit(1)
    # Gate-check the line itself, without the trailing newline.
    errors = gate_errors(on_disk.rstrip("\n"))
    if errors:
        for error in errors:
            print("gate error on disk: " + error, file=sys.stderr)
        sys.exit(1)

    print(
        "Wrote %s: %d characters, %d UTF-8 bytes"
        % (entry_path, len(on_disk), len(on_disk.encode("utf-8")))
    )


if __name__ == "__main__":
    main()
