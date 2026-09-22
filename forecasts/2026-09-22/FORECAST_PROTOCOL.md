# Frozen reduced forecasts and paired 3D discrepancy test

22 September 2026. No forced outcome at either reserved 3D condition has been run.
Use cases A/B and unforced coefficients from transfer-preflight-01. Their common
new sweep is s=.25, eta=.1, T=20, positive Gaussian sigma8. Retain each measured
slope/action/time scale and exact pattern-frequency history. Coefficients are
measured from the unforced potential and imposed bar, never from 3D torques.

## Reduced forecast

For each condition compute noisy DF at128x2048 and256x4096 on+/-64, dtmax=.025,
plus a fine-grid half-step and unforced noisy counterpart. Use positive
collisionless characteristic quadratures512x8192 and1024x16384, same domain and
dt. Compare their mean bar impulses. Do not use failed negative Fourier D0
populations. Independent stochastic batches8209..8216 (32768paths each, paired
eta=.1 and0) estimate the response distribution and prospective sampling scale.
These are new-condition reduced outcomes; they are not 3D outcomes.

Forecast C is noisy minus collisionless mean bar impulse, converted to physical
Lz by2u. Freeze its numerical refinements, independent path intervals and an
adequacy band of +/-20% of the predicted magnitude before any3D outcome. This
20% is an operational approximation target, not a probabilistic model-error bar.
It is intentionally distinct from the earlier map's5e-5 quadrature gate, whose
failures remain failures. A qualified forecast requires all local mass/positivity/
budget gates, noisy unforced checks, the selected refinements smaller than10% of
this adequacy half-width, and consistent independent stochastic estimates.
Otherwise report a forecast with an unresolved numerical qualification; do not
quietly widen its band. The numerical shifts are not rigorous error bounds.

## Paired discrepancy, with no fitted control-variate coefficient

The full3D experiment evolves the actual Cartesian bar potential without fast-angle
averaging. Alongside it integrate the constant-coefficient reduced equations from
the same sampled Js, psi=2theta_phi and the same Brownian increments. Preserve
bar impulse separately from stochastic action changes in both. The complete3D
noise map keeps instantaneous fast actions and angles fixed, not initial ones.

Let X be one particle's3D noisy-minus-collisionless bar-Lz contrast and Y the
corresponding reduced contrast. The primary transfer discrepancy is mean(X-Y).
This directly estimates E[X]-E[Y]. Test it against the frozen20% adequacy band,
including its95% iid paired sampling interval and measured numerical shifts.
No coefficient multiplying Y is estimated from the3D sample: it is fixed to1.
Report the ordinary mean(X), mean(Y), their covariance and standard errors too.
The variance-reduced estimate C_forecast+mean(X-Y) is labelled as such, never
presented as the raw3D mean. A small residual is meaningful only after the
independent forecast and reduced-step/budget checks pass.

This pairing does not make agreement automatic. If the reduction is biased, its
nonzero paired mean remains. It reduces shared phase/noise sampling scatter. It
also distinguishes this test from the old same-action phase replication: both
new conditions and independently determined physical coefficients are fixed
before3D response measurement.

## 3D settings and decision

Start65536particles per condition: seed8301 for A,8302 for B. The zero-noise,
noisy and unforced counterparts share initial conditions; each particle has its
own independent noise stream. Portable Cartesian KDK dtmax=.01; noise cadence
at most2 physical time units, centered in deterministic blocks. Refinements use
dtmax=.005 and half noise cadence independently, on the first16384particles of
each condition, with a matched32768-normal leaf stream and identical endpoint
Brownian increments. Define per-particle streams below before production; do not
accidentally change initial samples or noise paths when N changes.

The one predeclared sample extension increases each condition from65536 to524288
if the95% paired-discrepancy half-width exceeds10% of |C_forecast|. Its trigger
uses precision, not the sign of the discrepancy, and retains the first sample.
Record power/runtime before launch; do not exceed the campaign allocation.
For adequacy, the entire paired95% interval enlarged by measured independent
numerical shifts must lie inside the frozen20% band. Outside it with adequate
precision is failure; partial overlap is unresolved. Numerical shifts must be
less than10% of the adequacy half-width. These checks concern the interpreted
contrast, not the initial action RMS. No extrapolation to physical SIDM or
collectively reacting haloes.

If a constant-coefficient forecast fails, inspect the already measured local
coefficient variation, fast-action evolution and off-resonant harmonic spectrum.
A separately frozen varying-coefficient resonant Hamiltonian, calibrated only to
those unforced tables, is the bounded discriminating test; it must not be fitted
to the failing3D result. Do not claim a specific cause from failure alone.

## Resource cap

Reduced forecast preparation:2scientific core-hours, case wall limits2400s.
3D production/refinements initially within the original8core-hour allocation;
any needed reallocation is recorded before an extension. At most4scientific
workers total, nice10 and one core. All raw paths/budgets remain archived.

## Recorded visual evidence and aliasing

The201whole-run snapshots resolve slow resonant evolution, but their Cartesian
positions do not resolve fast orbital periods. Do not animate connected fast
orbits from those sparse frames. Before production, additionally record the
first64fixed IDs at approximately0.2physical time spacing in three40-unit
windows: start, middle and end. Save actual native integrator states, splitting
calls into shorter segments at the same native timestep; do not interpolate.
Mark states immediately before/after canonical kicks at the same timestamp so
the imposed phase-space jumps are visible. The existing whole-run clock remains
appropriate for slow angles/actions and accumulated torque. A short non-held-out
pilot must verify that added sampling changes the endpoint by less than1e-10
and retains the unchanged scientific gates.
