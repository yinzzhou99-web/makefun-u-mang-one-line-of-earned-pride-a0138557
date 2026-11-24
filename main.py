#!/usr/bin/env python3
"""One Line of Earned Pride.

Writes a single line of text, 1 to 240 characters, to /output/entry.txt:
a quiet, earned moment of pride for someone in a scene.
"""

import os

LINE = "The apprentice filed the same joint until the two pieces slid together without a sound."


def main() -> None:
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(LINE + "\n")


if __name__ == "__main__":
    main()
