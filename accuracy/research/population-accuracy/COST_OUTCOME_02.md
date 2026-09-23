# Measured estimator efficiency and its failure regime

All16corrected matched-weight cases completed, using345job CPU-seconds
(346.82seconds including measured process overhead). Each sweep uses eight
independent batches of90,112initial points, with paired Brownian partners and
fine/coarse numerical paths. Both estimators evaluate exactly the same positive
piecewise-linear population. This corrects and preserves the first timing run.

The cost account measures the shared full-T20 integration once, plus each
method's actual population setup and evaluation. It does not count the same
trajectories as independent experiments. T10 is a saved measurement within that
same measured full-T20 workload. The separately saved per-case timing repeats
allow readers to inspect timing variability.

For the moving s0.25 condition:

| Weight | Cost × variance ratio, T10 | Cost × variance ratio, T20 |
|---|---:|---:|
| Reference halo in this slice |21774|6928|
| Slope-matched exponential |21738|6910|
| Gaussian σ=8 |655.1|122.4|
| Gaussian σ=1 |1.760|1.590|
| Gaussian σ=1/8 |0.951|1.007|
| Gaussian σ=1/64 |0.982|0.993|

The ratio is(raw variance × raw CPU)/(remainder variance × remainder CPU).
Above one favors the cumulative remainder. Values near one show no substantial
advantage; below one favors raw weighting. For moving T20 halo weights the
paired-batch bootstrap interval is about[6735,7229]. For the narrowest weight it
is[0.9910,0.9942]. These intervals quantify the recorded eight-batch conditional
variance/time calculation, not the tails of every possible experiment.

The actual mean accounted batch CPU at moving T20 is18.40seconds for raw halo
weighting and18.56seconds for its remainder. The improvement comes from reduced
variance, not a dramatically faster orbit integrator. Multiplying variance by
measured CPU projects the cost of repeated independent batches at a chosen
precision. We did **not** directly time a6900-fold longer raw calculation at the
same final error. The fixed allocation, independent-batch scaling and recorded
workflow define the projection. The between-batch ratio is also supplied and is
noisier: about2749for that halo example. Do not hide this uncertainty by quoting
only the more stable within-stratum variance estimate.

The gain vanishes when a narrow weight varies sharply across a typical bar
displacement: the nonlinear remainder is no longer small compared with the raw
impulse. This is an interpretation of the measured stress test and the local
Taylor expansion, not a universal formula for efficiency or a physical halo model.

## One pointwise consistency flag is retained

23of24paired95%raw-minus-remainder intervals contain zero. The stationary,
T10,σ1stress comparison has mean0.03622and interval[0.00190,0.07055], about2.50
estimated standard errors from zero. All samples and that flag remain published.
The comparisons are correlated and these are pointwise intervals; this single
flag is not by itself a demonstration of estimator bias. Nor is it erased by
the analytical identity or the other intervals. There was no sample enlargement
or outlier removal to obtain agreement.

The exact-map identity, full auxiliary support, discrete-weight equivalence,
and local path-budget checks support that the two methods target the same
observable. The maximum measured path-budget error and all covariance arrays
are in the runnable release. A future precision target should use independent
variance evidence appropriate to that population, rather than assume the broad-
halo gain applies to a narrow selection.

Evidence: cost-analysis-02/result.json; estimator-cost-02's16recorded cases;
cost-weight-controls-02/result.json. Figures02fixes an initial axis-label scale
presentation issue without changing any numerical value. Neither the timing
repair nor the presentation correction supplies new independent physical samples.
