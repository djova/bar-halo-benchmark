# Saved operands for checks-v2

These two small archives support arithmetic replay of saved stellar responses,
not regeneration of trajectories. `operand-manifest.json` records bytes and
SHA-256 for the archives and `data/checks-v2.json`. Use `numpy.load` with
`allow_pickle=False`. Every numeric array is float64; `inner_mask` is Boolean.
No missing path is removed. There are 4096 original sampled states, ordered
identically across both archives. The experiment's seed is recorded in the JSON.

## warm-fine-dilution.npz

| Field | Axes | Meaning |
|---|---|---|
| Rc | state | Guiding radius, in Hernquist length units |
| inner_mask | state | Exactly Rc < 0.25; not a current-position selection |
| positive | carrier × state | Original fine positive energy estimator, including forward remainder and inverse capture; carriers are numerical zero, 5, 8 |
| paired | carrier × state | The carrier 5 or 8 value minus that state's numerical-zero value |

Energy is in G=M_h=a_h=1 units. Values already include physical-target to
proposal weighting. The whole-population mean is per stellar mass one.
For the heating-fraction figure the inner numerator is the mean of `paired`
times `inner_mask`; it is **not** divided by inner mass. Its ratio to the
whole mean has the same-sample delta-method SE described in CHECKS_V2.md.

## warm-coarse-comparison.npz

`Rc`, `guide_weight`, and `radial_q` have state axis. Guide weight is the
physical/proposal guiding-radius ratio; radial_q is the strictly positive
radial-action proposal density. The target-density underflows remain present.

For each of prefixes `old_` and `new_`, `forward_remainder`, `inverse_capture`,
and `positive` have carrier × state axes, ordered numerical zero, 5, 8.
They satisfy `positive = guide_weight * (forward_remainder + inverse_capture)
/ radial_q`. Recorded inverse-capture zeros do not remove the inverse term
from the operator. All arrays preserve the underlying numerical operands.

Old means refer to the completed original coarse map; new means refer to the
completed coarse map of a resource-stopped extension. Per-path differences
are formed before averaging, preserving pairing and cancellation.
The additional conditional-cohort readouts use Rc < 0.25, 0.5, 1, 2 and exact
target mass `1-(1+Rc_upper)*exp(-Rc_upper)`, not a measured sample mass.

In JSON, `Rc_upper: null` means the full population. It is not missing data.
The incomplete fine maps and inverse compositions are explicitly missing;
the extension is COST_PARTIAL and scientific qualification is false.
No finite halo/star cost or stellar-survival bound follows from this replay.

## Other checks

Spatial fields, all four sign-case operands, six grid memberships, signed
cross differences and component scales are stored directly in `checks-v2.json`.
The sealed forecast includes all seven grid contractions and numerical proxies.
The reader reconstructs those relationships without running an orbit.
Running the separate NumPy unforced-forecast operator is optional and explicit.

New code, derived values and documentation use the repository MIT license.
