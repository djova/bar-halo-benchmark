# Frozen instantaneous-field diagnostic completion 02

Prepared as an immutable continuation for coordinator review on 1 October 2026. **Completion 02 has not been launched.** The earlier cost-stop measurement (archive reference: `ECHO_FINITE_DIAGNOSTIC_01.md`) and its source/protocol remain unchanged. Only resource caps and file/output names change; the nine-row plan, all physics, gates, support and the 1.2 safety factor are identical. This proposal follows the retained finite-map failure (archive reference: `ECHO_FINITE_FAILURE_01.md`). It evaluates the field only at `t = tau = 16`, where the exact shape contrast is zero. It cannot validate a late spatial echo, even if its numerical gates pass.

The source is echo_finite_diagnostic_completion.py (archive reference: `../../scripts/discovery/echo_finite_diagnostic_completion.py`), SHA-256:

```
a9daf7840e4e1b9daee72921caee3d91d2a45a1b4617b131a67c465926ce9ee8
```

The external supervisor (archive reference: `../../scripts/discovery/echo_finite_diagnostic_completion_supervisor.py`) has SHA-256:

```
6ce6db69d7fb2e4386e4c587ba69c072f09e07ffd586115d82438b4551d5401e
```

Only the output destination and required coordinator-approved source, protocol and supervisor hashes are launch arguments. The physics, time, amplitude, refinement directions, gates and cost rules below are frozen in the source.

## Unchanged physics and exact-zero test

Keep the original isochrone background `G=M=1, b=0.5`, initial isotropic distribution and pre-forcing binding-energy taper from 0.02 to 0.04. Here `E_bind = -E_orb > 0`. The selected cohort is 0.952162896372471 of the reference halo mass; weights remain absolute, without renormalization. The unselected halo has not been tested.

Pulse A remains spherical degree/order `(2,2)`, integrated mass 0.006, scale 0.8, orientation zero. B remains `(4,4)`, integrated mass 0.010, scale 1.6, orientation `pi/8`. Both have angular density contrast magnitude 0.5. All four angular shape-sign histories retain both positive monopole pulses. The final-state domain remains `0.009 <= E_bind <= 1`; the original global kick/support bounds and inverse-history support test are unchanged.

Use full amplitude factor **1.0** for every field row. The unchanged mapping/work probes retain both original factors 1.0 and 0.5. No amplitude is selected from the diagnostic result.

The readouts are the signed complex **degree-two, order-two** Newtonian potential, radial force and tangential force in the existing log-radius annulus centered on radius one, width 0.1. Their units are the reference potential or force units. Negative potential and inward-negative radial force preserve the existing convention. A real azimuthal field includes the conjugate coefficient, with maximum amplitude `2 |C|`. This does not measure all allowed angular sectors, a stellar response or collective gravity.

Immediately after B, position is unchanged. Its velocity impulse is an exact unit-Jacobian substitution in the velocity integral. Consequently the four-sign contrast of every position-only readout is exactly zero. Compute that contrast using the inverse-map final-state quadrature; do not replace it with its analytic zero. Retain both direct distribution-contrast integrals and all four individual complex field and absolute mass integrals.

No field dates after 16 are evaluated. The inherited six-orbit Cartesian mapping probes include a forward/backward propagation after B solely to audit the inverse map; they do not measure a later density or force. There is no memory-erasure, separation, live-disk or collective-field calculation in this allocation.

## Preserve mathematics and avoid the old import limit

The archived preflight installs a hard 100-second process limit on import. The new driver **does not import it**. Instead, seven functions are copied statically: `json_ready`, `write`, `complex_json`, `pulse`, `loss_bound`, `cartesian_probe_checks` and `finite_row`. Their syntax trees must exactly match the archived source before evaluation and at closure. The only change to `final_grid_chunk` replaces its two-line uniform energy-node expression with `energy_nodes()`. An additional syntax-tree comparison verifies that all its remaining mathematical expressions are identical.

The runtime audit compares against the immutable archived source, not a newly edited working copy. The scalar mass and row annotations are separate diagnostic functions. In particular, the pulse gradients, support test, cohort, inverse Cartesian action finder, phase propagation, gravitational readout, Jacobian and case contrast remain unchanged.

Frozen archived inputs are:

| Input | SHA-256 |
| --- | --- |
| Archived source | `d222c0ba4321678ce96a328714b8ef95c969f77fed6f3d6db862b97afeffd6b3` |
| Archived configuration | `25f1a061c4de3fff4581e0b42ef6667877ac1cc3410ec2b4e899923693008925` |
| Archived measurement result | `9ec150abe878f86d15c7685953a5e2bcb640d933c0f747bf03f534062c505e05` |
| Original preflight protocol | `2139dcc9a5254d3ff48678a5db876949aa790160647b5e44d4dca261b2e8a67f` |
| `echo_halo.py` | `9bedf5c1f8a6e87358a6fbedc242b23b28fa30e6102fb1e0ebe3882e68af0797` |
| `echo_monopole.py` | `e8a45d0467f067132377ca418456960b39f26ae6c0f7eeb1f05f9ee666afe570` |
| `echo_multipole_pulse.py` | `96eb3c6c66d579389fafbae1a326f0686bb773b1b13e3c448a3abbbd87fe06c3` |
| `echo_two_frequency.py` | `daa16d290759510fc0ca3b9b30179d9aca5e0138cd2f453ce0be2c2afeeabd35` |
| Loaded AGAMA binary | `f6c04e4941aff3538d3bb08f6446d731b788d85406af94092cf856fbd139d000` |
| Frozen leading reference arrays | `2d26635a86096770e0187a812a1c99728fd13591f85e8531703df42ca99c777c` |

The independent Gaussian/constant-Hessian control passed in the original measurement. This diagnostic explicitly **inherits** that result; it does not report another independent known-limit validation.

## Mass reduction and fixed refinement matrix

The unforced isotropic mass reduces analytically to

```
M = (2 pi)^3 integral dE_bind f_cohort(E_bind)
    L_max(E_bind)^2 (2 E_bind)^(-3/2),
L_max(E_bind) = (1-E_bind)/sqrt(2 E_bind).
```

This exactly integrates the L and orientation variables. Evaluate a cheap uniform-energy ladder with 16, 32, 64, 128, 256, 512, 1024 and 2048 Gauss–Legendre nodes, plus the two partitioned rules below. Save every absolute mass and difference from the fixed cohort mass. For every six-dimensional row also save its difference from the corresponding scalar-energy mass. This isolates the unforced energy/taper error; it does not assume the perturbed field has the same sole source of error.

Grid counts are ordered `(energy, L fraction, inclination, eccentric anomaly, apsidal angle, node)`. Unchanged uniform eccentric anomaly uses the exact radial-angle Jacobian `1-e cos(eta)`. All nine rows and their order are frozen:

| Row | Counts | Refinement relative to comparison row |
| --- | --- | --- |
| `baseline_regression` | `(16,4,6,16,12,16)` | Reproduce the archived failure with uniform final energy nodes |
| `energy_uniform64` | `(64,4,6,16,12,16)` | Energy count only, versus baseline |
| `energy_split88` | `(88,4,6,16,12,16)` | Partition final energy at the original taper endpoints; comparison anchor |
| `energy_split176` | `(176,4,6,16,12,16)` | Double the energy count in each fixed partition, versus split88 |
| `L8` | `(88,8,6,16,12,16)` | Double L fraction only, versus split88 |
| `radial32` | `(88,4,6,32,12,16)` | Double eccentric-anomaly phase count only, versus split88 |
| `inclination12` | `(88,4,12,16,12,16)` | Double inclination count only, versus split88 |
| `apsidal24` | `(88,4,6,16,24,16)` | Double apsidal phase count only, versus split88 |
| `node32` | `(88,4,6,16,12,32)` | Double node phase count only, versus split88 |

The split88 energy rule uses `[0.009,0.02]:8`, `[0.02,0.04]:16`, `[0.04,1]:64` nodes. Split176 doubles each count. The lower partition is retained even though the unforced initial distribution vanishes there: perturbed inverse histories can contribute in that final-state interval. These partitions change only quadrature allocation. The original smooth initial taper, support and mass remain unchanged. Final-energy partitions do not guarantee resolution of the shifted initial-energy taper or phase filaments.

The baseline must reproduce all three archived mixed field coefficients and unforced mass to `1e-12` absolute. This is a regression check, not a field-error tolerance. Retain all one-factor directions irrespective of their gate outcomes; there is no automatic choice of a favorable grid, combined winner, larger count or adjusted allowance.

## Gates, cost and termination

Preserve the original physical gates without loosening them:

| Gate | Fixed tolerance |
| --- | --- |
| Each complex instantaneous field magnitude | At most 10% of its frozen full-amplitude leading first-window coefficient peak |
| Unforced absolute mass relative to fixed cohort mass | At most 0.1% |
| Absolute mixed mass | At most `1e-6` reference-halo mass |
| Internal Cartesian mapper roundtrip | At most `1e-8` |
| Six-orbit Cartesian inverse probes / external work | At most `1e-8` / `1e-12` |
| Probe post-B binding support | Not below the original rigorous binding floor minus `1e-12` |

The saved peaks are approximately `3.34e-9` potential, `1.13e-8` radial force and `6.76e-9` tangential force. Actual gates use the archived precise values. Save all complex components, case masses, unforced and mixed masses, support exclusions, minimum inverse energies, roundtrip errors, cancellation discrepancies and stage CPU. A passing mixed mass does not substitute for passing the gravitational field.

Use one nice-10 scientific process, with OMP, OpenBLAS, MKL and NumExpr threads fixed to one. The proposed total reservation is **320 CPU seconds including supervision**. The standalone driver installs soft/hard CPU limits of 317/319 seconds before scientific imports and checks a 315-second checkpoint between chunks. The supervisor stops on 317 observed combined child/supervisor CPU seconds. It imposes a finite 900-second wall limit, then SIGTERM, SIGKILL after two seconds and at most three further seconds for reaping. No persistent scheduler or timer is involved.

The 320-second total is a reservation with stopping headroom, rather than a single kernel-enforced combined CPU limit: the child's 319-second limit is hard, and the supervisor's overhead is measured separately. Unexpected supervisor exceptions after child launch also invoke the same bounded termination/reaping path before writing a failure receipt. If termination has already started, cleanup retains the existing deadline rather than granting another interval.

Before starting the remaining eight rows, profile the reproduced baseline and calculate

```
projected_remaining_CPU = 1.2 * baseline_stage_CPU
                          * remaining_grid_points / baseline_grid_points.
```

The fixed remaining matrix has 75.5 times the baseline point count. The reviewed first diagnosis measured 3.260461759 CPU seconds for its full-amplitude baseline, projecting **295.3978353654 remaining CPU seconds after the fixed 20% safety allowance**. Its original 295-second checkpoint left 291.351517413 seconds, so it stopped exactly as specified. The new 315-second checkpoint leaves approximately 311 seconds if the measured profile repeats; no quadrature rule or outcome gate was changed to fit the allocation. Imports, probes and mass ladder consume additional recorded CPU. This is a projection, not a benchmark promise. If the live projection exceeds `315 - process_CPU_so_far`, stop after the baseline/mass ladder and retain the cost review. Do not launch a partial favorable subset or change the safety factor. If the matrix proceeds, evaluate all fixed rows in order; a later CPU interruption preserves completed rows and separately labeled partial quadrature sums.

The outer receipt uses exact `wait4` user-plus-system CPU for the entire reaped child, including imports, failure handling and exit, plus supervisor CPU at the receipt. The ledger counts that outer job once and never sums its nested child again. If reaping fails within the finite margin, report only the observed CPU lower bound. Completion reports termination, not a scientific pass.

Both invocations refuse pre-existing output directories. Their failure handlers can write only after creating their own directory. At start, snapshot and hash the new source, this protocol, original source/config/result/protocol and mathematical helpers. Before completion verify those live inputs and snapshots again, together with the loaded AGAMA and reference hashes. The supervisor requires its coordinator-approved hash before starting the child, snapshots its source, and retains the approved pin for both live and snapshot checks at closure. Explicit JSON normalization accepts NumPy scalars/arrays, uses real/imag arrays for complex fields, and rejects nonfinite floats, unsupported types and non-string object keys. Syntax and static function-audit checks are preparation checks, not scientific jobs.

Even if one or more rows pass, the result establishes only a numerical direction worth checking. A converged combined grid, weaker amplitude, late waveform, memory erasure, separation and self-consistent response remain separate gates. This diagnostic will not advance them.

## Proposed launch after coordinator approval

Replace the protocol hash token with the final reviewed SHA; a protocol cannot embed its own hash. This command is documentation and has not been executed:

```
nice -n 10 .venv/bin/python scripts/discovery/echo_finite_diagnostic_completion_supervisor.py \
  --out results/discovery-20261001/echoes/finite-map-diagnostic-completion02 \
  --expected-source-sha a9daf7840e4e1b9daee72921caee3d91d2a45a1b4617b131a67c465926ce9ee8 \
  --expected-protocol-sha PROTOCOL_SHA_FROM_FINAL_REVIEW \
  --expected-supervisor-sha 6ce6db69d7fb2e4386e4c587ba69c072f09e07ffd586115d82438b4551d5401e
```
