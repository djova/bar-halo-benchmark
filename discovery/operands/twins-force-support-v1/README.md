# Compact saved force and response-support operands

The five NPZ files use only numeric and boolean arrays; loading requires no
pickle. `manifest.json` defines each axis, dtype, shape, size, checksum, source
artifact hash, and pairing rule. The result record is
`../../data/twins-force-support-v1.json`. File order and array prefixes identify
the matching rows there.

- `selected-force.npz`: 36 static cases, 128 selected IDs per case. Both saved
  native and direct vectors are retained, including the rounded-input direct
  calculation. No full particle fields or particle coordinates.
- `continuum-quadrature.npz`: original saved node weights and integrands for
  thirty force and four virial integrations. Adaptive and central integrations
  remain scalar records; the replay does not regenerate them.
- `paired-live-diagnostics.npz`: nine original cases, all 31 diagnostic epochs,
  plus saved selected endpoint forces. No trajectory states.
- `early-energy-operands.npz`: three direct-potential epochs, specific kinetic
  energies, masses, isolated-partner family budget errors, and selected state
  differences. No live states, toy endpoints, or integration machinery.
- `action-support.npz`: sixteen history/library combinations, original actions,
  masses, stored DF ratios and odd weights, final partner impulses, and response
  contributions. Bin summaries are descriptive and post hoc.

False scientific gates are retained values, not missing data. Every array is in
the corresponding G=M0=1, isochrone b=.5 model units. Times are model times, not
Gyr. The isolated-partner toy, live halo, and prescribed tracer calculations are
separate dynamical systems; the manifest and companion note describe their scope.

The independent-sign replacement sampler is pending. No successful live bar,
collective-stability, observational-matching, or SIDM claim is added by this
saved-arithmetic packet.
