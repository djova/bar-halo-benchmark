# Early validation of hidden galactic dynamics

This portable report contains the completed collision-law and modified-inertia
reference experiments, followed by the recorded halo-echo comparisons. Halo twins
and selective feedback heating remain active campaign branches; this checkpoint
reports no final outcome for either. The campaign is exploratory, with no
live-galaxy or observational validation established here.

The [source bundle guide](README.md) distinguishes supplied operands, arithmetic
verification, three regenerated known-limit controls and optional full-response
calculations. The [control receipt](reproductions/public-controls-01/receipt.json)
is a software reproduction of those reference controls, not another physical
sample. The [manifest](manifest.json) records released file hashes, preserved
archive hashes and explicit release-only transformations.

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
