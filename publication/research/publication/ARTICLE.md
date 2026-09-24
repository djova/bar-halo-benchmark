# Population dependence of angular-momentum transfer at a noisy sweeping resonance

{{RELEASE}}

## Abstract {#abstract}

Scattering changes the angular momentum exchanged between a bar and resonant orbits. The net effect depends on how the orbits are populated, but local calculations often replace that population with a simple distribution. We test the error introduced by this replacement in a prescribed sweeping-resonance model with additive action diffusion. A Gaussian, an exponential and a reference isochrone distribution are matched in density and slope at the initial resonance. In the tested slice of orbital actions, the Gaussian gives a positive noise-minus-smooth transfer contrast at an early time when the reference distribution gives a negative contrast. At a later time both contrasts are negative, but the Gaussian contrast has 4.7 times the reference magnitude. The exponential closely follows the reference at both times. We explain this difference using a response kernel that separates the dynamics of the orbits from their initial abundance. The kernel also provides a test of population-approximation error. At a second sweep rate, all eight comparisons accepted by this test satisfy the specified 5 per cent accuracy criterion in an independent calculation; four other accurate comparisons are rejected because the test discards signed cancellation. A finite-displacement control reduces the sampling variance for broad populations. These results identify a source of error in finite-time resonance calculations and a way to assess it within the prescribed local model. Their extension to a self-consistent halo remains untested.

[Learn the foundations](learn.html) · [Inspect and reproduce](reproduce.html) · [Claim registry](claims.json) · [Download this article](paper.md)

## Introduction {#previous-work}

A rotating bar continually accelerates and decelerates the particles of its surrounding halo. For most orbits, the phase relative to the bar changes rapidly, and successive torque contributions largely cancel. Near a resonance, that phase changes slowly enough for the torque to accumulate. Some orbits become trapped and oscillate about a preferred phase relative to the bar. The angular momentum exchanged by the population therefore depends on both the response of individual orbits and the number of particles occupying each part of phase space.

Scattering can change this exchange even when it produces only a small change in an orbit's total action. The relevant scale is the width of the resonance. [Hamilton et al. (2023)](https://arxiv.org/abs/2208.03855) showed that diffusion across this width can sustain torque at a stationary bar resonance, where phase mixing would otherwise suppress it. A slowing bar introduces another effect: its resonances move through action space, carrying trapped particles into regions with a different background population. [Chiba (2023)](https://arxiv.org/abs/2305.00022) showed how this motion contributes to the torque and argued that diffusion should weaken the associated population contrast. Related competition between migration and diffusion occurs at planetary corotation resonances in gaseous discs ([Ogilvie & Lubow 2006](https://doi.org/10.1111/j.1365-2966.2006.10506.x)). These results motivate a calculation of the net finite-time effect; they do not imply that scattering must change the transfer in the same direction in every population.

Such a calculation requires an initial distribution function. A convenient local approximation matches its value and slope at the resonance. This is sensible when the response is confined to a region over which the slope changes little. A moving resonance, however, samples an interval of actions, and diffusion can broaden the relevant region further. Matching at one point then leaves an uncontrolled choice: the approximation may contain too much or too little material where the torque contributions have opposite signs. It is this choice, rather than a change to the equations of motion, that we investigate here.

We compare three positive populations with the same central density and slope while holding the bar and diffusion law fixed. The reference is the isotropic distribution associated with an isochrone potential, restricted to one pair of fast actions. The alternatives are an exponential and a Gaussian. This construction isolates population dependence: replacing the population cannot change the imposed force or noise. We first measure its effect on accumulated bar transfer, then use an action-dependent response kernel to locate the source of the difference. Finally, we test whether the kernel can identify acceptable approximations at a second sweep rate and measure the computational benefit of a variance-reduced estimator. The calculation addresses one local resonance contribution, rather than the total torque on a galactic bar.

## A prescribed sweeping resonance {#model}

### Orbital variables and scales

Consider the corotation resonance of an imposed quadrupole bar. Its slow action and angle are \(J_s=L_z/2\) and \(\psi=2(\theta_\phi-\phi_{\rm bar})\), where \(L_z\) is the specific angular momentum about the rotation axis. The canonical azimuthal angle \(\theta_\phi\) advances with the orbital frequency; it is generally different from a particle's instantaneous geometric azimuth. Averaging over the remaining, rapidly varying angles leaves a one-degree-of-freedom Hamiltonian. Expanding about the resonance action \(J_{\rm res}\), we use

<div class="equation-label" id="EQ-HAM-01">Local Hamiltonian</div>

```math
H(J_s,\psi,t_{\rm phys})=
\frac{a}{2}[J_s-J_{\rm res}(t_{\rm phys})]^2-b\cos\psi.
```

Here \(a<0\) is the local derivative of the resonant frequency and \(b>0\) is the bar-coupling amplitude. Both coefficients are held constant. Thus \(\dot\psi=a(J_s-J_{\rm res})\) and \(\dot J_s=-b\sin\psi\): the action displacement sets how quickly the orbit moves through bar phase, while the phase sets the sign of its torque.

Define the action scale \(u=\sqrt{b/|a|}\), time scale \(t_0=1/\sqrt{|a|b}\), dimensionless time \(t=t_{\rm phys}/t_0\), and moving action coordinate \(j=(J_s-J_{\rm res})/u\). For a stationary resonance without noise, the separatrix half-width is \(2u\) and the small-amplitude libration period is \(t_{\rm lib}=2\pi t_0\). These reference scales remain useful when the resonance moves. The sweep rate \(s=\dot J_{\rm res}/b\) compares that motion with the largest action-change rate the bar can supply.

We add independent Gaussian action increments with constant diffusion coefficient. In the scaled variables,

<div class="equation-label" id="EQ-DYN-01">Reduced dynamics</div>

```math
\begin{aligned}
\mathrm d\psi&=-j\,\mathrm dt,\\
\mathrm dj&=(-\sin\psi-s)\,\mathrm dt+\sqrt{2D}\,\mathrm dW_t,\\
D&=\frac{2\eta}{\pi}.
\end{aligned}
```

The Wiener increment has zero mean and variance \(\mathrm dt\). If \(D_{\rm phys}\) is the diffusion coefficient in the unscaled action, then \(\eta=D_{\rm phys}t_{\rm lib}/(2u)^2\). It compares diffusion over a reference libration with the squared resonance half-width. The term \(-s\) arises solely from the moving coordinate. With \(D=0\), an equilibrium requires \(j=0\) and \(\sin\psi=-s\); a finite stable libration region exists for \(|s|<1\), on the branch with \(\cos\psi<0\). At \(s=0\), its centre is \(\psi=\pi\). Noise allows particles to leave that region, so deterministic trapping does not imply permanent locking in the stochastic model.

Our principal comparison has \(s=0.25\) and \(\eta=0.1\). The bar has its full, constant amplitude from \(t=0\); the initial phases are uniform, rather than equilibrated with the bar. We measure the response at \(T=10\) and 20, approximately 1.59 and 3.18 reference libration periods. These are finite-time experiments with a specified turn-on, not estimates of a stationary torque.

### Initial populations

The reference population is taken from the isotropic distribution function of an isochrone potential with \(G=M=1\) and scale radius \(c=0.5\), tabulated using AGAMA ([Vasiliev 2019](https://arxiv.org/abs/1802.08239)). We fix \((J_r,J_z)=(0.08,0.05)\) and \(J_{s,0}=0.25\). The calibrated coefficients are \(a\simeq-2.7911\) and \(b\simeq8.8585\times10^{-7}\), giving \(u\simeq5.63\times10^{-4}\). Writing the initial displacement as \(x=(J_s-J_{s,0})/u\), the three unwindowed weights are

<div class="equation-label" id="EQ-POP-01">Initial populations</div>

```math
\begin{aligned}
w_{\rm H}(x)&=f_{\rm halo}(J_s;J_r,J_z)/f_{\rm ref},\\
w_{\rm E}(x)&=\exp(gx),\\
w_\sigma(x)&=\exp\!\left(gx-\frac{x^2}{2\sigma^2}\right).
\end{aligned}
```

The constant \(f_{\rm ref}\) is the halo DF at the initial resonance and \(g\simeq-0.00475\) is its logarithmic derivative with respect to \(x\). All three weights have value one and derivative \(g\) at \(x=0\). We use \(\sigma=8\) for the initial Gaussian comparison. The Gaussian's logarithmic slope becomes \(g-x/\sigma^2\), whereas the exponential retains the constant slope \(g\). This difference in curvature is the variable under test.

A common window leaves the weights unchanged for \(|x|\leq24\) and tapers them to zero at \(|x|=40\). We also use a wider window, flat to 48 and zero at 64, to check sensitivity to this truncation. Central density is preserved; each windowed population is not separately normalized to unit mass. Such a normalization would change the amount of material represented and obscure the effect we wish to measure. Full calibration and window definitions are given in the [population methods](population-methods.html).

### The measured angular-momentum transfer

The final action contains three contributions: torque from the bar, the coordinate shift and the imposed random impulse. To distinguish them, define

<div class="equation-label" id="EQ-OBS-01">Accumulated bar impulse</div>

```math
\begin{aligned}
B(T)&=-\int_0^T\sin\psi\,\mathrm dt,\\
j(T)-x&=B(T)-sT+\Xi_T,\qquad
\Xi_T=\sqrt{2D}\,W_T.
\end{aligned}
```

Only \(B\) measures transfer mediated by the bar. For a population \(w\), our response \(\mathcal R[w]\) is the accumulated transfer with diffusion minus that without diffusion, averaged over initially uniform phase and integrated over \(x\). A positive response means that noise increases the transfer to the sampled population. A negative response means it decreases that transfer; it does not determine the sign of the total torque in either treatment.

The reported responses are dimensionless. Multiplication by \(4u^2(2\pi)^3f_{\rm ref}\simeq2.70\times10^{-6}\) converts them to an angular-momentum contribution per unit fast-action area in the isochrone model's units. Integrating over the rest of the halo and other resonances would be a separate calculation.

### Numerical methods

We compute the response using stochastic trajectories and, for selected comparisons, a separately evolved distribution. The trajectories use split phase drifts and action kicks, with shared Brownian paths for paired timestep refinements. Each of eight independent seeded batches contains 1,572,864 initial points distributed among 176 action strata. The fine timestep is 0.00625; its paired control uses 0.0125. Sampling errors are estimated from the variation between batches. Antithetic noise partners and different population weights within a batch remain paired; they are not additional independent realizations.

For the distribution \(f(j,\psi,t)\), the same dynamics imply

<div class="equation-label" id="EQ-FP-01">Distribution evolution</div>

```math
\frac{\partial f}{\partial t}
-j\frac{\partial f}{\partial\psi}
-(\sin\psi+s)\frac{\partial f}{\partial j}
=D\frac{\partial^2 f}{\partial j^2}.
```

The initial condition is \(f(j,\psi,0)=w(j)/(2\pi)\). We solve this equation by Fourier Strang splitting on a periodic numerical domain. The physical population is compactly windowed inside that domain. Domain enlargement and edge-mass checks test contamination by periodic wrapping; timestep and mesh refinements test the measured transfer. The Fourier method does not enforce positivity, so negative mass is monitored separately. For the zero-diffusion reference we use direct fourth-order characteristic integration, which resolves the fine phase-space structure without evolving it on a Fourier grid. At the second sweep rate, the principal noisy calculation uses 6,144 action cells on \([-96,96]\), 256 phase cells and timestep 0.025; the wider population window uses 8,192 action cells on \([-128,128]\). The collisionless quadrature uses 40,960 action nodes on \([-160,160]\) and 1,024 phase nodes, with timestep 0.025. The [frozen numerical protocol](protocols/ACCURACY_PLAN.md) specifies their refinements and acceptance criteria. Refinement differences estimate numerical sensitivity; they are not rigorous bounds on the continuum error.

## Population dependence of the transfer {#population-result}

Figure F-POP-01 shows the result of changing only the initial weight. At \(T=10\), diffusion increases the Gaussian's accumulated transfer by \(1.51\times10^{-3}\), but decreases the halo-weighted transfer by \(3.90\times10^{-3}\). The sampling intervals resolve both signs, and the signs survive the specified timestep and window checks. Matching the initial density and slope therefore does not preserve even the direction of the noise-induced change in this example.

At \(T=20\), diffusion decreases the transfer for both populations. The Gaussian response is \(-0.16195\), compared with \(-0.03420\) for the halo, a magnitude ratio of **{{RATIO}}**. Suppression thus survives replacing the Gaussian by the reference halo population, but its magnitude is much smaller. The exponential gives \(-0.003899\) and \(-0.034223\) at the two times. Its point differences from the halo are only about 0.050 and 0.068 per cent. These close means do not by themselves establish accuracy at that level; such a claim would require the paired uncertainty and numerical error of the difference.

{{FIG-POP}}

**Figure F-POP-01.** Change in accumulated bar transfer caused by diffusion, for populations with the same density and slope at the initial resonance. The Gaussian gives the wrong early sign relative to the reference halo weighting and a larger late suppression; the exponential closely follows the reference. Both panels use s = 0.25, η = 0.1 and the cutoff-40 window. The ordinate is the dimensionless response \(\mathcal R[w]\), conditional on one fast-action slice. Error bars are pointwise 95 per cent Student-t intervals from eight independent batches; they do not include numerical sensitivity. The panels show two measured endpoints, with different vertical scales. [Values and numerical controls](results/populations.json).

{{POPULATION_TABLE}}

This result suggests a more precise question than whether the initial curvature is small. Over which actions must the approximation preserve the population gradient? A difference far from the dynamically relevant region need not affect the transfer. Conversely, a modest difference can matter if it changes the balance of large, oppositely signed contributions. We use the response kernel to identify that region and measure this balance.

## The action-dependent response {#kernel}

Because the bar and the noise do not depend on the population, the orbit calculation can be performed before choosing its weight. Define

<div class="equation-label" id="EQ-KER-01">Response kernel</div>

```math
\begin{aligned}
K_B(x)&=\mathbb E[B_{\rm noise}-B_{\rm smooth}\mid x],\\
\mathcal R[w]&=\int w(x)K_B(x)\,\mathrm dx.
\end{aligned}
```

The expectation averages over initial phase and noise. The kernel measures what the imposed dynamics do to particles starting at \(x\); the weight specifies how much material starts there. Trapping can make an individual trajectory highly nonlinear without spoiling this separation. It requires only that changing the population leave the evolution law unchanged.

Let \(Q_{\rm p}\) be a primitive of \(K_B\). Integration by parts gives

<div class="equation-label" id="EQ-GRAD-01">Gradient representation</div>

```math
\mathcal R[w]=[wQ_{\rm p}]_{\rm boundary}
-\int w'(x)Q_{\rm p}(x)\,\mathrm dx.
```

Figure F-GRAD-01 displays the ingredients of this integral. The boundary term vanishes for the compact windows used here. This form shows exactly which population gradients matter: the contribution at each action is \(-w'Q_{\rm p}\). It also explains why agreement at the initial resonance is insufficient. The Gaussian changes the derivative away from that point, where the primitive kernel can still be appreciable.

{{FIG-GRAD}}

**Figure F-GRAD-01.** How population gradients weight the recorded response at T = 10, s = 0.25 and η = 0.1. (a) Population gradients; (b) their common primitive kernel; (c) signed contributions to the gradient integral; (d) cumulative response across the complete cutoff-40 window. The grey strip marks \(|x|<4\). Panels (a)–(c) show the central interval \(|x|\leq16\). Products are evaluated on the original fine cells before summation into display cells; multiplying the displayed mean curves is not equivalent. Shaded curve bands are pointwise 95 per cent Student-t intervals from eight batches, without numerical-error expansion. These are terms in the integration-by-parts representation, not separate cohorts of initial orbits. The explanatory curves describe the recorded kernel estimate; the sampling and numerical checks for the endpoint values are supplied with Figure F-POP-01.

For the Gaussian at \(T=10\), integrating the gradient contribution inside and outside \(|x|=4\) gives approximately \(-0.011058\) and \(+0.012565\). Their sum is positive. For the halo, the corresponding contributions are \(-0.004835\) and \(+0.000934\), giving a negative sum. The Gaussian's imposed curvature changes this balance enough to reverse the sign. The exponential, whose gradient remains close to the halo's over the relevant interval, largely preserves it.

This decomposition explains the population dependence of the measured response. It does not by itself separate diffusion-supported friction from changes in resonant capture: that would require additional dynamical diagnostics. Its use here is to calculate several population responses from one set of trajectories and to make the error of a chosen approximation explicit.

## Testing a population approximation {#accuracy}

Suppose \(h\) is the reference weight and \(v\) an approximation. Subtracting their gradient representations gives a signed integral of \(v'-h'\). Taking its absolute value yields

<div class="equation-label" id="EQ-ERR-01">Population-error bound</div>

```math
\left|\mathcal R[v]-\mathcal R[h]\right|
\leq \int |v'(x)-h'(x)|\,|Q_{\rm p}(x)|\,\mathrm dx.
```

This bound is exact for an exact kernel and the stated boundary treatment. It is small when the approximation preserves the gradient where the response is sensitive. Its limitation is equally clear: taking absolute values loses cancellations, so the bound can be larger than the actual error.

In practice, \(Q_{\rm p}\) is estimated from trajectories. We enlarge the gradient integral to account for its sampling uncertainty and measured numerical sensitivity, then add the uncertainty in the approximate response itself. We accept an approximation at the requested accuracy only when this total allowance lies below the target. For the 5 per cent tests, the absolute target is set using a conservative lower estimate of the reference response. A separate sign test asks whether the expanded response interval excludes zero.

The sampling calculation uses eight independent batches and a Student-t envelope with Bonferroni allocation over the specified kernel cells and scalar estimates. Paired timestep differences and factor-two mesh refinements supply numerical-error estimates. These choices produce a reproducible decision rule, but its coverage is approximate: the exact inequality does not turn sampled kernels or refinement differences into rigorous error bounds.

We tested the rule at \(s=0.5\), twice the original sweep rate, keeping \(\eta=0.1\). The new dynamics require a new kernel. The candidate family comprises the exponential and Gaussians with \(\sigma=8,32,128,512\), at both endpoints and both windows. These choices and the decisions were fixed before the independent distribution calculations were examined. Figure F-ACC-01 compares the resulting error allowances with the independent outcomes. Among twenty candidate comparisons, the rule accepted eight: the exponential and Gaussian of width 512 at two times and two windows. All eight meet the specified 5 per cent target in the independent calculation, including its numerical-error estimates. The comparisons share one dynamical condition and one sampled kernel; their count does not represent eight independent physical regimes.

{{FIG-ACC}}

**Figure F-ACC-01.** Performance of the population-error test at s = 0.5 and η = 0.1. Orange circles show the total error allowance divided by the frozen 5 per cent target. Blue crosses show the discrepancy between the approximate response predicted from the kernel and the independently evolved halo response, expanded by the halo's numerical-error estimate and divided by the same target. The latter includes kernel-estimation error, whereas the intrinsic population error compares independently evolved populations. All eight accepted candidates meet the target. Four Gaussian-128 comparisons also meet it but are rejected by the test; eight remaining candidates are independently outside the target. Four halo self-references are excluded from these counts. [Full values](#table-accuracy).

The four conservative rejections illustrate the cost of discarding cancellation. For Gaussian 128 at \(T=10\) in the primary window, the signed population contrast from the mean kernel is approximately \(9.48\times10^{-5}\) in magnitude. The integral of the absolute gradient contributions is \(5.20\times10^{-4}\), already larger than the \(4.38\times10^{-4}\) target before adding kernel uncertainty. More precise kernel sampling does not restore the cancellation discarded by taking absolute values. The test can therefore identify useful approximations while declining some that would in fact be accurate.

### Explore the error calculation {#interactive-decision}

{{ACCURACY_INTERACTIVE}}

{{ACCURACY_TABLE}}

Computing the new kernel required about 5,105 worker CPU-seconds; evaluating the six-profile diagnostic took about 0.8 seconds. The kernel is the expensive step. Once it and the full reference DF are available, directly contracting them is also cheap. The error test is useful for assessing a simplifying population choice, not as a claim that approximating a known DF is always faster than using it.

## Estimating small transfers efficiently {#estimator}

Directly averaging weighted impulses can be inefficient. An individual orbit may gain or lose much more angular momentum than the net transfer of a broad population. The estimate then depends on cancellation between large sampled terms. We reduce that variance by subtracting a control whose integrated expectation is known to vanish.

Let \(F'=w\). From the action budget, removing the coordinate shift and random impulse gives \(y=j+sT-\Xi_T=x+B\). For a fixed noise history, the map from the initial phase plane to \(\psi,y\) preserves area. The time derivative of the integrated primitive displacement can therefore be written as an integral of \(-w(y)\sin\psi\) over that plane. Its angular average vanishes, and the primitive displacement is initially zero. With uniform initial phase and sufficient auxiliary action support, the finite displacement \(F(x+B)-F(x)\) has zero integrated expectation. Consequently,

<div class="equation-label" id="EQ-EST-01">Finite-displacement estimator</div>

```math
\begin{aligned}
\int w(x)\,\mathbb E[B]\,\mathrm dx
&=-\int\mathbb E\!\left[F(x+B)-F(x)-w(x)B\right]\,\mathrm dx.
\end{aligned}
```

The left-hand side is the generally nonzero transfer. On the right, the first-order term has cancelled *inside the remainder*. For a weight that varies slowly over the displacement, the remainder begins with \(w'B^2/2\); the estimator uses its negative. This replaces a large fluctuating impulse by a smaller quantity controlled by the variation of the weight.

The identity needs more than area preservation alone. The auxiliary initial-action region must extend beyond the physical support by the maximum bar impulse, so that translated trajectories are accounted for even when their starting weights vanish. Those auxiliary samples add no physical mass. The [derivation](methods/CUMULATIVE_IDENTITY.md) specifies the support and symmetry assumptions; action-dependent noise, nonuniform initial phases or a responding halo require a new argument. We apply the identity separately to the noisy and smooth transfers and subtract them.

Variance reduction by subtracting a known contribution is established practice. In cosmological neutrino calculations, [Elbers et al. (2021)](https://arxiv.org/pdf/2010.07321) use a δf construction to sample departures from a reference distribution. Our control instead uses the finite-displacement identity for the accumulated bar impulse. The useful question is how much this particular construction reduces variance for the present target, and where it ceases to help.

{{FIG-COST}}

**Figure F-COST-01.** Efficiency of the finite-displacement estimator on matched paths and weights. Left: raw-to-remainder cost-times-variance ratio. Right: precision projected under independent repetition of the measured batch workload, with circles marking the eight-batch estimates. The broad halo population benefits strongly, whereas the narrowest Gaussian does not. Costs include trajectory integration to T = 20, paired timestep refinement, setup and method-specific evaluation; both methods exclude I/O and common covariance assembly. T = 10 receives the same full-workload cost. Intervals are whole-batch bootstrap intervals. Conditional and between-batch variance estimates are reported separately in the [complete records](#table-cost).

Figure F-COST-01 shows the measured efficiency across broad and narrow weights. For the halo weight at \(s=0.25\), \(T=20\), the raw and remainder calculations cost about 18.40 and 18.56 CPU-seconds per batch. Their conditional cost-times-variance ratio is approximately 6,928; using the noisier variance between the eight batches gives about 2,749. The gain comes from lower variance, not faster orbit integration. For a Gaussian of width \(1/64\), the ratio is about 0.993 and the advantage disappears, as expected when the weight changes sharply over an impulse displacement. One of the 24 pointwise paired method-comparison intervals excludes zero; it remains in the record and is not, by itself, evidence of bias after multiple comparisons.

{{COST_INTERACTIVE}}

{{COST_TABLE}}

## Discussion and conclusions {#limitations}

The population choice can alter a finite-time noise response even when central density and slope are matched. In our example, the Gaussian gives the opposite early sign from the reference halo slice and a late suppression about 4.7 times larger. The exponential succeeds much better because its gradient follows the reference over the actions that contribute to the response. The relevant matching condition is therefore distributed over that interval, rather than confined to the initial resonance.

The response kernel makes this statement quantitative. It identifies how changes in the population gradient affect the transfer and provides an error test that can be evaluated before a new population is evolved. At the second sweep rate, the accepted approximations satisfy the independent numerical comparison. The conservative rejections show that this usefulness comes with a limitation: an absolute bound can discard cancellation essential to the final answer. A failure to accept an approximation need not mean that the approximation is inaccurate.

These conclusions concern a fixed external evolution. The halo DF enters as an initial weight on one pair of fast actions; it does not generate a responding potential. In a self-consistent system, redistribution of particles can alter the forces and resonance locations. The connection between DF structure and dynamical friction in such systems is discussed, for example, by [Dattathri et al. (2026)](https://arxiv.org/abs/2511.11804v2), but their collective core dynamics are absent from this model. The present calculation neither measures a full-halo torque nor provides a universal correction for one.

The constant coefficients, additive diffusion, finite population window and abrupt bar turn-on further define the scope of the result. A different history or noise law requires a new kernel. Our attempted transfer to prescribed-field three-dimensional orbits remains statistically unresolved; even successful agreement there would leave collective halo response untested. The noise coefficient has not been calibrated to dark-matter scattering. **These experiments do not test CDM against SIDM.**

<span id="conclusions"></span>
The practical result is a way to assess a population substitution in a controlled resonance calculation: compare its gradient with the reference over the region weighted by the kernel, retain cancellation when computing the response, and include kernel uncertainty when assessing the error. The finite-displacement estimator makes that assessment affordable for broad populations. Its extension to a broader range of resonances and noise histories can be tested independently of the population example presented here.

## Supporting evidence and earlier studies {#models}

The main argument above is self-contained. This section connects it to the machine-readable records and to earlier investigations without treating their different physical models as interchangeable.

{{MODELS}}

{{CLAIM:POP-01}}

{{CLAIM:PA-ACC-01}}

{{CLAIM:PA-ACC-02}}

{{CLAIM:EST-01}}

{{LIMITATIONS}}

The earlier 24 population forecasts passed their original criterion, max(0.0002, 5% of forecast). A later assessment combining numerical-error estimates leaves two early Gaussian-12 window comparisons marginal. Their original outcomes remain unchanged in the [historical assessment](diagnostics/population-accuracy/joint-error-assessment.json). The prescribed-field study also retains two separate corrections: the smooth response replicated under new phases at the same actions and forcing, and constant diffusion with restoring drift can fail a flat finite-lag variance screen. Neither correction is a result of the present population comparison. [Earlier response study](response.html).

## Data, code and correspondence {#reproduction}

The [public benchmark](https://github.com/djova/bar-halo-benchmark) contains inputs, numerical methods and reproduction commands. The [reproduction map](reproduce.html) distinguishes checking supplied values from rerunning the evolution and states the coverage of each released study. The archived project receipt documents exact reproduction of 162 saved arrays; that is software reproducibility, not additional physical sampling or external scientific review.

{{CLAIM:REP-01}}

Questions and corrections can be submitted through the [public issue tracker](https://github.com/djova/bar-halo-benchmark/issues), using an equation, figure or claim identifier and the release version. Analysis, software and exposition were developed with AI assistance. The human project maintainer is djova; no institutional affiliation or outside endorsement is asserted.

{{REVISION}}

{{BIBLIOGRAPHY}}
