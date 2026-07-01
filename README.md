# OSDR Astrobotany — Interactive FAIR & Multi-omics Notebook

An interactive [Jupyter Book](https://jupyterbook.org/) that turns NASA's
**Open Science Data Repository (OSDR)** into an explorable, publication-ready
**astrobotany** tool — a standardised **FAIR assessment** of the repository plus
**interactive visualisation, data storytelling, and multi-omic integration**,
all built live on the public
[OSDR biodata API](https://visualization.osdr.nasa.gov/biodata/api/).

- **Repository:** https://github.com/dr-richard-barker/OSDR_juypter_book.io
- **Book source:** [`chapters/`](chapters/) (classic Jupyter Book v1)
- **API backbone:** `https://visualization.osdr.nasa.gov/biodata/api/v2/`
- **Author:** Richard Barker and the OSDR team

> **This README is the project's source of truth for status** — every goal, what's
> achieved (✅), partial (⚠️), and outstanding (📋). Keep it current.

---

## 🎯 Goals & where we stand

| # | Goal | Status |
| --- | --- | --- |
| 1 | **Make OSDR data discoverable** — see what data exists across the ~640 studies | ✅ achieved |
| 2 | **Assess FAIRness transparently** — score every dataset on reproducible F/A/I/R criteria, surface gaps | ✅ achieved |
| 3 | **Visualise & tell data stories** — interactive charts, drill-downs, cross-dataset narratives | ✅ achieved |
| 4 | **Be a living, reproducible publication tool** — auto-deploying, re-runnable, citable | ⚠️ build/deploy ✅, cleanup ✅, `CITATION.cff` ✅; **only Zenodo DOI pending** |
| 5 | **Astrobotany theme** — plant-focused, *zero residual rodent* analysis | ✅ achieved |

---

## ✅ What we've built (achievements)

### Foundation — the book builds & deploys
| Deliverable | Status |
| --- | --- |
| Clean `chapters/_config.yml`, valid `parts:` `_toc.yml`, real landing page | ✅ |
| Pinned deps (`jupyter-book<2`) + CI that **builds** the book and deploys to Pages | ✅ |
| `binder/requirements.txt` runtime env (incl. `scanpy`, `pydeseq2`, `openpyxl`) | ✅ |
| 🚀 **Launch buttons** (Binder/Colab/Thebe) on every notebook page | ✅ |
| Reader-focused home page: "how to use this book" tabs + launch badges | ✅ |
| Broken GitBook screenshots stripped from intro chapters | ✅ |

### Discoverability & FAIR — [`OSDR_FAIR_assessment.ipynb`](chapters/OSDR_FAIR_assessment.ipynb)
| Deliverable | Status |
| --- | --- |
| Live FAIR scorecard over the repository (whole-repo + most-common-gap chart) | ✅ |
| **Plant share of OSDR** (live: 70 / 640 = **10.9%**) + plant-subset drill-down (species, assay, factors, year) | ✅ |
| Astrobotany FAIR view (FAIR scores for the plant subset) | ✅ |

### Interactive explorers & data stories
| Deliverable | Status |
| --- | --- |
| [`osdr-public-api.ipynb`](chapters/osdr-public-api.ipynb) — live, runnable API tour (replaced the static page, moved to the end) | ✅ |
| [`OSDR_dataset_explorer.ipynb`](chapters/OSDR_dataset_explorer.ipynb) — drill-down: dataset → assays → samples → data → story | ✅ |
| [`OSDR_data_story.ipynb`](chapters/OSDR_data_story.ipynb) — **cross-study** reproducibility across 7 *Arabidopsis* spaceflight studies | ✅ |
| [`OSDR_methylation_layer.ipynb`](chapters/OSDR_methylation_layer.ipynb) — **epigenome × transcriptome** (OSD-217) + GO/KEGG enrichment | ✅ |
| [`OSDR_tomato_microbiome.ipynb`](chapters/OSDR_tomato_microbiome.ipynb) — **host × microbiome** (VEG-05) + host functional enrichment | ✅ |
| [`OSDR_tomato_microbiome_pipeline.ipynb`](chapters/OSDR_tomato_microbiome_pipeline.ipynb) — raw 16S/ITS → genus table → host-link **recipe** | ✅ |

### Astrobotany conversion (the CARA *Arabidopsis* arc)
All demo notebooks were re-authored from rodent spaceflight data to the **CARA
experiment** ([OSD-120](https://osdr.nasa.gov/bio/repo/data/studies/OSD-120),
*Arabidopsis* roots, spaceflight vs ground), and the whole repo was de-rodented
(reference docs re-themed, glossary trimmed) — see the chapter table below.

---

## 📋 Loose ends / outstanding (no surprises)

| Item | Status | Notes |
| --- | --- | --- |
| Remove stale root files | ✅ **done** | Deleted old `_config.yml`/`_toc.yml`, `.readthedocs.yaml`, `SUMMARY.*`, all root `*.html`, and stale root build dirs. Root is now just docs + `chapters/`, `binder/`, `.github/`. |
| `CITATION.cff` | ✅ **done** | [`CITATION.cff`](CITATION.cff) (CC0-1.0). |
| Contributor guide | ✅ **done** | [`CONTRIBUTING.md`](CONTRIBUTING.md). |
| GitHub Pages enabled | ✅ **confirmed** | Source: GitHub Actions; CI deploys on push to `main`. |
| Zenodo DOI | ⚠️ **ready to mint** | `.zenodo.json` + [`RELEASE.md`](RELEASE.md) are in place — turn on the Zenodo↔GitHub hook and cut a `v1.0` release to get the DOI, then drop it into `CITATION.cff` + README. |
| Quantitative tomato microbiome | ⚠️ recipe + FAIR write-up | OSD-766 is **raw 16S/ITS only**; the [pipeline notebook](chapters/OSDR_tomato_microbiome_pipeline.ipynb) produces real genus abundances in a DADA2/QIIME2 env, and the [tomato chapter](chapters/OSDR_tomato_microbiome.ipynb) §5 FAIR check quantifies the reuse gap. |
| Submitter "improve your FAIRness" reports | ✅ **done** | [`OSDR_fairness_report.ipynb`](chapters/OSDR_fairness_report.ipynb) — per-dataset report card + prioritised, actionable fixes. |
| Scheduled full-repo FAIR scoring over time | ✅ **done** | [`OSDR_fair_over_time.ipynb`](chapters/OSDR_fair_over_time.ipynb) + [`_fair_snapshot.py`](chapters/_fair_snapshot.py) + a monthly cron workflow. First snapshot: 640 datasets, FAIR overall **91.0** (Reusable 69.3 = the gap). |

---

## 🔑 Key scientific findings so far

- **OSDR exposes 640 datasets**; **plants are ~10.9%** (live), overwhelmingly *Arabidopsis*.
- The API metadata has **no licence field** → FAIR criterion **R1.1 fails repository-wide** (a real, actionable reuse gap).
- The *Arabidopsis* **spaceflight transcriptome is reproducible** across 7 independent studies (positive cross-study correlation; a consistent "core" responds in the same direction).
- **Epigenome × transcriptome (OSD-217):** genome-wide methylation–expression coupling is *weak* (as expected in plants); the multi-omic hit genes enrich for **photosynthesis / light-harvesting** and **desiccation / high-light stress** — a coordinated light/energy response in roots.
- **Tomato (VEG-05):** the host root spaceflight response enriches for **phenylpropanoid & flavonoid biosynthesis, ROS metabolism, stress** — the plant→microbe signalling/defence pathways that bridge to the **PGPR-rich flight microbiome** (*Rhizobium, Azospirillum, Burkholderia*) documented in OSD-766.

---

## 📚 The book's contents

**Part 1 — Interactive FAIR assessment** · `OSDR_FAIR_assessment.ipynb`

**Part 2 — Introduction to OSDR & data access** · `how-to-access-data-in-the-osdr` · `osdr-data-visualization-portal` · `environmental-data-for-space-biology-experiments` · `radlab-overview` · `open-science-abbreviations`

**Part 3 — Demo notebooks (the CARA *Arabidopsis* arc)**

| Notebook | What the reader does |
| --- | --- |
| `Tabular_Data` | Load/wrangle OSD-120 root RNA-seq; NaN/outlier/scaling on a CARA seedling table |
| `Clustering` | Unsupervised clustering separates spaceflight vs ground roots |
| `Regression` | Predict root **length** (CARA phenotypes) from gene expression |
| `Classification` | Classify flight-vs-ground and light-vs-dark from expression |
| `rr9-phenotypes_Lesson_01` | Compare root traits (length/surface/volume/diameter) flight vs ground |
| `Image_Data` | Image analysis on CARA *Arabidopsis* root photographs |
| `Methods`, `Methods_Lesson_01` | Shared AI/ML method library, on OSD-120 |
| `PubMed_scraping…`, `Knowledge-graph…` | Literature + knowledge-graph figures |

**Part 4 — Interactive explorers & data stories** · `osdr-public-api` · `OSDR_dataset_explorer` · `OSDR_data_story` · `OSDR_methylation_layer` · `OSDR_tomato_microbiome` · `OSDR_tomato_microbiome_pipeline`

---

## 🏗️ Architecture & conventions

- **Book root is [`chapters/`](chapters/)** — content *and* sample data live there; build with `jupyter-book build chapters/`.
- **Classic Jupyter Book v1** (Sphinx / `jb-book`). ⚠️ v2 is a different MyST/Node tool and is incompatible — keep `jupyter-book<2`.
- **Notebooks are NOT executed in CI** (`execute_notebooks: off`) — they ship with saved outputs; refresh locally.
- **Notebooks are generated from `_make_*.py` scripts** (the reproducible source of truth). To change a generated notebook, edit its `_make_*.py`, re-run it, then `jupyter nbconvert --execute`.
- **Interactive charts use Plotly** (`notebook_connected` renderer) so they survive in static HTML; large scatters are sampled + WebGL.
- **Functional enrichment uses the free [g:Profiler](https://biit.cs.ut.ee/gprofiler/) API** (`athaliana`, `slycopersicum`) — `requests` only, no key.

---

## 🚀 Build, develop & refresh

```bash
pip install -r chapters/requirements.txt
jupyter-book build chapters/              # output: chapters/_build/html/index.html

# Refresh a generated notebook with live data, e.g. the FAIR assessment:
cd chapters
python _make_fair_notebook.py
jupyter nbconvert --to notebook --execute --inplace OSDR_FAIR_assessment.ipynb
```

---

## ⚠️ Honest data limitations

- **OSD-766 microbiome:** raw 16S/ITS only — no processed taxonomy via the API; the tomato host↔microbe link is **group-level / hypothesis-generating** (host & microbiome are different sample sets). Community composition is cited from the published study; the pipeline notebook generates real abundances when run in a bioinformatics env.
- **OSD-767 tomato RNA-seq:** only *unnormalized* counts are served — the chapter normalises to CPM itself.
- **Methylation:** only OSD-217 exposes processed WGBS; OSD-220/OSD-416 are raw-only.

---

## 🌐 OSDR biodata API (base `…/biodata/api/v2/`)

| Purpose | Endpoint |
| --- | --- |
| List all datasets | `/v2/datasets/` |
| Dataset metadata | `/v2/dataset/{ACCESSION}/` |
| Assays in a dataset | `/v2/dataset/{ACCESSION}/assays/` |
| Files in a dataset | `/v2/dataset/{ACCESSION}/files/` |
| Query metadata across studies | `/v2/query/metadata/?<field>` |
| Query data columns | `/v2/query/data/` |

(Full file listings, incl. processed-data categories, are richer via `https://osdr.nasa.gov/osdr/data/osd/files/{N}`.)

---

## 📄 Licence
See [`LICENSE`](LICENSE). Built on NASA OSDR open data.
