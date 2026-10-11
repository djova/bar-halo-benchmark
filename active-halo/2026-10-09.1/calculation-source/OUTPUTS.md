# Raw output definitions and completion

The run constructs inputs and fresh numerical states. It consumes no saved
orbit/kernel/wake/work array. Archive arrays are standard uncompressed NumPy
npz, with no pickle objects. Physical time uses sqrt(a³/(G Mtotal))=1.
All coefficient and overlap normalizations remain those in the frozen modules.

`START.json` records explicit orbital/cycle configuration, frozen physical
input hashes, package manifest SHA256, and the fresh-construction declaration.
`inputs.json` records the complete frozen population, selected configuration
and physical source/time conventions. Successful `TERMINAL.json` closes
unchanged sources and reports process CPU/wall time; it does not qualify physics.

`orbit-library.npz` saves every ndarray returned by fresh `build_library`:
original GL e/eta nodes and quadrature weights, physical L/Lc/action weights,
all signed n/k frequencies and physical radial Fourier coefficients, actions,
turning radii/residuals, solver controls/refinement/CPU registers, value and
derivative moments, and numerical Parseval tail proxies. No probability
normalization or population mass correction is applied. Tail proxies are
retained-node empirical diagnostics, not continuum or pointwise resonance bounds.

`history.npz` contains the complete uniform physical `time` and full
`spatial_metric`. For each `F0`/`A` and `m-2`/`m2` prefix it saves `kernel`
with shape(Nt,Nbasis,Nbasis), physical `source`, `source_derivative` and
`source_shape_derivative` with shape(Nt,Nbasis). For each additional
`self0`/`self1` prefix it saves `wake` and the six physical time histories:
`power`, `shape_power`, `torque`, `work`, `shape_work`, and `impulse`.
Raw kernel-diagnostic JSON strings retain real/imaginary K(0) and first-step
secants for all basis pairs; these are uncorrected finite-window diagnostics.

The wake is the induced potential coefficient c. Bare uses total forcing b;
own-field uses b+c. Both calculations start with the actual zero induced
state. Negative-m source is the conjugate physical source, but its kernel and
wake are computed separately from the full signed action contractions.
The physical spatial Gram matrix remains negative on its diagonal.

`result.json` records all eight signed cells and four paired totals. W2 and
J2 are work/impulse from physical spatial source overlap; `shape_W2` is
amplitude-change work, `rotational_W2=Omega*J2`. `orbit_Q2` and
`canonical_J2` are endpoint action budgets. `self_U2=.5 c†D c` uses the
unchanged negative gravitational metric. Raw residuals are
Q2+self_gravity*U2-W2 and canonical_J2-J2. No energy/impulse repair is made.
Conjugate-wake differences, actual finite-quadrature halo mass, maximum orbit
refinement registers and runtime numerical versions are retained.

`progress.json` is incomplete until every signed cell and final archive have
finished. `checkpoint.npz` contains only completed cells plus their available
kernel/source arrays; it is a partial prefix, never a complete physical cycle.
During fresh library construction no orbital prefix archive is supplied by
the frozen builder. A failure can therefore leave only the explicit inputs
and progress receipt. Later failures preserve the last complete atomic cell
checkpoint and raw completed-cell records. `failure.json`, if writable, names
the stage and error without presenting a partial sum as complete.

Numerical completion requires a successful process, complete `result.json`,
complete final `history.npz`, complete orbit library, and successful unchanged
`TERMINAL.json` bound to the same `START.json` manifest/configuration. One
complete flag alone is insufficient. A wrapper supplying its own I/O owns
its outer terminal closure instead. Checkpoint completion cannot repair a
missing endpoint or a failed terminal source check.

The selected GL64 target is provisional. Complete=true certifies a complete
numerical reproduction attempt only. Portable equivalence, numerical
convergence, continuum response, real-axis power and stability remain
unqualified. A future admitted comparator must inspect raw arrays and full
budgets with independently selected numerical allowances; no bitwise pass or
new scientific threshold is introduced here.
