# Final numerical result: timestep passes, cadence uncertainty remains

The last declared six-case matrix completed on 22 September 2026. It uses the
same first 16,384 case B particles, frozen physics, fourth-order integrator and
nested Brownian paths. Both noisy and collisionless trajectories are retained.
The allowance remains 1.8126730139721574e-7 in physical model Lz units.

| Change from candidate | Estimator | Mean shift | Nominal 95% paired interval | Decision |
| --- | --- | --- | --- | --- |
| Half integration step | Raw 3D noise contrast | +4.26515e-10 | [-1.22283e-9, +2.07586e-9] | Pass |
| Half integration step | 3D minus reduced discrepancy | +4.26515e-10 | [-1.22283e-9, +2.07586e-9] | Pass |
| Half noise cadence | Raw 3D noise contrast | -5.88419e-9 | [-1.89956e-7, +1.78188e-7] | Fail |
| Half noise cadence | 3D minus reduced discrepancy | -1.19455e-7 | [-4.04744e-7, +1.65835e-7] | Fail |

All four point shifts fit inside the allowance. Two cadence intervals do not.
The raw cadence interval exceeds the allowance by about 4.8%; the discrepancy
interval reaches 2.23 times the allowance. Do not replace these interval gates
with a point-only conclusion or a rounded value. Every local budget/identity
gate passes. That is necessary verification, not a physical prediction result.

The deterministic microstep changes from 0.009999412 to 0.004999706 in the step
test, at the same 0.499970599 noise cadence. The half-cadence test uses cadence
0.249985300 and a slightly different deterministic microstep, 0.009614819,
because each block is divided into an integer number of steps. The independent
step test is small; the cadence test still contains that rounding change and
must not be described as perfectly fixed deterministic steps.

The 20 largest squared deviations supply 95.68% of the raw cadence variance
and 91.98% of the discrepancy variance. One path supplies more than half of the
raw cadence variance; three supply half of the discrepancy variance. All paths
remain. Student-t intervals are nominal iid sampling approximations, not
rigorous truncation-error bounds or guaranteed coverage for rare tails.

The reduced trajectories also change under cadence refinement: their paired
mean shift is +1.13571e-7, with interval [-9.57752e-8, +3.22917e-7]. Therefore,
subtracting the reduced response does not automatically cancel the uncertainty
in this numerical intervention. The same Brownian endpoints agree to 7.3e-17;
the intermediate kicks approximate the same imposed white-noise law. Cadence
is not a physical noise correlation time.

## Scientific interpretation and stopping decision

The remaining numerical qualification limit is localized to the cadence
comparison and its rare-path sampling uncertainty. This does not demonstrate
a large cadence bias, reject white diffusion, or establish failure of the
constant-coefficient physical reduction. The point changes alone are small.

The candidate prefix's raw 3D contrast is +1.84591e-6 with interval
[-2.26057e-5, +2.62975e-5]. Its paired model discrepancy is -2.53607e-7 with
interval [-6.77745e-6, +6.27024e-6]. This fixed numerical prefix is not a
replacement for the original full sample or a sufficiently precise magnitude
test. Its sign and physical adequacy remain unresolved.

As committed before the matrix, no further automatic numerical ladder or
larger population run follows this failure. The planned 524,288-particle
extension remains unrun. No physical parameter, phase sample, threshold or
forecast is changed. Finish the same-seed clean reproduction and publish the
bounded result. The campaign has not established a predictive 3D response law.

Authoritative readback: final-numerical-analysis-01/result.json. The companion
figure shows all four unchanged intervals and every particle's contribution to
the ranked variance. The original failed numerical attempts remain archived.
