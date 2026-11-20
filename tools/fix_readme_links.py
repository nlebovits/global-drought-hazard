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
