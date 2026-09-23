# Matched estimator variance and measured computation cost

This is a methods benchmark at the **existing** s=0 and0.25, eta0.1 conditions,
not a second prospective dynamical test. Keep the observable, initial sampling,
Brownian paths, antithetic pairing, fine/coarse integration and physical weights
identical between raw and remainder estimators. No estimator-dependent trimming.

At each sweep use eight fresh seeds96211–96218,176unit-width strata on[-88,88],
512initial samples per stratum, coarse dt0.025/fine dt0.0125, T10/T20. The primary
cost/variance measurements use the fine, antithetic contrast. Save coarse values
as numerical context, not a new physical qualification. All population weights
have the same central density and slope and window24/40. Compare the halo,
exponential, and Gaussians with widths8,1,1/8,1/64. The narrow profiles deliberately
stress the control variate; they are estimator tests, not representative halo DFs.

Measure actual process CPU separately for the shared numerical integration,
raw weight construction/evaluation, and positive cumulative-density construction/
remainder evaluation. Include each method's setup cost. Time each postprocessing
path three times in alternating order and retain all measurements; use the median
to reduce timing noise. Integration is measured once per batch and shared in the
cost accounting, because both methods use exactly those same trajectories. State
this explicitly: the benchmark does not rerun the same dynamics twice to pretend
the workloads are physically independent. Both timed workflows include the same
fine/coarse numerical-control integration. Exclude common audit covariance and
file-writing costs from both, and report total job CPU separately.

Use within-stratum covariance and eight independent batch estimates. Show raw
minus remainder with its paired interval, and the cost-times-variance ratio with
a paired bootstrap over all eight batches. A projected CPU requirement for a
specified standard error is measured batch CPU times(batch variance/targetSE^2),
assuming independent repeated batches and fixed allocation. It is not a directly
timed execution at that final precision, a wall-clock promise, or a rare-event
variance bound. Report separately the between-batch and conditional estimates.

There are16finite jobs on **one** nice10 single-thread worker, ceiling one core-hour,
per-case limit240seconds. Together with the two kernel workers this respects the
campaign maximum of three. Expected integration cost is~39seconds per batch from
the earlier pilot. Preserve all stress cases, including no-gain or worse results.
