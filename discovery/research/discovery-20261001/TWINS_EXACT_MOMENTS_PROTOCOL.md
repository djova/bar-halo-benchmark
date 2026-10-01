# Analytic zero-streaming halo twins: preflight protocol

Frozen before any forced contraction of this family. This is an unforced
analytic/numerical preflight, not a replacement for a failed historical gate.
No bar response, torque vector or orbit history is used to select its parameters.

Use the self-consistent unsoftened spherical isochrone with G=M=1 and b=0.5,
relative potential Ψ=1/[b+sqrt(b²+r²)], binding energy e=Ψ−v²/2 in (0,1),
and its exact isotropic distribution function F₀(e). For each **fixed**
p∈{4,6,8}, define

\[
\delta F_p=L_z\left[g_{0,p}(e)+L^2 e^p\right],\qquad
g_{0,p}(e)=-\frac{4p\,e^{p-1}}{(p+5/2)(p+7/2)}
             +\frac{8b\,e^p}{p+7/2}.
\]

The proposed populations are F±=F₀±αₚδFₚ. The preflight must independently
derive the velocity-angular integrals and verify that each local mean velocity
vanishes at every radius and inclination. Density and even velocity moments
should agree by parity, but that statement must follow from the actual formula.
It must also verify the isochrone density expansion, Eddington coefficients,
escape and central limits, numerical density recovery, and comparison with the
existing AGAMA reference DF.

## Normalization fixed without a forced outcome

Choose αₚ so that |αₚδFₚ/F₀|≤0.5 **globally**, rather than normalizing to the
maximum of a finite sampled orbit library. The positivity construction uses
the first 13 positive terms of the exact F₀ power series as a lower bound.
After e∈[0,1] and t=L/Lmax(e)∈[0,1] replace the orbital domain, bound the
ratio by exact rational tensor-product Bernstein coefficients. Four uniform
dyadic subdivisions in each variable are fixed in advance. The resulting
rational upper coefficient Bₚ fixes

\[
\alpha_p=\frac{4}{5\pi^3 B_p}.
\]

No response-dependent adjustment of this conservative normalization is allowed.
The full numerical DF uses 96 positive series terms; its tail bound and an
independent numerical Eddington inversion are recorded. An ordinary numerical
maximum is diagnostic only and cannot replace the all-domain positivity bound.

## Numerical checks and evidence

- Numerical Eddington inversion: nonsingular substitution with 64 and 128
  Gauss–Legendre nodes over a fixed binding-energy grid, including both tails.
- Density recovery: independent Gauss–Jacobi speed integrals, orders 32 and 64.
- Local moment integrals: radial points 0.01, 0.1, 0.3, 1, 3, 10, 30 and 100,
  inclinations |z|/r=0, 0.5, 0.9 and 0.999; velocity orders 12 and 24.
  Report density, all three first moments and all six second-tensor components.
- A third azimuthal moment is recorded only as an unforced diagnostic of hidden
  higher velocity structure; it does not select a population.
- Compare the exact DF to the pinned AGAMA implementation on a fixed energy/
  angular-momentum grid. Approximation differences are reported, not hidden.
- No particle sampling, orbit integration, live stability test or bar evolution.

Use one numerical thread, nice=10, at most 180 CPU seconds. Preserve this protocol,
executed source, exact rational positivity operands, numerical values, code/library
hashes and terminal state in a new immutable output directory. The root reviews
the derivation and preflight before any forced contraction or further evolution.

An exact F(E,L,Lz) with the matching density is a stationary solution of the
unsoftened spherical collisionless model. This establishes neither collective
stability nor equilibrium under a softened or disk-containing evolution force.
There is no novelty, live-galaxy or observational claim at this stage.
