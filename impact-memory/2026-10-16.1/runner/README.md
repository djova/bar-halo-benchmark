# Portable archived-state sign construction

This reproduces the full four-state, 203-current-row entropy construction and
independent versus balanced rounding on all sixteen fixed seeds. It is a
same-code port of the recorded construction, not independent physics validation.
No simulations, forces, equilibrium construction or scientific pass are included.

Use Python 3.10 or later with NumPy and SciPy already installed. The original run
used NumPy 1.26.4 and SciPy 1.17.1. The standalone runner sets single-thread BLAS
environment variables before numerical imports and reports the versions used.
There is no dependency installer or host-specific runtime machinery.

Run the full calculation (there is no fixture-only or favorable-subset mode):

    python -B run.py --inputs inputs/inputs.json --output ../control-output

The output directory must not exist, its parent must exist, and it must lie
outside the read-only input directory. Inputs are never modified. Numerical
failures retain an incomplete report; there is no automatic retry or repair.

The input manifest uses schema `assembly-control-public-inputs-v1` with exactly
`schema`, `physical_parameters`, `scientific_source_sha256` and `states`.
The exact public physical parameters and source hashes are constants in run.py.
States are ordered nominal synchronous, nominal lagged, halfstep synchronous,
halfstep lagged. Each record has `label`, `arm`, `dt`, `time`, `file`, `sha256`,
`bytes` and `arrays`. `file` is a unique local NPZ basename. `arrays` maps exactly
`xv`, `mass`, `cohort`, `particle_id` to `{shape, dtype}` metadata. Each NPZ has
only those four arrays, preserving all 12288 particles, original values/dtypes
and IDs. The host comprises the first 8192 IDs; each satellite has 2048 IDs.
The exporter must authenticate their origin separately: this runner checks the
public manifest and content hashes, not the original trajectory implementation.

Outputs retain every h, sign assignment, original/fractional/rounded moment,
held-out diagnostic, terminal landing record and per-state summary. Scalar
residual normalization is the original sum of absolute particle contributions.
No subsequent torque or work error is inferred from that normalization. The
small analytic and QR fixtures run as prerequisites to the full calculation.

EXTRACTION.json records original source hashes, exact selected-definition hashes
and portable-module hashes. Only allowlisted scientific definitions are copied;
the public I/O runner has been newly written. Port equivalence must compare the
full numerical outputs against the original run, excluding execution timings
and intentionally different file/provenance metadata. Such equivalence is still
a shared-implementation check, not independent confirmation of the science.
