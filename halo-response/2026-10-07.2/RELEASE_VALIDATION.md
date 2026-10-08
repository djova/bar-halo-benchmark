# Validation and limits of release2026-10-07.2

The portable central collective calculation completed the full prescribed
T120 cycle for all five populations with its own generated orbital library
and induced fields. Its finite formula controls and actual zero-drive,
zero-initial-generator operator control passed. A separately retained
same-configuration comparison with the existing implementation completed and
passed every required shared-recorded-time check. This is agreement between
implementations of the same canonical equations, not an independent algorithm,
fresh physical sample, continuum convergence or global stability test.

The tested command uses the reference grid with an explicit dt=.02 override,
not the preset's dt=.01 default. The cycle has rise/fall12, T120, shape.8,
Omega.12 and physical bar mass.1. The angle is prescribed; no autonomous
rotor is integrated. Numerical versions and the five source/document hashes
are retained in the public reference and comparison summary.

The comparison requires every regular recorded step0..6000 at stride50,
physical work and impulse, canonical Q/J, included/projected field energy,
external interaction, shape work, separate exact discrete flux, raw physical
and discrete residuals, self torque and every full5x5x5 complex coefficient
column. Energy-ledger and coefficient maximum absolute differences use2e-12;
impulse/torque differences use2e-11. All actual shared and unmatched checkpoint
step lists are retained, rather than interpolated or fabricated. Actual
differences appear in the public numeric summary; these implementation
tolerances do not become physical error allowances.

The public reference uses the runner's source-produced schema with a selected
science/configuration/diagnostic whitelist. It preserves all recorded rows and
initial/final physical quantities, but excludes process-limit observations,
timing/memory reports, dense generators, orbit/checkpoint archives, operational
owner IDs, private paths, receipts and producer-input infrastructure. Running
the released code generates a complete local result and bounded checkpoints;
no private campaign output is required to initialize it.

The five collective source files are copied exactly as tested. Their historical
pre-validation wording remains immutable; this companion supersedes only that
status. The older six bare companions, fifteen public result files and data
schema are copied exactly from2026-10-07.1. That release and its checksum list
are unchanged. The new checksum list binds this release's actual files; it
certifies byte identity, not scientific interpretation.

Earlier limitations remain: the finite-amplitude magnitude check failed its
original qualification despite supporting the active sign; separate adaptive
confirmation is not pooled with the principal ensemble. The linear collective
assessment uses finite one-axis empirical allowances rather than rigorous
continuum bounds or a tested finest combined corner. The background positivity
certificate does not certify a perturbed distribution or collective stability.
The full hidden signs have the same unforced spectrum under proper rotation;
their driven handedness does not alter that symmetry statement. No source
comparison establishes autonomous acceleration, a formation history, observed
galaxy applicability or a new dark-matter interaction law.

Installation validates provenance, controlled public fields, privacy exclusions,
fixed file membership and staged/installed checksums. The public repository
commit, tag and push require the owner's separate verified installation receipt;
the installer performs none of those actions and runs no new calculation.
There is no new CI service or remote build obligation in this release.
