# Prospective population forecasts: outcome 01

The recorded response kernel predicts the independently evolved new populations under the original operational criterion. All three shapes, both sweeps, both durations and both windows meet that criterion and their numerical/window comparisons. This is reuse of the same prescribed local operator with new initial populations. It is not a new Cartesian prediction or a statement about a complete halo.

The predictions were committed at `4b633b6` before the independent matrix at `dba35d6` began. None of the shapes or coefficients was fit to these outcomes. The 23 numerical calculations include refinements and controls; they are not 23 independent confirmations of a physical theory. The 24 comparisons share kernel batches and are correlated. Their 95% sampling intervals are pointwise, not simultaneous.

## Frozen forecasts and independent measurements

The table uses the original window (plateau 24, cutoff 40). Both windows are retained in the complete JSON. Units are integral(w K_B), with the original absolute central density and no per-window mass normalization.

| Sweep s | T | Population | Frozen forecast | Independent evolution |
|---:|---:|---|---:|---:|
| 0 | 10 | gaussian12 | +0.013138926 | +0.013147730 |
| 0 | 10 | gaussian20 | +0.013331777 | +0.013333559 |
| 0 | 10 | quartic20 | +0.013435089 | +0.013436017 |
| 0 | 20 | gaussian12 | +0.022156957 | +0.022093955 |
| 0 | 20 | gaussian20 | +0.022557093 | +0.022539638 |
| 0 | 20 | quartic20 | +0.022781935 | +0.022784706 |
| 0.25 | 10 | gaussian12 | -0.000627219 | -0.000559961 |
| 0.25 | 10 | gaussian20 | -0.002546331 | -0.002510489 |
| 0.25 | 10 | quartic20 | -0.003481773 | -0.003461369 |
| 0.25 | 20 | gaussian12 | -0.086765069 | -0.086446894 |
| 0.25 | 20 | gaussian20 | -0.052135524 | -0.051964187 |
| 0.25 | 20 | quartic20 | -0.031571809 | -0.031483172 |

## What the accuracy claim permits

The complete independent-minus-predicted 95% interval must fit inside the larger of ±0.0002 and ±5% of the frozen forecast magnitude. Numerical/window comparisons must separately remain below the original 0.0002 scale. These are operational checks, not certified error bounds. Consequently this is **not uniform 5% accuracy**.

The tightest row is the moving Gaussian of width 12 at T10: its independent-minus-predicted interval is [-0.000062449, +0.000196966], just inside ±0.0002. Its collisionless grid change is 0.0000235424. The remaining interval margin is smaller than that numerical change; the plot must not suggest a rigorous combined error certificate. No additional refinement or relaxed threshold was used to move this row across a boundary.

The primary population inference is unchanged: moving-resonance suppression survives actual halo weighting at T20 with a much smaller magnitude, while the original Gaussian and halo have opposite signs at T10. The width-12 comparison now independently confirms that broadening the selected Gaussian can change its early-time sign within this fixed model. The precise transition width is not independently measured, and no universal curvature law follows.

## Reproduce and inspect

`reproduce_heldout.py` in the public benchmark regenerates all forecasts from the released kernel, then runs all 23 numerical cases and compares the full decisions. A forecast-only mode checks arithmetic without claiming new forced evolution. Full public-source reproduction of the original population experiment remains a separate running check at this checkpoint.

The public package retains `population/heldout/reference.json`, `population/heldout/forecast/result.json`, the frozen protocols and every case recipe in `population/heldout/reproduction.json`. The original complete matrix remains in the experiment archive; the public command regenerates it without private files. The inspected figure shows all 24 comparisons, including the near-boundary interval. No condition is omitted.
