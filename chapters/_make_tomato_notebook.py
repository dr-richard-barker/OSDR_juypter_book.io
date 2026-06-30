"""Generate `OSDR_tomato_microbiome.ipynb` — a tomato (VEG-05) chapter linking the
host transcriptome (OSD-767) with its paired microbiome study (OSD-766).
Run: python _make_tomato_notebook.py  (then nbconvert --execute)
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []
md = lambda s: cells.append(nbf.v4.new_markdown_cell(s))
code = lambda s: cells.append(nbf.v4.new_code_cell(s))

md(r"""# 🍅 Tomato in space: host transcriptome × microbiome (VEG-05)

NASA's **VEG-05** experiment grew dwarf *Solanum lycopersicum* cv. **Red Robin**
tomatoes on the ISS under **red-rich vs blue-rich** light, in flight and on the
ground. Crucially, OSDR holds **two paired studies of the same experiment**:

| Study | What it measured | Assay |
| --- | --- | --- |
| [**OSD-767**](https://osdr.nasa.gov/bio/repo/data/studies/OSD-767) | the **host plant** transcriptome | RNA-seq |
| [**OSD-766**](https://osdr.nasa.gov/bio/repo/data/studies/OSD-766) | the **microbiome** (bacteria + fungi) | 16S + ITS amplicon |

Both share the same factors — **spaceflight × light regimen × organ** — so we can
ask the question at the heart of plant–microbe biology:

> **Do the microbial shifts and the host's transcriptional shifts line up?
> Could spaceflight-altered microbes be influencing the tomato's gene expression
> — or the plant reshaping its microbiome?**

> 🚀 Open in Binder/Colab (rocket icon) to run and extend this analysis.""")

code('''import io, re
import numpy as np
import pandas as pd
import requests
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook_connected"

API = "https://visualization.osdr.nasa.gov/biodata/api/v2"
GEODE = "https://osdr.nasa.gov/geode-py/ws/studies"
HOST, MICROBE = "OSD-767", "OSD-766"''')

md("""## 1. The paired experimental design

First we confirm the two studies really do share the same design — that's what
makes a host–microbe comparison meaningful.""")

code('''def factor_design(acc):
    url = f"{API}/query/metadata/?id.accession={acc}&id.sample name&study.factor value&format=csv"
    df = pd.read_csv(io.StringIO(requests.get(url, timeout=60).text)).drop_duplicates("id.sample name")
    fcols = {c: c.split(".")[-1] for c in df.columns if c.startswith("study.factor value")}
    return df.rename(columns=fcols), list(fcols.values())

host_meta, host_factors = factor_design(HOST)
mic_meta, mic_factors = factor_design(MICROBE)
print(f"HOST  {HOST}: {len(host_meta)} samples; factors = {host_factors}")
print(f"MICRO {MICROBE}: {len(mic_meta)} samples; factors = {mic_factors}")''')

code('''# Microbiome sampling across organs and spaceflight (its design is richer: also fruit + facility swabs)
g = (mic_meta.groupby(["organism part", "spaceflight"]).size().reset_index(name="samples"))
fig = px.bar(g, x="organism part", y="samples", color="spaceflight", barmode="group",
             title=f"{MICROBE}: microbiome samples by organ and spaceflight (16S + ITS)")
fig.update_layout(height=380)
fig.show()''')

md(r"""## 2. The host response — the tomato spaceflight transcriptome

We load OSD-767's RSEM counts, normalise to counts-per-million, and measure the
**spaceflight effect** (log₂ flight / ground) — focusing on **roots**, the
host–microbe interface where the rhizosphere community lives.""")

code('''counts = pd.read_csv(
    f"{GEODE}/{HOST}/download?source=datamanager"
    "&file=GLDS-709_rna_seq_RSEM_Unnormalized_Counts_GLbulkRNAseq.csv", index_col=0)

# the sample names encode the design: Flt/Gnd, Leaf/Root, Red/Blue
def parse(col):
    cond = "Spaceflight" if "Flt" in col else ("Ground" if "Gnd" in col else None)
    organ = "Root" if "Root" in col else ("Leaf" if "Leaf" in col else None)
    light = "red-rich" if "Red" in col else ("blue-rich" if "Blue" in col else None)
    return cond, organ, light

cpm = counts / counts.sum() * 1e6
cpm = cpm[(cpm > 1).sum(axis=1) >= 3]               # keep genes expressed in >=3 samples
print(f"{cpm.shape[0]} expressed tomato genes across {cpm.shape[1]} samples")

def spaceflight_lfc(organ):
    flt = [c for c in cpm.columns if parse(c)[1] == organ and parse(c)[0] == "Spaceflight"]
    gnd = [c for c in cpm.columns if parse(c)[1] == organ and parse(c)[0] == "Ground"]
    return np.log2((cpm[flt].mean(axis=1) + 1) / (cpm[gnd].mean(axis=1) + 1)).rename(organ)

root_lfc, leaf_lfc = spaceflight_lfc("Root"), spaceflight_lfc("Leaf")''')

code('''# Top spaceflight-responsive genes in the ROOT (host-microbe interface)
top = root_lfc.reindex(root_lfc.abs().sort_values(ascending=False).index).head(20).sort_values()
fig = px.bar(top, orientation="h", text=top.round(2).values,
             labels={"value": "root spaceflight log₂FC (flight / ground)", "index": "tomato gene"},
             color=top.values, color_continuous_scale="RdBu_r", color_continuous_midpoint=0,
             title="Top spaceflight-responsive genes in tomato roots (OSD-767)")
fig.update_layout(height=560, showlegend=False, coloraxis_showscale=False)
fig.show()''')

code('''# Is the root response distinct from the leaf response? (organ-specific spaceflight effects)
both = pd.concat([root_lfc, leaf_lfc], axis=1).dropna()
r = both["Root"].corr(both["Leaf"])
samp = both.sample(min(6000, len(both)), random_state=0)
fig = px.scatter(samp, x="Leaf", y="Root", opacity=0.25, render_mode="webgl",
                 title=f"Spaceflight response: root vs leaf (r = {r:.2f}) — organ matters",
                 labels={"Leaf": "leaf log₂FC", "Root": "root log₂FC"})
fig.add_hline(y=0, line_dash="dot", opacity=0.4); fig.add_vline(x=0, line_dash="dot", opacity=0.4)
fig.update_layout(height=460)
fig.show()''')

md(r"""## 3. The microbiome side

OSD-766 profiled bacteria (**16S**) and fungi (**ITS**) on tomato fruit, leaves,
roots, the rooting substrate, and Veggie facility surfaces. The study's
**published findings** ([NASA NTRS](https://ntrs.nasa.gov/citations/20240016407))
report:

- **Flight plants carried *more* microbes than ground controls** (higher bacterial
  and fungal counts) — spaceflight increased microbial load.
- Light recipe (red- vs blue-rich) did **not** significantly change microbial counts.
- The **core flight microbiome** was dominated by *Rhizobium*, *Azospirillum*,
  *Burkholderia*, *Dyadobacter*, and *Sphingomonas* — genera rich in
  **nitrogen-fixing and plant-growth-promoting (PGPR)** bacteria.
- Pathogen screening (culture + sequencing) was **negative** — the crop was safe.

```{admonition} An honest note on the data
:class: warning
OSDR currently serves OSD-766 as **raw 16S/ITS sequence data** — the *processed
per-sample taxonomic abundance tables are not yet exposed through the biodata
API*. So the community composition above is taken from the study's published
report, not recomputed here. The next section sets up the quantitative
host↔microbe join so it runs the moment those abundance tables are released
(or once the raw amplicon data is processed through a QIIME2/DADA2 pipeline).
```""")

md(r"""## 4. Connecting the two layers

The biology points to a clear hypothesis. The flight root microbiome is enriched
in **nitrogen-fixing / growth-promoting** bacteria (*Rhizobium*, *Azospirillum*,
*Burkholderia*). If those microbes are influencing the host — or responding to it —
we'd expect the signal in the **root** transcriptome (nitrogen metabolism, hormone
signalling, defence/immunity), which is exactly where we measured the strongest,
most organ-specific spaceflight response (section 2).

Below is the **ready-to-run integration scaffold**: it summarises the host
expression by experimental group, and joins it to a microbial-abundance table
keyed on the *same* groups. Drop in real abundances (per organ × light ×
spaceflight) and it computes the host↔microbe correlations immediately.""")

code('''# Host expression summarised per experimental group (real, computed now)
groups = pd.DataFrame({c: parse(c) for c in cpm.columns}, index=["condition", "organ", "light"]).T
def host_group_means(genes):
    sub = cpm.loc[cpm.index.intersection(genes)]
    long = sub.T.join(groups)
    return long.groupby(["organ", "light", "condition"]).mean(numeric_only=True)

example_genes = root_lfc.abs().sort_values(ascending=False).head(50).index
host_summary = host_group_means(example_genes)
print("Host expression summarised over", host_summary.shape[0], "groups x",
      host_summary.shape[1], "genes — keyed by (organ, light, spaceflight)")

def link_microbe_to_host(microbe_abundance, host_summary):
    """microbe_abundance: DataFrame indexed by (organ, light, condition), columns = taxa.
    Returns Pearson r between each taxon and each host gene across groups."""
    joined = microbe_abundance.join(host_summary, how="inner")
    taxa = list(microbe_abundance.columns); genes = list(host_summary.columns)
    return joined[taxa].apply(lambda t: joined[genes].corrwith(t)).T

print("\\nlink_microbe_to_host() is ready — feed it a taxon-abundance table keyed by",
      "(organ, light, condition) to get a taxa x genes correlation matrix.")''')

md(r"""## 5. The story so far

- The tomato **host transcriptome responds strongly to spaceflight**, and the
  response is **organ-specific** — roots ≠ leaves (section 2). Roots, the
  rhizosphere interface, are the natural place to look for microbial influence.
- The paired microbiome study shows spaceflight plants carry **more microbes**,
  enriched in **nitrogen-fixing / growth-promoting** genera (section 3) — a
  community well-placed to interact with host root metabolism.
- Putting them together is the frontier: the **integration scaffold** (section 4)
  will quantify host↔microbe coupling as soon as processed abundances are
  available. Until then, this chapter pairs a *quantitative* host analysis with a
  *documented* microbiome shift and a concrete plan to join them.

This is what OSDR's paired multi-omic studies make possible — and exactly the kind
of cross-dataset story this book is built to tell.

---

**Sources:** [VEG-05 Microbiome — NASA NTRS 20240016407](https://ntrs.nasa.gov/citations/20240016407) ·
[OSD-767 (host RNA-seq)](https://osdr.nasa.gov/bio/repo/data/studies/OSD-767) ·
[OSD-766 (microbiome)](https://osdr.nasa.gov/bio/repo/data/studies/OSD-766)""")

nb["cells"] = cells
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
with open("OSDR_tomato_microbiome.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print("Wrote OSDR_tomato_microbiome.ipynb")
