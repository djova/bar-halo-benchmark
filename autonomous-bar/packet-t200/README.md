# Autonomous rigid-bar follow-up: inspect the recorded comparison

Evidence release, 6 October 2026. This package exposes the completed finite
comparison and its unresolved physical interpretation. It does not reproduce
the particle evolution. The neighbouring precursor runner uses different
libraries and parameters and must not be used as this experiment's runner.

The baseline contains eight independent randomized libraries (7510101–7510108),
each supplying F0, plus and minus populations in fixed and responsive halo
fields: 48 population histories. The growth-step comparison uses the same
first four libraries in the responsive field, with paired baseline and refined
preparation. Populations, clock nodes and checkpoint continuations are not
additional independent libraries.

In units G = M_total = a = 1, the positive-density rigid bar has mass and
axial inertia 0.1 and initial angular speed 0.5946035575013605. Its speed is
held during shape growth through t = 20, then evolves autonomously through
t = 200. The responsive halo updates its represented field. This is a
constrained rotor and collisionless halo, not a live stellar disc or SIDM model.

## Read

`evidence/results.json` contains all 36 saved endpoint/late-window comparisons.
`evidence/readout-schema.json` defines the two CSVs, units, pairing and missing
values. Empty post-release cells before t = 20 mean unavailable, never zero.
The CSVs retain 101 actual saved nodes per history. Connecting them in a plot
does not create new simulated states. The three baseline figures and the
growth-step figure show actual recorded data.

The complete eight-library responsive endpoint interval spans zero. The
same-four preparation-step sensitivity exceeds the frozen numerical-share
criterion. Neither result establishes a physical null, a continuum upper
bound, or a robust ordering. Student-t intervals are nominal pointwise
sampling summaries, not calibrated simultaneous coverage or discretization
bounds. Full free-step, particle-number, basis and angular-order refinement
remains incomplete.

## Check saved arithmetic

Use Python 3.10 or later; no third-party dependency is needed:

```sh
python3 inspect.py evidence > arithmetic-recomputed.json
```

For files downloaded individually from the explorer, put `inspect.py`, both
CSVs and `results.json` in one directory and run `python3 inspect.py .` there.

The reader reconstructs signed within-library contrasts, their nominal t7/t3
intervals, zero-aware absolute displays, the same-four pairing, and the two
necessary interpretation failures from the supplied scalar operands. It also
checks the release/free impulse decomposition. Its own execution uses seconds
of CPU on the project host; that is not a runtime forecast for simulating a
halo. The included `arithmetic-check.json` is a record of a project-executed
check, not a claim that the reader has run it or that an outside group has
reproduced the dynamics.

`evidence/manifest.json` records hashes of the authentic exported operands,
readouts and growth figure, together with executed scientific source versions.
The added baseline figures are supporting published copies; the export
manifest does not claim to hash them. Source hashes identify private raw
records but do not make the phase archives or checkpoints publicly available.

## Reproduce dynamics

Complete public trajectory reproduction is **not available for this packet/T200
experiment**. Initial-state construction, the exact driver/native force
implementation and the owned continuation chain require a separate release.
No simulation is launched by reading this package or running the arithmetic
reader. The older local-resonance releases retain their own reproducibility
scope and scientific conclusions.

The arithmetic-reader source is offered under the public benchmark's MIT
license. Original text, original figures and original scalar data are offered
under CC BY 4.0, with attribution to Galaxy Bar and the identified evidence
release. No third-party observational catalogue is included here. These terms
do not relicense AGAMA, GSL or any separately supplied native dependency.
