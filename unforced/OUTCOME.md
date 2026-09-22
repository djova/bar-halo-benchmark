# Bar-free controls: known-law agreement and retained boundary failures

Retrospective review, 22 September 2026. All 16 original distribution controls,
four separately recorded domain replacements and 24 stochastic batches have
complete records and matching raw-array checksums. No simulation was rerun.
The source is the exact archived solver from commit847a4325, SHA256
`bc1359a145b4ecaeb8dcf026a7c62bfdbbbb28ccbff4b3de6c8524117b6d6db5`.
It hardcodes population width8; slope is explicitly recorded in each case.
The first readback attempt stopped on the missing width field. The successful
review establishes that width from the archived code, not a current default.

## What should happen without the bar?

With delta=2 eta/pi, the physical action change is W, a Brownian increment with
mean0 and variance2 delta T. The comoving coordinate also changes by −sT;
adding sT back separates coordinate motion from physical transfer. The initial
Gaussian's full variance becomes64+2 delta T. None of this impulse is bar torque.

Each row below combines eight independent seeds at ONE condition, totaling
262144 paths. Different rows reuse the seed family and are not independent.
Intervals are pointwise95%, conditional on the imposed Brownian law; they are
descriptive checks, not newly introduced qualification gates.

| s | eta | T | Mean W | 95% mean interval | Var(W) / expected variance |
|---|---|---|---|---|---|
| 0 | 0.1 | 25.13274 | +0.00058295 | [−0.00626489, +0.00743078] | 1.002357 |
| 0.4 | 0.1 | 20 | +0.00092893 | [−0.00517976, +0.00703762] | 1.000592 |
| 1.2 | 1 | 6.66667 | +0.00599268 | [−0.00516021, +0.01714557] | 0.996796 |

All three mean intervals contain zero. The chi-square intervals for variance
contain their known expectations. This is agreement at the reported precision,
not proof that every possible implementation error is absent. Every recorded bar
impulse is zero. The largest final individual budget residual is1.799e-13,
within the original1e-9 path target. All original trajectory budget gates remain
passed; no new gate or clipping was used.

## A closed budget does not establish an adequate computational domain

The original eta=1 distribution controls at s=0.1,0.4,1.2 fail their unchanged
1e-7 variance target. Their signed variance errors are1.7906e-7,6.0555e-6 and
1.0928e-7. The s=0.4 case also fails the mean target. Mass, positivity and the
recorded moment budgets pass in all three cases. Thus a correct budget that
includes boundary transport can coexist with an inadequate approximation to
the intended unbounded Gaussian problem.

The four pre-existing controls that move the periodic boundary from |j|=64 to128,
at unchanged action spacing, all pass their original gates. The largest absolute
variance error there is9.5504e-10. The original s=0 control already passed and is
retained alongside its domain comparison. These are the previously declared
repairs, not a new ladder or a retrospective pass for the original failures.

## Scope and reproduction

This verifies the coverage and recorded behavior of the bar-free operator.
It does not qualify the forced response, the new3D forecast, measured gravitational
fluctuations, physical SIDM or a live collective halo. Distribution moments come
from the original full-grid summaries; the saved decimated density is not used
as if it contained the complete grid. Stochastic moments and final budgets were
recomputed from every individual recorded action and Brownian endpoint.

Canonical readback: `unforced-review-01/result.json`. Canonical figures:
`unforced-figures-02`. Version01 uses the same data; version02 adds standalone
interval/sampling captions, clearer ticks and shading behind the points.
The full table retains all44controls, all prior decisions and every input hash.
The source and exact analytic equations are supplied with the public benchmark.
Recreating a figure from the reference table is arithmetic reproduction;
regenerating the trajectories from seeds is a separate task. Neither adds a new
independent physical sample.
