# Identical ordinary halo moments, different prescribed-bar response

**Preliminary prescribed-field result, 1 October 2026.** Two analytic halo
populations can have exactly the same density, local mean velocity and all even
velocity moments, while their responses to an imposed rotating bar differ. For
the fixed p = 8 construction at the reference frequency, the measured accumulated
angular-momentum-transfer contrast is **8.49×10⁻⁵**, with a nominal pointwise
95% interval **[5.54×10⁻⁵, 1.15×10⁻⁴]**. These are reference mass–action units;
they are neither a galaxy slowdown nor a dark-matter constraint.

The corresponding plus/minus transfer ratio is **1.446**, a ratio of ensemble
point estimates. We have not established a confidence interval for that ratio
or reached the original factor-of-two ambition. The shared reference transfer
has substantial uncertainty, which is retained alongside the better determined
paired contrast. This is a tracer calculation in prescribed fields, with no
reacting halo or stellar disc.

## What was deliberately held equal

In the unsoftened spherical isochrone with G = M = 1 and b = 1/2, the frozen positive
populations are

\[
F_\pm=F_0(e)\pm\alpha_p L_z[g_{0,p}(e)+L^2e^p],\qquad p\in\{4,6,8\},
\]

\[
g_{0,p}(e)=-\frac{4p\,e^{p-1}}{(p+5/2)(p+7/2)}
          +\frac{8b\,e^p}{p+7/2},\qquad e=-E.
\]

Odd velocity parity preserves density and every even moment. A separate
Beta-integral cancellation preserves all three local mean velocities at every
radius and inclination. An exact rational positivity construction fixes each
α before reading the family's forced responses and gives F±≥F₀/2 throughout
the bound orbital domain. Higher odd moments can differ: the public data
contain the actual unforced azimuthal third moments at eight radii and four
inclinations. Those profiles illustrate hidden velocity structure; they do not
predict the torque by themselves.

See the [derivation](TWINS_EXACT_MOMENTS_DERIVATION.md),
[frozen unforced protocol](TWINS_EXACT_MOMENTS_PROTOCOL.md) and
[independent internal algebra check](TWINS_EXACT_MOMENTS_CHALLENGE.md).
Stationarity and self-consistency hold for this spherical unsoftened reference.
Collective stability, a softened live equilibrium and formation-history
reachability remain untested.

## What the measured contrast supports

The eight independently randomized action/phase libraries are the sampling
units. All three populations and both stationary bar frequencies share those
libraries, so the six comparisons are correlated. The full contrast and
contrast/reference covariance matrices and all eight library vectors are
available in [the scientific export](../../data/twins-exact.json).
Student-t intervals with seven degrees of freedom have uncalibrated coverage;
supplementary Bonferroni intervals apply only to these six comparisons.

At the reference frequency, p = 4 has an unresolved sampling sign and fails one
of the two doubled-phase checks. The p = 6 and p = 8 contrasts pass the selected
phase and timestep screen, whose frozen allowance is 10% of the measured
contrast. The largest p = 8 phase shift is 2.82×10⁻⁶, or 3.32% of its contrast.
The half-step shift is 2.10×10⁻¹². These are selected numerical comparisons,
not a complete discretization error bound.

For p = 6, the supplementary six-comparison interval is nominally positive, but
its lower margin (1.24×10⁻⁶) is smaller than the largest measured phase shift
(2.92×10⁻⁶). The recorded screen decisions remain unchanged; they must not be read as
a joint sampling-and-numerical sign guarantee. The p = 8 supplementary lower
margin is 3.95×10⁻⁵, substantially larger than the selected shift, while still
subject to the stated sampling and numerical limitations.

The second stationary frequency has no doubled-phase comparison. Its timestep
checks alone do not qualify phase accuracy. Neither frequency is a new-history
prospective prediction: these are known recorded trajectories contracted with
populations fixed from unforced inputs, without response fitting. The
[response protocol](TWINS_EXACT_RESPONSE_PROTOCOL.md) records that distinction.

Physical mass is preserved absolutely. Because the trajectories were sampled
from the approximate AGAMA distribution Fq, the contraction uses
m(F₀±αδF)/Fq, with no separate population normalization. The represented exact
mass is recorded rather than silently rescaled. Angular-momentum and
energy/external-work residuals are supplied as numerical bookkeeping checks;
they do not establish a live-halo or observational result.

## What this teaches us, and what would test it next

Matching the ordinary local halo moments need not specify its response to a
rotating gravitational perturbation. This construction removes the finite-grid
streaming mismatch of the earlier search, but it does not establish different
self-consistent bars. An independent forcing history and a stability
test are separate next experiments. The derivation is internally checked, not
externally reviewed; priority relative to existing halo-population and
resonant-response work remains an open scholarly question.

The scientific export contains actual scalar values, paired refinements,
covariances, velocity-moment quadrature checks and hashed archive selectors.
The [compact analysis replay](../../README.md#exact-moment-halo-twins)
regenerates the six contractions, their intervals and covariance from released
saved impulses and sampling-density operands. Full orbit evolution and the
velocity-marginal quadrature are not regenerated by that replay. The older
preliminary coarse readback is retained; this summary uses the terminal
`exact-response-final-01` record and does not overwrite that history.
