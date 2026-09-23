# One new-condition independent population matrix

This matrix tests the already frozen diagnostic at s0.5,eta0.1. All numerical
forecasts must be committed, with a FROZEN_PREDICTIONS marker, before the first
case starts. No forecasts exist yet at protocol drafting. The source shares the
existing verified forward/characteristic solvers; it does not reuse kernel
trajectories or fit any coefficient to a forced population outcome.

Evolve every member of the fixed family (halo, exponential, Gaussian widths
8,32,128,512), same absolute central density and initial slope. Record T10/T20,
both physical windows24/40 and48/64. Domain changes are numerical, window changes
are different physical populations. Do not normalize any population to unit mass.

The noisy forward cases are base(J96,3072actions,128angles,dt.025),
fine(6144,256), halfstep(base mesh,dt.0125), domain(J128,4096,128),
wide(domain mesh,window48/64), wide-fine(J128,8192,256), wide-halfstep(wide mesh,
dt.0125), wide-domain(J160,5120,128), and unforced-wide. This gives the wide
physical population its own timestep and numerical-domain checks.
The positive collisionless cases cover **both windows** in each run:
base(J160,10240,256,dt.025), fine(20480,512), finer(40960,1024),
halfstep(base mesh,dt.0125), domain(J192,12288,256). Use eight-phase chunks to
bound memory. The auxiliary domain exceeds the negative-substep impulse bound.

There are14cases. Central responses use noisy-fine (or wide-fine) minus smooth-
finer. Retain base/fine and fine/finer characteristic changes. All positivity,
mass, impulse budgets, source hashes and bar-free controls must pass. Record
mesh, timestep and domain differences for each response and for every population
minus halo contrast using matching refinements. Pairing is essential: do not
add separate population errors in quadrature. Report physical-window changes
separately. No further resolution or sample ladder is part of this experiment.

## What would falsify the diagnostic?

For every profile, time and window, compare the independently evolved
population-minus-halo response with the frozen gradient-mismatch allowance.
Expand the independent difference by the sum of absolute *paired* numerical
refinement changes. This is a practical numerical proxy, not a proven bound.
An interval wholly inside the allowance supports that comparison. An interval
wholly outside contradicts it. Overlap is inconclusive. Do not treat the absence
of a detected failure as demonstrated accuracy.

Also test each frozen approximate-response point estimate against the
independently evolved halo response. For a5% qualification, require its error
plus the independent halo numerical proxy to fit5% of the conservative lower
absolute independent halo response. An error known to exceed5% contradicts a
positive qualification; overlap is inconclusive. The physical population error
and the sampled-kernel forecast error are distinct, and both must be shown.
Check qualified signs against independent halo intervals that exclude zero.

Report all rows, including the halo self-comparison as a numerical reference,
conservative unqualified approximations that actually work, and failures.
The full family shares kernels and numerical grids: it is not24independent
physical validations. The unchanged criterion has no absolute tolerance floor
that could be relabeled as5% accuracy. The source and exact arithmetic are public.

## Cost and process guard

Use at most two nice10 single-thread workers after kernel completion, with the
host-wide scientific maximum still three. Ceiling six core-hours for this matrix,
3600seconds for fine/finer cases and1800for other cases, with the unchanged
campaign production stop2026-09-24T03:35:36Z. The prior three-population23case
matrix cost2.35core-hours in a clean reproduction; this14case/six-population
matrix should fit but measured usage decides. No expensive 3D task is added.
