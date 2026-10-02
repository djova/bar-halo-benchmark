# An admissible halo is not yet a formation history

1 October 2026. Analytical scope assessment; no new trajectories or observations.

The exact-moment construction demonstrates that present density and ordinary
velocity moments need not determine a halo's response to a prescribed bar.
It does not show how that halo formed. In particular, a collisionless
disturbance cannot turn the exact smooth reference distribution into either
of our exact constructed twins. This follows from a known phase-space
conservation law, rather than from a failed numerical search.

Write the construction as

$$
F_\pm=F_0\pm\alpha\,\delta F,
$$

where $F_0$ depends on energy, $\delta F$ is odd in $L_z$, and $\alpha\ne0$.
The [construction and positivity certificate](TWINS_EXACT_MOMENTS_DERIVATION.md)
give $F_\pm\ge F_0/2$. Integrating over the full phase space, with
$d\Gamma=d^3x\,d^3v$, velocity reversal makes the cross term vanish:

$$
\int F_0\,\delta F\,d\Gamma=0.
$$

Consequently the quadratic phase-space functional is

$$
\mathcal C_2[F_\pm]
\equiv\int F_\pm^2\,d\Gamma
=\mathcal C_2[F_0]
+\alpha^2\int(\delta F)^2\,d\Gamma
>\mathcal C_2[F_0].
$$

These integrals are finite for the constructed isochrone populations: the
reference distribution is bounded and has finite mass, and the certified
bound $|\alpha\delta F|\le F_0/2$ controls the perturbation's square. The
last inequality is strict because the perturbation is nonzero on a set of
nonzero phase-space volume.

A smooth collisionless Hamiltonian evolution transports the fine-grained
distribution while preserving phase-space volume. It therefore preserves
$\mathcal C_2$, including when the external potential depends on time. This
rules out an exact transition from that fine-grained $F_0$ to either exact
$F_\pm$. Ordinary positive averaging that preserves mass and phase-space
volume cannot solve the problem: Jensen's inequality makes this convex
functional decrease under such mixing. This is an application of the
established collisionless mixing restrictions discussed by
[Tremaine, Hénon & Lynden-Bell (1986)](https://doi.org/10.1093/mnras/219.2.285)
and [Dehnen (2005)](https://arxiv.org/abs/astro-ph/0504246).

The restriction concerns the specified initial distribution. It does not
exclude formation from another progenitor, a reference halo with unresolved
fine-grained structure, or an approximately matched final population. Empirical
particle delta functions are also not the smooth distributions in this proof.
This is not an exclusion of cosmological halo formation.

The two twins have identical distribution-value spectra under velocity
reversal, and hence identical Casimirs to each other. In the spherical
construction, a proper half-turn about an axis in the equatorial plane also
flips $L_z$ while preserving energy and $L^2$. Acting on both positions and
velocities, this rotation exchanges the two distributions.
This removes the particular Casimir obstruction between them; it supplies
neither a demonstrated encounter history nor a way to rotate the halo while
preserving a disk and its environment.

The useful next formation test must start from a physically specified
progenitor and evolve an allowed perturbation. It should measure the resulting
population and bulk-profile changes, then freeze the population before testing
a new bar history. Matching present moments, stationarity in the construction
potential, stability under self-gravity, and reachability from a progenitor are
four different requirements. None can substitute for the others.
