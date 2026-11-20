"""Repair the child links in generated subcatalog READMEs.

portolan-cli 0.9.0 writes a subcatalog's child links with the subcatalog
path twice, as in `annual-extent/annual-extent/extent-raster/`. Run after
`portolan readme`:

    python3 -I tools/fix_readme_links.py catalog
"""

import re
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
for readme in root.rglob("README.md"):
    rel = readme.parent.relative_to(root).as_posix()
    if rel == ".":
        continue
    text = readme.read_text()
    fixed = re.sub(r"\]\(" + re.escape(rel + "/" + rel + "/"), "](", text)
    if fixed != text:
        readme.write_text(fixed)
        print("fixed", readme.relative_to(root))

# portolan-cli 0.9.0 also links root children as `catalog/<id>/`, and its Quick
# Start reads `./items.parquet`, which only runs from inside the collection.
DATA_URL = "https://data.source.coop/portolan-mirrors/global-drought-hazard/"
for readme in root.rglob("README.md"):
    rel = readme.parent.relative_to(root).as_posix()
    text = readme.read_text()
    fixed = re.sub(r"\]\(catalog/([^)/]+)/\)", r"](\1/README.md)", text) if rel == "." else text
    if rel != ".":
        fixed = fixed.replace('read_parquet("./items.parquet")',
                              f'read_parquet("{DATA_URL}{rel}/items.parquet")')
    if fixed != text:
        readme.write_text(fixed)
        print("fixed", readme.relative_to(root))
