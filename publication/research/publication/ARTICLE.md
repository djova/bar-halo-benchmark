# Finite-time population bias in noisy sweeping resonances

*A response-kernel benchmark and an operational test of population approximations*

{{RELEASE}}

## Abstract {#abstract}

Local resonance models often replace an orbital population with a convenient analytic approximation. What information must that approximation preserve to recover the sign and magnitude of angular-momentum transfer? We address this question for a prescribed sweeping resonance with constant additive action diffusion. At fixed central density and slope, a selected Gaussian and reference-halo weighting in one fast-action slice give opposite noise-induced transfer changes at the earlier of two recorded endpoints. Both give suppression at the later endpoint, but the Gaussian magnitude is **{{RATIO}}** times larger. A slope-matched exponential closely follows the halo response at both times. The difference is explained by how the population gradient weights cancelling contributions across the resonance's region of sensitivity.

We construct a reusable response kernel, an operational allowance for population-approximation error, and a cumulative-remainder estimator that reduces variance for broad weights. At one prospectively selected sweep rate, eight advance 5% qualifications are supported by independent numerical calculations; four other accurate comparisons remain unqualified because the allowance discards cancellation. These are correlated comparisons within one local model. The result provides a way to assess population approximations; transfer to three-dimensional orbits and a live halo remains unvalidated. The local noise is not a calibrated SIDM collision operator. **These experiments do not test CDM against SIDM.**

[Learn the foundations](learn.html) · [Inspect and reproduce](reproduce.html) · [Claim registry](claims.json) · [Download this article](paper.md)

## The population approximation in a resonance calculation {#previous-work}

A rotating bar exchanges angular momentum with orbits whose phases evolve slowly relative to its forcing. The net transfer depends both on the response of those orbits and on their abundance in phase space. A local model makes the first part tractable by retaining a slow action and a resonant angle. Approximating the initial distribution simplifies the second part. Matching its density and slope at the initial resonance is an appealing choice, but a moving resonance samples a finite interval of actions. Two populations that agree at the starting point can therefore give different finite-time responses.

Our question is whether that population approximation preserves the change in accumulated bar transfer caused by imposed noise. We hold the dynamics fixed and vary only the positive initial weight, preserving its central density and slope. This comparison isolates population sensitivity within the stated operator. We use *population bias* to mean the change in the target response caused by replacing the reference population; it is distinct from statistical bias in an estimator of that response.

[Hamilton, Tolman, Arzamasskiy & Duarte](https://arxiv.org/abs/2208.03855) studied how diffusion sustains stationary resonant friction, including an initially linear local distribution. [Chiba](https://arxiv.org/abs/2305.00022) studied moving-resonance feedback, compared collisionless reduced dynamics with three-dimensional calculations, and anticipated that diffusion can replenish a friction-producing gradient while erasing a trapped–untrapped density contrast. [Ogilvie & Lubow](https://doi.org/10.1111/j.1365-2966.2006.10506.x) treated a related migration–diffusion competition at planetary corotation in gas. Different physical assumptions prevent treating that analogue as a galactic-halo prediction.

Variance reduction also has direct astrophysical predecessors. [Elbers et al. (2021), sections 2–2.3](https://arxiv.org/pdf/2010.07321), use a δf decomposition to sample departures from a model neutrino distribution and explicitly formulate its control-variate interpretation. Their cosmological calculation includes gravitational feedback. Here the control instead uses a zero-integral primitive identity for accumulated bar impulse under a prescribed canonical map. This is a useful comparison of constructions and assumptions; equivalence, optimality and priority of our specific estimator remain unestablished. We do not claim the control-variate principle as new.

The importance of the underlying distribution function also appears in self-consistent core dynamics: [Dattathri et al.](https://arxiv.org/abs/2511.11804v2) relate different friction, stalling and buoyancy behaviours to phase-space structure. Their evolving host and collective modes are absent here. Our calculation addresses the narrower question of population weighting under a fixed external evolution; it does not test their proposed core mechanisms.

The contribution is a quantified counterexample together with a usable diagnostic: a convenient population can change the early sign, yet another inexpensive approximation can preserve the response. The recorded kernel identifies which gradient differences matter, and the independent comparison tests an allowance declared before its outcomes. We also measure when the remainder estimator makes that calculation more efficient. A targeted literature review is not an exhaustive priority search. [Detailed scholarly positioning](diagnostics/population-accuracy/SOURCES.md).

## Scope and model families {#models}

The results in this article concern **RES-POS**, a positive population in a prescribed local noisy resonance. The gravitational field and noise law do not respond to that population. The original collisionless galaxy simulations and the prescribed-field Cartesian tests are separate studies, and neither supplies a successful validation of this reduction. Earlier signed-perturbation calculations (**RES-SIGNED**) use different populations and boundaries. Their results cannot be interchanged with those below.

{{MODELS}}

## Model, populations and observable {#model}

The slow action measures displacement from the instantaneous resonance, and the resonant angle describes an orbit's phase relative to the imposed bar. In this corotation construction, \(J_s=L_z/2\) and \(\psi=2(\theta_\phi-\phi_{\rm bar})\); the canonical angle \(\theta_\phi\) need not equal geometric azimuth. The implemented frequency gradient is negative. After rescaling action and time, the dynamics are

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

Here \(s\) is the constant dimensionless sweep rate, \(\eta\) specifies the diffusion strength, and \(W_t\) is a standard Wiener process. The sine term is the bar torque; \(-s\) is advection caused by the moving coordinate. Keeping these terms separate prevents motion of the coordinate system from being counted as physical transfer.

The accumulated bar impulse \(B\) excludes both \(-sT\) and the Brownian impulse; the path budget checks all three separately. Our observable is **noise minus smooth accumulated bar-mediated transfer**. Positive means more transfer from the imposed bar to the sampled slice. A negative contrast can arise when both treatments transfer angular momentum to the halo but the noisy one transfers less; it does not by itself imply that the bar gains angular momentum.

The initial resonant phase is uniform. The reference is an analytical isochrone-halo distribution function evaluated at fixed fast actions: radial action 0.08 and vertical action 0.05, central slow action \(J_{s,0}=0.25\). Set \(x=(J_s-J_{s,0})/u\), \(u\approx0.0005633691\). The initial logarithmic slope is \(g\approx-0.0047493212\). Before the common compact window:

<div class="equation-label" id="EQ-POP-01">EQ-POP-01 · Initial populations</div>

```math
\begin{aligned}
w_{\mathrm H}(x)&=\frac{f_{\mathrm{halo}}(J_s;J_r,J_z)}{f_{\mathrm{ref}}},\\
w_{\mathrm E}(x)&=\exp(gx),\\
w_{\sigma}(x)&=\exp\!\left(gx-\frac{x^2}{2\sigma^2}\right).
\end{aligned}
```

The original Gaussian has \(\sigma=8\). Central density and slope are held fixed; populations are **not renormalized to unit mass**. The common window is flat for \(|x|\leq24\) and tapers to zero at \(|x|=40\); the wider comparison uses 48 and 64. Moving this physical taper changes the population. Enlarging the solver domain or auxiliary sampling support is instead a numerical check. Every response remains conditional on the stated fast-action slice.

All response tables display dimensionless \(\int wK_B\,\mathrm dx\). Multiplication by \(4u^2(2\pi)^3 f_{\mathrm{ref}}\approx2.7022892\times10^{-6}\) gives the angular-momentum contribution **per unit fast-action area** in the analytical model's units. The local time T is dimensionless; it is not the original galaxy's Gyr clock. T = 20 is about 3.18 reference librations. [Exact calibration, windows and numerical algorithms](population-methods.html).

## A failed Gaussian approximation and a successful exponential {#population-result}

The first comparison uses identical forcing, noise and duration for all three populations. At \(T=10\), the Gaussian gives a positive contrast whereas the halo gives a negative one. At \(T=20\), both contrasts are negative, with substantially stronger suppression for the Gaussian. Thus the late suppression survives reference-halo weighting, but the Gaussian misrepresents its magnitude and its earlier sign. The exponential follows the halo at both endpoints.

{{CLAIM:POP-01}}

{{FIG-POP}}

{{POPULATION_TABLE}}

**Figure F-POP-01.** Population selection changes the early sign and late magnitude of the noise-minus-smooth accumulated bar transfer. Only the initial weight changes: s = 0.25, η = 0.1, central density, initial slope and cutoff 40 are shared. Values are dimensionless \(\int wK_B\,\mathrm dx\), conditional on one fast-action slice. The two endpoints are recorded measurements, not a resolved time history. Intervals are pointwise 95% Student-t intervals across eight independent trajectory batches; paired numerical controls are assessed separately. The early signs survive the declared timestep/window allowances. [Complete values and numerical controls](results/populations.json); [interactive weighting](population-response.html#population-explorer). Analysis version and checksums: [DS-POP](datasets.json).

The exponential's point differences from the halo are about 0.050% and 0.068%. These close means do not certify sub-0.1% accuracy: the relevant uncertainty is that of the paired difference, together with numerical sensitivity. The [difference record](diagnostics/population-accuracy/joint-error-assessment.json) retains that assessment.

The population definitions reveal why agreement at the initial resonance is insufficient. Before tapering, the Gaussian has \(\mathrm d\ln w_\sigma/\mathrm dx=g-x/\sigma^2\), whereas the exponential retains \(\mathrm d\ln w_{\rm E}/\mathrm dx=g\). The Gaussian therefore introduces a gradient change across the sampled action interval even though it matches the same initial slope. To determine whether that change matters, we need the dynamical sensitivity across the interval, rather than the curvature at one point alone.

## Separating orbital response from population weighting {#kernel}

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

The first integral separates two ingredients: \(K_B\) describes the mean change in bar impulse for a given starting action, while \(w\) supplies the amount of material there. The second representation exposes sensitivity to the population gradient. It is the product \(-w'Q_{\mathrm p}\), integrated with its sign, that determines the response. Matching \(w'\) at one point controls neither that product elsewhere nor its cancellation.

At \(T=10\), the Gaussian's gradient-coordinate contributions inside and outside \(|x|=4\) are approximately \(-0.011058+0.012565=+0.001508\). For the halo they are \(-0.004835+0.000934=-0.003901\). The positive term outweighs the negative one for the Gaussian, while the negative term dominates for the halo. This decomposition explains the sign difference. **The terms are contributions to the gradient integral, not two literal cohorts of initial orbits.** The [weighting explorer](population-response.html#population-explorer) shows the populations, kernel and cumulative cancellation together.

Reusing a measured kernel for another population tests the accuracy of this calculation. The linearity in \(w\) is an exact property of the external-field problem, not a new physical theory. Changing the sweep or noise changes the dynamics and requires a new kernel.

## When can an approximate population be used? {#accuracy}

For a candidate approximation v and reference h, the exact-kernel inequality is:

<div class="equation-label" id="EQ-ERR-01">EQ-ERR-01 · Exact-kernel error bound</div>

```math
\left|\mathcal R[v]-\mathcal R[h]\right|
\leq \int\left|v'(x)-h'(x)\right|\left|Q_{\mathrm p}(x)\right|\,\mathrm dx.
```

This allowance weights each gradient mismatch by the magnitude of the response sensitivity. It can remain small when a population differs in a dynamically unimportant region, and large when a small mismatch occurs where the response is sensitive. It also discards cancellation, making it conservative. Include the boundary mismatch if it is nonzero.

The exact-kernel inequality and its numerical implementation have different evidentiary status. The implemented kernel is estimated, so its plug-in integral alone is not a rigorous bound. The protocol uses eight independent batch estimates, a nominal simultaneous Student-t envelope with Bonferroni allocation across finite kernel cells and scalar contractions, paired timestep differences, and factor-two mesh refinements. Population contractions retain covariance from shared paths. Antithetic partners, times, windows and population weights are not independent batches.

The full allowance combines population mismatch and the approximate response's sampling/numerical allowance. A sign is qualified only when the expanded response interval excludes zero. A magnitude is qualified at 5% only when the full allowance fits the frozen target, defined using a conservative lower estimate of the halo response. Near cancellation, absolute error remains meaningful while percentage accuracy may be unqualified. Measured refinement differences are **numerical proxies**, not proved bounds; general confidence coverage has not been established.

{{CLAIM:PA-ACC-01}}

The prospective condition has s = 0.5, η = 0.1. Populations, both times, both windows, forecasts and criteria were frozen before independent evolution. Fourteen independent numerical cases combine positive distribution evolution with collisionless characteristic calculations, including timestep, mesh and domain controls. They are distinct computational pathways; the stochastic kernel was not fitted to their outcomes. [Frozen protocol](protocols/ACCURACY_PLAN.md) · [full outcome](diagnostics/population-accuracy/ACCURACY_OUTCOME_01.md).

{{FIG-ACC}}

**Figure F-ACC-01.** The allowance identifies eight acceptable approximations and conservatively rejects four others that also meet the target. The twenty candidates share s = 0.5 and η = 0.1; their population, endpoint and window vary. Orange circles show full forecast allowances; blue crosses show approximate-kernel forecast discrepancy against the independently evolved halo, including its numerical proxy. Both are divided by the frozen absolute 5% target. The discrepancy includes kernel-estimation error and is distinct from **intrinsic population error**, R[v] − R[h], measured by paired independent evolution. The four halo self-references are excluded from candidate counts. [Complete table](#table-accuracy) · [DS-ACC metadata](datasets.json).

### Interrogate the decision {#interactive-decision}

{{ACCURACY_INTERACTIVE}}

{{ACCURACY_TABLE}}

{{CLAIM:PA-ACC-02}}

At primary-window T = 10, Gaussian 128's signed mean-kernel contrast has magnitude about 0.00009479, whereas the absolute-gradient integral is about 0.00052005, already above the 0.00043771 target before explicit kernel uncertainty. Discarding cancellation explains part of the conservative rejection. More samples alone need not repair it. All twenty independent population discrepancies plus their proxies fit their stated gradient allowances. All new-condition responses are negative: this prospective test does not validate performance across both signs.

The new kernel cost about 5,105 worker CPU-seconds; the six-profile diagnostic took about 0.8 seconds. If the full DF and kernel are already known, the full contraction is also cheap. The diagnostic audits a simplifying assumption; it does not make the kernel free or always beat direct use of the known DF.

## Measuring a small net transfer without large cancellation noise {#estimator}

The raw estimator averages weighted bar impulses. For a broad, slowly varying population, individual positive and negative impulses can be much larger than their net response. Resolving that small difference by direct averaging is expensive. A control with known zero integrated expectation lets us estimate the same transfer from a nonlinear remainder, which is small when the population varies slowly across the impulse displacement.

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

**Figure F-COST-01.** Variance reduction makes broad-population responses cheaper to estimate, but gives no advantage for the narrowest stress population. Raw and remainder estimates use identical paths, discrete weights and target quantities. Left: the raw-to-remainder cost-times-variance ratio, not a measured trajectory-integration speedup. Right: precision projections assume independent batches at fixed allocation; circles show measured eight-batch estimates. Cost includes integration to T = 20, the paired timestep control, setup and method-specific evaluation; I/O and common covariance assembly are excluded from both. T = 10 is charged that same workload. Whole-batch bootstrap intervals describe uncertainty in the ratio; conditional and between-batch variance estimates remain distinct. [All recorded values](#table-cost) · [DS-COST metadata](datasets.json).

{{COST_INTERACTIVE}}

{{COST_TABLE}}

For moving T = 20 halo weighting, batch costs are about 18.40 versus 18.56 CPU seconds. The advantage comes from variance reduction, not faster trajectory integration. The conditional cost-times-variance ratio is about 6,928, while the noisier between-batch ratio is about 2,749. At Gaussian width 1/64 the ratio is about 0.993: the advantage disappears. One of 24 pointwise raw-minus-remainder intervals excludes zero; this retained multiple-comparison flag is not itself proof of bias. The earlier unmatched-weight timing attempt and corrected benchmark remain in [provenance](archive.html).

## Domain of validity and unresolved extensions {#limitations}

The calculation establishes population sensitivity under a fixed local evolution. It does not determine which noise law describes a halo or whether a full galaxy develops a bar. Extending it to a physical halo requires integrating over fast actions and relevant resonances, testing the reduction against Cartesian dynamics, and accounting for the response of the gravitational field. A successful prescribed-field three-dimensional test would address only the second of those steps. The restrictions below specify the present domain.

{{LIMITATIONS}}

The earlier 24 population forecasts all passed their original operational criterion, max(0.0002, 5% of forecast). A later combined-proxy assessment leaves two early Gaussian-12 window comparisons marginal, retaining 22 qualifications. Historical passes are preserved; they do not become uniform 5% claims. [Exact old and expanded assessments](diagnostics/population-accuracy/joint-error-assessment.json).

The earlier smooth response is **independent-phase replication at the same actions and forcing**. Constant diffusion with restoring drift can fail the old pooled finite-lag flatness screen; its failure alone does not establish non-Markovian physics. These corrections remain in the [prescribed-field study](response.html) and [learning example](learn.html#learn-5).

## Conclusions {#conclusions}

Matching central density and slope is insufficient to preserve finite-time resonant transfer in the tested model. The Gaussian counterexample changes the earlier sign and amplifies the later suppression. Yet the slope-matched exponential closely follows the reference halo. The useful distinction is therefore which gradient differences overlap the dynamics' region of sensitivity, as measured by the primitive response kernel.

The resulting diagnostic supplies a practical decision: use a population approximation when its expanded error allowance fits the required accuracy, qualify its sign only when the corresponding interval excludes zero, and retain an unqualified outcome otherwise. Its eight successful advance qualifications at one new sweep rate demonstrate usefulness within this benchmark. Its four conservative rejections show the cost of discarding signed cancellation. The cumulative-remainder estimator makes broad-weight calculations more efficient, with a measured loss of that advantage for sharply concentrated weights.

The transferable product is the recorded kernel, the explicit approximation-error calculation and the runnable benchmark. Applying them to a new dynamical condition requires that condition's kernel; applying them to a live halo requires additional physical validation. Within the present domain, a researcher can test a simplifying population choice before interpreting its predicted transfer.

## Reproduction, criticism and revision history {#reproduction}

{{CLAIM:REP-01}}

A fresh public-source run at numerical revision 66143eb reproduced the accuracy calculation's 162 saved arrays exactly and checked the central figure. This is a **project reproduction receipt**, not an external audit and not additional independent physical samples. The present editorial revision does not rerun those experiments. [Receipt](diagnostics/population-accuracy/accuracy-reproduction.json).

Use the [per-study reproduction map](reproduce.html) to distinguish reading, checking supplied records, and rerunning underlying evolution. Original galaxy outputs are public; the public reduced benchmark does not promise complete reproduction of every galaxy initial condition and trajectory. The private working repository is not required to read or reproduce the released local-model results.

For criticism, cite a claim ID such as **PA-ACC-01**, figure ID, dataset version and exact row. [Open a public issue](https://github.com/djova/bar-halo-benchmark/issues). In particular: is an equivalent cumulative estimator already published; is its scope useful; which error source is missing; and which test would most efficiently falsify the proposed application? No outside review or endorsement is claimed.

{{REVISION}}

{{BIBLIOGRAPHY}}
