# Warm radial primitive and physical second-moment bound

Analytical derivation2026-10-01, prepared for independent root scrutiny.
This concerns the exact stationary warm target and exact Hamiltonian pulse.
It is not a numerical tail certificate for a fixed-step or tabulated action
implementation. No physical trajectory experiment is authorized here.

## Target, support and finite primitive integral

At each conservedL>0 use radial canonical measure dr dp, r>0,
E=p²/2+Phi(r)+L²/(2r²), with minimumEc(L)<0. Define
J(E,L)=pi^-1 integral_rp^ra sqrt[2(E−Veff)]dr andOmega=dE/dJ>0.
The physical conditional DF is g_L(E)=exp(−J/Js)/(2piJs) forEc<=E<0,
and zero atE>=0. It is normalized because dr dp=dJ dtheta,
theta-volume2pi. It decreases withE. Physical energies belowEc do not
exist at fixedL; that point is not an omitted phase-space support interval.

Set F_L(E)=−integral_E^0 g_L(e)de onEc<=E<0, andF_L=0 outside the
bound support. The conditional primitive has finite integral in full radial
phase space without any frequency supremum assumption:

integral |F_L| dr dp
= Js^-1 integral_0^infinity J exp(−J/Js) Omega(J,L)dJ
<= |Ec(L)|/e.

The equality follows by changing to actions and exchanging the two positive
integrals. The inequality uses (J/Js)exp(−J/Js)<=1/e and
integralOmega dJ=0−Ec. Therefore volume preservation gives
integral[F_L(E_M)−F_L(E)]dr dp=0 for a globally defined canonical mapM.
Splitting initial bound and unbound support yields the exact forward response
remainder plus inverse E>=0 capture term already specified. No capture term
is inferred absent from a finite sample. g is continuous to zero at escape;
there is no escape seam atom. The isolated circular phase point causes no
extra support term because a physical map at fixedL cannot attainE<Ec.

## A global action-energy comparison

For the actual potential, Phi(r)−Phi0<=A r globally with conservativeA=2.
The Hernquist radial force is<=1. Each interior finite gas component has
maximum radial force .05/n_s times2/(3sqrt3 s²), where
n_s=8³/(64+s²)^(3/2), s=.2 or1.3; their sum plus1 is below2.
The exterior force beyond8 is also below2. Integrating the force from0
establishes the inequality, including the spatial cutoff.

Compare at fixedL to the confining linear potentialAr, shifted to the same
Phi0. Pointwise Hamiltonian ordering implies action ordering at a fixed
energy abovePhi0: J_actual(delta,L)>=J_linear(delta,L). Consequently
delta_actual(J,L)<=delta_linear(J,L). The comparison is well-defined
although the real potential has a finite escape energy and the confining
comparison does not.

For a linear-potential energydelta with delta³>=32A²L², take the radial
interval[delta/(4A),delta/(2A)]. Throughout it,Ar<=delta/2 and
L²/(2r²)<=8A²L²/delta²<=delta/4, so radial momentum>=sqrt(delta/2).
Hence J_linear>=delta^(3/2)/(4sqrt2 pi A). Below that threshold,
delta<32^(1/3)A^(2/3)L^(2/3). Both cases imply

delta_actual(J,L)<=C A^(2/3)(J+L)^(2/3),
C=(4sqrt2 pi)^(2/3).

No circular coefficient or frequency distribution was fitted. The bound
uses a deliberately conservative force ceiling and covers all eccentricities.

## Primitive maximum at small angular momentum

Integrating by parts in action gives

Fmax(L)=−F_L(Ec)
= [1/(2piJs²)] integral_0^infinity
exp(−J/Js)[E(J,L)−Ec(L)]dJ.

The boundary terms vanish: E−Ec=0 atJ=0, and the exponential at infinity.
Using E−Ec<=E−Phi0=delta and (J+L)^(2/3)<=J^(2/3)+L^(2/3),

Fmax(L)<=[C A^(2/3)/(2piJs)]
[L^(2/3)+Gamma(5/3)Js^(2/3)].

At the Hernquist center the gas is smooth, Phi−Phi0=r+O(r²),
L~Rc^(3/2), kappa~sqrt(3/Rc), and
Js=(eta vc)²/kappa~eta²L/sqrt3, eta=.1. Therefore Fmax=O(L^(−1/3)).
This argument avoids assuming or numerically fitting sup_J Omega_r.
The exact identity integral g_L² dr dp=1/(4piJs) remains available.

## Physical compact support and importance sampling

The redistribution potentialPsi is exactly zero outside8. An initially
bound orbit can first enter that region only if
L<=Lcut=8sqrt[−2Phi(8)], because it has not encountered forcing before
that first crossing and its static energy is still<0. L remains conserved
after entry. Stable circular angular momenta increase withRc in this actual
potential, so the potentially affected guiding radii have a finite upper bound.

Let B=max|Psi|, m=max|a| andW=B integral_0^T |a'|dt. At any intermediate
time, static energy is<=W+mB for initially bound forward or inverse states.
Thus speed<=vmax=sqrt[2(W+mB−Phi0)]. Any affected initial radius is<=
8+T vmax, and its endpoint is<=8+2T vmax. Radial momenta are bounded by
vmax. These inequalities also cover the inverse-map support term.

The conditional proposal mixture has q_L>=.5q_tail,
q_tail=(1+Rc)/[(r−rmin+1+Rc)² 2sqrt(−2Veff)]. On this compact affected
initial bound region it has a uniform positive floor because1+Rc>=1,
Rc andr are bounded, andsqrt(−2Veff)<=sqrt(−2Phi0). The guiding proposal
includes .5 of the physical guiding density, so p_Rc²/q_Rc<=2p_Rc.
These bounds are statements about the exact proposal and physical flow,
not about its computed floating-point endpoints.

Write the conditional positive operandA_L as the forward concavity
remainder plus inverse capture. It is zero on states unaffected by the pulse,
where the exact static flow conserves energy. On affected states it is bounded
by sums of |F_L(E_M)|,2|F_L(E)| andg_L(E)|DeltaE|. Volume preservation,
the finite phase-region volume,|DeltaE|<=W and the proposal floor bound the
conditional second moment by constants times

Fmax(L)² + W²/(4piJs).

At smallL, the physical guiding density pushed toL is p_L~L^(1/3).
The full weighted second-moment integral therefore has only integrable
central powers L^(−1/3) andL^(−2/3). Away fromL=0 the affected interval
is compact and the same quantities are finite. Fixed coeval guiding-cohort
normalization changes only a finite constant. This gives a route to finite
variance of the exact physical forward estimator without discarding lowL,
rare capture paths or high-action proposal states.

## What this does not establish

Finite variance is not a quantitative standard-error forecast or empirical
coverage guarantee. It does not make512 states sufficient. The comparison
bound does not certify arbitrary-small-radius KDK physical accuracy; numerical
energy changes in the nominally unaffected region are outside the compact
physical-response proof. A numerically evaluated Jr changes the implemented
DF unless its approximation errors are controlled. Forward/inverse canonical
identities alone establish the numerical-map response, not accuracy to the
continuous pulse. Those distinctions remain mandatory in the proposed pilot.
