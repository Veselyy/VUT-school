"""Format generated study-guide HTML (Prettier)."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
PRETTIER_CONFIG = TOOL_DIR / ".prettierrc.json"
PRETTIER_VERSION = "3.5.3"


class HtmlFormatError(Exception):
    """Raised when HTML does not match the expected formatter output."""


def _prettier_cmd() -> list[str] | None:
    if shutil.which("prettier"):
        return ["prettier"]
    if shutil.which("npx"):
        return ["npx", "--yes", f"prettier@{PRETTIER_VERSION}"]
    return None


def format_html(html: str, *, hint_path: Path | None = None) -> str:
    """Return formatted HTML. On failure returns input unchanged and prints a warning."""
    base = _prettier_cmd()
    if not base:
        print("Warning: prettier/npx not found, HTML left unformatted", file=sys.stderr)
        return html

    args = [*base, "--parser", "html"]
    if PRETTIER_CONFIG.is_file():
        args.extend(["--config", str(PRETTIER_CONFIG)])
    if hint_path is not None:
        args.extend(["--stdin-filepath", str(hint_path)])

    try:
        result = subprocess.run(
            args,
            input=html,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        err = (exc.stderr or exc.stdout or str(exc)).strip()
        print(f"Warning: HTML format failed ({err}), output left unformatted", file=sys.stderr)
        return html

    return result.stdout


def format_html_file(path: Path) -> Path:
    """Format file in place. Returns path."""
    path = path.resolve()
    text = path.read_text(encoding="utf-8")
    formatted = format_html(text, hint_path=path)
    if formatted != text:
        path.write_text(formatted, encoding="utf-8")
        print(f"Formatted {path}")
    return path


def check_html_file(path: Path) -> None:
    """Verify file matches Prettier output. Raises on failure or missing prettier."""
    base = _prettier_cmd()
    if not base:
        raise RuntimeError(
            "Prettier not found. Install prettier or ensure npx is available."
        )

    path = path.resolve()
    args = [*base, "--check", "--parser", "html"]
    if PRETTIER_CONFIG.is_file():
        args.extend(["--config", str(PRETTIER_CONFIG)])
    args.append(str(path))
    subprocess.run(args, check=True)
