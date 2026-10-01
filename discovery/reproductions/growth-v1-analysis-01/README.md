# Growing-bar v1 saved-arithmetic replay

The recorded check recomputed 12,894 numerical values with maximum absolute
difference zero. Python 3.11.14, NumPy 1.26.4, and SciPy 1.17.1 were used.
The run uses saved impulses and frozen weights, never AGAMA or new evolution.

From the benchmark repository root, with a fresh output directory:

```sh
python discovery/scripts/discovery/replay_twins_growth_v1.py --out growth-v1-arithmetic-check
```

The receipt is arithmetic verification, not a new physical sample, calibrated
confidence coverage, or a guarantee that discretization proxies bound errors.
