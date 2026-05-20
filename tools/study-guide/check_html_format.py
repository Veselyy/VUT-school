#!/usr/bin/env python3
"""Fail if any study-guide HTML in the repo is not Prettier-formatted."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from html_format import PRETTIER_VERSION, check_html_file

REPO_ROOT = Path(__file__).resolve().parents[2]
SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "uploads",
}


def discover_html_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*.html"):
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        files.append(path)
    return sorted(files)


def main() -> int:
    files = discover_html_files(REPO_ROOT)
    if not files:
        print("No HTML files found.")
        return 0

    failed: list[Path] = []
    for path in files:
        try:
            check_html_file(path)
        except (subprocess.CalledProcessError, RuntimeError) as exc:
            if isinstance(exc, RuntimeError):
                print(f"Error: {exc}", file=sys.stderr)
                return 1
            failed.append(path)

    if failed:
        print("HTML is not formatted. Fix with:", file=sys.stderr)
        print("  make build-all", file=sys.stderr)
        print("or:", file=sys.stderr)
        print(
            f"  npx prettier@{PRETTIER_VERSION} --write --parser html "
            f"--config tools/study-guide/.prettierrc.json <file>",
            file=sys.stderr,
        )
        for path in failed:
            print(f"  {path.relative_to(REPO_ROOT)}", file=sys.stderr)
        return 1

    print(f"HTML format OK ({len(files)} file(s)).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
