# Independent radial harmonic prediction

This note records a second-order prediction before comparison with the exact spherical-pulse response. It is an extension of established collisionless echo theory, not a new basic mechanism. The physical model, taper, absolute normalization and frozen readouts remain those in [ECHO_MONOPOLE_PROTOCOL.md](ECHO_MONOPOLE_PROTOCOL.md).

At fixed total angular momentum L, the spherical impulse is a Hamiltonian perturbation `a_i U_i(J,theta)`, with J=Jr and theta the radial angle. Throughout this note E is **positive binding energy**, `E=-E_orb`, where the physical orbital energy `E_orb=v^2/2+Phi0<0` for bound orbits and `Phi0(infinity)=0`. Define Fourier coefficients by `U(theta)=sum_k U_k exp(i k theta)`. The equilibrium f0 is independent of theta, and Ω(J,L) is the radial frequency. Liouville's equation gives the first pulse perturbation

```
f_A^(1) = f0'(J) d_theta U_A.
```

Immediately before pulse B, its k coefficient is `i k f0' U_A,k exp(-i k Ω tau)`. Applying the second pulse through `-{f_A^(1),U_B}` and drifting to t gives a mixed pair `(k,n)` with final harmonic `m=k+n` and phase

```
exp[-i (m*t - n*tau) Ω(J,L)].
```

Thus `(k,n)=(-1,2)` and its complex conjugate refocus at2tau, while `(-2,3)` refocuses at3tau. Nonrefocusing pairs also exist; a physical mass pulse excites many harmonics. This is why a late feature alone does not establish an echo.

For the angle-dependent observable O(J,theta), integrate the action derivative by parts. The resulting coefficient of a_A a_B is

```
R_kn(t) = integral dGamma_JL f0'(J) U_A,k
          [ k*m U_B,n' O_-m
            + n*k U_B,n O_-m'
            - i*n*k*m*(t-tau) Ω' U_B,n O_-m ]
          exp[-i (m*t-n*tau) Ω].
```

The measure is `dGamma_JL=(2pi)^3*2L*dJ*dL`, with the radial angle already averaged. Primes denote J derivatives at fixed L. The outer action boundary has zero tapered DF. At the circular boundary, nonzero radial harmonics vanish; the relevant boundary product vanishes. Numerical refinement still checks endpoint behavior.

For the canonical constant-shear control, U_A,-n1=U_B,n2=1/2, O_-m=1 and Ω'=s. The only remaining bracket term integrates `f0' exp(-i delta Ω)` to `i delta s exp[-i Ω0 delta-(sigma*s*delta)^2/2]`. This recovers the previously derived mixed-mode formula, including its sign and zero at exact refocusing. That is an independent convention check.

The numerical implementation evaluates Fourier coefficients of the actual Plummer impulse potentials and the actual Newtonian potential averaged over the frozen R=1 annulus. The potential convention is negative, `Phi=-G integral dm/max(r,R)` for the spherical readout; adding positive mass makes its contribution more negative. The radial-force convention is negative for inward acceleration. Mixed responses remain signed and can have either sign. The implementation differentiates coefficients with symmetric steps in J at fixed L, and separately tests step size, Fourier truncation and energy/L/radial-angle quadrature. The isochrone derivatives are `Ω=(2E)^1.5` and `dΩ/dJ=-3Ω^2/(2E)`. It also saves the first-order A-only gravitational response.

Required controls are: negligible imaginary residual for the real spherical observable; zero first-order response immediately at A; zero total mixed position readout immediately at B as Fourier resolution increases; convergence of the individual refocusing channels and full sum; and agreement of `a_A*a_B*sum R_kn` with the small-positive-pulse Eulerian and forward calculations. A passing perturbative channel is not evidence of a finite-duration, self-consistent or stellar response.

For a monopole, a varying outer shell can add a spatially constant inner potential without exerting force there. Therefore the frozen R=1 potential is a halo-memory observable, but a dynamical radial readout additionally requires converged radial force, enclosed mass or potential differences. The independent prediction can evaluate the annular R=1 radial force and `Phi(0.5)-Phi(1)` without changing the primary coefficient. This qualification applies even if the primary potential passes every echo control.

Source: [echo_monopole_response.py](../../scripts/discovery/echo_monopole_response.py). Closest primary predecessor: [Chiba et al. (2025), *Galactic echoes*](https://arxiv.org/html/2506.16512v2).
