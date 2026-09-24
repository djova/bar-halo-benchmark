# Substantive editorial repair — article 2026-09-24.2, PDF 2026-09-24.3

The previous revision retained too much audit history and procedural language in
place of a clear physical argument. This release rewrites the introduction,
derives the local Hamiltonian and scaled equations, states the initial bar
preparation, explains the measured transfer, and shows how population gradients
change its sign. The finite-displacement estimator now includes its phase-average
argument. The PDF separates the main scientific narrative from the website's
model registry and historical records.

The [editorial repair record](web/diagnostics/communication/EDITORIAL_REPAIR_2026-09-24.md)
identifies the earlier writing failures and the changes to the communication
skill. These are our editorial judgments; they do not claim an individual
researcher's style, approval or endorsement. No private correspondence is included.

A fourth figure combines previously published population gradients, primitive
kernels and signed contributions. Its generator is supplied in
`scripts/publication/gradient_figure.py`, and its source checksum and arithmetic
checks are in `web/diagnostics/population-accuracy/gradient-figure-receipt.json`.
No orbit or distribution evolution was rerun for this release. The population,
accuracy and cost operands, old principal figures and previous releases retain
their scientific content. The PDF includes ten pages, four figures and seven
bibliography entries; its complete LaTeX source is in `../manuscript/`.

The clean publication is built and its current-release consistency checks are
recorded below. These establish delivery, arithmetic consistency and export
fidelity, not writing quality, physical validity or outside scientific review.
The [standalone-build receipt](release-checks/editorial-repair-public-build.json)
records reconstruction of all 24 accuracy rows, 66 claim pointers and 186 numeric
cells in each article representation, with 97 manifest artifacts checked. The
[packaging receipt](release-checks/editorial-repair-package.json) records unchanged
population/accuracy/cost rows and three original figure files, matching manuscript
inputs and output hashes, and a scoped scan for private operational paths or
correspondence. The PDF SHA-256 is
`b7ec4733c2bd7d80c174f979e28c7c1ec92a1b8e22296d6db2593aa2d499606b`.

Canonical access remains client-dependent; the pinned GitHub mirror remains
the reading fallback. Prior release records follow unchanged.

---

# Editorial release 2026-09-24.1

The article and PDF export 2026-09-24.2 share a revised narrative. A 230-record
arXiv screen and twelve focused body reviews inform the updated communication
skill; exact reading depths, versions and limits are recorded in the
[communication review](web/diagnostics/communication/WRITING_REVIEW_2026-09-24.md).
This is editorial work, not external scientific review or a new experiment.

The project consistency checker reconstructs the same central numerical results.
All published population, accuracy and cost rows, their CSV values and the three
principal figures were compared with the prior commit and are unchanged. Earlier
publication releases and the preceding PDF export retain their original bytes.
The revised PDF has ten pages, three figures and six bibliography entries.
No unresolved citations or overflowing TeX boxes were found; rendered pages were
visually inspected. Desktop/mobile Chromium and WebKit checks cover the PDF link,
no-JavaScript reading, keyboard focus, layout and downloaded file hash. These are
project-reported publication checks, not astrophysical validation.

Canonical automated-client access remains partial. The pinned public GitHub
mirror remains the fallback; no universal crawler-access claim is made.

---

# Publication release 2026-09-23.1 — reading and verification audit

The canonical article, learning guide and evidence interface are published at
[Galaxy Bar](https://djova.ca/galaxy-bar/paper.html). This release consolidates
existing research; it does not add a physical simulation or an external review.

## What is public

- [Research article](https://djova.ca/galaxy-bar/paper.html) and its
  [complete Markdown](https://djova.ca/galaxy-bar/paper.md).
- [Six learning modules](https://djova.ca/galaxy-bar/learn.html),
  [reproduction map](https://djova.ca/galaxy-bar/reproduce.html), and
  [agent entry](https://djova.ca/galaxy-bar/agents.html).
- Versioned claims, models, campaigns, datasets, figure metadata, full principal
  tables and numerical source records, discovered through the
  [manifest](https://djova.ca/galaxy-bar/manifest.json).
- A retained snapshot under `releases/2026-09-23.1/` and public source tag
  `publication-2026-09-23.1` at commit
  `5d60fb5d6e1b71cbc67517223886d71fb6f0a941`. The tag is not moved by this audit.

The source package distinguishes inspectable original-galaxy outputs from fully
reproducible reduced experiments. It does not contain private original-galaxy
initial conditions or promise to regenerate all historical movies.

## Checks actually performed

A fresh anonymous HTTPS clone and isolated publication build regenerated all
35 compared central artifacts identically. This rebuilt the article and tables,
not the simulations. The earlier 162-array receipt remains a report of its
separate numerical reproduction.

Anonymous arithmetic verification reproduced the population magnitude ratio
4.735323064643955, eight supported advance qualifications at one new dynamical
condition, and four conservative rejections. It also distinguished the broad
conditional cost-times-variance ratio 6928.3538 from the between-batch estimate
2749.3991 and the narrow-population ratio 0.992683. None is a newly measured
physical result or a general simulation speedup.

Chromium and WebKit checks at three widths exercised the controls, deep links,
keyboard focus, text zoom, reduced-motion setting and semantic structure.
The article and complete 24-row accuracy table remain readable with JavaScript
disabled; missing interactive data leaves the static evidence visible. These
checks are not a human screen-reader audit or a WCAG certification.

A clean remote Cloudflare browser read the current article with JavaScript
disabled, including its release label and complete table, without target-site
credentials. The kernel archive was also downloaded anonymously and its checksum
verified. The linked receipts below separate content access, arithmetic checks,
and source preservation; they are not independent scientific confirmations.

## Access findings and supported reading paths

The edge initially inserted an analytics script into some HTML responses.
A configuration scoped to Galaxy Bar now disables that injection. A descriptive
anonymous reader receives HTML and data matching the published build exactly.
No login, cookie, private network, installation or execution is needed to read.

Two limitations remain explicit: the default `Python-urllib/3.12` user agent gets
Cloudflare error 1010 on both the custom domain and Pages alias, and one external
browsing service reports the canonical URLs as inaccessible. The scoped browser
integrity setting did not remove the generic-client rejection; its remaining
cause is not established. These failures do not imply that the public article
is absent or that all anonymous readers fail.

Use a descriptive user agent, as the supplied `verify_publication.py` does.
An independently accessible static fallback is the
[tagged Markdown article](https://raw.githubusercontent.com/djova/bar-halo-benchmark/publication-2026-09-23.1/publication/web/paper.md)
and the [tagged publication directory](https://github.com/djova/bar-halo-benchmark/tree/publication-2026-09-23.1/publication).
The external browsing service successfully retrieved that same full article.

## Receipts and review status

See [release-checks](release-checks/) for the fresh build, arithmetic, remote
reader, anonymous payload and scientific-preservation records. The anonymous
HTML receipt retains the rejected generic reader separately from the successful
named-reader checks. Operational audits establish delivery, not convergence,
physical validity or novelty. No independent cold-start scientific agent review
or external researcher review is claimed, and no researchers were contacted.

Public criticism is welcome through [issues](https://github.com/djova/bar-halo-benchmark/issues).
Please cite a claim, figure or dataset ID and the release version.

## Presentation revision 2026-09-23.2

The next source tag preserves the scientific measurements and adds build-time
KaTeX, semantic MathML and locally served WOFF2 fonts. The current pages contain
99 typeset expressions; 24 substantial numeric tables now use native expanders.
Graphs remain visible by default. All 24 accuracy records remain in the HTML.
Both browser engines pass desktop and mobile rendering checks, and all 30 current
root pages were reviewed for desktop table overflow without JavaScript.
The previous source tag and website snapshot remain unchanged. No new physics
or stronger accuracy claim is introduced by this presentation revision.

## Corrective publication revision 2026-09-23.3

The finite-displacement control has zero integrated expectation; the weighted
first-order impulse is the potentially nonzero signal. The article and supporting
accuracy page now state that correctly. Noise impulse Xi_T is distinguished from
standard Wiener motion W_t. The guide defines actions and orbital angles and
explicitly switches off noise before deriving deterministic phase locking.

Claim metadata now separates physical controls, assessed comparisons and
uncertainty methods, and selects exact rows with identities and actual protocols.
The publication consistency checker reconstructs 24 rows of accuracy/sign
classifications and independent three-way assessments from supplied operands.
It also checks the manifest, article numeric cells, JSON/CSV consistency and claim
pointers, and accepts an expected release. Twelve tests, including semantic
mutations with refreshed hashes, pass locally. The arithmetic returns eight
supported advance qualifications, four conservative rejections, eight outside
5%, and fifteen supported sign qualifications. It does not rerun any simulation
or certify the coverage of numerical proxies.

The agent guide, manifest and README expose pinned raw GitHub links to the
article, claims, values, derivation, protocols and scientific source. Included
Markdown links resolve to that tag; omitted historical material is labelled
website-only. Canonical-site accessibility remains partial across clients.
These content changes are not an edge-access repair or a universal crawler test.
Earlier release tags and numerical evidence are unchanged. No external researcher
has been contacted and no external scientific endorsement is claimed.

### Public retrieval and reconstruction after tagging

A fresh anonymous clone of `publication-2026-09-23.3` with a fresh Python3.11.14
environment and pinned dependencies regenerates the tracked publication web
files identically, builds the site, and passes its consistency checker. No
scientific evolution is rerun. The two older publication tags remain unchanged.

The web browsing service retrieves the tagged agent guide, article, claims,
population/accuracy/cost values, finite-displacement derivation and pinned
scientific reproduction instructions. A default Python reader, without custom
headers, retrieves eleven central mirror/source resources with matching bytes.
The full raw mirror passes the expected-release consistency checker as well.
The canonical browsing path still fails through that service, and the generic
Python reader gets403 there; the named anonymous reader and live browsers work.
This is a tested fallback, not universal canonical accessibility or an independent
scientific review. See [the corrective receipts](release-checks/corrections-2026-09-23.3/).

### Delivery checks for the corrective release

The Cloudflare and tailnet publication interfaces pass Chrome/WebKit checks,
including mobile, no-JavaScript evidence, missing-data behavior and keyboard
navigation. All 7,300 publication files on each site match the audited build.
The full canonical-domain and new Pages-alias privacy scans each pass22,796
file instances; local release checks pass15,280. These verify delivery and
privacy, not physical convergence or independent scientific confirmation.
The remaining canonical generic-reader/browsing-tool limitations above persist.

## Editorial release 2026-09-23.4

The Fourier example now shows the numerator expansion: its oscillating terms
vanish while the constant a/2 survives. The normalization and results are unchanged.
Mirror links labelled interactive go to the canonical site, with distinct static
value links. The article uses the included, byte-identical accuracy protocol.
All three original principal figures are in the manifest and use pinned raw
GitHub URLs beside the mirrored text. No figures or numerical results were
recomputed. Release .3 and its evidence remain immutable.

This fixes the identified publication links, not universal client access.
Canonical-site and some browser-service retrieval remains client-dependent.

### Editorial patch checks

The .4 mirror was read anonymously with default Python headers: ten central
resources, including the frozen accuracy protocol and all three principal PNGs,
match the released bytes; the images have image/png content types. The web
browsing service also retrieved the article, learning guide, manifest, protocol
and estimator figure. That service still could not retrieve the canonical article.
This is evidence for the pinned fallback, not universal client access.

The existing publication consistency checker passes on the tagged raw mirror
and canonical site at expected release .4. Targeted regression checks exercise
the reported link failures. Chrome and WebKit checks pass at desktop and mobile
sizes, with complete static evidence and missing-data behavior. The corrected
Fourier example was visually inspected. These checks do not rerun simulations
or establish scientific validity; .3 and the numerical evidence are unchanged.

Both the canonical domain and new Pages alias pass full public privacy and
byte-matching scans (23,063 file instances each). The earlier 140 deployment
ID/URL/commit mappings are preserved, with their historical audit chain retained.
Anonymous mirror and browsing-service observations are in the
[editorial access receipts](release-checks/editorial-2026-09-23.4/).
These are project-reported delivery checks, not external scientific review.
