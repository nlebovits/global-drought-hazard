"""Render one framed 3:2 PNG thumbnail per item, and one for the collection.

Each thumbnail is the 100-year return level of the item's threshold on a
world view in Web Mercator (latitude about -64.5 to 82), coloured with the
same YlOrRd ramp and 0 to 6 month range as the default render, over the Esri
World Light Gray canvas. Downsampling uses the maximum, so the sparse
patches of SPEI -2.5 and -3.0 stay visible.

    uv run -q --python /usr/bin/python3 --with pillow --with matplotlib --with "numpy<2" \
        python -I tools/make_thumbs.py catalog
"""

import shutil
import sys
from pathlib import Path

import numpy as np
from matplotlib import colormaps
from osgeo import gdal
from PIL import Image

gdal.UseExceptions()
C = Path(sys.argv[1]).resolve() / "drought-hazard"
W, H = 1024, 683
HALF = 20037508.34
BOUNDS = [-HALF, -9.5e6, HALF, -9.5e6 + 2 * HALF * H / W]
BASEMAP = """<GDAL_WMS><Service name="TMS"><ServerUrl>https://services.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/${z}/${y}/${x}</ServerUrl></Service>
<DataWindow><UpperLeftX>-20037508.34</UpperLeftX><UpperLeftY>20037508.34</UpperLeftY><LowerRightX>20037508.34</LowerRightX><LowerRightY>-20037508.34</LowerRightY><TileLevel>16</TileLevel><TileCountX>1</TileCountX><TileCountY>1</TileCountY><YOrigin>top</YOrigin></DataWindow>
<Projection>EPSG:3857</Projection><BlockSizeX>256</BlockSizeX><BlockSizeY>256</BlockSizeY><BandsCount>3</BandsCount></GDAL_WMS>"""
CMAP = colormaps["YlOrRd"]


def warp(src, alg, **kw):
    return gdal.Warp("", src, format="MEM", dstSRS="EPSG:3857", outputBounds=BOUNDS, width=W,
                     height=H, resampleAlg=alg, **kw).ReadAsArray()


def main():
    try:
        base = warp(BASEMAP, "bilinear").transpose(1, 2, 0).astype(np.float32)
    except RuntimeError:
        base = np.full((H, W, 3), 235, np.float32)
    for item in sorted(C.glob("spei-*")):
        t = item.name.removeprefix("spei-")
        cog = item / f"global-drought-spei-{t}-return-period-100-years.tif"
        a = warp(str(cog), "max", srcNodata=-3.4e38, dstNodata=np.nan)
        valid = ~np.isnan(a)
        img = base.copy()
        img[valid] = CMAP(np.clip(a[valid] / 6, 0, 1))[:, :3] * 255
        out = item / "thumbnail.png"
        Image.fromarray(img.astype(np.uint8)).save(out, optimize=True)
        print(item.name, out.stat().st_size, "px with data:", int(valid.sum()))
    shutil.copy(C / "spei-1.0" / "thumbnail.png", C / "thumbnail.png")


main()
