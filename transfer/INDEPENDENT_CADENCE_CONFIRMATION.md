# Independent cadence confirmation: explicit amendment

22 September 2026, before any new forced outcome in the specified sample.
This is an amendment to the stopping decision in FINAL_NUMERICAL_OUTCOME.md,
not a claim that the original protocol anticipated another numerical test.
The original 16,384-particle matrix remains failed. Its means fit the unchanged
allowance, while cadence intervals do not; the discrepancy shift is 0.82 standard
errors from zero and its variance is concentrated in a few paths. That identifies
a sampling limitation, but does not prove the true cadence bias is negligible.

The user's active goal requires attempting a predictive physical transfer test
where prerequisites permit. With the deadline unchanged and resources available
under the master plan's 48 core-hour ceiling, make one fixed independent
confirmation at exactly the existing candidate and half-cadence settings. No
further integration refinement, changed noise law, physical coefficient, forecast,
or relaxed acceptance threshold is introduced. Do not repeat this confirmation
or enlarge its sample after its outcome. Publish it alongside the original failure.

## Fixed sample and comparisons

Use seed 8302, unused stable particle IDs 65,536 through 196,607 inclusive:
131,072 particles. Initial actions, phases and Brownian streams are determined by
those IDs using the unchanged source. They are disjoint from the entire original
65,536-particle physical sample and all prior numerical prefixes. Four contiguous
32,768-ID chunks run with and without noise at each of:

- Candidate: fourth-order dtmax .01, Brownian refinement 4.
- Half cadence: fourth-order dtmax .01, refinement 8.

Also run the first 16,384 IDs of this NEW sample at dtmax .005/refinement 4,
with and without noise. Match them to the same IDs in the first candidate chunk.
Run 4,096 of the new IDs with no bar, both with and without noise, at the candidate
settings for the full prescribed duration. All 20 cases have finite endpoints
and 7,200-second wall limits. At most three nice=10 single-core workers run this
matrix, leaving a slot for the already active clean reproduction.

The complete sample is analyzed once all cases terminate. Do not inspect or use
partial torque means to change its size, settings, order or stopping. Runtime,
completion and safety/budget state can be monitored. No old sample is pooled into
the new numerical confidence intervals. Preserve every path, including large
changes. Check exact IDs, initial states, source/library/forecast hashes, finite
arrays, local and unforced budgets, and shared Brownian endpoints.

Compute raw X = 3D noisy minus smooth bar impulse and paired discrepancy X-Y,
where Y is the corresponding reduced contrast. For both cadence and step, require
the absolute mean shift AND its whole nominal pointwise 95% Student-t interval
inside the unchanged numerical allowance 1.8126730139721574e-7 physical Lz units.
All checks must pass; no point-only replacement. Report per-chunk means and tail
concentration without dropping chunks or changing the primary iid estimator.
These sampling intervals are not rigorous bounds on the discretization limit.
The actual microsteps differ slightly in the cadence test through integer block
subdivision; retain the original explanation and the independent step check.

## Power, resources and next decision

Eight times the prior numerical sample predicts a discrepancy-shift half-width
near 1.009e-7 if its variance repeats. Under the illustrative assumption of zero
true bias and normal errors, this gives about 88% probability that the whole
interval fits the margin. Neither zero bias nor that power is established.
The observed old mean is not used as a target or removed from the new result.

Measured original CPU predicts 11.606 core-hours for the cadence matrix,
1.111 for the new step pair, and about .166 for unforced controls. A separate
40-block random-stream timing (pilot seed8192, no forced trajectories) checks
prefix overhead. Allow at most 14 scientific core-hours for this matrix, with a
CPU-aware finite supervisor; preserve stopped outputs if the limit is reached.
Reconcile actual CPU plus all earlier interruption upper bounds before any later
production. Expand the campaign planning ceiling from 32 to 48 core-hours, as
allowed by PLAN.md; this is a ceiling, not a requirement to spend it. Deadline
and the eight-hour review reserve are unchanged. No host timer is created.

Including the remaining clean reproduction and interruption bounds, linear
runtime extrapolation puts this confirmation plus the original capped physical
sample near 46.8 core-hours before prefix and throughput overhead. Therefore a
full physical extension is NOT automatically authorized by this estimate. If the
confirmation qualifies, make a measured cost decision before launching it. The
524,288-ID cap, frozen forecast and physical adequacy band remain unchanged; every
ID in any primary physical sample must use the qualified candidate operator.
Keep the earlier full sample separately. Never combine different operators.

If the confirmation fails or cannot finish within resources, report numerical
qualification unresolved. It does not falsify the physical reduction. If it
passes, any subsequent physical interval is conditional on this numerical
screen; report that selection and also the disjoint physical-sample diagnostic.
The confirmation is a prospective independent numerical test after a failed
screen, not a new physical prediction and not retrospective preregistration.
