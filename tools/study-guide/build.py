#!/usr/bin/env python3
"""Build study-guide HTML from Markdown (shared theme + auto config from cetnosti.txt)."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from html_format import format_html
from subject_layout import BUILD_CONFIG, USER_CONFIG, sync_build_config
from theme import (
    MERMAID_SCRIPT,
    THEME_HREF_FROM_SUBJECT,
    THEME_HREF_FROM_WEB_SLUG,
    ensure_web_theme_assets,
    stylesheet_links,
    tier,
)

WEB_ROOT = "web"

TOOL_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOL_DIR.parent.parent

TOC_LINK_RE = re.compile(
    r"<li>\s*<a\s+[^>]*href=\"#([^\"]+)\"[^>]*>(.*?)</a>\s*</li>",
    re.DOTALL | re.IGNORECASE,
)

MERMAID_RE = re.compile(
    r'<pre class="mermaid"><code>(.*?)</code></pre>',
    re.DOTALL,
)

H2_COUNT_RE = re.compile(r"<h2\s+id=\"", re.IGNORECASE)


def load_config(subject_dir: Path) -> dict:
    return sync_build_config(subject_dir)


def run_pandoc(md_path: Path, lang: str) -> str:
    result = subprocess.run(
        [
            "pandoc",
            str(md_path),
            "--standalone",
            "--toc",
            "--mathjax",
            "-V",
            f"lang={lang}",
            "-t",
            "html5",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def fix_mermaid_blocks(doc: str) -> str:
    def repl(match: re.Match[str]) -> str:
        content = html.unescape(match.group(1).strip())
        return f'<pre class="mermaid">\n{content}\n</pre>'

    return MERMAID_RE.sub(repl, doc)


def transform_toc(toc_html: str, freqs: list[int]) -> str:
    idx = 0

    def repl_li(match: re.Match[str]) -> str:
        nonlocal idx
        anchor = match.group(1)
        raw = re.sub(r"\s+", " ", match.group(2)).strip()
        m = re.match(r"^(\d+)\.\s+(.+?)(?:\s+\([^)]+\))?$", raw, re.IGNORECASE)
        if not m:
            return match.group(0)
        num, title = m.group(1), m.group(2).strip()
        count = freqs[idx] if idx < len(freqs) else 0
        idx += 1
        t = tier(count)
        return (
            f'<li class="tier-{t}"><a href="#{anchor}">'
            f'<span class="toc-num">{num}.</span> {html.escape(title)} '
            f'<span class="toc-freq">{count}×</span></a></li>'
        )

    return TOC_LINK_RE.sub(repl_li, toc_html)


def wrap_topics(main_html: str, freqs: list[int]) -> str:
    parts = re.split(r"(?=<h2\s+id=)", main_html)
    intro = parts[0].strip()
    if intro:
        intro = f'<div class="intro">{intro}</div>\n'
    articles: list[str] = []

    for i, part in enumerate(parts[1:]):
        m = re.match(
            r'<h2\s+id="([^"]+)">(\d+)\.\s+([^<]+?)(?:\s+\([^)]*výskyt[^)]*\))?</h2>(.*)',
            part,
            re.DOTALL | re.IGNORECASE,
        )
        if not m:
            continue
        tid, num, title, body = m.group(1), m.group(2), m.group(3).strip(), m.group(4)
        count = freqs[i] if i < len(freqs) else 0
        t = tier(count)
        articles.append(
            f'<article class="topic tier-{t}" id="{tid}">\n'
            f'<header class="topic-header">\n'
            f'<span class="topic-num" aria-hidden="true">{num}</span>\n'
            f"<h2>{html.escape(title)}</h2>\n"
            f'<span class="freq" title="Výskyt na zkouškách">{count}×</span>\n'
            f"</header>\n"
            f'<section class="answer" aria-label="Odpověď">\n'
            f"{body.strip()}\n"
            f"</section>\n"
            f"</article>\n"
        )

    return intro + "".join(articles)


def apply_layout(doc: str, freqs: list[int]) -> str:
    doc = fix_mermaid_blocks(doc)

    toc_m = re.search(r'(<nav id="TOC".*?</nav>)', doc, re.DOTALL)
    if not toc_m:
        raise ValueError("Missing TOC in pandoc output (use ## headings for topics)")
    new_toc = transform_toc(toc_m.group(1), freqs)
    doc = doc[: toc_m.start()] + new_toc + doc[toc_m.end() :]

    body_m = re.search(r"</nav>\s*(.*)\s*</body>", doc, re.DOTALL)
    if not body_m:
        raise ValueError("Missing body content after TOC")
    wrapped = wrap_topics(body_m.group(1), freqs)
    return doc[: body_m.start(1)] + wrapped + doc[body_m.end(1) :]


def extra_css_href(subject_dir: Path, config: dict) -> str | None:
    theme_extra = config.get("theme_extra")
    if not theme_extra:
        return None
    if (subject_dir / theme_extra).is_file():
        return theme_extra
    return None


def inject_theme(doc: str, theme_href: str, extra_href: str | None = None) -> str:
    links = stylesheet_links(theme_href, extra_href)
    doc = re.sub(r"<style>.*?</style>", links, doc, count=1, flags=re.DOTALL)
    if MERMAID_SCRIPT.strip() not in doc:
        doc = doc.replace("</body>", f"{MERMAID_SCRIPT}\n</body>")
    return doc


def publish_web(html: str, subject_dir: Path, config: dict) -> None:
    pages = config.get("github_pages")
    if not pages:
        return
    slug = pages.get("slug")
    if not slug:
        raise ValueError("github_pages.slug is required when github_pages is set")
    site_dir = REPO_ROOT / WEB_ROOT / slug
    site_dir.mkdir(parents=True, exist_ok=True)
    (site_dir / "index.html").write_text(html, encoding="utf-8")
    (site_dir / ".nojekyll").write_text("", encoding="utf-8")

    extra = config.get("theme_extra")
    if extra and (subject_dir / extra).is_file():
        shutil.copy2(subject_dir / extra, site_dir / extra)

    images_from = pages.get("images_from")
    if images_from:
        src = subject_dir / images_from
        dst = site_dir / "images"
        if src.is_dir():
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst)
            print(f"Copied images → {dst}")


def build_subject(subject_dir: Path) -> Path:
    subject_dir = subject_dir.resolve()
    config = load_config(subject_dir)
    print(f"Updated {subject_dir / BUILD_CONFIG}")

    source = subject_dir / config["source"]
    output = subject_dir / config["output"]
    lang = config.get("lang", "cs")
    freqs = config["topic_freq"]

    raw = run_pandoc(source, lang)
    n = len(H2_COUNT_RE.findall(raw))
    if n != len(freqs):
        raise ValueError(f"Internal mismatch: {n} topics in HTML, {len(freqs)} frequencies")

    layout = apply_layout(raw, freqs)
    extra_href = extra_css_href(subject_dir, config)

    local_html = format_html(
        inject_theme(layout, THEME_HREF_FROM_SUBJECT, extra_href),
        hint_path=output,
    )
    output.write_text(local_html, encoding="utf-8")
    print(f"Wrote {output}")

    pages = config.get("github_pages")
    if pages and pages.get("slug"):
        ensure_web_theme_assets()
        web_index = REPO_ROOT / WEB_ROOT / pages["slug"] / "index.html"
        web_html = format_html(
            inject_theme(layout, THEME_HREF_FROM_WEB_SLUG, extra_href),
            hint_path=web_index,
        )
        publish_web(web_html, subject_dir, config)
        print(f"Wrote {web_index}")

    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build subject study guide HTML")
    parser.add_argument(
        "subject",
        nargs="?",
        help="Subject folder (e.g. IPP); default: cwd if predmet.json exists",
    )
    args = parser.parse_args(argv)

    if args.subject:
        subject_dir = Path(args.subject)
        if not subject_dir.is_absolute():
            candidate = REPO_ROOT / subject_dir
            if candidate.is_dir():
                subject_dir = candidate
    else:
        subject_dir = Path.cwd()
        if not (subject_dir / USER_CONFIG).is_file() and not (subject_dir / "study.config.json").is_file():
            parser.error("Pass subject folder (e.g. IPP) or run from folder with predmet.json")

    try:
        build_subject(subject_dir)
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
