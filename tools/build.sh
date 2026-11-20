#!/bin/sh
# Rebuild every COG in catalog/ from the HDX dataset global-drought-hazard.
#   WORK=/scratch/gdh tools/build.sh
# Needs: aria2c, jq, GDAL with Python bindings, numpy.
set -eu
REPO=$(cd "$(dirname "$0")/.." && pwd)
WORK=${WORK:?set WORK to a scratch directory}
mkdir -p "$WORK/raw"
jq -r '.[] | "\(.url)\n  out=\(.file)"' "$REPO/tools/hdx_resources.json" > "$WORK/aria.txt"
aria2c -q -i "$WORK/aria.txt" -d "$WORK/raw" -j 10 -x 8 -s 8 --auto-file-renaming=false --allow-overwrite=true
# HDX lists sizes about 1.8 KB larger than its file store serves; check the served size.
jq -r '.[] | "\(.file) \(.served_size)"' "$REPO/tools/hdx_resources.json" | while read -r f s; do
  [ "$(stat -c%s "$WORK/raw/$f")" = "$s" ] || { echo "size mismatch: $f" >&2; exit 1; }
done
for t in 1.0 1.5 2.0 2.5 3.0; do mkdir -p "$REPO/catalog/drought-hazard/spei-$t"; done
jq -r '.[].file' "$REPO/tools/hdx_resources.json" | xargs -P 15 -I{} sh -c '
  t=$(echo {} | sed -E "s/global-drought-spei-([0-9.]+)-.*/\1/")
  python3 -I "$0/tools/make_cog.py" "$1/raw/{}" "$0/catalog/drought-hazard/spei-$t/{}"' "$REPO" "$WORK"
