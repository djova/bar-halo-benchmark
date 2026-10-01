# Exact archived echo source versions

The radial baseline/delay/amplitude controls used an earlier `echo_monopole.py`
source than the stronger-amplitude run. The only radial-solver change adds
full-process CPU accounting; the numerical evolution is unchanged. The current
`echo_halo.py` helper also changes the original quadrupole sampler to explicit
PRNG sampling and corrects its comments. The deterministic radial solver does
not call that sampler. Original quasi-random quadrupole confidence labels
remain unqualified.

The final spatial source adds a first-only calculation, a selectable DF
finite-difference step and refined quiet-field dates. With the original options
its leading bilinear formula is retained. The original direct-prediction source
and its three helper snapshots are included here for exact inspection.

The manifest records all snapshot hashes and their archived scientific IDs.
These are inspection copies, not scripts to execute in this directory: the
solvers’ `ROOT` assumptions expect `scripts/discovery/` in the package layout.
For an exact source-version rerun, use a separate checkout and replace the
corresponding optional `scripts/discovery/` files with the selected complete
snapshot family, preserving the released protocols and explicitly selected
AGAMA library. No such optional halo rerun was executed in the public control
receipt.
