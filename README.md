# Bar–halo response: dynamics and population

A reproducible experiment separating what a prescribed resonance does to orbits
from how much halo material occupies those orbits.

At the same central physical density, bar history and imposed noise, replacing a
selected Gaussian with the reference isochrone halo distribution changes the
response substantially. Moving-resonance suppression survives at model time
T = 20, with about **4.7 times smaller magnitude**. At the predeclared T = 10
check, the two populations have **opposite signs** despite matching central density
and slope. Independent trajectory and distribution/characteristic calculations
support these finite-time measurements.

The measured response kernel also predicts three new populations whose magnitude
forecasts were committed before independent evolution. All declared comparisons
meet their original operational criterion. This is **not uniform 5% accuracy**:
the absolute tolerance matters, and one small response lies close to its boundary.
Separate numerical checks do not provide a rigorous combined-error certificate.

These results concern an externally prescribed local resonance model, constant
additive action diffusion, and one fixed fast-action slice of a halo. They do not
establish a total halo torque, a live halo response, physical SIDM, or agreement
with observed galaxies. Negative contrast means less bar transfer than the smooth
control; it need not mean reversed total torque.

**[Explore the population result and recorded kernels](https://djova.ca/galaxy-bar/population-response)** ·
**[Read the equations, evidence and limits](https://djova.ca/galaxy-bar/population-methods)**

## Matched estimator cost and narrow-population limits

The new [matched-cost package](accuracy/README.md) compares raw and cumulative
estimators on identical numerical weights and paths, measures their CPU cost,
and retains narrow populations where the advantage disappears. It includes all
16 finite cases, paired covariance, timing repeats and a one-command reproduction.
The separate new-sweep approximation diagnostic is still awaiting independent
population outcomes; this cost release does not claim that validation passed.

## Regenerate the measurements

Use Linux with Python 3.11, the tested interpreter and CPU-accounting platform.
Install the exact dependencies once:

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
```

Then choose either complete experiment. These commands run offline after setup;
initial phases and noise are generated from seeds. No private files, credentials,
AGAMA installation or compiled gravity solver are needed for these local tests.

```sh
.venv/bin/python reproduce_population.py --out reproduced-population
.venv/bin/python reproduce_heldout.py --out reproduced-heldout
```

| Command | What it regenerates | Output and approximate CPU cost |
|---|---|---|
| `reproduce_population.py` | All 16 original trajectory batches, four central distribution/characteristic calculations, kernels and intervals | `population-response.png`; about four core-hours |
| `reproduce_heldout.py` | All 24 frozen forecasts and the 23 independent new-population numerical cases | `heldout-predictions.png`; about 2.3 core-hours |

One nice-10 worker is the default. `--workers 2` or `--workers 3` uses that many
single-thread workers; core-hours are summed CPU time, not elapsed time. The two
commands have finite six- and four-core-hour guards respectively, finite case
limits, and an optional earlier `--stop-utc` deadline. They refuse an existing
output directory. A guard-stopped run is incomplete, never a passing reproduction.

The [population guide](population/README.md) explains the released DF table,
absolute normalization, covariance, source manifests and exact verification scope.
`--check-forecasts-only` on the held-out command checks arithmetic without rerunning
forced evolution. Reproducing old seeds verifies the package; it is not a new
independent physical sample. The [complete held-out public-source rerun](population/reproductions/heldout-01/result.json)
passed with all checked differences exactly zero and an inspected regenerated
figure. The [complete original population rerun](population/reproductions/population-01/result.json)
also passed: all 20 cases, 24 analysis comparisons and ten saved kernel arrays
reproduce exactly. Both commands generated their inspected figures successfully.

## What has not transferred to three dimensions?

A new halo-weighted Cartesian design pilot retains all initial-action/phase strata,
both windows, both endpoints and its numerical controls. Its physical-discrepancy
uncertainty is much too large for the intended test. The original cost rule stops
sample enlargement with that estimator. This is an unresolved prediction, not a
physical rejection or a claim that all possible methods require huge computers.
The [complete pilot report](https://djova.ca/galaxy-bar/population-methods#halo-pilot)
preserves every condition, variance diagnostic, forecast and stopping assumption.
The earlier failed Gaussian 3D qualification is also unchanged.

## Earlier benchmarks and the separate software contribution

| Topic | Runnable source and detailed evidence |
|---|---|
| Matched stationary and moving Gaussian controls | [Matched benchmark](EARLIER_BENCHMARKS.md#reproduce-the-matched-stationary-and-moving-comparison), `reproduce_matched.py` |
| Finite-lag diffusion inference and finite elastic-jump limits | [Known-limit controls](FINITE_LAG_CONTROLS.md), `reproduce.py` |
| Earlier Cartesian tests, numerical refinements and preserved failures | [Optional transfer package](transfer/README.md) |
| Bar-free controls and boundary diagnostics | [Unforced records and readback](unforced/README.md) |
| AGAMA turning-phase coordinate repair | [Minimal regression, proposed patch and high-precision evidence](optional-agama/MINIMAL_REGRESSION.md) |

The AGAMA artifact is checked against the recorded current upstream revision and
independent 80-digit coordinates. It does not establish incidence in real galaxies
or maintainer acceptance. Optional AGAMA/GSL components retain their upstream
licenses and require a separate build; neither binary is redistributed here.

## What was already known?

Diffusion sustaining stationary resonant friction, competition with moving-resonance
feedback, and related migration–diffusion effects have clear predecessors. See
[Hamilton, Chiba, Ogilvie–Lubow and the source-grounded positioning](population/research/population-response/SOURCES.md).
Neither opposing noise effects nor linearity in an externally evolved initial
population is claimed as a discovery. The bounded addition is a quantitatively
checked population dependence, reusable response data and prospectively tested
population predictions, with an explicit unsuccessful route to a 3D test.
