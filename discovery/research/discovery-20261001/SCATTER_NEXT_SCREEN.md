# A stronger collision comparison: full conditional drift and raw second tensor

This design addresses a limitation found in the first experiment. Viscosity
and measured shear matching leave the local resonant-action drift/diffusion
tensor undetermined. The following two positive elastic laws match that
entire tensor for the linear action J=v_x in the reference gas, while retaining
different higher angular harmonics. Root independently checked the algebra.

For an equal-mass event define u=v1-v2, g=|u|, c=cos(theta), M1=E[c],
M2=E[c^2], and uniform azimuth. The conditional jump moments are

```
E[delta v1] = (M1-1) u/2
E[delta v1 delta v1^T]
    = g^2(1-M2) I/8 + (3M2+1-4M1) u u^T/8.
```

The generators multiply these by the actual velocity-dependent event rate,
not a constant average collision frequency. Use the following all-forward
laws, without backward label exchange or artificial zero-angle events:

| Law | Distribution of c | M1 | M2 | Rate at fixed g |
|---|---|---:|---:|---:|
| A | c=0 with probability1/4; c=2/3 with probability3/4 | 1/2 | 1/3 | Gamma_A(g) |
| B | c=1/3 always | 1/3 | 1/9 | 3 Gamma_A(g)/4 |

Both viscosity cross-sections equal kappa because sigma_total,A=kappa/(2/3)
and sigma_total,B=kappa/(8/9). Thus at every relative speed and density
Gamma_A=rho*g*3*kappa/2 and Gamma_B=3 Gamma_A/4. Both give exactly

```
velocity drift = -Gamma_A(g) u/4
raw second tensor = Gamma_A(g) g^2 I/12.
```

This matches the full conditional first two increments of J=v_x. It is stronger
than scalar viscosity matching. Nonlinear energy-increment second moments
involve higher velocity increments and are not matched; real halo actions are
not linear v_x and would need a fresh derivation.

The fourth angular harmonic is E[P4(c)]=-49/216 for A and1/81 for B.
The l=4 eigenvalues are Gamma_A*265/216 and Gamma_A*20/27, ratio53/32,
while l=2 and the conditional velocity tensors match. Angular-harmonic freedom
is known kinetic physics; this construction is a better controlled experiment,
not a new particle theory.

Both transition probabilities depend only on the incoming/outgoing direction
dot product. Reversing the pair event has the same kernel; exact pair energy
and momentum and Maxwell detailed balance are preserved. Ideal fixed-angle
rings are reference operators, not a claimed realistic SIDM differential
cross-section. No Gaussian truncation is used.

The earlier symmetric-ring idea (c=+-1/sqrt(3) versus a mixture0,+-a) also
matches raw moments, but backward events complicate tagged-action interpretation.
The all-forward construction replaces it before any new-law outcomes.

The bounded implementation uses scatter_moment_screen.py, with an unchanged
conservative engine and separate wrapper/protocol hashes. Its controls and
either-sign criteria were frozen after the delta=.05 stage closed, in
[SCATTER_MOMENT_PROTOCOL.md](SCATTER_MOMENT_PROTOCOL.md), within the original
combined 2-core-hour ceiling. The original waveform is calibration selected
from earlier results; new-law outcomes on the second waveform are prospective
but that waveform has already been used with other collision laws. Terminal
outcomes are summarized in [PUBLIC_TERMINAL_BRANCHES.md](PUBLIC_TERMINAL_BRANCHES.md).
The full `SCATTER_FINDINGS.md` is an archived findings record, not a file supplied
by this limited release.

## A continuous positive-law extension, derived but not evolved

The conditional match need not require infinitely thin angular rings. This
extension was derived while the frozen A/B runs were in progress and does not
change their kernels, endpoints or gates. Let h be a full cosine-band width,
with 0<h<.5. Define a smooth-band A law as the following mixture:

```
central band: uniform c in [0,h], weight p=(1+h)/(4-2h)
side band: uniform c in [c_A-h/2,c_A+h/2], weight 1-p
c_A=(4+h)/6.
```

Its exact M1=1/2 and M2=1/3 follow by mixture moments. Define B as a uniform
band centered on `c_B=(2-sqrt(1-3*h^2/4))/3`, of the same full width h.
Its M2=c_B^2+h^2/12 satisfies `3 M2+1-4 M1=0`. Matching viscosity gives
`Gamma_B/Gamma_A=1/[2(1-c_B)]`; multiplying its conditional drift and raw
second tensor yields the same `-Gamma_A*u/4` and `Gamma_A*g^2 I/12` again.
All cosines remain between zero and one. These are finite-density positive
reversible angular kernels; sharp band edges can be separately regularized.

For h=.1, c_A=.683333, p=.289474, c_B=.334586 and rate ratio .751412.
The fourth angular decay ratio remains 1.59855, close to the zero-width
53/32 value. This removes a need for delta-angle support algebraically.
No sampler, Maxwell evolution or forced-response result for these finite
bands is included in the initial screen. Any robustness claim would require
a separately frozen validation and response experiment.
