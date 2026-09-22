# Preserve the original discrepancy gate as well as the raw-torque check

22 September 2026, while the first final-matrix case is running and before any
case in that matrix completes. The final matrix protocol explicitly requires
the raw3D contrast changes to meet the unchanged numerical margin. The original
FORECAST_PROTOCOL also requires qualification of the primary3D-minus-reduced
discrepancy. Both requirements apply: the added raw-torque check does not replace
or relax the original discrepancy check.

For each halfstep and halfcadence comparison report and gate both
mean(X_fine-X_candidate) and mean((X-Y)_fine-(X-Y)_candidate), using the same
particles and each run's corresponding reduced path. Require both point shifts
and both complete nominal95%intervals inside +/-1.8126730139721574e-7. Numerical
qualification fails if either requirement fails. Report reduced-only shifts too,
but do not use their cancellation to bypass the raw check or vice versa.

This records the inheritance explicitly before inspecting these outcomes.
No source, particle, physical parameter or numerical margin changes.
