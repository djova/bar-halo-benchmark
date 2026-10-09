# Release 2026-10-07.3: validation and limits

The guarded packager writes this additive release only after the two exact
joint producers and their exact comparison close successfully with unchanged
inputs. The recorded public source selects F0/A_full_plus at ne=neta=128,
N=64, nCB=6, dt=0.01, T=120, rise/fall=12, Omega=0.12, shape=0.8 and
bar mass 0.1. Its executed caps are 16600/21000 CPU/wall seconds,
4096 MiB memory and 64 MiB output. A successful resource receipt is not
additional physical evidence.

The five consumed files are preserved byte for byte under
`collective/calculation-source/`; all five original hashes remain in the
reference and `CHECKSUMS.sha256`. In particular, historical README/METHOD
preparation statements are not silently rewritten. Current instructions live
in `collective/README.md`. The unchanged existing public MIT license is copied
as `LICENSE`. Releases .1 and .2 are checked but never overwritten.

[reference/result.json](collective/reference/result.json) is an explicit
public projection of the closed public solver result. It retains every actual
recorded scientific row, initial/final state, exact scientific settings,
source hashes, units, full represented DF maps, and supplied measured resource
operands. It excludes runtime paths, environment, original owner identifiers,
error messages, checkpoints, phase-space libraries and generator arrays. Its
source-result hash and projection rule are recorded in the payload; the private
installation receipt also binds the source and generated public hashes.

[equivalence-summary.json](collective/equivalence-summary.json) reports the
actual common-step maxima, original tolerances, steps/times at maxima, final
work/impulse operands and unmatched-step lists. The complete nominal 241-row
history is included in the reference. No beneficial rows are selected and no
unmatched rows are interpolated. The exact compared differences must pass
2e-12 energy/coefficient and 2e-11 impulse tolerances before installation.
The source-free m=0/±1 declaration and F0 l2 benchmark are preserved.

[ward-density-kick.json](diagnostics/ward-density-kick.json) is a separate
checksum-bound completed equal-time known-null diagnostic at GL32/Fourier32
and GL64/Fourier64, retaining CB0–6 and both F0/A populations. Both original
physical-seed and refinement screens passed; the raw nonzero matrices, density
coefficients, field energy and source-torque residuals remain in the record.
Its explicit public projection excludes only the private source-path inventory
and preserves all scientific fields plus actual caller/outer resource values.
Those overlapping CPU measurements are not additive. The private packaging
receipt binds the complete source-result and released projection hashes.

[The method document](methods/WARD_DENSITY_KICK.md) labels the consumed protocol
as historical and includes the exact contraction function extracted from its
checksum-bound caller without importing or executing it. The excerpt needs
the original helper context and is not a newly tested portable runner. An
equal-time density null tests the projection, not a causal evolution or global
stability, and does not repair a failed dipole benchmark or establish an error
bound for forced-cycle work. No independent collective physics is added by
either this diagnostic or its publication.

This validates a **same-equation numerical implementation comparison** and
makes it independently runnable. It establishes neither independent physical
samples nor rigorous numerical-error coverage, global stability, finite-
amplitude collective dynamics, sustained energy extraction, autonomous
acceleration, formation feasibility or an observed-galaxy interpretation.
The original numerical failures and scientific qualifications stay in their
own records. Public source is an evidence-access route; client-dependent
canonical-site access remains unresolved.

The packager performs no simulations, dependency installation, build, Git
mutation, remote execution or deployment. Local installation is distinct from
the owner's later commit/tag/push and scoped publication. Its operational
receipts remain private. Checksums document exact released bytes and support
inspection; they do not prove the physical interpretation.
