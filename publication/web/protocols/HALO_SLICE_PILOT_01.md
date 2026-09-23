# Halo-weighted Cartesian pilot 01 — prospective design

This is a new design pilot, not a rerun of the failed Gaussian qualification.
It is frozen before any new halo-weighted Cartesian trajectory. The informative
primary endpoint is T10: the qualified local model predicts opposite population
signs there. T20 remains a mandatory second endpoint in every pilot path. We do
not select an endpoint after inspecting the pilot. No physical parameters are
refitted; use the original case-B isochrone, quadrupole, canonical action noise,
Jr=0.08, Jz=0.05, Js0=0.25, s=0.25 and eta=0.1.

## Magnitude forecast and physical measure

Freeze all four moving halo forecasts (two times, two windows) from the complete
original eight-batch validation before starting the pilot. Preserve their pointwise
95% intervals, the independent deterministic estimates and the original operational
local numerical/window allowance 2e-4. The predicted quantity is integral(w K_B),
with the absolute physical DF and no per-window mass normalization. Conversion to
angular-momentum transfer per fast-action area is4u^2(2pi)^3F_ref, as in PLAN.md.
The existing Gaussian forecast, failed qualification and sample remain unchanged.

The Cartesian response estimate is sum_h (dx_h/8) mean_h[w(x)*(B_D-B_0)/(2u)].
Here Cartesian B is actual accumulated Lz bar torque, and the mean averages within
one initial-action/resonant-phase cell, both fast angles and both m=2 sectors.
The reduced paired discrepancy replaces B_D-B_0 by its Cartesian-minus-reduced
value along the same initial conditions and Brownian paths. It is a control
variate for the physical model discrepancy, not a fit to the forced outcome.
Do not apply the local cumulative-remainder identity to the Cartesian fixed-fast-
action slice: its full flow need not preserve the conditional two-dimensional measure.

## Complete fixed proposal

Use action edges [-64,-24,-16,-8,-4,-2,-1,0,1,2,3,4,6,8,12,16,24,64] and eight equal
resonant-phase intervals spanning [-pi,pi]. Every one of 136 cells gets 16 independent
points for each of two new seeds 95601 and 95602: 2176 points per seed,4352 total.
Sample uniformly inside each cell and independently in the two fast angles;
sample each m=2sector with probability 1/2. Store all arrays, labels and actual DF
weights. Both 24/40 and 48/64 smooth windows use these same points. A zero narrow-window
weight does not remove the path or its wide-window contribution. No trimming.

The proposal stream is PCG64 SeedSequence[seed,101], distinct from the original
Gaussian stream. Brownian leaves and nested bridges retain the verified existing
scheme. All settings of a seed use identical initial points and shared leaves.
The finite physical duration is 20 time_units, split into two equal halves so the
saved T10 and T20 endpoints are exact. Base blocks are at most 2 physical time units.

## Limited numerical matrix

For each seed run noisy and smooth counterparts at candidate(dt.01,noise refine 4),
halfstep(.005,4) and halfcadence(.01,8), plus one unforced noisy candidate. Fourteen
finite cases, initially at most two scientific workers once slots are free; the
sum with the clean reproduction must not exceed three. Aggregate cap 7200 CPU seconds,
per-case wall cap 1200 seconds, original production UTC stop. No automatic extension.
The same patched AGAMA coordinate library and native fourth-order Cartesian solver
are pinned by hash. A small unforced initial-sampling/control calculation must pass
before the forecast/matrix is committed; it does not include any forced trajectory.
The unforced controls also check action/angle round trips for the proposal and
20 independent 80-digit coordinate probes across the full initial action range
at radial turning phases. These are bounded probes, not a universal mapper bound.

Track torque, stochastic Lz, stochastic energy, deterministic work and reduced
coordinate motion separately. Retain existing local limits: torque and reduced
budget<1e-9; coordinate roundtrip, kick Lz, kick fast-action and kick-angle errors
<1e-10. The unforced control additionally requires zero bar torque<1e-12,
fast-action changes <5e-6 and noise variance within its declared five-standard-error
screen. Report work residuals explicitly; do not relabel an untested energy bound
as passed. Any failed local gate blocks a qualified physical interpretation.
Actual action extrema are sampled for all paths at each base-block end, and before/
after every nonzero kick. They are sampled extrema, not certified continuous bounds.

## Pilot analysis and conditional decision

Only analyze the full terminal matrix. Verify all initial arrays/weights and shared
Brownian endpoint identities before differencing. Within each cell estimate weighted
variances separately for Cartesian-minus-reduced physical discrepancy, raw Cartesian
contrast, paired and raw timestep/cadence changes, and wide-minus-narrow selection.
Retain both pilot seeds separately and their complete pooled strata. Report the
largest 20 variance contributions; do not discard them. Report actual slow/fast-action
excursions and fraction leaving the original unforced coefficient scan. This pilot
cannot by itself certify a 3D forecast or an absence of rare tails.

The possible validation target remains operational 20% model adequacy, now applied
to these newly frozen halo magnitudes. The sampling design aims at a95%half-width
<=10% of each forecast magnitude for the physical discrepancy, and <=2% for numerical
step/cadence differences. The local forecast interval and 2e-4 numerical scale remain
separate, and would enlarge a final model comparison. A nonzero numerical pilot
mean must also be included in any qualification projection; low variance alone
cannot establish adequacy. Both windows/times remain required diagnostics.

For cost screening, calculate even the optimistic stratified Neyman lower variance
(sum_h measure_h*sigma_h)^2/N, then a cautious projection using four times the
maximum of the pooled and either-seed cell variance, a nonzero minimum allocation,
and a simultaneous max-over-target allocation. This factor is a declared planning
margin, not a confidence bound against rare unseen paths. Require at least 128 points
per cell in a potential independent validation. Exclude all pilot seeds from that
validation. Source, exact allocation, new seeds and acceptance rules must be frozen
in a SEPARATE protocol before validation. Pilot means must never supply a fitted
physical correction to the prospective magnitude prediction.

If even the optimistic cost cannot fit the remaining campaign ceiling, or the
cautious full design cannot fit with its numerical and coordinate checks, stop the
conditional stage with the measured limitation. Do not increase amplitude/noise,
shorten the endpoint, narrow the population, relax a threshold or remove a stratum
to obtain significance. A scientifically useful outcome can be a quantified cost/
domain obstruction alongside the independent local population result.
