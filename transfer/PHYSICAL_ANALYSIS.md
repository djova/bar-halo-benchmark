# Inspect the conditional full-population estimator

This is analysis preparation. The original independent numerical confirmation
is complete and failed its noise-cadence interval criteria. The conditional
524,288-ID physical extension will not run in this campaign. The separate
same-sample reproduction of that confirmation has completed and reproduces the
failed numerical qualification. No physical reference result or full-population
reproduction is claimed here.

The unchanged prepared analyzer and its original assembly contract are now public:
`scripts/noise_sweep/analyze_physical_transfer.py` and
`PHYSICAL_TRANSFER_ASSEMBLY.md`. They require exact candidate-operator coverage
of seed8302 IDs0–524287, including the complete independent numerical confirmation.
They preserve the frozen prediction and numerical allowance, refuse mismatched
sources or incomplete inputs, and report both the full population and the fixed
393,216-ID diagnostic that excludes the numerical-confirmation sample.

The public package can exercise this full analysis pathway now, using only its
pinned Python/NumPy/SciPy environment:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  nice -n 10 python transfer/check_physical.py --out physical-analysis-check.json
```

This creates temporary **mathematical fixtures**, not simulated orbits. It uses
the exact full-size seeded action–angle array, artificial torque vectors with
known means, and explicitly artificial Cartesian states, kernel identities and
gate placeholders. The numerical analyzer receives all20case fixtures. The
physical analyzer then assembles all524288IDs and recovers independently known,
different full-sample and disjoint means. Separate corruptions must be refused:
failed numerical qualification, a changed source manifest, and both members of
a pair sharing the same wrong initial state. Smaller controls cover gaps,
overlaps, ordering, mixed operators, nonfinite values and decision boundaries.

The fixtures are deleted on exit. They establish software behavior only: no
force solver is called, no actual trajectory is validated and no physical
inference follows. On the experiment CPU the check takes about five seconds.
An isolated package-copy check and its source hashes are recorded in
`reference/physical-analysis-controls.json`. This is not a new dependency build.

Once complete, qualified simulation directories exist, the actual readback is:

```sh
python transfer/scripts/noise_sweep/analyze_physical_transfer.py \
  --prefix-root PREFIX_CASE_DIRECTORY \
  --confirmation-root CONFIRMATION_CASE_DIRECTORY \
  --confirmation-analysis CONFIRMATION_ANALYSIS_JSON \
  --physical-root PHYSICAL_CASE_DIRECTORY \
  --forecast transfer/forecast.json \
  --out physical-analysis
```

Those directory arguments must contain real recorded output with the exact
configuration and source identities required by the assembly contract. This
command does not generate missing trajectories or relax a failed prerequisite.
The original confirmation did not meet the prerequisite for additional physical
production. This package check does not launch it or supply the missing sample.
The already published commands reproduce the earlier numerical matrix and the
fixed independent confirmation separately.

Packaging correction, 22 September 2026: this check's manifest retained two older
hashes after the confirmation driver's deadline/reference-comparison update.
The manifest now names the current driver and its unchanged packaged manifest.
The scientific analyzers, forecast, fixed-ID design and acceptance criteria are
unchanged. The earlier successful fixture receipt remains historical evidence;
the corrected package passes separately with the same disposable fixtures.
An isolated copy containing only the tracked source files passes the full
assembly and refusal checks in 4.35 CPU seconds using the existing pinned
environment. [Current fixture receipt](reference/physical-analysis-controls-current.json).
This does not repeat a scientific calculation or rebuild the dependency.
