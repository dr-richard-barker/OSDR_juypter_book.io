"""Generate `OSDR_fairness_report.ipynb` — a submitter-facing tool: pick a dataset,
get a FAIR scorecard plus a prioritised, actionable list of how to improve it.
Run: python _make_fairness_report_notebook.py  (then nbconvert --execute)
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []
md = lambda s: cells.append(nbf.v4.new_markdown_cell(s))
code = lambda s: cells.append(nbf.v4.new_code_cell(s))

md(r"""# 📋 "Improve your FAIRness" — a per-dataset report

The [FAIR assessment chapter](OSDR_FAIR_assessment.ipynb) scores the *whole*
repository. This is the **submitter-facing flip side**: point it at **one
accession** and it produces a **FAIR report card** plus a **prioritised list of
concrete fixes** — what's missing and exactly how to improve it.

> 🚀 Run it live (rocket icon), change `ACC`, and re-run to audit any OSDR dataset.""")

code('''import requests
import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook_connected"

API = "https://visualization.osdr.nasa.gov/biodata/api/v2"
ACC = "OSD-120"     # <<< put your accession here and re-run''')

md("""## 1. The FAIR rubric (with fixes)

Each check maps to a FAIR sub-principle and carries an **actionable
recommendation** that fires when the check fails — so the output is advice, not
just a score.""")

code('''def present(meta, key):
    return meta.get(key) not in (None, "", [], {}, "n/a", "N/A")

def fair_checks(meta):
    """Return rows of (principle, check, passed, recommendation)."""
    def any_present(*keys):
        return any(present(meta, k) for k in keys)
    rows = [
        # Findable
        ("Findable", "Has an accession / identifier", any_present("accession", "identifiers", "study identifier"),
         "Register a stable accession/identifier."),
        ("Findable", "Rich title + description", present(meta, "study title") and present(meta, "study description"),
         "Add a descriptive study title AND a full study description."),
        ("Findable", "Organism indexed", present(meta, "organism"),
         "Record the organism in the study characteristics."),
        ("Findable", "Public release date set", present(meta, "study public release date"),
         "Set a public release date so the dataset is time-stamped and findable."),
        # Accessible
        ("Accessible", "Retrievable via the API", True,
         "—"),
        ("Accessible", "Authoritative source URL", present(meta, "authoritative source url"),
         "Provide an authoritative source URL for the record."),
        # Interoperable
        ("Interoperable", "Assay technology type (controlled term)", present(meta, "study assay technology type"),
         "Specify the assay technology type using a controlled vocabulary term."),
        ("Interoperable", "Measurement type", present(meta, "study assay measurement type"),
         "Specify the assay measurement type."),
        ("Interoperable", "ISA characteristics / factors", any_present("characteristics", "study factor type"),
         "Add ISA study characteristics and experimental factor types."),
        ("Interoperable", "External data-source linkage", any_present("data source accession", "project link"),
         "Link an external data-source accession (e.g. GEO/SRA) or a project link."),
        # Reusable
        ("Reusable", "Protocols described", present(meta, "study protocol description"),
         "Add descriptions of the study protocols (collection, extraction, processing)."),
        ("Reusable", "Explicit licence", False,
         "Add an explicit licence. (Note: the OSDR API exposes no licence field today, so this fails repository-wide — a systemic gap to flag upstream.)"),
        ("Reusable", "Provenance: funding / grant", any_present("study funding agency", "study grant number"),
         "Record the funding agency and grant number for provenance."),
        ("Reusable", "Linked publication", any_present("study publication title", "study publication author list"),
         "Link the associated publication (title + authors)."),
    ]
    return pd.DataFrame(rows, columns=["principle", "check", "passed", "recommendation"])''')

md("## 2. Your FAIR report card")

code('''meta = requests.get(f"{API}/dataset/{ACC}/", timeout=60).json()[ACC]["metadata"]
title = meta.get("study title", "")
print(f"{ACC}: {title[0] if isinstance(title, list) else title}\\n")

checks = fair_checks(meta)
# per-principle score
score = (checks.groupby("principle")["passed"].mean() * 100).round(0)
score = score.reindex(["Findable", "Accessible", "Interoperable", "Reusable"])
overall = round(score.mean(), 0)
print(f"Overall FAIR score: {overall:.0f}/100")

fig = px.bar(score, range_y=[0, 100], text=score.values,
             labels={"value": "score", "index": "FAIR principle"},
             title=f"{ACC} — FAIR report card (overall {overall:.0f}/100)",
             color=score.index, color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(height=380, showlegend=False)
fig.show()''')

code('''# Full checklist: what passed (✓) and what didn't (✗)
view = checks.copy()
view["status"] = view["passed"].map({True: "✓ pass", False: "✗ fix"})
view[["principle", "check", "status"]]''')

md(r"""## 3. Prioritised action list — how to improve this dataset

Just the failing checks, with the specific fix for each. Work top-to-bottom to
raise the score.""")

code('''todo = checks[~checks["passed"]][["principle", "check", "recommendation"]].reset_index(drop=True)
if len(todo):
    print(f"{len(todo)} improvement(s) would raise {ACC}'s FAIR score:\\n")
    for i, r in todo.iterrows():
        print(f"{i+1}. [{r['principle']}] {r['check']}")
        print(f"   → {r['recommendation']}\\n")
else:
    print(f"{ACC} passes every check in this rubric. 🎉")
todo''')

md("""## 4. You're not alone — the most common gaps across OSDR

To show where effort matters most, we score a sample of datasets and rank the
checks that fail most often. These are the **highest-impact fixes** for the
repository as a whole.""")

code('''ids = list(requests.get(f"{API}/datasets/", timeout=60).json())[:60]   # raise for a bigger sample
fail_counts = pd.Series(0, index=fair_checks({}).set_index(["principle", "check"]).index)
n = 0
for acc in ids:
    try:
        m = requests.get(f"{API}/dataset/{acc}/", timeout=60).json()[acc]["metadata"]
    except Exception:
        continue
    c = fair_checks(m).set_index(["principle", "check"])
    fail_counts = fail_counts.add((~c["passed"]).astype(int), fill_value=0)
    n += 1

gap = (100 * fail_counts / n).round(0).sort_values(ascending=True)
gap.index = [f"{p}: {c}" for p, c in gap.index]
fig = px.bar(gap, orientation="h", labels={"value": "% of datasets missing this", "index": ""},
             title=f"Most common FAIR gaps across {n} OSDR datasets")
fig.update_layout(height=480, showlegend=False)
fig.show()''')

md(r"""## 5. Use it on your own dataset

Change **`ACC`** at the top to any accession and re-run — you'll get that
dataset's report card and a tailored fix list. Submitters can use this *before*
release to close FAIR gaps; reviewers can use it to give concrete feedback.

```{tip}
The single most common Reusability gap is the **missing licence field** — it
fails for every dataset because the API doesn't expose one. That's a systemic
fix for OSDR itself, not any individual submitter.
```""")

nb["cells"] = cells
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
with open("OSDR_fairness_report.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print("Wrote OSDR_fairness_report.ipynb")
