"""v2: curated primary-factor DE contrast per Arabidopsis spaceflight microarray study.

Caches raw CSVs to disk so re-runs are cheap. Parses headers with the csv module
(handles commas inside quoted contrast names). Writes de_cache2.json.
"""
import requests, io, json, csv, os, sys
import pandas as pd

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw_de")
os.makedirs(CACHE_DIR, exist_ok=True)
OUT = sys.argv[1] if len(sys.argv) > 1 else "de_cache2.json"

# Spaceflight studies: file + substrings that must ALL appear in the chosen contrast.
# We target the wild-type / Col-0 Space-Flight vs Ground-Control contrast so every
# study isolates the same factor (spaceflight) in comparable genetic background.
STUDIES = {
    "OSD-44":  ("GLDS-44_array_differential_expression_GLmicroarray.csv",
                ["wild type", "ground control", "space flight"]),
    "OSD-121": ("GLDS-121_array_differential_expression_GLmicroarray.csv",
                ["space flight", "ground control"]),
    "OSD-147": ("GLDS-147_array_differential_expression.csv",
                ["wild type", "ground control", "space flight"]),
    "OSD-205": ("GLDS-205_array_differential_expression.csv",
                ["wild type", "ground control", "space flight"]),
    "OSD-213": ("GLDS-213_array_differential_expression_GLmicroarray.csv",
                ["space flight & ug", "ground control"]),
    "OSD-469": ("GLDS-469_array_differential_expression_GLmicroarray.csv",
                ["space flight", "wild type", "ground"]),
}

def dl_url(acc, fname):
    return f"https://osdr.nasa.gov/geode-py/ws/studies/{acc}/download?source=datamanager&file={fname}"

def fetch(acc, fname):
    path = os.path.join(CACHE_DIR, f"{acc}.csv")
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        return path
    print(f"{acc}: downloading {fname}", flush=True)
    r = requests.get(dl_url(acc, fname), timeout=600)
    with open(path, "wb") as f:
        f.write(r.content)
    print(f"  saved {os.path.getsize(path)/1e6:.0f} MB", flush=True)
    return path

def read_header(path):
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.reader(f)
        return next(reader)

def pick_contrast(cols, must_have):
    """Find the Log2fc column whose lowercased name contains all must_have substrings.

    Rejects cross-background contrasts: if 'wild type' is required, BOTH sides of
    the ')v(' comparison must be wild type (so genotype is not confounded with the
    spaceflight factor). A side that names a KO/mutant on only one arm is skipped.
    """
    cands = []
    for c in cols:
        if not c.lower().startswith("log2fc"):
            continue
        name = c.lower()
        if not all(s in name for s in must_have):
            continue
        # split the two arms of the contrast
        body = name.split("log2fc_", 1)[-1]
        arms = body.split(")v(")
        if len(arms) == 2:
            a, b = arms[0], arms[1]
            if "wild type" in must_have:
                if not ("wild type" in a and "wild type" in b):
                    continue
            # reject if exactly one arm mentions a knockout/mutant
            ko_a = any(k in a for k in ["ko", "mutant", "knockout", "-/-"])
            ko_b = any(k in b for k in ["ko", "mutant", "knockout", "-/-"])
            if ko_a != ko_b:
                continue
        cands.append(c)
    cands.sort(key=len)
    return cands[0] if cands else None

results = {}
SYM_ALL = {}
for acc, (fname, must) in STUDIES.items():
    try:
        path = fetch(acc, fname)
        cols = read_header(path)
        cols = [c.strip() for c in cols]
        # id column
        id_col = next((c for c in ["TAIR", "SYMBOL", "ProbesetID"] if c in cols), None)
        lc = pick_contrast(cols, must)
        if not lc:
            # relax: just need flight + ground
            lc = pick_contrast(cols, ["space flight", "ground"])
        if not lc or not id_col:
            print(f"{acc}: NO MATCH (id={id_col}, contrast among {[c for c in cols if c.lower().startswith('log2fc')][:3]})", flush=True)
            continue
        suffix = lc[len("Log2fc"):]
        adjp = "Adj.p.value" + suffix
        pcol = "P.value" + suffix
        want = {id_col, lc, adjp}
        if "SYMBOL" in cols:
            want.add("SYMBOL")
        df = pd.read_csv(path, usecols=lambda c: c.strip() in want, low_memory=False)
        df.columns = [c.strip() for c in df.columns]
        ren = {id_col: "gene_id", lc: "log2fc", adjp: "adj_p"}
        if "SYMBOL" in df.columns:
            ren["SYMBOL"] = "symbol"
        df = df.rename(columns=ren)
        if "symbol" not in df.columns:
            df["symbol"] = ""
        df["log2fc"] = pd.to_numeric(df["log2fc"], errors="coerce")
        df["adj_p"] = pd.to_numeric(df["adj_p"], errors="coerce")
        df = df.dropna(subset=["gene_id", "log2fc", "adj_p"])
        df["gene_id"] = df["gene_id"].astype(str).str.upper()
        df = df[df["gene_id"].str.startswith("AT")]
        # collapse multi-mapping probes to strongest per gene
        df = df.reindex(df["log2fc"].abs().sort_values(ascending=False).index)
        df = df.drop_duplicates(subset="gene_id", keep="first")
        sig = df[(df["adj_p"] < 0.05) & (df["log2fc"].abs() >= 1.0)]
        # record symbol for every significant locus (first token before '|')
        for g, s in zip(sig["gene_id"], sig["symbol"]):
            if isinstance(s, str) and s and s != "nan" and g not in SYM_ALL:
                SYM_ALL[g] = s.split("|")[0]
        up = int((sig["log2fc"] > 0).sum())
        down = int((sig["log2fc"] < 0).sum())
        top = sig.reindex(sig["log2fc"].abs().sort_values(ascending=False).index).head(50)
        results[acc] = {
            "contrast": lc[len("Log2fc_"):],
            "n_tested": int(len(df)),
            "n_sig": int(len(sig)),
            "n_up": up, "n_down": down,
            "sig_loci": sig["gene_id"].tolist(),
            "sig_lfc": {g: round(float(v), 3) for g, v in zip(sig["gene_id"], sig["log2fc"])},
            "top_loci": [
                {"gene_id": g, "symbol": (s if isinstance(s, str) and s != "nan" else ""),
                 "log2fc": round(float(f), 3), "adj_p": float(p)}
                for g, s, f, p in zip(top["gene_id"], top["symbol"], top["log2fc"], top["adj_p"])
            ],
        }
        print(f"{acc}: {len(df)} tested, {len(sig)} sig ({up} up / {down} down)  contrast={lc[len('Log2fc_'):][:55]}", flush=True)
    except Exception as e:
        import traceback; traceback.print_exc()
        print(f"{acc}: ERROR {type(e).__name__}: {e}", flush=True)

# cross-study recurrence within the flight set
from collections import defaultdict
loci_studies = defaultdict(list)
loci_dir = defaultdict(list)
for acc, d in results.items():
    for g in set(d["sig_loci"]):
        loci_studies[g].append(acc)
        loci_dir[g].append(1 if d["sig_lfc"].get(g, 0) > 0 else -1)

# symbol lookup (all significant loci across studies)
sym = dict(SYM_ALL)

recur = []
for g, studies in loci_studies.items():
    if len(studies) >= 2:
        dirs = loci_dir[g]
        consistent = "up" if all(x > 0 for x in dirs) else ("down" if all(x < 0 for x in dirs) else "mixed")
        recur.append({"gene_id": g, "symbol": sym.get(g, ""), "n_studies": len(studies),
                      "studies": studies, "direction": consistent})
recur.sort(key=lambda r: (-r["n_studies"], r["gene_id"]))

out = {"studies": results, "recurrence": recur, "symbols": sym,
       "n_flight_studies": len(results)}
with open(OUT, "w") as f:
    json.dump(out, f, indent=1)
print(f"\nWROTE {OUT}: {len(results)} flight studies, {len(recur)} recurrent loci (>=2)")
for r in recur[:25]:
    print(f"  {r['gene_id']} ({r['symbol']}): {r['n_studies']} studies [{r['direction']}] {r['studies']}")
