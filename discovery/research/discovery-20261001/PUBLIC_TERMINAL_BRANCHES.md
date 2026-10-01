# Two completed reference experiments

These early validation results close the collision-law and modified-inertia
branches of the 1 October 2026 campaign. A prescribed gas experiment did not
produce a collision-law impulse contrast that passed its selected numerical
checks. A frequency-domain experiment verified exact harmonic reference
solutions and quantified how much a shared circular calibration leaves
undetermined. Neither result establishes a live-galaxy response or an observed
prediction.

The compact figure data are [scattering.json](../../data/scattering.json)
and [inertia.json](../../data/inertia.json). They retain
unrounded numerical values, conditions, control decisions, original file
SHA256 values and exact JSON pointers. The source and reproduction bundle await
a clean public release. Evidence record IDs identify archived inputs; they
are not live public URLs.

## Matching collisions did not yield a qualified impulse contrast

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

## Equal circular laws leave different harmonic frequencies

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

## Inspecting the plotted evidence

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
