# Bounded diagnosis of the strict calibration discrepancy

22 September 2026. The clean calibration retains 100 failed strict scalar checks,
all numerical DF slopes or their scaled values, with maximum difference1.954e-9.
No original coefficient, threshold, forecast or running source is changed.

Evaluate the QuasiSpherical DF in the original and independently rebuilt AGAMA
libraries at IDENTICAL original action points, retaining the binary64 values.
Use all original central and scan rows of both cases, Js offsets h=1e-5,2e-5,
4e-5 and8e-5 (Jphi offsets2h). For each fixed pair compare the original difference
of binary64 logarithms with a50-decimal-digit logarithm difference of the exact
same binary64 DF inputs. This separates evaluation differences in the DF from
roundoff in taking/subtracting its logarithms. Report differences as a function
of h; changing h also introduces truncation error, so a smaller cross-build
difference is not an absolute derivative accuracy proof.

The original and rebuilt action grids have slightly different derived widths.
The shared original grid removes that correspondence change from this diagnosis.
Keep the complete previous reproduction failure; do not replace its inputs or
call a new algebraic expression a retrospective pass. This diagnoses numerical
reproducibility only, with no forced trajectories or new physical coefficient fit.

Two sequential single-core nice10 evaluations, each capped60wallseconds, followed
by a finite table readback. At most one additional scientific worker runs beside
the three independent-confirmation workers. Record input/source/library hashes,
CPU and high-precision package version. No new simulation or host timer.
