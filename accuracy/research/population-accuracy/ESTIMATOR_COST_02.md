# Matched numerical weights: correction to cost benchmark01

The first completed16case benchmark is retained in estimator-cost-01 and
cost-analysis-01. Review found a numerical-population mismatch: raw weights were
evaluated from the analytical/tabulated formula directly, whereas the cumulative
estimator used the positive piecewise-linear density at spacing1/8192. The
physical targets coincide in the continuum, but the timed discrete observables
must be identical before interpreting a method comparison. This is particularly
relevant to the deliberately narrow stress profiles.

The corrected raw path evaluates **the same two neighboring density nodes and
linear interpolation** as Population.evaluate. It computes only the nodes each
particle needs, rather than constructing an unnecessary full primitive. The
remainder path is unchanged. A direct control compares every population's weights
and repeated estimator outputs against the common Population implementation.
The original source is retained in cost-version-01 and commita121905.

Repeat all16cases with the same seeds, allocation, dynamics, endpoints, windows,
timing order, and analysis, following ESTIMATOR_COST_01. This is a software/timing
correction, **not new independent physical samples**. Both old and corrected
measurements remain inspectable. Use one nice10 single-thread worker, a further
3000CPU-second cap and240seconds per case, within the existing three-core-hour
analysis/cost allocation and24core-hour campaign total. No diagnostic, prospective
family, physical parameter or held-out acceptance criterion changes.
