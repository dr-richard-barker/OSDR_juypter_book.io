"""Score EVERY OSDR dataset on FAIR and record a timestamped snapshot.

Writes two CSVs (read by OSDR_fair_over_time.ipynb):
  - fair_latest.csv   : per-dataset scores from this run (the current full-repo picture)
  - fair_history.csv  : one summary row per run, appended over time (the trend)

Run locally to seed, and on a schedule (see .github/workflows/fair_snapshot.yml)
to accumulate the history. Usage:  python _fair_snapshot.py [--date YYYY-MM-DD]
"""
import argparse
import datetime
import time
import os
import requests
import pandas as pd

API = "https://visualization.osdr.nasa.gov/biodata/api/v2"
PLANT = "arabidopsis|thaliana|brassica|oryza|solanum|plant"


def present(meta, key):
    return meta.get(key) not in (None, "", [], {}, "n/a", "N/A")


def fair_scores(meta):
    p = lambda k: 1 if present(meta, k) else 0
    any_p = lambda *ks: 1 if any(present(meta, k) for k in ks) else 0
    F = [any_p("accession", "identifiers", "study identifier"),
         1 if present(meta, "study title") and present(meta, "study description") else 0,
         p("organism"), p("study public release date")]
    A = [1, p("authoritative source url"), 1]
    I = [p("study assay technology type"), p("study assay measurement type"),
         any_p("characteristics", "study factor type"), any_p("data source accession", "project link")]
    R = [p("study protocol description"), 0,                       # explicit licence: API exposes none
         any_p("study funding agency", "study grant number"),
         any_p("study publication title", "study publication author list")]
    sc = lambda t: round(100 * sum(t) / len(t), 1)
    return sc(F), sc(A), sc(I), sc(R)


def run(date):
    ids = list(requests.get(f"{API}/datasets/", timeout=120).json())
    print(f"Scoring {len(ids)} datasets...")
    rows = []
    for i, acc in enumerate(ids, 1):
        try:
            meta = requests.get(f"{API}/dataset/{acc}/", timeout=60).json()[acc]["metadata"]
        except Exception:
            continue
        f, a, i_, r = fair_scores(meta)
        org = meta.get("organism", "")
        org = org[0] if isinstance(org, list) and org else (org if isinstance(org, str) else "")
        rows.append({"accession": acc, "organism": org, "Findable": f, "Accessible": a,
                     "Interoperable": i_, "Reusable": r,
                     "FAIR overall": round((f + a + i_ + r) / 4, 1)})
        if i % 100 == 0:
            print(f"  {i}/{len(ids)}")
        time.sleep(0.02)

    latest = pd.DataFrame(rows)
    latest.to_csv("fair_latest.csv", index=False)
    print(f"Wrote fair_latest.csv ({len(latest)} datasets)")

    is_plant = latest["organism"].str.contains(PLANT, case=False, na=False)
    summary = {
        "date": date,
        "n_datasets": len(latest),
        "n_plant": int(is_plant.sum()),
        "plant_pct": round(100 * is_plant.mean(), 1),
        "Findable": round(latest["Findable"].mean(), 1),
        "Accessible": round(latest["Accessible"].mean(), 1),
        "Interoperable": round(latest["Interoperable"].mean(), 1),
        "Reusable": round(latest["Reusable"].mean(), 1),
        "FAIR overall": round(latest["FAIR overall"].mean(), 1),
    }
    hist_path = "fair_history.csv"
    hist = pd.read_csv(hist_path) if os.path.exists(hist_path) else pd.DataFrame()
    hist = pd.concat([hist[hist.get("date") != date] if len(hist) else hist,
                      pd.DataFrame([summary])], ignore_index=True)
    hist = hist.sort_values("date")
    hist.to_csv(hist_path, index=False)
    print(f"Appended snapshot for {date} to fair_history.csv (now {len(hist)} snapshot(s))")
    print(summary)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    run(ap.parse_args().date)
