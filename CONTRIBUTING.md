# Contributing

Thanks for helping develop the **OSDR Astrobotany** interactive book! This guide
covers how the project is built and how to add or change content.

## How the book is structured

- The book lives entirely in [`chapters/`](chapters/) — content **and** the sample
  data it loads. Build with `jupyter-book build chapters/`.
- [`chapters/_toc.yml`](chapters/_toc.yml) is the table of contents (parts →
  chapters). [`chapters/_config.yml`](chapters/_config.yml) is the book config.
- CI ([`.github/workflows/static.yml`](.github/workflows/static.yml)) builds the
  book and deploys `chapters/_build/html` to GitHub Pages on every push to `main`.

## Conventions (please follow)

- **Classic Jupyter Book v1** (Sphinx / `jb-book`). ⚠️ Do **not** upgrade to
  Jupyter Book v2 — it's a different MyST/Node tool and is incompatible. Keep
  `jupyter-book<2` in `chapters/requirements.txt`.
- **Notebooks are not executed in CI** (`execute_notebooks: off`); they ship with
  saved outputs. Refresh outputs locally before committing.
- **Many notebooks are generated from `_make_*.py` scripts** — these are the
  reproducible source of truth. To change a generated notebook, edit its
  `_make_*.py`, regenerate, then re-execute (see below). Don't hand-edit the
  generated `.ipynb`.
- **Interactive charts use Plotly** with `pio.renderers.default = "notebook_connected"`
  so they render in the static HTML. Sample large scatters and use
  `render_mode="webgl"` to keep pages light.
- **Functional enrichment** uses the free [g:Profiler](https://biit.cs.ut.ee/gprofiler/)
  API (`athaliana`, `slycopersicum`) — `requests` only, no key.
- Everything is built **live on the OSDR biodata API**; prefer real, reproducible
  queries over committed data dumps.

## Add or update a generated notebook

```bash
cd chapters
python _make_<thing>_notebook.py                 # regenerate the .ipynb
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 OSDR_<thing>.ipynb
cd .. && jupyter-book build chapters/            # rebuild and eyeball _build/html
```

Then add the file to `chapters/_toc.yml` if it's new.

## Runtime environment

- The **book build** only needs `chapters/requirements.txt`.
- **Running the analysis notebooks** needs the fuller stack in
  [`binder/requirements.txt`](binder/requirements.txt) (`scanpy`, `pydeseq2`,
  `openpyxl`, etc.). The 🚀 launch buttons (Binder/Colab) use it.

## Pull requests

1. Branch, commit, and open a PR against `main`.
2. Make sure `jupyter-book build chapters/` succeeds and changed notebooks
   re-execute with **0 errors**.
3. Keep the astrobotany focus and the honest-about-limitations tone.

## A note on data limitations

Be transparent when a dataset's processed data isn't available (e.g. raw-only
amplicon): present what's real, cite published findings where appropriate, and
provide a runnable path to the rest rather than fabricating results.
