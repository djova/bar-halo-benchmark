# Fixed independent precision check of the matched moving reduced model

22 September 2026, after the matched stationary control passed. The moving
distribution estimate has qualified numerical changes, but its original eight
independent path batches have a95% interval that includes zero. Do not call the
matched sign change independently resolved on that evidence.

Run one new fixed sample: eight disjoint seeds8501..8508,524288 trajectories per
seed, each with eta=.1 and eta=0, s=.25, T20, sigma8 and the unchanged B slope
-0.004749321154862916. Use the existing independent trajectory implementation,
dt=.0125, and matched initial particles/random stream between noisy and smooth.
Total4194304 new independent initial particles. There is no early stopping or
further sample extension. The original eight batches remain in their archived
record; do not pool them silently or change the frozen3D magnitude forecast.

The original batch standard error.00275818 predicts a new Student-t95%half-width
about.00163, roughly20%of the .00804390 distribution contrast, under square-root
sample scaling. This is a planning estimate, not a guarantee or acceptance
interval. The new timestep is half the original stochastic step; the independent
distribution timestep shift is already5.77e-7. We do not pretend that the old and
new stochastic samples share Brownian paths or that their difference is a pure
timestep estimate.

Report all eight contrasts, equal-weight batch mean and Student-t95% interval,
the exact paired particle IDs/initial-action identity, raw hashes and local
budget gates. Require the new interval to contain the unchanged distribution
contrast before an independent-agreement claim. Report sign resolution
separately. Failure remains failure; no fitted correction or third sample.
This refines a reduced-model measurement only, not3D qualification or halo physics.

Ceiling1corehour from map8, one nice10 single-core worker,300s finite wall limit
per case. Inspect recorded CPU before any additional work. Combined scientific
concurrency remains at most4 with the active Cartesian diagnosis and clean rerun.
