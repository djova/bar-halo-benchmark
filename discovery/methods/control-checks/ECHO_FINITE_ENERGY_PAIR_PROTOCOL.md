# Frozen energy-only instantaneous-field pair

Prepared for coordinator review on 1 October 2026. **No pair has been launched.** This is a bounded numerical continuation of the nine-row diagnosis (archive reference: `ECHO_FINITE_DIAGNOSTIC_02.md`), which retained every row and failed the complete field-zero gate throughout. The new pair tests the demonstrated energy instability. It does not select a favorable outcome, change the physical model or evaluate a later field.

Source: echo_finite_energy_pair.py (archive reference: `../../scripts/discovery/echo_finite_energy_pair.py`), SHA-256:

```
4663c487d3928d1e4ca333c39dbafbe6f8b603411731372eff344fba0aec6b9a
```

Supervisor: echo_finite_energy_pair_supervisor.py (archive reference: `../../scripts/discovery/echo_finite_energy_pair_supervisor.py`), SHA-256:

```
f87ed7df4546e155dbdab993bd2e92fbcaf46e027a806ac14cd0d60f07ad6cb4
```

Only the output destination and coordinator-approved source/protocol/supervisor hashes are launch arguments. The two rows, time, amplitude, support, gates and cost allowance are frozen in the source. This is a separate source/protocol/output set; the failed pilot, first cost-stop and completed nine-row sources and receipts remain immutable.

## Physical setup and exact-zero observable

Keep `G=M=1, b=0.5` and the same isotropic isochrone distribution. Its smooth initial binding-energy taper is zero below 0.02 and full above 0.04, fixed before forcing. Positive binding energy is `E_bind=-E_orb`. The selected cohort mass is `0.952162896372471` reference-halo mass. All weights are absolute; there is no normalization, clipping or new cohort selection.

Keep pulse A `(ell,m)=(2,2)`, integrated mass 0.006, scale 0.8 and orientation zero. Keep B `(4,4)`, mass 0.010, scale 1.6 and orientation `pi/8`. Angular density contrast magnitudes remain 0.5. Four angular shape-sign histories share both positive monopoles. These are halo-only diagnostic impulses, not a demonstrated physical encounter acting on every gravitating component.

Every field row is **t = tau = 16, full amplitude factor 1.0**. The unchanged deterministic mapping/work/support probes retain the original amplitude factors 1.0 and 0.5, including their already disclosed forward/backward propagation after B. Those probes do not measure a later gravitational field.

Measure the same signed complex **degree-two/order-two** potential, radial force and tangential force in the log-radius annulus centered on radius one, width 0.1. Units are the reference potential/force units. Potential has the Newtonian negative sign; inward radial force is negative. The real azimuthal field includes the conjugate coefficient, with maximum amplitude `2 |C|`. No other angular degree or live stellar response is measured.

B changes velocity without changing position. Its exact unit-Jacobian velocity substitution requires the four-sign positional-field contrast to vanish immediately. Compute the result from the unchanged Eulerian inverse maps and subtract the distributions before gravitational summation. Save all four full complex operands, direct contrast, case masses, mixed mass, unforced mass, support exclusions, minimum inverse energies, roundtrip and subtraction discrepancies. Do not replace the numerical value by zero, subtract an earlier residual, or contrast nonlinear amplitude magnitudes.

The final binding-energy domain remains `[0.009,1]`, containing the globally proved attainable bound support. The original inverse-history exclusion is unchanged: histories below the proved post-A support have zero initial DF contribution. This is a support proof, not removal of kicked particles. All admissible histories use the same action finder, exact background propagation and inverse impulses. Initial inverse states below the original taper remain zero by the original DF.

## Two rows; all other counts unchanged

Grid order is `(energy, L fraction, inclination, eccentric anomaly, apsidal angle, node)`. Retain L4, inclination6, eccentric anomaly16, apsidal12 and node16 in both rows. The exact radial-angle Jacobian remains `1-e cos(eta)`.

| Row, evaluated in this order | Grid counts | Final binding-energy partitions |
| --- | --- | --- |
| `energy_split352` | `(352,4,6,16,12,16)` | `[0.009,0.02]:32`, `[0.02,0.04]:64`, `[0.04,1]:256` |
| `energy_split704` | `(704,4,6,16,12,16)` | `[0.009,0.02]:64`, `[0.02,0.04]:128`, `[0.04,1]:512` |

These double and quadruple the fixed segmented176 counts. The lower interval remains present for perturbed final-state support. Partition boundaries allocate quadrature nodes and do not alter the initial DF. Both rows must be retained regardless of their gate values; there is no automatic favorable-grid selection or orientation rescan.

Retain the cheap uniform scalar-energy mass ladder 16 through 2048 nodes, plus these two new segmented rules. It analytically integrates L/orientation using `(2 pi)^3 integral f_cohort(E) L_max(E)^2 (2E)^(-3/2) dE`, with `L_max=(1-E)/sqrt(2E)`. Save the corresponding six-dimensional minus scalar mass difference for each row.

Compare signed field changes both with saved segmented176 and, for the second row, with segmented352. Report differences relative to the fixed precise leading peaks; do not call a small difference independent accuracy evidence.

## Unchanged gates and frozen cost admission

The preserved seven mathematical functions must exactly match the archived original syntax trees; the grid function still differs only by its reviewed energy-node provider. New driver changes are row allocation, resource caps, prior-receipt provenance and cost/comparison bookkeeping. There is no solver rewrite.

Require the original tolerances: every complex field magnitude at most 10% of its frozen leading full-amplitude peak; unforced cohort mass relative error at most 0.1%; absolute mixed mass at most `1e-6`; mapper and deterministic inverse errors at most `1e-8`; external work at most `1e-12`; probe binding not below the rigorous floor minus `1e-12`. The peak coefficients are precisely `3.341803570152769e-9`, `1.1284622757699359e-8` and `6.760514915717661e-9`, respectively. All three field gates apply together.

The frozen cost profile is the **saved segmented176 row** in the preceding measurement (archive reference: `../../results/discovery-20261001/echoes/finite-map-diagnostic-completion02/measurement/result.json`), SHA-256 `4b377941b087c71151ea732379b05e2aa2fd9659a1bdc618086a0b37eb9823e9`. Its 12,976,128 points cost 32.354210703 CPU seconds. The pair contains 77,856,768 points, giving

```
projected_pair_CPU = 1.2 * 32.354210703 * 6
                   = 232.9503170616 seconds.
```

This profile is frozen before the pair, drawn from the preceding segmented-energy calculation because it measures the actual high-node work. It is not chosen from new outcomes. Compare the projection against `255 - process_CPU_so_far` after startup, scalar mass and mapping probes. If it does not fit, retain those records and launch neither field row. If it fits, run both in order with the same 1.2 allowance; later CPU exhaustion retains completed rows and separately labeled partial sums. Neither grids nor allowances may be adjusted during the run.

Reserve **260 summed CPU seconds**. Use one nice-10 scientific worker and OMP/OpenBLAS/MKL/NumExpr threads all one. The child installs soft/hard CPU limits 257/259 before scientific imports and checks a 255-second checkpoint between chunks. The supervisor's observed combined CPU stop is 257 seconds; wall limit is 900 seconds, followed by SIGTERM, SIGKILL after two seconds and at most three further seconds for reaping. Exceptional cleanup retains the existing stop deadline and exact `wait4` receipt where available. Total reservation is stopping headroom rather than a single combined kernel limit.

Both programs refuse pre-existing output directories and write failures only after their own successful directory creation. At start snapshot/hash this source/protocol, the original failure source/config/result/protocol, mathematical helpers and the preceding diagnosis. At closure verify live and snapshot hashes again, plus the same loaded AGAMA and leading-reference array hashes recorded in the previous frozen protocol (archive reference: `ECHO_FINITE_DIAGNOSTIC_COMPLETION02_PROTOCOL.md`). The supervisor records and checks its approved source pin and start snapshot. JSON normalization explicitly rejects unsupported/nonfinite types and encodes every complex field as real/imag arrays.

Count exact full reaped-child CPU plus supervisor CPU at the receipt as one outer ledger row; never add its nested child again. If reaping fails, label the observed CPU lower bound. `COMPLETE` means measurement termination, not scientific agreement. The independent constant-Hessian benchmark remains an inherited earlier pass, not a newly measured control.

A pair that passes still needs joint L/radial-phase convergence, weaker-amplitude controls and independent nontrivial readouts before any finite late echo claim. A failed pair remains a numerical failure, not proof that physical memory is absent. The document-only velocity-coordinate assessment (archive reference: `ECHO_FINITE_DIAGNOSTIC_02.md`) is outside this solver implementation.

## Proposed launch after exact-hash review

This command has not been executed. Replace the protocol token with the coordinator-reviewed SHA:

```
nice -n 10 .venv/bin/python scripts/discovery/echo_finite_energy_pair_supervisor.py \
  --out results/discovery-20261001/echoes/finite-energy-pair-01 \
  --expected-source-sha 4663c487d3928d1e4ca333c39dbafbe6f8b603411731372eff344fba0aec6b9a \
  --expected-protocol-sha PROTOCOL_SHA_FROM_FINAL_REVIEW \
  --expected-supervisor-sha f87ed7df4546e155dbdab993bd2e92fbcaf46e027a806ac14cd0d60f07ad6cb4
```
