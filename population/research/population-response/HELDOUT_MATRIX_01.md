# Independent new-population evolution — matrix 01

Frozen after the original deterministic refinements, before any forced evolution
of Gaussian12, Gaussian20 or Quartic20. This implements HELDOUT_POPULATIONS_01.md.
It does not change the physical coefficients, bar history, diffusion, populations,
normalization, two durations or the declared 2e-4 numerical comparison scale.
The complete eight-batch kernel predictions must be saved and committed before
this matrix starts; their hashes are then included in the execution manifest.

For each s=0 and0.25, evolve all three positive shapes together with the noisy
forward distribution solver: base(J96,3072actions,128angles,dt.025), fine(6144,256),
halfstep(base mesh,dt.0125), domain(J128,4096,128), wide(same domain mesh,window48/64),
wide-fine(J128,8192,256), and unforced-wide(domain mesh). All record T10 and T20.
The original window remains24/40. Numerical domain and physical taper changes
remain separate. No mass renormalization is performed.

The independent positive collisionless quadrature covers both windows in every
run. At each sweep use base(J160,10240,256,dt.025), fine(20480,512), halfstep(base
mesh,dt.0125), and domain(J192,12288,256). At the moving sweep also use finer
(J160,40960,1024), based on the prior Gaussian's measured fine/finer change.
The central collisionless answer is stationary-fine or moving-finer. Retain the
moving base/fine change even when fine/finer is the final refinement comparison.
The auxiliary domain exceeds the full negative-substep impulse bound, as in the
original positive-characteristic verification. No further grid ladder is included.

There are23cases, run by at most two nice10 single-thread workers. The measured
original costs (fine noisy~833–856s; fine/finer characteristics~310/1294s) motivate
an aggregate4core-hour ceiling, with finite per-case wall limits and the campaign
production stop2026-09-24T15:32:27Z. Source changes or output failures stop scientific
qualification. Reproduction can use one remaining scientific worker; total live
scientific workers must never exceed three. Use actual measured CPU for accounting.
This reallocates unused stage/reserve time within the unchanged32core-hour ceiling.

## Comparisons and decision

Check each population, sweep and duration, both windows; no selected subset.
Require every local mass, positivity, impulse-budget and bar-free gate to pass.
For characteristics report action/angle refinement, timestep and auxiliary-domain
changes for both windows. For noisy evolution report base/fine mesh, base/halfstep,
base/domain, and wide/wide-fine mesh changes. The physical window comparison uses
matched domain meshes and characteristic-domain outputs. Require every relevant
absolute change below2e-4. Changes are operational diagnostics, not rigorous bounds.

For the narrow window, the central result is noisy-fine minus the finest prescribed
collisionless quadrature. For the wide window it is noisy-wide-fine minus the same
finest quadrature with wide weights. Compare these with the frozen eight-batch
forecasts using independent-minus-predicted differences, Student-t7 intervals and
exactly the allowance recorded in the forecast: max(2e-4,5%of forecast magnitude).
The entire interval must be contained in that allowance, and both forecast and
independent numerical/window qualifications must pass. Retain failed and unresolved
rows without relaxing any condition. This verifies new-population prediction within
the local prescribed model; it is not a held-out Cartesian or physical SIDM test.
