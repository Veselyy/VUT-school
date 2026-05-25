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
from dataclasses import dataclass
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

MERMAID_RE = re.compile(
    r'<pre class="mermaid"><code>(.*?)</code></pre>',
    re.DOTALL,
)

H2_COUNT_RE = re.compile(r"<h2\s+id=\"", re.IGNORECASE)

H2_TOPIC_RE = re.compile(
    r'<h2\s+id="([^"]+)">(\d+)\.\s+(.*?)(?:\s+\([^)]*výskyt[^)]*\))?</h2>(.*)',
    re.DOTALL | re.IGNORECASE,
)


@dataclass
class Topic:
    anchor: str
    heading_html: str
    body: str
    freq: int
    toc_title: str
    source_order: int

MATH_SPAN_RE = re.compile(
    r'<span\s+class="math inline">\s*\\\((.+?)\\\)\s*</span>',
    re.DOTALL | re.IGNORECASE,
)
STRONG_RE = re.compile(r"<strong>(.*?)</strong>", re.DOTALL | re.IGNORECASE)
HTML_TAG_RE = re.compile(r"<[^>]+>")

LATEX_UNICODE = {
    "alpha": "α",
    "beta": "β",
    "lambda": "λ",
    "mu": "μ",
    "sigma": "σ",
}


def latex_inline_to_unicode(tex: str) -> str:
    key = tex.strip().lstrip("\\")
    return LATEX_UNICODE.get(key, tex)


def flatten_heading_html(fragment: str) -> str:
    """Pandoc inline HTML (math, strong) → plain text for TOC."""

    def math_repl(match: re.Match[str]) -> str:
        return latex_inline_to_unicode(match.group(1))

    text = MATH_SPAN_RE.sub(math_repl, fragment)
    text = STRONG_RE.sub(r"\1", text)
    text = HTML_TAG_RE.sub("", text)
    return html.unescape(re.sub(r"\s+", " ", text).strip())


def normalize_heading_html(fragment: str) -> str:
    return re.sub(r"\s+", " ", fragment).strip()


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


def escape_mermaid_for_html(code: str) -> str:
    """Escape < > so HTML parser does not break; Mermaid reads decoded text from DOM."""
    return (
        code.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def fix_mermaid_blocks(doc: str) -> str:
    def repl(match: re.Match[str]) -> str:
        content = html.unescape(match.group(1).strip())
        escaped = escape_mermaid_for_html(content)
        return f'<pre class="mermaid">\n{escaped}\n</pre>'

    return MERMAID_RE.sub(repl, doc)


def parse_topics(main_html: str, freqs: list[int], toc_titles: list[str]) -> list[Topic]:
    parts = re.split(r"(?=<h2\s+id=)", main_html)
    topics: list[Topic] = []

    for i, part in enumerate(parts[1:]):
        m = H2_TOPIC_RE.match(part)
        if not m:
            continue
        title_fallback = flatten_heading_html(normalize_heading_html(m.group(3)))
        topics.append(
            Topic(
                anchor=m.group(1),
                heading_html=normalize_heading_html(m.group(3)),
                body=m.group(4).strip(),
                freq=freqs[i] if i < len(freqs) else 0,
                toc_title=toc_titles[i] if i < len(toc_titles) else title_fallback,
                source_order=i,
            )
        )

    return topics


def sort_topics_by_freq(topics: list[Topic]) -> list[Topic]:
    return sorted(topics, key=lambda t: (-t.freq, t.source_order))


def render_toc(topics: list[Topic]) -> str:
    items: list[str] = []
    for rank, topic in enumerate(topics, start=1):
        t = tier(topic.freq)
        items.append(
            f'<li class="tier-{t}"><a href="#{topic.anchor}">'
            f'<span class="toc-num">{rank}.</span>'
            f'<span class="toc-title">{html.escape(topic.toc_title)}</span>'
            f'<span class="toc-freq">{topic.freq}×</span></a></li>'
        )
    return f'<nav id="TOC" role="doc-toc">\n<ul>\n' + "\n".join(items) + "\n</ul>\n</nav>"


def render_articles(topics: list[Topic]) -> str:
    articles: list[str] = []
    for rank, topic in enumerate(topics, start=1):
        t = tier(topic.freq)
        articles.append(
            f'<article class="topic tier-{t}" id="{topic.anchor}">\n'
            f'<header class="topic-header">\n'
            f'<span class="topic-num" aria-hidden="true">{rank}</span>\n'
            f"<h2>{topic.heading_html}</h2>\n"
            f'<span class="freq" title="Výskyt na zkouškách">{topic.freq}×</span>\n'
            f"</header>\n"
            f'<section class="answer" aria-label="Odpověď">\n'
            f"{topic.body}\n"
            f"</section>\n"
            f"</article>\n"
        )
    return "".join(articles)


def apply_layout(doc: str, freqs: list[int], toc_titles: list[str]) -> str:
    doc = fix_mermaid_blocks(doc)

    toc_m = re.search(r'(<nav id="TOC".*?</nav>)', doc, re.DOTALL)
    if not toc_m:
        raise ValueError("Missing TOC in pandoc output (use ## headings for topics)")

    body_m = re.search(r"</nav>\s*(.*)\s*</body>", doc, re.DOTALL)
    if not body_m:
        raise ValueError("Missing body content after TOC")

    topics = parse_topics(body_m.group(1), freqs, toc_titles)
    if len(topics) != len(freqs):
        raise ValueError(f"Parsed {len(topics)} topics, expected {len(freqs)}")

    sorted_topics = sort_topics_by_freq(topics)
    parts = re.split(r"(?=<h2\s+id=)", body_m.group(1))
    intro = parts[0].strip()
    intro_html = f'<div class="intro">{intro}</div>\n' if intro else ""

    main = intro_html + render_articles(sorted_topics)
    tail = doc[body_m.end() :]
    if not tail.lstrip().startswith("</body>"):
        tail = "</body>\n" + tail
    return (
        doc[: toc_m.start()]
        + render_toc(sorted_topics)
        + "\n"
        + main
        + tail
    )


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
    if 'pre class="mermaid"' in doc and MERMAID_SCRIPT.strip() not in doc:
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
    toc_titles = config.get("topic_toc_titles", config.get("topic_titles", []))

    raw = run_pandoc(source, lang)
    n = len(H2_COUNT_RE.findall(raw))
    if n != len(freqs):
        raise ValueError(f"Internal mismatch: {n} topics in HTML, {len(freqs)} frequencies")
    if len(toc_titles) != n:
        raise ValueError(f"Internal mismatch: {n} topics in HTML, {len(toc_titles)} TOC titles")

    layout = apply_layout(raw, freqs, toc_titles)
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
