# AGENTS.md: Global Drought Hazard

A Portolan mirror of the IFHV [Global Drought Hazard](https://data.humdata.org/dataset/global-drought-hazard)
rasters (Weller & Mann, 2022), published on the Humanitarian Data Exchange
under CC BY 4.0. The upstream dataset is static: HDX shows the last change on
2023-01-16.

## Contents

One collection, `drought-hazard`: 30 global Float32 COGs of SPEI-6 extreme
value return levels, five thresholds (items) by six return periods (assets).
Read [drought-hazard/AGENTS.md](drought-hazard/AGENTS.md) for the URL pattern,
the value semantics, and recipes that run.

Root STAC: `https://data.source.coop/portolan-mirrors/global-drought-hazard/catalog.json`.
The item index `drought-hazard/items.parquet` lists every item and asset in
one file.

## Before you use it

- The model ran at about 0.5°. The published 0.0083° grid is a bilinear
  resampling for display.
- The producer says it "should not be used for local or regional
  applications".
- The producer does not fully define the unit ("number of months"). Compare
  values within one threshold, not as absolute counts.

## License and citation

CC BY 4.0. Cite: Weller, Daniel & Mann, Holger (2022): Global Drought Hazard.
A global raster data set of extreme value analyses of the Standardized
Precipitation Evapotranspiration Index via Poisson-Generalized Pareto Point
Process modelling. Distributed by The Humanitarian Data Exchange: Institute
for International Law of Peace and Armed Conflict.

## Maintenance

Build scripts and metadata are in
[nlebovits/global-drought-hazard](https://github.com/nlebovits/global-drought-hazard).
Report problems there.
