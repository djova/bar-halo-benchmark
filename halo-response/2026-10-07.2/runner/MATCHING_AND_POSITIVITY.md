# Exact initial matching and a full-support positivity certificate

**Release binding remains pending.** The publisher must supply the clean
`certificate.json`, execute `verify_certificate.py` under the campaign meter,
and bind its closed readback before publishing this folder. This note states
the analytic theorem and the verification contract; it does not invent a
published proof, numerical readback or response benchmark.

Use G=M=a=1, psi=(1+r²)^(-1/2), H0=v²/2-psi, e=-H0, Q=14/33 and
C=24sqrt2/(7pi³). The positive physical bar monopole has mass .1; the halo
has density 3psi^5/(4pi)-15Mb psi^7/(8pi) and mass .9. Their spherical
potentials sum to unit Plummer. The fixed source's physical quadrupole and
positive total density are given in README.md; the signed quadrupole density
alone is not a separately nonnegative source.

On bound support define

    F_c=C[g(e)+Lz sum_p c_p h_p(e,L²)],  g=e^(7/2)(1-Qe²),
    h_p=-a_p e^(p-1)+b_p e^(p+1)+L²e^p,
    a_p=4p/[(p+5/2)(p+7/2)], b_p=4/(p+1),
    p=5,6,7,8,10,12.

Set F_c=0 on unbound support. The endpoint/boundary limits below belong to
the same physical distribution; they are not cutoffs. All coefficients in
this release denote their actual binary64 rational values, not exact decimal
numbers or an ideal LP optimum.

## Stationarity, density, current and the complete even DF

Every F_c depends on the spherical invariants H0,L²,Lz and is stationary in
the common H0. The odd term changes sign under complete velocity reversal,
so its density and every even velocity test integral vanish. More strongly,

    [F_c(x,v)+F_c(x,-v)]/2=F0(x,v)

pointwise, not merely after a finite list of moment contractions. Positivity
and stationarity alone do not establish linear or nonlinear stability.

The current null is independent of that reversal statement. At fixed x let
t=z_hat cross x, so Lz=t dot v. Angular isotropy of the speed-dependent
pieces and t dot x=0 give the contribution of one basis term:

    j_p/C=t{(4pi/3)[-a_p M_(4,p-1)+b_p M_(4,p+1)]
                 +(16pi/15)r² M_(6,p)},
    M_(q,s)=integral_0^sqrt(2psi) v^q (psi-v²/2)^s dv
           =(2psi)^((q+1)/2) psi^s B((q+1)/2,s+1)/2.

Writing D_p=(p+5/2)(p+7/2), the exact beta-function recurrences give

    M_(4,p+1)/M_(4,p-1)=psi² p(p+1)/D_p,
    M_(6,p)/M_(4,p-1)=5p psi²/D_p.

Consequently the current bracket divided by (4pi/3)M_(4,p-1) is

    (4p/D_p)[-1+psi²(1+r²)]=0.

Thus every basis member, every finite mixture and both signs have exactly
zero first velocity moment at every position. Initial density, pointwise
zero current and the entire reversal-even DF all match F0. These statements
concern the initial equilibrium. A drive can generate later currents and
change the distribution. The initial condition is not claimed to be obtainable
from F0 by an infinitesimal canonical rearrangement with the same Casimirs.

## A sufficient inequality on all bound support

Parameterize circular energy and arbitrary allowed angular momentum by

    e=u(1+u²)/2, L=t(1-u²)/sqrt(u), Lz=mu L,
    0<=u,t<=1, -1<=mu<=1.

Here u is the circular-orbit potential coordinate for the chosen e, not the
instantaneous particle potential psi(x). Interpret u=0 by its limit. This
closed parameter square includes arbitrarily weak binding, every radial and
circular limit and both extreme inclinations. Define exact rational polynomials

    D(u)=1-Q u²(1+u²)²/4,
    H_p=u^(p-5)(1-u²)(1+u²)^(p-4)t/2^(p-4)
        *[-a_p+b_p u²(1+u²)²/4
          +t²(1-u²)²(1+u²)/2],
    H_c=sum c_p H_p.

Direct substitution yields

    [F_c-F0]/F0=mu sqrt2 H_c/[sqrt(1+u²)D].

D is positive throughout: D>=1-Q=19/33. Since sqrt2<99/70 and
sqrt(1+u²)>=1, the single sufficient condition

    |H_c(u,t)| <= (35/99)D(u)

proves F0/2<=F_c<=3F0/2 on the full physical bound support. This condition
is conservative. It does not characterize every positive six-power mixture
or place a rigorous bound on the measured physical response.

## Exact Bernstein proof and public regeneration

All H_p fit common tensor Bernstein degree (31,3); D fits degree31 in u and
degree0 in t. Dyadic subdivision of the complete u/t intervals produces the
closed patches recorded in certificate.json. On every patch the Bernstein
basis functions are nonnegative and sum to one. Therefore all coefficient
inequalities

    |sum_p c_p H_(p,ij)| <= (35/99)D_i

prove the pointwise inequality between all grid points and at the patch
edges. Positive D coefficients follow already from degree elevation of its
constant and negative power terms; exact half subdivision preserves them
by convex averaging. The original optimizer may remove identical absolute
rows, but the public verifier removes none: it checks every raw patch/index.
It regenerates the combined polynomials for the two actual vectors, rather
than trusting a scalar maximum or an opaque constraint digest.

The clean certificate binds exact Q, powers, degree/subdivision, positive
denominator minimum, full-A and separately represented .9 coefficient
rationals, their closed exact maximum constraint ratios and normalized slack.
It identifies the closed original primal result/receipt digests and the
reviewed method ancestors without private host paths or copied trajectory
archives. Those origin hashes document provenance; the independent regenerated
inequalities supply the positivity check.

The verifier uses only Python's standard library and exact Fraction arithmetic:

```sh
python verify_certificate.py --output positivity-verification.json
```

It first hash-checks the actual runner, frozen README/requirements, theorem and
verifier. It reads the two runner coefficient tuples through literal AST parsing
without importing the numerical runner. It constructs the analytic H/D power
polynomials, elevates their Bernstein degrees and subdivides every patch.
Every denominator must be strictly positive; every exact maximum must be <=1
and equal its closed certificate operand. An incomplete/resource-limited run
fails. No positivity grid, LP solver or numerical scientific package is used.
Execution is still computational work and remains owner-metered before release.

The negative full-A population follows by exact central symmetry of the
absolute inequalities. Binary halving is exact for these finite normal
constants, so half-A follows by uniform contraction. F0 is the exact zero
odd vector. The actual rounded .9 tuple requires and receives a separate
primal check; it is not treated as an exact directional scaling of A.

This proves the positivity of the declared analytic DFs with their exact
represented coefficient constants. Ordinary floating evaluation can suffer
cancellation error, and still needs its own arithmetic challenge. This note
does not prove stability, response convergence, self-gravitating activity,
autonomous rotor acceleration, realistic formation or observational relevance.
The central bare complete-cycle claim requires the separately bound numerical
work readbacks. [Nelson & Tremaine (1995)](https://arxiv.org/pdf/astro-ph/9408068)
already provide nonrotating halo energy emission when the even DF changes;
the additional controlled question here is exact initial matching.
