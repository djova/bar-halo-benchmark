# Descriptive domain readback of the original unforced calibration

22 September 2026. This completes the coefficient/DF-variation report explicitly
requested in TRANSFER_PREPARATION.md. The full unforced table has already been
measured and inspected; this is a retrospective descriptive readback, not a new
preregistration or a forecast fitted to any forced outcome. The independent
cadence confirmation is still running. Do not read its partial torques, change
its sources or launch additional trajectories for this task.

Use only the original unforced-coefficients/result.json whose hash is embedded
in forecast-freeze-01/forecast.json, and the two frozen configurations. Retain
both A and B, including A's failed forecast prerequisite and unused3Dseed.
No new dependency evaluation or forced integration is required.

For each case, report the recorded frequency gradient a, coupling b and halo-DF
log slope relative to their central values over two originally requested regions:
the prescribed resonance path Js0 through Js0+speed*end, and the Gaussian initial
population mean plus/minus3standard deviations (99.7300% initial probability).
Use actual table nodes and piecewise-linear endpoint interpolation; ranges refer
to this table representation, not rigorous bounds between unmeasured points.
Keep the32-cubed scan distinct from the64-cubed central coupling reference.

Also expose the following consequences of the same declared inputs:

- Compare the selected Gaussian's *initial* log slope along the prescribed
  resonance path with the tabulated analytical halo-DF slope there. The Gaussian
  matches the halo slope locally at the initial reference action; it is not the
  whole halo distribution. These curves are not evolved noisy or forced densities.
- Report the unforced azimuthal/radial angle periods and their ratio to the
  reference small-amplitude libration period2pi*time_unit. Model duration20 is
 20local time units, not20full librations. Check the exact isochrone frequency
  and derivative formulas against the archived table without importing AGAMA.
- For the15archived largest harmonics, identify each integer wavevector, its
  coupling relative to the retained resonance and its signed detuning divided by
  the reference libration frequency. Rank by wavevector identity, not assumed
  amplitude order. This is a truncated central-action spectrum, not a complete
  search for resonance overlap or a bound on omitted torque.

Generate readable, separately exportable figures for case B: coefficient
variation across the initial region with the prescribed sweep marked; initial
gradient encountered by the sweep; and coupling versus frequency detuning.
Measured coefficient markers and interpolating lines must be distinguished from
the analytically computed initial Gaussian and prescribed trajectory. No synthetic
simulation frames or new physical-model curves are introduced.

This readback introduces no pass/fail threshold for the constant-coefficient
approximation. A percentage change in a or b is not a percentage torque error,
and separated harmonic frequencies do not establish a valid transport prediction.
The frozen +/-20% operational band and all numerical gates remain unchanged.
Original100strict cross-build slope comparison failures also remain failures.
If the qualified physical test later fails, these inputs may inform the already
planned bounded discriminator; they do not identify its cause by themselves.

Budget: one nice10single-core analysis, at most120seconds wall time, no new
scientific worker beyond the four-worker host limit. Archive its input/source
hashes and CPU use, inspect the actual figures, publish the data, code, methods
and limitations on the existing sites and in the standalone package.
