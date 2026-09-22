# Full 3D prediction test: finite execution matrix

22 September 2026, before either held-out 3D outcome. Forecasts and both
qualifications must be frozen and committed before launching this matrix.
Use the unchanged FORECAST_PROTOCOL.md estimand, physics and decision band.

For A/seed8301 and B/seed8302 run65536 particles in four configurations:
bar/noise, bar/no-noise, unforced/noise, unforced/no-noise. Initial particle IDs
and Brownian leaves agree across counterparts. Independent numerical refinements
use the first16384IDs: half Cartesian timestep, and half noise cadence, each
with both bar/noise and bar/no-noise. Compare the actual paired contrast on
that same baseline prefix. Preserve raw3D and paired-reduced arrays, means,
covariance, budgets and individual residuals. Do not use moving-coordinate
advection or the random-kick angular momentum as bar torque.

All baseline settings remain dtmax.01/noisecadence<=2; independent changes are
.005 and cadence<=1. Use only the qualified separate AGAMA-stable-v2 library.
Archive its hash and the native force-kernel hash in each result. The original
library, failed coordinate probes, old simulations and reduced failures remain.

Report95% iid intervals for both the physical paired discrepancy and the
numerical shift estimated on matched particles. Numerical sampling uncertainty
must remain visible; a small shift sample mean alone is not an upper bound.
The stated forecast band and its numerical criterion remain unchanged.

Runtime projection from the t12720,4096-particle non-held-out pilot is roughly
0.52corehours for65536particles atdt.01 and0.23corehours for16384atdt.005.
Eight base cases plus eight refinements should fit the existing8core-hour
transfer allocation. This is a conservative projection, not a guaranteed runtime.
The raw reduced noisy-minus-smooth SD is1.408action units; its projected
65536-particle ordinary95% half-width is0.01078, larger than the approximately
0.008forecast. That is why the unfitted paired3D-minus-reduced discrepancy is
the primary precision test. No3D residual variance has yet been observed.
The predeclared524288extension uses precision, not sign, and requires a recorded
resource check before launch. All cases get finite7200s wall limits, at most
four nice10 single-core workers total. Deadline and production cutoff unchanged.

## Prerequisite decision before any held-out3D outcome

Both final quadratures meet the unchanged numerical criterion. A's independent
stochastic95% interval is[-0.00810238,+0.00503309], narrowly excluding its
-0.00821363distribution contrast. Its qualification is therefore FAILED despite
passing local/numerical checks. This is not evidence of failed3Dphysics, and may
be a sampling fluctuation; do not alter the criterion or hide the original sample.
B's independent interval contains its contrast and all its prerequisites PASS.
Freeze both forecasts with their actual qualifications in forecast-freeze-01.
Run only the eight Bcases from the specified matrix initially. Seed8301 remains
unused; choosing B follows the declared prerequisite, not a3Doutcome. The runner
must require the selected case's qualification, not demand all unrelated cases
pass. This decision reduces the initial resource projection, unchanged ceilings.
