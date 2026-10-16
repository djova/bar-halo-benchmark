# Reading and reproducing this follow-up

This release reports a scientific stop of the tested routes. It does not claim
that hidden halo memory is absent. The proposed formation-to-stellar mechanism
has not been established.

## Read and inspect

Read [the report](README.md), its three figures, the small JSON records in
`evidence/`, and the [data dictionary](DATA_DICTIONARY.md). No executable,
credentials or private repository is required. `manifest.json` records the
release, file sizes and SHA256 hashes. The repository tag
`impact-memory-2026-10-16.1` pins this collection.

The evidence records are selected projections of completed research outputs.
Their numerical values are unchanged; operational paths are omitted. The
figures retain the recorded failed qualifications. Reading these records is not
rerunning their simulations.

## Execute the new construction

With Python 3.10 or later, NumPy and SciPy already available, run from `runner/`:

```sh
python -B run.py --inputs inputs/inputs.json --output ../control-output
```

The output directory must be new. The runner sets single-thread numerical
library variables before importing those libraries; it installs nothing and
does not contact a network service. The tested environment used NumPy 1.26.4
and SciPy 1.17.1. Other numerical-library versions may produce different
roundoff or optimizer paths; output includes their versions.

This performs the full four-endpoint construction, not a saved-label check:

- Read all 12,288 particles in each endpoint, including both satellites.
- Reconstruct 203 host-current constraints and independent held-out features.
- Solve the fractional positive velocity-sign construction for each state.
- Generate all 16 fixed independent and balanced realizations per state.
- Preserve complete signs, moments, flight records and qualifications.

Only host velocity signs are changed; satellite states remain identical.
The code evaluates diagnostic functions but does not integrate forces or orbits.
It does not create a physically attained halo, a stationary equilibrium, a live
stellar disk, or a finite-time response bound.

The original complete constructor used 86.830720 measured local CPU seconds.
The portable reconstruction and input projection used 81.946894 CPU seconds
on the recorded host. Its first comparison then failed because NumPy does not
support Boolean subtraction. A separate saved-output comparison used 0.442642
CPU seconds; it did not rerun the construction. Both attempts remain accounted.
These are measured single-host costs, not universal runtime predictions.

All 1,088 numerical arrays matched the original exactly, including the complete
sign assignments. [EQUIVALENCE.json](runner/EQUIVALENCE.json) records each check.
Its prospective floating tolerance was relative 1e-10 and absolute 1e-12;
integer signs and identities required exact equality. Those are software
equivalence tolerances, not physical accuracy criteria. Exact agreement is not
promised across arbitrary library versions or hardware.

## What is shared and what remains unavailable

The portable scientific functions are copied verbatim from frozen source by
an allowlisted AST extraction. `runner/EXTRACTION.json` records source,
definition and generated-module hashes. The public file reader and output glue
are separately written. This is shared-code reproduction, not independent
physical confirmation.

The four input archives retain every original particle value, dtype, physical
mass and identifier. Their projection was compared exactly against the complete
archived endpoints. The release intentionally does not include the large force,
orbit and kernel histories from which the other figures were made. Thus it
does **not** publicly reproduce the assembly trajectories or the collective
response comparison. Their selected evidence and figure readouts are inspection
material; the original archives and failures remain preserved separately.

No simulation of stellar-bar growth, saturation, heating, or an observational
sample was completed in this phase. Reproducing this constructor cannot establish
any of those claims.

Project-authored code, text and generated data in this collection use the
repository's MIT license. Linked literature retains its own rights. Report
specific questions through the [public issue route](https://github.com/djova/bar-halo-benchmark/issues);
this release has not undergone external peer review.
