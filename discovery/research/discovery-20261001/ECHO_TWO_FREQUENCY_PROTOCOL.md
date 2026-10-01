# Spherical halo echoes with nonzero apsidal harmonics

Frozen design review1 October2026, before a new spatial-multipole response is measured. Complete the radial controls first. Initial source/harmonic/profile pilot cap100CPU seconds, one nice10 thread; no large angular tensor or live disk is authorized by this pilot.

## Correct interpretation of the original quadrupoles

Both original spatial pulses have physical azimuthal m=2. In a planar orbit, their same-sign m=4 sum does not provide a post-second-pulse azimuthal echo. However, this argument does not apply unchanged to an inclined spherical orbit. Let i be inclination, h the fixed node, and psi the in-plane orbital angle. Then

```
(x+iy)^2/r^2 = exp(2ih) [sin^2(i)/2
                  + (1+cos^2(i)) cos(2psi)/2 + i cos(i) sin(2psi)].
```

Thus each physical m=2 field contains apsidal harmonics ell=0,±2. The node has zero background frequency. Two ell=0 radial harmonics can refocus at2tau and produce an m=4 gravitational potential, whose orbit-plane average contains an ell=0 term proportional to sin^4(i). Our original two-angle Fourier audit explicitly holds `theta_phi-theta_z` fixed and finds these radial channels. The original quadrupole result remains **unresolved**, with serious quadrature failures; it is not disqualified by the planar m argument and does not demonstrate the destruction of a correctly designed two-frequency echo.

For the new test, use physical m=2 first and m=4 second. In canonical spherical coordinates `(theta_r,theta_L,node)` conjugate to `(Jr,L,Lz)`, the declared pair is

```
k_A = (-1,-2,-2), k_B = (2,4,4) = -2 k_A,
k_out = (1,2,2).
```

Both dispersive phases cancel at2tau: radial and apsidal. The physical node phase has zero frequency. Report three families separately: radial-only (`m_r≠0,m_L=0`), apsidal-only (`m_r=0,m_L≠0`), and two-frequency (`m_r≠0,m_L≠0`). The declared pair belongs to the last family. This is collinear Fourier-vector rephasing, not a claim that arbitrary noncollinear vectors can universally refocus. The isochrone Hessian in Jr,L has determinant `-3 Lambda''(L) I^-7`, with `Lambda''=1/(L^2+2)^1.5`, so its two dispersive frequencies are independent at finite actions.

## Positive source with an exact potential

Here M_I is **time-integrated external mass**, in reference-halo mass×time units. The source is a time-integrated positive density; an actual finite pulse needs a separate time profile. Let x=r/s, l=2 or4 and

```
rho_I = rho_Plummer(M_I,s)
        {1 + epsilon [2x/(1+x^2)]^l sin^l(theta) cos[l(phi-phi0)]}.
```

Since `2x/(1+x^2)≤1`, `|sin^l(theta)cos(l phi)|≤1` and `|epsilon|<1`, the density is everywhere positive, with minimum at least `(1-|epsilon|)rho_Plummer`. Its total integrated mass is M_I because the angular term integrates to zero. The multipole has a finite radial moment and is smooth at the center.

Its integrated potential is exactly

```
psi = -M_I / sqrt(r^2+s^2)
      - 3 M_I epsilon 2^l / [(2l+1)(2l+3)s]
        x^l / (1+x^2)^(l+1/2)
        sin^l(theta) cos[l(phi-phi0)].
```

For the solid harmonic `Q_l=Re[exp(-il phi0)(x+iy)^l]`, the independent Poisson identity is

```
Laplacian { Q_l (r^2+s^2)^(-l-1/2) }
  = -(2l+1)(2l+3) s^2 Q_l (r^2+s^2)^(-l-5/2).
```

Verify its coefficients with an independent finite-difference Laplacian, then compare the analytical Cartesian velocity kick with finite differences of psi. Check first-order canonical action/angle changes against derivatives of the same psi. A positive source and an exact kick do not prove a realistic moving satellite or gas history.

Freeze s_A=0.8,l_A=2,phi_A=0 and s_B=1.6,l_B=4,phi_B=pi/8; epsilon_A=epsilon_B=0.5. Freeze integrated masses M_A=0.006,M_B=0.010 and a factor-of-two smaller amplitude control. The initial DF is the same95.21629%-mass tapered cohort as the radial screen, with absolute weights. A global gradient triangle bound, including both positive monopoles, must prove bound support before any finite trajectory run.

## Shape contrast and what it measures

All four shape-sign cases share both positive monopole pulses. Use epsilon_A=±0.5 and epsilon_B=±0.5 and form the signed complex contrast

```
D = [C(++ ) - C(+-) - C(-+) + C(--)] / 4.
```

One-pulse controls cancel algebraically, but retain them for equilibrium, relaxation and work audits. This isolates the leading angular bilinear response, removing monopole×angular contamination. Finite monopole impulses change actions and frequencies at higher order; they are not magically removed from finite-amplitude trajectories. The phase-intervention and memory controls still need independent treatment.

The primary readout is the imaginary equatorial l=m=2 Newtonian potential coefficient, averaged over the original width0.1 annulus atR=1. Preserve its sign and complex phase. Save its actual annulus-averaged radial and tangential force coefficients, without replacing them with a central-radius derivative. The basic angular moment selects A's negative node harmonic and B's positive node harmonic. An m=6 sum is secondary and has no corresponding generic post-pulse refocusing. Twelve apsidal and sixteen node samples are a minimal leading-order angular check; neither count establishes finite-amplitude convergence.

## Cheap harmonic route before a tensor calculation

The orbit-plane solid harmonic obeys

```
(x+iy)^l/r^l = exp(il node)
   sum_h binom(l,h) A^(l-h) B^h exp[i(l-2h)psi],
A=(1+cos i)/2, B=(1-cos i)/2.
```

With `psi=theta_L+chi(theta_r,Jr,L)`, the radial Fourier coefficients need only a grid in E,L,theta_r. Inclination factors are low-degree polynomials. Their products and derivatives in this l2×l4×l2 response can be integrated with five Gauss–Legendre inclination nodes; node selection is exact. Those nodes are used in polynomial algebra, not passed through the polar AGAMA map.

For a general pair k,n, m=k+n, the integration-by-parts leading readout is

```
R_kn = integral dGamma (k dot grad f0) U_A,k
        [ (m dot grad U_B,n) O_-m
          + U_B,n (n dot grad O_-m)
          - i(t-tau) (n dot grad(m dot Omega)) U_B,n O_-m ]
        exp[-i(m dot Omega*t - n dot Omega*tau)].
```

Check canonical signs against the existing one-angle result and a two-angle constant-Hessian Gaussian benchmark. Boundary terms vanish when the physical harmonic coefficient and the normal Fourier component are handled together; pole/circular boundaries must be audited rather than dropped by convention. In `(Jr,L,Lz)`, derivatives of inclination coefficients contribute through `cos i=Lz/L` and cannot be omitted.

First profile with no more thanE64,L8,radial128 Fourier samples and declared readout dates around2tau. Record radial-only and nonzero-apsidal pieces, source positivity, map/gradient checks and actual cost. Refine only a resolved channel. A leading-order halo-force prediction is a mechanism screen; finite-amplitude confirmation, memory erasure, self-gravity and stellar response remain separate gates. Closest primary predecessor remains [Chiba et al., *Galactic echoes*](https://arxiv.org/html/2506.16512v2).

## Measured source/profile gate

The [positive-source preflight](../../results/discovery-20261001/echoes/multipole-source-01/result.json) completes in0.235 full-process CPU seconds. It verifies both shape signs: finite-difference Poisson relative error≤5.64×10^-8, Cartesian gradient difference≤1.42×10^-12, density at least0.5 times the positive Plummer source everywhere by proof, and canonical impulse errors decreasing with impulse strength. The global two-pulse binding-loss bound is0.0101652, preserving at least0.00983482 binding energy for the frozen initial cohort. These proofs include common monopoles.

The leading predictor [echo_two_frequency.py](../../scripts/discovery/echo_two_frequency.py) integrates orientation polynomials exactly, and compares its independent inclined-orbit geometry against the Cartesian mapper to3.45×10^-15. An independent integral of the unsmoothed Newtonian force verifies the actual annular radial-force estimator to8.4×10^-17. The two-angle constant-Hessian Gaussian canonical check agrees with its closed characteristic function to2.83×10^-13. Its E64,L8,phase128,nmax8,13-date pilot costs2.14 full-process CPU seconds. This is cheap enough to refine before interpreting amplitudes.

Failures are preserved: pilot01 failed a broadcasting expression in the independent Gaussian check; pilot02/03 exposed the check's incorrect `k=+K` gradient sign despite declaring the echo pair `k=-K,n=N`. Correcting the benchmark sign restores its analytic agreement. No physical response was measured in those failures. This correction did not alter the halo-response formula, whose f-gradient is evaluated for its signed Fourier vector.

All source/configuration snapshots are saved before numerical evaluation. The leading angular contrast omits higher-order frequency/action changes due to finite common monopoles; direct first-order monopole potential and force readouts are saved separately. It therefore predicts a channel and cost, rather than already proving physical finite-amplitude refocusing.

The E512,L24,phase512,nmax16 refinement costs172.68CPU seconds. E256→512 with these simultaneous refinements changes the genuine two-frequency radial-force channel by0.21% of its peak, potential4.05%, and total channels roughly5%. Independent direct Poisson-bracket integration costs174.58s and agrees with the integration-by-parts two-frequency potential and force to1.7×10^-8 and3.8×10^-8 of peak. Full total radial force agrees to0.015%; it includes less well-converged nonrefocusing channels. This independently tests the inclination derivatives and action-boundary treatment rather than merely reusing the one-angle timing relation.

The fixed physical two-frequency force coefficient is8.84×10^-9, corresponding to0.052ppm of the reference force after its azimuthal conjugate is included. The total predicted radial-force field is0.066ppm, tangential0.040ppm. These quantities are unamplified halo fields, not a stellar-structure prediction. No finite-amplitude spatial matrix is advanced on this usefulness result.

The13-date mixed-response profile samples the early first-A response only at2,4 and misses a large transient near1. Its apparent53% potential and47% tangential-force relaxation ratios were therefore unreliable. A separate first-only screen including1,2,3,4,5 initially gave3.9%, but a mean over those selected dates was also an inadequate estimator. The final criterion is **time-integrated RMS over0..8**, with the same integral definition over each fixed pre-B window0.75tau..tau. All four candidate separations16,32,48,64 were specified before this refined readout.

E512,L24,phase512,nmax16 first-only screens at temporal cadences1,0.25,0.125 retain the actual complex field. Cadence1 underestimates the early radial-force RMS by19%; the two finer steps agree to0.0018% early radial RMS, and their tau16 pre-B radial RMS to0.033%. E1024,L32 at cadence0.125 verifies the tau16 late RMS to2.3×10^-6 relative to E512,L24. Final tau16 ratios are3.48% potential,4.07% radial force and3.49% tangential force. At tau48 they are0.890%,0.0666%,0.878%. Tau64's already tiny radial residual changes2.2% under the energy/L refinement; it is not used to establish an echo. This temporal-control failure is distinct from the earlier stochastic quadrupole's47% ratio, which used a different pulse shape and remains its own sampled diagnostic. None of these quiet-readout measurements is finite-amplitude echo confirmation.

Final records are in [two-frequency-readback-02](../../results/discovery-20261001/echoes/two-frequency-readback-02/result.json). No finite trajectory matrix or live disk was launched: the below0.1ppm usefulness gate fails even though a quiet first-pulse gravitational readout can be established. Total echo-branch recorded CPU is4,783.55s plus11.7797s failed-pilot lower bound at16:34UTC, with older startup and brief read-only inspections unmetered, within the original two-hour cap.
