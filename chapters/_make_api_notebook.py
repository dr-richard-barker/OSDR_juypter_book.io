"""Generate `osdr-public-api.ipynb` — an interactive replacement for the static
osdr-public-api.md reference. Live, runnable examples against the OSDR API.

Run:  python _make_api_notebook.py    (then execute with nbconvert)
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []
md = lambda s: cells.append(nbf.v4.new_markdown_cell(s))
code = lambda s: cells.append(nbf.v4.new_code_cell(s))

md(r"""# Exploring the OSDR API (interactive)

This notebook is a **hands-on tour of the NASA OSDR
[biodata API](https://visualization.osdr.nasa.gov/biodata/api/)** — the engine
behind this whole book. Instead of just reading example URLs, you can **run**
every request here and change it.

> 🚀 **Make it live:** hover the rocket icon at the top-right and open this page
> in **Binder** or **Colab**, then run the cells with **Shift + Enter**. Change an
> accession or a search term and re-run to explore your own questions.

The API has two complementary interfaces:

| Interface | What it's for | Returns |
| --- | --- | --- |
| **REST** | Traverse one dataset at a time: dataset → assays → samples → files | JSON |
| **Query** | Pull one field across *all* datasets at once | CSV |

Base URL: `https://visualization.osdr.nasa.gov/biodata/api/v2/`""")

code('''import io
import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook_connected"   # keeps charts interactive in the static book

API = "https://visualization.osdr.nasa.gov/biodata/api/v2"''')

md("""## 1. REST — list every dataset

Start at `/v2/datasets/`. Each entry links to that dataset's own REST URL, so you
can traverse from here into any study.""")

code('''datasets = requests.get(f"{API}/datasets/", timeout=60).json()
print(f"OSDR currently exposes {len(datasets)} datasets via the API.")
list(datasets)[:5]''')

md("""## 2. Look inside one dataset

Change `acc` to any accession (e.g. `OSD-37`, `OSD-321`) and re-run. Here we use
**OSD-120**, the *Arabidopsis* CARA spaceflight study featured throughout this book.""")

code('''acc = "OSD-120"            # <-- change me and re-run
meta = requests.get(f"{API}/dataset/{acc}/", timeout=60).json()[acc]["metadata"]

print(meta["study title"], "\\n")
{k: meta.get(k) for k in
 ["organism", "study assay technology type", "study factor type",
  "flight program", "managing nasa center"]}''')

md("""## 3. List the assays in that dataset

Each dataset contains one or more assays (e.g. RNA-seq, imaging). The assay name
is the key you use to drill further into samples and data.""")

code('''assays = requests.get(f"{API}/dataset/{acc}/assays/", timeout=60).json()[acc]["assays"]
list(assays)''')

md(r"""## 4. Query — one field across the *whole* repository

The Query interface flattens metadata so you can pull a single field for every
study at once. Below we fetch the **organism** of every sample as CSV, then ask:
*what fraction of OSDR is plant data?* — computed **live** from the API.""")

code('''url = f"{API}/query/metadata/?id.accession&study.characteristics.organism&format=csv"
m = pd.read_csv(io.StringIO(requests.get(url, timeout=120).text))

# the query returns one row per sample -> collapse to one organism per dataset
per_dataset = m.groupby("id.accession")["study.characteristics.organism"].first()

PLANT = "arabidopsis|thaliana|brassica|oryza|plant"
is_plant = per_dataset.str.contains(PLANT, case=False, na=False)
print(f"{is_plant.sum()} of {len(per_dataset)} datasets are plants "
      f"({100 * is_plant.mean():.1f}%) — computed live from the API")''')

code('''# Top organisms in OSDR, live (plants highlighted)
top = per_dataset.value_counts().head(12).rename_axis("organism").reset_index(name="datasets")
top["plant"] = top["organism"].str.contains(PLANT, case=False, na=False)
fig = px.bar(top.sort_values("datasets"), x="datasets", y="organism", orientation="h",
             color="plant", color_discrete_map={True: "#2e7d32", False: "#90a4ae"},
             title="Organisms in OSDR (live from the API; plants in green)")
fig.update_layout(height=420, showlegend=False)
fig.show()''')

md("""## 5. Search the repository

The search API does free-text search with `AND` / `OR` / `NOT`. Change the query
and re-run to find datasets on any topic.""")

code('''query = "Arabidopsis AND root"        # <-- try "spaceflight AND microgravity", etc.
res = requests.get("https://osdr.nasa.gov/osdr/data/search",
                   params={"term": query, "size": 5}, timeout=40).json()

print(f"{res['hits']['total']} results for {query!r}. First 5:")
for h in res["hits"]["hits"]:
    src = h["_source"]
    print(f"  {src.get('Study Identifier', h['_id'])}: {src.get('Study Title', '')[:70]}")''')

md(r"""## Endpoint reference

| Purpose | Endpoint |
| --- | --- |
| List all datasets | `/v2/datasets/` |
| Dataset metadata | `/v2/dataset/{ACCESSION}/` |
| Assays in a dataset | `/v2/dataset/{ACCESSION}/assays/` |
| Files in a dataset | `/v2/dataset/{ACCESSION}/files/` |
| Query a metadata field across studies | `/v2/query/metadata/?<field>` |
| Query data columns | `/v2/query/data/` |

**Output formats:** the REST interface returns JSON; the Query interface returns
CSV by default (also `json`, `json.records`, `tsv`, `html`).

### Going further
- **Full API docs & filter fields:** <https://visualization.osdr.nasa.gov/biodata/api/>
- **Search UI / advanced operators:** <https://osdr.nasa.gov/bio/repo/search>
- **Bulk download (AWS S3 Registry of Open Data):** <https://registry.opendata.aws/nasa-osdr/>

```{tip}
Everything above is just `requests` + `pandas`. Copy any cell into your own
analysis, swap the accession or query, and you have a live OSDR data pipeline.
```""")

nb["cells"] = cells
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3",
                                "language": "python"}
with open("osdr-public-api.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print("Wrote osdr-public-api.ipynb")
