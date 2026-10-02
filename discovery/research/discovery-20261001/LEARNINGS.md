# What the discovery screens have taught us

Scientific closure review, 2 October 2026. Publication remains in preparation. These
are controlled-model results and decisions about further work, not five
discoveries or observationally validated galaxy models. The
[current progress record](../../REPORT.md) distinguishes closure from historical execution status.

## A mass profile and ordinary kinematics do not specify an orbital population

The strongest halo-twin construction matches density, all local mean velocities
and every raw even-total-degree velocity moment initially at every position.
Both smooth, positive distributions remain above half the reference DF. Higher
odd moments differ. This is a continuum identity, stronger than matching a
finite set of radial bins; it still does not prove collective stability.

Under one prescribed bar, the strongest pair has a resolved angular-momentum
transfer contrast. The ratio of endpoint point estimates is about 1.45, without
a ratio confidence interval. The initial factor-of-two ambition is not reached.
A gradually grown bar supports another population's contrast under the declared
three-population interval. These are external-field responses, not different
self-consistent bar histories. See [the exact-twin result](PUBLIC_TWINS_EXACT_SUMMARY.md)
and [the growth calculation](TWINS_GROWTH_RECOVERY_READBACK_V1.md).

The live prerequisite screen exposes a separate ambiguity: a finite shell's
velocity moment can change because particles move into and out of that shell,
even in a stationary potential. The same particle samples cross the original
moment threshold in the analytic field as well as the live calculation. Their
residual difference does not isolate force mismatch from collective response.
An accurate particle integrator and a quiet-looking movie are insufficient
stability evidence. See [the phase comparison](../../CHECKS.md).

There is also an exact formation restriction. The constructed populations have
a larger quadratic phase-space integral than the smooth reference. Exact
collisionless evolution, or convex mixing of that exact reference, cannot
create either exact twin. This excludes that particular proposed history;
it does not exclude other progenitors or approximate populations. A separate
symmetry argument (the reflection argument is stated below) predicts that an axisymmetric
prescribed field cannot distinguish their scalar energy responses. The useful
signal must be tied to an appropriate nonaxisymmetric interaction. In a fixed
axisymmetric imposed field, reversing the azimuthal velocity leaves scalar
energy evolution unchanged, while the twin DF difference is odd in Lz. The
integrated scalar-energy contrast therefore vanishes by reflection symmetry.

A further test asks whether unforced information predicts the response magnitude.
A uniform orbital-angle grid misses brief pericentre passages of some radial
orbits. An independent analytic eccentric-anomaly calculation with the correct
time measure repairs that specific quadrature problem while retaining those
orbits. It does not by itself certify a torque: Fourier tails, the full action
integral, signed cancellation and weak-forcing applicability still matter.
See [the coefficient diagnosis](../../source-snapshots/twin-forecast/README.md).

A finite-time prediction was sealed before independent Cartesian evolution at
a new, much weaker bar history. All three families have a resolved positive
transfer difference at both amplitudes. The paired test supports a quarter-size
response when the amplitude is halved, as expected for the second-order law.
The absolute-magnitude forecasts nevertheless remain unresolved under the
declared five-percent test: action-library sampling uncertainty dominates the
small measured timestep and phase changes. Agreement within an interval is not
an accuracy qualification. The p = 4 family's sealed Fourier-tail limitation
also remains. No post-outcome sample extension is made. See
[the sealed forecast](../../CHECKS_V2.md) and the
[fixed direct protocol](../../TWINS_WEAK.md).
This weak-field calculation does not validate the older, stronger bar history.

## A small whole-disk heating average can conceal a substantial inner cost

The measured cost is specific energy, not stellar velocity dispersion. For
example, a uniform canonical radial-momentum shift by k adds mean energy k²/2
to a population with zero initial mean radial momentum, while leaving its
instantaneous radial velocity variance unchanged. Coherent motion and random
motion must be separated before interpreting an energy deposit as stellar
overheating. Neither radial nor vertical dispersion is measured by the scalar
energy controls in this campaign.

In the original cored example, a high-frequency positive gas redistribution
preferentially heats a selected stationary halo population. The whole-star
specific-energy cost is 0.00338 of the halo-tag value; the fixed inner guiding
cohort gives 0.08996. Those are different population averages. Distant stars
dilute the whole-population result, so it is not a co-spatial stellar-survival
bound. A central stellar hole and a maximum circular frequency limit that
example. See [the cored result](FEEDBACK_PUBLIC_SUMMARY.md).

The centrally populated cusp removes that frequency-gap argument. Its actual
halo response is now resolved under the two fixed finite gas pulses, with
explicit external-work, support and numerical controls. The energy gains are
only about fifteen and four parts per million of the selected tag's binding
energy. The deepest binding cohort contributes almost none. Heating the tag
therefore does not establish a transformed cusp or a dark-matter core.
See [the finite cusp calculation](../FEEDBACK_CUSP_FINITE_RESULT.md).

The coeval warm stellar estimate initially fails because a few sampled paths
carry almost the entire signal. A new full-support proposal, constructed from
unforced information, preserves the physical population and materially improves
sampling precision. Its independent 4,096-state calculation nevertheless fails
the frozen all-state inverse-replay tolerance. Underflowed target values do not
justify deleting those paths. Selected extended-precision maps diagnose a large
roundoff component, but they cannot qualify the whole population.

The first attempted all-state refinement stops at its measured-cost admission rather
than quietly enlarging the allocation. Its complete first map remains useful
for an arithmetic-sensitivity comparison. Sampling precision, reversibility,
force-integration accuracy and the physical population being averaged are
different questions; one passing check cannot stand in for the others. That
original partial stage supplies no qualified stellar cost. The stellar guiding
cohort and halo binding tag also remain different physical selections.

A saved-array comparison makes the dilution quantitative. The inner guiding
cohort contains 2.65% of the physical stellar mass but contributes about 95.6%
and 99.9% of the sampled paired heating at the two fixed carrier frequencies.
The corresponding empirical standard errors are 2.47 and 0.068 percentage
points, preserving numerator–denominator covariance. The original failed
scientific qualification remains; these are descriptive sampled contributions,
not a qualified stellar-survival measurement. An all-state coarse-map
extended-arithmetic comparison changes the energy means by only about 10⁻¹⁹,
without supplying the missing fine and inverse-composition controls. See
[the saved readback](../../CHECKS_V2.md).

A small native implementation reproduces the tested extended-arithmetic force,
full-size short maps and complete selected maps exactly, including signed zeros.
Its measured short-map speedups exceed two. This removes a specific cost
obstacle to attempting the missing whole-population controls; it is an
implementation result, not a repaired physical measurement. The original failed
population and cost-stopped refinement remain unchanged. A separately frozen
all-state stage now completes all original criteria. Its complete coarse map
matches all seven archived NumPy extended-arithmetic fields exactly and passes
the measured timing admission. Both coarse and fine inverse compositions meet
the unchanged tolerance on all 4,096 states; the response, support, work,
refinement and selected reference controls pass as well. Its fine paired
specific-energy means are approximately 9.75×10⁻⁷ and 1.07×10⁻⁷ for the whole
stellar population, and 3.51×10⁻⁵ and 4.05×10⁻⁶ per unit mass of the inner
guiding cohort. The different denominators are part of the measurement.

A saved-only reader initially fails exact covariance reconstruction because it
groups a multiplication and division differently from the original operation.
The maximum covariance difference is 2.42×10⁻²⁷. Reproducing the original order
restores exact equality without relaxing a tolerance or changing any trajectory
or scientific output. The original reader failure remains. Its corrected
success verifies saved arithmetic, not statistical coverage or physical
replication. The new energy measurement is qualified within the stated gates;
it still establishes neither co-spatial stellar survival, velocity dispersion,
a core nor a universal no-hide bound.
The [terminal numerical closure](../../WARM_COST.md) records
the precise observables, fixed thresholds and retained failures.

## Recoverable orbital memory is not necessarily a visible gravitational signal

Independent formulations and memory-erasure, timing and amplitude controls
support a radial halo echo. Its stronger frozen force is only about twenty-two
parts per million of the background. The illustrative unamplified stellar
readout is too small to establish visible structure. A potential perturbation
inside an exterior spherical shell can also be spatially constant: the force,
not merely the potential, is essential. See [the radial echo](PUBLIC_ECHO_SUMMARY.md).

The separate spatial two-frequency model predicts an even smaller gravitational
sector. All four finite shape-sign cases retain common positive monopoles;
their quarter-signed contrast selects the response odd in both perturbations,
rather than applying the original neither/A/B/AB intervention. Finite
inverse-map quadrature produces a false signal at an instant
where positions, and hence the mixed density field, must be unchanged. Energy
refinement repairs the mass integral before it repairs that field. Subsequent
known-zero grids pass their declared threshold, but that prerequisite does not
certify later filamented distributions.

At the first declared late date, the finer finite field is close to the saved
weak-pulse prediction. The coarse and fine fields nevertheless disagree by
roughly 29%, 64% and 29% of their respective local scales, failing every
five-percent refinement gate. Selecting the result that resembles the theory
would conceal the numerical failure. The blocked later matrix remains blocked;
cross grids diagnose the numerical direction, not a new physical force.
They identify the angular-momentum quadrature as the dominant tested direction;
the radial channel also retains a smaller phase-grid sensitivity. Neither
cross grid is a convergence confirmation.
See [the finite-field result](../../CHECKS_V2.md).

A validated finite spatial sector would still need memory, separation and
amplitude controls before an echo interpretation. Collective amplification and
a visible stellar readout are further physical tests, not consequences of a
phase-space animation.

## Two other screens reach useful stopping points

The conservative collision-law pair matches conditional drift and the second
velocity tensor while retaining a different higher moment. Its moving-wave
contrast does not retain a qualified sign under timestep and cell refinement.
That is neither a SIDM result nor evidence that every scattering law is
interchangeable. Ordinary transport matching is the premise of a prospective
discriminator, not proof of one.

Published modified-inertia harmonic equations pass their known limits and
residual checks. Frequency filters with the same circular calibration give
substantially different secondary frequencies. General causal evolution,
admissibility and observations do not select among them here. This exposes
information missing from circular calibration; it does not validate a
replacement theory of gravity. See [the terminal screens](PUBLIC_TERMINAL_BRANCHES.md).

## What deserves a larger experiment

The weak-bar test now illustrates why a forecast frozen before independent
driven outcomes is useful even when its accuracy remains unresolved. Its
response sign and quadratic scaling survive, while the magnitude test exposes
the cost of action-population sampling. A larger experiment would need a
prospectively designed precision strategy, followed by a separate collective
stability and live-bar test. It should not simply continue the current sample
until a favorable interval appears. Numerical and sampling limitations should
stop or narrow a claim rather than produce a favorable redefinition. Models,
clocks, population selections and normalization must remain explicit.

Saved-array readers make reported arithmetic inspectable. They do not repeat
orbit evolution, establish general statistical coverage or confront observed
galaxies. A delivery audit verifies publication bytes, not the science. The
purpose of these checks is to remove a consequential ambiguity and identify
which hypothesis deserves a larger physical experiment.
