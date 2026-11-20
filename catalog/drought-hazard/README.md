# SPEI-6 drought return levels

Extreme value return levels of the 6-month Standardised Precipitation Evapotranspiration Index (SPEI-6), modelled per grid cell from the [CSIC Global SPEI Database](https://spei.csic.es/spei_database/) for January 1902 to December 2018 with Poisson-Generalized Pareto point process models. Each item is one SPEI threshold (-1.0, -1.5, -2.0, -2.5, -3.0) and holds six cloud-optimized GeoTIFFs, one per return period: 25, 50, 100, 250, 500, and 1000 years. A pixel is the number of months with SPEI at or below the threshold for that return period. Higher values mean more severe drought. The model resolution is about 0.5°. Read [AGENTS.md](AGENTS.md) for access patterns.

![drought](https://img.shields.io/badge/drought-blue) ![climate hazards](https://img.shields.io/badge/climate_hazards-blue) ![hazards and risk](https://img.shields.io/badge/hazards_and_risk-blue) ![SPEI](https://img.shields.io/badge/SPEI-blue) ![extreme value analysis](https://img.shields.io/badge/extreme_value_analysis-blue) ![return period](https://img.shields.io/badge/return_period-blue)

## Spatial Coverage

- **Bounding Box**: [-180.0, -89.9999928, 179.9999856, 90.0]
- **CRS**: EPSG:4326

## Temporal Coverage

- **Start**: 1902-01-01T00:00:00Z
- **End**: 2018-12-31T23:59:59Z

## Bands

| Band | Name | Data Type | Unit | Nodata | Min | Max | Mean | Std Dev | Valid % | Description |
|------|------|-----------|------|--------|------|------|------|---------|---------|-------------|
| 1 | return_level | float32 | months | -3.4e+38 | 1.287380337715149 | 3.715528726577759 | 2.6147970772103855 | 0.23260348916377563 | 25.9938 | Months with SPEI-6 at or below -1.0 for a 25-year return period. |

## Files

| File | Size | Checksum |
|------|------|----------|
| ./items.parquet | 105.1 KB | 122088f0d591... |
| ./thumbnail.png | 298.1 KB | 122032e2fa64... |
| spei-1.0/global-drought-spei-1.0-return-period-25-years.tif | 179.3 MB | 122053f3e4ff... |
| spei-1.0/global-drought-spei-1.0-return-period-50-years.tif | 178.1 MB | 122064fce0b1... |
| spei-1.0/global-drought-spei-1.0-return-period-100-years.tif | 176.8 MB | 1220ceef64df... |
| spei-1.0/global-drought-spei-1.0-return-period-250-years.tif | 175.2 MB | 1220ad1db8ca... |
| spei-1.0/global-drought-spei-1.0-return-period-500-years.tif | 175.6 MB | 1220384d0ba4... |
| spei-1.0/global-drought-spei-1.0-return-period-1000-years.tif | 176.4 MB | 1220843b9562... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/38ee3c61-6130-4a26-b5b4-1106a477a689/download/global-drought-spei-1.0-return-period-25-years.tif | 990.0 MB | 1220e5a69606... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/19a8be65-f87b-4567-8c29-ede5d4f2a24d/download/global-drought-spei-1.0-return-period-50-years.tif | 992.1 MB | 122092289431... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/0d5619c0-dbd4-4cd8-87e7-6a7082b8cac4/download/global-drought-spei-1.0-return-period-100-years.tif | 989.0 MB | 12200b1c4b47... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/ee36b652-6d1f-47bc-afa6-37974c4c1a12/download/global-drought-spei-1.0-return-period-250-years.tif | 978.7 MB | 122057b93377... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/0a6bd7da-5a45-437d-b311-29a60c0c675a/download/global-drought-spei-1.0-return-period-500-years.tif | 976.3 MB | 12207f004728... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/1e3134d0-0b90-48d1-829a-f046cf8b6442/download/global-drought-spei-1.0-return-period-1000-years.tif | 976.5 MB | 12200bfb4dca... |
| spei-1.5/global-drought-spei-1.5-return-period-25-years.tif | 200.8 MB | 122079a3fb74... |
| spei-1.5/global-drought-spei-1.5-return-period-50-years.tif | 197.6 MB | 1220318b0c57... |
| spei-1.5/global-drought-spei-1.5-return-period-100-years.tif | 190.5 MB | 122053e28181... |
| spei-1.5/global-drought-spei-1.5-return-period-250-years.tif | 180.5 MB | 1220f376f4bf... |
| spei-1.5/global-drought-spei-1.5-return-period-500-years.tif | 175.1 MB | 1220e7cf5e5a... |
| spei-1.5/global-drought-spei-1.5-return-period-1000-years.tif | 171.3 MB | 122064149dd9... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/59b97435-f016-42b4-9546-57ce03d2ddcc/download/global-drought-spei-1.5-return-period-25-years.tif | 1006.3 MB | 12204d725681... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/c5d8e7b5-de7e-435e-a2fb-9f9a36902b74/download/global-drought-spei-1.5-return-period-50-years.tif | 1002.1 MB | 12208394daff... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/6744572e-d5d1-4033-9d64-c87dc565586a/download/global-drought-spei-1.5-return-period-100-years.tif | 997.6 MB | 1220030244a6... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/add1394c-618d-41d9-a168-b1a8243d3dbc/download/global-drought-spei-1.5-return-period-250-years.tif | 987.1 MB | 12206ed6706d... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/eb934a71-ab3c-4e03-9b78-acf35abaa592/download/global-drought-spei-1.5-return-period-500-years.tif | 976.6 MB | 12205ba79ef7... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/b8814be7-b176-4140-85aa-30fde540b9b6/download/global-drought-spei-1.5-return-period-1000-years.tif | 961.4 MB | 12209c509c85... |
| spei-2.0/global-drought-spei-2.0-return-period-25-years.tif | 177.2 MB | 1220e52eb1c7... |
| spei-2.0/global-drought-spei-2.0-return-period-50-years.tif | 161.9 MB | 1220808d62f6... |
| spei-2.0/global-drought-spei-2.0-return-period-100-years.tif | 155.1 MB | 1220f82e3c63... |
| spei-2.0/global-drought-spei-2.0-return-period-250-years.tif | 147.0 MB | 122074597554... |
| spei-2.0/global-drought-spei-2.0-return-period-500-years.tif | 138.1 MB | 122093647878... |
| spei-2.0/global-drought-spei-2.0-return-period-1000-years.tif | 133.3 MB | 122016327789... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/3d067bc4-e6bd-413e-a490-2010aa842a63/download/global-drought-spei-2.0-return-period-25-years.tif | 808.3 MB | 1220f2e984e1... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/08061f08-fed5-41f5-8234-7b9d94a7346b/download/global-drought-spei-2.0-return-period-50-years.tif | 844.3 MB | 122031286d0e... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/e21f4f89-d2f6-484e-95d9-847679b44a61/download/global-drought-spei-2.0-return-period-100-years.tif | 838.1 MB | 12209e4b8726... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/74fceaa8-e950-47ca-8bca-f1d8ef24fbdd/download/global-drought-spei-2.0-return-period-250-years.tif | 815.0 MB | 122014d886e9... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/430b28bb-b255-453f-9426-60eb1ed1a087/download/global-drought-spei-2.0-return-period-500-years.tif | 785.3 MB | 1220c2401052... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/8b617ce9-3ef2-44cd-a1f7-fd7397ec720d/download/global-drought-spei-2.0-return-period-1000-years.tif | 758.6 MB | 12200d3836d5... |
| spei-2.5/global-drought-spei-2.5-return-period-25-years.tif | 36.8 MB | 12201c6a18f0... |
| spei-2.5/global-drought-spei-2.5-return-period-50-years.tif | 42.2 MB | 12202c102335... |
| spei-2.5/global-drought-spei-2.5-return-period-100-years.tif | 41.4 MB | 122056516075... |
| spei-2.5/global-drought-spei-2.5-return-period-250-years.tif | 39.6 MB | 12206c22b989... |
| spei-2.5/global-drought-spei-2.5-return-period-500-years.tif | 38.4 MB | 1220a4869561... |
| spei-2.5/global-drought-spei-2.5-return-period-1000-years.tif | 39.1 MB | 1220f00c047c... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/8e786a75-1c73-46df-8e62-4fdf6d52c633/download/global-drought-spei-2.5-return-period-25-years.tif | 95.3 MB | 1220e02a7a26... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/60e43ac3-31ba-4b89-91c3-6c293f4e7c49/download/global-drought-spei-2.5-return-period-50-years.tif | 144.9 MB | 122074042f45... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/2f4890c7-593a-4790-b7fb-ad8626718b43/download/global-drought-spei-2.5-return-period-100-years.tif | 163.3 MB | 122037b25003... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/32e15d48-b03b-47b3-8fd2-6a110a9e0523/download/global-drought-spei-2.5-return-period-250-years.tif | 159.5 MB | 12200d96c087... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/956544da-03ae-451a-a85a-7b976be0dd14/download/global-drought-spei-2.5-return-period-500-years.tif | 155.0 MB | 12207ba7f347... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/b8655e91-ed6f-4304-8c48-ef3a54c77e05/download/global-drought-spei-2.5-return-period-1000-years.tif | 154.5 MB | 12205caeca5e... |
| spei-3.0/global-drought-spei-3.0-return-period-25-years.tif | 23.9 MB | 12203f1d3f69... |
| spei-3.0/global-drought-spei-3.0-return-period-50-years.tif | 24.3 MB | 12206dbca17d... |
| spei-3.0/global-drought-spei-3.0-return-period-100-years.tif | 24.3 MB | 12203916494d... |
| spei-3.0/global-drought-spei-3.0-return-period-250-years.tif | 24.2 MB | 1220ca5c99a2... |
| spei-3.0/global-drought-spei-3.0-return-period-500-years.tif | 24.1 MB | 1220325e2a6e... |
| spei-3.0/global-drought-spei-3.0-return-period-1000-years.tif | 24.2 MB | 1220a3b25216... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/10b998e2-be41-483e-a662-52706937923c/download/global-drought-spei-3.0-return-period-25-years.tif | 37.7 MB | 1220272c7c96... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/97161fb1-3161-47d6-b4b6-fccf79461ba6/download/global-drought-spei-3.0-return-period-50-years.tif | 43.4 MB | 1220588b868c... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/e58ff655-72cb-4565-92af-4ceb3730c657/download/global-drought-spei-3.0-return-period-100-years.tif | 45.7 MB | 1220305f7e57... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/4487541d-84ef-4763-97a0-92a3c730514d/download/global-drought-spei-3.0-return-period-250-years.tif | 45.4 MB | 12200a4b07bc... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/b0b6422b-82e6-4bd3-8aea-e028611b87f7/download/global-drought-spei-3.0-return-period-500-years.tif | 45.0 MB | 122032b81d3b... |
| https://data.humdata.org/dataset/30b85665-4c3d-4dc3-b543-3a567a3dea37/resource/772e5350-4d9e-46e9-a5c6-6aafc955ab5b/download/global-drought-spei-3.0-return-period-1000-years.tif | 45.0 MB | 1220d8fa552d... |

## Quick Start

```python
import geopandas as gpd

gdf = gpd.read_parquet("https://data.source.coop/portolan-mirrors/global-drought-hazard/drought-hazard/items.parquet")
print(gdf.head())
```

## STAC Metadata

- **root**: `../catalog.json`
- **parent**: `../catalog.json`

## Source

[https://data.humdata.org/dataset/global-drought-hazard](https://data.humdata.org/dataset/global-drought-hazard)

## Processing Notes

Each item directory holds the six HDX files of one threshold under their upstream file names. The HDX methodology: time-varying parameters for non-stationarity, declustering for tail dependence, and spatiotemporally weighted error term corrections per cell; results resampled bilinearly from about 0.5° to about 0.0083° for publication.

## Citation

Weller, Daniel & Mann, Holger (2022): Global Drought Hazard. A global raster data set of extreme value analyses of the Standardized Precipitation Evapotranspiration Index via Poisson-Generalized Pareto Point Process modelling. Distributed by The Humanitarian Data Exchange: Institute for International Law of Peace and Armed Conflict.

## Attribution

Weller & Mann (2022), Global Drought Hazard, IFHV, Ruhr University Bochum, CC BY 4.0

## License

[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/)

## Contact

Portolan Mirrors <nissim@radiant.earth>

## Known Issues

The producer states that the data "should not be used for local or regional applications" and that "some areas may be under- or overestimated". The model output is at about 0.5°; the 0.0083° grid is a bilinear resampling for publication, so it adds no detail. The producer describes a value as "the number of months" with SPEI at or below the threshold for the return period, but does not say whether the count is per drought event or how it is aggregated; values range from 0 to 5.93. At SPEI -2.0 and below, cells where the model has no estimate are nodata, so coverage falls from 26% of the grid at SPEI -1.0 to 0.44% at SPEI -3.0.

---

*Generated by [Portolan](https://github.com/portolan-sdi/portolan-cli) from STAC metadata and .portolan/metadata.yaml*
