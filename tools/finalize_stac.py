"""Apply the STAC fields that `portolan add` cannot write.

Run from the repository root after every `portolan add`:

    python3 -I tools/finalize_stac.py catalog

The script is idempotent. It writes:

- the 1902 to 2018 interval on every item and the collection
- one data asset per return period (rp-25 ... rp-1000) with band statistics
  read from the COG, and one source asset per file pointing at HDX
- the render extension: default rp-100, plus one render per return period
- item_assets, item titles, and the collection thumbnail
- the root self, vcs, and issues links

It removes the item thumbnails that `portolan add` writes, the
`render:colormap_name` hint, and the deprecated proj:epsg field.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SLUG = "global-drought-hazard"
DATA_URL = f"https://data.source.coop/portolan-mirrors/{SLUG}/"
REPO = f"https://github.com/nlebovits/{SLUG}"
HDX = Path(__file__).resolve().parent / "hdx_resources.json"

EXT_RENDER = "https://stac-extensions.github.io/render/v2.0.0/schema.json"
EXT_ITEM_ASSETS = "https://stac-extensions.github.io/item-assets/v1.0.0/schema.json"
COG = "image/tiff; application=geotiff; profile=cloud-optimized"
TIFF = "image/tiff; application=geotiff"
RPS = [25, 50, 100, 250, 500, 1000]
NODATA = -3.4e38
START, END = "1902-01-01T00:00:00Z", "2018-12-31T23:59:59Z"
RESCALE = [[0, 6]]
COLORMAP = "ylorrd"


def load(p):
    return json.loads(p.read_text())


def save(p, d):
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")


def add_ext(d, *exts):
    d.setdefault("stac_extensions", [])
    for e in exts:
        if e not in d["stac_extensions"]:
            d["stac_extensions"].append(e)


def file_fields(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    return {"file:size": p.stat().st_size, "file:checksum": "1220" + h.hexdigest()}


def band(tif, threshold, rp):
    info = json.loads(subprocess.run(["gdalinfo", "-json", str(tif)], capture_output=True,
                                     text=True, check=True).stdout)
    m = info["bands"][0]["metadata"][""]
    return {
        "name": "return_level",
        "description": f"Months with SPEI-6 at or below {threshold} for a {rp}-year return period.",
        "data_type": "float32",
        "nodata": NODATA,
        "unit": "months",
        "statistics": {
            "minimum": float(m["STATISTICS_MINIMUM"]),
            "maximum": float(m["STATISTICS_MAXIMUM"]),
            "mean": float(m["STATISTICS_MEAN"]),
            "stddev": float(m["STATISTICS_STDDEV"]),
            "valid_percent": float(m["STATISTICS_VALID_PERCENT"]),
        },
    }


def render(title, key):
    return {"title": title, "assets": [key], "nodata": NODATA,
            "colormap_name": COLORMAP, "rescale": RESCALE}


def fix_item(path, hdx):
    d = load(path)
    t = d["id"].removeprefix("spei-")  # "1.0"
    threshold = f"-{t}"
    old = d["assets"]
    by_href = {a["href"].lstrip("./"): a for a in old.values()}
    assets = {}
    for rp in RPS:
        name = f"global-drought-spei-{t}-return-period-{rp}-years.tif"
        tif = path.parent / name
        prev = by_href.get(name, {})
        ff = ({k: prev[k] for k in ("file:size", "file:checksum")}
              if prev.get("file:size") == tif.stat().st_size and "file:checksum" in prev
              else file_fields(tif))
        assets[f"rp-{rp}"] = {
            "href": f"./{name}", "type": COG,
            "title": f"{rp}-year return period",
            "description": f"Months with SPEI-6 at or below {threshold} for a {rp}-year return period. "
                           "Float32, nodata -3.4e38.",
            "roles": ["data"], **ff, "bands": [band(tif, threshold, rp)],
        }
    for rp in RPS:
        r = hdx[f"global-drought-spei-{t}-return-period-{rp}-years.tif"]
        assets[f"source-rp-{rp}"] = {
            "href": r["url"], "type": TIFF,
            "title": f"HDX original: {r['name']}",
            "description": "The upstream GeoTIFF on the Humanitarian Data Exchange (strip-tiled, LZW, no overviews).",
            "roles": ["source"], "file:size": r["served_size"],
            "file:checksum": "1220" + r["sha256"],
        }
    thumb = path.parent / "thumbnail.png"
    if thumb.exists():
        assets["thumbnail"] = {"href": "./thumbnail.png", "type": "image/png", "title": "Thumbnail",
                               "description": f"The 100-year return level at SPEI {threshold}, rendered by tools/make_thumbs.py.",
                               "roles": ["thumbnail"], **file_fields(thumb)}
    d["assets"] = assets
    p = d["properties"]
    p["title"] = f"SPEI {threshold} or lower"
    p["description"] = (f"Return levels of months with SPEI-6 at or below {threshold}, "
                        "for return periods of 25 to 1000 years.")
    p["datetime"], p["start_datetime"], p["end_datetime"] = None, START, END
    p.pop("proj:epsg", None)
    p["renders"] = {"default": render(f"SPEI {threshold}, 100-year return period", "rp-100")}
    for rp in RPS:
        p["renders"][f"rp-{rp}"] = render(f"SPEI {threshold}, {rp}-year return period", f"rp-{rp}")
    add_ext(d, EXT_RENDER)
    save(path, d)
    return d


def fix_collection(cdir, hdx):
    cpath = cdir / "collection.json"
    c = load(cpath)
    for link in c["links"]:
        if link["rel"] == "item":
            item = fix_item((cdir / link["href"]).resolve(), hdx)
            link["title"] = item["properties"]["title"]
    c["extent"]["temporal"]["interval"] = [[START, END]]
    c.get("summaries", {}).pop("proj:epsg", None)
    add_ext(c, EXT_ITEM_ASSETS)
    c["item_assets"] = {
        f"rp-{rp}": {"type": COG, "roles": ["data"], "title": f"{rp}-year return period",
                     "bands": [{"name": "return_level", "data_type": "float32",
                                "nodata": NODATA, "unit": "months"}]}
        for rp in RPS}
    c["item_assets"].update({f"source-rp-{rp}": {"type": TIFF, "roles": ["source"]} for rp in RPS})
    thumb = cdir / "thumbnail.png"
    if thumb.exists():
        c["assets"]["thumbnail"] = {"href": "./thumbnail.png", "type": "image/png", "title": "Thumbnail",
                                    "description": "The 100-year return level at SPEI -1.0, rendered by tools/make_thumbs.py.",
                                    "roles": ["thumbnail"], **file_fields(thumb)}
    if "geoparquet-items" in c["assets"]:
        c["assets"]["geoparquet-items"]["title"] = "Item index"
        c["assets"]["geoparquet-items"]["description"] = (
            "STAC GeoParquet copy of every item in this collection, one row per item. "
            "The item JSON is normative.")
    save(cpath, c)


def fix_root():
    rp = ROOT / "catalog.json"
    r = load(rp)
    r["links"] = [l for l in r["links"] if l["rel"] not in ("self", "vcs", "issues")] + [
        {"rel": "self", "href": DATA_URL + "catalog.json", "type": "application/json"},
        {"rel": "vcs", "href": REPO, "type": "text/html", "title": "Build scripts and metadata"},
        {"rel": "issues", "href": REPO + "/issues", "type": "text/html", "title": "Report a problem"},
    ]
    save(rp, r)


def drop_cli_thumbs():
    for t in ROOT.rglob("*.thumb.jpg"):
        t.unlink()


def main():
    drop_cli_thumbs()
    hdx = {r["file"]: r for r in load(HDX)}
    fix_root()
    for cpath in sorted(ROOT.rglob("collection.json")):
        fix_collection(cpath.parent, hdx)


main()
