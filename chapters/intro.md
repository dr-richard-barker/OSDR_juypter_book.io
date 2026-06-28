# Open Science Data Repository — Interactive FAIR Notebook

Welcome! This interactive Jupyter Book is a tool for **exploring, assessing, and
telling stories with** data from NASA's [Open Science Data Repository
(OSDR)](https://osdr.nasa.gov/), built on top of the public
[biodata API](https://visualization.osdr.nasa.gov/biodata/api/).

The goal is a publication-ready tool that helps you:

- **Find** what data is available across OSDR (GeneLab + ALSDA) studies.
- **Assess** each dataset against **FAIR** principles — Findable, Accessible,
  Interoperable, Reusable.
- **Visualise** metadata and results interactively for data storytelling.

## How this book is organised

```{tableofcontents}
```

## Getting started

Every notebook can be launched live (Binder / Colab / your own Jupyter) and the
markdown chapters explain the OSDR data systems and APIs. To build this book
locally:

```bash
pip install -r requirements.txt
jupyter-book build .
```

The OSDR biodata API is the backbone of the interactive layer:

| Purpose | Endpoint |
| --- | --- |
| List all datasets | `/v2/datasets/` |
| Dataset metadata | `/v2/dataset/{ACCESSION}/` |
| Assays in a dataset | `/v2/dataset/{ACCESSION}/assays/` |
| Query metadata across studies | `/v2/query/metadata/` |
| Query data columns | `/v2/query/data/` |

Base URL: `https://visualization.osdr.nasa.gov/biodata/api/v2/`
