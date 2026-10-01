# Fixed analytic populations contracted against recorded histories

Frozen 1 October 2026 after the independent unforced derivation/preflight and
before reading any bar response for the new family. The analytic family and
normalizations are already fixed by
[the exact-moment protocol](TWINS_EXACT_MOMENTS_PROTOCOL.md) and
[derivation](TWINS_EXACT_MOMENTS_DERIVATION.md). This reuses the existing
randomized experiment's known forcing histories; it is **not** a prospective
prediction of a new physical history or a response-optimized population search.

Use p={4,6,8} with α values fixed by the exact rational global bounds in
`exact-moments-preflight-02/frozen-populations.json`. No coefficient, amplitude,
duration, pattern frequency or normalized mass changes in response to the
contractions. Both imposed stationary histories have amplitude 0.03 and duration
300, with reference resonance origins Js=0.30 and 0.40. All three populations
share the same recorded trajectories.

## Physical weights and checks before interpretation

The recorded action families were sampled with AGAMA method 4 from its
isotropic sampling DF Fq, with one common deterministic `Fq.totalMass()` divided
by the number of families. The exact analytic targets are F±=F₀±αδF, each of
true mass one. For folded positive-Lz actions use

\[
r_i=F_0(e_i)/F_q(e_i),\qquad h_i=\alpha\delta F(e_i,L_i,|L_{z,i}|)/F_q(e_i).
\]

The plus response is half the weighted sum of (r+h) times the prograde impulse
and (r−h) times the full-velocity-reversed impulse; the minus response swaps
these weights. Their contrast is Σmᵢhᵢ(Bpro−Bretro). The exact-reference response
uses the common r weight. No population or library is separately renormalized
to sampled unit mass. The finite sample's represented mass Σmᵢrᵢ is recorded,
not used to rescale these absolute physical responses.

Stop before scientific interpretation if energies leave (0,1), the sampling DF
is nonpositive/nonfinite, its binary does not match the archived one, recorded
masses differ from the stated common normalization, or the corrected analytic
multiplier exceeds 0.5 beyond 10⁻¹⁰ arithmetic slack. A sampled reference-DF
ratio departing from unity by more than 0.001 triggers a review. Record these
checks and all sampler-returned mass estimates; do not confuse the latter with
the fixed physical normalization actually used.

## Uncertainty and numerical qualification

The eight whole action/phase libraries are the uncertainty units. Preserve
each library's three population contrasts at both histories, and their full
six-by-six covariance. Report nominal pointwise Student-t intervals with seven
degrees of freedom and supplementary Bonferroni intervals for the six selected
population/history contrasts. The nominal coverage of eight-library intervals
is uncalibrated, and the supplementary family does not cover the entire earlier
adaptive campaign. Phase nodes and population contractions are not independent
replications.

Freeze a material-error screen: every available selected paired phase or
timestep change for a history must be smaller than 10% of that history's
eight-library mean contrast in absolute value. The denominator is the measured
contrast, not initial mass or action RMS. Retain signed shifts, absolute weighted
family differences, ratios and unresolved/missing checks. The parent matrix
has doubled reference-phase rules for two libraries and half timesteps for
one library at each history; it has no doubled-phase frequency history.
Passing these limited checks is not a complete discretization bound or live
qualification. A missing comparison remains untested.

If the parent experiment is still running, read only complete coarse files and
write a clearly preliminary immutable result. After its COMPLETE marker appears,
write a **new** final readback including refinements and the terminal parent
record; never update the preliminary result in place. Do not edit any running
source, array or configuration.

## Budget and advancement

This task performs array contractions and DF evaluations, with no particle
sampling, orbit integration or live evolution. Use one thread, nice=10 and at
most 120 CPU seconds. Snapshot this protocol and executed source, and hash the
frozen family, parent configuration, every response/library array read, relevant
source and binary versions. Complete-array public reproduction is not yet
available.

The original factor-of-two galaxy ambition is assessed separately from whether
a smaller tracer contrast resolves. Any fresh forcing history or live simulation
requires a later scientific and cost review; this readback cannot authorize it.
