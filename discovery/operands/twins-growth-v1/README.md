# Saved growing-bar response operands

Eight compact NPZ files retain all 25 recorded family impulse/work values, saved
actions, absolute masses, and frozen population weights. Library 0 also contains
the three completed numerical refinements. The manifest defines each axis,
unit, pairing rule, seed, file size, and checksum. The complete original-array
hashes identify omitted original archives; they are not the subset file hashes.

For ratio r=F0/Fq and signed h=deltaF/Fq, plus assigns partner masses
m(r+h)/2 and m(r-h)/2. Minus swaps them; the reference uses mr. Thus the
contrast is sum m h (Ipro-Iretro). All supplied weights are frozen operands,
not rebuilt by an AGAMA call or normalized to a selected tracer mass.

Run from the public benchmark repository root:

```sh
python discovery/scripts/discovery/replay_twins_growth_v1.py --out growth-arithmetic-check
```

Only NumPy and SciPy are needed. Reading files never launches an experiment.
The script recomputes all recorded population contractions, eight-library
intervals/covariances, and selected refinement decisions from these operands.
It compares them with the supplied numerical targets. This is saved-arithmetic
verification, not resampling, orbital integration, a new physical validation,
or a proof of numerical-error or confidence-interval coverage.

The new complete record contains eight retained original coarse cases plus
three newly completed refinements. The interrupted original command stays
interrupted. Its partial CPU reading is not a complete runtime; its reserved
9000-second upper cap is not CPU actually spent. No live halo, evolving bar,
SIDM operator, or observed-galaxy comparison is included.
