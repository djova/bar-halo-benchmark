# Galaxy Bar canonical article release

This is the clean source, exact central evidence and static website for the
versioned research article. It contains no host deployment configuration,
credentials or private initial-condition archives. Numerical experiments remain
in the parent benchmark; this directory does not rerun them.

From this directory, with Python3.11 and Node22 available:

```sh
python3.11 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/publication/generate.py --benchmark ..
npm ci --prefix web
node build.mjs
python3 -m http.server 8795 --directory dist
```

Open `/paper.html`. Generation recomputes tables, ratios, metadata and hashes
from supplied records; it does not simulate orbits. NumPy inspects the parent
package arrays for shape/type metadata. The build links historical explorers
and missing legacy assets to the canonical public site; it reproduces the
central article, not every original galaxy movie. The versioned public snapshot
and this Git tag preserve the evidence. See `web/reproduce.md` for inspection,
arithmetic verification and numerical reproduction with measured resource costs.

Code, original article/learning text and derived result tables in this release
use the parent MIT license. Original third-party catalogues and papers retain
their authors' terms; no blanket third-party license is granted here.

This is AI-assisted work, maintained by djova, and not externally reviewed.
Public issues are the criticism route; cite a claim or dataset ID.

Release 2026-09-23.2 adds build-time KaTeX with local fonts and expandable numeric
values. It preserves the previous 2026-09-23.1 source tag and all numerical
results. The [reading audit and access fallback](RELEASE_AUDIT.md) documents the
preceding release's checks and the generic-client retrieval limitation.
