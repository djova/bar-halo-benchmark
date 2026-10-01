# Halo twins: force checks, a failed live screen, and where the response originates

This is a saved-data companion to the prescribed-bar twin experiment. It brings
together distinct checks without turning them into a claim that a stable live
galaxy with different bar evolution has been constructed. No new scientific
evolution is performed by the extraction or replay commands below.

The analytical construction preserves even velocity moments while changing odd
structure in the orbital population. Its prescribed-bar response is therefore an
interesting constrained counterexample. The original live realization uses
coincident velocity-reversed pairs, fails its declared energy screen, and cannot
establish collective stability or live bar braking. A proposed alternative
sampler is a separate, pending experiment.

## Which result belongs to which model?

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| Exact odd-in-angular-momentum DF identities | Density and specified even moments agree in the continuous analytical model | Stability, force accuracy, or exact finite-particle equilibrium |
| 36 static tree/direct comparisons | The two tighter openings pass the declared errors at the fixed selected targets | A bound for every particle, equilibrium, or live dynamics |
| Softened continuum quadrature | Size of the softened construction/evolution-force mismatch in the spherical model | That finite-particle sampling or tree error is absent |
| Nine original paired live cases | Recorded drift, budgets, and failed numerical qualification | A collective instability caused by the odd population perturbation |
| Isolated partner toy | A separate integration problem reproduces the approximate early energy-offset scale | Unique diagnosis of the full live system, or its equilibrium |
| Action-support decomposition | Which starting actions contribute to the recorded prescribed-bar contrast | Capture histories, trapping probabilities, a new independent physical sample |

The [analytical derivation](TWINS_EXACT_MOMENTS_DERIVATION.md) remains the source
for the continuous identities. Replaying selected-force operands is a different
operation from checking that proof. The
[growth readback](TWINS_GROWTH_RECOVERY_READBACK_V1.md) gives the separately
qualified, gradually grown prescribed-bar result. That bar does not react to
the tracer population.

## Static force opening: 36 selected comparisons

The static matrix uses 4,096, 16,384, and 32,768 reversal pairs; three
populations; softenings 0.025 and 0.0125; and tree openings 0.125 and 0.0625.
Each case has 128 selected particle IDs at 64 distinct initial positions.
Relative error is the norm of tree-minus-direct acceleration divided by the
direct norm, with a floor of $10^{-14}$. Every target is retained. The declared
screen is a 95th percentile below 0.005 and a 99th percentile below 0.01.

All 36 tighter-opening cases pass that selected screen. This does not replace
the earlier failed screens at openings 0.25 and 0.5 or establish a continuum
solution. The packet contains both saved force vectors, specific potentials,
rounded-input direct vectors, residuals, IDs, and timing operands. The replay
recomputes the percentiles and the decision for each case. Whole-particle
plus/minus RMS summaries are also reported from the source record but are
explicitly outside this selected-array replay's coverage.

## Continuum softening and the retained finite-difference failure

For the spherical isochrone with $G=M_0=1$ and scale $b=0.5$, the central
restoring coefficient changes from 2 to 1.98792517796649 at softening 0.025,
a decrease of about 0.604%; at softening 0.0125 it decreases by about 0.154%.
The global virial-force deficit is much smaller: about 0.0624% and 0.0157%,
respectively. These are continuum force differences, rather than evidence that
the sampled halo is an exact equilibrium of the softened particle force.

Thirty saved radial force integrals and four global quadrature records are
included. The NumPy replay contracts their saved weights and integrands. It
does not independently generate quadrature nodes or repeat the adaptive
integrations. Central coefficients and adaptive results are saved scalar
operands; their ratios and consistency decisions can be recalculated.

One original verification gate fails: the finite-difference derivative test.
The separate post hoc, 80-digit known-formula diagnosis supports the analytical
derivative and identifies truncation in that test. Both records remain visible.
The replay only subtracts the saved high-precision decimal operands; it does
not perform an independent high-precision differentiation. The old failed
finite-difference gate remains false.

## The original paired live screen remains numerically unqualified

The original live calculation has 8,192 halo particles, no stellar disc, no bar,
and no collisions. Two initial draws were evolved to model time 15 with step
0.01; the first draw's three populations were also evolved with step 0.005.
Softening is 0.025 and tree opening is 0.125. Sampling assigns two coincident
particles opposite velocities and population-dependent physical masses.

All nine cases fail the declared relative-energy criterion of $10^{-4}$.
Their momentum, angular-momentum vector, and selected endpoint-force screens
pass. The step comparison of the recorded shell second moments also fails for
the reference and minus populations, while the plus comparison passes. There
are rapid-adjustment flags in the reference population too. Consequently,
these flags do not establish a collective instability of the selected twins.

The compact packet includes all 31 diagnostic epochs for each case: radial
quantiles, fixed-shell masses, diagonal raw velocity second moments, coverage,
density-mode amplitudes, total energy, momentum, and angular momentum. It
includes selected endpoint force vectors, but excludes particle trajectories.
The replay reconstructs the metrics, rapid-adjustment flags, numerical screens,
and coarse/fine comparison. The combined numerical qualification remains
**false**. Completing an integration is not equivalent to passing its screen.

## Early energy offsets and a separate coincident-partner toy

At times 0, 0.5, and 15, the original live archive's direct all-particle
potentials give nearly the same early energy offset as the native potential.
The direct energy change at 0.5, normalized by the original native $|E_0|$, is
about $6.4963\times10^{-4}$. This distinguishes the observed budget problem
from a simple error in the native potential readout at those three snapshots;
it does not establish that every force component is accurate.

The diagnostic toy evolves each original coincident reversal pair in a smooth
isochrone plus the softened force from **its own partner only**. Inter-family
self-gravity is absent. Its initial additional partner binding is about
$-0.0036621$, or $-2.804\%$ of the original live $|E_0|$. Its early energy
offset at step 0.01 is about $6.5080\times10^{-4}$ in that same normalization.
Halving the step reduces the toy error approximately quadratically. Eight
preselected families were checked against a separately recorded DOP853
integration.

The offset agreement makes coincident-partner integration a plausible
contributor. It is not proof of a unique cause. Reducing the toy integration
error does not remove the physical sampling correlation or qualify the
original live system. This packet retains masses, specific kinetic energies,
direct potentials, family budget errors, and selected state **differences**;
it contains neither full live states nor full toy endpoints.

## Post hoc action support: sums, not independent orbital populations

For each of eight whole orbit libraries, the packet preserves the original
proposal mass $m_i$, stored DF weights, actions $(J_r,J_z,L_z)$, and the two
partner impulses $B_{i,+}$ and $B_{i,-}$. For each odd population $p$, the
absolute family contrast is

$$c_{p,i}=m_i h_{p,i}(B_{i,+}-B_{i,-}).$$

The reference contribution is

$$r_i=\tfrac12 m_i q_i(B_{i,+}+B_{i,-}),$$

where $q_i=F_0/F_q$ and $h_{p,i}=\delta F_p/F_q$. Here the comparison is
**plus population minus minus population** under one prescribed bar history.
It is not the noisy-minus-smooth observable in the earlier resonance study.
All quantities are absolute accumulated tracer $L_z$ transfer in the stated
model units; there is no renormalization within bins.

The saved actions define positive binding energy, circularity, and inclination
coordinates using the unsoftened analytical isochrone. The replay reconstructs
the six energy bins and five bins for each other coordinate, their positive
and negative sums, top-family absolute-contribution fractions, and the
descriptive eight-library covariance. These partitions were chosen after the
response calculation. They do not provide new advance sign qualifications.

Cancellation is substantial. In the fully present p8 case, the mean positive
and negative contributions are approximately $1.8276\times10^{-4}$ and
$-9.7810\times10^{-5}$, leaving $8.4949\times10^{-5}$. For the gradually
grown case they are approximately $1.5341\times10^{-4}$ and
$-9.7725\times10^{-5}$, leaving $5.5682\times10^{-5}$. The energy interval
0.4–0.7 contributes more than the total net contrast in each history because
other intervals partly cancel it. These are signed response contributions,
not literal positive/negative orbital cohorts or counts of captured particles.

The original action-support metadata says growth refinement was pending when
that record was produced. It is retained as history. The later growth recovery
is documented separately, with its original interrupted parent left incomplete.

## Inspect and replay

The [local dataset manifest](../../operands/twins-force-support-v1/manifest.json)
defines every array's axes, units, dtype, shape, file size, and checksum. The
[compact result record](../../data/twins-force-support-v1.json) exposes the
source operands and preserves failed decisions. From the `discovery` directory
in the clean public package:

```sh
python scripts/discovery/replay_twins_force_support_v1.py --out reproductions/force-support-local
```

Dependencies are Python and NumPy only. The supplied reproduction receipt
records the actually measured execution cost and arithmetic differences for
that preparation. This is a cheap saved-data consistency check; it neither
reproduces the underlying evolution nor independently validates astrophysical
applicability or confidence coverage.

The next live sampling proposal uses one independently sampled position per
particle and a common random sign switch across the two populations. It avoids
deliberate coincident partners while introducing odd-moment sampling noise that
must be checked. Until that new draw and its controls qualify, no replacement
live-halo result is claimed.
