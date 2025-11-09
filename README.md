# Legal Network Analysis

An open textbook on legal network analysis with hands-on, executable Jupyter notebooks. This repository hosts the source of the book, built with TeachBooks/JupyterBook, and includes all notebooks, images, and supporting files needed to reproduce the content.

<img alt="Maastricht University" src="book/figures/um-logo.png" width="160" />

## Metadata
- Title: Legal Network Analysis
- Authors: Gustavo Arosemena, Gijs van Dijck, Roland Moerland
- Institution: Maastricht University — Law and Tech Lab
- Place: Maastricht
- Version: 0.1
- Date: November 1, 2023

If published via GitHub Pages, the book will be available at: `https://<username-or-org>.github.io/legal-network-textbook/`.

## Repository Structure
- `book/`: JupyterBook/TeachBooks source
  - `_config.yml`: Book configuration (theme, metadata, options)
  - `_toc.yml`: Table of contents (generated from `nbconfig.json`)
  - `content/`: All chapter/appendix notebooks and assets
    - `*.ipynb`: Notebooks for Chapters and Appendices
    - `images/`: Image assets (mirrors original structure)
    - `data/`, `src/`: Supporting datasets and code
  - `figures/`: Site assets (favicon, logo)
- `scripts/`: Migration and maintenance helpers
  - `update_toc_from_nbconfig.py`: Regenerate `_toc.yml` from `nbconfig.json` (hybrid mapping)
  - `fix_paths_in_notebooks.py`: Normalize image paths inside notebooks
- `TO MIGRATE/`: Read-only copy of the original Vue/Vite app (kept as backup)

## Getting Started

Build locally using either TeachBooks or JupyterBook:

```
pip install -r requirements.txt

# Option A (TeachBooks)
teachbooks build book

# Option B (JupyterBook)
jupyter-book build book
```

Open `book/_build/html/index.html` in your browser to preview locally.

To publish on GitHub Pages, enable Pages for this repo (source: GitHub Actions) and let the included workflow build and deploy the site.

## Content Outline

Chapters
- Chapter_1_Introduction
- Chapter_2_Key_Concepts
- Chapter_3_Centrality
- Chapter_4_Communities
- Chapter_5_Estimation_and_embeddings
- Chapter_6_Data_Collection_and_Preparation

Appendices
- Appendix_1_Getting_data_in
- Appendix_2_Text_Similarity_Net
- Appendix_3_Normalization
- Appendix_4_Vector_Scaling
- Appendix_5_Plotting
- Appendix_6_Software

The full list and order are maintained in `book/_toc.yml` and generated from `TO MIGRATE/public/nbconfig.json`.

## Migration & Maintenance

This repo was migrated from an older Vue/Vite app. All notebooks and assets now live under `book/content/` so that relative links remain valid.

- Regenerate ToC from the original outline:
  - `python3 scripts/update_toc_from_nbconfig.py`
  - Applies a hybrid mapping to reconcile name mismatches without renaming files.
- Normalize image paths inside notebooks:
  - `python3 scripts/fix_paths_in_notebooks.py`
- Additional notes and troubleshooting: see `book/README.md` (covers common ToC mismatches, image/data path issues, and build errors).

## License and Reuse

Except where otherwise noted, content is available under the [CC BY 4.0 License](https://creativecommons.org/licenses/by/4.0/). See `LICENSE` in this repository.

## Citation

If you use this work, please cite it. See `CITATION.cff` for citation metadata.

## Contributing

Issues and pull requests are welcome. For small fixes, feel free to open a PR. For larger changes, please open an issue first to discuss scope and approach.

