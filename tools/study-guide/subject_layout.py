"""Standardní rozložení složky předmětu a synchronizace _build.json."""

from __future__ import annotations

import json
import re
from pathlib import Path

USER_CONFIG = "predmet.json"
BUILD_CONFIG = "_build.json"
SOURCE_MD = "otazky.md"
OUTPUT_HTML = "otazky.html"
FREQ_FILE = "vyskyty.txt"
IMAGES_DIR = "obrazky"
IMAGES_DIR_LEGACY = "podklady_obrazky"
MATERIALS_DIR = "podklady"
THEME_EXTRA = "predmet.css"

# Zpětná kompatibilita se starými názvy
_LEGACY = {
    USER_CONFIG: "study.config.json",
    BUILD_CONFIG: "build.config.json",
    SOURCE_MD: "priprava_na_zkousku.md",
    OUTPUT_HTML: "priprava_na_zkousku.html",
    FREQ_FILE: "cetnosti.txt",
    THEME_EXTRA: "styly.css",
}

H2_MD_RE = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.MULTILINE)
FREQ_LINE_RE = re.compile(r"^(.+?)\s+(\d+)x\s*$", re.IGNORECASE)


def resolve_path(subject_dir: Path, primary: str, legacy_key: str) -> Path:
    primary_path = subject_dir / primary
    if primary_path.exists():
        return primary_path
    legacy = subject_dir / _LEGACY[legacy_key]
    return legacy if legacy.exists() else primary_path


def parse_md_topics(md_text: str) -> list[tuple[int, str]]:
    topics: list[tuple[int, str]] = []
    for m in H2_MD_RE.finditer(md_text):
        topics.append((int(m.group(1)), m.group(2).strip()))
    return topics


def parse_vyskyty(text: str) -> list[int]:
    counts: list[int] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = FREQ_LINE_RE.match(line)
        if not m:
            raise ValueError(f"Invalid line in {FREQ_FILE}: {line!r} (expected: Název otázky 14x)")
        counts.append(int(m.group(2)))
    return counts


def resolve_images_dir(subject_dir: Path) -> str:
    if (subject_dir / IMAGES_DIR).is_dir():
        return IMAGES_DIR
    if (subject_dir / IMAGES_DIR_LEGACY).is_dir():
        return IMAGES_DIR_LEGACY
    return IMAGES_DIR


def load_user_config(subject_dir: Path) -> dict:
    path = resolve_path(subject_dir, USER_CONFIG, USER_CONFIG)
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing {subject_dir / USER_CONFIG}. Create with new_subject.py."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def load_previous_freqs(subject_dir: Path) -> list[int] | None:
    path = resolve_path(subject_dir, BUILD_CONFIG, BUILD_CONFIG)
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    freqs = data.get("topic_freq")
    return freqs if isinstance(freqs, list) else None


def resolve_topic_freqs(subject_dir: Path, topic_count: int) -> list[int]:
    freq_path = resolve_path(subject_dir, FREQ_FILE, FREQ_FILE)
    if freq_path.is_file():
        counts = parse_vyskyty(freq_path.read_text(encoding="utf-8"))
        if len(counts) != topic_count:
            raise ValueError(
                f"{FREQ_FILE} has {len(counts)} lines but {SOURCE_MD} has {topic_count} topics (##)."
            )
        return counts

    previous = load_previous_freqs(subject_dir)
    if previous and len(previous) == topic_count:
        return previous

    return [1] * topic_count


def sync_build_config(subject_dir: Path) -> dict:
    study = load_user_config(subject_dir)
    md_path = resolve_path(subject_dir, SOURCE_MD, SOURCE_MD)
    if not md_path.is_file():
        raise FileNotFoundError(f"Missing {subject_dir / SOURCE_MD}")

    topics = parse_md_topics(md_path.read_text(encoding="utf-8"))
    if not topics:
        raise ValueError(f"No ## topics found in {SOURCE_MD}")

    nums = [n for n, _ in topics]
    if nums != list(range(1, len(topics) + 1)):
        raise ValueError(f"{SOURCE_MD}: topic numbers must be 1..{len(topics)} without gaps")

    freqs = resolve_topic_freqs(subject_dir, len(topics))
    images_from = resolve_images_dir(subject_dir)

    config: dict = {
        "generated": True,
        "title": study.get("title", subject_dir.name),
        "lang": study.get("lang", "cs"),
        "source": SOURCE_MD,
        "output": OUTPUT_HTML,
        "topic_freq": freqs,
        "topic_titles": [title for _, title in topics],
    }

    pages = study.get("github_pages") or study.get("web")
    if pages:
        slug = pages.get("slug") if isinstance(pages, dict) else pages
        config["github_pages"] = {
            "slug": slug or subject_dir.name.lower(),
            "images_from": images_from,
        }

    extra_path = resolve_path(subject_dir, THEME_EXTRA, THEME_EXTRA)
    if extra_path.is_file():
        config["theme_extra"] = THEME_EXTRA

    (subject_dir / BUILD_CONFIG).write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return config


def write_vyskyty_template(
    subject_dir: Path, topics: list[tuple[int, str]], freqs: list[int] | None = None
) -> None:
    lines = []
    for i, (_, title) in enumerate(topics):
        count = freqs[i] if freqs and i < len(freqs) else 1
        lines.append(f"{title} {count}x")
    (subject_dir / FREQ_FILE).write_text("\n".join(lines) + "\n", encoding="utf-8")
