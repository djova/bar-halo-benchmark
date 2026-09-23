# Finite-time population bias in noisy sweeping resonances

**A reproducible response-kernel benchmark and population-approximation test**

Galaxy Bar project · Research note for external criticism · 23 September 2026

This computational research note was developed with AI-assisted analysis and
software implementation. It has not undergone external scientific review.
The interactive publication and executable package are the primary presentation;
this document is a compact manuscript for substantive criticism.

## The question

What information about an initial orbital population must be retained to predict
its finite-time response to a noisy, moving resonance? A reduced model often
replaces a physical distribution function with a convenient tracer population.
Matching the density and its slope at one action need not match the distribution
over the region actually sampled by the response.

We study this choice in an externally prescribed local resonance model. At the
same central density, initial logarithmic slope, bar history and noise strength,
a selected Gaussian and reference-halo weighting in the tested action slice give
opposite early noise effects. At a later endpoint both show suppression, but the
Gaussian magnitude is about 4.735 times larger. A slope-matched exponential is much
closer to the halo calculation. This motivates a practical question: can a cheap
approximation be checked *before* independently evolving the desired population?

At a preselected doubled sweep rate, a frozen gradient-mismatch allowance
qualifies eight of twenty candidate comparisons for 5% accuracy. Independent
population evolution supports all eight. Four other comparisons meet 5% but are
not qualified by the allowance: the procedure is informative and conservative
within this family. It is not a universal accuracy certificate.

The contribution is a quantitative, reusable calculation with explicit
error and cost evidence. The model's linear dependence on initial population,
the gradient triangle inequality and control-variate variance reduction are not
claimed as new mathematical principles.

## The dynamical experiment

Let j be the slow action measured from the moving resonance, ψ the resonant
angle, and s its dimensionless sweep rate. The implemented case has negative
frequency gradient. In its dimensionless convention,

    dψ = −j dt
    dj = (−sin ψ − s) dt + √(2D) dW,    D = 2η/π.

The bar impulse is B(T)=−∫sinψ dt. The −s term moves the coordinate origin;
the Brownian impulse is imposed scattering. Neither is counted as bar torque.
The numerical path budget keeps these three contributions separate. Positive
noise-minus-smooth response means increased transfer from the imposed bar to
the sampled halo slice; negative response means less transfer than the smooth
control, not necessarily a reversal of the total transfer.

The initial resonant phase is uniform. The reference population is the isochrone
halo DF evaluated on one fixed pair of fast actions, with central slow action
J<sub>s,0</sub>=0.25, radial action 0.08 and vertical action 0.05 in the analytical
model's units. The coordinate x=(J<sub>s</sub>−J<sub>s,0</sub>)/u uses
u≈0.0005633691. We compare positive weights at fixed central density and slope,
without resetting their masses to one:

    halo:          wH(x) = fhalo(Js, fixed fast actions) / fref
    exponential:   wE(x) = exp(gx)
    Gaussian:      wσ(x) = exp(gx − x²/(2σ²)),   g ≈ −0.0047493212.

Every profile receives the same smooth compact window. The primary window has
plateau 24 and cutoff 40; the wider check has plateau 48 and cutoff 64. Moving the
physical taper is different from enlarging the numerical domain or auxiliary
sampling support. The displayed response is ∫wK<sub>B</sub>dx. Multiplication by
4u²(2π)³f<sub>ref</sub>≈2.7022892×10<sup>−6</sup> gives the differential angular-
momentum contribution per unit fast-action area. None of these numbers is the
total torque of a complete halo.

## A failed approximation and a successful one

The original moving condition has s=0.25, η=0.1, and endpoints T=10 and 20.
These correspond to finite elapsed times; T=20 is about 3.18 reference librations.
The resonance sweeps across 2.5 reference half-widths by the later endpoint.

| Initial weight | Response at T=10 | Response at T=20 |
|---|---:|---:|
| Gaussian, σ=8 | +0.00150765 | −0.16194914 |
| Reference halo in the tested slice | −0.00390068 | −0.03420023 |
| Slope-matched exponential | −0.00389873 | −0.03422348 |

![Three populations at the two recorded endpoints](https://djova.ca/galaxy-bar/diagnostics/population-accuracy/population-comparison.png)

**Figure 1: Population choice at fixed dynamics.** Both endpoints use common
absolute density normalization. Intervals describe the trajectory sampling;
the linked records supply paired numerical controls. The early Gaussian and
halo signs are resolved. The late magnitude ratio is conditional on this model
and duration, not a universal correction. Reference-halo weighting refers to
the isochrone DF in the tested action slice.

The exponential-minus-halo point differences are about 0.050% and 0.068%. Their
paired sampling intervals are tight, but those percentages alone are not a
certified sub-0.1% accuracy statement. Both statistical and numerical uncertainty
must be considered. The broader lesson is not that every local approximation
fails: the gradient structure retained by the approximation matters.

For the moving condition and primary window, pairing the two populations within
each of the eight batches gives the following difference. All entries retain
the response units of Figure 1.

| Endpoint | Exponential minus halo | Paired sampling 95% interval | Absolute-difference proxy including refinements |
|---|---:|---:|---:|
| T = 10 | +1.9423 × 10⁻⁶ | [1.9005, 1.9840] × 10⁻⁶ | 2.0065 × 10⁻⁶ |
| T = 20 | −2.3252 × 10⁻⁵ | [−2.3373, −2.3132] × 10⁻⁵ | 2.3457 × 10⁻⁵ |

The last column adds the maximum absolute paired sampling endpoint, the paired
timestep allowance, and the sum of absolute paired changes in the independent
solver/window checks. The separate stochastic window-change intervals remain
in the released record. This is a practical assessment of the small difference;
it is not a rigorous joint certificate for a percentage whose halo denominator
also has numerical uncertainty. The paired calculation is independently
recomputed by the public `reproduce_accuracy_audit.py` command.

At early time, the Gaussian's gradient-coordinate contributions inside and
outside radius 4 are approximately −0.011058 and +0.012565. The corresponding halo
terms are −0.004835 and +0.000934. Different cancellation produces different signs.
These are terms in an integral decomposition, not literal cohorts of starting
orbits. The public explorer separately retains the ordinary initial-action
kernel and actual population-weighted orbit cohorts.

## Separate orbital response from material weighting

For this prescribed, population-independent dynamics, define

    KB(x) = E[Bnoise − Bsmooth | initial action x],
    R[w] = ∫w(x)KB(x) dx = −∫w′(x)Q(x) dx.

Here Q is a primitive response kernel, with the boundary term included or zero
for the shared compact support. The orbit dynamics can be strongly nonlinear;
linearity in the initial population follows from the external evolution, not
from weak trapping. It need not survive self-consistent gravitational response
or an evolving population-dependent collision law.

The kernel predicted three previously unevolved populations in the earlier
campaign. All 24 correlated comparisons passed their original operational tests.
Those allowances were max(0.0002, 5% of the forecast); this was never uniform 5%
accuracy. A subsequent joint numerical-proxy assessment retains 22/24: both early
width-12 window comparisons remain marginal. Their historical pass is preserved,
while their expanded error assessment is stated separately. Reproducing these
calculations does not create additional independent physical evidence.

## Turn gradient mismatch into a decision

For an approximation v to a desired weight h, the exact kernel gives

    |R[v] − R[h]| ≤ ∫|v′ − h′| |Q| dx.

This elementary inequality weights population error where the dynamics are
sensitive to it. Matching a derivative at one point is insufficient, but a
nearby gradient over the relevant region can make the allowance small. Signed
cancellation may make the bound conservative; a rejection need not mean an
approximation is wrong.

![Frozen error allowances and independently measured discrepancies for all twenty candidate comparisons](https://djova.ca/galaxy-bar/diagnostics/population-accuracy/population-accuracy.png)

**Figure 2: A prospective test of population-approximation accuracy.** Orange
circles show the full allowance frozen before independent evolution; blue
crosses show the approximate-kernel forecast's absolute discrepancy from the
independently evolved halo. The scale is the frozen 5% target, with values below
one shaded. Blue intervals add the independent halo's numerical proxy. All
profiles, endpoints and windows are shown. Gaussian 128 illustrates conservatism:
its orange point lies outside the budget while its blue point fits inside.
The interactive version exposes the signed gradient-coordinate contributions
and the larger absolute allowance, separately from this total forecast error.

The kernel itself is sampled. We therefore use eight independent batches and
a nominal simultaneous Student-t envelope across its finite cells, with
Bonferroni allocation between kernel and scalar-contraction families. Population
contractions preserve their covariance. Paired timestep differences and
factor-two mesh changes provide practical numerical allowances. Those
refinements are not proven truncation bounds; Student-t coverage of Monte Carlo
batch means is an approximation. This is an operational accuracy diagnostic,
not a distribution-free certificate.

The prospective condition doubles the sweep to s=0.5 at the same η=0.1. It uses
its own newly sampled kernel. The family—halo, exponential, and Gaussian widths
8, 32, 128, 512—was fixed before the new outcomes, as were both times and windows.
No absolute error floor can be relabeled as 5% accuracy. Near cancellation the
test reports absolute errors and leaves percentages unqualified. Numerical
forecasts are committed before independent forward-distribution and positive-
characteristic population evolution.

**Prospective outcome.** All fourteen independent numerical cases completed
with their mass, positivity, support and applicable budget/analytical controls
passing. Of twenty candidate comparisons, eight were qualified for 5% accuracy
in advance: the exponential and Gaussian 512 at both times and windows. Every
one is supported after adding the independent numerical proxies. There are no
contradicted or inconclusive 5% qualifications. All fifteen qualified signs
are independently supported. Four halo self-comparisons are numerical
references and are excluded from these candidate counts.

| Approximation | Intrinsic population error at T=10 | At T=20 | Frozen 5% decision / independent assessment |
|---|---:|---:|---|
| Exponential | 0.056% | 0.171% | Qualified / supported |
| Gaussian 8 | 348% | 763% | Not qualified / outside 5% |
| Gaussian 32 | 16.6% | 49.9% | Not qualified / outside 5% |
| Gaussian 128 | 1.06% | 3.27% | Not qualified / within 5% |
| Gaussian 512 | 0.118% | 0.365% | Qualified / supported |

Table values use the primary window and the point ratio
|R[v]−R[h]|/|R[h]| from independent evolution; they are not certified percentage
limits. Both physical windows have the same qualitative decisions. The frozen
allowance plus its uncertainty contains the independently measured population
error and paired numerical proxy in all twenty candidate comparisons. The
four Gaussian-128 rejections quantify conservatism. No threshold, population or
numerical ladder was changed after seeing these outcomes.

The recorded mean kernel also shows why those rejections occur. At the primary
window, Gaussian 128's signed population error has magnitude about 0.00009479
at T = 10, while the absolute-gradient integral is 0.00052005; at T = 20 the two are
0.00216566 and 0.00347405. Before any explicit kernel-uncertainty expansion, the
latter integral already exceeds the frozen 5% target at both endpoints and both
windows. Thus the reported conservatism is not solely an effect of the
simultaneous confidence factor: discarding signed cancellation matters. These
are contractions of the recorded mean kernel, not exact-kernel bounds or a
new prospective test. More samples are not automatically a remedy for an
absolute-contribution allowance.

This test supports a usable distinction within the declared regime: preserve
the gradient across the response-sensitive action region, rather than imposing
curvature merely to select convenient tracers. The test does not establish a
universal width threshold. Twenty correlated comparisons at one new dynamical
condition are not twenty independent validations of a theory. The allowance's
Student-t approximation and refinement proxies remain limitations even though
this particular prospective check succeeds. Every independently evolved
response in the new condition is negative; this prospective sign check does
not establish performance across a sign-changing family. The original
opposite-sign population example remains a separate s=0.25 result.

The diagnostic does not make the kernel free. The new kernel required about
5,105 worker CPU-seconds; contracting the six-profile family and both windows
and times took about 0.8 CPU-seconds. When the complete reference DF and kernel
are already available, directly contracting the reference DF is itself cheap.
The allowance then audits an approximation or supports a compact representation;
it is not a cheaper substitute for a known exact contraction. Any savings from
reusing a kernel across populations must be distinguished from the cost of
constructing a new kernel when the dynamics change. These measured costs do
not establish a universal break-even point against another solver.

## Estimate a small transfer without subtracting large raw impulses

Let F′=w and y=j+sT−W=x+B. Under the specified additive, externally prescribed
noise and canonical maps, phase-space area and the zero phase mean of bar torque
give the zero-integral identity ∫E[F(x+B)−F(x)]dx=0. Thus

    ∫w(x)E[B]dx = −∫E[F(x+B) − F(x) − w(x)B]dx.

The right side estimates a nonlinear remainder. For a nearly affine local
weight its leading term is proportional to w′B²/2, rather than the much larger
first-order impulse. Its support requires auxiliary initial actions extending
past the physical window by the maximum bar impulse. Those auxiliary samples
do not add halo mass. The derivation requires more than area preservation alone,
and does not automatically extend to action-dependent torque/noise, nonuniform
initial phase or live collective response.

![Estimator efficiency and measured versus projected precision](https://djova.ca/galaxy-bar/diagnostics/population-accuracy/estimator-efficiency.png)

**Figure 3: Variance versus actual computation cost.** Both estimators use
identical paths and numerical weights, including method-specific setup costs.
The left panel shows the conditional cost-times-variance ratio and whole-batch
bootstrap intervals. The right distinguishes measured eight-batch precision
from repeated-batch cost projections. Narrow Gaussian stress populations expose
where the advantage vanishes. The first timing run's weight-representation
mismatch and its matched-weight correction remain in the provenance appendix.

The corrected 16-case benchmark used about 347 worker CPU-seconds. At moving
T=20, a halo-weighted batch costs 18.40 seconds with raw weighting and 18.56
seconds with the remainder. The conditional cost-times-variance ratio is about
6,928, with a paired-batch bootstrap interval [6,735, 7,229]. The gain comes from
variance reduction; it is not a directly timed 6,928-fold speedup at a specified
final error. The noisier between-batch ratio is about 2,749. Both estimates and
their assumptions remain available.

For a Gaussian of width 1/64, that ratio is about 0.993: the advantage disappears.
This is consistent with the remainder losing its small-gradient advantage when
the weight varies sharply across a bar displacement. It is not a universal
efficiency law. One of 24 pointwise paired raw-minus-remainder intervals excludes
zero (stationary T=10, width 1); all samples and that flag are retained. No sample
was enlarged or removed to force agreement.

A fresh public-source run regenerated all 16 numerical mean/covariance records
exactly, with CPU performance independently remeasured. The variance-reduction
principle is established Monte Carlo methodology. Priority for this particular
cumulative construction has not been established; its practical contribution
rests on measured usefulness, stated assumptions and reusable code.

## Relationship to prior work and scope

[Hamilton et al.](https://arxiv.org/html/2208.03855v2) studied diffusion-supported
stationary resonant friction and explicitly used a local linear population.
[Chiba](https://arxiv.org/html/2305.00022v2) analyzed moving-resonance feedback,
compared a collisionless reduction with three-dimensional calculations, and
discussed competing diffusion effects. These works already supply the physical
setting; the qualitative possibility of opposing effects is not our discovery.

[Ogilvie & Lubow](https://doi.org/10.1111/j.1365-2966.2006.10506.x) provide an
important migration–diffusion analogue in gaseous planetary corotation
resonances, with different physical assumptions. Control variates also have a
large independent literature, including [Dellaportas & Kontoyiannis](https://academic.oup.com/jrsssb/article-abstract/74/1/133/7074993).
The present benchmark is not their reversible-MCMC setting and claims neither
the control-variate principle nor a Poisson-equation method as new.

The bounded result concerns a single fast-action slice, finite duration,
prescribed bar and constant additive action diffusion. Three-dimensional
transfer remains unvalidated: the archived Cartesian pilot was stopped because
its estimator could not resolve the required discrepancy within the measured
cost budget. That is unresolved agreement, not evidence that the local model
is wrong. Neither this experiment nor a successful local diagnostic establishes
physical SIDM, collective halo response, an asymptotic torque law or agreement
with observed galaxies.

## Reproducibility and external criticism

The [public benchmark repository](https://github.com/djova/bar-halo-benchmark)
contains exact input generation or arrays, source, frozen seeds, dependency
versions, numerical reference outputs and commands. The accuracy release adds
the eight-kernel, fourteen-case experiment through `reproduce_accuracy.py`,
alongside the corrected-cost and retrospective-audit commands. The original
kernel and independent stages used 1.42 and 2.31 worker core-hours respectively;
these are summed CPU work, not elapsed wall time. A fresh HTTPS clone at public
commit `66143eb`, with an isolated pinned Python environment, reproduced all
eight kernels and fourteen independent cases. Every one of 162 saved numeric
arrays matches exactly, as do all checked forecasts and qualification outcomes.
The regenerated figure has identical RGB pixels and was visually inspected.
The two stages used 1.31 and 2.29 worker core-hours in the rerun. This repeats
released seeds; it verifies reproducibility, not additional physical evidence.
The [complete receipt](https://djova.ca/galaxy-bar/diagnostics/population-accuracy/accuracy-reproduction.json)
records source, dependencies, arrays, decisions and figure checks. Private
archives are not a dependency of the scientific release.

The most useful external questions are whether an equivalent finite-time
population counterexample or cumulative estimator already exists; whether the
diagnostic is sufficiently informative to guide a real reduced calculation;
and which physical generalization would most decisively test its relevance.
No external endorsement or reviewer agreement is implied.
