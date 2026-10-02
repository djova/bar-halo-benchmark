# Warm radial target: equivalence to the original inclination population

Readback2026-10-01, before preparation of physical pilot source.
The radial formulation retains the original intended stellar population
for spherical energy observables. It integrates the inclination and orientation
variables analytically; it does not replace inclination.03 with zero.
It is an independent numerical realization of the same analytic target,
not an exact reuse of the original mapped particles or approximate gas table.

## Original frozen stellar construction

`feedback_cusp_weak.py`, in `prepare`, draws the physical guiding law
p_Rc(Rc)=Rc exp(−Rc), normalized onRc>0, with a known importance proposal.
It sets vc²=Rc Phi'(Rc), kappa²=Phi''(Rc)+3Phi'(Rc)/Rc,
Js=(.1vc)²/kappa, L=Rc vc, Jr from an exponential of meanJs,
i from Rayleigh scale.03, andLz=L cos(i). It passes spherical actions
(Jr,Jz,Jphi)=(Jr,L−|Lz|,Lz) to AGAMA and draws all three canonical
angles independently uniform on[0,2pi). Its force source is the same
Hernquist+finite gas potential used by the proposed radial experiment.
The tilt distribution is a fixed physical part of the model, separate
from the guiding-radius importance proposal.

The original code's exact target p_Rc follows from its Gamma2 inverse CDF;
its saved star_weight is the reciprocal mixture-density ratio. Reweighting
the original response families does not implicitly condition their action
window. The proposed pilot samples a different full-support proposal and
uses explicit density ratios to the same physical target.

## Full canonical measure

The circular mapRc->L is monotone: L²=Rc³Phi', so
dL/dRc=Rc³kappa²/(2L)>0 in this actual potential. Write
p_L(L)=p_Rc(Rc)/(dL/dRc).

Let P_i(i)=i/.03² exp[−i²/(2*.03²)] fori>=0. The conditional inclination
pushforward is

P_z(z|L)=sum_{i>=0: cos(i)=z/L} P_i(i)/(L|sin(i)|), −L<z<L.

Every preimage is included; the mathematical Rayleigh support has not
been truncated to prograde inclinations. The endpoint degeneracies have
measure zero and the pushforward remains normalized. At fixed sign ofLz,
dJz dJphi=dL dLz becauseJz=L−|Lz| andJphi=Lz have Jacobian1.
Therefore the ideal full phase-space DF in canonical action-angle measure is

f(Jr,L,Lz)=p_L(L) P_z(Lz|L) exp(−Jr/Js(L)) /[(2pi)³ Js(L)].

IntegratingLz and the two orientation angles produces

p_L(L)dL × exp(−Jr/Js)dJr/Js × dtheta_r/(2pi).

Spherical radial dynamics has dr dp_r=dJr dtheta_r at fixedL. Changing
back toRc gives exactly

p_Rc(Rc)dRc × g_L(E)dr dp_r,
g_L(E)=exp[−Jr(E,L)/Js(L)]/(2piJs(L)).

Both the unforced radial energy and the entire spherical pulse/map depend
onL,Jr,theta_r and notLz or the two orientation angles. Their integration
is consequently exact for energy, inverse capture and the radial primitive.
The.03 tilt remains in the marginalized physical model. No additional
mass factor, selection probability or orientation renormalization appears.

## Explicit proposed weights and cohorts

With guiding proposalq_Rc and conditional radial proposalq_L(r,p_r),
the ordinary energy operand is

[p_Rc/q_Rc] [g_L(E)/q_L(r,p_r)] DeltaE.

The positive forward-control operand is

[p_Rc/q_Rc] [R_L(E,E_f)+capture_L(E,E_inverse)]/q_L(r,p_r).

The physical target is normalized exactly by its defining canonical measure;
its computed Monte Carlo mass is checked against1, not divided back to1.
For a declared guiding cohortRc<c, multiply by its indicator and divide by
the independently known massM(c)=1−(1+c)exp(−c). That operation reports
energy per unit cohort mass; the absolute physical energy remainsM(c) times
the reported conditional value. No instantaneous radial cut, action-window
normalization or outcome-dependent cohort replaces this guiding selection.

## Numerical qualifications and observables not recovered

The old AGAMA setup uses a spherical Multipole gas approximation on4096
radial points and a repaired ActionMapper. Its finite-phase Fourier averages,
action reconstruction and direct analytic-force integration have the recorded
mapping/trajectory limitations. The proposed direct radial integral uses
the actual analytic potential. Thus equality of the intended analytic stellar
population is exact; equality to the old numerical mapped-particle distribution
is only approximate and must be checked, not assumed. The new variableL
action implementation must first match the independently checked scalar
radial implementation and preserve its normalization/support controls.

Marginalizing orientation does not recover finite radial or vertical velocity
dispersion, thickness, bar response or the post-pulse phase distribution of
visible structure. Even conserved inclination can coexist with vertical
expansion if orbital radii change. Any such observable would require restoring
the original tilt/orientation distribution and an appropriate phase/velocity
measurement. A radial energy result alone is not old-disk survival.

Frozen source provenance: original warm construction
`feedback_cusp_weak.py` SHA
`35e0bb53990c8f50091703661d43a2f5a29756d866f13abfd5ea3cf1d1bb60a0`.
Its saved initial family arrays SHA
`9cc039eff46d440c576c51a1465b1c7377c240590466af18be59ad2cd778f0da`.
The prospective scalar radial source derives from the executed known-map
version SHA
`f911acef5c130586637608f29cf5c00c0a2bd9c46a98fe16a1b6891d140cd8a5`;
its later stdout-only repair changes no physical target or action algorithm.
