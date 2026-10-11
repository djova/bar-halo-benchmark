# Fresh strength calculations from fixed cached cycle inputs

This additive executable computes new own-field responses of the frozen family
\(F_\lambda=F_0+\lambda(F_A-F_0)\). It uses the unchanged scientific modules in
the twelve-file independent-cycle capsule. It leaves that capsule intact and
requires actual cached inputs; it does not replay endpoint tables or interpolate
own-field histories. **This extension has not been executed or cost measured.**
Its source preparation supplies no new scientific result.

Python 3.11 or newer on a POSIX platform with `resource.RLIMIT_AS` is required.
The recorded numerical environment is NumPy 1.26.4 and SciPy 1.17.1. No package
installation is performed. The unchanged capsule checksum is
`61c963c8d0c6b929701c5f5b18491741713b15fb69380583b0ab4a247fef2a00`;
all capsule files and the actual imported scientific module paths are checked.
The copied calculation/header helpers match the frozen calculation source
`70932b2368900e59a259434a41a3c1aa94fb3e1287a056ebd6dfd07af798ec73`.
No private host path, owner receipt, process identifier or ledger is an input.

## What is fresh

The fixed cycle has duration120, rise/fall12, source shape0.8, pattern speed
\(\Omega=0.12\), harmonic frequency \(\omega=2\Omega=0.24\), N64 and spatial
CB0–6. Both actual signed sectors \(m=-2,+2\) are retained. Shape0.8 is already
included in the physical first-order source; work, torque and field energy are
coefficients per \(\epsilon^2\), where the actual perturbation is
\(\epsilon\) times that source.

For every selected \(\lambda\), the cached bare kernel is exactly affine,
\(K_\lambda=(1-\lambda)K_0+\lambda K_A\). The own response is a **fresh**
Volterra solve with that kernel. The orbital derivative is contracted from the
actual library with the frozen DF derivatives, then combined affinely. Every
selected bare and own cell gets a fresh full orbital energy/angular budget,
work history and full-raw-Gram self-field energy. Own budgets use \(b+c\);
bare budgets use \(b\), with no self-field term in their energy-budget identity.
Bare wakes alone use exact affinity. Cached own wakes, cached work curves and
endpoint scalar tables are not consumed.

Three fixed layouts are available: GL32/dt0.05, GL32/dt0.025 and GL64/dt0.025.
The two GL32 layouts deliberately share one identical GL32 library. These
controls are correlated and are not three independent physical theories.
Raw Gram off-diagonal and Hermitian defects, K(0), slope proxies, signed budgets
and power/shape/torque histories are preserved; no Ward repair, conjugacy
projection, normalization or endpoint correction is applied.

## Inputs and commands

Keep this directory separate from the existing capsule. In an eventual outer
release, `../calculation-source` denotes that unchanged capsule. The capsule can
also be supplied at another location explicitly through `--capsule`.

Inspect the required manifest without importing NumPy or performing a solve:

```sh
python -B run_strength.py --capsule ../calculation-source --inspect
```

Inspection emits an **unbound** template. Execution refuses it until actual
file byte sizes/SHA256 values, the runner/README hashes and the fixed complete
configuration have been bound. The manifest lives beside regular cached files;
all numeric paths are single relative filenames. A bound manifest states
`cache_provenance` as shown by inspection, identifies the unchanged capsule and
scientific source hashes, and records each layout's exact configuration,
`history` descriptor and the shared `libraries["32"]`/`libraries["64"]`
descriptors. A descriptor is exactly `{"path": "file.npz", "bytes": actual,
"sha256": "actual"}`. Hashes authenticate supplied files; they do not prove
independent physical validation. No future or placeholder data digest is valid.

The needed inputs are the raw history archive for each selected layout and one
GL32/GL64 orbit library as needed. Only ten history arrays are loaded: time,
full spatial metric, the four F0/A signed kernels and the four signed bare wakes.
Only the eight original library arrays e/eta/L/weight/nu/radial/radial_n/inplane_k
are loaded. All archive headers are bounded and exclude object/structured dtypes
before numerical imports; loading uses `allow_pickle=False`. Existing numeric
history archives may contain additional bounded fields, which are not loaded.
The complete inputs can be independently regenerated with the existing capsule:

```sh
python -B ../calculation-source/run_cycle.py --preset gl64-provisional --ne 32 --neta 32 --dt 0.05 --output gl32-coarse-fresh
python -B ../calculation-source/run_cycle.py --preset gl64-provisional --ne 32 --neta 32 --dt 0.025 --output gl32-fine-fresh
python -B ../calculation-source/run_cycle.py --preset gl64-provisional --output gl64-fine-fresh
```

Those commands are expensive fresh orbit/kernel calculations, separate from
this cached extension. They require their own prior resource allowance. The
already completed central GL64 CLI took17620.373073 CPU seconds on the recorded
host; that is not a platform guarantee, an E128 reproduction or a timing for
this extension. Its62-array/117-scalar equivalence was delivery of the same
frozen equations, not new independent physics. Additional cache packaging and
actual manifest hashes remain a release dependency; no numerical cache is
bundled with this source draft.

Run only after obtaining an external complete CPU/wall allowance. For example,
substitute the approved operational limits in this command; they are not
scientific parameters or measured cost promises:

```sh
python -B run_strength.py --capsule ../calculation-source --input-manifest cache/inputs.json --output fresh-strength-output --cpu-seconds APPROVED_CPU --wall-seconds APPROVED_WALL
```

The default performs \(\lambda=0.5,0.75\) on all three layouts:12 fresh own
solves and24 fresh signed orbital budgets including bare controls. Optional
`--lambda` selects one or more of exactly0,0.25,0.5,0.75,1; optional `--layout`
selects only the three named layouts. `--full` performs the entire fixed
five-strength/three-layout calculation:30 fresh own solves and60 fresh signed
budgets. It is **unmeasured** and does not inherit a canonical18-cell cost.
A subset receipt identifies precisely what ran and never claims a full map.

Whenever both GL32 layouts and the two fixed confirmation strengths are
selected, their four work/impulse forecasts are written once before any selected
GL64 own solve. They combine the GL32 step difference and fine budget residual;
action uncertainty remains unbounded. Actual GL64 values are compared only
later. With missing GL32 controls/strengths, the forecast is explicitly absent.
No parameter or confirmation point is selected after the outcome.

The runner sets one numerical thread and a4GiB process address-space limit;
selected input files total at most256MiB, each history at most64MiB and each
library at most128MiB. Output includes atomic temporaries within256MiB. These
limits may cause an honest failure and are not measured peak-RSS/runtime
certificates. External execution admission and storage monitoring remain the
caller's responsibility. Input file identities are checked during execution,
checksums are checked initially and finally, and source/manifest hashes are
rechecked. A STOP file in the fresh output requests interruption.

## Outputs and interpretation

`result.json` retains actual selected cells, signed totals, raw budget/metric/
kernel diagnostics, complete/partial product descriptors and any forecast
comparison. Each layout's `*-history.npz` retains completed raw wakes and six
recorded histories per cell. A full layout contains148 numeric members; header
capacity is160. `frozen-forecasts.json` is immutable once written. A successful
`TERMINAL.json` requires completion of every selected cell and unchanged inputs.
A stopped/capped calculation can leave partial products and cannot qualify a
prefix; failure may prevent a final receipt entirely.

All outputs remain finite-library numerical calculations with the same physical
and discretization assumptions. The existing independent-cycle sign evidence
is conditional on empirical refinements; original expanded magnitude/waveform
checks remain failed. This extension does not retroactively repair them. It
establishes neither a continuous dressed active band, causal stationarity,
continuum stability, an autonomous free-growing mode nor natural bar formation.
The positive supported quadrupole is a conservative source test, not established
stellar-bar mechanics. Source self-gravity is counted once; additional positive
constitutive support is disclosed separately in the outer scientific report.

Code is distributed under the outer release's MIT license, copyright ©2026
djova; retain that notice and the unchanged capsule's source notices. The new
model outputs carry the project's explicit data-rights notice. No third-party
observational catalogue is included or relicensed. Final package inclusion,
actual cached-input provenance, any execution/equivalence assessment and public
scientific projection remain conditional on the final assessed results and
release review.
