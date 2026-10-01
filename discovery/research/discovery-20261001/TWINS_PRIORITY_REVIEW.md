# Priority review: analytic halo twins with zero local streaming

2026-10-01. Literature assessment, prepared before examining any forced
response of the proposed family. No simulations were run for this review.

The construction offers a useful **stronger control**, but neither odd-DF
reweighting nor the dependence of bar response on orbital populations is new.
The potentially distinctive feature is a smooth three-integral perturbation
whose *entire local first-velocity-moment field vanishes*, while its odd higher
moments remain free. I found no exact published counterpart to this particular
isochrone formula in the sources checked. That is a search result, not a priority
claim.

## What is being compared

The preflight proposes, in the unsoftened spherical isochrone,

\[
F_\pm(e,L^2,L_z)=F_0(e)\pm\alpha_p L_z[g_{0,p}(e)+L^2e^p],
\qquad p\in\{4,6,8\},
\]

\[
g_{0,p}(e)=-\frac{4p\,e^{p-1}}{(p+5/2)(p+7/2)}
             +\frac{8b\,e^p}{p+7/2}.
\]

Density and velocity moments of even total degree are unchanged by parity under
\(\mathbf v\mapsto-\mathbf v\). The additional first-moment cancellation is
the substantive extra constraint; it must be verified using the actual DF and
potential, rather than inferred from zero total angular momentum. The existing
[preflight protocol](TWINS_EXACT_MOMENTS_PROTOCOL.md) separately requires an
all-domain positivity bound. This memo does not certify that bound or audit its
execution.

## Closest primary predecessors

**Lynden-Bell (1960; 1962): the classical construction.**
[Can Spherical Clusters Rotate?](https://doi.org/10.1093/mnras/120.3.204)
establishes that spherical density does not force a nonrotating orbital
population. The later
[Stellar Dynamics: Exact Solution of the Self-Gravitation Equation](https://adsabs.harvard.edu/pdf/1962MNRAS.123..447L),
p. 448, explicitly adds an antisymmetric DF component without changing density:
“the general solution may be obtained by adding any antisymmetrical bit”.
These are direct predecessors of the parity argument, not evidence for our
extra zero-local-streaming cancellation. The latter paper is conventionally
cited as 1962; its current publisher metadata uses a 1961 issue date.

**Dejonghe (1987): fixed density and velocity dispersions need not fix the DF.**
[A completely analytical family of anisotropic Plummer models](https://adsabs.harvard.edu/pdf/1987MNRAS.224...13D),
Section 4, constructs distinct \(F(E,L)\) with the same density and spatial
dispersion profiles, using freedom in the augmented density off the physical
potential-radius relation. The abstract states that “a degeneracy in the model
space persists”. These populations are even in velocity, and their higher even
moments/line profiles can differ. Our proposed odd perturbation preserves *all*
even moments and instead varies higher odd structure. This is a more restrictive
comparison, not a discovery that low-order kinematics underdetermine the DF.

**Hunter & Qian (1993); van den Bosch & de Zeeuw (1996): do not confuse two-
and three-integral freedom.**
[Two-integral distribution functions for axisymmetric galaxies](https://doi.org/10.1093/mnras/262.2.401),
Section 5.1, gives an odd-part inversion from a specified rotational-velocity
field: “The contour integral method is useful for calculating the odd part”.
The primary PDF was read
from [ADS](https://articles.adsabs.harvard.edu/pdf/1993MNRAS.262..401H).
[Self-consistent, axisymmetric two-integral models of elliptical galaxies with embedded nuclear discs](https://arxiv.org/abs/astro-ph/9607035),
Section 4.2, explicitly writes the integral connecting \(\rho\langle
v_\phi\rangle\) to \(L_z f_o(E,L_z)\) and describes inversion when the complete
streaming field is supplied. Their counterrotating components do not impose
pointwise cancellation for the combined system. The proposed null direction
depends on \(L^2\), an additional integral; it must not be presented as a
counterexample to two-integral inversion.

**An & Evans (2005); Chatzopoulos et al. (2015): positive odd additions and
three-integral spherical-density systems are established.**
[Simple Models for the Distribution of Dark Matter](https://arxiv.org/abs/astro-ph/0508419),
Appendix B, permits an arbitrary bounded odd \(\xi(L_z)\) multiplying the even
DF, keeps density and second moments fixed, and calculates the resulting mean
rotation. Its interpretation is “switching the direction of rotations for a
certain fraction of stars”.
[The old nuclear star cluster in the Milky Way](https://arxiv.org/abs/1403.5266),
Section 3.3, explicitly uses \([1+g(L_z)]f(E,L^2)\): “the density of the system
is still rotationally invariant but f− is not”. Neither displayed family
supplies our particular nonzero odd perturbation with zero local streaming.
The distinction between spherical density and a rotationally invariant full DF
is therefore essential here.

**Athanassoula (2003): the bar-population premise is already explicit.**
[What determines the strength and the slowdown rate of bars?](https://arxiv.org/abs/astro-ph/0302519),
Sections 2.2 and 8, connects resonant angular-momentum exchange to the halo DF
and velocity dispersion. The conclusion also calls for exploring other DFs.
The text states that angular-momentum change “does not only depend on the
strength of the bar”. Matching density alone and observing a different response
would add little to that established result. Our stronger moment constraints
are the reason this particular control could be informative.

**Chiba & Kataria (2024): direct odd-DF/resonant-torque predecessor.**
[Origin of reduced dynamical friction by dark matter halos with net prograde rotation](https://arxiv.org/html/2311.07640v2),
Section 2, uses \(f=(1+g)f_+\), with bounded odd \(g(L,L_z)\), including a
smooth \(\tanh(\chi L_z/L)\) family. Section 3 explains torque through
action-space DF gradients; Sections 4.3–4.4 compare resonance calculations and
live simulations. Its mean rotation varies with the odd-part amplitude. This
is a close framework for interpreting a future response measurement, but does
not itself match zero local streaming across distinct nonzero odd DFs.

**Kataria & Shen (2024): fixed total spin already gives different live bars,
with an important zero-spin qualification.**
[Importance of Initial Condition on Bar Secular Evolution: Role of Halo Angular Momentum Distribution Discontinuity](https://arxiv.org/html/2406.17113v1),
Section II, holds \(\lambda=0.1\) across four distributions while their radial
retrograde fractions differ. Section IV states: “For the non-rotating halo
(λ=0), we find similar secular evolution irrespective of discontinuity.”
That negative zero-spin finding must be acknowledged. It is scoped to their
tested family, not a theorem covering all zero-spin DFs. Our proposed test
holds local streaming at zero everywhere and uses smooth functions, rather
than merely matching the integral defining total spin.

## Recommended claim boundary

Call the family **zero-streaming spherical-density halo models**, or define
“nonrotating” explicitly as vanishing local mean velocities. Their handed
higher-moment structure means that they are not velocity-reversal symmetric,
and the full DF need not be invariant under arbitrary spatial rotations.

Once the algebra and positivity preflight passes, the bounded construction
claim is: *Within this unsoftened isochrone potential, the analytic family
holds density, all even velocity moments and the full mean-velocity field
fixed while varying higher odd velocity structure.* This is a controlled
example within established DF methods; priority for the precise formula and
constraint combination remains open.

A later prescribed-bar measurement could establish a response degeneracy
under these strengthened controls. It would not yet establish different
live-galaxy evolution, a dynamically stable self-gravitating pair, a plausible
formation history, or an observationally invisible halo. Higher odd projected
velocity information could in principle distinguish the populations, but its
actual projection and observability require a calculation.

Keep collective stability separate. For example,
[Meza (2002)](https://arxiv.org/abs/astro-ph/0208565) finds stability for selected
velocity-reversed isotropic models, whereas
[Alimi, Perez & Serna (1999)](https://arxiv.org/abs/astro-ph/9903087) finds
stability depends on anisotropy and the construction used. Neither result
qualifies this new energy-/angular-momentum-dependent perturbation.

Recommendation: retain the experiment as a sharper diagnostic of hidden
phase-space structure, explicitly acknowledge these constructions and the
Kataria–Shen zero-spin result, and reserve novelty language for specialist
review. Do not advertise “same halo spin, different bar” or “the DF matters” as
the new contribution.

Reading scope: targeted primary-paper sections and abstracts, including full
texts of the closest construction/inversion and bar-response papers. Searches
also covered zero-streaming, counterrotation and velocity-skewness wording.
No exact match was located; the review is not an exhaustive priority proof and
does not examine any new forced-outcome files.
