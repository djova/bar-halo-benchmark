# Complete public reproduction of the numerical confirmation

22 September 2026. All twenty cases completed normally, with no stopped or
missing case. The public source copy used the existing separate pinned Python
environment and previously independently built AGAMA/GSL dependency. This was
not another dependency build, new phase sample or physical experiment.

The [comparison criteria](INDEPENDENT_CONFIRMATION_REPRODUCTION.md) were fixed
before the run. Every one of the 156 declared scalar comparisons passes the
unchanged absolute tolerance of 1e-9. The largest difference is
5.473281163958631e-13. All scientific settings, source identities, local gates,
particle coverage and the numerical decision agree with the original reference.
**The numerical qualification remains false.** Both cadence intervals still fail;
the conditional physical extension remains unrun and the forecast unresolved.

## Saved arrays: reproducible measurements are not bitwise trajectories

The separate archive comparator checks the actual recorded-array checksums,
shapes, dtypes and finite values before comparing all 300 arrays across the
20 cases. It compares bytes in C order, distinguishing positive and negative
floating-point zero. All 100 required initial-state, ID, time and event arrays
match byte for byte. Canonical noise-action increments and reduced bar impulses
also match byte for byte in every case. In total, 164 of the 300 arrays are
bitwise identical.

| Quantity | Largest absolute difference across all cases |
| --- | ---: |
| Declared ensemble scalar | 5.473281163958631e-13 |
| Initial Cartesian component | 4.773959005888173e-15 |
| Final Cartesian component | 2.4422618049246836e-5 |
| Individual final bar angular-momentum impulse | 1.624182701569568e-8 |
| Recorded path-array component | 3.5636299777763725e-7 |

The Cartesian maximum is a component-wise maximum in the benchmark's model
units, not a dimensionless relative error or a bound on physical-model accuracy.
No bitwise Cartesian equivalence is claimed. The descriptive largest-path ranks
agree in all four comparisons, but these paths remain in the primary estimate;
rank agreement is not an additional physical result.

The [full-precision receipt](https://github.com/djova/bar-halo-benchmark/blob/main/transfer/reference/clean-confirmation-reproduction.json) includes every scalar and every per-case array
comparison. It distinguishes original and reproduced array/library hashes.
The reproducibility check does not add an independent statistical sample, narrow
the original sampling intervals or establish the imposed noise as a halo model.

## Resources, archive and provenance

The scientific workers used 44,247.727585 CPU seconds, or 12.291035440277778
CPU hours, below the fixed 14-hour ceiling. Three workers were used, each at
nice=10 and one force-solver thread. The final case ledger is terminal at
21:30:43 UTC with all twenty cases complete and no stop reason. The separate
full-array comparison used 2.72 reported user-plus-system CPU seconds. Its
standalone adaptation used another 2.75 CPU seconds and returned identical
comparisons; only the comparator source-file hash changes with its import path.

The source copy is public commit `beb10e1d7833fece83d82767c3fd17fb5353e1c0`.
Later packaging/documentation repairs leave all eighteen frozen scientific
inputs unchanged. The forecast remains SHA256
`d455a54900fb1ffb190e906554afc25ee02719e12c4989995d3240c7913e54a4`.
A durable local copy of all 107 output files matches the isolated run byte for
byte; its manifest is retained alongside the original records. The public
[standalone package](https://github.com/djova/bar-halo-benchmark/tree/main/transfer)
generates the inputs and outputs from seeds without that local archive.

Evidence in the project: `isolated-confirmation-analysis-01/result.json`,
`isolated-confirmation-archive-01.json`, the terminal reproduced case ledger,
and `noise-confirmation-comparison-cpu-01.txt`. These verify the bounded
reproduction. The [scientific assessment](https://djova.ca/galaxy-bar/noise-methods#limits) explains
what the original measurements do and do not establish.
