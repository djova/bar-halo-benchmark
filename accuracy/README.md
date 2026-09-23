# Population-approximation accuracy and estimator cost

This release regenerates a frozen population-approximation test at one new
sweep rate, together with the independent numerical experiment used to assess
it. The system is a prescribed local resonance with additive action noise and
reference-halo weighting in one fixed fast-action slice. It is not a live halo,
physical SIDM model, or validated three-dimensional bar prediction.

The [research note](research/population-accuracy/RESEARCH_NOTE.md) explains the
population counterexample, the useful exponential approximation, the gradient
diagnostic and the estimator. The [frozen protocol](research/population-accuracy/PLAN.md)
specifies the prospective comparisons and error rules. Read the reference
outcome in `test/reference-analysis.json`, including inconclusive or rejected
qualifications. Reproduction is not another independent physical sample.

## Reproduce the complete prospective investigation

From the repository root, create an isolated Python 3.11 environment:

```sh
python3.11 -m venv /tmp/bar-accuracy-venv
/tmp/bar-accuracy-venv/bin/pip install -r accuracy/requirements.lock.txt
/tmp/bar-accuracy-venv/bin/python reproduce_accuracy.py \
  --out /tmp/bar-accuracy-reproduction --workers 2
```

Use a fresh output directory. The command runs analytical and assembly controls,
all eight stochastic kernel batches, and all fourteen independent positive-
population calculations. It checks the regenerated kernel arrays and all frozen
forecasts before proceeding to the independent comparison, then checks every
reference outcome and creates the central accuracy figure. The kernels and
independent populations evolve separately; the forecast is not fitted to them.

The default wall deadline is 24 hours from invocation; `--stop-utc` accepts an
earlier ISO-8601 deadline. Each case also has a finite wall limit. The two stages
have aggregate CPU ceilings of four and six core-hours. A stopped or failed
case prevents a complete scientific assessment; it is not replaced by a zero.
Workers run at nice 10 with one numerical thread each. Select one to three
workers to fit the host's available resources. There is no background timer.

Outputs include `forecast-comparison.json`, the full per-case records,
`analysis/result.json`, `figures/population-accuracy.png`, and `result.json`.
The numerical comparison uses relative tolerance 1e-9 and absolute tolerance
1e-11 to allow harmless platform rounding. CPU timings and source-location
hashes are deliberately not numerical equality targets. The recipe preserves
the original experiment's seeds and outcomes, including failures or unresolved
comparisons; it does not perform a fresh prospective validation.

The gradient inequality is exact for the stated boundary treatment. Its
implemented allowance uses estimated kernels, approximate Student-t coverage
and practical numerical-refinement proxies. Neither a reproduced calculation
nor an operational qualification turns those proxies into rigorous bounds.

## Reproduce the matched estimator-cost experiment

```sh
python reproduce_accuracy_cost.py --out /tmp/accuracy-cost-reproduction --workers 1
```

This regenerates all 16 finite stochastic cases, their paired means/covariances,
the cost analysis and its figure. A second population-comparison figure uses the
released historical reference; it does not rerun the earlier population campaign.
The original cost experiment used about 347 worker CPU-seconds. CPU timings
are measured again; changing hardware performance is not a new physical sample.

Raw and cumulative-remainder estimates use identical piecewise-linear weights,
shared paths and auxiliary support. Neither renormalizes the populations to
unit mass. The full-T20 workload, paired timestep calculation, integration,
setup and method-specific evaluation are charged to both reported endpoints.
I/O and common covariance assembly are excluded from both method costs.

The ratio of cost times variance estimates repeated-batch precision efficiency
under a fixed allocation. It is not a directly timed speedup to a final target
error. Eight-batch uncertainty, the noisier between-batch estimate and the one
pointwise raw/remainder consistency flag remain in the release. Narrow stress
weights show where the advantage disappears; they are not representative halo
DFs. See the [cost outcome](research/population-accuracy/COST_OUTCOME_02.md) and
[restricted estimator identity](research/population-response/CUMULATIVE_IDENTITY.md).

## Recompute the retrospective paired assessment

```sh
python reproduce_accuracy_audit.py --out /tmp/accuracy-retrospective-audit
```

This short command reproduces the joint numerical-proxy assessment of earlier
forecasts, the paired exponential-minus-halo uncertainty and the archived
raw/remainder covariance comparison. It uses exact historical mean/covariance
projections with original archive hashes and an extraction receipt. It does not
rerun trajectories. The separate population and held-out reproduction commands
regenerate those underlying experiments.

All 24 historical operational passes remain unchanged. The retrospective joint
assessment retains 22, with both early width-12 window comparisons marginal.
The original absolute allowance floor must not be described as uniform 5%
accuracy. Likewise, close exponential–halo point estimates do not alone certify
sub-0.1% accuracy.

## Portability and provenance

Scientific sources and numerical inputs are copied unchanged. The portable
queue launcher substitutes the current Python interpreter for the private
virtual-environment location; its separately recorded delta is logistical.
The source manifest checks release files before running. No private archive,
API, host service, AGAMA installation or supercomputer is required.

Original experiments and corrections remain in the project provenance. This
package does not overwrite the initial cost-weight mismatch, prior marginal
forecast, or unvalidated Cartesian result. External-review questions are
provided without implying that outside review or endorsement has occurred.
