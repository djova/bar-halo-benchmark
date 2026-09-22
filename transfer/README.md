# Optional full Cartesian transfer reproduction

This uses the exact frozen caseB conditions and unmodified archived3D runner.
It needs a C++17 compiler and a separately built AGAMA at revision
f302756b8af2b763db58e278e30478517dc8eea3 with the full stable-angles.patch from
../optional-agama applied. Preserve upstream licensing; no AGAMA/GSL binary is
redistributed. Do not use the deliberately failed half-angle-only patch.

Install transfer/requirements.txt in the pinned Python3.11 environment. On Linux,
with a C++ compiler, make, git and Python development headers available, the
optional helper builds pinned GSL2.8 and the patched AGAMA in a new local directory:

```
python transfer/build_linux.py --out dependency-build
```

This setup downloads the named upstream source dependencies, verifies the GSL
archive checksum, uses one nice10 compiler process, and installs nothing
system-wide. It disables unused optional integrations. Preserve the upstream
licenses. Use dependency-build/Agama as PATH_TO_PATCHED_AGAMA below. The final
experiment command runs offline after these prerequisites exist.

From the repository root:

```
python transfer/reproduce.py --agama PATH_TO_PATCHED_AGAMA --out reproduced-transfer
```

The default uses one nice10 scientific worker. `--workers 2` or `--workers 4` allows parallel
cases, each with one BLAS/OpenMP thread. It compiles a separate portable force
kernel, then regenerates the two forced and two unforced65536-particle samples
and matched16384-particle timestep/cadence refinements from fixed seeds. No private
initial arrays, host configuration or API credentials are used. Every case has a
7200second wall limit and outputs actual trajectories, budgets and source hashes.
The full run takes hours, depending on the CPU. --smoke runs only the independent
short unforced numerical pilot; it cannot reproduce or qualify the physical result.

The analysis retains raw3D means, paired reduced means, covariance, uncertainty,
actual numerical changes and the original failed caseA prerequisite. It will not
silently run caseA or change the frozen adequacy band. The clean dependency build
passes the independent80-digit coordinate test and the short unforced smoke.
The complete isolated eight-case rerun also passes. From a fresh dependency
build and environment, the seven checked means and numerical shifts differ by
at most1.66e-13, below the fixed1e-9 tolerance; every gate and decision agrees.
It uses2.39scientific core-hours. Individual trajectories are not bitwise
identical: the largest final Cartesian-component difference is1.93e-6. See
`reference/clean-reproduction.json` for every array comparison. The reference
checker rejects missing cases or controls, not just disagreeing means. The first archived3D experiment
is numerically unqualified: reproducing that failure is an intended outcome,
not something this command silently repairs.

## Reproduce the final timestep and noise-cadence matrix

The separate command below regenerates six16384-particle cases using the exact
fourth-order kernel and nested noise source:

```
python transfer/reproduce_numerical.py --agama PATH_TO_PATCHED_AGAMA --out reproduced-numerical
```

It uses one nice10single-core worker by default; `--workers 2` permits two. Each
case has a7200s limit. Allow roughly2.6CPUhours for the full matrix. `--smoke`
runs only two short unforced checks; those pass in a fresh pinned environment.
The compiled force kernel matches the original binary. The original final matrix is complete: both timestep intervals pass, but both
noise-cadence intervals miss the unchanged numerical allowance. The complete clean six-case matrix now reproduces every scientific decision,
including the failed cadence qualification. It uses2.636scientific core-hours.
The largest compared scalar difference is1.44e-13, below the unchanged1e-9
reproduction tolerance. Exact IDs, initial action–angle states, reduced torques and Brownian
streams match; Cartesian trajectories retain the documented small differences.
See `reference/clean-final-reproduction.json` for all array and scalar checks.
This fresh source/environment reuses the previously independently built AGAMA/GSL;
it is not a third dependency build or an independent physical sample.

The helper checks source manifests, records every case and supports `--resume`
after incomplete attempts have been preserved elsewhere. It runs the published
readback and compares against `reference/final-numerical-analysis.json` when that
terminal reference is available (now included). An absent comparison is recorded as null; it is
not a passing reproduction claim. `--reference` can name an explicit published
reference. Numerical qualification is separate from reproducibility, and a
faithfully reproduced failure remains a failure. Original protocols and the
clean-reproduction criteria are included alongside the source.

## Inspect and regenerate the unforced calibration

```
python transfer/reproduce_coefficients.py --agama PATH_TO_PATCHED_AGAMA --out reproduced-calibration
```

This optional two-second calculation regenerates the original action scans,
frequency gradients, bar Fourier coefficients and distribution-function slopes.
It checks their original checksum against the forecast's pre-outcome record and
derives every frozen orbital input. No forced trajectory is an input. The
original scripts and full reference table are in `scripts/noise_sweep/` and
`calibration/`; the command uses one nice10 single-core worker and a300s limit.

The independently rebuilt dependency reproduces the frequency gradients,
Fourier coefficients and all derived frozen orbital inputs within the declared
tolerances. It **does not pass every scalar comparison**:100of1304 checks miss
the fixed tolerance, all in finite-difference DF slopes or their scaled values.
The largest slope difference is1.954e-9. No reference or tolerance is adjusted.
The command writes the generated table and full verification, marks
`COMPARISON_FAILED`, and exits nonzero when those strict comparisons fail.
This does not change the original forecasts or establish their physical adequacy.
See `calibration/clean-comparison.json` for the complete readback and
`calibration/PROTOCOL.md` for the unchanged criteria and correspondence repair.

A shared-input arithmetic diagnosis retains the discrepancy even with50-digit
logarithms: the dominant difference is already in the returned DF values, rather
than logarithm subtraction. See [the measured outcome and limits](calibration/arithmetic/OUTCOME.md),
its protocol, raw binary64 values, scripts and figure. This does not identify the
internal dependency calculation responsible, or turn the original failed checks
into passes.

## Reproduce the fixed independent cadence confirmation

The original full twenty-case calculation has finished and **fails** the unchanged
noise-cadence interval criterion. Both timestep intervals and all local/unforced
checks pass. See [the outcome and stopping decision](INDEPENDENT_CADENCE_OUTCOME.md)
and [the full-precision reference](reference/independent-cadence-analysis.json).
The conditional physical extension will not run. The new complete standalone
rerun is pending; only its previously documented smoke/control execution is
verified at present.

On Linux, using the same pinned environment and patched dependency:

```sh
python transfer/reproduce_confirmation.py --agama PATH_TO_PATCHED_AGAMA --out reproduced-confirmation
```

This generates the exact twenty cases in the explicit amendment: 131,072 previously
unused particle IDs at candidate and half-cadence settings, a 16,384-particle
half-step pair, and a 4,096-particle unforced pair. It runs the unchanged scientific
analyzer only after every case is complete. No earlier sample is pooled in, no
physical parameters or numerical margin change, and no physical extension launches.

The command defaults to one worker at nice=10 using one core; `--workers 2` or
`--workers 3` runs concurrent cases. Each case has a 7,200-second wall limit, with
an aggregate 14 CPU-hour ceiling and a 41-hour elapsed stop for the complete queue.
Allow roughly 13 CPU-hours on the experiment's CPU; a slower machine may reach a
limit and preserve an incomplete result. Source and dependency hashes, exact
settings, individual arrays and a CPU ledger are recorded. Preserve stopped
attempts; the command refuses to overwrite an output directory. Use a separate
package checkout for concurrent reproduction commands.

`--show-design` prints every case without compiling or running anything. `--smoke`
runs only two 128-particle, short unforced checks in the same guarded pathway.
The package's execution and analyzer controls can be checked separately:

```sh
python transfer/check_confirmation.py
```

Those disposable fixtures check wall/CPU stops, external-source refusal,
descendant cleanup and a known reduced-only shift that must fail the discrepancy
gate even when the raw 3D shift passes. They are software checks, never simulation
evidence. An isolated public-source copy passes both real short unforced checks,
using the previously independently rebuilt dependency and pinned environment.
This is not a full twenty-case clean reproduction or a new dependency build.
The original confirmation is complete and failed its numerical qualification;
the complete same-sample standalone reproduction is now running. Its terminal
reference comparison is still pending. `reference_comparison: null` means no such
comparison, and reproducing a failed qualification does not change that decision.

The [unforced domain readback](calibration/domain/README.md) regenerates the coefficient ranges, initial-gradient comparison and retained harmonic spectrum from the original public inputs in about one CPU second. It introduces no new trajectory or physical qualification.

The [conditional full-population estimator](PHYSICAL_ANALYSIS.md) is also public. Its assembly pathway can be checked with disposable known-value fixtures. The original confirmation did not meet its prerequisite, so the physical extension will not run; those fixtures are not a physical sample.

The confirmation command now compares every aggregate, refinement and paired
chunk/control estimate against the complete reference. It requires the same
failed qualification and unchanged scientific margin. A successful reproduction
does not turn this into a qualified physical forecast. `--stop-utc` can shorten
the default stop using an explicit timezone-aware ISO timestamp.

After a complete rerun, regenerate the comparison and variance figures with:

```sh
python transfer/scripts/noise_sweep/plot_cadence_confirmation.py --analysis reproduced-confirmation/analysis/result.json --original-analysis transfer/reference/final-numerical-analysis.json --root reproduced-confirmation/cases --out reproduced-confirmation-figures
```

The two comparison panels use the same normalized horizontal scale. Original
and independent samples stay separate; no path is removed from the variance
curves. The archived figures are in `reference/confirmation-figures/`.
