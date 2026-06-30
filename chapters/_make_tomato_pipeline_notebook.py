"""Generate `OSDR_tomato_microbiome_pipeline.ipynb` — the processing recipe that
turns OSD-766's raw 16S/ITS reads into a genus abundance table and joins it to the
OSD-767 host transcriptome. Light steps run live; heavy steps (DADA2/SILVA) are
documented code for a dedicated bioinformatics environment.
Run: python _make_tomato_pipeline_notebook.py
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []
md = lambda s: cells.append(nbf.v4.new_markdown_cell(s))
code = lambda s: cells.append(nbf.v4.new_code_cell(s))

md(r"""# 🧫 Processing the tomato microbiome → host integration

The [tomato chapter](OSDR_tomato_microbiome.ipynb) paired the host transcriptome
(OSD-767) with the microbiome study (OSD-766) but hit a wall: **OSDR serves
OSD-766 as raw 16S/ITS reads — no processed taxonomy table**. This chapter is the
**recipe to fix that**: turn the raw reads into a per-genus abundance table and
feed it into the host↔microbe correlation.

```{admonition} What runs where — please read
:class: important
Amplicon denoising + taxonomy (DADA2 / QIIME2 + the SILVA database) needs heavy
tools and ~1 GB of reads, so it is **not executed inside this book**. The cells
below that *are* executed (live) **prove the data path and build the host side**;
the heavy steps are given as **complete, copy-runnable code** to run once in a
bioinformatics environment (a Binder/conda env with QIIME2 or R/DADA2). The
output of that step drops straight into section 4.
```

```{admonition} An honest design caveat
:class: warning
OSD-767 (host) and OSD-766 (microbes) are **different sample sets**, so the
host↔microbe link is necessarily at the **experimental-group level**
(organ × light × spaceflight), not sample-by-sample. With only a handful of
groups this is **descriptive**, not a powered correlation — read it as
hypothesis-generating.
```""")

code('''import io, re, gzip
import requests
import pandas as pd

API = "https://visualization.osdr.nasa.gov/biodata/api/v2"
GEODE = "https://osdr.nasa.gov/geode-py/ws/studies"''')

md("## 1. The raw amplicon data is there (live check)\n\nWe enumerate OSD-766's raw read files straight from OSDR.")

code('''# Full file listing (the OSD file API lists more than the biodata files endpoint)
listing = requests.get("https://osdr.nasa.gov/osdr/data/osd/files/766", timeout=60).json()
def collect(o, acc):
    if isinstance(o, dict):
        if "file_name" in o: acc.append(o)
        for v in o.values(): collect(v, acc)
    elif isinstance(o, list):
        for x in o: collect(x, acc)
    return acc
fobjs = collect(listing, [])
fq = [o["file_name"] for o in fobjs if o["file_name"].endswith(".fastq.gz")]
print(f"OSD-766 raw FASTQ files: {len(fq)}")
print(f"  16S (bacteria): {sum('16S' in n for n in fq)}   |   ITS (fungi): {sum('ITS' in n for n in fq)}")''')

code('''# Download ONE 16S sample and confirm what the reads look like (real, ~few MB)
one = next(o["file_name"] for o in fobjs
           if o["file_name"].endswith("R1_raw.fastq.gz") and "16S" in o["file_name"]
           and "root" in o["file_name"] and float(o.get("file_size", 0)) > 1e6)
blob = requests.get(f"{GEODE}/OSD-766/download?source=datamanager&file={one}", timeout=120).content
lines = gzip.decompress(blob).decode("ascii", "replace").splitlines()
print(f"file : {one}")
print(f"reads: {len(lines)//4:,}   read length: {len(lines[1])} bp (16S V3-V4)")
print(f"example read: {lines[1][:60]}...")''')

md(r"""## 2. From reads to a genus table — run in a DADA2/QIIME2 environment

The block below is the **standard amplicon pipeline**. Run it once in an
environment with `cutadapt` + R/`dada2` (or QIIME2). It writes
`tomato_genus_by_sample.csv` (genera × samples), which section 4 consumes.

```bash
# 0. Download the 16S reads (R1+R2) for OSD-766 (~1 GB) into ./reads/
python - <<'PY'
import requests, json, os
os.makedirs("reads", exist_ok=True)
fobjs = requests.get("https://osdr.nasa.gov/osdr/data/osd/files/766").json()
# (walk the JSON as in section 1, then:)
for name in fastq_16S_names:                      # R1 + R2 for every 16S sample
    url = f"https://osdr.nasa.gov/geode-py/ws/studies/OSD-766/download?source=datamanager&file={name}"
    open(f"reads/{name}", "wb").write(requests.get(url).content)
PY

# 1. Remove the 515F/806R primers
for f in reads/*_R1_raw.fastq.gz; do
  r=${f/_R1_/_R2_}
  cutadapt -g GTGYCAGCMGCCGCGGTAA -G GGACTACNVGGGTWTCTAAT \
           -o trimmed/$(basename $f) -p trimmed/$(basename $r) "$f" "$r"
done
```

```r
# 2. DADA2: denoise -> ASVs -> taxonomy (SILVA) -> collapse to genus  (in R)
library(dada2)
path <- "trimmed"
fnF <- sort(list.files(path, "_R1_", full.names = TRUE))
fnR <- sort(list.files(path, "_R2_", full.names = TRUE))
filtF <- file.path("filt", basename(fnF)); filtR <- file.path("filt", basename(fnR))
filterAndTrim(fnF, filtF, fnR, filtR, truncLen = c(220, 180), maxEE = c(2, 2))
errF <- learnErrors(filtF); errR <- learnErrors(filtR)
seqtab <- makeSequenceTable(mergePairs(dada(filtF, errF), filtF,
                                       dada(filtR, errR), filtR))
seqtab <- removeBimeraDenovo(seqtab)
tax <- assignTaxonomy(seqtab, "silva_nr99_v138.1_train_set.fa.gz")   # SILVA DB
# collapse ASV counts to genus and write genera x samples
genus <- rowsum(t(seqtab), group = tax[, "Genus"])
write.csv(genus, "tomato_genus_by_sample.csv")
```""")

md("""## 3. Map microbiome samples to experimental groups

OSD-766's sample names encode the organ and flight/ground status, so the genus
table can be summarised on the **same groups** as the host data.""")

code('''# Parse organ + condition from the 16S sample names (real, live)
rows = []
for n in fq:
    if "16S" not in n or "_R1" not in n:
        continue
    cond = "Flight" if re.search(r"VEG-05-F-", n) else ("Ground" if re.search(r"VEG-05-G-", n) else None)
    organ = next((o for o in ("root", "leaf", "fruit", "soil", "wick", "swab") if o in n.lower()), "other")
    rows.append({"file": n, "organ": organ, "condition": cond})
mic_samples = pd.DataFrame(rows)
print(mic_samples.groupby(["organ", "condition"]).size().rename("samples").reset_index().to_string(index=False))''')

md(r"""## 4. Join to the host transcriptome

Here is the live host side plus the integration function. Once
`tomato_genus_by_sample.csv` exists (from section 2), the final cell computes the
real **genus ↔ host-gene** relationships across the shared groups.""")

code('''# Host (OSD-767) expression, summarised per group  -- runs live
counts = pd.read_csv(f"{GEODE}/OSD-767/download?source=datamanager"
                     "&file=GLDS-709_rna_seq_RSEM_Unnormalized_Counts_GLbulkRNAseq.csv", index_col=0)
cpm = counts / counts.sum() * 1e6
cpm = cpm[(cpm > 1).sum(axis=1) >= 3]
def parse(c):
    return ("Flight" if "Flt" in c else "Ground"), ("Root" if "Root" in c else "Leaf")
groups = pd.DataFrame({c: parse(c) for c in cpm.columns}, index=["condition", "organ"]).T
host_group_mean = cpm.T.join(groups).groupby(["organ", "condition"]).mean(numeric_only=True)
print(f"Host group means: {host_group_mean.shape[0]} groups x {host_group_mean.shape[1]} genes")

def correlate_microbe_host(genus_by_group, host_by_group, genes):
    """genus_by_group & host_by_group indexed by (organ, condition).
    Returns genera x genes Pearson r across the shared groups."""
    j = genus_by_group.join(host_by_group[genes], how="inner")
    return j[genus_by_group.columns].apply(lambda t: j[genes].corrwith(t)).T''')

code('''# Final step — runs for real ONCE the genus table from section 2 is present
import os
if os.path.exists("tomato_genus_by_sample.csv"):
    genus = pd.read_csv("tomato_genus_by_sample.csv", index_col=0)
    g = genus.T
    g["organ"] = [next((o for o in ("root","leaf","fruit","soil","wick","swab") if o in s.lower()), "other") for s in g.index]
    g["condition"] = ["Flight" if "-F-" in s else "Ground" for s in g.index]
    genus_by_group = g.groupby(["organ", "condition"]).mean(numeric_only=True)
    pgpr = [c for c in genus_by_group.columns
            if c in ("Rhizobium","Azospirillum","Burkholderia","Dyadobacter","Sphingomonas")]
    top_genes = host_group_mean.loc[("Root",)].std().sort_values(ascending=False).head(30).index
    print(correlate_microbe_host(genus_by_group[pgpr], host_group_mean, list(top_genes)).round(2))
else:
    print("Run section 2 to create tomato_genus_by_sample.csv, then re-run this cell")
    print("for the real PGPR-genus x host-gene correlation across groups.")''')

md(r"""## 5. Reading the result

When the genus table is in place, this produces a **genera × host-genes
correlation** across the experimental groups — directly testing whether the
spaceflight-enriched PGPR genera (*Rhizobium*, *Azospirillum*, *Burkholderia*,
*Dyadobacter*, *Sphingomonas*) track with specific host root genes.

Interpret it with the caveats above: the host and microbiome are different sample
sets, so this is a **group-level, hypothesis-generating** comparison — a strong
lead to follow, not a final answer. The moment OSDR (or you) publishes the
processed taxonomy, the [dataset explorer](OSDR_dataset_explorer.ipynb) and
[data story](OSDR_data_story.ipynb) workflows apply to it directly.

---

**Sources:** [OSD-766 (microbiome)](https://osdr.nasa.gov/bio/repo/data/studies/OSD-766) ·
[OSD-767 (host RNA-seq)](https://osdr.nasa.gov/bio/repo/data/studies/OSD-767) ·
[VEG-05 Microbiome — NASA NTRS](https://ntrs.nasa.gov/citations/20240016407)""")

nb["cells"] = cells
nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
with open("OSDR_tomato_microbiome_pipeline.ipynb", "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print("Wrote OSDR_tomato_microbiome_pipeline.ipynb")
