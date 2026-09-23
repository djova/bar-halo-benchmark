# Population-approximation accuracy and estimator cost

This package extends the local population-response benchmark. Its first released
component reproduces the matched numerical-weight estimator comparison, including
the narrow populations for which the variance-reduction advantage disappears.
The new sweep-rate accuracy experiment is separately frozen and its independent
population outcomes are pending. A cost reproduction is not a validation of that
prospective experiment.

From the repository root, create an isolated Python3.11 environment and install
`accuracy/requirements.lock.txt`. Then run:

```sh
python reproduce_accuracy_cost.py --out /tmp/accuracy-cost-reproduction --workers 1
```

This regenerates all 16 finite stochastic cases, their paired means/covariances,
the cost analysis and its figure. A second population-comparison figure uses the
released historical reference; it does not rerun the earlier population campaign.
On the original host the cost experiment used about 347 CPU
seconds plus plotting and analysis. The same hardware, seeds and pinned numeric
dependencies reproduce numerical statistics; actual CPU timings should vary and
are deliberately measured again. The command checks statistical arrays against
the released reference and emits a receipt that explicitly excludes timing from
bitwise/numeric reproduction claims. A changed cost ratio caused by a new CPU is
not a new physical sample or a failure of identical-seed numerical reproduction.

The positive halo, exponential and narrow Gaussian weights keep the same central
density and slope. Neither method normalizes each selected population to unit
mass. Raw and remainder use the same piecewise-linear weight, shared Brownian
paths, full auxiliary support and numerical-control integration. Both endpoints
share a full-T20 workload. All strata and all eight batches per sweep are retained.

The ratio(cost × variance)raw/(cost × variance)remainder estimates repeated-batch
precision efficiency under the fixed allocation. It is not a directly timed
speedup at the final target precision. The eight-batch uncertainty, the noisier
between-batch estimate and the one pointwise raw/remainder consistency flag are
part of the release. The narrow stress populations are not representative halo
DFs. See the [outcome](research/population-accuracy/COST_OUTCOME_02.md) and
[restricted identity](research/population-response/CUMULATIVE_IDENTITY.md).

The original timing run is preserved in the project provenance; the released
recipe reproduces its corrected, matched-weight successor. Numerical sources
are copied unchanged; the finite queue launcher only substitutes the active
Python interpreter for a private virtual-environment location. No private files,
host service, API, live halo, AGAMA installation or supercomputer is required.
