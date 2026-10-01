# Hidden galactic dynamics: reference controls and evidence

This is a limited scientific source release for the exploratory October 2026
campaign. It supplies three independently runnable known-limit controls, the
terminal collision-law and modified-inertia solvers, optional halo-echo sources,
and compact published operands. It does **not** claim to reproduce all five
proposed directions or establish a new live-galaxy result.

The [interactive report](https://djova.ca/galaxy-bar/discovery.html) is separate
from the [earlier population-response article](../publication/web/paper.md).
Read the [completed collision/inertia summary](research/discovery-20261001/PUBLIC_TERMINAL_BRANCHES.md)
and [halo-echo model distinctions](research/discovery-20261001/PUBLIC_ECHO_SUMMARY.md).
The [manifest](manifest.json) records released file hashes and preserved source
hashes. Pin this repository's release commit when citing the package.

## Inspect, verify, reproduce

**Inspection:** read the two summaries and the compact
[collision-law](data/scattering.json), [inertia](data/inertia.json), and
[echo](data/echoes.json) exports. These preserve plotted values, conventions,
conditions, seeds where applicable, original archived record hashes, and exact
JSON pointers or array selections. Reading launches no computation and needs
no credentials. Archive record IDs are provenance names, not promises that a
corresponding raw run directory is included here.

**Verification:** recompute arithmetic from supplied operands: the collision-law
seed contrasts and pointwise intervals, the 53/32 angular-decay ratio, the three
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
