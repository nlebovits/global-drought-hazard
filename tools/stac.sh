#!/bin/sh
# Build the STAC JSON for the COGs that tools/build.sh wrote into catalog/.
# `portolan add` overwrites fields that finalize_stac.py sets, so never run it alone.
set -eu
REPO=$(cd "$(dirname "$0")/.." && pwd)
cd "$REPO/catalog"
portolan add drought-hazard --no-thumbnails
python3 -I "$REPO/tools/finalize_stac.py" .
portolan stac-geoparquet
portolan readme
python3 -I "$REPO/tools/fix_readme_links.py" .
portolan check --data-scope local
