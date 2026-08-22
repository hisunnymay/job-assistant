#!/usr/bin/env python3
"""Generate and insert a markdown outline (TOC) for a document."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
OUTLINE_HEADING = "## Outline"
OUTLINE_BLOCK_RE = re.compile(
    r"^## Outline\n.*?(?=\n---\n|\n# |\Z)",
    re.MULTILINE | re.DOTALL,
)

# Repeated feature/system subsection labels — skip so the TOC stays scannable.
SKIP_TITLES = {
    "overview",
    "user story",
    "functional requirements",
    "acceptance criteria",
    "goal",
    "potential features",
    "context",
    "current problem",
    "desired outcome",
}


def slugify(text: str) -> str:
    """GitHub-style heading anchor."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def extract_headings(lines: list[str], max_level: int) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    in_fence = False

    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        match = HEADING_RE.match(line)
        if not match:
            continue

        level = len(match.group(1))
        title = match.group(2).strip()
        if level > max_level:
            continue
        normalized = title.lower()
        if normalized == "outline" or normalized in SKIP_TITLES:
            continue
        headings.append((level, title))

    return headings


def build_outline(headings: list[tuple[int, str]], min_level: int) -> str:
    if not headings:
        return f"{OUTLINE_HEADING}\n\n_(No headings found.)_\n"

    lines = [OUTLINE_HEADING, ""]
    for level, title in headings:
        indent = "  " * (level - min_level)
        lines.append(f"{indent}- [{title}](#{slugify(title)})")
    lines.append("")
    return "\n".join(lines)


def find_insert_position(content: str) -> int:
    """Insert outline before the first numbered top-level section, else after front matter."""
    match = re.search(r"^# \d+\. ", content, re.MULTILINE)
    if match:
        return match.start()

    # Fallback: after first horizontal rule following Document Information
    match = re.search(r"^# Document Information\b.*?(?:\n---\n)+", content, re.DOTALL)
    if match:
        return match.end()

    return 0


def upsert_outline(content: str, outline: str) -> str:
    if OUTLINE_BLOCK_RE.search(content):
        return OUTLINE_BLOCK_RE.sub(outline.rstrip() + "\n\n", content, count=1)

    pos = find_insert_position(content)
    before = content[:pos].rstrip() + "\n\n"
    after = content[pos:].lstrip()
    return f"{before}{outline.rstrip()}\n\n---\n\n{after}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Add or refresh a markdown Outline section.")
    parser.add_argument(
        "path",
        nargs="?",
        default="new.md",
        type=Path,
        help="Markdown file to update (default: new.md)",
    )
    parser.add_argument(
        "--max-level",
        type=int,
        default=2,
        choices=range(1, 7),
        metavar="N",
        help="Include headings up to this level (default: 2 = # and ##)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the outline instead of writing the file",
    )
    args = parser.parse_args()

    path: Path = args.path
    if not path.is_file():
        print(f"File not found: {path}", file=sys.stderr)
        return 1

    content = path.read_text(encoding="utf-8")
    lines = content.splitlines()
    headings = extract_headings(lines, max_level=args.max_level)
    if not headings:
        print("No headings found.", file=sys.stderr)
        return 1

    min_level = min(level for level, _ in headings)
    outline = build_outline(headings, min_level)

    if args.dry_run:
        print(outline)
        return 0

    updated = upsert_outline(content, outline)
    path.write_text(updated, encoding="utf-8")
    print(f"Updated outline in {path} ({len(headings)} headings, max level {args.max_level}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
