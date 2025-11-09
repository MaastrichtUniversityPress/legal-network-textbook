#!/usr/bin/env python3
"""
Conservatively update book/_config.yml using metadata in TO MIGRATE/public/nbconfig.json:
- Set top-level author to comma-separated authors.
- Set sphinx.config.html_theme_options.logo.text to presentation.title.
- Optionally set logo images to figures/um-logo.png if present.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path('.')
CONFIG_PATH = ROOT / 'book' / '_config.yml'
NBCONFIG_PATH = ROOT / 'TO MIGRATE' / 'public' / 'nbconfig.json'


def main() -> int:
    cfg = CONFIG_PATH.read_text(encoding='utf-8')
    nb = json.loads(NBCONFIG_PATH.read_text(encoding='utf-8'))
    pres = nb.get('presentation', {})
    title = str(pres.get('title', '')).strip() or None
    authors = pres.get('authors', [])
    authors_str = ', '.join(map(str, authors)) if authors else None

    # Update author line (top-level)
    if authors_str:
        # Match a line starting with author: ... and replace the whole line
        if re.search(r'^author:\s*.*$', cfg, flags=re.MULTILINE):
            cfg = re.sub(r'^author:\s*.*$', f'author: {authors_str}', cfg, flags=re.MULTILINE)

    # Update logo text within html_theme_options.logo.text
    if title:
        # Locate the 'logo:' block and replace text:
        cfg = re.sub(
            r'(logo:\s*\n(?:[\s\S]*?)\n\s*text:\s*)(.*)$',
            lambda m: m.group(1) + title,
            cfg,
            flags=re.MULTILINE
        )
        # Fallback: directly replace a line with 'text: ...' under html_theme_options
        cfg = re.sub(r'(^\s*text:\s*).*$','\\g<1>'+title, cfg, flags=re.MULTILINE)

    # If figures/um-logo.png exists, point image_light and image_dark to it
    um_logo = Path('book/figures/um-logo.png')
    if um_logo.exists():
        cfg = re.sub(r'(^\s*image_light:\s*).*$','\\g<1>' + 'figures/um-logo.png', cfg, flags=re.MULTILINE)
        cfg = re.sub(r'(^\s*image_dark:\s*).*$','\\g<1>' + 'figures/um-logo.png', cfg, flags=re.MULTILINE)

    CONFIG_PATH.write_text(cfg, encoding='utf-8')
    print('Updated _config.yml with title and authors.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

