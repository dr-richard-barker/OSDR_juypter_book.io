# 🌱 OSDR Astrobotany — Interactive FAIR Notebook

Welcome! This is an **interactive Jupyter Book** for exploring, assessing, and
telling stories with the plant-biology data in NASA's
[Open Science Data Repository (OSDR)](https://osdr.nasa.gov/), built on the
public [biodata API](https://visualization.osdr.nasa.gov/biodata/api/).

You can **read** every page like a normal website, or **run** any notebook live —
changing the code, the dataset, and the charts yourself.

With this book you can:

- **Find** what plant data exists across OSDR and see how much of the repository it makes up.
- **Assess** each dataset against the **FAIR** principles (Findable, Accessible, Interoperable, Reusable).
- **Explore** a real *Arabidopsis* spaceflight story end-to-end — from raw data to machine learning.

---

## 🚀 How to use this book

There are three ways in. Pick the one that fits you:

`````{tab-set}
````{tab-item} 1. Just read it (no setup)
Click any chapter in the left sidebar and read straight through. Every notebook
already shows its **code, charts, and results**, so you get the full story
without running anything.
````

````{tab-item} 2. Run it live in the cloud (recommended)
Make it interactive with **no installation**:

1. Open any **notebook** page (e.g. *Working with Tabular Data*).
2. Hover the **🚀 rocket icon** at the **top-right** of the page.
3. Choose **Binder** (runs the whole book in your browser) or **Colab** (opens in
   Google Colab — needs a Google login).
4. Once it loads, run cells top-to-bottom with **Shift + Enter**, and start editing.

Or launch right now:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dr-richard-barker/OSDR_juypter_book.io/main?urlpath=lab/tree/chapters)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/dr-richard-barker/OSDR_juypter_book.io/blob/main/chapters/Tabular_Data.ipynb)

```{tip}
First Binder launch can take a minute while it builds the environment — that's
normal. After that it's instant.
```
````

````{tab-item} 3. Run on your own computer
For full control (and offline use):

```bash
git clone https://github.com/dr-richard-barker/OSDR_juypter_book.io
cd OSDR_juypter_book.io
pip install -r chapters/requirements.txt
jupyter lab chapters/      # open and run any .ipynb
```
````
`````

```{admonition} New here? Start with one click 🌱
:class: seealso
The **[Working with Tabular Data](Tabular_Data.ipynb)** notebook is the gentlest
entry point — load a real *Arabidopsis* spaceflight dataset and explore it. From
there, follow the analysis path below.
```

---

## 🧭 A suggested path through the book

You don't have to read in order, but this is the intended journey:

1. **The big picture** — [a live FAIR assessment of OSDR](OSDR_FAIR_assessment.ipynb):
   what data exists, how FAIR it is, and *what share of OSDR is plant data*.
2. **The Arabidopsis story (CARA / OSD-120)** — one spaceflight dataset, analysed
   stage by stage:
   *[Tabular data](Tabular_Data.ipynb) → [Clustering](Clustering.ipynb) →
   [Regression](Regression.ipynb) → [Classification](Classification.ipynb) →
   [Root phenotypes](rr9-phenotypes_Lesson_01.ipynb) → [Image analysis](Image_Data.ipynb).*
3. **Reference** — how the OSDR data systems, APIs and portals work (sidebar).

## 📚 Full contents

```{tableofcontents}
```

---

## ⚙️ Under the hood: the OSDR biodata API

The interactive layer is powered by the OSDR biodata API
(base URL `https://visualization.osdr.nasa.gov/biodata/api/v2/`):

| Purpose | Endpoint |
| --- | --- |
| List all datasets | `/v2/datasets/` |
| Dataset metadata | `/v2/dataset/{ACCESSION}/` |
| Assays in a dataset | `/v2/dataset/{ACCESSION}/assays/` |
| Query metadata across studies | `/v2/query/metadata/` |
| Query data columns | `/v2/query/data/` |
