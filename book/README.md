# Migration Notes (TeachBooks)

This repository was migrated from a Vue/Vite app to a TeachBooks/JupyterBook structure. The notebooks and assets now live under `book/content/` to preserve relative paths.

## Name Mapping (Hybrid)

We keep `TO MIGRATE/public/nbconfig.json` as the guide but map a few names to the actual files to avoid renaming notebooks:

- Chapter_5_Data_Collection_and_Preparation → Chapter_5_Estimation_and_embeddings + Chapter_6_Data_Collection_and_Preparation
- Chapter_6_Software → Appendix_6_Software
- Chapter_7_Plotting → (removed; no matching file)

Everything else is included as-is from `nbconfig.json` when a corresponding `book/content/<name>.ipynb` exists.

## ToC Generation

- Generate/refresh the book ToC from `nbconfig.json`:
  - `python3 scripts/update_toc_from_nbconfig.py`
  - This keeps `format:` and `root:` from the existing `_toc.yml` and rewrites the `parts:` section.
- The script prints any entries from `nbconfig.json` that don’t exist as notebooks in `book/content/`.

## Image Path Normalization

Notebooks reference images under `book/content/images/` using relative paths `images/...`.

- Normalize image links in markdown cells:
  - `python3 scripts/fix_paths_in_notebooks.py`
  - Rewrites `/images/...`, `/legal-network-textbook/images/...`, `./images/...`, and `../images/...` to `images/...`.

## Common Issues & Debugging

- Missing ToC entries:
  - Symptom: script prints skipped items or JupyterBook warns about missing files.
  - Fix: ensure a matching file exists at `book/content/<name>.ipynb`, or adjust `nbconfig.json` to the filename you actually have, then rerun the ToC script.

- Wrong order vs. reality:
  - Symptom: book order differs from `nbconfig.json`.
  - Fix: edit `TO MIGRATE/public/nbconfig.json` and run `python3 scripts/update_toc_from_nbconfig.py` again.

- Images not rendering:
  - Symptom: broken images after migration.
  - Checks:
    - Image files under `book/content/images/` exist (mirrors old `public/images` tree).
    - Notebook markdown uses `images/<subdir>/file.png` (relative), not absolute paths.
  - Fix: run `scripts/fix_paths_in_notebooks.py` and re-open the notebook.

- Data/aux files not found:
  - Symptom: code cells refer to `data/...` or `src/...` and fail when executed.
  - Fix: verify `book/content/data/` and `book/content/src/` exist and paths are relative from the notebook directory.

- Build errors referencing _toc.yml:
  - Symptom: JupyterBook build fails due to missing files in the ToC.
  - Fix: (1) regenerate ToC, (2) remove or rename problematic entries, or (3) add the missing notebook(s) into `book/content/`.

## Logo

`book/_config.yml` points `html_theme_options.logo.image_{light,dark}` to `book/figures/um-logo.png`, and the same file is also available under `book/content/images/` for in-notebook references.

## Useful Commands

- Refresh ToC: `python3 scripts/update_toc_from_nbconfig.py`
- Normalize image paths: `python3 scripts/fix_paths_in_notebooks.py`
- Quick check for non-relative image links: `rg -n "\((/|\./|\.\./)images/|src=\"(/|\./|\.\./)images/" book/content/*.ipynb`

