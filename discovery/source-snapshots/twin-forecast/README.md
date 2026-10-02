# Portable unforced forecast operator

`operator.py` contains eight scientific functions copied exactly from the
sealed calculation. `function-provenance.json` gives their original source
hashes and canonical Python AST hashes. Launch helpers and host-specific
potential snapshots are excluded. The only computational dependency is
NumPy; the recorded version is 1.26.4.

The input `operands/twin-forecast/populations.json` contains the frozen
populations and their archive checksum. No population was fitted to a forced
outcome. Expected contractions and all seven grid definitions are in
`data/checks-v2.json`. The model and quantity are described in CHECKS_V2.md.

From the public repository root, after creating the documented environment:

```sh
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
nice -n 10 .venv-discovery/bin/python discovery/scripts/discovery/reproduce_twin_forecast.py \
  --case a --cpu-cap 5 --output ./forecast-case-a
```

For the complete seven-grid matrix, choose another fresh directory and use
`--case all --cpu-cap 180`. Enclose it in a 360-second wall limit if `timeout`
is available. The recorded smoke costs 1.664 CPU seconds; the matrix costs
123.850 CPU seconds on the campaign host. These are measured costs, not
portable runtime guarantees. Each cap is a hard process CPU limit.
The full calculation can use substantially more memory than reading the
small JSON. Reading any publication page never launches this command.

The driver compares forecasts, absolute spectral contributions, cancellation
ratios and signed in-plane sums with the sealed outputs at relative tolerance
2e-11, absolute tolerance zero. It also compares both tail proxies for the
declared unpaired a/d/f and paired b/e/g grids. Case c's standalone tail is
recorded but not included in that particular driver assertion. It saves the
regenerated coefficient arrays for inspection; the receipt does **not** claim
that every array was compared or reproduced exactly.

Executing this operator regenerates unforced coefficients and a second-order
contraction. It does not evolve independently forced orbits, establish
weak-model applicability, reproduce the earlier epsilon=0.03/T=300 response,
or validate a live halo. The numerical tail proxies are not rigorous
discretization bounds. Family p=4 remains unqualified; every family is retained.
