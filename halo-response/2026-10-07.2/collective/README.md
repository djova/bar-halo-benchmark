# Portable central collective response

This NumPy/SciPy runner generates its own full-support Plummer action/orbit
library and evolves the central l2 collective response for all five published
DFs. It is an additive port of the existing robust/compact collective equations,
not an independent algorithm, new physical model or stability qualification.
The original bare runner and earlier release remain unchanged.

Keep these files together: `run.py`, `bare_run.py`, `README.md`, `METHOD.md`
and `requirements.txt`. `bare_run.py` is the exact immutable public bare runner,
SHA256 `abc1d554e8a642e4b2d0007f664a9b372c8d62c331966d37da517d3f66fdd9b1`.
The collective caller reads at most256KiB per local source/document and executes
only those checked bare bytes in a separate named module. It uses its orbital
pole/panel primitives and actual published DF constants, without patching it.
No campaign path, host service, saved trajectory or saved response is used.

Install Python3.11+ and the two packages in `requirements.txt`. The pinned
versions are the preparation environment, not a promise about all other
versions; the result records the versions actually used. Source preparation
has not run scientific imports, fixtures or histories. The campaign owner must
meter finite controls and a same-config reference comparison before scientific
use or publication as a validated collective reproduction.

```sh
python run.py --check-formulas --output collective-formula-check
python run.py --preset quick --output collective-quick
python run.py --preset reference --output collective-reference \
  --cpu-seconds 14400 --wall-seconds 43200 --memory-mib 4096
```

Every output directory must be new; an existing directory/file/link is refused.
The quick preset uses8x8 action nodes, signed radial N=8, nCB0..4 and dt=.02.
The reference preset uses64x64, N=32, nCB0..4 and dt=.01. Neither preset is
automatically a converged response. Both default to the complete T120 profile,
shape.8, rise/fall12, pattern speed.12 and physical Mb=.1, with all five actual
DFs and their own induced fields. `--check-formulas` runs only finite analytic
controls and records no physical endpoint or calculated response.

Explicit controls allow action/Fourier/basis/timestep refinement, nmax through6,
zero shape and `--self-gravity 0` bare controls. For a bounded comparison cycle,
set `--duration 12 --rise 6 --fall 6` and explicit matching grid/dt settings.
Cycle boundaries must be integer-step endpoints and rise/fall must be equal.
There is no quadrature tail cutoff, discarded node, frequency filter or mass
renormalization. An unresolved retained orbit aborts the entire calculation.

`result.json` contains actual coefficient histories, Q/J/projected U/included U,
external interaction, physical shape work and angular impulse, total physical
work, separate exact discrete flux, raw budget residuals, reality/field-solve
errors, initial absolute registers, conditioning and all orbital error/tail
channels. All five complex l2 m coefficients are explicit; m0/±1 are exact
zeros only for the declared zero seed and m±2 forcing. They are untested
stability sectors. The pattern is prescribed; no autonomous rotor evolves.

`checkpoint.npz` is atomically updated inside this newly owned output directory
and binds a completed step, actual coefficients/registers and recorded history.
It has no resume API. `--save-library` saves the freshly generated orbital
library; `--save-generator` includes the current dense generator in checkpoints.
These switches increase cost/output and need an explicit adequate output limit.
No archives are required to start another independent reconstruction.

CPU, wall, memory and aggregate output limits are explicit CLI controls.
On supporting Unix systems the runner lowers inherited CPU/address-space
limits, installs a wall alarm without extending an earlier inherited alarm,
and checks budgets cooperatively. Unsupported
limits are reported honestly; a cooperative timeout may wait for an active
native library call. A conservative named-array/import estimate rejects an
obviously undersized memory envelope but is not a peak-RSS prediction.
Writes are bounded by `--output-mib`; the current checkpoint and its temporary
successor both count during replacement. A timeout or failed step preserves
the prior checkpoint and cannot report a complete physical endpoint. Expired
budgets or a hard OS kill can prevent final failure JSON; the last checkpoint remains incomplete
evidence. The directory is never silently recycled for a retry. Directory
identity is held by an open descriptor where supported and checked against
the original file identity elsewhere. Atomic new-file publication requires
filesystem hard links; there is no overwrite fallback on unsupported storage.

The original bare bundle's separate matching/positivity certificate concerns
the stationary background DFs. This runner does not verify that proof and does
not certify a perturbed DF or nonlinear evolution. Matching/field conventions
and equations are described in `METHOD.md`. No bounded history, finite formula
check or source/reference agreement establishes continuum or whole-halo
stability. Opposite hidden variants have equal full unforced spectra; a driven
same-handed bar comparison does not change that symmetry statement.
