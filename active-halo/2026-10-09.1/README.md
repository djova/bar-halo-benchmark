# Hidden halo response: reproduce the complete driven cycle

**Outer release draft; packaging and publication remain pending.** This text
is intended to accompany the unchanged twelve-file calculation capsule. It
does not replace a historical release or the capsule's frozen README.

The calculation follows two positive stationary halo populations through the
same imposed gravitational cycle, including each population's own induced
field. Initially they have the same density, the same complete distribution
even under velocity reversal, and zero current at every position. Their
different odd orbital populations nevertheless produce different wakes and
opposite total cyclic work in the assessed calculation. Matching the initial
even distribution does not force passive response.

## Scientific result and reproduction scope

The independent energy128 × circularity64 refinement gives total work
coefficients approximately **+1.949638e-5 for F0** and **−6.024305e-6 for A**.
Its cumulative empirical sign ranges are approximately
`[+1.825591e-5, +2.073686e-5]` and
`[−7.155030e-6, −4.893579e-6]`, respectively. These ranges summarize the
recorded refinement and budget proxies; they are not rigorous continuum
intervals or confidence intervals. Circularity refinement and joint coverage
remain incomplete. Both original expanded work-magnitude screens remain false.
The raw complex waveform distances from the earlier refined calculation are
0.3283% and 0.2968%, while expanded empirical distances are 29.426% and
33.597%, failing the original 5% waveform target. Preserve this distinction
when interpreting the opposite signs.

The portable full preset reproduces the **energy64 × circularity64 GL64
calculation**, rather than the separate energy128 refinement. Its actual CLI
run has completed, and the same-configuration comparison passed all **62
original saved arrays and 117 raw scalar operands**, plus 12 separately
declared source-formula checks, using the predeclared software allowance
`5e-12 + 5e-10*abs(reference)`. Complex kernels, wakes, recorded clocks,
signed budgets and raw diagnostics were compared without phase alignment or
budget repair. This establishes delivery equivalence of the same equations.
Scientific independence belongs to the separate orbital construction and
causal evolution compared with the earlier solver; the portable rerun is not
another independent physical confirmation.

The evidence concerns the whole imposed cycle. It does not yet establish a
continuous dressed active frequency band, continuum or global stability,
sustained stationary emission, autonomous free-source growth, stellar-bar
formation, or an observed-galaxy match. The formal-spectrum assessment is not included in this finite-cycle report;
this scope choice implies neither failure nor unavailability. The earlier
126-case pole matrix is unfunded and uncompleted. Free-source growth remains
unqualified and is not implied by these cycle or delivery results.

The separate reciprocal source model derives its shape inertia Ms from the
carrier's potential-flow displacement. Its total stiffness Ks includes source
self-gravity once plus additional positive conservative constitutive support.
Its supported frequency is not a natural barotropic-fluid Ritz frequency, and
its mechanics have not been demonstrated for a stellar bar. This test does not
establish that actual baryonic galaxies supply this stiffness.
The public cycle runner uses the imposed source;
it does not test that source's autonomous motion.

## Calculation files and environment

The eventual release places the unchanged capsule in `calculation-source/`,
beside this outer README, `LICENSE`, `requirements.txt`, assessed figures and
privacy-reviewed validation records. Its `checksums.json` SHA-256 is:

```text
61c963c8d0c6b929701c5f5b18491741713b15fb69380583b0ab4a247fef2a00
```

The twelve files include `run_cycle.py`, `portable_io.py`, the three frozen
scientific modules, population and preset inputs, output definitions and the
checksum manifest. The runner constructs fresh orbits, signed Fourier
coefficients, retarded kernels and bare/own-field histories. It consumes no
saved numerical inputs and has no resume route. A source checksum identifies
those bytes; an actual run's output and terminal records identify a new
reproduction.

Use **Python ≥3.11**, **NumPy 1.26.4** and **SciPy 1.17.1** from a managed
environment. The completed validation used Python 3.11.14 with those dependency
versions. `requirements.txt` records the numerical pins; the runner installs
nothing and requires no plotting dependency or network access. Set numerical
thread counts to one in the execution environment, including OpenMP,
OpenBLAS, MKL, NumExpr, Accelerate and BLIS where present.

The capsule README, configuration status strings and preset name
`gl64-provisional` retain their preparation-time wording. Their old statements
that public GL64 execution or equivalence is pending are historical. This
outer status and the completed validation receipt supersede that execution
status, without changing the frozen source or upgrading scientific
qualification.

## Inspect, then regenerate

From the eventual release root, inspect either configuration without numerical
integration:

```sh
cd calculation-source
python3 -B run_cycle.py --preset gl8-preview --preview
python3 -B run_cycle.py --preset gl64-provisional --preview
```

For an actual fresh calculation, choose a new output directory outside the
capsule whose parent already exists:

```sh
python3 -B run_cycle.py --preset gl8-preview --output ../reproduced-gl8 --expected-manifest-sha256 61c963c8d0c6b929701c5f5b18491741713b15fb69380583b0ab4a247fef2a00
python3 -B run_cycle.py --preset gl64-provisional --output ../reproduced-gl64 --expected-manifest-sha256 61c963c8d0c6b929701c5f5b18491741713b15fb69380583b0ab4a247fef2a00
```

GL8 regenerates its smaller energy8 × circularity8, Fourier N16, spatial
CB0–2 and dt=.1 calculation. It is a useful executable preview, with its own
completed CLI/equivalence checks; it does not reproduce the full GL64 or E128
result. The full preset uses energy64 × circularity64, Fourier N64, spatial
CB0–6 and dt=.025, giving 4,801 recorded times. Both use duration T=120,
rise/fall=12, envelope peak .8 and pattern speed Ω=.12. The quadrupole
frequency is ω=2Ω=.24; the CLI's `omega` parameter denotes pattern Ω.
Both m=−2,+2 sectors, both populations and bare/own-field responses are
computed separately in the fixed total potential. Halo mass .9 is the exact
equilibrium complement to the .1 material carrier, not a .9 rescaling of the
Plummer density.

The full portable run used **17,620.373073 process-tree CPU seconds** on the
validation host, with maximum child RSS 1,016,408 KiB. Its admitted limits were
27,000 CPU seconds, 43,200 wall seconds, 4 GiB RAM and 512 MiB output. These
measurements and limits are not runtime or memory guarantees on another
platform. Choose external resource limits before running: portable I/O checks
source/output identity, atomic writes and an optional `STOP` file, but supplies
no CPU, wall-time, RAM or aggregate-output ceiling.

## Outputs, units and figures

`result.json` contains eight signed endpoint records and four paired totals.
`history.npz` contains the actual clock, complex kernels/wakes, physical
sources, power, shape-power, torque, work, shape-work and angular-impulse
histories. `orbit-library.npz` contains the fresh orbital inputs. `START.json`
and a successful unchanged-input `TERMINAL.json` bind the run to its source
manifest and configuration. A checkpoint, partial prefix or isolated
`complete` flag is not a complete reproduction; retain failed receipts rather
than substituting a partial result.

Write the physical perturbation as ε times the saved first-order source. Its
peak shape .8 is already included. Wake coefficients are per ε; work W2,
power P2 and angular impulse J2 are per ε². In model units G=Mtotal=a=1;
with t*=sqrt(a³/(G Mtotal)), E*=G Mtotal²/a and
J*=Mtotal sqrt(G Mtotal a), physical work, power and impulse are
ε²E*W2, ε²(E*/t*)P2 and ε²J*J2. Do not apply .8² again. These weak
perturbation coefficients are not stellar-bar mass fractions.

The completed figure assets available for the final release are
`independent-cycle-wake-refinement` (PNG/SVG),
`bare-discrete-power-and-strength` (PNG/SVG),
`cycle-work-mechanism` (PNG/SVG/CSV), and
`finite-cycle-strength-work` (SVG). The first shows raw complex history
comparisons; the second shows discrete bare frequency points and the central
bare-affine strength relation, not a continuous dressed band. The mechanism
figure separates recorded rotational and envelope-change work over the whole
E128 energy × 64 circularity cycle, dt=0.025. Its global source overlap is not
a density-axis angle or a free-growth measurement. The fourth shows five
computed strengths with GL64 energy × 64 circularity centers, dt=0.025, and
separate empirical action/time/budget allowances. It connects no collective
responses and establishes no threshold or stationary band. Exact values and
full numeric downloads belong beside the figures; a large default table is
unnecessary. Final figure URLs, sanitized validation downloads and the report
remain publication dependencies.

## License and public data boundary

Retain the included **MIT License**, copyright ©2026 djova, with distributed
software and associated documentation. The unchanged notice has SHA-256
`fb80925f435f5b06903d07918d84e5b234de5604cb0a03e8b5b050334ec79331`.
NumPy and SciPy retain their own licenses and are not bundled. Generated
figure/numeric downloads must carry an explicit project-rights notice; this
package includes no third-party observational catalogue and grants no rights
to external papers or data merely because they are linked.

Public validation must retain actual source/configuration/result identities,
the distinction between delivery and scientific evidence, and all failed
accuracy screens. Export only reviewed scientific fields. Private host
meters, operational inventories, process identifiers, credentials, local
filesystem paths and unreviewed operating-system failure text are not public
dependencies or package contents. Historical releases and their claims remain
unchanged.


## Five-strength finite-cycle extension

This report also includes the closed Work C assessment: five fixed strengths, three fixed refinements, both signed sectors and bare/own-field responses. The endpoint controls are retained; eighteen intermediate own-field cells were solved freshly. Full signed endpoint budgets, shape/rotation work, empirical sensitivities and the four frozen forecast comparisons are available under `evidence/strength-map.json` and the accompanying CSV files. Original expanded accuracy failures remain unchanged. No stationary band, threshold, stability or free growth is inferred.

The separate `cached-strength/run_strength.py` and `cached-strength/README.md` are source-prepared executable extensions. This report provides no bound cache assets or public extension execution receipt. Their use requires the authenticated cached libraries/kernels described in that README; preparing source or checking the already completed central GL64 CLI does not establish that this new extension has executed. Its public runtime and large-cache hosting remain separate release duties.
