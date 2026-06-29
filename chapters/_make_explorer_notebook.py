"""Generate `OSDR_dataset_explorer.ipynb` — an interactive drill-down explorer:
pick a dataset, traverse its assays + samples, and plot the data, for data
storytelling. Run:  python _make_explorer_notebook.py  (then nbconvert execute)
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []
md = lambda s: cells.append(nbf.v4.new_markdown_cell(s))
code = lambda s: cells.append(nbf.v4.new_code_cell(s))

md(r"""# 🔎 OSDR dataset explorer

A guided **drill-down** through a single OSDR dataset: **dataset → assays →
samples → data → story**. Change one accession at the top and the whole notebook
re-tells the story for *your* dataset.

> 🚀 **Make it live:** open this page in **Binder** or **Colab** via the rocket
> icon (top-right), then run the cells with **Shift + Enter**.

We default to **OSD-120** — the *Arabidopsis* CARA spaceflight study — so the
story is: *how does a plant root gene respond to spaceflight?*""")

code('''import io, datetime
import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook_connected"

API = "https://visualization.osdr.nasa.gov/biodata/api/v2"

ACC = "OSD-120"     # <<< change this to any accession (e.g. OSD-37, OSD-321) and re-run''')

md("## 1. The dataset at a glance")

code('''meta = requests.get(f"{API}/dataset/{ACC}/", timeout=60).json()[ACC]["metadata"]

def show(v):
    return ", ".join(map(str, v)) if isinstance(v, list) else v

try:
    released = datetime.datetime.utcfromtimestamp(int(meta["study public release date"])).date()
except Exception:
    released = "n/a"

print(f"{ACC}: {show(meta.get('study title',''))}\\n")
for label, key in [("Organism", "organism"), ("Assay type", "study assay technology type"),
                   ("Factors studied", "study factor type"), ("Flight program", "flight program"),
                   ("NASA center", "managing nasa center")]:
    print(f"  {label:18}: {show(meta.get(key, '—'))}")
print(f"  {'Released':18}: {released}")''')

md("## 2. Drill into its assays\n\nEach dataset holds one or more assays — the actual measurements taken.")

code('''assays = requests.get(f"{API}/dataset/{ACC}/assays/", timeout=60).json()[ACC]["assays"]
for name in assays:
    print("•", name)''')

md(r"""## 3. Drill into its samples & experimental design

Using the Query interface, we pull every sample with its **factor values** (the
experimental variables). This reveals the design — e.g. spaceflight vs ground,
across ecotypes.""")

code('''url = (f"{API}/query/metadata/?id.accession={ACC}"
       "&id.assay name&id.sample name&study.factor value&format=csv")
samples = pd.read_csv(io.StringIO(requests.get(url, timeout=60).text))
factor_cols = [c for c in samples.columns if c.startswith("study.factor value")]
design = samples.drop_duplicates("id.sample name")
print(f"{len(design)} samples; factors: {[c.split('.')[-1] for c in factor_cols]}")
design.head()''')

code('''# Visualise the design: sample counts across the first two factors
if len(factor_cols) >= 2:
    f1, f2 = factor_cols[0], factor_cols[1]
    g = design.groupby([f1, f2]).size().reset_index(name="samples")
    fig = px.bar(g, x=f1, y="samples", color=f2, barmode="group",
                 labels={f1: f1.split('.')[-1], f2: f2.split('.')[-1]},
                 title=f"{ACC}: experimental design (sample counts)")
    fig.update_layout(height=380); fig.show()
else:
    print("This dataset exposes fewer than two factor columns.")''')

md(r"""## 4. Drill into the data — a gene's response to spaceflight

For transcriptomic datasets we load the processed **normalized counts** and ask a
storytelling question: *does this gene behave differently in spaceflight vs
ground?* Change `GENE` to any [AGI locus](https://www.arabidopsis.org/).""")

code('''# Find the normalized-counts file for this dataset (works for GeneLab RNA-seq studies)
files = requests.get(f"{API}/dataset/{ACC}/files/", timeout=60).json()
fkey = list(files)[0]
names = list(files[fkey].get("files", files[fkey]))
counts_file = next((n for n in names
                    if "Normalized_Counts" in n and n.endswith(".csv") and "rRNArm" not in n), None)
print("counts file:", counts_file)

counts = pd.read_csv(f"https://osdr.nasa.gov/geode-py/ws/studies/{ACC}/download"
                     f"?source=datamanager&file={counts_file}", index_col=0)
print(f"{counts.shape[0]} genes × {counts.shape[1]} samples")''')

code('''GENE = "AT1G29930"     # <<< change me (default = CAB1, a light-responsive gene)

expr = counts.loc[GENE].rename_axis("sample").reset_index(name="expression")
# label each sample from its name (GeneLab convention encodes the design)
expr["condition"] = expr["sample"].str.contains("_FLT_").map({True: "Spaceflight", False: "Ground"})
expr["ecotype"] = expr["sample"].str.extract(r"Atha_([A-Za-z0-9-]+)_root")

fig = px.box(expr, x="condition", y="expression", color="ecotype", points="all",
             title=f"{GENE} expression in {ACC}: spaceflight vs ground roots",
             labels={"expression": "normalized expression"})
fig.update_layout(height=420); fig.show()''')

md(r"""## 5. Tell your own story

You now have a repeatable drill-down. To explore a different question:

- Change **`ACC`** (top) to another study — the metadata, assays, samples and
  design all update.
- Change **`GENE`** to any locus to see its spaceflight response.
- Swap the box plot for any other Plotly chart.

```{tip}
This explorer is just the OSDR API + pandas + Plotly. Everything you see is
re-runnable and editable — a starting point for your own OSDR data story.
```""")

nb["cells"] = cells
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
with open("OSDR_dataset_explorer.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print("Wrote OSDR_dataset_explorer.ipynb")
