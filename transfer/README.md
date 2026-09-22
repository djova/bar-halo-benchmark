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

The default uses one nice10 scientific worker. --workers2 or4 allows parallel
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

It uses one nice10single-core worker by default; `--workers2` permits two. Each
case has a7200s limit. Allow roughly2.6CPUhours for the full matrix. `--smoke`
runs only two short unforced checks; those pass in a fresh pinned environment.
The compiled force kernel matches the original binary. The complete clean matrix
is now being rerun with the previously independently built AGAMA/GSL dependency;
its reference comparison is **not yet verified**. No new physical parameters,
particle sample or numerical margin are introduced.

The helper checks source manifests, records every case and supports `--resume`
after incomplete attempts have been preserved elsewhere. It runs the published
readback and compares against `reference/final-numerical-analysis.json` when that
terminal reference is available. An absent comparison is recorded as null; it is
not a passing reproduction claim. `--reference` can name an explicit published
reference. Numerical qualification is separate from reproducibility, and a
faithfully reproduced failure remains a failure. Original protocols and the
clean-reproduction criteria are included alongside the source.
