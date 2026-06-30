"""Generate `OSDR_fair_over_time.ipynb` — the full-repository FAIR maturity tracker.
Reads the committed snapshots (fair_latest.csv / fair_history.csv) produced by
_fair_snapshot.py, so the book build stays fast. Run: python _make_fair_over_time_notebook.py
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []
md = lambda s: cells.append(nbf.v4.new_markdown_cell(s))
code = lambda s: cells.append(nbf.v4.new_code_cell(s))

md(r"""# 📈 OSDR FAIR maturity — the whole repository, over time

The [FAIR assessment](OSDR_FAIR_assessment.ipynb) scores a live sample; the
[fairness report](OSDR_fairness_report.ipynb) audits one dataset. This page is the
**big picture**: **every** OSDR dataset scored, and tracked **over time** so the
repository's FAIR maturity can be watched as it improves.

The scoring is done by [`_fair_snapshot.py`](_fair_snapshot.py) and recorded in
two committed files — `fair_latest.csv` (this run's per-dataset scores) and
`fair_history.csv` (one summary row per run). A scheduled GitHub Action re-runs it
monthly, so the trend below grows on its own.""")

code('''import pandas as pd
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook_connected"

latest = pd.read_csv("fair_latest.csv")
history = pd.read_csv("fair_history.csv")
print(f"Latest snapshot: {len(latest)} datasets scored")
print(f"History: {len(history)} snapshot(s) recorded")''')

md("## 1. The current full-repository picture")

code('''# Distribution of overall FAIR scores across every dataset
fig = px.histogram(latest, x="FAIR overall", nbins=20,
                   title=f"Overall FAIR score across all {len(latest)} OSDR datasets")
fig.update_layout(height=360)
fig.show()''')

code('''# Mean score per FAIR principle (whole repository)
means = latest[["Findable", "Accessible", "Interoperable", "Reusable"]].mean().round(1)
fig = px.bar(means, range_y=[0, 100], text=means.values,
             labels={"value": "mean score", "index": "FAIR principle"},
             title="Mean FAIR principle scores across the whole repository")
fig.update_layout(height=360, showlegend=False)
fig.show()''')

code('''# Where are the weak spots? Plant subset vs the rest
PLANT = "arabidopsis|thaliana|brassica|oryza|solanum|plant"
latest["group"] = latest["organism"].str.contains(PLANT, case=False, na=False).map(
    {True: "Plant datasets", False: "All other organisms"})
by_group = latest.groupby("group")[["Findable", "Accessible", "Interoperable", "Reusable"]].mean().round(1)
fig = px.bar(by_group.T, barmode="group", range_y=[0, 100],
             labels={"value": "mean score", "index": "FAIR principle"},
             title="FAIR scores: plant datasets vs the rest of OSDR")
fig.update_layout(height=380)
fig.show()''')

md(r"""## 2. Tracking FAIR maturity over time

Each scheduled run appends a row to `fair_history.csv`. The trend below starts with
the first snapshot and fills in as the Action runs — a living record of whether the
repository is getting more FAIR.""")

code('''hist_long = history.melt("date", value_vars=["Findable", "Accessible", "Interoperable", "Reusable"],
                         var_name="FAIR principle", value_name="mean score")
fig = px.line(hist_long, x="date", y="mean score", color="FAIR principle", markers=True,
              range_y=[0, 100], title="OSDR FAIR maturity over time (mean score per principle)")
fig.update_layout(height=420)
fig.show()''')

code('''# Snapshot table: dataset count, plant share, and overall FAIR at each time point
history[["date", "n_datasets", "n_plant", "plant_pct", "FAIR overall"]]''')

md(r"""## 3. How this updates

- **Automatically:** `.github/workflows/fair_snapshot.yml` runs `_fair_snapshot.py`
  on a monthly cron and commits the refreshed CSVs — the charts above then reflect
  the new data on the next book build.
- **Manually:** `cd chapters && python _fair_snapshot.py` re-scores the whole
  repository now and appends today's snapshot.

```{tip}
The persistent **Reusability** gap you'll see is the missing licence field
(API-wide) plus, for many datasets, absent processed/analysis-ready data — the
highest-impact targets for raising OSDR's FAIR score over time.
```""")

nb["cells"] = cells
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
with open("OSDR_fair_over_time.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print("Wrote OSDR_fair_over_time.ipynb")
