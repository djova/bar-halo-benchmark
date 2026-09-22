# Reproduce the calibration without a forced outcome

22 September 2026. Package the original, unchanged unforced coefficient scripts
and full tables whose checksum was frozen before the first 3D outcome. A short
standalone command must regenerate both action neighborhoods, all original angle
quadratures, action scans and reported Fourier harmonics. It also derives every
orbital input in the frozen forecast from these regenerated quantities.

Use a fresh copied source directory and the already independently built patched
AGAMA/GSL and pinned Python environment. This is not a third dependency rebuild.
No forced trajectories are inputs. Compare all scalar quantities with relative
tolerance 1e-10 and absolute floor 1e-13; compare phases modulo 2π with tolerance
1e-12. These are reproduction criteria, not the physical prediction band.
Require the original local gates and preserve case A's failed response prerequisite.

One nice=10, single-core worker, 300-second wall limit; original CPU cost was
2.04 seconds. Charge actual CPU to the existing controls/package allocation.
This regenerates previously declared inputs; it adds no physical sample or
parameter intervention. Do not change original scripts, coefficients, forecast,
running cases or thresholds if the reproduction fails.

The first clean output reproduces the same harmonic set, but two equal-amplitude
case A terms exchange ranks 13 and 14 after the dependency rebuild. The first
positional comparison therefore fails on their wavevector identities. Preserve
that output and failure. Compare harmonics by their unique integer wavevector,
requiring exactly the same set, then apply every unchanged numerical tolerance.
This changes correspondence, not the coefficients or allowed error. Record which
list reordered. Reuse the completed unforced output; no new physics run is needed.

The complete readback retains a strict comparison failure: 100 of 1,304 numeric
comparisons miss the fixed tolerance. Every failure is a finite-difference
distribution-function slope or its scaled version; the largest absolute slope
difference is 1.954e-9, and the largest tolerance ratio is 2.322. Frequency
gradients, Fourier coefficients, their wavevectors and derived frozen orbital
inputs all pass. Both cases' complete orbital-input mappings pass; case A's
separate failed response prerequisite remains failed. This is not a claim that
all calibration scalars reproduce within the declared tolerance.

Report the full comparison instead of stopping at its first numeric failure.
The helper exits nonzero and writes COMPARISON_FAILED for this rebuilt dependency;
it writes COMPLETE only when all declared comparisons pass. The output remains
useful for inspecting the calibration. No threshold, reference table or frozen
forecast changes. Differences in the numerically differentiated DF are localized,
but their precise arithmetic origin has not been independently established.
The clean run uses 2.3414 scientific CPU seconds, charged to controls/package.
