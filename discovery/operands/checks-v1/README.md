# Saved operands for the control checks

These small operands allow arithmetic replay of the .4 control figures. They do
not contain particle initial conditions or regenerate any force or orbit.
[Hashes and byte sizes](manifest.json) identify every input. The scientific
readouts and original archive hashes are in [checks-v1.json](../../data/checks-v1.json).

- `phase-profiles.json`: all 31 epochs for each of six seed/population cases,
  with both analytic and original coarse live records. Each record contains model
  time and four fixed-shell masses, counts, coverage flags and diagonal raw
  velocity second moments. `second_diagonal` is ordered radial, azimuthal,
  vertical and has reference velocity-squared units. It is mass-normalized;
  multiplying by the saved shell mass recovers its raw numerator. There are no
  missing frames. Seeds are 50511 and 50512, populations F0, plus and minus.
- `warm-initial.npz`: the actual 512-state sampled guide and radial coordinates,
  physical/proposal weights, actions and exact proposal-component identities.
  Guiding radius Rc is in Hernquist length units; actions use its reference
  angular-momentum units. `guide_component` identifies the guide mixture and
  `radial_component` identifies the radial proposal part. They are proposal
  labels, not physical populations. The original seed is exposed in the JSON.
- `warm-fine-response.npz`: three treatments ordered unforced, carrier 5,
  carrier 8, each on the same 512 paths. `positive_64` and `positive_32` are
  the weighted forward-curvature plus inverse-capture estimates at two curvature
  node counts. They have specific-energy units. Their unforced row is subtracted
  path by path. `ordinary_signed_*` retains signed weighted forward energy
  increments. `R_*` and `support_*` separately retain curvature and capture
  terms. No path is deleted for a negative value, underflow or tiny weight.

For an inner cohort, multiply the paired values by its Rc selection and divide
by the **exact declared physical cohort mass**, not the sampled mass. Empirical
standard errors use 512 IID proposal states. Covariance between treatments is
preserved by taking paired path differences. The two carriers, cohorts and
numerical refinements are correlated.

The echo JSON supplies all four complex sign-case field integrals, their
contrast weights and the direct mixed-field integral. The full complex error,
not an isolated real or imaginary value, determines each component's zero gate.
The direct integral and separate sign-case reduction can differ at round-off.

Run the NumPy-only arithmetic reader from the repository root:

```sh
python discovery/scripts/discovery/replay_checks_v1.py --out checks-arithmetic
```

Install the existing pinned discovery requirements if NumPy is unavailable.
No AGAMA, pyfalcon, credentials or private archive is required for this reader.
It must not be reported as rerunning the numerical experiment.
