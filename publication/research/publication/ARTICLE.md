# Finite-time population bias in noisy sweeping resonances

*A response-kernel benchmark and an operational test of population approximations*

{{RELEASE}}

## Abstract {#abstract}

A local resonance calculation must specify which orbital population its dynamics act upon. We demonstrate **finite-time population-selection bias in a prescribed noisy sweeping-resonance model**, and provide a reproducible response-kernel diagnostic and variance-reduced estimator for assessing that bias. At matched central density and slope, a selected Gaussian and reference-halo weighting in the tested action slice give opposite early noise effects. Their later suppression magnitudes differ by a factor of **{{RATIO}}**. A slope-matched exponential closely follows the halo calculation. At one new sweep rate, all **eight advance 5% qualifications** survive independent numerical comparison; four other accurate comparisons are conservatively rejected.

This is a bounded computational-methods result. It does not establish a new physical torque mechanism, a complete halo torque, or a validated prediction for a live galaxy. The galaxy simulations are collisionless. The local noise model is not a calibrated SIDM collision operator. **These experiments do not test CDM against SIDM.**

[Learn the foundations](learn.html) · [Inspect and reproduce](reproduce.html) · [Claim registry](claims.json) · [Download this article](paper.md)

## Which physical system is being discussed? {#models}

{{MODELS}}

The results below concern model **RES-POS**, a positive initial population in a local resonance with imposed noise. Earlier signed-perturbation calculations with reservoirs (**RES-SIGNED**) have different initial and boundary conditions. They are retained as supporting experiments, not interchangeable resolutions of RES-POS. The original self-gravitating galaxies motivate the question; they do not validate the reduction. Even a successful prescribed-field Cartesian test would still leave collective live-halo response untested.

## What was already known? {#previous-work}

[Hamilton, Tolman, Arzamasskiy & Duarte](https://arxiv.org/abs/2208.03855) studied how diffusion sustains stationary resonant friction, including an initially linear local distribution. [Chiba](https://arxiv.org/abs/2305.00022) studied moving-resonance feedback, compared collisionless reduced dynamics with three-dimensional calculations, and anticipated that diffusion can replenish a friction-producing gradient while erasing a trapped–untrapped density contrast. [Ogilvie & Lubow](https://doi.org/10.1111/j.1365-2966.2006.10506.x) treated a related migration–diffusion competition at planetary corotation in gas. Different physical assumptions prevent treating that analogue as a galactic-halo prediction.

Variance reduction also has direct astrophysical predecessors. [Elbers et al. (2021), sections 2–2.3](https://arxiv.org/pdf/2010.07321), use a δf decomposition to sample departures from a model neutrino distribution and explicitly formulate its control-variate interpretation. Their cosmological calculation includes gravitational feedback. Here the control instead uses a zero-integral primitive identity for accumulated bar impulse under a prescribed canonical map. This is a useful comparison of constructions and assumptions; equivalence, optimality and priority of our specific estimator remain unestablished. We do not claim the control-variate principle as new.

Our addition is the quantified population counterexample, a reusable recorded response calculation, and a prospectively tested accuracy procedure with a measured estimator-cost comparison. A targeted literature review is not an exhaustive priority search. [Detailed scholarly positioning](diagnostics/population-accuracy/SOURCES.md).

## Model, populations and observable {#model}

The implemented frequency gradient is negative. In dimensionless slow action \(j\) and resonant angle \(\psi\), measured relative to the moving resonance:

<div class="equation-label" id="EQ-DYN-01">EQ-DYN-01 · Reduced dynamics</div>

```math
\begin{aligned}
\mathrm d\psi &= -j\,\mathrm dt,\\
\mathrm dj &= (-\sin\psi-s)\,\mathrm dt + \sqrt{2D}\,\mathrm dW_t,\\
D &= \frac{2\eta}{\pi}.
\end{aligned}
```

<div class="equation-label" id="EQ-OBS-01">EQ-OBS-01 · Accumulated bar impulse</div>

```math
B(T)=-\int_0^T\sin\psi\,\mathrm dt.
```

The accumulated bar impulse \(B\) excludes the moving-coordinate term \(-sT\) and Brownian impulse. The path budget checks all three separately. Our response is **noise minus smooth accumulated bar-mediated transfer**, not instantaneous torque. Positive means more transfer from the imposed bar to the sampled slice. Negative means less than the smooth control, and need not mean that the bar gains angular momentum.

The initial resonant phase is uniform. The reference is an analytical isochrone-halo distribution function evaluated at fixed fast actions: radial action 0.08 and vertical action 0.05, central slow action \(J_{s,0}=0.25\). Set \(x=(J_s-J_{s,0})/u\), \(u\approx0.0005633691\). The initial logarithmic slope is \(g\approx-0.0047493212\). Before the common compact window:

<div class="equation-label" id="EQ-POP-01">EQ-POP-01 · Initial populations</div>

```math
\begin{aligned}
w_{\mathrm H}(x)&=\frac{f_{\mathrm{halo}}(J_s;J_r,J_z)}{f_{\mathrm{ref}}},\\
w_{\mathrm E}(x)&=\exp(gx),\\
w_{\sigma}(x)&=\exp\!\left(gx-\frac{x^2}{2\sigma^2}\right).
\end{aligned}
```

Central density and slope are held fixed; populations are **not renormalized to unit mass**. The primary window has plateau 24 and cutoff 40; the wider comparison has plateau 48 and cutoff 64 in x. Moving this physical taper differs from enlarging the solver domain or auxiliary sampling support. These are conditional contributions from one slice, not integrals over an entire halo.

All response tables display dimensionless \(\int wK_B\,\mathrm dx\). Multiplication by \(4u^2(2\pi)^3 f_{\mathrm{ref}}\approx2.7022892\times10^{-6}\) gives the angular-momentum contribution **per unit fast-action area** in the analytical model's units. The local time T is dimensionless; it is not the original galaxy's Gyr clock. T = 20 is about 3.18 reference librations. [Exact calibration, windows and numerical algorithms](population-methods.html).

## Population choice changes the finite-time answer {#population-result}

{{CLAIM:POP-01}}

{{FIG-POP}}

{{POPULATION_TABLE}}

**Figure F-POP-01.** Sweep s = 0.25, imposed noise η = 0.1, cutoff 40, two recorded endpoints. Intervals are pointwise 95% Student-t intervals across eight independent trajectory batches, with paired controls retained separately. The early signs survive the declared timestep/window allowances. The late ratio is conditional on this population, slice and duration. [Complete values and numerical controls](results/populations.json); [interactive weighting](population-response.html#population-explorer). Analysis version and checksums: [DS-POP](datasets.json).

The exponential's point differences are about 0.050% and 0.068%. These are not certified sub-0.1% accuracies. The paired sampling and numerical assessment is in [the difference record](diagnostics/population-accuracy/joint-error-assessment.json). Matching a slope at one point can impose the wrong curvature; preserving the gradient over the sensitive region can work well.

At T = 10, the Gaussian's gradient-coordinate contributions inside and outside radius four are approximately \(-0.011058+0.012565=+0.001508\). For the halo they are \(-0.004835+0.000934=-0.003901\). Different cancellation changes the sign. **These terms are an integral decomposition, not two literal orbital cohorts.** The [original explorer](population-response.html) distinguishes these coordinates from initial-orbit cohorts.

## Why a response kernel is reusable {#kernel}

For fixed, population-independent evolution, define the phase/noise-averaged action response \(K_B(x)\). Let \(Q_{\mathrm p}\) denote its primitive; the subscript distinguishes it from the galaxy's Toomre Q.

<div class="equation-label" id="EQ-KER-01">EQ-KER-01 · Response and population weighting</div>

```math
\begin{aligned}
K_B(x)&=\mathbb E[B_{\mathrm{noise}}-B_{\mathrm{smooth}}\mid x],\\
\mathcal R[w]&=\int w(x)K_B(x)\,\mathrm dx\\
&=[wQ_{\mathrm p}]_{\mathrm{boundary}}-\int w'(x)Q_{\mathrm p}(x)\,\mathrm dx.
\end{aligned}
```

For the common compact support, the boundary term vanishes. Nonlinear trapping of individual orbits is compatible with linear dependence on the initial population. This identity does not automatically apply to a self-consistent gravitational field or a collision law whose coefficients depend on the evolving population.

The kernel separates dynamical sensitivity from how much material occupies each action. Forecasting another population tests the accuracy and reuse of this numerical calculation; it does not discover a new linearity principle. A new dynamical condition needs its own kernel.

## An error allowance that can decline to predict {#accuracy}

For a candidate approximation v and reference h, the exact-kernel inequality is:

<div class="equation-label" id="EQ-ERR-01">EQ-ERR-01 · Exact-kernel error bound</div>

```math
\left|\mathcal R[v]-\mathcal R[h]\right|
\leq \int\left|v'(x)-h'(x)\right|\left|Q_{\mathrm p}(x)\right|\,\mathrm dx.
```

Include the boundary mismatch if it is nonzero. The implemented kernel is estimated, so its plug-in integral alone is not a rigorous bound. The protocol uses eight independent batch estimates, a nominal simultaneous Student-t envelope with Bonferroni allocation across finite kernel cells and scalar contractions, paired timestep differences, and factor-two mesh refinements. Population contractions retain covariance from shared paths. Antithetic partners, times, windows and population weights are not independent batches.

The full allowance combines population mismatch and the approximate response's sampling/numerical allowance. Its 5% target uses a conservative lower estimate of the halo response. Near cancellation, report absolute error and leave the percentage unqualified. Measured refinement differences are **numerical proxies**, not proved bounds; general confidence coverage has not been established.

{{CLAIM:PA-ACC-01}}

The prospective condition has s = 0.5, η = 0.1. Populations, both times, both windows, forecasts and criteria were frozen before independent evolution. Fourteen independent numerical cases combine positive distribution evolution with collisionless characteristic calculations, including timestep, mesh and domain controls. They are distinct computational pathways; the stochastic kernel was not fitted to their outcomes. [Frozen protocol](protocols/ACCURACY_PLAN.md) · [full outcome](diagnostics/population-accuracy/ACCURACY_OUTCOME_01.md).

{{FIG-ACC}}

**Figure F-ACC-01.** All twenty candidates at one new condition. Orange circles show full forecast allowances; blue crosses show approximate-kernel forecast discrepancy against the independently evolved halo, including its numerical proxy. Both are scaled by the frozen 5% target. This discrepancy is distinct from **intrinsic population error**, R[v] − R[h], which the paired independent calculation also measures. The four halo self-references are excluded from candidate counts. [Complete table](#table-accuracy) · [DS-ACC metadata](datasets.json).

### Interrogate the decision {#interactive-decision}

{{ACCURACY_INTERACTIVE}}

{{ACCURACY_TABLE}}

{{CLAIM:PA-ACC-02}}

At primary-window T = 10, Gaussian 128's signed mean-kernel contrast has magnitude about 0.00009479, whereas the absolute-gradient integral is about 0.00052005, already above the 0.00043771 target before explicit kernel uncertainty. Discarding cancellation explains part of the conservative rejection. More samples alone need not repair it. All twenty independent population discrepancies plus their proxies fit their stated gradient allowances. All new-condition responses are negative: this prospective test does not validate performance across both signs.

The new kernel cost about 5,105 worker CPU-seconds; the six-profile diagnostic took about 0.8 seconds. If the full DF and kernel are already known, the full contraction is also cheap. The diagnostic audits a simplifying assumption; it does not make the kernel free or always beat direct use of the known DF.

## Estimating a small response efficiently {#estimator}

Let \(F'=w\). Here \(W_t\) is a standard Wiener process, with independent increments of mean zero and variance equal to the elapsed time. Define the accumulated action-noise impulse \(\Xi_T=\sqrt{2D}\,W_T\), starting from \(W_0=0\), so that \(y=j+sT-\Xi_T=x+B\). Under the stated external additive noise, uniform initial phase and canonical evolution, a zero-integral primitive identity gives:

<div class="equation-label" id="EQ-EST-01">EQ-EST-01 · Cumulative-remainder identity</div>

```math
\begin{aligned}
\int w(x)\,\mathbb E[B]\,\mathrm dx
&=-\int\mathbb E\!\left[F(x+B)-F(x)-w(x)B\right]\,\mathrm dx.
\end{aligned}
```

The finite-displacement control \(F(x+B)-F(x)\) has zero integrated expectation under the stated assumptions. Subtracting it from the weighted impulse \(w(x)B\) leaves the negative nonlinear remainder. The first-order weighted impulse itself is **not** assumed to have zero expectation: its integrated expectation is the physical signal. The remainder begins with \(w'B^2/2\) for a slowly varying weight; the estimator uses its negative. The derivation requires more than area preservation alone. Auxiliary initial-action support must extend beyond the physical window by the maximum bar impulse; those samples do not add physical halo mass. Do not transplant this identity to action-dependent forcing/noise, nonuniform phases or live response without another derivation. [Complete derivation and support restrictions](methods/CUMULATIVE_IDENTITY.md).

{{CLAIM:EST-01}}

{{FIG-COST}}

**Figure F-COST-01.** Matched raw and remainder estimates use identical paths and discrete weights. Cost includes integration to T = 20, the paired timestep control, setup and method-specific evaluation; I/O and common covariance assembly are excluded from both. T = 10 is charged that same workload. Conditional and between-batch variance estimates differ. Error bars are whole-batch bootstrap intervals, not universal runtime guarantees. [All recorded values](#table-cost) · [DS-COST metadata](datasets.json).

{{COST_INTERACTIVE}}

{{COST_TABLE}}

For moving T = 20 halo weighting, batch costs are about 18.40 versus 18.56 CPU seconds. The advantage comes from variance reduction, not faster trajectory integration. The conditional cost-times-variance ratio is about 6,928, while the noisier between-batch ratio is about 2,749. At Gaussian width 1/64 the ratio is about 0.993: the advantage disappears. One of 24 pointwise raw-minus-remainder intervals excludes zero; this retained multiple-comparison flag is not itself proof of bias. The earlier unmatched-weight timing attempt and corrected benchmark remain in [provenance](archive.html).

## What remains unestablished {#limitations}

{{LIMITATIONS}}

The earlier 24 population forecasts all passed their original operational criterion, max(0.0002, 5% of forecast). A later combined-proxy assessment leaves two early Gaussian-12 window comparisons marginal, retaining 22 qualifications. Historical passes are preserved; they do not become uniform 5% claims. [Exact old and expanded assessments](diagnostics/population-accuracy/joint-error-assessment.json).

The earlier smooth response is **independent-phase replication at the same actions and forcing**. Constant diffusion with restoring drift can fail the old pooled finite-lag flatness screen; its failure alone does not establish non-Markovian physics. These corrections remain in the [prescribed-field study](response.html) and [learning example](learn.html#learn-5).

## Reproduction, criticism and revision history {#reproduction}

{{CLAIM:REP-01}}

A fresh public-source run at numerical revision 66143eb reproduced the accuracy calculation's 162 saved arrays exactly and checked the central figure. This is a **project reproduction receipt**, not an external audit and not additional independent physical samples. The current publication redesign does not rerun those experiments. [Receipt](diagnostics/population-accuracy/accuracy-reproduction.json).

Use the [per-study reproduction map](reproduce.html) to distinguish reading, checking supplied records, and rerunning underlying evolution. Original galaxy outputs are public; the public reduced benchmark does not promise complete reproduction of every galaxy initial condition and trajectory. The private working repository is not required to read or reproduce the released local-model results.

For criticism, cite a claim ID such as **PA-ACC-01**, figure ID, dataset version and exact row. [Open a public issue](https://github.com/djova/bar-halo-benchmark/issues). In particular: is an equivalent cumulative estimator already published; is its scope useful; which error source is missing; and which test would most efficiently falsify the proposed application? No outside review or endorsement is claimed.

{{REVISION}}

{{BIBLIOGRAPHY}}
