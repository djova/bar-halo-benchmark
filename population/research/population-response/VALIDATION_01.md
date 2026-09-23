# Fixed independent validation of population-weighted transfer

Frozen before any of seeds94501–94508 are generated. Both completed sampling
pilots are design data and are excluded from validation averages and intervals.
The original failed collisionless Fourier and positive-quadrature refinements
remain failed; a new estimator does not retrospectively pass them.

## Physical experiment and measured contrast

Keep the local case-B coefficients, eta0.1, s in{0,0.25}, central density,
three positive physical profiles, both windows24/40 and48/64, and T10/T20 fixed.
The primary estimator is the antithetic cumulative remainder at fine dt0.00625.
It estimates the same integral(w K_B), without normalizing by population mass.
Coarse dt0.0125 uses the same Brownian leaves; both noisy and collisionless
paths are paired. Raw and single-branch estimates remain inspectable controls.
The phase-space conversion stays4*u^2*(2pi)^3*Fref per unit fast-action area.

The cumulative density uses the positive piecewise-linear approximation at
spacing1/8192 and its exact primitive. The fixed interpolation tests and both
pilots compare it against1/4096. This numerical approximation and its measured
differences must be reported; do not call it an exact evaluation of the halo DF.

## Fixed sample and cost

At each sweep run eight batches, seeds94501 through94508. Each batch has
1,572,864independent initial points, for12,582,912per sweep. Each point has a
correlated positive/negative Brownian partner; partners are not extra independent
replicas. Both sweeps use the same frozen action allocation and seeds, so their
estimates are correlated and require pairing for a between-sweep contrast.

The allocation is exactly three times the integer candidate allocation from
cumulative-pilot-analysis-02. It keeps every one of176unit-width strata across
[-88,88], with at least768points per stratum. The candidate uses the maximum of
two pilot variances in each stratum, considers both physical means and paired
timestep differences, and projects a fourfold variance allowance. With the
larger sample the largest projected timestep half-width is approximately
0.000164. This is a design projection, not a variance bound or a claim that the
unknown timestep bias is zero.

The denser pilot costs about39CPU seconds for90,112initial points at this
timestep. Linear extrapolation gives about3.0core-hours for the sixteen cases
before the added kernel recording; it is a cost estimate, not a runtime promise.
Use a6core-hour batch ceiling and1800seconds per case. Two nice10 single-thread
workers leave the third scientific slot available for independent deterministic
checks. No other new scientific worker may take that slot concurrently.

## Analysis fixed before outcomes

- Use the mean of the eight independent batch estimates at each sweep.
  Report a two-sided95% Student-t interval from between-batch variation
  (seven degrees of freedom). Within-stratum covariance is a diagnostic;
  it does not replace between-batch variation or conceal a rare batch.
- For each profile and both durations, form fine-minus-coarse differences
  within every batch. Its complete95% interval must lie inside[-2e-4,2e-4]
  to pass the numerical precision criterion. A mean inside the allowance
  alone is not a pass. A failure with an interval including zero does not
  establish a nonzero bias or physical nonconvergence.
- Form wider-minus-narrower-window differences within each batch, with
  their original absolute weights. Apply the same interval criterion for
  a window-insensitive claim. A failed window test remains population-
  selection dependence, not a total-halo prediction.
- Check the raw/remainder paired difference, retained source/null tests,
  path budget and force-bound diagnostics. Do not count two correlated
  estimators as independent physical confirmations.
- Primary scientific endpoints are the halo and Gaussian contrasts at T20;
  T10 is the declared duration check, and the exponential is the declared
  local-slope comparison. A physical sign is resolved only when its sampling
  interval excludes zero and its numerical/window qualifications permit
  that interpretation. Report all prescribed profiles and times together.

No optional significance stopping, outlier trimming, sample extension or altered
allowance is authorized by this protocol. If resource guards interrupt cases,
retain them and do not silently replace an eight-batch analysis by the available
subset. A subsequent experiment would need its own explicit scientific reason
and independent registration.

## Reusable recorded kernel

Save both the raw conditional impulse means in the initial-action strata and a
primitive built from the measured bar displacements. The cumulative identity
gives R_w = integral w'(z) q(x,B,z) dz. The expected derivative of the difference
of noisy/smooth primitive kernels corresponds to K_B; a finite sample derivative
has uncertainty and must not be shown as an exact smooth response curve.

Each sampled triangle jumps at its starting action. The first point-sampled
contraction misses a1e-5 Gaussian tolerance and remains archived with exact
source copies. Exact cell averages of the same triangles resolve that quadrature
issue: pilot contractions agree with direct remainders to1.1e-8 and coarsening
changes are below3.7e-8. Preserve that distinction; no physical parameter changed.

Record both point values and exact cell averages on[-64,64] at spacing1/256.
The auxiliary starting domain covers all points capable of contributing there.
In every validation batch require all recorded-profile contractions and their
factor-two coarsening changes below1e-5. These are algebraic assembly checks,
not independent physical evidence. Keep covariance across populations and kernels
through the independent batches. Gradient-weighted contributions and literal
initial-orbit cohorts are different decompositions and must be labelled.

Independent deterministic confirmation, held-out population predictions,
coefficient-domain assessment and any new3Dtest remain separate tasks. This
sample alone does not validate a live halo, physical SIDM or observed galaxies.
