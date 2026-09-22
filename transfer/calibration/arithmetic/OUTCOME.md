# Calibration discrepancy: returned DF values, not logarithm subtraction

The shared-grid test evaluates136original calibration rows at four fixed finite-
difference offsets in each of the two dependency builds. Both evaluations use
exactly the same original action arrays. At the original offset h=1e-5, the
original build reproduces every archived derivative exactly. The rebuilt-versus-
original derivative difference still reaches1.95399252334e-9. Thus the small
change in the regenerated action grid is not needed to reproduce this discrepancy.

Taking50-decimal-digit logarithms of the same binary64 DF outputs does not remove
it: the maximum difference becomes1.95677962722e-9. The differential logarithm-
arithmetic contribution is only1.20896776352e-11. The difference between the DF
values themselves reaches4.6561e-11 relative, and none of the136paired values is
bitwise identical across builds. Increasing h eightfold leaves a maximum slope
difference1.8818e-9 while reducing the log-arithmetic contribution to1.58e-12.

This localizes the dominant discrepancy upstream of taking/subtracting the
logarithms, in the DF values returned by the rebuilt dependency. It does not
identify the responsible integration, interpolation or other internal operation.
High precision here applies to logs of fixed binary64 values, not to the DF
construction. Larger h also changes derivative truncation error. Neither build
is established as the exact physical DF by this comparison.

The two evaluations took0.0551scientificCPU seconds. All1088row/offset evaluations
and exact hexadecimal DF values are retained. The plot uses scan rows in its left
panel and all136rows per offset in its right panel. Ordinary and high-precision
curves nearly overlap; the separate log-arithmetic contribution is shown on a
logarithmic scale. Lines connect measured action points and offsets.

The original100of1304strict failed checks remain failed. No reference, tolerance,
calibration, frozen forecast or running orbit changes. This is a diagnosis of
numerical reproducibility, not new bar–halo physics. The unforced preparation
already reproduced all frozen orbital inputs within their declared tolerances.
