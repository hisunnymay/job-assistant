#!/usr/bin/env python3
"""Combine summary_*.md files into one markdown document with an outline."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SUMMARY_RE = re.compile(r"^summary_(\d+)\.md$", re.IGNORECASE)
OUTLINE_HEADING = "## Outline"

# Assign heading depth from section numbers, not the original # count.
# Source files mix `# 2.2` with `## 2.1`; the outline then looks uneven.
MAJOR_SECTION_RE = re.compile(
    r"^\d+\.\s+(Purpose of This Review|Starting Point|Major Turning Point|"
    r"Process Retrospective|Final Learning Summary)\b"
)
SUBSECTION_RE = re.compile(r"^\d+\.\d+\b")
LEARNING_RE = re.compile(r"^Learning \d+\b")
REFLECTION_RE = re.compile(r"^Reflection$")
PHASE_RE = re.compile(r"^Phase \d+:")
PRINCIPLE_RE = re.compile(r"^Principle \d+$")
CONCLUSION_RE = re.compile(r"^Overall Retrospective Conclusion$")
DOC_TITLE_RE = re.compile(r"^PRD Creation Retrospective")

# Repeated generic labels that would clutter the TOC.
SKIP_TITLES = {
    "outline",
    "goal",
    "overview",
    "context",
    "output:",
    "output",
    "before:",
    "before",
    "after:",
    "after",
    "how to improve",
    "hypothesis",
    "observable behavior",
    "metric",
    "interpretation",
    "question:",
    "question",
}


def slugify(text: str) -> str:
    """GitHub-style heading anchor."""
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_]+", "-", text)
    return text.strip("-")


def unique_slug(title: str, used: Counter[str]) -> str:
    base = slugify(title) or "section"
    used[base] += 1
    if used[base] == 1:
        return base
    return f"{base}-{used[base] - 1}"


def find_summary_files(directory: Path) -> list[Path]:
    files = []
    for path in directory.iterdir():
        match = SUMMARY_RE.match(path.name)
        if match and path.is_file():
            files.append((int(match.group(1)), path))
    files.sort(key=lambda item: item[0])
    return [path for _, path in files]


def structural_level(title: str) -> int | None:
    """Return a fixed heading level for numbered/named structure, else None."""
    if DOC_TITLE_RE.match(title):
        return 1
    if MAJOR_SECTION_RE.match(title):
        return 2
    if (
        SUBSECTION_RE.match(title)
        or LEARNING_RE.match(title)
        or REFLECTION_RE.match(title)
        or PRINCIPLE_RE.match(title)
        or CONCLUSION_RE.match(title)
    ):
        return 3
    if PHASE_RE.match(title):
        return 4
    return None


def normalize_headings(content: str) -> str:
    """Rewrite heading markers so siblings share the same depth."""
    lines = content.splitlines()
    in_fence = False
    last_orig = 1
    last_new = 1
    last_struct_new = 1
    out: list[str] = []

    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue

        match = HEADING_RE.match(line)
        if not match:
            out.append(line)
            continue

        orig = len(match.group(1))
        title = match.group(2).strip()
        fixed = structural_level(title)
        if fixed is not None:
            new = fixed
            last_struct_new = new
        elif orig > last_orig:
            new = min(6, last_new + 1)
        elif orig == last_orig:
            new = last_new
        else:
            new = max(last_struct_new + 1, last_new - (last_orig - orig))
        out.append(f"{'#' * new} {title}")
        last_orig = orig
        last_new = new

    return "\n".join(out) + "\n"


def combine_summaries(files: list[Path]) -> str:
    parts: list[str] = []
    for path in files:
        text = path.read_text(encoding="utf-8").strip()
        if text:
            parts.append(text)
    return normalize_headings("\n\n---\n\n".join(parts) + "\n")


def extract_headings(
    lines: list[str], max_level: int, skip_first_h1: bool = True
) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    in_fence = False
    skipped_title = False

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
        if skip_first_h1 and not skipped_title and level == 1:
            skipped_title = True
            continue
        if level > max_level:
            continue
        if title.lower() in SKIP_TITLES:
            continue
        headings.append((level, title))

    return headings


def build_outline(headings: list[tuple[int, str]]) -> str:
    if not headings:
        return f"{OUTLINE_HEADING}\n\n_(No headings found.)_\n"

    min_level = min(level for level, _ in headings)
    used: Counter[str] = Counter()
    lines = [OUTLINE_HEADING, ""]
    for level, title in headings:
        indent = "  " * (level - min_level)
        lines.append(f"{indent}- [{title}](#{unique_slug(title, used)})")
    lines.append("")
    return "\n".join(lines)


def insert_outline(content: str, outline: str) -> str:
    """Place the outline after the first top-level title, or at the top."""
    match = re.search(r"^# .+$", content, re.MULTILINE)
    if not match:
        return f"{outline.rstrip()}\n\n---\n\n{content.lstrip()}"

    end = match.end()
    before = content[:end].rstrip()
    after = content[end:].lstrip()
    if after.startswith("---"):
        after = after[3:].lstrip()
    return f"{before}\n\n{outline.rstrip()}\n\n---\n\n{after}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge summary_*.md files and generate a markdown outline."
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path("."),
        help="Directory containing summary_*.md files (default: current directory)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("summaries.md"),
        help="Combined markdown output path (default: summaries.md)",
    )
    parser.add_argument(
        "--max-level",
        type=int,
        default=3,
        choices=range(1, 7),
        metavar="N",
        help="Include headings up to this level in the outline (default: 3)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the outline and do not write the output file",
    )
    args = parser.parse_args()

    source_dir: Path = args.source_dir
    files = find_summary_files(source_dir)
    if not files and source_dir == Path("."):
        fallback = Path("history/summaries")
        files = find_summary_files(fallback)
        if files:
            source_dir = fallback
    if not files:
        print(f"No summary_*.md files found in {args.source_dir}", file=sys.stderr)
        return 1

    combined = combine_summaries(files)
    headings = extract_headings(combined.splitlines(), max_level=args.max_level)
    outline = build_outline(headings)
    document = insert_outline(combined, outline)

    if args.dry_run:
        print(outline)
        print(
            f"Would write {args.output} from {len(files)} files "
            f"({len(headings)} outline headings).",
            file=sys.stderr,
        )
        return 0

    args.output.write_text(document, encoding="utf-8")
    names = ", ".join(path.name for path in files)
    print(
        f"Wrote {args.output} from {len(files)} files ({names}); "
        f"outline has {len(headings)} headings (max level {args.max_level})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
