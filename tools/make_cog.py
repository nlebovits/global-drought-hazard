"""Convert one HDX GeoTIFF to a COG with exact embedded statistics.

GDAL 3.8 computes a NaN mean and standard deviation for these Float32 rasters,
so the statistics are computed here with numpy and written as STATISTICS_*
metadata. Pixel values and the nodata value (-3.4e38) are not changed.

    python3 -I tools/make_cog.py <in.tif> <out.tif>
"""

import sys

import numpy as np
from osgeo import gdal

gdal.UseExceptions()
src, out = sys.argv[1], sys.argv[2]
a = gdal.Open(src).ReadAsArray()
valid = a[(a > -1e38) & ~np.isnan(a)].astype(np.float64)
stats = {
    "STATISTICS_MINIMUM": repr(float(valid.min())),
    "STATISTICS_MAXIMUM": repr(float(valid.max())),
    "STATISTICS_MEAN": repr(float(valid.mean())),
    "STATISTICS_STDDEV": repr(float(valid.std())),
    "STATISTICS_VALID_PERCENT": repr(round(100 * valid.size / a.size, 4)),
}
del a, valid
ds = gdal.Translate("", src, format="VRT")
ds.GetRasterBand(1).SetMetadata(stats)
gdal.Translate(out, ds, format="COG", creationOptions=[
    "COMPRESS=DEFLATE", "PREDICTOR=3", "LEVEL=6", "BLOCKSIZE=512",
    "OVERVIEW_RESAMPLING=AVERAGE", "NUM_THREADS=2", "BIGTIFF=IF_SAFER"])
print(out, stats)
