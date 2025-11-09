#!/usr/bin/env python3
"""
Update book/_toc.yml using TO MIGRATE/public/nbconfig.json.

- Keeps existing 'format:' and 'root:' header lines if present.
- Replaces the 'parts:' section with two parts: Chapters and Appendices.
- Only includes entries that exist at book/content/<name>.ipynb.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path('.')
TOC_PATH = ROOT / 'book' / '_toc.yml'
NBCONFIG_PATH = ROOT / 'TO MIGRATE' / 'public' / 'nbconfig.json'
CONTENT_DIR = ROOT / 'book' / 'content'


def extract_header_lines(text: str) -> tuple[str, str]:
    fmt = None
    root = None
    for line in text.splitlines():
        if fmt is None and re.match(r"^\s*format:\s*", line):
            fmt = line.strip()
        if root is None and re.match(r"^\s*root:\s*", line):
            root = line.strip()
        if fmt and root:
            break
    if fmt is None:
        fmt = 'format: jb-book'
    if root is None:
        root = 'root: intro.md'
    return fmt, root


def main() -> int:
    toc_text = TOC_PATH.read_text(encoding='utf-8')
    fmt, root = extract_header_lines(toc_text)

    nbconfig = json.loads(NBCONFIG_PATH.read_text(encoding='utf-8'))
    order = nbconfig.get('notebooks', [])

    # Gather present notebooks by prefix for later reconciliation
    present = sorted([p.stem for p in CONTENT_DIR.glob('*.ipynb')])
    present_set = set(present)

    chapters: list[str] = []
    appendices: list[str] = []
    deferred_appendices: list[str] = []  # mapped items to append after processing order
    added: set[str] = set()
    missing: list[str] = []

    def add_item(name: str, to: str):
        if name in added:
            return
        if name not in present_set:
            return
        if to == 'chapters':
            chapters.append(name)
        else:
            appendices.append(name)
        added.add(name)

    for name in order:
        p = CONTENT_DIR / f"{name}.ipynb"
        if p.exists():
            if name.startswith('Appendix_'):
                add_item(name, 'appendices')
            else:
                add_item(name, 'chapters')
            continue

        # Hybrid mapping for known mismatches
        mapped = False
        if name == 'Chapter_5_Data_Collection_and_Preparation':
            # Prefer to insert both available chapters in intended slot if present
            add_item('Chapter_5_Estimation_and_embeddings', 'chapters')
            add_item('Chapter_6_Data_Collection_and_Preparation', 'chapters')
            mapped = True
        elif name == 'Chapter_6_Software':
            # Treat software as an appendix in this repo; defer to keep appendix order
            if 'Appendix_6_Software' in present_set and 'Appendix_6_Software' not in added:
                deferred_appendices.append('Appendix_6_Software')
            mapped = True
        elif name == 'Chapter_7_Plotting':
            # No chapter 7; appendix 5 plotting already handled via actual entry
            mapped = True  # effectively drop

        if not mapped:
            missing.append(name)

    # Append any remaining present notebooks not already added, maintaining grouping
    for name in present:
        if name in added:
            continue
        if name.startswith('Appendix_'):
            add_item(name, 'appendices')
        elif name.startswith('Chapter_'):
            add_item(name, 'chapters')

    # Finally, append deferred appendix mappings (e.g., Appendix_6_Software)
    for name in deferred_appendices:
        if name not in added and name in present_set:
            add_item(name, 'appendices')

    parts_lines = []
    parts_lines.append('parts:')
    if chapters:
        parts_lines.append('  - caption: Chapters')
        parts_lines.append('    chapters:')
        for name in chapters:
            parts_lines.append(f'    - file: content/{name}.ipynb')
    if appendices:
        parts_lines.append('  - caption: Appendices')
        parts_lines.append('    chapters:')
        for name in appendices:
            parts_lines.append(f'    - file: content/{name}.ipynb')

    new_toc = '\n'.join([
        fmt,
        root,
        '',
        *parts_lines,
        '',
    ])
    TOC_PATH.write_text(new_toc, encoding='utf-8')

    if missing:
        print('Note: The following items from nbconfig.json were not found and were skipped:')
        for m in missing:
            print(' -', m)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
