"""Generate `OSDR_FAIR_assessment.ipynb` (Phase 2 starter).

Builds a notebook that pulls datasets from the OSDR biodata API, scores each
against FAIR sub-criteria derived from the available metadata fields, and
renders an interactive Plotly scorecard + summary charts.

Run:  python _make_fair_notebook.py
Then it is executed by build_fair.sh / the dev workflow to embed outputs.
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []
md = lambda s: cells.append(nbf.v4.new_markdown_cell(s))
code = lambda s: cells.append(nbf.v4.new_code_cell(s))

md(r"""# A live FAIR assessment of OSDR datasets

This notebook is an **interactive, standardised FAIR assessment** of the data
available through NASA's Open Science Data Repository (OSDR), built directly on
the public [biodata API](https://visualization.osdr.nasa.gov/biodata/api/).

For every dataset it asks: how **F**indable, **A**ccessible, **I**nteroperable
and **R**eusable is it, judged from the metadata the API actually exposes?

> **How to run live:** set `MAX_DATASETS = None` below and re-run to score the
> entire repository. The version shown here scores a sample so the book builds
> quickly. Outputs are embedded; nothing runs when the book is built.""")

code('''import time
import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio

# CDN-backed renderer => interactive charts survive in the static book HTML
pio.renderers.default = "notebook_connected"

API = "https://visualization.osdr.nasa.gov/biodata/api/v2"

# Score a sample for a fast book build; set to None to score everything.
MAX_DATASETS = 60''')

md("""## 1. Find every dataset

The REST interface lists all datasets at `/v2/datasets/`. We start there and
traverse into each dataset's metadata.""")

code('''resp = requests.get(f"{API}/datasets/", timeout=60)
resp.raise_for_status()
all_ids = list(resp.json().keys())
print(f"OSDR currently exposes {len(all_ids)} datasets via the biodata API.")

ids = all_ids if MAX_DATASETS is None else all_ids[:MAX_DATASETS]
print(f"Scoring {len(ids)} of them in this run.")''')

md(r"""## 2. Define the FAIR rubric

Each principle is broken into concrete, checkable sub-criteria. A criterion
scores **1** if the corresponding metadata is present and non-empty, else **0**.
This is intentionally transparent and reproducible — edit the rubric to match
your community's FAIR maturity model.

Note one structural finding baked in below: the biodata API metadata does **not**
expose an explicit **licence** field, so `R1.1 (licence)` will fail for every
dataset. That is a real, repository-wide reusability gap worth flagging.""")

code('''def present(meta, key):
    """True if a metadata key exists and is not empty."""
    v = meta.get(key)
    return v not in (None, "", [], {}, "n/a", "N/A")

def fair_criteria(meta):
    """Return {principle: {criterion: 0/1}} for one dataset's metadata."""
    p = lambda k: 1 if present(meta, k) else 0
    return {
        "Findable": {
            "F1 accession/identifier": max(p("accession"), p("identifiers"),
                                           p("study identifier")),
            "F2 rich title+description": 1 if (present(meta, "study title") and
                                               present(meta, "study description")) else 0,
            "F2 organism indexed": p("organism"),
            "F4 public release date": p("study public release date"),
        },
        "Accessible": {
            "A1 REST/API retrievable": 1,                  # every dataset has a REST_URL
            "A1 authoritative source url": p("authoritative source url"),
            "A1 file listing available": 1,                # every dataset exposes /files/
        },
        "Interoperable": {
            "I1 assay technology type": p("study assay technology type"),
            "I1 measurement type": p("study assay measurement type"),
            "I2 ISA characteristics/factors": max(p("characteristics"),
                                                  p("study factor type")),
            "I3 data source linkage": max(p("data source accession"),
                                          p("project link")),
        },
        "Reusable": {
            "R1 protocols described": p("study protocol description"),
            "R1.1 explicit licence": 0,                    # not exposed by the API
            "R1.2 provenance (funding/grant)": max(p("study funding agency"),
                                                   p("study grant number")),
            "R1.2 linked publication": max(p("study publication title"),
                                           p("study publication author list")),
        },
    }''')

md("""## 3. Pull metadata and score every dataset

We fetch each dataset's metadata block and apply the rubric. Failures are
recorded rather than aborting the run, so a single flaky request can't break the
whole assessment.""")

code('''rows = []
for i, acc in enumerate(ids, 1):
    try:
        r = requests.get(f"{API}/dataset/{acc}/", timeout=60)
        r.raise_for_status()
        meta = r.json()[acc]["metadata"]
    except Exception as e:                      # noqa: BLE001 - keep the sweep going
        rows.append({"accession": acc, "error": str(e)})
        continue

    crit = fair_criteria(meta)
    row = {"accession": acc,
           "organism": meta.get("organism", ""),
           "assay": meta.get("study assay technology type", "")}
    for principle, checks in crit.items():
        row[principle] = round(100 * sum(checks.values()) / len(checks), 1)
        for name, val in checks.items():
            row[name] = val
    row["FAIR overall"] = round(
        sum(row[p] for p in ["Findable", "Accessible", "Interoperable", "Reusable"]) / 4, 1)
    rows.append(row)
    if i % 20 == 0:
        print(f"  scored {i}/{len(ids)}")
    time.sleep(0.05)                            # be polite to the API

df = pd.DataFrame(rows)
ok = df[~df.get("error", pd.Series(index=df.index)).notna()] if "error" in df else df
print(f"Scored {len(ok)} datasets successfully.")
ok.head()''')

md("""## 4. The FAIR scorecard

Per-principle and overall scores (0–100). Sortable in the live notebook; this
is the backbone other views build on.""")

code('''cols = ["accession", "organism", "Findable", "Accessible",
        "Interoperable", "Reusable", "FAIR overall"]
scorecard = ok[cols].sort_values("FAIR overall", ascending=False).reset_index(drop=True)
scorecard.head(20)''')

md("""## 5. Where does OSDR do well — and where are the gaps?

Average score per FAIR principle across the sampled datasets.""")

code('''means = ok[["Findable", "Accessible", "Interoperable", "Reusable"]].mean().round(1)
fig = px.bar(means, orientation="h",
             labels={"value": "Average score (0-100)", "index": "FAIR principle"},
             title="Average FAIR principle scores across sampled OSDR datasets",
             text=means.values)
fig.update_layout(showlegend=False, height=350)
fig.show()''')

code('''# Which individual sub-criteria are most often missing?
subcrit = [c for c in ok.columns if c[:2] in ("F1","F2","F4","A1","I1","I2","I3","R1")]
gap = (100 * (1 - ok[subcrit].mean())).round(1).sort_values(ascending=False)
fig2 = px.bar(gap, orientation="h",
              labels={"value": "% of datasets missing this", "index": "FAIR criterion"},
              title="Most common FAIR metadata gaps in OSDR")
fig2.update_layout(showlegend=False, height=500)
fig2.show()''')

code('''# Distribution of overall FAIR scores
fig3 = px.histogram(ok, x="FAIR overall", nbins=20,
                    title="Distribution of overall FAIR scores")
fig3.update_layout(height=350)
fig3.show()''')

md(r"""## 6. Next steps for the publication tool

This notebook is the **FAIR backbone**. Natural extensions:

- **Drill-down explorer** — pick any accession and render its assays, samples
  and data columns via `/v2/dataset/{acc}/assays/` and `/v2/query/data/`.
- **Data storytelling** — join FAIR scores with `study factor type` / `organism`
  to narrate *what* science is well-described vs. under-documented.
- **Submitter feedback** — turn the gap chart into per-dataset, actionable
  "to improve reusability, add X" reports.
- **Refresh on schedule** — run with `MAX_DATASETS = None` to score the whole
  repository and track FAIR maturity over time.""")

nb["cells"] = cells
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3",
                                "language": "python"}
with open("OSDR_FAIR_assessment.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print("Wrote OSDR_FAIR_assessment.ipynb")
