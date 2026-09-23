# Population-kernel predictions: frozen new shapes

Declare these shapes before contracting any completed validation kernel against
them or generating their forced outcomes. Existing Gaussian8, halo and exponential
profiles remain the calibration/assembly population set. No response parameter
will be fit to the new populations. This is a test of a reusable numerical
response operator in the specified external local model, not a new3Dphysical
prediction or a demonstration of novel linearity.

## Three physically positive test populations

Retain central density Fref and dimensionless initial slope g from the unforced
case-B halo, fixed fast actions, local dynamics, s0/.25, eta0.1, and T10/T20.
Multiply each shape by the same tested smooth24/40 and48/64 windows, without
renormalizing its mass:

- Gaussian12: exp(g*x - x^2/(2*12^2)).
- Gaussian20: exp(g*x - x^2/(2*20^2)).
- Quartic20: exp(g*x - x^4/(2*20^4)).

The first two vary the initial log-curvature through intermediate and broader
populations. The third shares the exponential's density, slope and log-curvature
at zero, while differing away from the initial resonance. It tests whether those
three local values alone suffice. These are controlled positive tracer shapes,
not three alternative equilibrium halo models. Both times are mandatory; none
is selected for a desired sign.

## Forecast, then independent check

After all16original validation batches complete, form every new population's
response by contracting its derivative with the recorded primitive kernel.
Retain eight batch contractions and their covariance, mean, pointwise95%t7
interval, fine/coarse step difference and doubled-kernel-cell comparison. Freeze
and commit those numerical forecasts BEFORE launching forced evolution of any
new shape. A forecast from an unqualified source kernel stays unqualified.

Validation should use the independent noisy distribution solver plus positive
fourth-order collisionless characteristic quadrature. Freeze a separate bounded
matrix after the current deterministic refinement establishes its cost and
precision. It must include grid, timestep, auxiliary-domain and physical-window
checks, and bar-free controls. Use the same absolute2e-4 numerical comparison
target; never repair a failed qualification by relaxing it.

For a qualified forecast and independent calculation, report the distribution
value minus each of the eight predicted batch responses. Its complete95%t7
interval must lie within +/-max(2e-4,0.05*abs(frozen forecast mean)) for a5%/absolute
accuracy statement. This is a declared operational criterion, not a rigorous
bound; report the raw difference and all numerical changes as well. No failed
profile, duration or sweep may be dropped. A held-out local-model success still
does not qualify transfer to Cartesian dynamics, a reacting halo or SIDM.

## What the result can teach

Report the exact population-weighting error against the exponential local-slope
approximation, paired through the kernel. Show the density, its gradient and the
signed primitive-kernel contraction on the same action coordinate. Also retain
raw initial-action conditional kernels, whose bins describe actual starting
orbit cohorts. The gradient decomposition is mathematically equivalent after
integration, but its bins are not those cohorts.

Quantify gradient-space contributions inside and outside|x|=4,8,16,24,40,64,
including signed cancellation and uncertainty. Any integral of an absolute noisy
estimate has an upward noise bias; do not label its tail as physical locality.
Use the kernel to evaluate the signed approximation error and an absolute-integral
diagnostic, with that limitation explicit. A useful criterion is conditional on
this measured response operator and its support, not a universal curvature law.
