# Positive joint energy for the F0 halo and supported quadrupole source

The isotropic reference halo F0, coupled reciprocally to the disclosed supported material quadrupole, has a positive conserved quadratic energy in its finite-energy linear quadrupole domain. This excludes nonzero exponentially growing eigenmotions in that domain. The proof includes halo self-gravity, source self-gravity and their interaction; it is not a damping theorem or a statement about the hidden population A.

## Equilibrium and physical conventions

Use units \(G=M_{\rm total}=a=1\), and set

\[
\psi=(1+r^2)^{-1/2},\qquad \Phi_0=-\psi,\qquad M_b=\frac1{10}.
\]

The spherical carrier and its actual halo complement are

\[
\rho_{b0}=\frac{15M_b}{8\pi}\psi^7,\qquad
\rho_{h0}=\frac{3}{4\pi}\psi^5-\frac{15M_b}{8\pi}\psi^7.
\]

Their masses are \(M_b\) and \(1-M_b\). The carrier monopole is already included in \(\Phi_0\); it is not added again. The halo is not obtained by multiplying the Plummer response by its mass fraction.

On the populated bound branch \(e=-H_0=\psi-v^2/2>0\),

\[
F_0(e)=\mathcal N e^{7/2}(1-Q_0e^2),\qquad
\mathcal N=\frac{24\sqrt2}{7\pi^3},\qquad Q_0=\frac{14}{33},
\]

\[
F_e=\frac{dF_0}{de}
=\frac{\mathcal N}{2}e^{5/2}(7-11Q_0e^2)>0.
\]

The Hamiltonian derivative is \(dF_0/dH_0=-F_e\). The unbound branch has \(F_0=0\).

All energies below refer to physical real perturbations. Complex notation denotes the Hermitian extension of those same real quadratic forms. In a spherical-harmonic expansion, the complete signed pair is included once, with \(c_{-m}=c_m^*\) for the physical field. The factors \(1/2\) in quadratic energies are not supplemented by another pair factor or by taking a second real-part projection.

## Halo energy and the quadrupole inequality

Let \(\delta\rho_h=\int\delta f_h\,d^3v\) and let its regular decaying potential satisfy \(\Delta\phi_h=4\pi\delta\rho_h\). Define

\[
Q_h=\frac12\int\frac{|\delta f_h|^2}{F_e}\,d^3x\,d^3v,\qquad
G_h=-\operatorname{Re}\int\delta\rho_h^*\phi_h\,d^3x
=\frac1{4\pi}\int|\nabla\phi_h|^2\,d^3x,
\]

\[
U_h=-\frac{G_h}{2},\qquad E_h=Q_h+U_h,\qquad
S_h=\int B_h|\phi_h|^2\,d^3x.
\]

Here \(Q_h\) is the positive particle term of the halo energy-Casimir Hessian: the equilibrium Casimir curvature is \(1/F_e\). Its actual velocity weight is

\[
B_h=\int F_e\,d^3v=\frac{d\rho_{h0}}{d\psi}
=\frac{15}{4\pi}\psi^4-\frac{105M_b}{8\pi}\psi^6
=B_P\left(1-\frac72M_b\psi^2\right),\qquad
B_P=\frac{15}{4\pi}\psi^4.
\]

Thus \(0<B_h\le B_P\). There is no escape-boundary contribution when differentiating the density because \(F_0(0)=0\). Velocity Cauchy and then spatial weighted Cauchy give

\[
\int\frac{|\delta\rho_h|^2}{B_h}\,d^3x\le 2Q_h,
\qquad
G_h^2\le
\left(\int\frac{|\delta\rho_h|^2}{B_h}\,d^3x\right)S_h
\le 2Q_hS_h.
\]

For any quadrupole harmonic \(Y_{2m}\), the positive radial function \(h=r^2\psi^5\) satisfies

\[
-\Delta(hY_{2m})=35\psi^4hY_{2m}.
\]

For \(\phi_h=u(r)Y_{2m}\), integration by parts therefore yields the ground-state identity

\[
\int|\nabla\phi_h|^2\,d^3x-35\int\psi^4|\phi_h|^2\,d^3x
=\|Y_{2m}\|_\Omega^2\int_0^\infty r^2h^2
\left|\left(\frac{u}{h}\right)'\right|^2dr\ge0.
\]

It first holds for compact regular fields and extends to their finite-gradient-energy closure. Orthogonality gives the same inequality for every combination of quadrupole harmonics; their normalization cancels. Consequently

\[
S_h\le\frac37G_h,\qquad
Q_h\ge\frac76G_h,\qquad E_h\ge\frac23G_h.
\]

For \(G_h=0\), no division is needed: the decaying potential and density vanish, while density-invisible particle perturbations retain their nonnegative \(Q_h\).

## The linked material source and reciprocal interaction

Write \(q=(q_c,q_s)\), \(p=M_s\dot q\). The carrier density family is

\[
\rho_b(q)=\rho_{b0}\left[1+\psi^2\bigl(q_c(x^2-y^2)+2q_sxy\bigr)\right].
\]

It is nonnegative for \(|q|\le1\); the linear model concerns its much smaller tangent near \(q=0\). Its perturbation has no monopole. The two potential tangents are

\[
B_c=-\frac{3M_b}{14}(x^2-y^2)\psi^5,\qquad
B_s=-\frac{3M_b}{14}(2xy)\psi^5,\qquad
\phi_b=q_cB_c+q_sB_s.
\]

The unit-velocity material displacements
\(\xi_c=\nabla[(x^2-y^2)/14]\) and \(\xi_s=\nabla[xy/7]\) satisfy
\(-\nabla\cdot(\rho_{b0}\xi_\alpha)=\partial\rho_b/\partial q_\alpha\).
Their mass inner products give the fixed shape inertia

\[
\int\rho_{b0}\xi_\alpha\cdot\xi_\beta\,d^3x
=M_s\delta_{\alpha\beta},\qquad M_s=\frac{M_b}{49}.
\]

This is a material shape motion, not rigid rotation or an adjustable rotor inertia. With \(\rho_\alpha=\partial\rho_b/\partial q_\alpha\), direct Poisson overlap gives

\[
\int\rho_\alpha B_\beta\,d^3x=K_g\delta_{\alpha\beta},\qquad
K_g=-\frac{15\pi M_b^2}{14336},\qquad
G_b=\frac1{4\pi}\int|\nabla\phi_b|^2\,d^3x=(-K_g)|q|^2.
\]

The real-to-signed normalization can be checked independently. For
\(\phi_{0,+}=-\sqrt{15/8}(x+iy)^2\psi^5\), \(\phi_{0,-}=\phi_{0,+}^*\), and their exact negative Poisson norm \(D_0=-175\pi/2048\), the source map is

\[
\mathsf Cq=S\binom{(q_c-iq_s)e_0}{(q_c+iq_s)e_0},\qquad
S=\frac{3M_b}{7\sqrt{30}},\qquad
\mathsf C^\dagger D\mathsf C=2S^2D_0I_2=K_gI_2.
\]

For basis potentials \(\phi_p\), define their densities and exact physical overlaps by

\[
\rho_p=\frac{\Delta\phi_p}{4\pi},\qquad
D_{pq}=\int\rho_p^*\phi_q\,d^3x
=-\frac1{4\pi}\int\nabla\phi_p^*\cdot\nabla\phi_q\,d^3x.
\]

The indices include both signed sectors; \(e_0=(1,0,\ldots)\) selects the explicitly displayed \(\phi_{0,+}\) or \(\phi_{0,-}\) in its respective block. If \(c\) represents the halo field, the real source force overlap is
\(a_\alpha=\int\delta\rho_hB_\alpha\,d^3x\), equivalently \(a=\mathsf C^\dagger Dc\). These identities use exact physical overlaps, not an assumed numerical Gram matrix or a seven-mode truncation of the proof.

The disclosed time-independent rotationally invariant support has

\[
\omega_s=\frac6{25},\qquad K_s=M_s\omega_s^2,
\qquad K_s=K_{\rm support}+K_g,
\qquad
E_b=T_b+\frac{K_s}{2}|q|^2,\quad T_b=\frac{|p|^2}{2M_s}.
\]

Source self-gravity is included in \(K_s\) once. This supported shape model is not a natural hydrostatic-fluid mode or a collisionless stellar bar. Its support stores energy; it supplies no time-dependent actuator power after release.

The interaction is

\[
V=\int\delta\rho_h\phi_b\,d^3x=q\cdot a
=-\frac1{4\pi}\operatorname{Re}\int\nabla\phi_h^*\cdot\nabla\phi_b\,d^3x,
\qquad |V|\le\sqrt{G_hG_b}.
\]

There is **no half** in \(V\): the total gravitational energy has two equal reciprocal cross terms and its overall factor \(1/2\) counts their sum once.

## Conservation and the positive square

For the same total perturbing potential \(\phi_h+\phi_b\), the linear halo equation and continuity equation are

\[
\partial_t\delta f_h+\{\delta f_h,H_0\}
=-F_e\,v\cdot\nabla(\phi_h+\phi_b),\qquad
\partial_t\delta\rho_h+\nabla\cdot\delta j_h=0.
\]

Since \(F_e\) is constant along the equilibrium characteristics, the transport contribution to \(\dot Q_h\) vanishes. Integration by parts gives

\[
\dot Q_h=-\int(\phi_h+\phi_b)\partial_t\delta\rho_h\,d^3x,
\quad \dot U_h=\int\phi_h\partial_t\delta\rho_h\,d^3x,
\quad \dot E_h=-q\cdot\dot a.
\]

The reciprocal source equations are \(\dot q=p/M_s\), \(\dot p=-K_sq-a\), so

\[
\dot E_b=-\dot q\cdot a,\qquad
\dot V=\dot q\cdot a+q\cdot\dot a,\qquad
\frac{d}{dt}(E_h+E_b+V)=0.
\]

The two internal energies need not change oppositely while the interaction changes. Set \(E=E_h+E_b+V\). The preceding inequalities give the explicit square completion

\[
\boxed{
E\ge T_b+\left(Q_h-\frac76G_h\right)
+\frac23\left(\sqrt{G_h}-\frac34\sqrt{-K_g}\,|q|\right)^2
+\left(\frac{K_s}{2}-\frac{3(-K_g)}8\right)|q|^2.}
\]

Thus \(K_s>3(-K_g)/4\) makes the joint quadratic energy strictly positive for every nonzero physical perturbation in the stated domain. The square and source remainder together control \(G_h\); the remaining particle term retains density-invisible energy. At the fixed source parameters the sufficient condition is

\[
\left(\frac6{25}\right)^2>\frac{2205\pi}{57344}M_b.
\]

For \(M_b=1/10\), it follows already from \(\pi<4\) and
\(36/625>441/28672\), without fitting any inertia, stiffness or response.

## Domain and the numerical falsifier

The domain consists of finite-\(Q_h\) tangent perturbations on the populated bound support, a regular decaying finite-gradient-energy quadrupole potential, and finite \(q,p\). Integration by parts is understood through the regular finite-energy closure, without an artificial wall or discarded weakly bound states. Arbitrary perturbations where \(F_e=0\), added unbound populations and finite-amplitude nonlinear source motion are outside the assertion. Dynamically accessible perturbations satisfying these conditions are included; the algebraic bound is not restricted to them.

An all-time conclusion requires the invariant simultaneous spatial/velocity-rotation \(l=2\) phase-space block. Initially quadrupolar density alone does not establish that condition. The isotropic F0 equilibrium, spherical transport and quadrupole source preserve this block for the released zero-halo seed

\[
q(0)=\epsilon(1,0),\qquad
p(0)=M_s\epsilon\omega_s(0,1),\qquad \delta f_h(0)=0,
\qquad E(0)=K_s\epsilon^2.
\]

Positive conserved energy excludes nonzero finite-weighted-energy exponentially growing eigenmotions of this particular linear F0/source system. It proves neither damping nor a frequency gap, and makes no global, other-sector, nonlinear or A-population claim. Density-invisible phase-space components and their energy must remain in any faithful physical realization.

A finite action/Fourier/profile operator does not automatically inherit this inequality. A growing F0 candidate in such an operator challenges its claimed faithful finite-energy representation: the physical metric, reciprocal force, support, domain and halo energy reconstruction must be checked. It does not overturn this theorem by itself. Reflection of spectral coefficients or conservation in an abstract signed bath alone is not a reconstruction of the physical halo energy. Numerical failures and unqualified outcomes must remain visible; no Ward, phase or symmetry repair is part of the proof.

*Historical derivations:* “F0 joint energy with the supported quadrupole source” and “Reciprocal supported source: factors, residues and energy scope,” research notes dated 9 October 2026, with the mechanical definitions in “Reciprocal two-coordinate quadrupole: prospective source contract.” The argument above restates their full chain rather than relying on an inertia-only excerpt.
