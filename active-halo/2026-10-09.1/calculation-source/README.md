# Portable central cycle draft

This private source draft reproduces the central finite-cycle calculation
from newly constructed Plummer action coefficients. It is not a replay of
result summaries, a new independent physical method, or an independently
qualified scientific release. No portable calculation has run. The GL64
configuration is provisional until the scientific owner selects a final
independently qualified refinement. Portable equivalence remains untested.

The modules in `scientific/` preserve the three frozen scientific sources
byte-for-byte: physical-radius/log-anomaly DOP853 orbit construction,
retarded response and physical work/endpoint budgets, and direct Volterra
quadrature. Their SHA256 values are enforced by `portable_io.py` as well as
the package manifest. No host I/O module, drive identity, credentials,
closed-owner lookup, command launcher or stored numerical payload is included.
The preserved orbit module retains its relative scientific derivation citation;
that citation is not an execution dependency or a host filesystem operation.

`run_cycle.py` is a new thin caller of those unchanged functions. Its scientific
call order and arithmetic match the central fresh-library cycle. Additional
source histories and raw imaginary initial-slope registers are saved for
inspection; they do not enter the calculation. F0 and A remain separate,
each with both signed m=-2,+2 and both bare/own-field cases. The full signed
n and k=-2,0,+2 action lattice is used. No static term, action node, harmonic,
raw Ward register or mass deviation is removed or repaired.

The fixed units are G=Mtotal=a=1, Mh=.9 and Mb=.1. The physical harmonic is
2 Omega=.24, with pattern Omega=.12. `inputs/population.json` records the
exact already selected six coefficients and F0 reference Q=14/33. The runner
checks these values before importing a numerical backend. It performs no
population/source search. The symmetric pulse has rise/fall12, shape.8 and
complete duration120; physical source scalar is 3 Mb/(7 sqrt30).

## Configurations and prospective invocation

An environment with Python3.10 or later, NumPy and SciPy is required. The draft
uses their existing documented APIs, without compiling a replacement solver.
Exact runtime versions will be recorded by each run. A tested release must
declare the versions used in its portable equivalence check; no dependency
version or cross-platform equivalence is certified by this source draft.
This document provides invocation syntax, not authorization to execute or
install dependencies.

From the package directory, the source-only size/configuration preview is:

```text
python3 run_cycle.py --preset gl8-preview --preview
python3 run_cycle.py --preset gl64-provisional --preview
```

An externally admitted fresh run would use:

```text
python3 run_cycle.py --preset gl8-preview --output ../gl8-fresh-run
python3 run_cycle.py --preset gl64-provisional --output ../gl64-fresh-run
```

The output parent must exist, the final directory must be new, and output
must be outside the immutable package. Pass the externally published manifest
digest with `--expected-manifest-sha256 DIGEST` to bind a released package.
`checksums.json` lists every package source/configuration file, excluding
itself; its own digest must be supplied by the release or execution admission.
The draft has no saved-library input option or resume path.

Every original orbital control and cycle parameter is explicit. CLI overrides
include `--ne`, `--neta`, `--nmax`, `--radial-modes`, `--orbit-tolerance`,
`--initial-solver-rtol`, `--minimum-solver-rtol`, `--maximum-refinements`,
`--phase-step`, `--phase-panels`, `--phase-probe-order`, `--duration`,
`--rise`, `--fall`, `--dt`, `--shape`, and `--omega`. The original `--ramp`
shorthand sets rise and fall together; mixing it with either explicit field
is rejected. `--omega` is pattern speed, not the m2 harmonic. For example,
GL128 can be requested by `--ne 128 --neta 128`; no scientific source edit
is needed.
All changes remain subject to the unchanged scientific resolution bounds.

## Runtime and memory expectations

The GL8 preview contains64 fresh orbits,99 signed n/k channels per orbit,
three radial basis channels and1201 physical times. The provisional GL64
target contains4096 fresh orbits,387 signed channels per orbit, seven basis
channels and4801 times. Its radial coefficient array alone is
4096*129*3*7*8=88,768,512 bytes; this is not a peak-memory estimate.

Orbit work scales with the number of fresh nodes and each node's adaptive
integration. Kernel contraction scales as four populations/signed-sector
calls times Nt*Naction*(2N+1)*3*Nbasis². Eight endpoint budgets require
Nt*Naction*(2N+1)*3*Nbasis potential contractions. The direct Volterra
history has quadratic Nt cost. Exact reuse of an identical physical orbit
across F0/A derivatives is part of this same method, not an accuracy shortcut.

Each endpoint routine retains a complex time-by-action block with up to2048
frequencies: one such GL64 block is157,319,168 bytes. Potential and phase
blocks coexist, with expression temporaries and the full library/history.
Library construction temporarily retains individual orbit rows and the
stacked array; numerical integrator workspaces add memory. Preview component
counts therefore do not claim a bounded peak RSS. Full cost and peak memory
must be measured under a separately chosen execution limit. There is no
automatic expansion or continuation after an external resource stop.

No complete portable CPU prediction is made. First meter the accounted GL8
configuration, compare its raw fields/work against the central calculation,
then price the selected full target. Numerical library/threading and platform
can affect time and reduction order. Use an externally bounded single-thread
process for the first equivalence test; the package does not change global
thread settings or install software.

## Portable I/O boundary and qualification

`PortableIO` verifies package SHA256/size closure before numerical imports,
rechecks it periodically and before its terminal receipt, refuses existing
output directories, and atomically replaces flushed output files. The check,
write and stop interface is passed to the unchanged scientific functions.
An externally created `STOP` file requests interruption at the next check.
No unsupported claim of a host-specific held-volume guarantee is made.
External admission remains responsible for CPU, wall, RAM, disk capacity,
and filesystem availability.

An external wrapper may call `run_cycle(config, io, definition, label)` with
its own admitted I/O object; `io` must implement `check()`,
`write(name,value,arrays=False,np=None)`, and optional mutable `stop`.
No private I/O implementation is bundled or imported. This supports a local
equivalence run with its existing storage/resource guard without changing
the scientific sources or portable command.

A failure leaves prior complete atomic checkpoints. A stop/output failure
may prevent a failure or terminal receipt; those files are never substitutes
for all required successful endpoints. `OUTPUTS.md` defines raw arrays and
completion. All scientific qualification and portable-equivalence flags stay
false in this draft. Root will meter equivalence and decide publication after
independent coefficient/action/time/basis qualification, not from a successful
portable process alone.
