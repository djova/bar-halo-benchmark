# Identical initial bulk states, opposite gravitational work

*Working draft, editorial update 2026-10-11; not externally reviewed. The
central cycle, its same-equation public reproduction and the four assessed
figures are recorded here. Final rendering and publication remain separate
release gates; formal-spectrum and free-source questions retain their own
scope below.*

Two positive stationary halo populations can match their initial density,
pointwise mean velocity and entire velocity-reversal-even distribution
yet exchange opposite total work with the same imposed gravitational cycle.
A fresh causal calculation constructs the orbital response independently of
the earlier solver and includes each population's induced gravity. At the
finer energy128 × circularity64 rule, its quadratic weak-response work
coefficients are

\[
W_{2,0}=+1.94964\times10^{-5},\qquad
W_{2,A}=-6.02430\times10^{-6}.
\]

Positive work enters the halo; negative work means that the halo returns
energy to the imposed source. A state's mean current therefore does not fix
the sign of its driven energy exchange. The wake depends on how occupied
orbits sample the source's phases, and their occupation can differ even when
all initial reversal-even data agree. The calculation tests this freedom
over an entire switched-off cycle, rather than inferring work from a torque
at one instant.

Both work signs survive the retained cumulative empirical refinement
allowances. The full complex-wake distances from the earlier JOINT result
are only 0.3283% for F0 and 0.2968% for A. Accumulating earlier action shifts
and sparse-clock interpolation allowances gives much larger waveform proxies,
29.426% and 33.597%, which fail the original 5% screen; these percentages are
not the observed distances. The work-magnitude screens and A's angular-impulse
screen also fail, while F0's impulse screen passes. Thus the evidence supports
a numerical finite-cycle sign replication with conditional uncertainty, not
a certified continuum magnitude or waveform. Shared DF, basis and linear-model
assumptions remain. Whether the active response also belongs to a stable medium
is a separate question. [AH-CYCLE](evidence.html#cycle)

**Figure AH-CYCLE-02 — completed assessed figure; publication pending.**
[PNG](figures/independent-cycle-wake-refinement.png)
· [SVG](figures/independent-cycle-wake-refinement.svg).
F0/A real and imaginary global wake overlaps compare old JOINT, independent
GL64 and fresh E128 results on their actual clocks. The observable
\(S D_0c_{+2,0}\) is an inertial positive-harmonic source overlap, not a
whole-halo density axis. Curves are unaligned and uncorrected; both signed
harmonics and all seven radial basis functions CB0–6 enter the assessment. The observed
agreement and failed expanded screens are retained together. The assessed
display archive has no cumulative W/J curves.

## What is identical, and what responds differently

Let \(e=-H_0>0\) be binding energy, \(L\) the angular-momentum magnitude
and \(L_z\) its signed axial component. The frozen family is

\[
F_0=Cg(e),\qquad
F_A=C[g(e)+L_z h(e,L^2)],\qquad
g(e)=e^{7/2}(1-14e^2/33),\qquad
C=\frac{24\sqrt2}{7\pi^3}.
\]

The hidden function is explicit:

\[
h(e,L^2)=\sum_{p\in\{5,6,7,8,10,12\}}c_p
 [-a_p e^{p-1}+b_p e^{p+1}+L^2e^p],\qquad
a_p=\frac{4p}{(p+\tfrac52)(p+\tfrac72)},\quad
b_p=\frac4{p+1}.
\]

The selected coefficients were frozen before this independent calculation.
Their full-support certificate gives \(F_0/2\le F_A\le3F_0/2\), so the odd
term redistributes occupation inside one positive population. The
[frozen coefficient vectors](evidence/coefficients.json)
and [actual positivity certificate](evidence/certificate.json)
retain the operands; the default article needs no coefficient table.
Both DFs are stationary because their arguments are unforced integrals.
Velocity reversal changes \(L_z\)'s sign while leaving \(e,L^2\) unchanged.
Thus their complete even parts match exactly:

\[
\frac{F_A(\mathbf x,\mathbf v)+F_A(\mathbf x,-\mathbf v)}{2}
=F_0(\mathbf x,\mathbf v),\qquad
\int\mathbf v F_A\,d^3v=\int\mathbf v F_0\,d^3v=\mathbf0 .
\]

The local-current identity holds power by power for the displayed \(a_p,b_p\);
oddness alone would not imply it. Opposite directions are unequally occupied
within particular binding-energy and tangential-speed ranges, while their
first-moment contributions cancel when all velocities at a position are
integrated. This is one population with a state-dependent direction imbalance,
not two separately gravitating fluids. A driven wake weights those same states
by their canonical derivatives and orbital phases, so cancellation of the
ordinary first moment does not force cancellation of the response.

Density and every initial velocity-reversal-even observable also match.
Consequently the initial kinetic and gravitational energies agree: A has no
extra initial bulk kinetic energy. The matching is initial, not a constraint
on later wakes or on the final state after forcing. Odd occupation changes
phase-space organization and higher invariants; the external potential can
complete a cycle without restoring the halo. A quantitative available-energy
bound for A has not been established. [AH-MATCH](evidence.html#matching)

The halo is the exact complement of a physical spherical carrier, rather than
a rescaled Plummer halo. With \(G=M_{\rm total}=a=1\),
\(\psi=(1+r^2)^{-1/2}\) and \(M_b=0.1\),

\[
\Phi_0=-\psi,\qquad
\rho_{b0}=\frac{15M_b}{8\pi}\psi^7,\qquad
\rho_{h0}=\frac{3}{4\pi}\psi^5(1-\tfrac14\psi^2).
\]

The halo has total mass \(M_h=0.9\), but neither its density nor its DF is
0.9 times the pure Plummer expression. The common monopole is fixed and
anchors the centre. The applied quadrupole derives from the carrier contrast
\(\rho_{b0}\psi^2[q_C(x^2-y^2)+2q_Sxy]\), with
\(B_C=-3M_b(x^2-y^2)\psi^5/14\) and
\(B_S=-3M_b(2xy)\psi^5/14\). It is a specified weak physical source,
not an evolving stellar bar. The overlap convention uses
\(S=3M_b/(7\sqrt{30})\), \(D_0=-175\pi/2048\) and
\(\int|Y|^2\,d\Omega=4\pi\);
\(c_{+2,0}\) is the first spatial coefficient of the induced potential.
[AH-MODEL](evidence.html#model)

**Figure AH-MATCH-01 — proposed analytic schematic.** The two DFs, their
exactly matched initial moments and the common positive carrier. It illustrates
the definitions, not sampled particles or an additional numerical result.

The linear response depends on canonical derivatives that these initial
matching conditions do not fix. In the spherical action chart
\((J_r,L,L_z)\), a harmonic \((n,k,m)\) has
\(\nu=n\Omega_r+k\Omega_L\) and
\(\kappa=nF_{J_r}+kF_L+mF_{L_z}\), with other actions held fixed.
For the affine odd term,

\[
\kappa_A=C[-\nu(g_e+L_z h_e)
            +2kLL_z h_{L^2}+mh].
\]

Here \(h_e\) holds \(L^2\) fixed, while \(h_{L^2}\) holds \(e\) fixed.
The isotropic reference has \(\kappa_0=-C\nu g_e\); the extra terms alter
the signed cross response of the two real quadrupole components. Zero
initial current does not fix that retarded phase relation. The global wake
overlap then determines energy and angular-momentum transfer. Exact spatial
angular closure here follows from the affine-\(L_z\) structure, rank-one
rotation covariance and parity; it is not imported from spherical density
or zero current alone. It does not remove density-invisible phase-space
components or establish stability in other angular sectors.
[AH-ANGULAR](evidence.html#angular)

## A complete causal cycle

The common imposed source has pattern speed \(\Omega=0.12\), quadrupole
harmonic \(\omega=2\Omega=0.24\), duration \(T=120\), rise/fall time 12 and
maximum envelope 0.8. The source returns to zero at the end. Total work
is measured from the physical real fields. Write
\(\rho=\rho_{h0}+\epsilon\delta\rho_1+O(\epsilon^2)\) and
\(\Phi_{\rm ext}=\epsilon\Phi_{{\rm ext},1}\), where \(\delta\rho_1\)
includes the own-field response. With \(\varphi\) the spatial azimuth,

\[
W_2(T)=\int_0^Tdt\int d^3x\,
       \delta\rho_1\,\partial_t\Phi_{{\rm ext},1},\qquad
\tau_2(t)=-\int d^3x\,
       \delta\rho_1\,\partial_\varphi\Phi_{{\rm ext},1}.
\]

Positive \(\tau_2\) delivers axial angular momentum to the halo; the imposed
driver receives the opposite torque. The spherical equilibrium contributes
no first-order quadrupole work. For constant pattern speed, rotational power
is \(\Omega\tau_2\), and ramp work remains part of the complete budget:

\[
W_2(T)=W_{2,\rm shape}+\Omega J_2(T),\qquad
J_2(T)=\int_0^T\tau_2(t)\,dt .
\]

The saved work split shows how the final signs arise. F0's rotational work
\(+2.0507\times10^{-5}\) is partly offset by shape work
\(-1.0103\times10^{-6}\). A instead returns rotational work
\(-7.4415\times10^{-6}\), partly offset by positive shape work
\(+1.4172\times10^{-6}\). Rotation therefore sets the final sign in both
populations, while changing the amplitude acts in the opposite direction.
At each time, rotation weights the out-of-phase global wake overlap; shape
power weights its in-phase component by the envelope derivative. A complete
source cycle need not make that shape contribution zero or reversible.
[Recorded split and diagnostics](evidence.html#mechanism)

**Figure AH-CYCLE-MECHANISM — E128 energy × 64 circularity, dt=0.025; completed and visually inspected; publication pending.**
[PNG](figures/cycle-work-mechanism.png)
· [SVG](figures/cycle-work-mechanism.svg)
· [full-clock numeric CSV](figures/cycle-work-mechanism.csv).
For each population, the full T120 record shows global source-phase overlaps,
instantaneous shape/rotational power and cumulative total/shape/rotational
work. Both saved signed partners and the full spatial Gram column enter the
overlap; it is not a literal density-axis angle. Total and shape work are
saved curves, and rotation work is \(\Omega\) times saved impulse. No new
integration, phase fit, conjugacy projection or field correction is applied.
This explains the recorded imposed cycle, without adding an independent
simulation or a sustained stationary-power claim. The original failed
expanded accuracy screens remain beside the transfer interpretation.

The newer method constructs fresh orbits in physical radius, independently
integrates angular coefficients and evolves the causal Volterra response.
Its independent physical construction is distinct from porting the same
equations into a public executable. The finer E128 paired impulse coefficients
are \(+1.7088941899192118\times10^{-4}\) for F0 and
\(-6.201246042854836\times10^{-5}\) for A. Their empirical allowances and
original magnitude-screen decisions are retained separately from the work
signs. [AH-CYCLE](evidence.html#cycle)

These are weak-response coefficients, not fractional bar changes. With
\(t_*=\sqrt{a^3/(GM_{\rm total})}\), \(E_*=GM_{\rm total}^2/a\) and
\(J_*=M_{\rm total}\sqrt{GM_{\rm total}a}\), physical work and impulse are
\(\epsilon^2E_*W_2\) and \(\epsilon^2J_*J_2\); the wake is first order
per \(\epsilon\). The coefficient calculation already includes the 0.8
envelope. The independent finite-cycle evidence does not imply sustained
finite-amplitude extraction.

## Changing the hidden population strength

The family \(F_\lambda=F_0+\lambda(F_A-F_0)\) changes which orbital states carry the direction imbalance. Every chosen strength retains the exact same initial density, complete even phase-space distribution and pointwise zero current. It adds no initial kinetic energy. What changes is the derivative of the population that weights the driven response.

The bare wake is affine in \(\lambda\). The collective wake is a separate response for each population: the halo feels the imposed field plus its own field, so an interpolation of endpoint wakes would not solve the intermediate system. Work C retains the completed \(\lambda=0,1\) controls and freshly solves all eighteen intermediate own-field signed cells across the three fixed layouts. Shared numerical methods and cached bare kernels remain correlated controls; this is a population/refinement comparison, not a second independent physical theory.

The figure uses the actual paired total \(W_2\). The recorded split is \(W_2=W_{{\rm shape},2}+0.12J_2\): changing the envelope can exchange work as well as rotation. Both signed sectors, full raw spatial metric, shape/rotation endpoints and signed energy/angular budget residuals remain in the downloads. Nothing is integrated again or repaired to enforce the identity. Four GL32 forecasts, \(W_2\) and \(J_2\) at each of \(\lambda=.5,.75\), were frozen before the corresponding GL64 intermediate own solves. All four time-only ranges miss the actual GL64 values; those failures remain visible. At \(\lambda=.75\), the expanded own-field work allowance includes zero, so its sampled sign remains unresolved.

**Figure AH-CYCLE-STRENGTH — five computed populations.** Paired total work over the full imposed T=120 cycle, with bare and own-field responses centered on GL64 energy × 64 circularity quadrature, dt=0.025. The article headline uses the separate E128 energy × 64 circularity result. Source shape .8 is included once; values are coefficients per ε² in model energy units. The total empirical bar sums action, time and finest-budget components, shown separately; it is not a confidence interval or rigorous enclosure. Own-field empirical work ranges are positive at λ=0, 0.25, 0.5; negative at λ=1; including zero at λ=0.75. These are sampled sign statements, not a monotonic trend, critical strength, stationary band or free growth. Markers are offset horizontally only for readability; no response values are interpolated.

[Standalone SVG](figures/finite-cycle-strength-work.svg) · [Complete scientific JSON](evidence/strength-map.json) · [Paired endpoint CSV](evidence/strength-endpoints.csv) · [Signed endpoint CSV](evidence/strength-signed-endpoints.csv) · [Scalar sensitivity CSV](evidence/strength-scalar-ranges.csv) · [Frozen forecasts CSV](evidence/strength-forecasts.csv).

The internal fine-centered sensitivity screens are additional recorded diagnostics. They do not replace the original E128 anchor/expanded magnitude and waveform criteria, whose failures remain in the preceding cycle evidence. Five computed strengths can support sampled sign comparisons; they do not locate a continuous threshold or prove any response between the samples.

## A separate bare frequency test

Fresh continuous-action resonant integration tests the same fixed source
at harmonic frequency 0.24. At retained Fourier cutoff N32, the bare
power coefficients are

\[
P_{2,0}=+1.2284257031\times10^{-7},\qquad
P_{2,A}=-6.2867623785\times10^{-8}.
\]

Here “bare” omits the induced field feedback. All 97 retained positive
representatives were assessed; the real-source conjugate pair is included
once in the physical power. Conditional retained-error and analytic omitted
harmonic-tail allowances preserve the opposite signs. They are not outward
interval bounds or certification of every retained branch and numerical
error. This tests an absorptive frequency response distinct from the
complete-cycle observable, whose ramp work and finite frequency window
remain essential. Physical power is
\(\epsilon^2(E_*/t_*)P_2\). [AH-BARE](evidence.html#assessed-scope)

The preselected neighboring probes constrain the interpretation: A emits
at 0.23 but absorbs weakly at 0.25, while F0 absorbs at both. These retained
N16 signs have empirical N8/N16 plus quadrature allowances, with higher
harmonic tails still unqualified. The preserved 0.26 failures leave its
pointwise result undefined. Connecting the recorded points cannot create
a qualified continuous band. For the fixed affine family
\(F_\lambda=F_0+\lambda(F_A-F_0)\), bare power is affine in \(\lambda\);
its five strengths reuse the same endpoint response, rather than supplying
five independent calculations or statistical samples. Collective dressing
requires a separate inverse for each strength. [AH-INNER](evidence.html#assessed-scope)

**Figure AH-BARE-02 — completed assessed figure; publication pending.**
[PNG](figures/bare-discrete-power-and-strength.png)
· [SVG](figures/bare-discrete-power-and-strength.svg).
Recorded frequency points only, with central N32 adverse-tail ranges distinct
from neighbor empirical proxies and an explicit undefined 0.26 annotation.
A separate central bare-\(\lambda\) panel shows its exact affine relation.
No frequency-connecting curve or dressed straight line.

## Finite-cycle exchange does not establish free growth

This report includes finite-cycle response and strength refinements. The formal-spectrum assessment is not included here; this scope choice asserts neither its failure nor its availability. Formal inversion, stationary absorption, global stability and autonomous source growth require their own evidence. The finite imposed cycle supplies none of those conclusions.

A free source requires a reciprocal physical mode, not fitted negative
damping. Its carrier potential-flow displacement gives shape inertia
\(M_s=M_b/49\), different from rigid \(I_z=M_b\). The total stiffness
\(K_s\) counts source self-gravity once and includes additional positive
conservative constitutive support, specified independently of the halo
outcome. Its supported frequency is not a natural barotropic-fluid Ritz
frequency, and its mechanics have not been demonstrated for a stellar bar.
The test does not establish that actual baryonic galaxies supply this stiffness.
A pole or initial-value test must retain halo, source and interaction energy,
angular momentum, signed partners and unforced halo
modes. The scoped positive-energy proof for F0 plus the supported source
supplies a control; it is not an A stability proof. Existing sampled contours
above \({\rm Im}\,z=0.01\) cannot exclude slower growth, and the anchored
dipole action-grid comparison fails its convergence margin. A fresh
N64-to-N128 comparison at fixed GL32 gives largest recorded contour-point
changes of \(1.62\times10^{-4}\) in the balanced operator and
\(5.59\times10^{-4}\) in inverse-times-change. Both resolutions retain
zero sampled winding counts, but their Fourier agreement does not remove
the much larger action discrepancy or qualify a uniform contour.
[Dipole refinement](evidence.html#limits)
The isolated translation benchmark is a different problem, not a neutral mode to impose on the
anchored halo. Continuous-band, continuum-stability and reciprocal free-mode
qualification remain open.
[AH-SOURCE](evidence.html#source)

[Full reference/source energy proof (F0 only)](f0-source-energy.html) · [Markdown proof](f0-source-energy.md).

The primary predecessors make the distinction narrower than “halos can emit.”
[Nelson & Tremaine (1995)](https://arxiv.org/pdf/astro-ph/9408068)
already found a nonrotating, tangentially biased halo that feeds a warp.
Their tangential-anisotropy emission comparison changes the even DF;
their separate fixed-anisotropy rotation family already preserves it.
Both calculations omit response self-gravity. They also distinguish halo emission from a passive halo
exciting a negative-energy warp while absorbing its energy.
[Nelson & Tremaine (1999; 1997 preprint)](https://arxiv.org/html/astro-ph/9707161)
provide the external-work, anti-Hermitian response, dressing and mode-energy
framework used to separate these mechanisms. Their full time-reversal
premises for reciprocity and the relevant instability criterion are stronger
than zero current.

[Chiba & Kataria (2024)](https://arxiv.org/html/2311.07640v2)
already preserve the entire even DF through bounded odd occupations and
study their effects on resonant bar torques. Their arbitrary bounded odd
occupation already permits current-null choices in principle. Their principal
models stream; their LBK calculation neglects response self-gravity and uses
slow/asymptotic limits. The narrower conjunction tested here is a positive stationary
population in the null space of the entire local current field, a matched
complete even DF, and opposite whole-population work over a switched-off
cycle including induced gravity. This is a comparison with the inspected
examples, not a literature-wide “first” claim.

[Gherghinescu et al. (2026)](https://arxiv.org/html/2605.26225v1)
also compare oppositely rotating populations with the same complete even DF.
Their tested populations stream, their tracers omit gravitational backreaction,
and their imposed bar remains on. [Kataria & Shen (2024)](https://arxiv.org/html/2406.17113)
find different live-bar histories at fixed integrated spin, but similar histories
in their tested zero-spin cases. Neither experiment tests the simultaneous
pointwise current null and complete own-field switched-cycle work here. These
precedents restrict the claim; even matching and DF-sensitive bar evolution
alone are not new. [Primary-paper challenge](evidence.html#prior)

No global stability, nonlinear bar formation, dark-matter microphysics or
observed-galaxy match follows. The physical source radius is not a measured
stellar bar length, and a pattern speed is not a slowdown age.
[AH-PRIOR](evidence.html#prior)

## Reproducing the calculation

The existing portable cycle regenerates fresh orbits and the energy64 ×
circularity64 GL64 causal history. Its actual full-preset CLI run and closed
comparison agree with all 62 original saved arrays and 117 raw scalar targets
under the predeclared software tolerance. This closes central executable reproduction;
it is neither another independent physical method nor equivalence to the
separate E128 refinement. The source manifest identifies code, not a new
result. The immutable central bare capsule remains a distinct N8/N16
calculation, not a full-seven-mode pole runner.

[Delivery readiness](README.md) gives the unchanged runner,
precise fresh-output commands and assessed completion status. The updated outer
[release instructions](README.md) distinguish that completed
GL64 execution from the separate E128 refinement. The capsule's frozen README
retains its historical preparation-time pending status. Packaging, public
figure/evidence links and final rendered review remain pending;
no public release or deployment is asserted here.



[Exact assessed values and methods](evidence.html) · [Fresh executable reproduction](README.md).
