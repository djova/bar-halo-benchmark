# A proposed variance reduction from the cumulative population

Derived during this campaign after inspecting the first positive moving
quadratures. This is a candidate numerical identity to verify before adoption,
not a novelty claim or a qualified physical result. It does not change the
physical population, imposed noise, sweep, duration or old acceptance criteria.

## Identity and restricted assumptions

Let x be the initial moving-frame action, B_t the accumulated **bar** impulse,
and W_t the prescribed additive action-noise impulse. The moving-frame equation
gives j_t = x + B_t - s t + W_t. Write y_t = j_t + s t - W_t = x+B_t.
Let F be an antiderivative of a positive, compactly supported physical weight w.
The initial resonant phase is uniform, and the external noise coefficient is
independent of phase, action and the population.

For a fixed Brownian realization applied to all initial points, Hamiltonian
shears, uniform drift and additive translations preserve phase-space area.
Subtracting the common translation to use (psi_t,y_t) also preserves area.
Since dy_t = -sin(psi_t) dt, there is no Ito correction in dF(y_t). Consequently,

    d/dt integral [F(x+B_t)-F(x)] dx dpsi0/(2pi)
      = integral w(y_t) [-sin(psi_t)] dy_t dpsi_t/(2pi) = 0.

It vanishes initially, hence the integral is zero at every prescribed time.
Expectation over Brownian paths preserves the identity. Independent Brownian
draws per Monte Carlo particle still estimate that same expectation; common
noise over initial phase space is a proof device, not a changed physical bath.
The argument needs the zero phase mean of the bar torque, not area preservation
alone: an arbitrary uniform action translation would not give the identity.
The positive-step angle/kick splitting has the same property: angle steps leave
B unchanged, and integrating each fixed-angle kick over y gives a displacement
times integral(w), whose phase average vanishes.

Define the nonlinear remainder

    R_w(x,B) = F(x+B)-F(x)-w(x) B.

Then the same physically weighted bar transfer can be estimated as

    integral w(x) E[B] dx = -integral E[R_w(x,B)] dx.

The noisy-minus-smooth contrast uses the difference of those remainders. It is
an alternative estimator of the original positive population, not a signed
physical distribution. For a locally affine weight, R = w' B^2/2, exposing why
a small gradient may be estimated much more accurately than by cancellation of
large positive and negative raw impulses. A globally affine density is not a
normalizable positive halo; this example is an algebraic limit, not a new input
population.

## Coverage is essential

If w vanishes outside [-c,c], then R vanishes outside [-c-T,c+T] because the bar
force has magnitude at most one and |B|<=T. The extra interval is needed even
where the physical starting density is zero. Sampling only [-c,c] would bias
the alternative estimator. For the wider cutoff64 and T20, use coverage at
least [-84,84], with a recorded buffer. The Brownian displacement does not enter
this support bound because it was subtracted explicitly from y. This argument
is exact for positive-step kicks; the fourth-order negative substep composition
requires its own larger bound or separate tail check.

This does not automatically apply to a live self-gravitating halo, a
population-dependent collision operator, action-dependent diffusion, an
arbitrary torque with action dependence, nonuniform initial angles, or a finite
absorbing/reflecting boundary. It is restricted to the stated local experiment.

## Required tests before adoption

1. Validate F and its derivative/increments against analytic compact profiles,
   explicit high-order quadrature, and mesh refinement. Numerical integration
   of the cumulative density must be much smaller than the 2e-4 response target.
2. Verify the zero integral of F(x+B)-F(x) for deterministic composed canonical
   maps and fixed externally prescribed kick histories, with enough action
   coverage. Preserve failures; do not use a forced halo answer to calibrate F.
3. Compare raw and remainder estimates with their paired covariance on fresh
   stochastic pilot samples covering the full required interval. Do not assume
   a variance improvement or treat their correlated estimates as independent.
4. Check known-limit and original forward/characteristic results, timestep,
   support and numerical quadrature. Freeze validation allocation and fresh
   seeds only after the pilot. The original pilot remains distinct.

The response may also be written as minus an integral of w' against a triangular
displacement kernel: R = B^2 integral_0^1 (1-u) w'(x+uB) du. This suggests a
smooth primitive of the requested action-response kernel, but that construction
and its derivative require separate tests. A stable integral is not evidence
that a noisy pointwise derivative is resolved. No universal curvature law or
priority claim follows from this derivation.
