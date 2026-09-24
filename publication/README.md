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

Release 2026-09-24.1 revises the scientific exposition around the population
approximation, its mechanism and the operational accuracy decision. A documented
literature review updates the reusable writing skill. The canonical article and
MNRAS PDF share this narrative. Numerical evidence and earlier releases are unchanged.
Interactive controls explicitly require the canonical site; static values, the
protocol and three principal figures retain pinned mirror URLs. The [reading audit and access fallback](RELEASE_AUDIT.md) documents the
preceding release's checks and the generic-client retrieval limitation.

## Anonymous fallback without a custom user agent

Canonical-site access remains partial across automated clients. No private
connector or execution is required for these pinned public files:

- [Article](https://raw.githubusercontent.com/djova/bar-halo-benchmark/publication-2026-09-24.1/publication/web/paper.md) and [agent guide/link-resolution rules](https://raw.githubusercontent.com/djova/bar-halo-benchmark/publication-2026-09-24.1/publication/web/agents.md)
- [Claims](https://raw.githubusercontent.com/djova/bar-halo-benchmark/publication-2026-09-24.1/publication/web/claims.json) and [manifest](https://raw.githubusercontent.com/djova/bar-halo-benchmark/publication-2026-09-24.1/publication/web/manifest.json)
- [Population values](https://raw.githubusercontent.com/djova/bar-halo-benchmark/publication-2026-09-24.1/publication/web/results/populations.json), [accuracy operands](https://raw.githubusercontent.com/djova/bar-halo-benchmark/publication-2026-09-24.1/publication/web/results/accuracy.json), [costs](https://raw.githubusercontent.com/djova/bar-halo-benchmark/publication-2026-09-24.1/publication/web/results/cost.json)
- [Estimator derivation](https://raw.githubusercontent.com/djova/bar-halo-benchmark/publication-2026-09-24.1/publication/web/methods/CUMULATIVE_IDENTITY.md) and [frozen protocol](https://raw.githubusercontent.com/djova/bar-halo-benchmark/publication-2026-09-24.1/publication/web/protocols/ACCURACY_PLAN.md)
- [Pinned scientific source](https://github.com/djova/bar-halo-benchmark/tree/cdb30b5b2f350d2f3de6831995b83f281fe2974e)

Relative paths inside JSON resolve against `https://raw.githubusercontent.com/djova/bar-halo-benchmark/publication-2026-09-24.1/publication/web/`; array paths marked
`path_in_public_package` resolve against the scientific-source revision instead.
Markdown links marked historical website-only need the canonical site.
The mirror contains the central evidence and all three principal figure images.
Interactive links require the canonical site; adjacent static-value links remain
in this mirror. Historical explorers are not all included.

To check supplied records without simulating: `python3 scripts/publication/verify_publication.py --origin web --expected-release 2026-09-24.1`.
Mutation tests: `python3 scripts/publication/test_verify_publication.py`.
The checker verifies its stated arithmetic, pointers and manifest; it does not
certify the error proxies or independently reproduce physical evolution.
