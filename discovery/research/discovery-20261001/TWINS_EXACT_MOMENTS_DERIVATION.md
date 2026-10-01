# Positive halo populations with identical local density and streaming

There is an analytic way to remove the finite-position streaming mismatch in
the first twin search. In the unsoftened spherical isochrone, three fixed odd
DF perturbations preserve density, every local mean velocity and every even
velocity moment. An independent positive-series normalization keeps both
populations nonnegative over the complete orbital domain. This is an initial-
equilibrium construction, not evidence that its bar response differs or that
it is collectively stable.

The unforced preflight uses p=4,6,8, chosen before any forced contraction. Its
[protocol](TWINS_EXACT_MOMENTS_PROTOCOL.md), source and exact rational operands
are preserved. No force history or optimized torque enters this construction.

## Deriving the local streaming cancellation

For G=M=1 and b=1/2, let

\[
\Psi(r)=\frac{1}{b+\sqrt{b^2+r^2}},\qquad
e=\Psi-\frac{v^2}{2},\qquad
r^2=\Psi^{-2}-2b\Psi^{-1}.
\]

The bound orbital domain has 0<e<1, 0≤L≤Lmax(e), |Lz|≤L, where

\[
L_{\max}(e)=\frac{1-e}{\sqrt{2e}}.
\]

Consider δF=Lz[g₀(e)+L²eᵖ]. At a fixed position with cylindrical radius
R=r sinθ, Lz=R vφ and L²=r²(vθ²+vφ²). Integrating directions in velocity space
gives ∫vφ² dΩ=4πv²/3 and
∫vφ²(vθ²+vφ²)dΩ=16πv⁴/15. With e=Ψ−v²/2, the remaining speed integrals are

\[
\int v_\phi\delta F\,d^3v
=R C_0\left[
\int_0^\Psi g_0(e)(\Psi-e)^{3/2}\,de
 +\frac85 r^2\int_0^\Psi e^p(\Psi-e)^{5/2}\,de\right],
\quad C_0=\frac{8\sqrt2\pi}{3}.
\]

The second coefficient is C₁=64√2π/15, so C₁/C₀=8/5. Write
g₀=−Aₚeᵖ⁻¹+Bₚeᵖ for this derivation only. Using the Beta integral and the
isochrone r² identity leaves two powers of Ψ. Their coefficients vanish when

\[
A_p=\frac85\frac{\mathrm B(p+1,7/2)}{\mathrm B(p,5/2)}
   =\frac{4p}{(p+5/2)(p+7/2)},\qquad
B_p=\frac{16b}{5}\frac{\mathrm B(p+1,7/2)}{\mathrm B(p+1,5/2)}
   =\frac{8b}{p+7/2}.
\]

Thus the azimuthal first moment is zero at **every** radius and inclination,
including the symmetry-axis limit R=0. Radial and polar first moments vanish
by velocity parity. This cancellation does not rely on a grid or a sampled
global-spin constraint.

Under complete velocity reversal δF is odd while the reference F₀ is even.
Hence density and all raw even moments agree for F±=F₀±αδF. Both local means
are zero, so all centered even moments agree as well. Higher odd moments can
differ; the preflight records the azimuthal third moment as a diagnostic.
Zero mean streaming is therefore not equality of the full velocity distribution.

## Independently recovering the reference distribution

Poisson's equation for the isochrone yields

\[
\rho(\Psi)=\frac{b(2-b\Psi)\Psi^4}{4\pi(1-b\Psi)^3}
=\frac{b}{8\pi}\sum_{n=0}^\infty(n+1)(n+4)b^n\Psi^{n+4}.
\]

All coefficients are positive and bΨ≤1/2. Eddington inversion has no boundary
term because ρ′(0)=0, and gives

\[
F_0(e)=\frac{1}{\sqrt8\pi^2}
\sum_{n=0}^\infty c_n(n+4)(n+3)
\mathrm B(n+3,1/2)e^{n+5/2},\qquad
c_n=\frac{b}{8\pi}(n+1)(n+4)b^n.
\]

Factor F₀=a₀e⁵ᐟ² S(e), where a₀=16b/(5√2π³), S(e)=Σsₙeⁿ, s₀=1. At b=1/2,

\[
\frac{s_{n+1}}{s_n}
=\frac{(n+2)(n+5)^2}{(n+1)(n+4)(2n+7)}.
\]

These rational coefficients provide a second implementation of the direct
Beta expression. For n≥6 this ratio is at most 3/4: multiplication by positive
denominators reduces the condition to
2n³+3n²−51n−116≥0. It is positive at n=6 and increasing thereafter. The tail
after the 96 numerical terms is therefore bounded by the next term divided
by 1−3e/4. This mathematical series-tail bound does not include floating-point
evaluation error.

The preflight also evaluates Eddington's integral directly from the rational
ρ″(Ψ), using Ψ=e(1−u²) to remove its endpoint singularity. It separately
integrates F₀ back to density with Gauss–Jacobi quadrature. Neither calculation
uses the fitted AGAMA DF. Maximum relative disagreements are 3.0×10⁻¹⁵ for
Eddington inversion and 8.9×10⁻¹⁶ for density recovery on the fixed test grids.

## A global positivity bound rather than a sampled maximum

Set t=L/Lmax(e) in [0,1]. Since the largest |Lz| is L,

\[
\frac{|\delta F|}{F_0}
\le\frac{|H_p(e,t)|}{\sqrt2a_0 S(e)},\qquad
H_p=e^{p-4}(1-e)t\left[-A_p+B_pe+\tfrac12(1-e)^2t^2\right].
\]

The finite escape limit requires p≥4; the central limit vanishes because
Lmax→0 while F₀(1)>0. The actual maximization over L also has only two relevant
candidates: Lmax, or L=√[−g₀/(3eᵖ)] when g₀<0 and the latter lies inside the
orbital domain. These extrema are used for an ordinary numerical diagnostic,
but not for the positivity proof.

Instead retain S₁₂, the first 13 positive terms, so S≥S₁₂ everywhere. Express
Hₚ and S₁₂ in a common tensor-product Bernstein basis of degrees 12 and 3 on
[0,1]². Four dyadic subdivisions in each coordinate give 256 closed boxes.
All denominator coefficients dᵢⱼ remain positive. The ratio is a convex
combination of coefficient ratios hᵢⱼ/dᵢⱼ with positive weights proportional
to dᵢⱼ times their Bernstein basis functions. Consequently

\[
\frac{|H_p|}{S_{12}}\le
\mathcal B_p:=\max_{\text{boxes},i,j}\frac{|h_{ij}|}{d_{ij}}.
\]

All coefficients and subdivisions are computed with exact rational arithmetic.
This is an all-domain algebraic bound, unlike a numerical grid maximum. Choosing

\[
\alpha_p=\frac{4}{5\pi^3\mathcal B_p}
\]

then gives |αₚδF/F₀|≤1/2 and F±≥F₀/2. The formal normalization uses this exact
expression; reported decimal values are floating evaluations. This analytic
positivity statement is separate from the earlier training LP's floating-point
dual calculation, which was explicitly not an interval-arithmetic certificate.

| p | αₚ | Global ratio bound | Numerical max normalized multiplier |
| ---: | ---: | ---: | ---: |
| 4 | 0.15018625 | 3.32919958 | 0.50000000 |
| 6 | 9.87892469 | 0.05061280 | 0.49932450 |
| 8 | 63.05040501 | 0.00793016 | 0.49823589 |

For p=4, the exact rational 𝔅₄ is 67/390; its maximum is the escape/circular
limit, rather than a finite central orbit. The other exact rational bounds are
recorded in the preflight. They exceed the independent numerical maxima and
are never adjusted using a forced response.

## What is established, and what remains open

At 32 fixed positions, two velocity quadrature orders give maximum
first-moment differences 1.46×10⁻¹⁵ of reference RMS. Density and all second-
tensor differences are below 6.73×10⁻¹⁸ and 3.29×10⁻¹⁷ respectively. These
checks support the analytic identities; finite-grid checks alone would not
establish the all-position result.

[An independent internal challenge](TWINS_EXACT_MOMENTS_CHALLENGE.md) rebuilt
the Beta coefficients and DF recurrence from exact factorial expressions, and
rebuilt every positivity box by affine power substitution instead of the
original de Casteljau code. It reproduced the three rational bounds exactly.
That supports the derivation without constituting outside scientific review
or a test of collective stability.

F(E,L,Lz) is constant along orbits in the unsoftened spherical model, and its
unchanged density generates the same isochrone potential. The construction is
therefore stationary and self-consistent at that model level. It does not prove
collective stability, represent a softened live equilibrium, or survive adding
a self-gravitating stellar disk. Nor does it establish different torques,
formation-history reachability or novelty.

The pinned AGAMA reference differs from the exact DF by at most 3.24×10⁻⁶ on
the fixed energy/angular-momentum grid. A future contraction using AGAMA-drawn
particles must recover the analytic target by importance weights F±/Fq,
where Fq is the sampling DF. Using 1±αδF/F₀ on unchanged Fq weights would
instead define a slightly different population. Absolute mass normalization
must remain shared; matching each sample to unit mass would alter the experiment.

## Preserved evidence

The archived preflight record is identified as
`twins/exact-moments-preflight-02/result.json` in the
[scientific export](../../data/twins-exact.json). The fixed normalized
populations and exact rational operands are supplied as
[frozen-populations.json](../../operands/exact-twins/frozen-populations.json).
The [portable internal algebra challenge](../../scripts/discovery/twins_proof_challenge.py)
checks those operands without AGAMA; the original preflight source in
[source-snapshots](../../source-snapshots/README.md) imports AGAMA and is an
inspection record, not a standalone public reproduction command. The preceding
serialization failure and full historical grids are retained in the archive,
rather than supplied as additional runs in this compact package.
