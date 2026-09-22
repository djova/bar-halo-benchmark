# Read back the existing bar-free controls

22 September 2026. This is a retrospective evidence review of completed map
controls, specified before calculating this new summary. It introduces no new
simulation, physical sample, fitted operator, numerical ladder or acceptance gate.
The independent 3D confirmation remains failed and its physical extension stopped.

Review all 16 original distribution controls on the declared four sweep rates
and four diffusion strengths, including the reused s=0.4, eta=0.1 pilot. Retain
the four separately recorded eta=1 controls with doubled action domain. Verify
the complete markers, source records and raw-array checksums. Reconstruct the
final expected variance as sigma² + 2 delta T, delta=2 eta/pi, and the expected
physical mean change as zero. Reproduce the original mean/variance gate decisions
at their unchanged 1e-7 absolute targets. Retain original failures alongside
their replacements; a repaired control does not retrospectively pass the original.

Review all 24 unforced stochastic batches: seeds8201–8208 at the three declared
(s,eta) conditions (0,0.1), (0.4,0.1), (1.2,1). Read their recorded initial/final
actions, accumulated bar impulse and accumulated Brownian increment. Reconstruct
the physical budget j(T)+sT−j(0)=B+W. The original path-budget target is1e-9;
with the bar absent, the accumulated B must be zero. No stochastic impulse is
counted as bar torque. Compare recorded summary moments with the raw arrays.

Within EACH condition, the eight seeds are independent. The Brownian endpoint
has known mean0 and variance2 delta T. Report the sample mean and its exact-normal
pointwise95% interval using that known variance, plus sample variance and its
chi-square95% interval. Report every batch and the combined sample at that
condition. These are descriptive checks against a known law, not new binary
qualification gates or a family-wide significance test.

**Do not pool the three conditions as independent observations.** They reuse the
same seed family and related random-stream prefixes. Independence across seeds
within a condition does not imply independence across conditions. There is no
optional sample selection, path trimming or change of thresholds after readback.

This review can establish the coverage and numerical behavior of the imposed
bar-free operator at these recorded settings. It cannot calibrate that operator
to gravitational fluctuations, qualify the forced response, validate the 3D
forecast, or turn a finite-time variance check into a general diffusion diagnosis.
The source implementation records distribution mass/positivity/budget diagnostics
at saved times; those maxima are not rigorous bounds on every unsaved substep.

Keep the result and input hashes in a separate versioned directory. Publish the
complete small table, method and retained failures with the next scientific
update. A figure is useful only if it clarifies the exact-law comparison; do not
add decorative trajectories or another physical claim.
