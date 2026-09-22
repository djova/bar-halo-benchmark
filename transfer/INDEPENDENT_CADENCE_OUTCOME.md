# Independent numerical confirmation: qualification remains unresolved

22 September 2026. The fixed 20-case matrix ended normally at 16:47:28 UTC,
using 12.939978 CPU hours. All 13 frozen inputs are unchanged. Analysis ran
only after the complete matrix terminated. Every local and unforced gate passes,
as do the recorded identities and the timestep comparisons. Both noise-cadence
intervals fail the unchanged numerical allowance. The original failed prefix is
retained separately; no samples are pooled, trimmed, replaced or enlarged.

The allowance is **1.8126730139721574e-7** in the benchmark's normalized Lz units.
For each intervention, both the absolute mean and the entire nominal pointwise
95% iid Student-t interval must fit inside plus or minus this value.

| New-sample comparison | N | Mean change | 95% sampling interval | Interval fits? |
| --- | ---: | ---: | --- | --- |
| Half integration step: raw 3D contrast | 16384 | +5.8730793108e-10 | [-1.6654604413e-10, +1.3411619063e-9] | Yes |
| Half integration step: 3D minus paired reduced contrast | 16384 | +5.8730793108e-10 | [-1.6654604413e-10, +1.3411619063e-9] | Yes |
| Half noise cadence: raw 3D contrast | 131072 | +6.5804908301e-8 | [-9.6270954849e-8, +2.2788077145e-7] | No |
| Half noise cadence: 3D minus paired reduced contrast | 131072 | +1.2819100074e-8 | [-1.7692911231e-7, +2.0256731246e-7] | No |

All four means fit the allowance. The two cadence intervals reach 1.25715 and
1.11751 times its magnitude. They both include zero: this result does **not**
establish a nonzero cadence bias or prove nonconvergence. It fails to establish
the required numerical precision within this fixed experiment. Neither a new
physical failure nor an invalid diffusion law follows from this numerical screen.

The largest 20 cadence differences account for 95.1539% of the raw-contrast
variance and 88.6760% of the discrepancy variance. The largest individual changes
are 0.00418427 and 0.00415985 respectively. Every path remains in the estimate.
These descriptive concentrations do not establish chaos, divergent variance or
a particular statistical distribution. The stated Student-t intervals are nominal
sampling intervals, not rigorous discretization bounds or a simultaneous guarantee.

Although the cadence sample is eight times larger, its interval half-widths are
0.88050 and 0.66511 times those in the original prefix, rather than about 0.354
as an unchanged-variance extrapolation would suggest. The measured per-path
sample variances are 6.20309 and 3.53940 times larger. This describes two finite
samples with rare large differences; it is not a fitted sample-size law or a
reason to exclude those paths. The original power estimate explicitly assumed
repetition of the earlier variance and did not guarantee qualification.

The shared Brownian endpoint difference is 8.76035e-17. Half-step paired reduced
contrasts and Brownian endpoints agree exactly with their candidate counterparts. The
actual cadence intervention also changes the microstep slightly through integer
block subdivision; the independent half-step check and that previously declared
qualification remain part of the interpretation.

## Physical decision and stopping rule

The conditional 524288-ID physical assembly will **not** be launched. The explicit
amendment allowed this one independent numerical sample and prohibited repeating
or enlarging it after its outcome. Its failed qualification cannot be replaced by
a point-only criterion, a looser margin, a different sample or a selected path set.

The recorded candidate raw contrast is -1.2163270304e-5 with a conditional sampling
interval [-2.0655634741e-5, -3.6709058679e-6]. The paired 3D-minus-reduced discrepancy
is -3.6943475230e-7 with interval [-2.7225185379e-6, +1.9836490333e-6]. These are
available setup-specific measurements, not a qualified full-population forecast
test. Even before adding a numerical envelope, the discrepancy interval crosses
the frozen +/-1.8126730139721574e-6 physical adequacy boundaries. The forecast
therefore remains neither validated to its declared target nor falsified.

The reduced-model stationary and moving contrasts remain independently verified
at their stated conditions. The failed wider-map quadratures, unused case A,
unqualified cloud-to-white-noise calibration and all earlier limitations remain.
This campaign has not established a transferable bar–halo response law, physical
SIDM effect, live-halo prediction or observational agreement.

## Inspect and reproduce

Canonical analysis: `results/noise-sweep/independent-cadence-analysis-01/result.json`.
Canonical figures: `results/noise-sweep/independent-cadence-figures-02/`.
Figure version 01 uses the same numerical records; version 02 aligns the two
comparison panels to the same horizontal scale after visual review. This is a
display change only. The original protocol, raw checksums, per-chunk measurements,
all means and intervals remain available in the result and source records.

The standalone package can regenerate these same 20 cases from seeds. Re-running
the same sample in a separate environment checks reproducibility; it is not a new
independent statistical sample, does not change this stopping decision, and must
not be pooled with the original calculation as additional physical evidence.
