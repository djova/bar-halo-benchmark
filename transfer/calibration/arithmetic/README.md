# Recompute the arithmetic comparison and figure

With the pinned transfer environment installed, run from the repository root:

```sh
python transfer/calibration/arithmetic/analyze.py --root transfer/calibration/arithmetic --out reproduced-arithmetic-figure
```

This reads the two supplied unforced evaluations, verifies their identical action
inputs and exact hexadecimal DF values, and regenerates the measured figure and
summary. It needs no simulation dependency or private data. The figure is a
comparison of two dependency builds, not an exact DF accuracy test.

`evaluate.py --agama PATH_TO_BUILD --reference transfer/calibration/reference.json
--out NEW_DIRECTORY` evaluates a new build on the same original action grid.
It requires the separately built dependency and pinned mpmath1.3.0 from the
transfer requirements. The recorded original/rebuilt library hashes identify the
archived pair; do not label a different build as either member of that pair.
The high-precision operation is the logarithm of the returned binary64 DF values.
It does not increase the accuracy of the dependency's DF construction.
