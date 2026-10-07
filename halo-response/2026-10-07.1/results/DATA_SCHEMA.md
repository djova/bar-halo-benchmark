# Public halo-response figure packet

This directory contains the checked export for the new exploratory follow-up:
the principal fixed-background packet and a separate six-resolution linear
collective assessment. The figures come from closed numerical records; the
browser does not generate scientific measurements. The earlier publication
remains authoritative for its own experiments.

The page reads `figures.json` in this directory. The exporter supplies numerical
estimates, intervals, paired operands and qualification decisions. The browser
only displays them: it does not evolve orbits, evaluate a DF, rescale a
population, estimate covariance, calculate confidence intervals or determine
physical qualification. No inferred intermediate orbit frames are allowed.

## Common packet and public provenance

| Field | Required meaning |
|---|---|
| `schema` | Literal `galaxy-bar-halo-response-public-v2` |
| `publicationScope` | Literal `exploratory-follow-up` |
| `releasedAt` | Public release date or timestamp, at most 40 characters |
| `sources.article` | SHA-256 `73329bbea8ccdbc2107a1a5395710c97317ab397030dc583310e6852e3db8c8a` |
| `sources.interpretation` | SHA-256 `c74bc857775f09bb0fb93af25161d4f3fbd8ee7982b81187100174707c43d955` |
| `provenance.summary` | Short public description of the evidence and export, at most 1,000 characters |
| `artifacts` | At most 12 objects containing public `title`, site-relative `href` and full hexadecimal `sha256` |
| `hidden`, `bare`, `extension` | Independent optional sections; omit unpublished sections |

Every artifact link starts with `data/halo-response-20261007/`. URLs, parent
traversal, percent escapes, query strings and fragments are rejected. Artifacts
must actually be published and checked against their export manifest. A
displayed checksum is provenance, not proof that the browser independently
verified the file. The compact packet is limited to 2 MiB.

Display `provenance.summary` as the principal packet's original scope alongside
its recorded `releasedAt`, not as the current status of every follow-up section.
The separate six-resolution collective packet supplies the current linear
collective evidence; autonomous physical-source qualification remains pending.

Public files contain no machine paths, account details, private job identifiers
or raw seed labels. Use eight stable public whole-library labels, preserving the
same order across populations, probes and observables. Keep the private-to-public
mapping with the exporter. Do not turn quadrature nodes, velocity cells, time
samples or paired populations into independent draws.

The evidence release should include the matching theorem, the actual coefficient
certificate, the public executable verifier/runner, its instructions, exported
operands and a checksum manifest. Publication of a generic theorem alone does
not bind the selected actual binary coefficient vector. Population attenuation
records use their own actual coefficients and certificates.

## Figure 1: binding-resolved odd structure

`hidden.status` is `released`; `hidden.method` is `analytic-profile-export`.
`hidden.download` is an admitted artifact link. `hidden.profiles` contains
1–24 exported profiles, each with these fields:

| Field | Meaning |
|---|---|
| `id`, `label` | Unique public profile identifier and readable position/population label |
| `population` | One of the public population identifiers below |
| `coefficientsSha256` | Hash of the actual coefficient operand used for this profile |
| `radius`, `polarAngle` | Position in model units, with angle in radians from the fixed axis |
| `currentUnit` | Physical normalization of the plotted azimuthal current per unit binding energy |
| `samples` | 2–2,000 objects with strictly increasing `bindingFraction` and finite signed `currentPerBinding` |
| `integrals.ordinaryCurrent` | Actual exported integral of the ordinary azimuthal current |
| `integrals.energyCurrent` | Local azimuthal energy current, using H₀ = −e |
| `integrals.thirdMoment` | Local third azimuthal velocity moment, with its normalization stated in the download |
| `momentUnits` | Separate readable units for `ordinaryCurrent`, `energyCurrent` and `thirdMoment` |
| `analyticCurrentNull` | `true`, referring to the independently proved family identity |

`hidden.defaultProfile` identifies a supplied profile for the selected full
`hidden-plus` population. Choose its position prospectively from the initial
structural diagnostic, not from its forced work outcome.

The horizontal coordinate is `bindingFraction = e/ψ`, between zero and one.
The ordinate is **djφ/de**, not djφ/d(e/ψ). Record that distinction in the
download and include the ψ factor when verifying its integral. Analytic
endpoint values may be included only if evaluated and identified by the
exporter. Nothing is appended, clipped or integrated by the page. Line
segments are guides between exported analytic samples.

Retain small numerical current residuals. Do not force the exported integral
to zero or normalize a profile to its analytical answer. The energy current
is local, azimuthal and divergence-free, not radial energy emission. It is a
structural diagnostic and supplies no response/passivity qualification.

## Figure 2: complete-cycle work and controls

`bare` is the qualified **fixed-background, prescribed-cycle** export for the
retained narrative. The exact identity fields are:

| Field | Required value |
|---|---|
| `model` | `fixed-background-prescribed-cycle` |
| `completeCycle` | `true` |
| `duration` | `120` in dimensionless model time |
| `endpointAmplitude` | Two zeros: the imposed deformation vanishes at both endpoints |
| `amplitudeConvention` | `quadratic-coefficient` |
| `primaryNegativeWorkQualified` | `true`, from the separate scientific assessment |
| `finiteAmplitudeSignQualified` | `true` |
| `finiteAmplitudeMagnitudeQualified` | `false` |
| `finiteAmplitudeEstimateCorrelated` | `true` |

These flags identify the already retained claim. They are not a new assessor or
instructions to mark unresolved calculations as qualified. A changed finding
requires a reviewed narrative release, rather than replacing this packet.

`bare.uncertainty` contains `sampleUnit: whole-library`, `libraryCount: 8`,
`method: Student-t`, `degreesOfFreedom: 7`, `level: 0.95`, and `pointwise: true`.
`bare.libraryLabels` supplies eight distinct public labels in the actual paired
order. These nominal intervals provide no simultaneous coverage, calibrated
coverage guarantee or numerical bound.

`bare.cases` contains only recorded Ω = 0.10, 0.12 or 0.14, with no duplicates.
Each case has `omega`, `recordKind: linearized-orbit-estimate`, `complete: true`,
and `populations`. The Ω = 0.12 case is required. An absent probe stays disabled;
it is not extrapolated or displayed as zero. Forecasts and exploratory reused
libraries cannot be inserted as independent confirmation rows.

The public population identifiers and labels are:

| Identifier | Label and physical meaning |
|---|---|
| `reference` | Reference F₀ |
| `hidden-plus` | Selected full hidden population |
| `hidden-minus` | Properly rotated hidden population |
| `hidden-half` | Half hidden structure, using its actual certified coefficients |
| `hidden-ninetenths` | Nominal 90% hidden structure, using its separately certified rounded coefficients |

Every case retains at least the reference and both full hidden populations.
The two attenuation controls appear only where actually recorded. Each
population has `id`, `coefficientsSha256`, `work2` and `impulse2`. Each estimate
contains:

| Field | Meaning |
|---|---|
| `mean` | Supplied signed whole-library mean |
| `nominal95` | Supplied lower/upper pointwise sampling interval |
| `libraryValues` | All eight signed, paired whole-library values, in the shared label order |
| `refinementAllowance` | `{value, definition}` for the recorded primary Ω=.12 step comparison; `null` at neighbors, where the comparison was not performed |
| `rawBudgetAllowance` | `null` for these canonical tangent estimates: the finite-orbit mechanical proxy is a different comparison |
| `tangentConsistencyProxy.value`, `.definition` | Nonnegative maximum paired whole-library endpoint/TIME discrepancy; a tangent consistency diagnostic, not a finite physical mechanical error bound |

Each recorded probe also supplies `stepRefinementQualified`, true only at
Ω=.12, and `missingChecks`, an explicit list of unperformed controls. A
neighboring pointwise interval is not promoted to a numerically qualified
sign merely because it lies below zero. Missing proxies are null, never zero.

`bare.finiteAmplitude` separately retains the independently integrated
ε=.005 controlled-direct estimates, their raw physical mechanical proxy,
the supplied complete allowance, and shared-control covariance in the
evidence download. Those paths share a matched tangent control: the sign
qualification is correlated and does not establish forecast magnitude.

W₂ is the coefficient of ε² in **dimensionless total halo work**. J₂ is the
coefficient of ε² in **dimensionless angular impulse**. Do not divide either
coefficient by ε² again. Physical units are GM²/a and M√(GMa), respectively.
The exported total includes shape work plus Ω times angular impulse; an
open-history torque or an intermediate stored interaction energy is not the
complete-cycle witness. Retain failures in the evidence download and explain
selection/qualification separately.

The principal `hidden-plus.work2` at Ω = 0.12 must round to the printed retained
mean −4.36773 × 10⁻⁶ and interval [−4.65055, −4.08492] × 10⁻⁶. The display
checks these identities within 5 × 10⁻¹². This is a release/normalization check,
not a scientific tolerance or a replacement for independent budgets.

Diagnostic proxies remain separate from sampling whiskers. They are empirical
proxies, not rigorous continuum bounds. Tangent endpoint/TIME consistency is
not interchangeable with finite-orbit raw mechanical error. A finite-amplitude sign check using a
matched linearized control has correlated uncertainty; it is not a second
independent eight-library ensemble or qualified forecast magnitude.

Optional `bare.pulse` contains actual saved `{time, amplitude}` records with
strictly increasing times, starting at (0, 0) and ending at (120, 0), and at
least one positive amplitude. The amplitude is A(t), including the declared
shape once, not a reconstructed ε-scaled curve. Lines join saved nodes and do
not create new simulation states. `bare.download` links the closed-cycle export.

## Figure 3: separate linear collective packet

`collective-assessment.json` is independent of `figures.json`: copy the public
`result.json` produced by the reviewed `plot_collective_assessment.py` under
this public name, alongside `collective-assessment.png` and
`collective-assessment.csv`. Keep its private `owner-receipt.json` unpublished.
The renderer accepts schema `halo-response-collective-assessment-public-v1`,
complete six-row records and the pinned prospective assessor/criterion digests.
Publication still requires root's separate rendering, privacy, manifest and
actual pixel checks. The browser does not reconstruct component sums or decide
scientific qualification.

The packet's `records` retain the exact anchor/action128/Fourier16/Fourier64/
CB6/h=.01 coordinates, every available population's physical W2 and accumulated
J2, separate canonical Q+U/impulse, own endpoint orbit/self-field energies and
recorded raw residual maxima. Each population owns its linear response. Five
rows retain all five populations; Fourier64 has only its actual F0/A values.
No missing value is synthesized. `empirical_assessment` supplies F0/A anchor
values, five component budgets, total allowances and unchanged empirical
target/sign checks. CSV `anchor_*` fields retain this fixed-anchor scope and
are blank for other populations.

The static text is bound to root-supplied actual A W2
`-6.058545271387929e-6`, its allowance `3.6228416429609525e-8`, F0 W2
`1.9460900012728735e-5`, A J2 `-6.225750982534571e-5` and its allowance
`2.983031655453644e-7`. Public values must agree exactly before the figure and
table are displayed. Common model conventions are G=M=a=1, T120, rise/fall12,
Omega=.12, Mb=.1, reference Ib=.1 and shape=.8. W2/J2 are weak epsilon-squared
coefficients; reference inertia does not imply an evolved rotor.

Anchor segments are deterministic empirical proxies, not confidence intervals
or rigorous errors. The two Fourier shifts contribute their maximum, while
distinct absolute shifts and recorded raw physical residuals add without
cancellation. No combined finest corner has yet been tested, no bare forcing
tail is transferred, and no stability, nonlinear halo or autonomous-bar claim
is added. Public provenance is digests/version only; private paths, job IDs,
seed settings and source receipt dictionaries are excluded.

## Figure 4: a separately assessed autonomous extension

Omit `extension`, or give a status other than `qualified-release`, until the
scientific comparison has passed its own prospectively declared requirements.
The panel remains visibly pending. Conservation, quiet symmetry nulls or a
finite pole census alone do not provide such qualification.

A released extension has `status: qualified-release`, `complete: true`,
`independentBudgetQualified: true`, and `kind` equal to
`physical-autonomous-fixed-background`. Linear collective evidence uses the
separate packet and panel above. The autonomous extension supplies
a static public `figure` ending in `.svg` or `.png`, its `figureSha256`, explicit
`scope`, an informative `alt` and a scientifically complete `caption`.

The exporter binds the actual model, initial conditions, physical source,
duration, populations, paired numerical controls and qualification report.
A reactive fixed-background source must retain physical positive
inertia, actuator-free release, actual trajectory history, independent population
fields/states and errors relative to exchanged energy/angular momentum. This
extension certifies neither a fully nonlinear live halo nor a live stellar disc
or global stability. Prior rotor comparisons remain unqualified and physical-source
qualification is ongoing; no new nonlinear/autonomous history is supplied by
the collective packet.
Static figures must show only actual saved states or assessed comparisons; no
implied free-bar trajectory is allowed.

## Release checks and static access

The publication owner checks schema, arithmetic/units, actual evidence closure,
coefficient/source identities, privacy and plot-to-record agreement before
release. Ordinary signed values and paired covariances belong in the downloadable
evidence; the page is not a replacement assessor. Files and page text must agree
about failures, missing comparisons and qualification scope.

Publish static default versions of Figures 1 and 2 and insert them into the
HTML fallbacks before treating the page as a finished publication. Preserve the
known principal text, equations and uncertainty without JavaScript. The HTML
now uses the installed actual hidden-structure and principal-cycle PNGs as
defaults. They stay visible while records load, when records are unavailable,
and until a reader changes a control; detached SVG views replace them only
after construction. Images retain their full aspect ratios. Collective JSON
and the complete 27-row CSV remain linked without JavaScript. Check
missing/invalid data, phone/desktop layout, keyboard controls,
reduced motion and print output only in the separately admitted review stage.
