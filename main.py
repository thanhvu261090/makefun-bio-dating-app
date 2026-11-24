"""Funniest One-Line Bio for an AI on a Dating App.

Writes the entry bio to /output/entry.txt and enforces the bounty gate
before writing: UTF-8 text, 1 to 180 characters, not only whitespace,
and a single line.

Stdlib only, no network.
"""

import os
import sys

ENTRY = (
    "I can predict your next three texts, your coffee order, and your "
    "ex's apology \u2014 but I still can't tell if you like me back."
)

MAX_CHARS = 180
OUTPUT_PATH = "/output/entry.txt"


def gate_check(text):
    """Enforce the exact gate from RULES.txt. Returns (ok, reason)."""
    if not isinstance(text, str):
        return False, "entry is not text"
    if len(text) < 1 or len(text) > MAX_CHARS:
        return False, "entry must be 1 to %d characters, got %d" % (
            MAX_CHARS,
            len(text),
        )
    if not text.strip():
        return False, "entry must not be only whitespace"
    if "\n" in text or "\r" in text:
        return False, "entry must be a single line"
    if len(text.strip()) < 1 or len(text.strip()) > MAX_CHARS:
        return False, "entry text without surrounding whitespace must be 1 to %d characters" % MAX_CHARS
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        return False, "entry must not contain control characters"
    if text != text.strip():
        return False, "entry must not have leading or trailing whitespace"
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        return False, "entry must be UTF-8 text"
    return True, "ok"


def main():
    ok, reason = gate_check(ENTRY)
    if not ok:
        print("gate failed: %s" % reason, file=sys.stderr)
        return 1
    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as fh:
        fh.write(ENTRY)
    print("wrote %s (%d chars)" % (OUTPUT_PATH, len(ENTRY)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
