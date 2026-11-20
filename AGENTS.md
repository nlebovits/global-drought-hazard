# Agent instructions

This repository builds and publishes a Portolan mirror of the IFHV Global
Drought Hazard rasters from HDX. The published catalog is
`https://data.source.coop/portolan-mirrors/global-drought-hazard/catalog.json`.

## The build

`tools/build.sh` rebuilds every COG in `catalog/` from the HDX files in
`tools/hdx_resources.json`. Edit the `.portolan/metadata.yaml` files, never a
generated `README.md`. Run `tools/stac.sh` after you edit metadata.
`portolan add` overwrites fields that `tools/finalize_stac.py` sets, so never
run it alone. Keep `--data-scope local` on `portolan check`: the default scope
downloads the HDX originals and takes about ten minutes.

## Data never enters git

`.gitignore` excludes every data format. Do not commit a COG.

## Published agent guides

Every query in a `catalog/**/AGENTS.md` runs in `tests/test_agent_claims.py`
against the published data. Run it after you change a guide. A fence states
its result in comment lines, and every number there must occur in the output.
Every number in a guide comes from the HDX dataset page or from a query in the
same guide.
