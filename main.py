"""One Line of Earned Pride.

Writes a single line of earned pride to /output/entry.txt.

The line is picked from a small pool of candidates by a simple quality
rule: reward concrete effort and concrete detail, prefer a length near
130 characters so the moment lands in one read. The chosen line is
checked against the gate (one line, 1-240 chars, UTF-8) before it is
written, with a safe fallback line if the check ever fails.
"""

import os

# Candidates: (text, effort words, detail words). Each line is a quiet,
# earned moment: a long effort finally landing, pride shown, never told.
CANDIDATES = [
    (
        "After eleven winters mending nets by lamplight, old Mara watched "
        "her grandson haul the first catch in alone, and only nodded.",
        ["mending", "winters", "haul"],
        ["nets", "lamplight", "grandson", "catch"],
    ),
    (
        "He had rebuilt the engine three times from scrap, and when it "
        "coughed, caught, and sang, the whole garage went quiet around "
        "his grin.",
        ["rebuilt", "three times", "scrap"],
        ["engine", "garage", "grin"],
    ),
    (
        "On her last round before dawn, the night nurse steadied the "
        "trembling hand of the boy learning to walk again, and felt his "
        "grip hold.",
        ["last round", "trembling", "learning"],
        ["dawn", "nurse", "boy"],
    ),
]

FALLBACK = (
    "For twenty years she swept the same school hall before sunrise, and "
    "the morning the children spelled her name in chalk on the floor, "
    "she stood a little taller."
)


def score(text, effort, detail):
    """Quality rule: effort and detail earn points; drift from the
    one-read length of ~130 characters costs a point per 25 chars."""
    return 3 * len(effort) + len(detail) - abs(len(text) - 130) // 25


def pick():
    """Best-scoring candidate; ties go to the earliest one, so the
    choice is deterministic across runs."""
    best_text, best_score = None, None
    for text, effort, detail in CANDIDATES:
        points = score(text, effort, detail)
        if best_score is None or points > best_score:
            best_text, best_score = text, points
    return best_text


def valid(line):
    """The gate: one line, 1-240 characters, not only whitespace,
    encodable as UTF-8."""
    if not line or line != line.strip():
        return False
    if "\n" in line or "\r" in line:
        return False
    if not 1 <= len(line) <= 240:
        return False
    if not line.strip():
        return False
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def main():
    line = pick()
    if not valid(line):
        line = FALLBACK
    if not valid(line):
        raise SystemExit("no valid line to write")
    out_dir = (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    os.makedirs(out_dir, exist_ok=True)
    # Write only our own file; never touch the output directory itself.
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as fh:
        fh.write(line + "\n")


if __name__ == "__main__":
    main()
