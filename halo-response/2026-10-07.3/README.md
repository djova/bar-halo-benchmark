# Hidden halo response: joint-resolution executable release

Release **2026-10-07.3** adds a portable F0/A collective calculation and its
complete recorded reference at the tested joint resolution. This package is
installed only after the complete public run and its exact private counterpart
close unchanged and their comparison passes. The actual comparison values are
in [the equivalence summary](collective/equivalence-summary.json); the scope and
provenance are in [release validation](RELEASE_VALIDATION.md).

The physical question is whether positive stationary halos with identical
initial velocity-reversal-even distributions and zero mean velocity at every
position can have opposite total work under a cyclic rotating quadrupole.
The tested model includes each population's own induced gravitational field at
linear order. It does not establish sustained power, global stability, nonlinear
autonomous acceleration, live stellar-bar evolution or observational validation.

Start with [the current collective instructions](collective/README.md).
The five files in `collective/calculation-source/` are the **byte-exact source
consumed by the recorded run**. Its README and METHOD describe preparation at
that historical point; they are preserved for source provenance. Their earlier
untested-status statements and larger proposed CPU cap are superseded by the
current instructions outside that folder. Altering either historical document
would change the solver's five-file provenance check.

The [equal-time density-null diagnostic](diagnostics/ward-density-kick.json)
retains both fresh grids and both populations, including every raw matrix and
nonzero residual. It passed its original finite-grid physical-seed screens.
The [method and exact contraction-source excerpt](methods/WARD_DENSITY_KICK.md)
explain the velocity-integral identity and preserve the consumed historical
protocol. This check has no time evolution: it neither establishes causal
response or global stability nor repairs the isolated dipole failure or bounds
the forced-cycle work error. Its source excerpt is not a standalone runner.
This additive diagnostic does not alter the tested collective calculation.

The small [reference JSON](collective/reference/result.json) retains every
actual recorded public row, including all 241 nominal rows and any extra
checkpoint records, its two populations and full complex coefficient arrays.
It is a documented public projection of the source result, not a byte-identical
copy of the full operational record. Private paths, job metadata, checkpoints,
orbital libraries and generators are excluded. The original scientific scalar
values and coefficient rows are retained without repair, interpolation or
selection by outcome.

The diagnostic JSON is likewise a labelled public projection. Only its private
source-path inventory is excluded; both grids' complete scientific values,
refinement operands, original flags and reported resource values remain.
Source-result and consumed method hashes identify the projection's origin.

This is an executable **same-equation reproduction**, not an independent
physical sample or a proof that refinement proxies cover continuum error.
It requires the existing pinned NumPy/SciPy dependencies; it supplies no installer
and no private scientific archive. Reading the documents and JSON launches
nothing. The current source and evidence remain available in the earlier
[release .2](../2026-10-07.2/README.md) and
[release .1](../2026-10-07.1/README.md), which this additive release leaves
unchanged. All files included here use the unchanged [MIT license](LICENSE).
Public mirror access is a useful fallback, not a claim that every automated
client can retrieve the canonical website.
