# Portable bare and central collective halo response

Release `halo-response/2026-10-07.2` adds a portable NumPy/SciPy central collective
solver and one complete reference calculation to the earlier exploratory
benchmark. The six bare-runner companions, fifteen selected evidence files and
data schema are copied byte for byte from immutable release2026-10-07.1.
That release remains unchanged. This package is not externally reviewed.

The collective port generates its own full-support action/orbit quadrature and
each of the five represented distribution functions' own induced l2 field.
It requires Python3.11 or later and the pinned NumPy/SciPy dependencies; it uses
no host service, private archive or AGAMA installation. Keep all five files in
[collective/](collective/README.md) together. The bare dependency is exactly the
older public bare runner, not a separately fitted response.

From this release directory:

```sh
cd collective
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run.py --check-formulas --output local-formula-check
.venv/bin/python run.py --preset reference --dt 0.02 \
  --cpu-seconds 12000 --wall-seconds 24000 --memory-mib 4096 --output-mib 64 \
  --output local-reference
```

Every output directory must be new. Resource caps are finite operating limits,
not completion promises on another machine. The published reference uses
64x64 action nodes, signed radial Fourier supportN32, CB radial orders0..4,
dt=.02, T=120, rise/fall12, physical bar mass.1, shape.8 and prescribed
Omega=.12. The `reference` preset defaults to dt=.01; the explicit `.02`
override above reproduces the tested comparison. The quick preset is coarse.

[The reference JSON](collective/reference/result.json) retains every recorded
row, all five populations, all five complex l2 m columns, full radial
coefficients, initial registers, physical/discrete work and impulse ledgers,
and selected orbital/formula diagnostics. It is a public whitelist projection
of the runner's source-produced result schema; operational resource observations
and private provenance are excluded. [The comparison summary](collective/equivalence-summary.json)
contains the actual numerical differences and fixed tolerances against the
existing same-equation implementation. These are implementation checks using
shared equations and dependencies, not an independent physical sample,
statistical interval, continuum-error bound or stability proof.

Read [equations and provenance](collective/METHOD.md),
[release validation and limits](RELEASE_VALIDATION.md), and the unchanged
[evidence schema](results/DATA_SCHEMA.md). The immutable collective source
documents describe checks as pending because they predate the retained runs;
the validation companion records their subsequent completion without rewriting
hash-bound source files. The older [bare instructions](runner/README.md) and
[matching/positivity proof](runner/MATCHING_AND_POSITIVITY.md) remain available.

Negative prescribed-cycle halo work denotes energy returned to an external
driver. Neither runner evolves an autonomous stellar bar or responsive
nonlinear halo. Zero m0/±1 columns in the collective result are unforced,
zero-initial-generator sectors, not tests of their stability. The six-resolution
collective evidence retains empirical numerical allowances and incomplete
combined refinements; adding a portable solver does not strengthen those
physical qualifications or repair earlier magnitude failures.

`CHECKSUMS.sha256` lists relative release files and their SHA256 digests.
The benchmark's existing MIT license applies. Report reproducibility problems
or corrections through the [benchmark issue tracker](https://github.com/djova/bar-halo-benchmark/issues)
with the release, command, dependency versions and a sanitized error.
