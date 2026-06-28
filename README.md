# OSDR Interactive FAIR Notebook

An interactive [Jupyter Book](https://jupyterbook.org/) that turns NASA's
**Open Science Data Repository (OSDR)** into an explorable, publication-ready
tool — combining a **standardised FAIR assessment** of every dataset with
**interactive data visualisation and data storytelling**, built directly on the
public [OSDR biodata API](https://visualization.osdr.nasa.gov/biodata/api/).

- **Repository:** https://github.com/dr-richard-barker/OSDR_juypter_book.io
- **Book source:** [`chapters/`](chapters/) (built with classic Jupyter Book v1)
- **API backbone:** `https://visualization.osdr.nasa.gov/biodata/api/v2/`
- **Author:** Richard Barker and the OSDR team

---

## 🎯 Project goals

1. **Make OSDR data discoverable.** Let anyone see *what* data is available
   across the ~640 OSDR (GeneLab + ALSDA) studies, at a glance.
2. **Assess FAIRness, transparently.** Score every dataset against concrete,
   reproducible **F**indable / **A**ccessible / **I**nteroperable / **R**eusable
   sub-criteria derived from the metadata the API actually exposes — and surface
   the gaps.
3. **Visualise and tell stories.** Provide interactive charts and drill-downs so
   researchers, submitters, and the public can explore and narrate OSDR science.
4. **Be a living publication tool.** A reproducible, auto-deploying book that
   integrates *all* aspects of OSDR data and can be cited and re-run over time.

---

## 📦 Deliverables

### Status legend
✅ done · 🚧 in progress · 📋 planned

### Phase 1 — Reproducible, auto-deploying book *(✅ done locally; awaiting push)*

| Deliverable | File | Status |
| --- | --- | --- |
| Valid book configuration | [`chapters/_config.yml`](chapters/_config.yml) | ✅ |
| Valid table of contents (`parts:` format, real files only) | [`chapters/_toc.yml`](chapters/_toc.yml) | ✅ |
| Real landing page | [`chapters/intro.md`](chapters/intro.md) | ✅ |
| Pinned, complete dependencies (`jupyter-book<2` + viz libs) | [`chapters/requirements.txt`](chapters/requirements.txt) | ✅ |
| CI that actually **builds** the book and deploys to GitHub Pages | [`.github/workflows/static.yml`](.github/workflows/static.yml) | ✅ |
| Existing intro chapters + demo notebooks wired into the book | [`chapters/`](chapters/) | ✅ |

### Phase 2 — The publication tool *(🚧 started)*

| Deliverable | File | Status |
| --- | --- | --- |
| **Live FAIR assessment** notebook (scorecard + interactive Plotly charts) | [`chapters/OSDR_FAIR_assessment.ipynb`](chapters/OSDR_FAIR_assessment.ipynb) | ✅ |
| FAIR notebook generator (reproducible source of truth) | [`chapters/_make_fair_notebook.py`](chapters/_make_fair_notebook.py) | ✅ |
| Dataset / assay **drill-down explorer** (browse assays, samples, data columns) | _tbd_ | 📋 |
| **Data storytelling** views (FAIR × organism × factor type) | _tbd_ | 📋 |
| Per-dataset, actionable "improve your FAIRness" reports for submitters | _tbd_ | 📋 |
| Scheduled full-repository FAIR scoring (track maturity over time) | _tbd_ | 📋 |

### Phase 3 — Cleanup & publication *(📋 planned)*

| Deliverable | Status |
| --- | --- |
| Remove conflicting leftovers (stale root `*.html`, old root `_config.yml`/`_toc.yml`, broken `.readthedocs.yaml`) | 📋 |
| Enable GitHub Pages (Settings → Pages → Source: **GitHub Actions**) | 📋 |
| `CITATION.cff` + Zenodo DOI for the book | 📋 |
| Contributor guide | 📋 |

---

## 🔑 Key findings so far

- OSDR currently exposes **640 datasets** through the biodata API.
- The API metadata has **no explicit licence field**, so FAIR criterion
  **R1.1 (licence)** fails repository-wide — a real, actionable reusability gap.

---

## 🏗️ Architecture & conventions

- **Book root is [`chapters/`](chapters/)** — all content *and* sample data live
  there, so notebook relative paths work. Build with `jupyter-book build chapters/`.
- **Classic Jupyter Book v1** (Sphinx / `jb-book` TOC format). ⚠️ Jupyter Book
  **v2 is a different, MyST/Node-based tool and is NOT compatible** — keep
  `jupyter-book<2` pinned.
- **Notebooks are NOT executed in CI** (`execute_notebooks: off`). They ship
  with saved outputs; refresh them locally (see below). This keeps builds fast
  and green even though some notebooks hit the live API / large data files.
- **Interactive charts use Plotly** with the `notebook_connected` renderer so
  they survive in the static book HTML.

---

## 🚀 Build & develop locally

```bash
# 1. Install dependencies (classic Jupyter Book + viz libs)
pip install -r chapters/requirements.txt

# 2. Build the book
jupyter-book build chapters/

# 3. Open the result
#    chapters/_build/html/index.html
```

### Refresh the FAIR assessment with live data

```bash
cd chapters
python _make_fair_notebook.py            # regenerate the notebook source
jupyter nbconvert --to notebook --execute --inplace OSDR_FAIR_assessment.ipynb
# edit MAX_DATASETS in the generator (set to None) to score all ~640 datasets
```

Then rebuild the book to embed the new outputs.

---

## 🌐 The OSDR biodata API

Base URL: `https://visualization.osdr.nasa.gov/biodata/api/v2/`

| Purpose | Endpoint |
| --- | --- |
| List all datasets | `/v2/datasets/` |
| Dataset metadata | `/v2/dataset/{ACCESSION}/` |
| Assays in a dataset | `/v2/dataset/{ACCESSION}/assays/` |
| Files in a dataset | `/v2/dataset/{ACCESSION}/files/` |
| Query metadata across studies | `/v2/query/metadata/` |
| Query data columns | `/v2/query/data/` |

---

## 📂 Repository layout

```
chapters/                     # the Jupyter Book (build target)
  _config.yml                 # book settings
  _toc.yml                    # table of contents
  intro.md                    # landing page
  requirements.txt            # build + runtime dependencies
  OSDR_FAIR_assessment.ipynb  # Phase 2: live FAIR assessment
  _make_fair_notebook.py      # generator for the FAIR notebook
  *.md                        # intro chapters (API, viz portal, RadLab, …)
  *.ipynb                     # demo / analysis notebooks
  *.csv, *.bam, …             # sample data used by the notebooks
.github/workflows/static.yml  # CI: build + deploy to GitHub Pages
```

---

## 🗺️ Roadmap (next up)

1. Push Phase 1 + 2 and enable GitHub Pages.
2. Build the dataset/assay **drill-down explorer**.
3. Add **data storytelling** views joining FAIR scores with organism / factor type.
4. Phase 3 cleanup + DOI.

---

## 📄 Licence

See [`LICENSE`](LICENSE). Built on NASA OSDR open data.
