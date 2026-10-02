# Hidden galactic dynamics: reference controls and evidence

This is a limited scientific source release for the exploratory October 2026
campaign. It supplies three independently runnable known-limit controls, the
terminal collision-law and modified-inertia solvers, optional halo-echo sources,
compact published operands, a compact exact-twin saved-response analysis, and
the closed cored feedback experiment's outputs, completed growth histories and
finite cusp-pulse outputs with separate saved-arithmetic replay. The analytic twin construction
removes the earlier finite-grid streaming mismatch. This release does **not**
claim to reproduce every campaign experiment or establish a new live-galaxy result.

The [interactive report](https://djova.ca/galaxy-bar/discovery.html) is separate
from the [earlier population-response article](../publication/web/paper.md).
Read the portable [Markdown report](REPORT.md), the [exact-twin result](research/discovery-20261001/PUBLIC_TWINS_EXACT_SUMMARY.md), the [completed collision/inertia summary](research/discovery-20261001/PUBLIC_TERMINAL_BRANCHES.md),
the [halo-echo model distinctions](research/discovery-20261001/PUBLIC_ECHO_SUMMARY.md),
and the [cored selective-heating result](research/discovery-20261001/FEEDBACK_PUBLIC_SUMMARY.md).
The [interim scientific learning note](research/discovery-20261001/LEARNINGS.md)
connects these outcomes to the remaining tests. The [manifest](manifest.json)
records released file hashes and preserved source
hashes. Pin this repository's release commit when citing the package.

## Inspect, verify, reproduce

**Inspection:** read the summaries and the compact
[collision-law](data/scattering.json), [inertia](data/inertia.json), and
[echo](data/echoes.json), [exact-twin response](data/twins-exact.json),
[unforced velocity](data/twins-velocity.json), and [feedback](data/feedback.json)
exports. These preserve plotted values, conventions,
conditions, seeds where applicable, original archived record hashes, and exact
JSON pointers or array selections. Reading launches no computation and needs
no credentials. Archive record IDs are provenance names, not promises that a
corresponding raw run directory is included here.

**Verification:** recompute arithmetic from supplied operands: the collision-law
seed contrasts and per-condition nominal 95% intervals (not simultaneous
intervals), the 53/32 angular-decay ratio, the three
harmonic frequencies, or the saved echo-force peaks. This checks published
relationships conditional on supplied outputs; it does not evolve the underlying
physical experiment.

**Known-limit reproduction:** generate inputs from equations and recorded seeds,
then run the three controls below. The original Python interpreter was
3.11.14; the tested numerical versions are pinned in
[requirements.lock.txt](requirements.lock.txt). That file pins the three direct
numerical dependencies, rather than every transitive packaging dependency.

From the repository root:

```sh
python3.11 -m venv .venv-discovery
.venv-discovery/bin/python -m pip install -r discovery/requirements.lock.txt
.venv-discovery/bin/python discovery/scripts/discovery/reproduce_controls.py \
  --out ./discovery-controls-rerun
```

Choose an output directory that does not already exist. After dependency
installation, this command works offline. It runs three sequential numerical
children at nice=10, one numerical thread each, with a 180-second wall limit
for each child. Its receipt reports child CPU, source hashes and original gates.
The test is inexpensive on the recorded platform; use the included
[control reproduction receipt](reproductions/public-controls-01/receipt.json)
for its measured cost, rather than treating that as a universal runtime.

The command regenerates:

- Published harmonic reference equations at q=2,4,8, including single-frequency,
  selected conservation, multiple-guess and mode-grouping checks.
- A fixed-seed equal-mass elastic operator test, with matched conditional
  velocity drift and raw second tensor and a fourth angular-decay ratio 53/32.
- A known constant-shear collisionless echo on a canonical cylinder, including
  analytical prediction and erased-memory controls.

It does **not** regenerate the 16-seed collision-law response matrix, radial
halo echo, spatial two-frequency halo prediction, heating experiments, halo
twins, live galaxies, or observations. Repeating released seeds is a software
reproduction, not an additional independent physical sample. Passing these
controls cannot establish numerical convergence or physical validity for those
other calculations.

## Run one full collision-law case

The equal-mass gas has one periodic position and three velocity components.
Both elastic laws conserve pair momentum and energy. An external moving cosine
wave supplies the signed impulse. The optional `--role equilibrium` and
`--role stress` controls use the same engine; no halo, self-gravity or calibrated
SIDM operator is supplied.

These two commands regenerate the original-waveform pair at one recorded seed:

```sh
nice -n 10 .venv-discovery/bin/python discovery/scripts/discovery/scatter_moment_screen.py \
  --out ./collision-A-260521 --law A --role resonance --seed 260521 \
  --n 8192 --cells 32 --dt 0.01 --duration 40 --kappa 0.02 \
  --epsilon 0.25 --omega0 0.5 --sweep 0.025
nice -n 10 .venv-discovery/bin/python discovery/scripts/discovery/scatter_moment_screen.py \
  --out ./collision-B-260521 --law B --role resonance --seed 260521 \
  --n 8192 --cells 32 --dt 0.01 --duration 40 --kappa 0.02 \
  --epsilon 0.25 --omega0 0.5 --sweep 0.025
```

Read `/history/79/impulse` in each `result.json` and calculate **B minus A**. A single seed cannot reproduce the reported interval. The original
16 seeds are 260521 through 260536. The second waveform uses epsilon=0.16,
sweep=0.04 and seeds 260541 through 260556. The selected refinements independently
use dt=0.005 or cells=64 with all original seeds. Complete settings and operators
are in [SCATTER_MOMENT_PROTOCOL.md](research/discovery-20261001/SCATTER_MOMENT_PROTOCOL.md).

The included `scatter_moment_analyze.py` expects the historical named directory
layout under `discovery/results/discovery-20261001/scattering`, including the
ordinary-control results. Its phases are `controls`, `original`, `second`, and
`refinement-original`. The protocol and exports identify those filenames. No
one-command full-ensemble launcher or runtime promise is included. Do not run
an analysis phase against an incomplete set, substitute a saved control flag for
regenerated controls, or interpret the one-seed commands as a new significance
test. The published final refinement sign requirement failed.

## Exact-moment halo twins

The [exact-twin summary](research/discovery-20261001/PUBLIC_TWINS_EXACT_SUMMARY.md)
and [derivation](research/discovery-20261001/TWINS_EXACT_MOMENTS_DERIVATION.md)
construct frozen positive populations with identical local density, mean velocity
and all even-total-degree velocity moments. The p=8 reference-frequency contrast
is 8.49e-5 in reference mass–action units and passes the selected phase/timestep
screen. The p=4 phase screen fails; p=6 has a positive supplementary lower margin
smaller than its largest measured phase shift. The other frequency has no phase
refinement. These flags remain separate from a combined error guarantee. The
plus/minus ratio 1.446 is a ratio of point means without a qualified ratio interval.
No live response or prospective forcing-history forecast is established.

The [response export](data/twins-exact.json) preserves six correlated comparisons,
all eight library vectors and contrast/reference covariance. The
[velocity export](data/twins-velocity.json) shows a recorded unforced marginal
and third moments; its quadrature is not rerun by the following command.
The [velocity source notes](operands/exact-twins/README.md#unforced-velocity-view)
identify its fixed inputs, equations and output selections. The gradual bar-growth
ensemble is supplied in the .3 addition described below.

After installing the dependencies above, replay the saved-response analysis:

```sh
nice -n 10 .venv-discovery/bin/python discovery/scripts/discovery/replay_twins_exact.py \
  --out ./twins-analysis-rerun
```

The [eight compact NPZ libraries](operands/exact-twins/manifest.json) total
301,638 bytes and supply binding energy, L, folded Lz, common absolute masses,
sampling density Fq, both partner impulses for both histories, and four selected
refinement pairs. They contain no initial states, phase arrays or movies. Original
input hashes and exact array selections are retained. Fq was evaluated once with
the archived AGAMA DF during extraction; public replay uses that stored operand
and requires only NumPy and SciPy. It rebuilds the original 96-term positive F0
series, uses frozen alpha without fitting, and applies Fplus/minus divided by Fq
without per-population or per-library mass renormalization.

The [checked analysis execution](reproductions/twins-analysis-01/receipt.json)
reproduced 808 numerical values exactly: all six means and standard errors,
pointwise and six-comparison Bonferroni intervals, plus/minus/reference
uncertainties, full covariance and selected paired contractions. This is an
arithmetic/software replay conditional on supplied response impulses, not
regeneration of orbit evolution, a new physical sample or a test of another
forcing history. Eight-library Student-t coverage remains uncalibrated.

The separate unforced algebra challenge uses Python's standard-library
Fraction and Decimal arithmetic:

```sh
nice -n 10 .venv-discovery/bin/python discovery/scripts/discovery/twins_proof_challenge.py \
  --out ./twins-proof-rerun.json
```

It independently rebuilds all three exact rational positivity bounds and the
streaming cancellation from [frozen operands](operands/exact-twins/frozen-populations.json).
For the optional 80-digit alpha check, install
[proof-optional-requirements.lock.txt](proof-optional-requirements.lock.txt) and
add `--mpmath`; the [recorded proof execution](reproductions/twins-proof-01/result.json)
used mpmath 1.3.0. The original AGAMA-importing preflight and its original
contraction source are inspection snapshots; the portable adapters are the
commands above. No collective-stability or formation-history claim follows.

The [priority review](research/discovery-20261001/TWINS_PRIORITY_REVIEW.md)
places the construction alongside earlier halo-population and resonant-response
work; it does not establish novelty.

## Cored selective heating: published outputs

The [feedback summary](research/discovery-20261001/FEEDBACK_PUBLIC_SUMMARY.md)
and [scientific export](data/feedback.json) report a prescribed frequency-8 gas
pulse in a fixed, initially cored spherical potential. It gives much less energy
per unit mass to the selected whole stellar population than to a stationary
central halo tracer. Inner stars receive substantially more heating than that
whole-population normalization suggests. The retained amplitude, timestep and
independent-estimator checks qualify this bounded example; they establish
neither a dark-matter core nor acceptable heating in an observed old disk.

This package supplies the recorded feedback outputs and scientific summary,
without a feedback simulation or bootstrap replay. Its evidence hashes identify
archived records. The separate cuspy-halo and gradual-bar calculations now have
published outcomes and saved-array replay packages, described below. Their
complete orbital evolution is not regenerated by those readers.

## Optional halo-echo calculations

The radial and spatial source families are provided for inspection and manual
reproduction. They require AGAMA as well as the dependencies above. This bundle
redistributes neither AGAMA nor GSL binaries. The existing outer-repository
[dependency build](../transfer/build_linux.py) retrieves pinned AGAMA revision
`f302756b8af2b763db58e278e30478517dc8eea3` and GSL 2.8 and applies the existing
[stable-coordinate patch](../optional-agama/stable-angles.patch).
Inspect its prerequisites and upstream licenses before executing it. A dependency
build is a separate, longer operation; it is not run by the known-limit driver.

From the repository root, an optional local build and explicit library selection
are:

```sh
.venv-discovery/bin/python transfer/build_linux.py --out ./discovery-agama-build
export ECHO_AGAMA_LIBRARY="$(pwd)/discovery-agama-build/Agama"
```

The environment value resolves the user's own build directory and supplies no
credentials. `echo_halo.py` imports this directory before its fallback search.
Keep the export in the shell used for the following optional commands.

For the recorded baseline radial cohort, the finite run can be invoked as:

```sh
nice -n 10 .venv-discovery/bin/python discovery/scripts/discovery/echo_monopole.py \
  --out ./radial-echo-rerun --ne 512 --nL 32 --nr 256 \
  --tau 16 --amplitude 0.002 --support-amplitude 0.004 \
  --taper-low 0.02 --taper-high 0.04 --cadence 1 --end-factor 2.5 \
  --memory-ne 512 --memory-nL 65 --memory-nr 128 \
  --radial-quadrature eccentric_anomaly --memory-quadrature eccentric_anomaly \
  --method eulerian
```

The full recorded config and operator details are in
[data/echoes.json](data/echoes.json) and
[ECHO_MONOPOLE_PROTOCOL.md](research/discovery-20261001/ECHO_MONOPOLE_PROTOCOL.md).
Check every output field rather than assuming this manual run reproduces the
held-out separation, stronger pulses, independent harmonic prediction, or
all numerical comparisons. The optional family also contains radial-response,
readback and specified stellar-oscillator tools. Their arguments identify
explicit input directories. Raw historical arrays are not input dependencies
of the forward solver and are not included as an opaque archive.

The positive-source spatial `echo_two_frequency.py` supplies a leading
canonical response prediction and a separate first-pulse quiet-field screen;
[ECHO_TWO_FREQUENCY_PROTOCOL.md](research/discovery-20261001/ECHO_TWO_FREQUENCY_PROTOCOL.md)
explains the Fourier selection and model restrictions. It is not a finite-
amplitude 3-D trajectory validation. The original `echo_halo.py` quadrupole
pilot remains unresolved; its default quasi-random action sample cannot be
assigned particle-IID confidence intervals. That helper is included because
the optional models reuse its field and coordinate routines, not because the
pilot has become a qualified result.

## Source preservation and licensing

Scientific source files and named frozen protocols are copied byte-for-byte from
the retained campaign. Their SHA256 values are recorded in the manifest.
The runnable optional echo files are the campaign’s final source versions.
Earlier baseline and spatial-prediction snapshot hashes are retained separately
in [source-snapshots/](source-snapshots/README.md), rather than silently claiming
that every historical result used the same final file.
Some protocols contain historical relative links into the experiment archive;
those identify unshipped records, not additional downloads. The clean summary
links are adapted to this package's `data/` layout; the manifest records both
their archived and released text hashes.

The outer repository's [MIT license](../LICENSE) applies to new code, original
expository text and derived data in this release. No new license is asserted
over cited papers or other third-party materials. AGAMA's own source is supplied
under its stated permissive terms, with included third-party components and
GPL restrictions from linked GSL; retain all upstream notices in any local
build. See [LICENSING.md](LICENSING.md). There are no downloaded papers,
upstream libraries, system binaries, host queues, credentials or private
operational records in this bundle.


## Added in discovery-2026-10-01.3

Read the [growing-bar response](data/twins-growth-v1.json) and
[its complete saved-arithmetic package](operands/twins-growth-v1/README.md).
The command regenerates contractions, intervals, covariance and selected
numerical decisions from supplied arrays. It does not regenerate the orbits:

```sh
python discovery/scripts/discovery/replay_twins_growth_v1.py --out growing-bar-arithmetic
```

The [cuspy halo record](data/feedback-cusp.json) and
[replay guide](research/FEEDBACK_CUSP_REPLAY.md) expose finite pulse energy gains,
paired numerical controls and a separately verified known map. No finite stellar
selectivity ratio or self-consistent core follows. Both additions have their own
model clock and uncertainty conventions. The earlier .2 tag and canonical paper
remain immutable. Reading these files needs no credentials or private host.

The [force and action-support package](research/discovery-20261001/TWINS_FORCE_SUPPORT_PUBLIC_V1.md)
retains the failed paired-particle live screen, its close-pair energy diagnosis,
selected force-opening refinements, and descriptive partitions of the recorded
bar response. Its [NumPy-only reader](scripts/discovery/replay_twins_force_support_v1.py)
recomputes 8,243 numeric and 221 logical/string values from five compact arrays:

```sh
python discovery/scripts/discovery/replay_twins_force_support_v1.py --out force-support-arithmetic
```

This recomputes saved diagnostics; it does not regenerate the forces or establish
live stability. The [two-integral boundary](research/discovery-20261001/TWINS_TWO_INTEGRAL_BOUNDARY.md)
explains why the analytic three-integral construction does not contradict
uniqueness results for more restricted distribution functions.


## Added in discovery-2026-10-01.4

[Checks behind the results](CHECKS.md) separates numerical qualification from
finite-sample shell variation, unresolved warm-star heating and spatial-echo
quadrature error. The [control operands](operands/checks-v1/README.md) include
all six paired phase profiles and two small warm-response arrays. A NumPy-only
reader reconstructs the published arithmetic without orbit evolution:

```sh
python discovery/scripts/discovery/replay_checks_v1.py --out checks-arithmetic
```

The nine original spatial exact-zero failures remain visible alongside a
separately frozen energy-only pair that clears the instantaneous gate. No late
finite spatial echo or stellar readout follows. The live quiet matrix passes its
new numerical checks but retains shell-moment flags; fixed-field phases explain
a substantial part of those excursions without proving softened equilibrium.
The finite warm-star measurement remains sampling-unresolved even after the
tighter selected reference passes. The original .1–.3 tags remain immutable.
