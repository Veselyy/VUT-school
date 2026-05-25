"""Shared HTML theme for all subject study guides."""

from __future__ import annotations

import html
import shutil
from pathlib import Path

TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parent.parent
THEME_CSS = TOOL_DIR / "theme.css"

# Relativní cesty z <KÓD>/otazky.html nebo web/<slug>/index.html
THEME_HREF_FROM_SUBJECT = "../tools/study-guide/theme.css"
THEME_HREF_FROM_WEB_SLUG = "../assets/study-guide/theme.css"

WEB_THEME_ASSETS = REPO_ROOT / "web" / "assets" / "study-guide" / "theme.css"


def tier(count: int) -> str:
    if count >= 7:
        return "high"
    if count >= 3:
        return "medium"
    return "low"


def ensure_web_theme_assets() -> Path:
    """Kopie globálního theme.css pro web/ (GitHub Pages)."""
    WEB_THEME_ASSETS.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(THEME_CSS, WEB_THEME_ASSETS)
    return WEB_THEME_ASSETS


def stylesheet_links(theme_href: str, extra_href: str | None = None) -> str:
    lines = [f'  <link rel="stylesheet" href="{html.escape(theme_href)}" />']
    if extra_href:
        lines.append(f'  <link rel="stylesheet" href="{html.escape(extra_href)}" />')
    return "\n".join(lines)


def document_head(
    title: str,
    lang: str = "cs",
    extra_head: str = "",
    theme_href: str = THEME_HREF_FROM_SUBJECT,
    extra_css_href: str | None = None,
) -> str:
    return f"""<!DOCTYPE html>
<html lang="{html.escape(lang)}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
{stylesheet_links(theme_href, extra_css_href)}
{extra_head}</head>
"""


def page_header(title: str, subtitle: str = "") -> str:
    sub_html = (
        f'\n    <p class="subtitle">{subtitle}</p>'
        if subtitle
        else ""
    )
    return f"""  <header class="page-header">
    <h1 class="title">{html.escape(title)}</h1>{sub_html}
  </header>"""


def intro_block(text: str) -> str:
    return f'  <div class="intro">{text}</div>\n'


def howto_block(text: str) -> str:
    return f'  <p class="howto">{text}</p>\n'


def footer_block(text: str) -> str:
    return f"  <footer>\n    {text}\n  </footer>\n"


# Embed pattern: https://stackoverflow.com/a/79725105 (dennuguyen, CC BY-SA 4.0)
MERMAID_SCRIPT = """
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
</script>
"""
