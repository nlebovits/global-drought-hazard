# Global Drought Hazard, as a Portolan catalog

This repository builds and maintains a [Portolan](https://www.portolan-sdi.org/)
mirror of the IFHV [Global Drought Hazard](https://data.humdata.org/dataset/global-drought-hazard)
rasters (Weller & Mann, 2022): extreme value return levels of the 6-month
SPEI, 1902 to 2018, for five thresholds and six return periods.

The published catalog is at
[source.coop/portolan-mirrors/global-drought-hazard](https://source.coop/portolan-mirrors/global-drought-hazard).
Open it in the
[data browser](https://browser.portolan-sdi.org/#/external/data.source.coop/portolan-mirrors/global-drought-hazard/catalog.json),
or read a point with GDAL:

```bash
gdallocationinfo -valonly -wgs84 \
  /vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-1.5/global-drought-spei-1.5-return-period-100-years.tif \
  36.82 -1.29
```

Read the [catalog agent guide](catalog/AGENTS.md) before you analyze the data.

## Build

Data never enters git. `tools/build.sh` downloads the 30 HDX GeoTIFFs listed
in `tools/hdx_resources.json`, checks their sizes, and writes one COG per file
into `catalog/drought-hazard/spei-T/` with `tools/make_cog.py`. That script
writes the statistics with numpy, because GDAL 3.8 computes a NaN mean for
these files.

```bash
WORK=/path/to/scratch tools/build.sh
uv run -q --python /usr/bin/python3 --with pillow --with matplotlib --with "numpy<2" \
  python -I tools/make_thumbs.py catalog
tools/stac.sh
```

`tools/stac.sh` runs `portolan add`, then `tools/finalize_stac.py`. That
script writes what the CLI cannot: the `rp-*` data assets with band
statistics, the HDX `source` assets, the renders, `item_assets`, the
1902 to 2018 interval, and the root links. Then `stac.sh` regenerates
`items.parquet` and the READMEs and runs `portolan check --data-scope local`.
With the default scope, the data pass downloads the 18 GB of HDX originals.

`rashid check` reports PTL-DAT-011 on every COG. It is a validator false
positive ([rashid#327](https://github.com/portolan-sdi/rashid/issues/327)).

## Publish

```bash
cd catalog
eval "$(source-coop creds --format env)"
portolan push --dry-run
portolan push
```

`catalog/.env` sets `PORTOLAN_REMOTE=s3://portolan-mirrors/global-drought-hazard/`
and `PORTOLAN_S3_ENDPOINT=https://data.source.coop`. It is not committed.

## Updates

HDX shows the dataset as static, last changed 2023-01-16. If IFHV publishes
new files, update `tools/hdx_resources.json`, rebuild, and publish a new
catalog version.

## Checks

- `.github/workflows/ci.yml`, on every push and pull request: lint, `portolan
  metadata validate`, and `rashid check --no-data` on the STAC JSON.
- `.github/workflows/live-claims.yml`, weekly and on pull requests that edit a
  guide: `tests/test_agent_claims.py` runs every SQL and bash fence in the
  agent guides against the published objects and checks each number its
  comments state, then rashid probes range requests and CORS on the host.
- `links.yml` and `vale.yml` are synced from portolan-ops.
