# AGENTS.md: SPEI-<!-- claim:spei-months -->6<!-- /claim --> drought return levels
<!-- claim-sources
spei-months: curl -fsS 'https://data.humdata.org/api/3/action/package_show?id=global-drought-hazard' | python3 -c 'import json, re, sys; print(re.search(r"\((\d+)-month SPEI\)", json.load(sys.stdin)["result"]["notes"])[1])'
tools: GDAL 3.12.4, DuckDB v2.0.0
-->

<!-- claim:cog-count Words -->
Thirty<!-- /claim --> global Float32 cloud-optimized GeoTIFFs, in <!-- claim:item-count words -->five<!-- /claim --> items of <!-- claim:assets-per-item words -->six<!-- /claim --> assets.
Every number below comes from the HDX dataset page or from a query in this
file. The queries ran against the published objects on 2026-11-20, and a
weekly job reruns them.
<!-- claim-sources
cog-count: duckdb -noheader -list -c "SELECT count(*) FROM read_parquet('https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet') AS i, json_each(to_json(i.assets)) AS a WHERE a.key LIKE 'rp-%' AND json_type(a.value) = 'OBJECT'"
item-count: duckdb -noheader -list -c "SELECT count(*) FROM read_parquet('https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet')"
assets-per-item: duckdb -noheader -list -c "SELECT DISTINCT count(*) FROM read_parquet('https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet') AS i, json_each(to_json(i.assets)) AS a WHERE a.key LIKE 'rp-%' AND json_type(a.value) = 'OBJECT' GROUP BY i.id"
tools: GDAL 3.12.4, DuckDB v2.0.0
-->

## Layout

| Item | Threshold | Assets |
|---|---|---|
| `spei-1.0` | SPEI -1.0 or lower | `rp-25`, `rp-50`, `rp-100`, `rp-250`, `rp-500`, `rp-1000` |
| `spei-1.5` | SPEI -1.5 or lower | same |
| `spei-2.0` | SPEI -2.0 or lower | same |
| `spei-2.5` | SPEI -2.5 or lower | same |
| `spei-3.0` | SPEI -3.0 or lower | same |

A COG URL follows one pattern, with `T` in `1.0 1.5 2.0 2.5 3.0` and `RP` in
`25 50 100 250 500 1000`:

```text
https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-T/global-drought-spei-T-return-period-RP-years.tif
```

Each item also carries `source-rp-*` assets that link the original HDX files.
Those are strip-tiled with no overviews, so read the COGs instead.

## What a pixel means

- The value is a return level from a Poisson-Generalized Pareto point process
  model of the <!-- claim:spei-months -->6<!-- /claim -->-month SPEI, <!-- claim:start-year -->1902<!-- /claim --> to <!-- claim:end-year -->2018<!-- /claim -->. The producer describes it as the
  number of months with SPEI at or below the threshold for the return period.
  The producer does not say whether the count is per drought event. Treat it
  as a relative severity score, and compare values within one threshold.
  <!-- claim-sources
  spei-months: curl -fsS 'https://data.humdata.org/api/3/action/package_show?id=global-drought-hazard' | python3 -c 'import json, re, sys; print(re.search(r"\((\d+)-month SPEI\)", json.load(sys.stdin)["result"]["notes"])[1])'
  start-year: curl -fsS 'https://data.humdata.org/api/3/action/package_show?id=global-drought-hazard' | python3 -c 'import json, sys; print(json.load(sys.stdin)["result"]["dataset_date"].strip("[]").split(" TO ")[0][:4])'
  end-year: curl -fsS 'https://data.humdata.org/api/3/action/package_show?id=global-drought-hazard' | python3 -c 'import json, sys; print(json.load(sys.stdin)["result"]["dataset_date"].strip("[]").split(" TO ")[1][:4])'
  tools: GDAL 3.12.4, DuckDB v2.0.0
  -->
- Higher is worse. Within a threshold, values rise with the return period.
- <!-- claim:band-count Words -->
  One<!-- /claim --> band, Float32, nodata <!-- claim:nodata code -->`-3.4e38`<!-- /claim -->. There are no NaN pixels. Mask on
  `value < -1e38`, not on equality, because <!-- claim:nodata code -->`-3.4e38`<!-- /claim --> prints
  as <!-- claim:nodata-printed code -->`-3.39999995214436e+38`<!-- /claim -->.
  <!-- claim-sources
  band-count: duckdb -noheader -list -c "SELECT DISTINCT json_array_length(a.value->'bands') FROM read_parquet('https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet') AS i, json_each(to_json(i.assets)) AS a WHERE a.key LIKE 'rp-%' AND json_type(a.value) = 'OBJECT'"
  nodata: gdalinfo /vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-1.0/global-drought-spei-1.0-return-period-100-years.tif | sed -n 's/^ *NoData Value=//p' | sed 's/e+/e/'
  nodata-printed: gdallocationinfo -valonly -wgs84 /vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-1.0/global-drought-spei-1.0-return-period-100-years.tif -30 0
  tools: GDAL 3.12.4, DuckDB v2.0.0
  -->
- The grid is EPSG:4326 at <!-- claim:pixel-size -->0.008333<!-- /claim -->° (<!-- claim:grid-width -->43200<!-- /claim --> x <!-- claim:grid-height -->21600<!-- /claim -->), but the model ran at
  about <!-- claim:model-resolution -->0.5<!-- /claim -->°. The fine grid is a bilinear resampling and adds no detail. Do
  not report results at a scale finer than <!-- claim:model-resolution -->0.5<!-- /claim -->°.
  <!-- claim-sources
  pixel-size: gdalinfo /vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-1.0/global-drought-spei-1.0-return-period-100-years.tif | awk -F'[(,]' '/^Pixel Size/ {printf "%.6f\n", $2}'
  grid-width: gdalinfo /vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-1.0/global-drought-spei-1.0-return-period-100-years.tif | awk '/^Size is/ {print $3 + 0}'
  grid-height: gdalinfo /vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-1.0/global-drought-spei-1.0-return-period-100-years.tif | awk '/^Size is/ {print $4 + 0}'
  model-resolution: curl -fsS 'https://data.humdata.org/api/3/action/package_show?id=global-drought-hazard' | python3 -c 'import json, re, sys; print(re.search(r"resolution of about ([0-9.]+) degrees", json.load(sys.stdin)["result"]["notes"])[1])'
  tools: GDAL 3.12.4, DuckDB v2.0.0
  -->
- Oceans are nodata. At SPEI -2.0 and below, land cells with no model
  estimate are nodata too. Coverage at the 100-year return period falls
  from <!-- claim:valid-pct-1.0 -->25.99<!-- /claim -->% of the grid at SPEI -1.0 to <!-- claim:valid-pct-3.0 -->0.44<!-- /claim -->% at SPEI -3.0. Much of the SPEI -3.0
  coverage is in Greenland and the Canadian Arctic Archipelago (see the item
  thumbnail).
  <!-- claim-sources
  valid-pct-1.0: duckdb -noheader -list -c "SELECT round(assets['rp-100'].bands[1].statistics.valid_percent, 2) FROM read_parquet('https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet') WHERE id = 'spei-1.0'"
  valid-pct-3.0: duckdb -noheader -list -c "SELECT round(assets['rp-100'].bands[1].statistics.valid_percent, 2) FROM read_parquet('https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet') WHERE id = 'spei-3.0'"
  tools: GDAL 3.12.4, DuckDB v2.0.0
  -->
- The producer says the data "should not be used for local or regional
  applications".

## Recipes

Coverage and mean per threshold, from the item index. Each row is the 100-year
asset of one item:

<!-- claim:recipe-coverage -->
```sql
SELECT id,
       round(assets."rp-100".bands[1].statistics.valid_percent, 2) AS valid_pct,
       round(assets."rp-100".bands[1].statistics.mean, 3) AS mean_months
FROM read_parquet('https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet')
ORDER BY id;
-- Output (GDAL 3.12.4, DuckDB v2.0.0):
-- spei-1.0  25.99  2.994
-- spei-1.5  25.99  2.436
-- spei-2.0  22.45  1.853
-- spei-2.5   4.47  1.263
-- spei-3.0   0.44  1.203
```
<!-- /claim -->

A return-level curve for one point, Nairobi (36.82 E, 1.29 S), at SPEI -1.5.
GDAL reads only the tile it needs:

<!-- claim:recipe-nairobi-curve -->
```bash
B=/vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-1.5
for rp in 25 50 100 250 500 1000; do
  printf '%s ' "$rp"
  gdallocationinfo -valonly -wgs84 "$B/global-drought-spei-1.5-return-period-$rp-years.tif" 36.82 -1.29 \
    | awk '{printf "%.2f\n", $1}'
done
# Output (GDAL 3.12.4, DuckDB v2.0.0):
# 25 1.74
# 50 1.90
# 100 1.98
# 250 2.04
# 500 2.06
# 1000 2.07
```
<!-- /claim -->

The same point at the 100-year return period across thresholds. Nairobi has
no estimate at SPEI -2.0 and below, so those print as nodata:

<!-- claim:recipe-nairobi-thresholds -->
```bash
for t in 1.0 1.5 2.0; do
  v=$(gdallocationinfo -valonly -wgs84 \
    "/vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-$t/global-drought-spei-$t-return-period-100-years.tif" \
    36.82 -1.29)
  awk -v t="$t" -v v="$v" 'BEGIN { if (v < -1e38) print t, "nodata"; else printf "%s %.2f\n", t, v }'
done
# Output (GDAL 3.12.4, DuckDB v2.0.0):
# 1.0 3.38
# 1.5 1.98
# 2.0 nodata
```
<!-- /claim -->

Clip the Horn of Africa (40 to 52 E, 2 S to 15 N) at SPEI -2.0, 100 years,
to a local GeoTIFF and summarize it:

<!-- claim:recipe-horn -->
```bash
gdal_translate -q -srcwin 26400 9000 1440 2040 \
  /vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-2.0/global-drought-spei-2.0-return-period-100-years.tif \
  horn.tif
gdalinfo -stats horn.tif | grep -E 'Size is|STATISTICS_(MAXIMUM|MEAN|VALID_PERCENT)'
# Output (GDAL 3.12.4, DuckDB v2.0.0):
# Size is 1440, 2040
# STATISTICS_MAXIMUM=3.2503819465637
# STATISTICS_MEAN=1.816493715523
# STATISTICS_VALID_PERCENT=47.43
```
<!-- /claim -->

In Python, `rasterio.open(url)` with the same HTTPS URL works. Read an
overview level (`out_shape`) for continental views; level 3 of the <!-- claim:pixel-size-short -->0.0083<!-- /claim -->°
grid is still finer than the <!-- claim:model-resolution -->0.5<!-- /claim -->° model.
<!-- claim-sources
pixel-size-short: gdalinfo /vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-1.0/global-drought-spei-1.0-return-period-100-years.tif | awk -F'[(,]' '/^Pixel Size/ {printf "%.4f\n", $2}'
model-resolution: curl -fsS 'https://data.humdata.org/api/3/action/package_show?id=global-drought-hazard' | python3 -c 'import json, re, sys; print(re.search(r"resolution of about ([0-9.]+) degrees", json.load(sys.stdin)["result"]["notes"])[1])'
tools: GDAL 3.12.4, DuckDB v2.0.0
-->
