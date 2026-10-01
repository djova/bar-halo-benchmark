# Halo twins with a gradually introduced bar

Prospective specification, 1 October 2026. This tests an important limitation of
the existing twin screen: its bar is fully present at the initial time. The
analytic zero-streaming populations are equilibria of the unbarred isochrone,
not of that suddenly barred field. A new growth history asks whether their
response difference survives removing the initial field discontinuity.

The three p=4,6,8 populations and conservative normalizations in
[the analytic construction](TWINS_EXACT_MOMENTS_PROTOCOL.md) remain unchanged.
Do not select p or enlarge its multiplier using the measured bar response.
The exact target/sampling-DF importance correction, common physical mass and
paired complete velocity reversal remain required. No per-population mass
renormalization is allowed.

## Fixed new history

Use the same G=M=1, b=0.5 spherical isochrone and broad quadrupole radius0.5.
Keep the stationary reference pattern speed defined by Jr=0.08, Jz=0.05,
Js=0.30. Introduce its amplitude continuously from0 to0.03 over100 reference
time units, using h(u)=u³(10−15u+6u²) for u=t/100 in[0,1], h=0 before
and h=1 after. The total endpoint is300, unchanged from the earlier screen.
The only changed physical input is amplitude history. The earlier whole-field
positivity proof applies because the amplitude never exceeds0.03.

The external work includes both rotation and growth:

\[
\partial_t\Phi_2=\Omega_p\tau_z+\epsilon'(t)\,\Phi_2/\epsilon(t).
\]

Implement the second term using the unit-amplitude potential, including at
epsilon=0; do not divide by a vanishing amplitude. Lz change, accumulated bar
torque and external work are distinct recorded channels. A smoothly imposed bar
is still external, with neither a live bar nor collective halo response.

## Independent checks before the ensemble

The current randomized matrix must terminate and the exact-family phase/step
readback must be reviewed first. Build a separate native kernel; do not modify
the running solver. Check it against a NumPy field and finite differences of
potential in space/time, including both ramp boundaries. Compare twelve fixed,
systematically selected paths through the full duration300 against DOP853 and
two fixed steps. Record the selected action/phase locations; no response-based
path selection is allowed. Give this preflight at most300 CPU seconds. It is
an independent selected-path verification, not full-library convergence.

Before selected integrations, freeze the following absolute screen allowances:
native/NumPy field disagreement1e-13; spatial/time finite-difference error1e-8;
coarse full-duration DOP853 differences5e-6 in each state component and1e-7 in
bar impulse and external work; coarse energy-minus-work budget1e-7 and Lz
bookkeeping budget1e-9. DOP853 uses rtol2e-11, atol2e-12. The half-step results
and order ratios are reported where larger than the reference noise floor;
do not demand a monotonic ratio for roundoff-limited paths. These absolute
selected-path screens are not a population-wide error guarantee. The separate
10%-of-contrast refinement gates below remain required.

## Sampling, recording and error gates

Eight new independent method4 libraries have512 action families, seeds
39401+100r, r=0..7. Each uses16 scrambled Sobol radial/vertical phase pairs and
32 equally spaced azimuth sectors with its own random offset:512 phase points
per sense. The primary uncertainty unit remains the whole independent library,
including its phase randomization. Use dt=0.01 and keep source/input/binary
hashes, mapped invariants, arrays and finite endpoint markers.

Retain all three population contrasts and their shared-reference covariance.
Report nominal pointwise Student-t intervals and a supplementary three-comparison
Bonferroni interval. Eight libraries do not establish calibrated coverage.
Ratios are point estimates unless their shared-reference uncertainty is treated.
All three comparisons share dynamics and are not independent physical regimes.

On library0, separately double azimuth sectors and radial/vertical phase nodes,
then halve dt. These isolate the two phase directions rather than conflating
them. Retain both signed and absolute weighted changes. A contrast is numerically
qualified only if each selected change is below10% of its ensemble magnitude;
otherwise retain the result as unqualified and identify the limiting direction.
The original factor-of-two ambition remains separate from a resolved small sign.

Save population-contracted cumulative transfer at the same25 recorded times,
the actual selected Cartesian traces, and final family impulses. A visualization
must identify these as tracer transfer under an imposed growing field, with
their own reference-time clock. Intermediate graph lines are guides only.

## Cost and scope

The anticipated ensemble plus three refinements costs roughly1.5–2 CPU-hours,
based on the current positive-source solver. Profile first and require the
root's total twin allocation to remain within8 CPU-hours. Use a single nice10
scientific worker with a hard finite timeout; no host timer. If the pilot fails,
stop before spending the ensemble allocation. Preserve every failed gate.

This is a prospective robustness experiment at a new forcing history. It is
not a magnitude prediction from an independently fitted response law, a live
stability test, an observed bar comparison or a new physical mechanism.
