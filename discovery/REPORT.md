# Early validation of hidden galactic dynamics

Release **discovery-2026-10-01.6** retains the prescribed-field bar-transfer,
finite halo-heating and radial-memory results. The [new recorded controls](CHECKS_V2.md)
show what the larger stellar sample, late spatial quadratures and sealed weak-bar
forecast do—and do not—establish. The [previous control collection](CHECKS.md)
retains the phase comparison and historical failed pilots.

The inner guiding cohort contains 2.65% of stellar target mass yet carries nearly
all sampled finite-pulse heating. The all-state stellar numerical qualification
still fails; an incomplete extension cannot repair it. In the spatial echo model,
the fine time28 field lies near the leading approximation, while all original
coarse-to-fine gates fail. Cross grids locate sensitivity to angular-momentum
quadrature; they do not establish an observable echo.

A new, separately sealed epsilon=10^-4, T=40 twin forecast has provisional
numerical proxies for p=6 and p=8; p=4 remains tail-unqualified. The independently
driven outcomes remain pending. It does not explain the earlier stronger,
longer forcing history. All seven **unforced** forecast grids regenerate with
the public NumPy operator; no exact-array or forced-evolution reproduction is
claimed. No observation, live bar or self-consistent core is validated.

The three principal questions remain: how do hidden orbital populations alter a
prescribed response; which stars bear a proposed halo-heating cost; and is
recoverable halo memory strong enough to yield a measurable spatial field?
The other screens retain a collision-law contrast with an unqualified numerical
sign and harmonic modified-inertia freedom without an observational test.

The [source guide](README.md) separates reading, saved arithmetic and explicit
execution. [The manifest](manifest.json) records hashes and scope. Reproduction
checks software/operands; it is not another independent physical sample. This
campaign remains preliminary and has not been externally reviewed.

## Identical ordinary halo moments, different prescribed-bar response

**Preliminary prescribed-field result, 1 October 2026.** Two analytic halo
populations can have exactly the same density, local mean velocity and all even
velocity moments, while their responses to an imposed rotating bar differ. For
the fixed p = 8 construction at the reference frequency, the measured accumulated
angular-momentum-transfer contrast is **8.49×10⁻⁵**, with a nominal pointwise
95% interval **[5.54×10⁻⁵, 1.15×10⁻⁴]**. These are reference mass–action units;
they are neither a galaxy slowdown nor a dark-matter constraint.

The corresponding plus/minus transfer ratio is **1.446**, a ratio of ensemble
point estimates. We have not established a confidence interval for that ratio
or reached the original factor-of-two ambition. The shared reference transfer
has substantial uncertainty, which is retained alongside the better determined
paired contrast. This is a tracer calculation in prescribed fields, with no
reacting halo or stellar disc.

### What was deliberately held equal

In the unsoftened spherical isochrone with G = M = 1 and b = 1/2, the frozen positive
populations are

\[
F_\pm=F_0(e)\pm\alpha_p L_z[g_{0,p}(e)+L^2e^p],\qquad p\in\{4,6,8\},
\]

\[
g_{0,p}(e)=-\frac{4p\,e^{p-1}}{(p+5/2)(p+7/2)}
          +\frac{8b\,e^p}{p+7/2},\qquad e=-E.
\]

Odd velocity parity preserves density and every even moment. A separate
Beta-integral cancellation preserves all three local mean velocities at every
radius and inclination. An exact rational positivity construction fixes each
α before reading the family's forced responses and gives F±≥F₀/2 throughout
the bound orbital domain. Higher odd moments can differ: the public data
contain the actual unforced azimuthal third moments at eight radii and four
inclinations. Those profiles illustrate hidden velocity structure; they do not
predict the torque by themselves.

See the [derivation](research/discovery-20261001/TWINS_EXACT_MOMENTS_DERIVATION.md),
[frozen unforced protocol](research/discovery-20261001/TWINS_EXACT_MOMENTS_PROTOCOL.md) and
[independent internal algebra check](research/discovery-20261001/TWINS_EXACT_MOMENTS_CHALLENGE.md).
Stationarity and self-consistency hold for this spherical unsoftened reference.
Collective stability, a softened live equilibrium and formation-history
reachability remain unestablished. The original short paired-particle live screen
failed its numerical qualification; its replacement is a separately frozen test.

### What the measured contrast supports

The eight independently randomized action/phase libraries are the sampling
units. All three populations and both stationary bar frequencies share those
libraries, so the six comparisons are correlated. The full contrast and
contrast/reference covariance matrices and all eight library vectors are
available in [the scientific export](data/twins-exact.json).
Student-t intervals with seven degrees of freedom have uncalibrated coverage;
supplementary Bonferroni intervals apply only to these six comparisons.

At the reference frequency, p = 4 has an unresolved sampling sign and fails one
of the two doubled-phase checks. The p = 6 and p = 8 contrasts pass the selected
phase and timestep screen, whose frozen allowance is 10% of the measured
contrast. The largest p = 8 phase shift is 2.82×10⁻⁶, or 3.32% of its contrast.
The half-step shift is 2.10×10⁻¹². These are selected numerical comparisons,
not a complete discretization error bound.

For p = 6, the supplementary six-comparison interval is nominally positive, but
its lower margin (1.24×10⁻⁶) is smaller than the largest measured phase shift
(2.92×10⁻⁶). The recorded screen decisions remain unchanged; they must not be read as
a joint sampling-and-numerical sign guarantee. The p = 8 supplementary lower
margin is 3.95×10⁻⁵, substantially larger than the selected shift, while still
subject to the stated sampling and numerical limitations.

The second stationary frequency has no doubled-phase comparison. Its timestep
checks alone do not qualify phase accuracy. Neither frequency is a new-history
prospective prediction: these are known recorded trajectories contracted with
populations fixed from unforced inputs, without response fitting. The
[response protocol](research/discovery-20261001/TWINS_EXACT_RESPONSE_PROTOCOL.md) records that distinction.

Physical mass is preserved absolutely. Because the trajectories were sampled
from the approximate AGAMA distribution Fq, the contraction uses
m(F₀±αδF)/Fq, with no separate population normalization. The represented exact
mass is recorded rather than silently rescaled. Angular-momentum and
energy/external-work residuals are supplied as numerical bookkeeping checks;
they do not establish a live-halo or observational result.

### What this teaches us, and what would test it next

Matching the ordinary local halo moments need not specify its response to a
rotating gravitational perturbation. This construction removes the finite-grid
streaming mismatch of the earlier search, but it does not establish different
self-consistent bars. The completed gradual-growth history below checks another forcing history.
Collective stability and self-consistent bar evolution remain separate tests. The derivation is internally checked, not
externally reviewed; priority relative to existing halo-population and
resonant-response work remains an open scholarly question.

The scientific export contains actual scalar values, paired refinements,
covariances, velocity-moment quadrature checks and hashed archive selectors.
The [compact analysis replay](README.md#exact-moment-halo-twins)
regenerates the six contractions, their intervals and covariance from released
saved impulses and sampling-density operands. Full orbit evolution and the
velocity-marginal quadrature are not regenerated by that replay. The older
preliminary coarse readback is retained; this summary uses the terminal
`exact-response-final-01` record and does not overwrite that history.

## Gradual bar growth retains a resolved contrast in one construction

The bar now starts at zero amplitude, grows through a fixed smooth ramp over
100 isochrone reference time units, and remains at amplitude 0.03 throughT = 300.
The positive p4, p6, p8 populations and pattern speed are unchanged. Eight new
independent whole action/phase libraries supply the ensemble; they are not
neighboring points from the earlier samples.

AtT = 300,p6 gives plus-minus accumulated transfer **3.69349e-5**. Its nominal
pointwise 95% interval is **[1.14981e-5,6.23717e-5]**; the supplementary
three-population interval is **[3.29115e-6,7.05787e-5]**. p8 is positive under
its pointwise interval but unresolved under that population-family interval;
p4 is unresolved under both. These sampling statements are not rigorous joint
sampling/discretization guarantees. Selected azimuth, radial-phase and timestep
checks pass; their signed shifts and larger absolute-family sums remain reported.

The [record](data/twins-growth-v1.json) supplies all 25 saved times, shared
covariance and selected refinements. The [readback](research/discovery-20261001/TWINS_GROWTH_RECOVERY_READBACK_V1.md)
explains the interrupted original and separate completion of its three planned
refinements. The original command remains interrupted. The [saved-array replay](operands/twins-growth-v1/README.md)
recomputes12,894 values from eight compact NPZ files; it evolves no orbits.

The distributions use three orbital integrals. They do not contradict uniqueness
arguments restricted to two-integral populations. Neither imposed history is
an independently calibrated magnitude forecast or evidence for live bar braking.

### The force law and particle sampling remain separate qualifications

The analytic equilibrium uses the unsoftened reference potential. A particle
realization evolved with softened forces therefore needs its own entrance and
unforced-evolution tests. The first paired-particle screen failed: all nine
cases exceeded its energy criterion. An independent all-particle direct-potential
calculation reproduced the early energy offset. A separate isolated-partner
calculation found the same scale and quadratic timestep dependence. The paired
particles shared positions, creating close-pair binding absent from the intended
smooth population. This is a concrete sampling problem, not evidence that the
analytic populations are collectively unstable.

A separately frozen, distinct-position sampler preserves matched initial
positions, masses and raw even-total-degree velocity products while sampling
opposite velocity signs probabilistically. Finite-sample mean velocities and
therefore centered moments need not match. All nine unforced runs are complete
and pass their declared numerical screens, including selected timestep checks.
Their shell-moment adjustment flags remain; the same-sample analytic phase
control explains a substantial contribution without establishing equilibrium
under the softened force. See [the paired controls](CHECKS.md#stationary-orbital-phases-move-finite-sample-shell-moments).
No driven live bar is qualified.
The [force/support evidence](research/discovery-20261001/TWINS_FORCE_SUPPORT_PUBLIC_V1.md)
and [compact record](data/twins-force-support-v1.json) preserve the failed gates,
selected force refinements and energy diagnosis. Their arithmetic reader checks
the supplied outputs; it does not rerun gravitational evolution.

## Finite central halo heating survives the cusp test

A separate Hernquist + positive finite gas model has a genuine inner circular
frequency8 resonance. Unlike the cored example, it cannot rely on a finite
upper circular-frequency gap. The halo and stellar populations both changed
between these models; this is a new physical experiment, not a controlled
change of halo density alone.

At the same amplitude 0.003 and duration 80, a new8,192 IID-state calculation gives
central tag-specific energy gains **(1.2939±0.1344)e-5** at frequency 5 and
**(3.8432±0.4390)e-6** at frequency 8. The errors are one empirical standard
error, not95% confidence intervals. Absolute target mass weighting is retained;
the sampled target is not renormalized. The finer timestep passes the frozen
selected work/inverse/angular-momentum/reference gates; the coarser frequency8
work gate fails and remains in the evidence.

These are small deposits—about 15.0 and 4.45 parts per million of the tag binding
energy. They do not establish a core. The finite-minus-weak differences are only
1.75 and 1.99 empirical standard errors, with rare contributions and uncalibrated
coverage; no robust nonlinear correction is qualified. The earlier 512-state
halo pilot failed its sampling-precision target and remains distinct.

The separate 512-state finite warm-star pilot is complete but fails its
sampling-precision gate. Tighter selected references repair a different
integrator comparison without qualifying the heating estimate. The weak cusp
calculation suggests that inner stellar costs are much larger than whole-disk
averages. No finite stellar/halo selectivity ratio is qualified: dividing the
halo gains into weak stellar values would combine different approximations.
See [the stellar precision controls](CHECKS.md#warm-stellar-heating-remains-statistically-unresolved).
Read the [physical summary](research/FEEDBACK_CUSP_PUBLIC_SUMMARY.md),
[finite result](research/FEEDBACK_CUSP_FINITE_RESULT.md),
[compact operands](data/feedback-cusp.json) and
[arithmetic replay instructions](research/FEEDBACK_CUSP_REPLAY.md).

## Two completed reference experiments

These early validation results close the collision-law and modified-inertia
branches of the 1 October 2026 campaign. A prescribed gas experiment did not
produce a collision-law impulse contrast that passed its selected numerical
checks. A frequency-domain experiment verified exact harmonic reference
solutions and quantified how much a shared circular calibration leaves
undetermined. Neither result establishes a live-galaxy response or an observed
prediction.

The compact figure data are [scattering.json](data/scattering.json)
and [inertia.json](data/inertia.json). They retain
unrounded numerical values, conditions, control decisions, original file
SHA256 values and exact JSON pointers. A [limited source bundle](README.md)
and a [known-control reproduction receipt](reproductions/public-controls-01/receipt.json)
are included in this package. The receipt covers three regenerated reference
controls, not the full response ensembles. Evidence record IDs identify archived
inputs; historical run directories are not included as live downloads.

### Matching collisions did not yield a qualified impulse contrast

The gas moves through a periodic cosine potential whose phase accelerates.
The potential applies a force to each particle, and the accumulated mean force
is the external impulse per unit particle mass. Collisions redistribute
velocities while conserving pair energy and vector momentum. Changing their
angular law can therefore change how particles sample the moving force. The
measurement is the signed difference in final impulse, rather than the
magnitude of a difference or a snapshot of particles inside a separatrix.

Matching a scalar transport coefficient is a useful approximation with
published support: [Fischer & Sagunski (2024), section 4.4](https://arxiv.org/html/2405.19392v2)
found viscosity matching effective in their dynamical-friction experiments.
Validated treatments of small and large scattering angles also precede this
screen, including [Arido, Fischer & Garny (2025)](https://arxiv.org/abs/2410.07175v2).
Our first viscosity-matched experiment found a positive 0.1-radian-minus-isotropic
contrast on one waveform, but its continuum magnitude remained unresolved and
the positive-sign endpoints failed under another waveform and weaker
transport. Its 0.2-radian stress control also failed the frozen equivalence
margin. Those outcomes remain visible in the export.

The stronger comparison matched more of the collision operator. Law A chooses
the scattering cosine 0 with probability 1/4 and 2/3 otherwise; law B uses
1/3. Uniform azimuths and the rate relation Gamma_B = 3 Gamma_A / 4 give both
laws the conditional velocity drift -Gamma_A u / 4 and raw second tensor
Gamma_A |u|² I / 12. Their fourth angular decay differs by 53/32. This matches
increments of the linear coordinate v_x; it does not match nonlinear energy
increments or halo actions. Analytic and sampled operator checks, Maxwell
controls and the full stress comparison all passed. The maximum stress
interval endpoint was 0.04524, within the fixed 0.05 initial-stress margin.

The default figure places the four final B-minus-A impulse intervals on the
same signed axis. With epsilon = 0.25 and sweep = 0.025, the mean was
-0.00537312 and its nominal 95% interval was [-0.01063874, -0.00010750].
This narrow exclusion of zero selected the frozen numerical refinements.
Halving the timestep gave -0.00494624, with [-0.01049270, 0.00060021]; doubling
the cell count gave -0.00212885, with [-0.00796445, 0.00370676]. Both intervals
include zero, so the required signed signal at every selected discretization
failed. The contrast-change intervals also include zero: the result does not
identify a particular numerical bias or a precise continuum magnitude.

On the second waveform, epsilon = 0.16 and sweep = 0.04, the mean was
0.00001286, with [-0.00436572, 0.00439144]. Its unresolved primary did not
select refinements. Each response interval uses 16 independent initial-state
seed pairs and a nominal per-condition Student-t interval. Shared initial
states do not provide shared stochastic collision histories. There was no
overall multiple-test pass; supplementary Bonferroni intervals for the two
waveforms both include zero and do not cover the earlier adaptive campaign.
The four-seed stress intervals are pointwise, not simultaneous history bands.
An interval containing zero demonstrates neither equal dynamics nor
convergence. This branch supplies no qualified reason to advance this
prescribed gas result to a responsive halo.

### Equal circular laws leave different harmonic frequencies

The inertia experiment solves complete harmonic histories in a separable
force field. For each axis, the acceleration measure is a sum of all modes,
weighted by their frequency ratios. The selected interpolation is
mu(x) = x / (1 + x), and the filters are Theta_q(y) = 2 / (1 + |y|^q),
with q = 2, 4 and 8. The equations and the q = 2 example are already in
[Milgrom (2022 v3), equations 20 and 27–32 and page 12](https://arxiv.org/pdf/2208.07073v3).
The common normalization Theta_q(1) = 1 fixes the same circular relation for
every filter while allowing different coupling between distinct frequencies.

All frozen checks passed across 126 two-axis cases, three initial guesses per
case and nine single-frequency benchmarks. The maximum logarithmic equation
residual was 3.12 × 10⁻¹⁴; the largest relative frequency spread across guesses
was 1.20 × 10⁻¹⁴. The single-frequency quadratic solution, harmonic energy and
force checks agree within their specified tolerances. These checks establish
a reference problem for the recorded modes, rather than general uniqueness or
a causal forced-response theory.

The default frequency figure holds Newtonian frequencies (1, 0.25), RMS
amplitudes (0.15, 0.0045), the interpolation and a0 = 1 fixed. The second-axis
frequency is 0.721857, 0.945364 and 1.192600 for q = 2, 4 and 8. Its range is
65.21% of the q = 2 frequency, while the first-axis range is 0.35%. Frequencies
use inverse reference time; amplitudes use reference length. These are
deterministic equation solutions, so the plot carries no statistical or
observational error bars. The calculation quantifies freedom in an existing
framework without establishing which filter describes stellar motion.

An equal-frequency comparison exposes a definition that matters before a
finite-window orbit solver can be used. With RMS amplitudes (0.15, 0.15),
Newtonian frequencies (1, 1 + 10⁻⁸) approach a solved frequency of 1.546923.
At exact equality, grouping the complex vector amplitude gives RMS amplitude
sqrt(2) × 0.15 and frequency 1.651670. The roughly 6.34% gap is the published
sharp-spectrum singular limit noted below equation 32. It is a grouping hazard
for this construction, not a measured discontinuity of stellar motion. A
finite-window spectral regularization must be defined before extending the
calculation. High-frequency suppression also depends on acceleration
amplitudes, not frequency ratios alone; the export records that structural
bound separately.

The usable outcome is an exact laboratory for comparing filter choices and
checking mode grouping. Observed kinematics and broader dynamical histories
remain untested.

### Inspecting the plotted evidence

The scattering figure rows are `full_moment_original`,
`full_moment_original_halfdt`, `full_moment_original_cells64` and
`full_moment_second`. They point to `primary_B_minus_A` or the exact
`rows/0/contrast` and `rows/1/contrast` fields in the archived analyses. The
original refinement trigger is stored separately from
`signed_signal_at_all_selected_discretizations = false`.

The inertia figure rows are `harmonic_filter_q2`, `harmonic_filter_q4` and
`harmonic_filter_q8`, pointing to `benchmarks/3`, `benchmarks/48` and
`benchmarks/93` in the retained second screen. Its grouping rows point to all
three entries of `degenerate_frequency_limit`. Each export's `evidence` object
gives the exact archived file hash and JSON pointers, and its
`recorded_provenance` object retains the recorded source and protocol hashes.
Rounded prose values do not replace those numerical operands.

## Recoverable halo memory with a small gravitational readout

A selected spherical halo population passes radial echo controls in a prescribed gravitational background. Its stronger tested pulses produce a force about 22 parts per million of the reference halo force. A separate spatial model has a verified leading prediction involving two orbital frequencies, with an even smaller force. Neither calculation establishes regenerated stellar structure or a self-consistent galaxy response.

The public data are in [echoes.json](data/echoes.json). This export contains recorded signed curves, unrounded operands, stable row keys, archived file hashes and exact JSON or array selections. The [limited source bundle](README.md) includes optional halo-echo sources and exact historical snapshots. Its [known-control reproduction receipt](reproductions/public-controls-01/receipt.json) covers the constant-shear echo and the harmonic/operator controls, not the halo predictions. Evidence IDs identify retained records; historical run directories are not included as live downloads.

### Original quadrupole pilot

The initial experiment applied two spatial quadrupole pulses and measured a complex gravitational multipole. Its late response failed numerical refinement. The original AGAMA sampling used quasi-random adaptive subsets, so historical independent-particle confidence labels were unjustified; the corrected block spread is descriptive. These pure quadrupoles were also not guaranteed positive standalone density sources. This pilot remains unresolved and is separate from the two models below.

### Selected radial halo population

The radial experiment uses an isotropic isochrone distribution with a smooth energy taper specified before forcing. It retains 95.21629% of reference halo mass with absolute weights. The remaining halo response is untested. Positive Plummer mass impulses at times zero and tau preserve the full angular-momentum vector. The measurement is the signed combination g_AB − g_A − g_B + g_0, averaged over a narrow annulus around radius one.

Independent dynamics and harmonic predictions, weak pulse-product scaling, a held-out separation and action-preserving radial memory erasure support the first 2 tau interval. The primary odd force statistic falls by a factor of roughly 7,300 when memory is erased. Baseline force is 1.8 parts per million of the background; stronger admissible pulses give 21.6 parts per million. Their isolated stable stellar oscillator reaches about 0.012 km/s if circular speed is illustratively set to 200 km/s. Its 0.015 km/s absolute-force bound applies to the specified interpolated field, rather than a self-gravitating disk.

Default force rows are `radial_baseline`, `radial_baseline_memory_erased`, `radial_separation_holdout` and `radial_stronger_holdout`. The export also retains the four counterfactual case arrays and additional amplitude controls. Time uses the reference dynamical unit; force uses G M0 / L0². No curve is normalized to the selected cohort mass.

### Positive spatial two-frequency model

The later spatial model combines positive Plummer sources with bounded angular density terms, using first m = 2 and then m = 4. Its declared Fourier vectors align both radial and apsidal phases at 2 tau. Radial-only, apsidal-only, two-frequency and nonrefocusing contributions are exported separately as full complex coefficients. Independent canonical formulations agree, but this remains a leading mathematical prediction without finite-amplitude spatial or memory-erasure confirmation. The entire angular force is below 0.1 part per million of the background.

Quiet controls use time-integrated RMS over fixed early and late intervals. Eighth-step temporal sampling and an energy/action refinement correct a sparse-date artifact; at tau = 16 the remaining potential, radial-force and tangential-force RMS values are 3.48%, 4.07% and 3.49% of their early values. These controls belong to this spatial model. They do not change its small force or establish a visible disk response.

[Chiba et al., *Galactic echoes*](https://arxiv.org/html/2506.16512v2) already supplies the underlying galactic echo theory. The present result verifies specified halo gravitational readouts. Halo self-gravity, realistic finite-duration encounters, direct stellar forcing, observational comparisons and useful structure regeneration remain untested.

## A controlled selective-heating example, with a spatial qualification

A prescribed gas fluctuation can give much less energy to mildly warm
coeval stars than to a stationary central halo tracer in this fixed,
initially cored spherical model. The contrast survives direct orbit
evolution, amplitude and timestep controls. It does not demonstrate a
dark-matter core or an acceptable old stellar disk.

The pulse oscillates at frequency 8, above the maximum circular radial
frequency 5.7548. Circular stars barely absorb it, while eccentric halo
orbits and warm stars still couple through higher radial harmonics.
This is a restricted frequency window outside the earlier ten-function
response bound, whose maximum nominal frequency was 5.

The resolved central forward energy is (2.393 ± 0.235)×10⁻⁶ per unit tagged
halo mass. The whole stellar population gains (8.089 ± 1.697)×10⁻⁹ per unit
stellar mass, giving point cost 0.00338. Errors are one family standard
error; radial phase particles are quadrature nodes. A frozen empirical
bootstrap upper-star/lower-central ratio 0.00598 passes the 0.02 sample
usefulness criterion, without certifying unseen continuum tails.

That whole-disk normalization substantially dilutes inner heating. Stars
with guiding radius below 0.25 constitute about 3.5% of the population and
gain (2.153 ± 0.485)×10⁻⁷ per unit cohort mass, giving cost 0.08996. The same
cohort's earlier frequency-5 waveform cost is 2.31294: the frequency-8
reduction is still about 26-fold in this inner group. Neither ratio is an
observational co-spatial stellar-heating bound. The measured inner radial
variance change is about 2.07×10⁻⁷; it is a separate moment diagnostic.

Halving the timestep changes central energy 0.0052%. Halving the amplitude
changes the quadratically rescaled stellar energy -0.098%, but the halo
changes +7.16%, which is retained as finite-amplitude response. An
independent local action derivative accurately predicts the direct warm
response. A positive passive ensemble expression agrees only after
population integration, explaining a preserved finite-sample discrepancy
between the two weak estimators.

The limitations are physically important. The halo tracer is cored and
does not generate the imposed field; the stellar guiding distribution has
a central density hole. Spherical forcing conserves the full angular-momentum
vector and hence the spherical angular action \(L-|L_z|\). It does not
guarantee unchanged vertical velocity dispersion or thickness. The pulse adds
only a few parts per million of the tag's
binding energy, and the tag excludes less-bound orbits that pass through
the center. A finite positive-density gas construction supplies a finite
continuity-flow kinetic budget, but no hydrodynamic feedback engine or
core-energy budget. The separate cuspy-halo calculation above now resolves a
small finite heating signal; its centrally populated warm-star pilot remains
sampling-unqualified. Those results do not establish the cored model's cost
ratio in a cusp.

Feedback heating and resonant coupling are established prior work:
[Pontzen and Governato](https://arxiv.org/abs/1106.0499),
[Ogiya and Mori](https://arxiv.org/abs/1206.5412) and
[Hashim et al.](https://arxiv.org/abs/2209.08631). The present contribution
is a bounded quantitative example and its adversarial controls. The
[scientific export](data/feedback.json) retains unrounded outputs,
normalizations, control results and hashes identifying the archived findings.
This release publishes outputs and this summary; it does not regenerate the
feedback orbit ensembles, response matrices or bootstrap. The completed finite
cuspy-halo result is reported above, with the unresolved coeval stellar cost
kept separate.
