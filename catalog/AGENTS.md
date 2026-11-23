# AGENTS.md: Global Drought Hazard

A Portolan mirror of the IFHV [Global Drought Hazard](https://data.humdata.org/dataset/global-drought-hazard)
rasters (Weller & Mann, <!-- claim:citation-year -->2022<!-- /claim -->), published on the Humanitarian Data Exchange
under CC BY <!-- claim:license-version -->4.0<!-- /claim -->. The upstream dataset is static: HDX shows the last change
on <!-- claim:hdx-last-change -->2023-01-16<!-- /claim -->.
<!-- claim-sources
citation-year: curl -fsS 'https://data.humdata.org/api/3/action/package_show?id=global-drought-hazard' | python3 -c 'import json, re, sys; print(re.search(r"Mann, Holger \((\d{4})\)", json.load(sys.stdin)["result"]["caveats"])[1])'
license-version: curl -fsS https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/collection.json | python3 -c 'import json, sys; print(json.load(sys.stdin)["license"].rsplit("-", 1)[1])'
hdx-last-change: curl -fsS 'https://data.humdata.org/api/3/action/package_show?id=global-drought-hazard' | python3 -c 'import json, sys; print(json.load(sys.stdin)["result"]["last_modified"][:10])'
tools: GDAL 3.12.4, DuckDB v2.0.0
-->

## Contents

<!-- claim:collection-count Words -->
One<!-- /claim --> collection, `drought-hazard`: <!-- claim:cog-count -->30<!-- /claim --> global Float32 COGs of SPEI-<!-- claim:spei-months -->6<!-- /claim --> extreme
value return levels, <!-- claim:item-count words -->five<!-- /claim --> thresholds (items) by <!-- claim:assets-per-item words -->six<!-- /claim --> return periods (assets).
Read [drought-hazard/AGENTS.md](drought-hazard/AGENTS.md) for the URL pattern,
the value semantics, and recipes that run.
<!-- claim-sources
collection-count: curl -fsS https://data.source.coop/portolan-mirrors/global-drought-hazard/catalog.json | python3 -c 'import json, sys; print(sum(link["rel"] == "child" for link in json.load(sys.stdin)["links"]))'
cog-count: duckdb -noheader -list -c "SELECT count(*) FROM read_parquet('https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet') AS i, json_each(to_json(i.assets)) AS a WHERE a.key LIKE 'rp-%' AND json_type(a.value) = 'OBJECT'"
spei-months: curl -fsS 'https://data.humdata.org/api/3/action/package_show?id=global-drought-hazard' | python3 -c 'import json, re, sys; print(re.search(r"\((\d+)-month SPEI\)", json.load(sys.stdin)["result"]["notes"])[1])'
item-count: duckdb -noheader -list -c "SELECT count(*) FROM read_parquet('https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet')"
assets-per-item: duckdb -noheader -list -c "SELECT DISTINCT count(*) FROM read_parquet('https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet') AS i, json_each(to_json(i.assets)) AS a WHERE a.key LIKE 'rp-%' AND json_type(a.value) = 'OBJECT' GROUP BY i.id"
tools: GDAL 3.12.4, DuckDB v2.0.0
-->

Root STAC: `https://data.source.coop/portolan-mirrors/global-drought-hazard/catalog.json`.
The item index `drought-hazard/items.parquet` lists every item and asset in
one file.

## Before you use it

- The model ran at about <!-- claim:model-resolution -->0.5<!-- /claim -->°. The published <!-- claim:pixel-size-short -->0.0083<!-- /claim -->° grid is a bilinear
  resampling for display.
  <!-- claim-sources
  model-resolution: curl -fsS 'https://data.humdata.org/api/3/action/package_show?id=global-drought-hazard' | python3 -c 'import json, re, sys; print(re.search(r"resolution of about ([0-9.]+) degrees", json.load(sys.stdin)["result"]["notes"])[1])'
  pixel-size-short: gdalinfo /vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-1.0/global-drought-spei-1.0-return-period-100-years.tif | awk -F'[(,]' '/^Pixel Size/ {printf "%.4f\n", $2}'
  tools: GDAL 3.12.4, DuckDB v2.0.0
  -->
- The producer says it "should not be used for local or regional
  applications".
- The producer does not fully define the unit ("number of months"). Compare
  values within one threshold, not as absolute counts.

## License and citation

CC BY <!-- claim:license-version -->4.0<!-- /claim -->. Cite: Weller, Daniel & Mann, Holger (<!-- claim:citation-year -->2022<!-- /claim -->): Global Drought Hazard.
A global raster data set of extreme value analyses of the Standardized
Precipitation Evapotranspiration Index via Poisson-Generalized Pareto Point
Process modelling. Distributed by The Humanitarian Data Exchange: Institute
for International Law of Peace and Armed Conflict.
<!-- claim-sources
license-version: curl -fsS https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/collection.json | python3 -c 'import json, sys; print(json.load(sys.stdin)["license"].rsplit("-", 1)[1])'
citation-year: curl -fsS 'https://data.humdata.org/api/3/action/package_show?id=global-drought-hazard' | python3 -c 'import json, re, sys; print(re.search(r"Mann, Holger \((\d{4})\)", json.load(sys.stdin)["result"]["caveats"])[1])'
tools: GDAL 3.12.4, DuckDB v2.0.0
-->

## Maintenance

Build scripts and metadata are in
[nlebovits/global-drought-hazard](https://github.com/nlebovits/global-drought-hazard).
Report problems there.
