# What the original unforced inputs say about the model's domain

22 September 2026. This is a descriptive measurement within the specified setup,
using the original table already hashed into the frozen forecasts. It fills the
variation report requested in TRANSFER_PREPARATION.md. No forced trajectory or
partial independent-confirmation result was used. The forecast, sample and all
acceptance rules are unchanged.

For the tested case B, the maximum fractional departure from the central value is:

| Region in slow action | Frequency gradient a | Bar coupling b | Halo-DF logarithmic slope |
| --- | ---: | ---: | ---: |
| Prescribed resonance path,0.250000 to 0.252817 | 0.745% | 2.104% | 0.353% |
| Initial mean±3σ,0.236308 to 0.263350 | 3.666% | 10.965% | 1.751% |

The latter interval contains 99.7300% of the declared initial Gaussian probability;
it is a descriptive interval, not a particle-selection cut. Every particle remains
in the experiment. The table has 65 nodes; endpoint values use linear interpolation.
These are ranges of that representation, not rigorous continuous-domain bounds
or estimates of the torque error. The scan uses 32³ angles and the central coupling
reference 64³; the original central quadrature difference is retained.

The chosen population is a more consequential limit on extrapolation. Along the
prescribed path, its **initial logarithmic slope becomes 17.4497 times steeper**.
The original halo DF's slope at fixed Jr=.08 and Jz=.05 becomes 0.99647 times its
starting value, a 0.353% decrease in magnitude. The selected initial density at the
ending resonance is 0.80327 times that at the starting resonance. These are properties
of the initial distributions sampled along a prescribed path, not measurements of
the evolved noisy or bar-forced density.

Both the reduced and Cartesian experiments already include the SAME full curved
Gaussian initial population. The 17.45 factor therefore does not identify an omitted
term or explain a failed matched prediction. It quantifies why a result for these
selected tracers cannot automatically become a law for the complete halo. The
previous width experiment concerns a different reference setup; it is not a new
case-B width sweep.

The reference libration period is 3995.87088 model time units. It spans 313.633
azimuthal-angle cycles and 460.392 radial-angle cycles. The full duration 20 local time
units corresponds to 3.18310 reference librations; over it the imposed pattern
frequency decreases 0.79414%, moving the resonance 2.5 reference half-widths.

Amplitude alone does not identify the resonant term. At the central action, the
archived (1,0,2) bar harmonic is stronger than (0,0,2), but oscillates 460.39 times faster
than the reference small-amplitude libration frequency. Every other member of
the 15 retained central harmonics has a nonzero detuning of at least 166.87 times that
frequency. This truncated spectrum is not a complete search for other resonances,
a statement about the entire action distribution, or a bound on unaveraged torque.

Case A is retained in the JSON. Its corresponding endpoint initial-Gaussian slope
ratio is 15.9441, and its swept coupling change 2.273%. Its separate forecast
prerequisite remains failed and its 3D seed remains unused. No qualification changes.

Exact isochrone frequencies and frequency gradients agree with every archived
scan point within 8.89e-16. An independent complex-step derivative verifies the
factor-of-two slow-action convention within 3.11e-15. The original 100 strict
cross-build DF-slope failures are unchanged; this readback neither repairs nor
relaxes them. No AGAMA re-evaluation was required.

Canonical readback and figures: result.json and the accompanying figures.
All numerical case fields match versions 01 and 02 exactly; only figure presentation
changed. The script runs from the full-precision public coefficient table and
forecast with NumPy/Matplotlib, without any simulation dependency. See
PROTOCOL.md for method and scope. A qualified held-out 3D
magnitude test is still required before assessing the physical reduction.
