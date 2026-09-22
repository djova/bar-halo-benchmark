# Final bounded joint step and cadence qualification

22 September 2026, after fourth-order and rare-path readback. The original3D
and subsequent fourth-order prefix remain numerically unqualified. Do not replace
their recorded conclusions. In the fourth-order check, the point shift passes
but its nominal95%interval exceeds the fixed1.8126730139721574e-7 margin.
The20largest differences account for99.9747%of its sample squared deviations.

Exact replays of selected ID14202 agree with the original .02/.01endpoints,
then show much smaller endpoint changes at .005/.0025. Its early trajectory
differences grow continuously; improved local work accounting alone does not
establish the torque. This does not establish chaos, a Lyapunov exponent, or
population convergence. Every particle remains in the primary estimand.

Run one six-case matrix on the SAME first16384Bparticles, seed8302, same frozen
potential, initial distribution and noise coefficient:

* Candidate fourth-order dt=.01, Brownian refinement4 (cadence approximately.5),
  both noisy and smooth.
* Halfstep dt=.005, same refinement4, both noisy and smooth.
* Halfcadence dt=.01, refinement8 (cadence approximately.25), both noisy and smooth.

The exact base block is end/ceil(end/2). Each deterministic half-block divides
into an integer number of steps no larger than dt. Report actual microsteps;
the refinement8microstep is slightly below.01 because of that integer rounding.
Do not describe the cadence comparison as exactly fixed deterministic steps.
The separate halfstep check bounds that component only where it qualifies.

The new nested Brownian source retains the original two-leaf endpoints and
particle-ID prefixes. Known Gaussian covariance checks pass and its refinement1
pilot reproduces all15original recorded arrays bitwise. Keep Brownian endpoint,
initial-state, forecast/source/library hashes and existing local budget checks.
Paired3D-minus-reduced estimates must be computed at each cadence because the
reduced paths change too. Moving-coordinate advection is never counted as torque.

Require BOTH the point shift and the full nominal95%paired interval for each
3D noisy-minus-smooth numerical difference to lie inside the unchanged margin.
Report residual differences separately, covariance, all raw means and the largest
individual changes. Outlier concentration makes a normal interval only an
approximation; passing a point shift alone is insufficient. Do not clip, trim,
replace particles selectively or relax the margin. No physical adequacy claim
from the16384prefix, even if numerical checks pass.

This is the final such numerical matrix for this campaign: no automatic ladder
after another failure. If it fails, report the numerical precision limit and
its location, without claiming a failure of the physical reduction. If it passes,
make a separate recorded resource/power decision before any full-population test.
The original particle extension remains held and is not implicitly restarted.

Ceiling3.5corehours, one nice10 single-core worker while the two clean3D workers
and one matched-reproduction worker run. Six finite cases, each7200s wall limit.
Expected runtime from pilots is roughly2.7corehours; inspect measured usage.
Reallocate1unused corehour from coefficients/solver to diagnosis: controls2,
coefficients7,map8,transfer10,diagnosis5; total32unchanged. All earlier diagnostic
attempts and restart loss bounds count against diagnosis5. Deadline unchanged.
