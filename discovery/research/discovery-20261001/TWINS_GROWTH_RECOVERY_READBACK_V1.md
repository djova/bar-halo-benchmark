# Gradually introducing the bar: completed response and numerical controls

The frozen halo populations retain different measured angular-momentum responses
when the external bar grows continuously from zero. At time 300, **p6 is positive
under both the nominal pointwise interval and the predeclared three-population
Bonferroni interval**. p8 is positive pointwise but unresolved under that family
interval; p4 is unresolved under both. All three populations pass the selected
phase and timestep screens. Numerical qualification and statistical resolution
are separate outcomes.

This is a prescribed-field tracer experiment. It does not measure the braking
of a live bar, collective halo stability, or an observed galaxy. There is no
imposed diffusion or SIDM collision operator in this particular experiment.
The contrast is the transfer of the plus population **minus the minus
population**, not noisy-minus-smooth transfer from the earlier local study.

## What changed, and what stayed fixed

The unbarred model is the spherical isochrone with G=M=1 and b=0.5. Its frozen
positive p4, p6, and p8 distribution-function pairs have identical density,
zero local mean velocities, and even velocity moments in the analytic model.
Their higher odd moments differ. All populations share the same externally
prescribed bar, action libraries, and recorded trajectories; only their frozen
physical weights differ. No population is rescaled to a selected unit tracer
mass.

The bar amplitude rises from zero to 0.03 over 100 reference time units through
the previously declared smooth quintic ramp, then stays at 0.03 until time
300. The reference pattern speed and populations were frozen before this new
history was integrated. This checks robustness to gradual growth; it is not
a magnitude forecast fitted independently of the forced calculation.

Eight independently drawn action/phase libraries provide the ensemble. Each
has 512 action families, 16 scrambled radial/vertical phase pairs, 32 azimuth
sectors, and both prograde and complete velocity-reversed senses. The sampling
unit is the whole library. Phase nodes, senses, times, and populations are not
independent replicates. All intervals below are nominal Student-t calculations
with seven degrees of freedom; their coverage has not been calibrated. The
three-comparison family is this history's three endpoint contrasts, not every
historical campaign or every recorded time.

## Recorded endpoint response

The quantity is the accumulated bar-mediated angular-momentum transfer contrast,
in reference angular-momentum units, using common absolute halo mass weighting.
It is neither instantaneous torque nor a percentage of a complete live halo's
torque. The full precision values and shared covariance are in the numerical
record; the following values are rounded for reading.

- **p4:** contrast 2.56076e-6; standard error 1.61448e-6. Pointwise 95% interval
  [−1.25689e-6, 6.37841e-6]; three-population interval
  [−2.48862e-6, 7.61015e-6]. Its sign is unresolved.
- **p6:** contrast 3.69349e-5; standard error 1.07572e-5. Pointwise 95% interval
  [1.14981e-5, 6.23717e-5]; three-population interval
  [3.29115e-6, 7.05787e-5]. Both nominal intervals support a positive sign.
- **p8:** contrast 5.56823e-5; standard error 1.92858e-5. Pointwise 95% interval
  [1.00787e-5, 1.01286e-4]; three-population interval
  [−4.63498e-6, 1.159996e-4]. Pointwise resolution does not establish familywise
  resolution.

The reference mean transfer is 1.95616e-4, with standard error 7.62296e-5 and
pointwise interval [1.53613e-5, 3.75870e-4]. The plus/minus endpoint ratios of
means are 1.01318, 1.20850, and 1.33189 for p4, p6, and p8. These are **point
ratios**, with shared uncertainty supplied separately; no ratio interval or
factor-of-two contrast is established.

## Numerical checks and retained cancellation

On the original library 0, the declared controls separately double azimuth
sectors, double radial/vertical phase pairs, and halve the integration step.
The acceptance criterion uses each signed net shift, requiring its magnitude
to be less than 10% of the eight-library ensemble contrast. All nine decisions
pass. This is a selected-library screen, not a bound on every orbit or every
library.

The absolute-family sums are much larger than the net phase shifts: up to
93.4% of the p4 ensemble contrast and 26.9% of the p6 contrast. They explicitly
retain cancellation that the signed criterion uses. They are reported as
diagnostics; the protocol never called them alternative 10% acceptance bounds.
More phase points did not make every family's impulse individually identical.

<details>
<summary>Complete endpoint refinement operands</summary>

| Refinement | Population | Signed net shift | Absolute weighted family sum | Net / ensemble magnitude | Original signed gate |
| --- | --- | ---: | ---: | ---: | --- |
| Azimuth double | p4 | −2.22122e-7 | 2.08875e-6 | 8.67405% | Pass |
| Azimuth double | p6 | 1.00521e-6 | 8.21900e-6 | 2.72156% | Pass |
| Azimuth double | p8 | 1.28495e-6 | 6.53121e-6 | 2.30764% | Pass |
| Radial/vertical double | p4 | −8.36432e-8 | 2.39164e-6 | 3.26634% | Pass |
| Radial/vertical double | p6 | 2.41836e-7 | 9.92537e-6 | 0.654763% | Pass |
| Radial/vertical double | p8 | 8.09135e-7 | 8.85059e-6 | 1.45313% | Pass |
| Half timestep | p4 | 3.89164e-13 | 1.48247e-12 | 1.51972e-5% | Pass |
| Half timestep | p6 | 3.73204e-12 | 1.41931e-11 | 1.01044e-5% | Pass |
| Half timestep | p8 | 3.74097e-12 | 1.62000e-11 | 6.71842e-6% | Pass |

</details>

Across the eight coarse and three refinement cases, the largest recorded
per-path energy-minus-external-work discrepancy is 5.54210e-9, and the largest
Lz-minus-integrated-torque discrepancy is 7.19922e-11. The energy account includes
both the bar's rotation and amplitude growth. Small bookkeeping residuals do
not alone establish a small population-response error; the separate paired
refinements remain relevant.

## Interruption, recovery, and resource accounting

The original command disappeared during its first refinement, after all eight
coarse cases had completed. Its last status reports 5171.80689222 CPU seconds
at azimuth-refinement time 262.5. That is a partial reading, not final actual
CPU use. The original 9000-second hard limit remains a conservative reservation;
it is not a claim that 9000 seconds were spent. The cause of the interruption
has not been established.

The new complete composite retains those original eight coarse cases and adds
only the three originally planned refinements. It finished on 1 October at
21:10:25 UTC, reporting **3245.138764121 CPU seconds (0.901427 hours)** and
3245.471943 wall seconds. Its measured first-case profile projected
3333.195626 CPU seconds, within the unchanged new soft cap of 3500 seconds.
The new hard cap was 3600 seconds and the internal wall limit 4200 seconds.
The partial original reading and upper reservation are recorded separately
from this measured new-command cost.

All 72 copied artifacts retained their frozen hashes after execution. The newly
mapped radial/vertical initial-state hash also stayed unchanged. Both doubled
phase rules contain the original coarse states exactly. Replaying the saved
azimuth initial conditions reproduces every retained family impulse and work,
all 512 recorded six-component traces and their impulse/work histories, trace
IDs, and all 22 recorded times through 262.5 **byte for byte**, with zero maximum
differences. Contraction and budget histories also match exactly. The partial
checkpoint does not contain every particle's evolving state, so this is not a
claim that a full-particle restart was performed.

The original command remains interrupted, without its own completion marker.
Completing the composite does not create a new eight-library sample or relabel
the interrupted process complete.

## Prepared public saved-array check

The proposed compact package contains eight NPZ files totalling 4,418,689 bytes.
They retain all 25 recorded family impulse/work values, original actions,
absolute masses, frozen ratios/odd weights, and the three library-0 controls.
Axes, units, seeds, pairing, sizes, subset hashes, and original full-array hashes
are provided separately. No private host paths, process IDs, credentials,
complete Cartesian initial-condition arrays, or binaries are included.

A NumPy/SciPy-only script independently recomputes the published contractions,
means, standard errors, both interval conventions, shared covariance, signed
and absolute refinement values, and decisions from those operands. The local
prepared-package readback matched **12,894 numerical values exactly**, with
maximum absolute difference zero. Extraction took 0.405265 CPU seconds and the
saved-arithmetic check 0.0583353 CPU seconds in the recorded environment.

This is analysis reproduction from supplied outputs. It does not resample
AGAMA, rerun trajectories, independently validate the gravity integration,
calibrate uncertainty coverage, or establish observational agreement. The
package is prepared for root review; no new public tag or deployment is claimed.
