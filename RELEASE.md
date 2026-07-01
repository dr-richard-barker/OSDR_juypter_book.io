# Releasing & minting a Zenodo DOI

The book is citable via [`CITATION.cff`](CITATION.cff); this adds a permanent,
versioned **DOI** by archiving a GitHub release on Zenodo. `.zenodo.json` (repo
root) supplies the archive metadata automatically — you only do the one-time
hook-up and the click.

## One-time setup
1. Sign in to <https://zenodo.org> with your GitHub account.
2. Go to **Zenodo → Account → GitHub**, and flip the switch **ON** for
   `dr-richard-barker/OSDR_juypter_book.io`.

## Cut a release (mints the DOI)
1. On GitHub: **Releases → Draft a new release**.
2. **Tag**: `v1.0` (create it on `main`). **Title**: `v1.0`.
3. Publish. Zenodo automatically archives the release and issues a DOI.

## After the DOI exists
1. Copy the DOI (e.g. `10.5281/zenodo.XXXXXXX`).
2. Add it to:
   - [`CITATION.cff`](CITATION.cff) — add under the top level:
     ```yaml
     identifiers:
       - type: doi
         value: 10.5281/zenodo.XXXXXXX
     ```
   - [`README.md`](README.md) — a DOI badge:
     `[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)`
3. Commit. Future releases get a new version DOI under the same "concept" DOI.

> Metadata (title, authors, keywords, licence = CC0-1.0) comes from `.zenodo.json`.
> If Zenodo rejects the `license` value, set it in the Zenodo deposit UI and it
> will stick for later versions.
