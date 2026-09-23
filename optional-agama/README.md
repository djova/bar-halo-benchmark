# Optional analytical-coordinate benchmark

This deliberately difficult coordinate test is separate from the resonance
measurements. It tests AGAMA revision
`f302756b8af2b763db58e278e30478517dc8eea3` from
https://github.com/GalacticDynamics-Oxford/Agama . Preserve the upstream LICENSE
and build prerequisites. AGAMA's source and its linked GSL library have their
respective upstream terms; this repository does not redistribute either binary.
Credit: Eugene Vasiliev and AGAMA contributors.

Build an unchanged checkout and a separate copy with `stable-angles.patch`
applied using `git apply`. Run the same check on each built library directory:

```
python -m pip install -r optional-agama/requirements.txt
python optional-agama/check_coordinates.py --library PATH_TO_AGAMA --out coordinate-result
```

The test compares4096uniform phases and deliberately selected radial turning
phases, including an independent80-digit mpmath forward mapping. See
`reference/coordinate-check.json` for the complete original, intermediate and
final measurements. The half-angle-only patch is preserved as a failed
intermediate diagnostic; use the full stable-angles patch for the combined
repair. The original source and binaries in the experiment were unchanged.

The three changes stabilize two half-angle formulas and retain the signed radial
mean anomaly internally. Actions, forces, the Hamiltonian and physical parameters
are unchanged. Extreme turning-phase probes do not establish how often the defect
matters in a galaxy. This is a numerical-methods benchmark, not new bar physics.

## Four-case current-upstream regression

[The minimal regression](MINIMAL_REGRESSION.md) isolates four nondegenerate
turning-phase inputs. A23September2026check finds upstream master still at the
pinned revision. Fresh executions of the unchanged and separately patched
libraries preserve both the failures and the machine-precision repaired values.
This small review artifact includes80-digit coordinates, exact inputs and
receipts; it does not imply maintainer review or acceptance.
