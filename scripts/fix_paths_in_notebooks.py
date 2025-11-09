#!/usr/bin/env python3
"""
Normalize image paths inside markdown cells of notebooks in book/content/.

Rules:
- /images/...                    -> images/...
- /legal-network-textbook/images -> images/...
- ./images/...                   -> images/...
- ../images/...                  -> images/...

Already-relative paths like images/foo.png remain unchanged.
Handles both Markdown links and HTML <img src="..."> tags by simple string replacements.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

CONTENT_DIR = Path("book/content")


def fix_text(text: str) -> str:
    replacements = [
        ("(/images/", "(images/"),
        ("src=\"/images/", "src=\"images/"),
        ("href=\"/images/", "href=\"images/"),
        ("(/legal-network-textbook/images/", "(images/"),
        ("src=\"/legal-network-textbook/images/", "src=\"images/"),
        ("href=\"/legal-network-textbook/images/", "href=\"images/"),
        ("(./images/", "(images/"),
        ("src=\"./images/", "src=\"images/"),
        ("href=\"./images/", "href=\"images/"),
        ("(../images/", "(images/"),
        ("src=\"../images/", "src=\"images/"),
        ("href=\"../images/", "href=\"images/"),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def process_notebook(nb_path: Path) -> bool:
    changed = False
    with nb_path.open("r", encoding="utf-8") as f:
        nb = json.load(f)

    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        src = cell.get("source", "")
        if isinstance(src, list):
            text = "".join(src)
        else:
            text = str(src)
        new_text = fix_text(text)
        if new_text != text:
            changed = True
            # write back as list of lines to preserve formatting
            cell["source"] = [line + "\n" for line in new_text.splitlines()]

    if changed:
        with nb_path.open("w", encoding="utf-8") as f:
            json.dump(nb, f, ensure_ascii=False, indent=1)
            f.write("\n")
    return changed


def main() -> int:
    if not CONTENT_DIR.exists():
        print(f"Not found: {CONTENT_DIR}", file=sys.stderr)
        return 1
    notebooks = sorted(CONTENT_DIR.glob("*.ipynb"))
    any_changed = False
    for nb in notebooks:
        changed = process_notebook(nb)
        print(("updated" if changed else "ok    "), nb)
        any_changed = any_changed or changed
    return 0 if any_changed or notebooks else 0


if __name__ == "__main__":
    raise SystemExit(main())

