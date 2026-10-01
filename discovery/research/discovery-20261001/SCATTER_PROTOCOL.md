# Scattering laws and a moving resonance: conservative reference screen

Frozen 1 October 2026 before operator/evolution results. Scope: a one-dimensional
periodic gas with three velocity components and a moving cosine potential.
This isolates a kinetic question with equal-mass elastic events and exact
linear momentum/kinetic energy conservation at each event. It is not a halo,
bar evolution model, or an observational SIDM discriminator.

## Literature boundary

Angular laws approximately map through the viscosity cross-section in relaxed
halos and even a constant-density dynamical-friction experiment. Finite-angle
collision versus angular diffusion differences are already established.
We test a prescribed moving resonance and measure whether differences survive
equilibrium, ordinary relaxation and numerical controls.

- [Fischer & Sagunski 2024](https://arxiv.org/abs/2405.19392), particularly their angular matching comparison.
- [Arido et al. 2025](https://arxiv.org/abs/2410.07175), hybrid small/large-angle methods and their validation.
- Existing project `COLLISION_DESIGN.md`, `MAXWELL_MOMENT_CHECK.md` and
  `HIGH_N_COLLISION_OUTCOME.md`: isotropic first-two-moment Gaussian truncation
  fails Maxwell fourth-moment equilibrium, and the old physical halo rate
  refinement remains unresolved. Neither result is reused as a passing control.

## Reference operator

The domain is x in [0,2pi), velocities in R^3, and
`U=-epsilon*cos(x-phi(t))`, `phi=omega0*t+sweep*t^2/2`.
Mass per particle is 2pi/N, so the uniform mean mass density is one.
The spatial cells provide a recorded finite DSMC approximation. Cells sample
uniform random disjoint unordered pairs. Exact compensation for their
selection probability preserves the intended mean rate over all pairs;
odd occupancy leaves one uniformly selected particle unpaired.

Each accepted event rotates the relative velocity, keeping its magnitude and
pair center velocity fixed. Compare isotropic outgoing directions with fixed
small angles delta=.2,.1 radians and uniform azimuth. These are reversible
positive angular kernels, velocity-independent viscosity cross-section
`sigma_V/m=kappa=.02`; total cross-sections are kappa/(2/3) and
kappa/sin(delta)^2. Particle labels are numerical; the identical-particle
symmetrized kernel has the same even-angular and one-particle transport.

For an angular harmonic l, pair-direction eigenvalue is
`rho |u| sigma_tot [1-P_l(cos delta)]`. Isotropic nonzero l has eigenvalue
`rho |u| sigma_tot`. All selected laws match l=2 exactly, because
`1-P_2(cos delta)=3 sin(delta)^2/2`. In the small-angle limit the l=4 value
divided by rho|u|kappa approaches 5. This reference preserves Maxwell
equilibrium; a moment-truncated isotropic Gaussian does not.

## Frozen checks and pilot matrix

1. Operator, 262144 independent Maxwell pairs, seed260100: pair conservation
   <1e-12 absolute, sampled angular sin-squared mean within .003, l=2 matching
   <1e-10, delta=.05 l=4 within .3% of its derived small-angle limit.
2. Evolution seeds260101–260104, with identical initial arrays per seed.
   Equilibrium: N=8192, cells32, duration20. Stress relaxation:
   N=32768, cells32, duration30; initial variances(1.6,.7,.7).
   Compare delta0,.2,.1; dt=.01 for delta0/.2, .0025 for delta.1.
   Maximum accepted-candidate probability <.1; collision energy/momentum
   relative residual <1e-10. Require equilibrium total rate within5% of
   Maxwell reference `Gamma=kappa*4/sqrt(pi)/angular_weight` and Maxwell
   second/fourth moments within5 analytical sampling SE. Match the entire
   measured normalized stress decay using paired seed intervals inside ±.05
   of initial stress; also report differences relative to the actual decay.
3. Resonance: N=8192,cells32,epsilon=.25,omega0=.5,sweep=.025,duration40,
   same seeds and laws. Include collisionless kappa0 controls. Record signed
   forcing impulse, external work, instantaneous separatrix population,
   event kick scale q and Ncoll per libration. Half-width=2sqrt(epsilon),
   libration period=2pi/sqrt(epsilon). The instantaneous separatrix fraction
   is a diagnostic, not a proof of finite-time trapping.
4. A candidate difference must exceed both its paired-seed uncertainty and
   selected timestep/cell refinement before interpretation. Refine dt/2 and
   cells64 for all four seeds for delta0/.2. The .2→.1 comparison is itself
   the bounded small-angle convergence check. No Gaussian surrogate is fitted.
   A resolved candidate may receive a held-out epsilon=.16,sweep=.04 forcing
   after the above controls. No live halo production follows from this screen.

Use nominal95% Student-t paired-seed intervals with four independent seeds;
do not mistake particle counts for independent realizations. Within this
exploratory multiple-outcome screen, intervals select follow-up, not discovery.
The same pass tolerances apply to every seed/law. Do not erase a failure or
silently retune cross-sections to obtain a difference.

Actual per-job CPU/wall costs, PIDs, dates, hashes and raw states are archived
under results/discovery-20261001/scattering. One nice10 single-thread worker;
combined initial scattering/inertia cap is2 core-hours.

## Control-driven advancement, frozen before forcing outcomes

The complete original control matrix is retained. Maxwell, rate and conservation
gates pass for every law. Delta=.1 stress-history intervals fit the ±.05
margin; delta=.2 has one endpoint at .05736, so its ordinary-relaxation
equivalence is unresolved. The global control flag remains false.
The scientifically qualified forcing comparison is therefore delta=.1 versus
isotropic. Delta=.2 remains a diagnostic of approach to the small-angle limit.
Selected timestep and cell refinement shifts from delta=.2 to delta=.1 before
any forcing outcome is inspected; all physical parameters and margins stay
fixed. Delta=.1 refinement uses dt=.00125 and cells64 with dt=.0025.

The q diagnostic will additionally report an exchange-invariant velocity kick:
assign the outgoing pair velocities to the nearest incoming velocities, then
measure the x component of that kick. A backward event can exchange the labels
of identical particles; a labelled action jump alone is not a physical
distinguishing statistic. This additional diagnostic does not change any
collision event, history, parameter or control result.

## Independent conditions, frozen before their outcomes

Following the resolved original impulse contrast, keep q/force-law choices
fixed. The waveform holdout uses epsilon=.16,sweep=.04,kappa=.02 and fresh
seeds260211–260214. The independent transport condition uses kappa=.01 with
the original waveform and fresh seeds260201–260204. That transport condition
receives the full original Maxwell and stress control matrix and the same
pass margins. Any law whose controls fail remains unqualified. Selected
delta=.1/isotropic timestep and cell refinement applies to the transport
condition too if a resolved signal remains. No candidate parameters are fit
to either condition.

The nominal95% stress intervals are pointwise across recorded times, not
simultaneous confidence bands. Four seeds qualify an exploratory comparison;
they do not provide a discovery significance threshold. The near-separatrix
population remains an instantaneous diagnostic.
