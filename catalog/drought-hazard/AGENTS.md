# AGENTS.md: SPEI-6 drought return levels

Thirty global Float32 cloud-optimized GeoTIFFs, in five items of six assets.
Every number below comes from the HDX dataset page or from a query in this
file. The queries ran against the published objects on 2026-11-20, and a
weekly job reruns them.

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
  model of the 6-month SPEI, 1902 to 2018. The producer describes it as the
  number of months with SPEI at or below the threshold for the return period.
  The producer does not say whether the count is per drought event. Treat it
  as a relative severity score, and compare values within one threshold.
- Higher is worse. Within a threshold, values rise with the return period.
- One band, Float32, nodata `-3.4e38`. There are no NaN pixels. Mask on
  `value < -1e38`, not on equality, because `-3.4e38` prints as
  `-3.39999995214436e+38`.
- The grid is EPSG:4326 at 0.008333° (43200 x 21600), but the model ran at
  about 0.5°. The fine grid is a bilinear resampling and adds no detail. Do
  not report results at a scale finer than 0.5°.
- Oceans are nodata. At SPEI -2.0 and below, land cells with no model
  estimate are nodata too. Coverage at the 100-year return period falls from
  25.99% of the grid at SPEI -1.0 to 0.44% at SPEI -3.0. Much of the SPEI -3.0
  coverage is in Greenland and the Canadian Arctic Archipelago (see the item
  thumbnail).
- The producer says the data "should not be used for local or regional
  applications".

## Recipes

Coverage and mean per threshold, from the item index. Each row is the 100-year
asset of one item:

```sql
SELECT id,
       round(assets."rp-100".bands[1].statistics.valid_percent, 2) AS valid_pct,
       round(assets."rp-100".bands[1].statistics.mean, 3) AS mean_months
FROM read_parquet('https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet')
ORDER BY id;
-- spei-1.0  25.99  2.994
-- spei-1.5  25.99  2.436
-- spei-2.0  22.45  1.853
-- spei-2.5   4.47  1.263
-- spei-3.0   0.44  1.203
```

A return-level curve for one point, Nairobi (36.82 E, 1.29 S), at SPEI -1.5.
GDAL reads only the tile it needs:

```bash
B=/vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-1.5
for rp in 25 50 100 250 500 1000; do
  printf '%s ' "$rp"
  gdallocationinfo -valonly -wgs84 "$B/global-drought-spei-1.5-return-period-$rp-years.tif" 36.82 -1.29 \
    | awk '{printf "%.2f\n", $1}'
done
# 25 1.74
# 50 1.90
# 100 1.98
# 250 2.04
# 500 2.06
# 1000 2.07
```

The same point at the 100-year return period across thresholds. Nairobi has
no estimate at SPEI -2.0 and below, so those print as nodata:

```bash
for t in 1.0 1.5 2.0; do
  v=$(gdallocationinfo -valonly -wgs84 \
    "/vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-$t/global-drought-spei-$t-return-period-100-years.tif" \
    36.82 -1.29)
  awk -v t="$t" -v v="$v" 'BEGIN { if (v < -1e38) print t, "nodata"; else printf "%s %.2f\n", t, v }'
done
# 1.0 3.38
# 1.5 1.98
```

Clip the Horn of Africa (40 to 52 E, 2 S to 15 N) at SPEI -2.0, 100 years,
to a local GeoTIFF and summarize it:

```bash
gdal_translate -q -srcwin 26400 9000 1440 2040 \
  /vsicurl/https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/spei-2.0/global-drought-spei-2.0-return-period-100-years.tif \
  horn.tif
gdalinfo -stats horn.tif | grep -E 'Size is|STATISTICS_(MAXIMUM|MEAN|VALID_PERCENT)'
# Size is 1440, 2040
# STATISTICS_MAXIMUM=3.2503819465637
# STATISTICS_MEAN=1.816493715523
# STATISTICS_VALID_PERCENT=47.43
```

In Python, `rasterio.open(url)` with the same HTTPS URL works. Read an
overview level (`out_shape`) for continental views; level 3 of the 0.0083°
grid is still finer than the 0.5° model.
