# Population-weighted resonance response

This experiment separates the response of an imposed resonance from the amount
of halo material that occupies each action. It compares a selected Gaussian,
the reference isochrone halo DF, and a local exponential with the same central
density and slope. The bar, prescribed noise, sweep histories and durations are
unchanged between populations. No selected window is renormalized to unit mass.

## Regenerate the measurements and central figure

From the repository root, using the pinned Python 3.11 environment:

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python reproduce_population.py --out reproduced-population
```

The final command runs offline. It generates all initial phases and noise from
fixed seeds, runs the complete sixteen-case independent trajectory sample and
four independent central distribution/characteristic calculations, rebuilds the
response kernels and intervals, checks them against released values, and writes
`population-response.png`. It refuses an existing output directory.

Allow approximately four core-hours, estimated from the original calculations.
One nice-10 worker is the default; `--workers 2` or `--workers 3` runs finite cases
in parallel, with one numerical thread per worker. The aggregate scientific
ceiling is six core-hours and every case has a finite wall limit. A run stopped
by those limits remains incomplete. A later timestamp does not bypass a scientific
check. `--stop-utc YYYY-MM-DDTHH:MM:SSZ` can supply an earlier external deadline.

This command reproduces the original seeds. It is not a new statistical sample.
It reruns the paired trajectory step/window checks, but it does not rerun every
archived distribution refinement, the prospective new-population tests, or any
three-dimensional orbit test. Their separate qualifications remain visible in
the source records. A reproduced failure stays a failure.

## Inputs that do not require a private repository

`inputs/halo-table/` contains the complete tabulated unforced DF and its metadata,
including the canonical measure, source revision and checksum. The model is an
isochrone halo with G = M = 1 and scale radius 0.5, conditioned on fast actions
Jr = 0.08, Jz = 0.05, near Js = 0.25. The original table was evaluated with the
stated AGAMA distribution function; the default reproduction needs only the
included table, NumPy and Matplotlib, not an AGAMA installation.

The table covers all physical weights. The exact positive piecewise-linear
approximation and its primitive are regenerated, never fetched from private
simulation arrays. `inputs/allocation.json` fixes the action strata and counts.
There are eight independent batches per sweep, each with 1,572,864 initial points.
The Brownian partners, step pairs and population weights within each batch are
correlated measurements, not extra independent replicas.

The numerical solver source under `scripts/` and `benchmark/` is copied unchanged
from the experiment. The launcher alone uses the active Python interpreter instead
of a private repository environment path; `launcher-portability.json` records that
small adaptation and both hashes. `source-manifest.json` verifies its bytes and the exact inputs.
`reproduction.json` lists the finite cases. The relative execution paths and
current run deadline differ from the original host; the physical configuration,
seeds, allocation, integrators and measurement definitions do not.

## What the numbers mean

The displayed contrast is integral(w K_B) dx, where K_B is the mean change in
accumulated **bar** impulse caused by the imposed noise at each starting action.
Positive means more angular momentum transferred from the bar to this population;
negative means less. Moving-coordinate advection and stochastic kicks are
accounted for separately from bar torque.

For m = 2 corotation and the specified canonical measure, the physical transfer
per unit fast-action area is 4u²(2π)³Fref times the displayed integral. A single
fixed-action slice is a differential contribution, not a finite total-halo torque.
The imposed diffusion is not a physical SIDM collision operator, and the halo
and bar do not react collectively to these tracer paths.

The primitive kernel gives the same integrated response through −integral(w′Q).
Its contributions are gradient-coordinate terms, not literal cohorts of initial
orbits. Both the ordinary conditional kernel and the primitive are recorded.
The zero-integral cumulative control reduces cancellation under this particular
external Hamiltonian and additive-noise operator. It does not generally carry
over to a fixed-fast-action slice in full Cartesian dynamics.

## Inspect figures without rerunning the physics

```sh
.venv/bin/python population/plot_population.py \
  --analysis population/reference/validation-analysis.json \
  --distribution population/reference/result.json \
  --out archived-population-response.png
```

This reconstructs a figure from released records. It is explicitly not an
underlying-experiment reproduction. The full `reproduce_population.py` command
above performs that work. The reference kernel archive retains all independent
batches so new population contractions preserve covariance.

## Scope, preceding theory and prospective tests

The mechanisms of diffusion-sustained stationary friction and weakened moving
resonance feedback have predecessors. See the linked primary sources and frozen
protocols in `research/population-response/`. No novelty is claimed for linearity
in a prescribed external population or for a response/adjoint construction.

The useful target is a quantitatively checked population dependence and a reusable
way to predict the error of a local population approximation. New Gaussian widths
12 and 20 and a quartic profile are declared separately. Their predicted magnitudes
must be committed before independent forced evolution starts. A kernel prediction
within this same reduced model is distinct from a new three-dimensional physical
prediction or an observed-galaxy comparison.

## Reproduce the prospective new-population test

The complete original test meets its frozen magnitude criterion for all three new
shapes, both sweeps, both durations and both windows. This is not uniform 5%
accuracy: the allowance is the larger of 0.0002 and 5% of the forecast magnitude.
The small moving width-12 response at T10 only narrowly fits that allowance; its
remaining interval margin is smaller than a measured quadrature change. Separate
numerical checks are operational diagnostics, not rigorous combined error bounds.

```sh
.venv/bin/python reproduce_heldout.py --out reproduced-heldout
```

This first reconstructs all 24 forecasts from the recorded independent kernel
batches, then reruns all 23 distribution/characteristic cases, checks all means
and decisions, and writes `heldout-predictions.png`. No sample or failed outcome
is omitted. Allow roughly 2.3 core-hours, measured in the original matrix, with
a four-core-hour cap and finite per-case/48-hour wall limits. One nice-10 worker
is the default. Add `--check-forecasts-only` to regenerate just the arithmetic,
without claiming to rerun the forced experiment.

The original forecasts were committed before new-shape evolution. Running this
command later reproduces that historical prospective test; it does not create a
new prospective physical experiment. The correlated 24 comparisons share kernel
batches and are not independent confirmations of a physical theory. See
[the outcome](research/population-response/HELDOUT_OUTCOME_01.md) and
[every comparison](heldout/reference.json). The original failed Cartesian
qualification remains unchanged.

For a scheduled local reproduction, `--stop-utc YYYY-MM-DDTHH:MM:SSZ` sets an
earlier production deadline without overriding the finite CPU and wall limits.
The complete clean public-source rerun finished successfully at pinned commit
`2528a4d85f71aa6f330184bf063b3d74b2e57d1a`. All 24 forecasts, all 23 cases, and
every checked measurement, numerical change and decision reproduce exactly. The
run used 2.35 scientific core-hours with two single-thread workers. Its regenerated
figure was inspected and is pixel-identical to the original. See the
[complete receipt](reproductions/heldout-01/result.json) and
[regenerated figure](reproductions/heldout-01/heldout-predictions.png).

An earlier preparation receipt had an incorrect lockfile hash. The final receipt
retains that correction: both pinned Git versions contain the same actual lock
bytes, and all eleven dependency pins match the measured environment. Numerical
source, installed versions and outcomes are unchanged. The original population
command remains in progress; this success does not stand in for its completion.
