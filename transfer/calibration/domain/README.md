# Read the domain of the frozen model

The original unforced calibration and exact initial population quantify the
model assumptions without any forced trajectory. Case B’s orbital coefficients
vary modestly along the sweep, while the selected Gaussian’s initial logarithmic
density slope grows 17.45 times steeper. Both reduced and Cartesian experiments
already contain that same Gaussian; this limits whole-halo extrapolation, rather
than identifying a missing term in their matched comparison.

From the repository root, with the pinned NumPy/Matplotlib environment:

```sh
python transfer/calibration/domain/analyze.py --coefficients transfer/calibration/reference.json --forecast transfer/forecast.json --out reproduced-domain
```

The command runs offline in about one CPU second and regenerates all three
figures, their PDFs and both case records. It verifies that the unforced input
checksum matches the original frozen forecast. No AGAMA build, private file or
simulation array is required. The output directory must be new.

[Method and limits](PROTOCOL.md) · [Measured interpretation](OUTCOME.md) ·
[Full-precision readback](result.json).

The 17.45 factor concerns the **initial** distributions sampled along the prescribed
resonance path, not evolved noisy or bar-forced densities. Coefficient ranges and
the 15 retained central harmonics are not torque-error bounds. Original failed
calibration/numerical qualifications and the frozen physical band are unchanged.
