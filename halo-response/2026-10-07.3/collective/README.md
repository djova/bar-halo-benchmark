# Current instructions for the joint F0/A collective calculation

These instructions describe the completed reference included in release
2026-10-07.3. The install requires a passing closed comparison; see
[the result](reference/result.json) and
[the equivalence summary](equivalence-summary.json) for actual operands.
The consumed five-file source is preserved in `calculation-source/`.
Its README and METHOD are historical preparation records, not the current
execution status or resource instructions.

The tested reference selects **F0, then A_full_plus**, with energy/circularity
orders 128/128, radial Fourier support N=64, radial basis n=0..6, dt=0.01,
T=120, rise/fall=12, Omega=0.12, shape=0.8 and bar mass 0.1. The retained
complex density coefficients have order population x m=-2..2 x n=0..6.
The source directly represents m=±2; its source-free m=−1,0,+1 entries are
retained as declared zeros. These are canonical linear response coefficients,
not positive particle masses or a nonlinear halo trajectory.

The actual executed runtime limits were **16,600 CPU seconds, 21,000 wall
seconds, 4,096 MiB address-space limit and 64 MiB output limit**. They are
caps, not measured usage or a portable runtime guarantee. Actual portable
process time, outer process-tree meter time and measured maximum child RSS are
copied into the reference's `resource_observations` from the complete records;
these different measurements must not be added as independent consumption.
The five-population default is a different, larger allocation. The F0/A
selector is essential to this tested four-GiB command.

## Reproduce

Use an environment with the exact versions in
[requirements.txt](calculation-source/requirements.txt). On a managed host,
obtain dependencies through its approved deployment procedure. This release
does not install software. Set a single computational thread and use a new
output directory. From the release root:

```sh
joint_parent="$(cd collective && pwd -P)"
cd collective/calculation-source
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
NUMEXPR_NUM_THREADS=1 BLIS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
python run.py --preset reference --ne 128 --neta 128 --radial-modes 64 \
  --nmax 6 --dt 0.01 --duration 120 --rise 12 --fall 12 --omega 0.12 \
  --shape 0.8 --populations F0 A_full_plus --cpu-seconds 16600 \
  --wall-seconds 21000 --memory-mib 4096 --output-mib 64 \
  --output "$joint_parent/reproduced-joint"
```

The intended output is the `collective/reproduced-joint/` sibling of
`calculation-source/`. Its parent must already exist and be a real path.
Use the resolved parent above: the frozen runner rejects a literal
`--output ../reproduced-joint`, because `Path.absolute()` does not normalize
`..` while the parent-identity check requires a resolved path. Existing outputs
are refused. Leave all five source files unchanged, including README and
METHOD: the runner hashes all five before and after its calculation. It does
not need AGAMA, a compiler, private archives, saved generators or saved orbit
libraries. A stop or cap failure remains incomplete; a prefix is not a cyclic
endpoint and no resume is supported.

The formula-only and smaller default calculations in the historical README
are separate controls or settings. They do not reproduce the joint result.
The older all-five dt=0.02 calculation remains separately documented in
[release .2](../../2026-10-07.2/collective/README.md).

The release also contains a separate
[equal-time density-null record](../diagnostics/ward-density-kick.json) and
[method/source excerpt](../methods/WARD_DENSITY_KICK.md). Those retain both
grids and all nonzero raw residuals of a completed projection diagnostic.
They add no evolution, independent collective-response confirmation or
forced-work error bound, and do not modify these five calculation files.

## Interpret and check the output

The reference preserves the actual step/time records, complete initial and
final rows, population order, coefficients, represented DF maps, canonical
energy and impulse, negative self-field energy, external interaction energy,
shape work, angular transfer, total and discrete work, physical/discrete
budget residuals, reality diagnostics and field-solve residuals. Its
`public_projection` explains which operational fields were omitted and binds
the unmodified source-result hash. No scientific row is dropped or altered.

The complete comparison requires absolute differences at most 2e-12 for energy
and coefficient channels and 2e-11 for impulse channels, at every common actual
recorded time. The F0 l2 energy-gap comparison uses 2e-12. Shared and unmatched
step lists are retained separately; no interpolation turns an unmatched record
into a matched one. Those are software-equivalence tolerances, not confidence
intervals, continuum bounds, or a global-stability claim. The comparison shares
equations, physical populations and quadrature with the reference calculation;
it does not add an independent physical experiment.
