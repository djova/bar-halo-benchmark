# Reproduce bare complete-cycle halo work

This small NumPy/SciPy runner generates its own Plummer actions, orbital
Fourier coefficients and finite forcing history. It computes the total halo
work coefficient `W2` and axial angular impulse coefficient `J2` for five
fixed populations. It needs no archived trajectories, response scalars, host
services or campaign filesystem. The method is established collisionless
response theory; the experiment tests stronger matching of the initial DFs.

**Publication status:** source draft. Formula fixtures and both quick/reference
calculations still require the owner's metered numerical comparison against
the full campaign. No scalar benchmark or runtime is asserted here. The public
repository is intended to be [bar-halo-benchmark](https://github.com/djova/bar-halo-benchmark),
but this new folder and the proof companions are not yet published.
Before release the publisher must provide and bind
[MATCHING_AND_POSITIVITY.md](MATCHING_AND_POSITIVITY.md) and
[certificate.json](certificate.json). These pending companions are not runtime
inputs. The runner does not claim to certify global DF positivity numerically.

## Run

Use Python 3.11 or later. The pinned packages match the campaign's numerical
environment; other versions are recorded but not presumed equivalent.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run.py --check-formulas --output formulas.json
.venv/bin/python run.py --preset quick --output quick.json
.venv/bin/python run.py --preset reference --output reference.json
```

The default quick setting is GL32 in binding and circularity, with radial
Fourier modes `n=-16,...,16`. It is **coarse** and cannot qualify continuum
work or its sign. The reference setting is GL128/GL128 and `n=-64,...,64`;
the word reference denotes a reproducible setting, not a proven error bound.
Compare action orders and Fourier cutoffs separately. `--ne`, `--neta`,
`--radial-modes`, orbital orders and tolerance expose bounded refinements.
Changing `--omega`, `--duration`, `--ramp` or `--shape` changes the experiment.

BLAS/OpenMP thread settings are forced to one before scientific imports.
The default process allowance is 3,600 CPU seconds, 7,200 wall seconds and
2,048 MiB address space. The CLI permits bounded changes. Unix process limits
are installed when supported; portable cooperative time checks and their
limitations are recorded. No jobs are scheduled. An unresolved retained node,
resource limit or interruption produces failure, never a response with that
node silently deleted. Output files must be new. `complete=true` means the
configured calculation finished, not that it passed continuum qualification.

## Fixed physical inputs

Use `G=M=a=1`, `psi=(1+r^2)^(-1/2)` and
`H0=v^2/2-psi`. The positive baryonic source has mass `Mb=0.1` and density

\[
\rho_b=\frac{15M_b}{8\pi}(1+r^2)^{-7/2}
 \left[1+\varepsilon A(t)
 \frac{x_b^2-y_b^2}{1+r^2}\right],\qquad \theta=\Omega t.
\]

Here `(x_b,y_b)` are coordinates rotated into the source frame. For
`|epsilon A|<=1` the **total** source density is nonnegative. Its fixed
monopole potential is `-Mb(r^2+3/2)(1+r^2)^(-3/2)` and is already included
in `H0`. The halo density is

\[
\rho_h=\frac{3}{4\pi}\psi^5-\frac{15M_b}{8\pi}\psi^7,
\]

so the combined spherical potential is exactly unit Plummer and the halo mass
is `0.9`. The response ignores induced halo gravity. The quadrupole potential
per unit contrast is

\[
B=-\frac{3M_b}{14}(x_b^2-y_b^2)(1+r^2)^{-5/2}.
\]

The default cycle has `Omega=0.12`, `T=120`, equal rise/fall duration `R=12`,
and peak `A=0.8`. During either edge its normalized shape is
`s^3(10-15s+6s^2)`, with `s=t/R` or `(T-t)/R`; it is constant between edges.
The perturbation is zero at both endpoints. Work includes switching and
rotation. The script reports `rotation_W2=Omega*J2` and the remaining
`switching_W2` separately. Negative total `W2` is energy returned to the
external driver, not a prediction of freely increasing pattern speed.

## Initial halo populations

With binding `e=-H0`, define

\[
F_c=C\left[e^{7/2}(1-Qe^2)+L_z\sum_p c_p h_p(e,L^2)\right],\quad
C=\frac{24\sqrt2}{7\pi^3},\quad Q=\frac{14}{33},
\]

\[
h_p=-\frac{4p}{(p+5/2)(p+7/2)}e^{p-1}
       +\frac{4}{p+1}e^{p+1}+L^2e^p.
\]

The powers are `5,6,7,8,10,12`. The actual binary64 candidate A is fixed in
`run.py`: decimal round-trip representations are

```text
3.795853269534006   -135.59804126193885   678.294264313138
-800.1997907110583   259.1199993421909   -136.73855372860442
```

The populations are `F0`, `A_full_plus`, `A_full_minus`, `A_half_plus`, and
`A_nine_tenths_plus`. Signs and the exact binary halving reuse the full-A
certificate. The separately represented nine-tenths coefficients are embedded
explicitly; they have a separate exact certificate and are not rescaled during
analysis. JSON records every actual coefficient.

Each odd basis term has zero density and zero first velocity moment at every
position. Thus all five initially share density, pointwise zero mean velocity
and the entire velocity-reversal-even DF. They are stationary functions of
the common spherical invariants; zero current is not time-reversal invariance.
The full-support positivity certificate targets `F0/2 <= Fc <= 3F0/2` using
exact rational Bernstein inequalities on the combined polynomial, including
weak-binding and radial/circular limits. Sampled factor extrema emitted by
this runner are only diagnostics, never a substitute for that certificate.
The companion must state its exact binary vectors and proof operands.

## Quadrature and response normalization

GL rules cover `0<e<1` and `0<eta=L/Lc(e)<1`; there is no imposed binding,
radius, angular-momentum or inclination cutoff. Refinement reaches farther
into the same domain rather than defining new physical support. Circular
orbits satisfy `e=uc(1+uc^2)/2`, `Lc=(1-uc^2)/sqrt(uc)`. The action measure is

\[
(2\pi)^3\frac{L_c^2\eta}{\Omega_r}\,de\,d\eta\,d\mu,
\qquad -1\leq\mu=L_z/L\leq1.
\]

Inclination is **not** normalized by `1/2`. The computed physical mass is
reported against the exact `0.9`; weights are never empirically renormalized.
Every action node is retained. Turning roots use `u=psi`, a stable pericentre
gap from the radial polynomial and an analytically integrated angular pole.
Adjacent-node GL8/16/32 panels give cumulative phases. Successive orbital
orders check frequencies, radial action, Fourier coefficients, Parseval norms
and phases. Failures at the bounded maximum order stop the calculation.

Only the physical forcing radial function `phi_02=-r^2(1+r^2)^(-5/2)` is
needed. Complex spherical harmonics have angular squared norm `4pi`.
For both `m=-2,+2` and every `k=-2,0,+2`, exact inclination moments are
`Ak=(3/4,1/2,3/4)` and `Bk=Ak*m*k/6`. All signed radial Fourier modes are
included; the other azimuthal components have exactly zero external forcing.
This restriction describes this bare quadrupole, not a general stability test.

Let `nu=n*Omega_r+k*Omega_L`. The full derivative contraction includes

\[
\kappa=-\nu F_e+2kL F_{L^2}+mF_{L_z}.
\]

The nodal frequency is zero but its DF derivative is retained. Inclination
integration gives `hbar=C Ak[-a nu+b]`, where
`a=g_e+(m k/6)L h_e` and `b=m h+(m k^2/3)L^2 h_L2`.
There is no second DF-factor multiplication. The external harmonic amplitude
is `b_(+/-2)=3Mb/(7sqrt(30))`; its two conjugate components are both present.

For detuning `delta=nu-m Omega`, the exact symmetric quintic history is

\[
H(\delta)=0.8(T-R)e^{i\delta T/2}
 \operatorname{sinc}\!\left[\frac{\delta(T-R)}{2\pi}\right]
 p\!\left(\frac{\delta R}{2}\right),\quad
p(x)=\frac{15[(3-x^2)\sin x-3x\cos x]}{x^5},
\]

with `p(0)=1`; the implementation uses a convergent even series near zero.
The formula uses the configured peak shape in place of `0.8` when overridden.
There is no time integrator or midpoint approximation. If `R_nk` is the radial
orbital coefficient, the whole-population cycle coefficients are

\[
W_2=-\frac12\sum_{n,k,m}\int W_{\rm action}\,\bar\kappa_m\,
 \nu|R_{nk}b_mH|^2,\qquad
J_2=-\frac12\sum_{n,k,m}\int W_{\rm action}\,\bar\kappa_m\,
 m|R_{nk}b_mH|^2.
\]

The factor `1/2` accompanies the full conjugate-pair sum; no further folding
factor is applied. Actual weak finite-amplitude work starts at `epsilon^2 W2`.
Finite-amplitude orbital integration is a separate check, not performed here.

## Read the results narrowly

The script records physical coefficients, method/source hashes, package
versions, process costs, orbital errors, reality and bare-affine checks.
`W2(A)+W2(-A)=2W2(F0)` is an exact bare control. The monotone `F0` should
absorb. These related populations are not independent discoveries of a sign.

Omitted radial-Fourier diagnostics use numerical Parseval gaps weighted by the
actual DF derivatives, frequencies and forcing history. A monotone exact
history envelope sharpens them away from resonance. These are **proxies**, not
rigorous total response-error bounds; they do not bound action quadrature or
an unresolved weak-binding contribution. Raw unweighted action norms are not
meaningful tail tests. GL nodes are deterministic and not independent samples;
no IID standard error or confidence interval is manufactured.

This reproducer does not supply response self-gravity, unforced stability,
nonlinear rotor evolution, a stellar disk, formation from an isotropic
reference, or observational implications. Collective/stability/autonomous
qualification remains separate from the controlled bare result.

Established antecedents include [Nelson & Tremaine (1999), §2.3](https://arxiv.org/pdf/astro-ph/9707161)
for complete work and response theory, [Perez & Aly (1996)](https://arxiv.org/pdf/astro-ph/9511103)
for dynamically accessible energy and odd DFs, and
[Chiba & Kataria (2024)](https://arxiv.org/html/2311.07640v2) for odd-DF torque
gradients at fixed density. [Nelson & Tremaine (1995)](https://arxiv.org/pdf/astro-ph/9408068)
already give nonrotating halo energy emission when the even DF changes.
The additional question here is the stronger exact initial matching.
See the pending public theorem companion for its full algebra and scope.

The portable implementation is a minimal extraction of the campaign's own
orbital, polynomial and window code patterns. Ancestor source hashes identify
that relationship; it is not an independently derived numerical method.
The code is intended for the benchmark's MIT public release. Publication,
clean proof packaging and benchmark binding belong to the repository owner.
