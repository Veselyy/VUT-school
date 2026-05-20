#!/usr/bin/env python3
"""Scaffold a new subject folder — user edits otazky.md, vyskyty, podklady; build generates the rest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from subject_layout import (
    FREQ_FILE,
    IMAGES_DIR,
    MATERIALS_DIR,
    SOURCE_MD,
    THEME_EXTRA,
    USER_CONFIG,
    write_vyskyty_template,
)

TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parent.parent
TEMPLATE_DIR = TOOL_DIR / "template"


def slugify(code: str) -> str:
    return code.strip().lower()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a new subject study-guide folder")
    parser.add_argument("code", help="Subject code, e.g. IPK (folder name)")
    parser.add_argument("title", help='Page title, e.g. "IPK — Příprava na zkoušku"')
    parser.add_argument(
        "--web",
        action="store_true",
        help="Publish built HTML to web/<slug>/ (for online preview)",
    )
    args = parser.parse_args(argv)

    code = args.code.strip().upper()
    subject_dir = REPO_ROOT / code
    if subject_dir.exists():
        print(f"Error: folder already exists: {subject_dir}", file=sys.stderr)
        return 1

    slug = slugify(code)
    subject_dir.mkdir(parents=True)
    (subject_dir / MATERIALS_DIR).mkdir()
    (subject_dir / MATERIALS_DIR / ".gitkeep").write_text("", encoding="utf-8")
    (subject_dir / IMAGES_DIR).mkdir()
    (subject_dir / IMAGES_DIR / ".gitkeep").write_text("", encoding="utf-8")

    md_template = (TEMPLATE_DIR / SOURCE_MD).read_text(encoding="utf-8")
    md_template = md_template.replace("{{TITLE}}", args.title)
    (subject_dir / SOURCE_MD).write_text(md_template, encoding="utf-8")

    predmet_template = (TEMPLATE_DIR / USER_CONFIG).read_text(encoding="utf-8")
    predmet_template = predmet_template.replace("{{TITLE}}", args.title).replace("{{SLUG}}", slug)
    predmet = json.loads(predmet_template)
    if not args.web:
        predmet.pop("github_pages", None)
    (subject_dir / USER_CONFIG).write_text(
        json.dumps(predmet, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    topics = [(1, "První téma"), (2, "Druhé téma"), (3, "Třetí téma")]
    write_vyskyty_template(subject_dir, topics)

    readme = (TEMPLATE_DIR / "README.md").read_text(encoding="utf-8")
    readme = readme.replace("{{CODE}}", code).replace("{{TITLE}}", args.title).replace("{{SLUG}}", slug)
    (subject_dir / "README.md").write_text(readme, encoding="utf-8")

    build_sh = f"""#!/usr/bin/env sh
cd "$(dirname "$0")/.."
exec python3 tools/study-guide/build.py {code}
"""
    build_script = subject_dir / "build.sh"
    build_script.write_text(build_sh, encoding="utf-8")
    build_script.chmod(0o755)

    print(f"Created {subject_dir}/")
    print()
    print("Ty edituješ:")
    print(f"  {SOURCE_MD}       — otázky a odpovědi (## 1. …)")
    print(f"  {FREQ_FILE}      — výskyty na zkouškách (Název 14x)")
    print(f"  {MATERIALS_DIR}/         — poznámky, PDF")
    print(f"  {IMAGES_DIR}/           — obrázky")
    print(f"  {USER_CONFIG}    — titul, slug pro web/")
    print(f"  {THEME_EXTRA}      — volitelné extra CSS předmětu")
    print()
    print("Build vygeneruje:")
    print("  _build.json, otazky.html, web/<slug>/")
    print()
    print(f"  python3 tools/study-guide/build.py {code}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
