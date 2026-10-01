# Recovery of the three growing-bar numerical refinements

New recovery specification, 1 October 2026. This is a numerical completion of
the already declared growing-bar matrix, not a new population or forcing
experiment. It supersedes no scientific criterion in
[the original protocol](TWINS_GROWTH_PROTOCOL_V1.md).

The original `growth-01` process disappeared without a terminal marker. Its
eight coarse cases have individual complete markers and full arrays. The last
azimuth-refinement checkpoint reaches time 262.5, with reported elapsed CPU
5171.80689222 seconds and case CPU 924.5943177029994 seconds. The cause is not
established. Do not mark that original command complete, overwrite its files,
or mistake its reduced checkpoint for a restartable full-particle state.

## Preserved experiment and frozen inputs

Retain the original eight libraries, all their completed results, their initial
states, and their sampling/phase rules. Compute their ensemble statistics only
from those eight completed results. Their populations, common physical masses,
importance weights, amplitude history, pattern speed, duration 300, 25 recorded
times, and uncertainty conventions are unchanged. No selection or resampling
is permitted in response to any coarse result.

Before any new evolution, copy and hash every original source/native snapshot,
the original start/config/profile/partial-status records, all eight completed
coarse products, and the saved partial azimuth refinement. Copy and hash this
recovery wrapper and protocol separately. Validate each original source against
the original `START.json` and every original completed array against its saved
result hash. `--prepare-only` performs this freeze without importing a scientific
helper or integrating an orbit. The frozen copy of the wrapper is the subsequent
execution entry point; it rejects changed manifest bytes.

Import only the copied original helpers, including the original AGAMA and native
growth binary. Do not import the current working-tree helpers. The original
`run_case`, population contraction, ensemble, and refinement functions are used
unchanged. Only their process-start clocks and finite CPU/wall bookkeeping are
reset for this new command.

## Three required recovered cases

1. **Azimuth double:** load the original saved 1024-phase, 64-sector initial
   states, actions, physical masses, and weights exactly. Integrate from zero
   with the original dt=0.01. Do not reconstruct these available states.
2. **Radial/vertical double:** retain the coarse library's actions, physical
   masses, offset, and seed. Generate only the previously unsaved 32 Sobol
   radial/vertical pairs, with 32 azimuth sectors, using the original phase rule
   and original mapper. Recompute no action library or importance weights.
   Save these newly mapped initial states and their hashes before integrating.
3. **Half step:** use the exact saved coarse-0 initial states, actions, masses,
   and weights with dt=0.005.

An independently written nesting check verifies the exact actions/masses/weights,
velocity-reversal pairing, phase angles, and coarse states inside each doubled
rule. Require the mapped nested states to agree within the original absolute
1e-12 allowance. Record exact-equality status and maximum differences rather
than implying all mapped states must be bitwise equal. Also call the unchanged
original nesting check; disagreement is an execution failure.

For the recovered azimuth case, compare **every** saved family impulse and work,
all 512 recorded Cartesian traces, trace impulses/work, trace IDs, and times
through the original checkpoint's time 262.5. Require numeric bitwise equality
of those arrays, and equality of the saved contraction and budget histories.
Archive maximum absolute differences even when equality holds. This is a
deterministic replay check using identical inputs and a single-thread binary,
not an independent physical sample. If it fails, retain the result and stop;
do not loosen the threshold or proceed to a silently altered composite.

## Cost qualification and terminal status

Use one nice=10 worker and one OMP/BLAS/MKL/NUMEXPR thread. The **new command** has
soft CPU 3500 seconds, hard CPU 3600 seconds, and wall limit 4200 seconds.
Its old partial azimuth timing suggests 1056.68 seconds for a full case. Three
such cases with 10% overhead project about 3487.04 seconds; this is a planning
estimate, not permission to exceed the cap.

Treat the recovered full azimuth case as a measured whole-case cost pilot.
After its replay check, require

`elapsed_new_CPU + 2 * azimuth_case_CPU * 1.10 <= 3500 seconds`.

If this fails, stop before the remaining two cases. Retain all outputs and the
failed cost gate. The root must reserve this new allocation separately from
the interrupted command; original actual CPU is incompletely measured, so its
original 9000-second hard cap remains a conservative upper reservation.

Apply the unchanged three selected signed-refinement gates: each endpoint net
shift must be less than 10% of the original eight-library ensemble contrast
magnitude for its population. Retain the absolute-family diagnostics, budget
histories, shared covariance, and failed scientific qualifications. No new
confidence or numerical-coverage claim is introduced.

A new complete composite, if all three cases finish, explicitly consists of
**eight retained original coarse cases plus three newly completed refinements**.
Its receipt reports new-command CPU separately and identifies the interrupted
parent and immutable parent hashes. Completion of this composite does not
change the original process's terminal status. A failed numerical qualification
is compatible with a complete finite command; these statuses stay separate.

This remains a prescribed-field tracer robustness test. It establishes neither
live-halo stability nor galaxy-bar evolution, SIDM behavior, observational
agreement, calibrated confidence coverage, or a prospective magnitude forecast.
