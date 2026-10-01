# Modified inertia: a bounded frequency-domain screen

Frozen before the first numerical screen, 1 October 2026. This branch evaluates
the proposed filters and exact harmonic histories; it does not evolve a galaxy.

The underlying equation is the scalar frequency-space inertia law, with the
force evaluated on the unknown modified trajectory. We select
`mu(x)=x/(1+x)`, `a0=1`, and `Theta_q(y)=2/(1+|y|^q)`, `q=2,4,8`.
The q=2 function is explicitly a published example, not a new function.
[Milgrom 2022, v3, equations 3, 20, 27–32 and page 12](https://arxiv.org/pdf/2208.07073v3).

For distinct separable harmonic modes with RMS amplitudes r_n, solve

```
A_n = sum_k omega_k^2 r_k Theta_q(omega_k/omega_n)
omega_n^2 mu(A_n/a0) = omega_N,n^2
```

Amplitudes carry length units and A carries acceleration units. No dimensioned
time parameter is added. A cosine's peak amplitude is sqrt(2) times its RMS
amplitude. Modes at an exactly common frequency must first be grouped into one
complex vector amplitude; summing their scalar norms gives a different model.

The frozen benchmarks are: all three q values; single-frequency r=.8 and
omega_N=.7 at a0=1e-8,1,1e8; two axes with omega_N=(1,R),
R=.25,.5,.9,1.1,2,4 and RMS amplitudes (.15,.15B),
B=.03,.1,.3,1,3,10,30. Each two-axis solve starts from .3,1,3 times the
Newtonian frequencies. Require logarithmic equation residual <1e-10,
independent initial-guess frequency spread <1e-8 and agreement <1e-10 with
the single-frequency quadratic solution. Test the on-solution modified
harmonic energy and dP/dt=F, with relative residuals <1e-10.

These conservation expressions are explicit for these orthogonal harmonic
modes only. They do not establish a general initial-value problem or a
causal response to imposed forcing. Published construction defines nonlocal
conserved quantities, and does not prove general history uniqueness.

Record the q-dependent frequency range. Separately diagnose the exact versus
near-degenerate frequency limit and the contamination estimate
`(a_internal/a_external)*Theta(omega_internal/omega_external)` at acceleration
ratio 1e12 and frequency ratios 1e2,1e4,1e6. These are structural checks,
not a fit to stars, galaxies, or microscopic stellar accelerations.

All results, source/protocol hashes and actual CPU time go to
`results/discovery-20261001/inertia/`. A successful screen qualifies an exact
reference problem; its relevance to observed vertical or radial motions
remains untested.

Implementation correction after screen-01: a sampled strict-decrease assertion
failed when Theta_8 rounded to exactly 2 at tiny arguments. The function's
derivative is `-2q y^(q-1)/(1+y^q)^2 < 0` for positive y. Screen-02 checks
nonincrease in floating samples and the analytical derivative sign. The
model, parameter matrix, tolerances and observed frequency results are
unchanged; the original failing artifact is retained.
