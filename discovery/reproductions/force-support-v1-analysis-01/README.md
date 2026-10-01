# Saved force/support arithmetic replay

This receipt was produced by executing the NumPy-only reader against the five
compact operands in this package. It verifies saved-array arithmetic, rather
than regenerating a force, quadrature integrand, initial condition, or orbit.

- Dataset: `twins-force-support-v1`.
- Python: 3.11.14; NumPy: 1.26.4.
- Numeric values compared: 8,243.
- Logical/string values compared: 221.
- Maximum absolute numeric difference: 1.1102230246251565e-16.
- Replay CPU: 0.110274789 seconds. This final reader run follows publication-status metadata consolidation; the numerical operands are unchanged.
- Extraction CPU: 0.741881763 seconds; wall: 0.742080756 seconds.
- Compact NPZ size: 6,649,470 bytes.

The original paired live numerical qualification remains **false**. Passing this
arithmetic replay does not qualify that live screen or prove a stability result.
The retained continuum finite-difference gate remains false; the separate saved
known-formula diagnosis is not rerun here. Whole-particle force RMS summaries are
reported source outputs, outside this selected-target replay's coverage.

From `discovery`, choose a new output directory:

```sh
python scripts/discovery/replay_twins_force_support_v1.py --out reproductions/force-support-local
```

NumPy is the only non-standard-library dependency. There are no native force
libraries, AGAMA, authentication steps, or remote services in this command.
