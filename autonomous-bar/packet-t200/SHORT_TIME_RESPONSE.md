# Short-time density and torque of stationary twins

Derived 2 October 2026 without new numerical execution. For the continuum
stationary twins, a common sudden perturbation permits density contrast
first at t^5. A force ramp starting as t^3 permits it first at t^8, and
its accumulated bar torque first at t^12. These are structural lower
orders, not universal nonzero signals or forecasts. Finite libraries do
not satisfy the stationary local-moment premises and can respond earlier.

## Assumptions and first operator

Let G(x,v)=F_plus-F_minus be stationary in the common initial potential
Phi0. Define symmetric raw moment tensors

    M^(n)_{i1...in}(x)=integral v_i1...v_in G(x,v) d³v.

Initially M^(0)=M^(1)=0 and every even moment is zero. Odd moments may
be nonzero. Spatial fields and moment tensors must permit the indicated
derivatives, and velocity/outer spatial boundaries must justify integration
by parts. The identities can also be understood weakly against smooth
spatial test functions. The new bound Plummer populations meet the local
moment assumptions; no initial empirical particle measure is substituted.

With acceleration a, the exact collisionless hierarchy is

    d_t M^(n) = -partial_j M^(n+1)_{j i1...in}
                + sum_r a_ir M^(n-1)_{i1...omit(ir)...in}.

Stationarity in a0=-grad Phi0 gives, in particular,

    partial_j M^(3)_{jkl}=0,
    partial_j M^(5)_{jklmn}=sum_(four slots) a0_k M^(3)_{lmn}.

The second relation is essential: replacing the initial odd moments by
arbitrary tensors would introduce a spurious unforced response.

After a common sudden acceleration increment b=-grad Phi1, the first
changed fourth moment is

    d_t M^(4)_{ijkl}(0)=b_i M^(3)_{jkl}+b_j M^(3)_{ikl}
                       +b_k M^(3)_{ijl}+b_l M^(3)_{ijk}.

The initial first three moment derivatives that could feed density vanish.
Four subsequent divergence steps therefore give

    d_t^n Delta rho(0)=0, n=0,...,4,
    d_t^5 Delta rho(0)=4 partial_i partial_j partial_k partial_l
                         [b_i M^(3)_{jkl}].

Because M^(3) is divergence free in every index, the same operator is

    Q_b = partial_i [M^(3)_{jkl} partial_j partial_k partial_l b_i],
    Delta rho(t)=(1/30) Q_b t^5 + higher orders.

For a potential perturbation, Q_b=-partial_i[M^(3)_{jkl}
partial_i partial_j partial_k partial_l Phi1]. Uniform, affine, or
quadratic-in-position force increments kill this coefficient. Nonzero
M^(3) alone is insufficient. For a time-independent post-switch field,
velocity parity also kills the sixth derivative; a changing field need
not have that additional zero.

## Ramp, bar torque and symmetry

More generally let b(x,t)=t^s b_s(x)+O(t^(s+1)), with integer s>=0.
Successive time integrations give

    Delta rho(t)=4 s!/(s+5)! Q_(b_s) t^(s+5)+O(t^(s+6)).

For quintic growth, eta(t)=c3 t^3+O(t^4), c3=10 eta_final/growth³.
If Phi_bar,shape=eta Phi1(x,theta(t)), theta(0)=theta0 and its history
is smooth and common, b3=-c3 grad Phi1(x,theta0). Hence

    Delta rho(t)=(c3/1680) Q_(-grad Phi1) t^8+O(t^9).

With q1=d_theta Phi1(x,theta0), the particle torque contrast and its
integrated halo angular impulse satisfy

    Delta tau_z(t)=(c3²/1680) t^11 integral q1 Q_(-grad Phi1) d³x+O(t^12),
    Delta I_z(t)=(c3²/20160) t^12 integral q1 Q_(-grad Phi1) d³x+O(t^13).

Spatial convergence is required for these torque integrals. A nonzero
local density coefficient does not prove their integrated coefficient is
nonzero: symmetry or radial cancellation can remove it. These expressions
are early-time identities, not a prediction for the T=200 signal.
During the actual held-speed growth, rotor Omega is exactly the common
imposed value. The t^12 impulse difference is carried by halo/actuator
angular transfer, not a rotor-speed contrast before release.

For axial twins, an axisymmetric common perturbation preserves the
v_phi-reflection pairing, so their density and z torque contrasts remain
zero at all times. For transverse twins in a pi-periodic common bar,
the density difference can exist, but its pi-odd part integrates to zero
against the pi-even z torque field. The transverse paired torque null is
therefore stronger than a short-time exponent. Neither claim establishes
the general cosine law for later self-consistent evolution.

## The new Plummer third moment is nonzero

In G=Mtotal=a=1 units, set Psi=(1+r²)^(-1/2), k=e_z cross x and

    S(r)=2 alpha_p C [4pi 2^(7/2)/105]
          Beta(p+1,9/2) Psi^(p+9/2).

Direct isotropic velocity contractions of the new hidden polynomial give

    M^(3)_{ijk}=A(r)(k_i delta_jk+k_j delta_ik+k_k delta_ij)
               +B(r)(k_i x_j x_k+k_j x_i x_k+k_k x_i x_j),
    A=S[(2p-3)/(p+5/2)*(1+r²)-2],   B=-2S.

Its divergence is proportional to A'/r+r B'+6B, identically zero.
It is nonzero for p6/p8 at nonzero twin strength. This independently checks
the stationarity constraint used above rather than assuming an arbitrary
third moment.

For the actual axial quadrupole, Phi1=kappa Q(1+r²)^(-5/2),
Q=x²-y² and kappa=-3Mb/14. Let D_z=-y partial_x+x partial_y.
With A0=-8S(0)/(p+5/2), B0=-2S(0), the potential operator has the local
expansion

    partial_i[M^(3)_{jkl} partial_i partial_j partial_k partial_l Phi1]
      =kappa[6615 A0+420 B0] D_z Q+O(r^4).

Both terms have the same sign for nonzero positive strength. Thus the
axial Plummer density coefficient does not vanish identically. The
quadratic core term alone would misleadingly give zero; its quartic and
sextic radial terms are needed. This local result does not resolve the
global torque integral or its finite-time magnitude.

## Earlier finite-library terms

Reversal partners give exact initial density and even-moment matching,
but their empirical G_N generally has nonzero local M^(1)_N and is not
stationary. Its unforced density contrast can start as

    Delta rho_N(t)=-t div M^(1)_N+O(t²).

With eta~t³, a generic ordinary-azimuth library can therefore have an
instantaneous torque-noise term t^4 and accumulated term t^5. Exact C4
axial sectors cancel this unforced m2 torque at every common bar angle,
but do not restore the continuum zero local first moment.

For such an initially odd empirical G_N, the first bar-induced density
term, relative to its own unforced evolution, is allowed at t^6:

    Delta rho_N,forced-Delta rho_N,unforced
      =t^6 { (1/60) partial_i partial_j[b3_i M^(1)_N,j]
             +(1/30) partial_i[b3_i div M^(1)_N] }+O(t^7).

These coefficients follow from the two surviving second-order transport
terms in Duhamel's formula; force integration alone cannot replace them.
In a C4 axial library this can produce bar-induced m2 torque at t^9 and
accumulated torque at t^10, earlier than the continuum t^12 term. The
coefficients can still vanish in a particular draw or additional symmetry.
These finite-library statements concern a common prescribed field; they
are not a forecast for later autonomous or responsive trajectories.

Initial-streaming covariance, particle-number and phase controls distinguish
these terms from the continuum identity. No recentering, spin subtraction,
local-mean correction or rejected realization is justified by this analysis.
Floating sector cancellation and time integration can add lower-order
residuals as well. Observing a fitted early-time power is not an all-domain
validation or a substitute for resolving those numerical floors.

## Quadratic force closure gives an exact rotor null

There is a stronger known closure in a different domain. Suppose every
particle's Hamiltonian per unit mass is

    h(z,theta,t)=0.5 z^T K(theta,t) z+k(theta,t)^T z+c(theta,t), z=(x,v),

with symmetric K, independent of rotor L. Add L²/(2I), with the same
positive I and initial theta/L for both populations. The coefficients are
common and regular enough for a unique coupled solution. For finite raw
mass M, first moment mu=integral z f and second matrix Q=integral zz^T f,
set A=J K, b=J k, where J is the canonical symplectic matrix. Then

    mu_dot=A mu+M b,
    Q_dot=A Q+Q A^T+b mu^T+mu b^T,
    theta_dot=L/I,
    L_dot=-0.5 tr(K_theta Q)-k_theta^T mu-M c_theta.

This closed system includes xx, xv and vv. Equal initial M, mu and Q
therefore force identical moments and autonomous rotor histories, despite
different higher moments. No initial stationarity is needed for this null.
Common imposed growth followed by release preserves it. Equal density and
velocity dispersion alone are insufficient: the full xv matrix matters.
The distributions and local higher moments need not become equal.

This is quadratic Hamiltonian moment closure, not a new theorem. It does
not apply globally to the actual Plummer halo: its r^-5 density tail makes
the positive second position moment diverge logarithmically. Equal
infinities cannot serve as finite initial data, and adding a global
quadratic force to that tail need not define finite torque or energy.
The actual Plummer monopole and rotor radial envelope are anharmonic, so
they do not have this closure even where finite diagnostics exist.

An instantaneous spatial window adds transport/flux terms to its moment
equations. Energy cuts need not inherit the twins' first/cross-moment
matching; changing the selected cohort also introduces flux. A fixed
advected cohort would obey the ideal quadratic closure only if its own
finite full moments were initially matched. This null helps identify why
spatial variation beyond a harmonic approximation can expose hidden
higher moments. It predicts no size or sign for the small pilot response.

## Global leading coefficient for the actual positive bar

2 October22:49 UTC. Independent Cartesian/pencil contractions now determine
the previously unspecified global coefficient in this specific model.
Numerical checking is pending; no forced outcome entered this derivation.
The earlier statement that a general torque projection *can* vanish remains
true. For this actual potential and p6/p8 tensor it does not vanish.

Write \(V=\kappa(x^2-y^2)h(r)\), \(h=(1+r^2)^{-5/2}\),
\(\kappa=-3M_b/14\), \(D_z=-y\partial_x+x\partial_y\),
\(q_\theta=-D_zV\), and \(S_0=S(0)>0\). The quantity is a **signed
halo-torque contrast**:

\[
I_p=\int q_\theta Q_{-\nabla V}\,d^3x
   =\int(\partial_iq_\theta)M^{(3)}_{jkl}V_{,ijkl}\,d^3x.
\]

The second form follows from one integration by parts, with vanishing
inner/outer surface terms. It uses the factor two in the signed tensor
from \(F_+-F_-\), not one population's moment. In the adopted units,
\[
S_0=\frac{1024\alpha_p}{245\pi^2}
       \mathrm B(p+1,9/2).
\]

For \(R=\boldsymbol r\cdot\nabla\), directly contracting the tensor gives
\[
M^{(3)}_{jkl}V_{,ijkl}
 =3A\,D_z\partial_i\nabla^2 V
  +3B\,D_z\partial_i[(R-2)(R-3)V].
\]
Here the two radial functions multiplying the same solid harmonic are
\[
\nabla^2 V=\kappa(x^2-y^2)u_A,\qquad
u_A=-35(1+r^2)^{-9/2},
\]
\[
(R-2)(R-3)V=\kappa(x^2-y^2)u_B,\qquad
u_B=5r^2(6r^2-1)(1+r^2)^{-9/2}.
\]

The angular contraction, keeping Cartesian derivatives of the rotating
vector components, yields
\[
I_p=-\frac{64\pi\kappa^2S_0}{5}
 \int_0^\infty r^2(1+r^2)^{-\lambda}P_c(r^2)\,dr,
\quad
\lambda=\frac p2+\frac{45}{4},\quad
c=\frac{2p-3}{p+5/2},
\]
\[
P_c(u)=(350-175c)u+(-210-35c)u^2
 +(1880-1120c)u^3+(1240-1260c)u^4-1200u^5.
\]

Each monomial integrates as
\(\tfrac12\mathrm B(k+3/2,\lambda-k-3/2)\).
Exact Beta recurrence reduces the sum, with \(t=2p+5\), to
\[
\boxed{
I_p=-32\pi\kappa^2S_0\,
\mathrm B\!\left(\frac52,\frac{2p+35}{4}\right)
\frac{5600(t+36)(t^2+32t+1764)}
 {t(t+14)(t+18)(t+22)(t+26)}
}.
\]
All factors following the minus sign are positive for p6/p8 and the
certified positive nonzero \(\alpha_p\). The rational factor also stays
positive for \(p\ge5\); that algebra alone is not a new positivity
certificate for an untested DF family.

The surface term decays as \(r^{-p-9.5}\), and the radial integrand as
\(r^{-p-10.5}\); the center is regular. Thus no tail cut is required.
The continuum quintic-onset result becomes
\[
\Delta\tau_{h,z}
 =\frac{c_3^2 I_p}{1680}t^{11}+O(t^{12}),\qquad
\Delta L_{z,h}
 =\frac{c_3^2 I_p}{20160}t^{12}+O(t^{13}).
\]

This establishes a negative **leading contrast**, not negative individual
torques or a later braking ordering. The bar speed is externally clamped
through growth. A formal onset expansion does not extrapolate to T20 or
T200, and empirical initial streaming permits earlier terms. It is a
specific mathematical explanation of how the hidden third moment can
produce a response despite equal density and even moments; it supplies
neither a live-halo convergence result nor a novelty claim.

A bounded metered Cartesian Taylor-jet quadrature is prepared to check
the global contraction independently of the radial derivative polynomial.
Its fixed32/64 radial orders cover0–infinity, with8x16 angular nodes.
It has not executed when this section is written.

### Actual independent numerical check

The subsequent `early-torque-coefficient-check-01` completed at
22:51:02 UTC with unchanged inputs and all seven checks passing. Its source
`check_early_torque.py` was independently reviewed at SHA256
`324aa24fb219b565f665bb3425a20d3777dc9c2c7f150612bdcca0251b78fb92`.
It differentiates the Cartesian potential with a generalized-binomial Taylor
jet through degree four, rather than using the radial polynomial above.
Fixed 32/64-node radial rules cover the full positive half-line; the fixed
8-by-16 angular rule integrates the polynomial angular dependence exactly
in exact arithmetic. No orbit evolution or particle library enters the check.

The checked normalized quantity is \(I_p/(S_0\kappa^2)\):

| Family | Closed Beta expression | Cartesian order 32 | Cartesian order 64 |
| --- | ---: | ---: | ---: |
| p6 | -6.049340596003346 | -6.049340596003322 | -6.049340596003319 |
| p8 | -3.173155830681601 | -3.1731558306815826 | -3.173155830681581 |

All relative discrepancies are below \(6.4\times10^{-15}\), comfortably
within the frozen numerical tolerances. The actual bar value, force and
halo-torque sign also pass their independent checks. The full process cost
was 0.513849 measured CPU seconds plus the explicit five-second closing
allowance. The input proof version remains in the job's frozen input copy;
this appended outcome does not modify that historical receipt.

These are mathematical and implementation checks of the global coefficient.
They do not establish finite-particle error, collective stability, an
autonomous pattern-speed contrast or validity of extending the onset series
to the experiment endpoints.

## Coupled live-halo onset: an independent conditional derivation

2 October23:16 UTC. Root and an independent reviewer derived the coupled
equations without reading forced outcomes. A self-consistent halo does not
automatically share the prescribed-field proof. Under the additional
premises below, however, its leading coefficient is the same.

Let \(\bar f=(f_++f_-)/2\), \(g=f_+-f_-\), and let
\(\mathcal P\) map self density to potential. The map is common, linear,
instantaneous and continuous on the required density/force class. Initially
both DFs are stationary in the **actual same** full potential \(\Phi_0\),
including the fixed physical bar monopole, with common density \(\rho_0\).
The common and difference fields are
\[
\Phi_c=\Phi_0+\eta V_{\theta(t)}+
       \mathcal P(\bar\rho-\rho_0),\qquad
\chi=\mathcal P\Delta\rho.
\]
With \(A_c=-\boldsymbol v\cdot\nabla_x+
\nabla\Phi_c\cdot\nabla_v\) and
\(B_\chi=\nabla\chi\cdot\nabla_v\), the exact coupled Vlasov equations are
\[
\partial_t\bar f=A_c\bar f+\tfrac14 B_\chi g,\qquad
\partial_tg=A_cg+B_\chi\bar f.
\]
The factors matter: the signed self potential is \(\chi\), not one twin's
half contribution.

Define spatial operators, acting on a potential,
\[
\mathcal E V=\nabla\cdot(\rho_0\nabla V),\qquad
\mathcal QV=-\partial_i(T_{jkl}V_{,ijkl})=Q_{-\nabla V},
\]
where \(T=M^{(3)}\) is the initial signed third tensor. For the common
quintic onset \(\eta=c_3t^3+O(t^4)\), the shared first moment changes at
order four, while the signed fourth moment changes at order four. Their
different paths through the hierarchy give
\[
\bar\rho-\rho_0=\frac{c_3}{20}\mathcal EV\,t^5+O(t^6),\qquad
\Delta\rho=\frac{c_3}{1680}\mathcal QV\,t^8+O(t^9).
\]
Thus the common induced self force begins at order five and the difference
self force at order eight. The latter acts on the populated reference
density through two integrations; the former acts on the stationary
signed DF through five. Both first alter the signed density at order ten.
Relative to the same prescribed growth history,
\[
\boxed{
\Delta\rho_{\rm live}-\Delta\rho_{\rm prescribed}
=\frac{c_3}{151200}
 (\mathcal Q\mathcal P\mathcal E+
  \mathcal E\mathcal P\mathcal Q)V\,t^{10}+O(t^{11})
}.
\]
This is the first **allowed** collective correction; its projection may
cancel. In particular it cannot change the nonzero order-eleven bar-torque
contrast established above. The first allowed collective alteration of
that contrast is order thirteen. This conclusion follows from the coupled
equations, rather than assuming both halos remain in one prescribed field.

For a *different theoretical preparation* with the physical constant-inertia
rotor free from time zero and equal initial angular momenta, reaction gives
\[
\Delta L_b=-\frac{c_3^2I_p}{20160}t^{12}+O(t^{13}),\qquad
\Delta\theta_b=-\frac{c_3^2I_p}{262080I_b}t^{13}+O(t^{14}).
\]
Its angle-dependent difference in the bar field begins at order sixteen,
too late to modify the leading coefficient. For positive \(\alpha_p\),
\(I_p<0\) therefore gives a positive leading signed rotor-speed contrast
in this theoretical variant. The **actual campaign clamps speed during
growth**; it does not implement or observe that pre-release separation.

This conditional result requires regular weak moment expansions,
stationarity under the actual initial force, valid spatial/velocity boundary
terms and convergent weighted torque integrals. A convergent finite-basis
operator can meet these continuum premises; changing the initial evolution
force while retaining an unrelated stationary DF cannot. The existing exact
halo potential is in the radial n0/n1 Plummer-basis span (see
`scf.exact_halo_coefficients`), but ordinary empirical source coefficients
fluctuate. Their finite local streaming, discreteness and sampled-force
nonstationarity can generate earlier terms. This proof supplies no new
numerical allowance, equilibrium verdict, damping or endpoint forecast.
