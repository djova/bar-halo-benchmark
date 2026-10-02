# Additional controls: population weighting, spatial readout, and a sealed forecast

Checkpoint `discovery-2026-10-01.6`. These controls extend the early-discovery
campaign, not the canonical noisy-resonance paper. Historical outcomes and
`checks-v1` remain unchanged. No new observation or live-galaxy test passed.

The [compact values](https://raw.githubusercontent.com/djova/bar-halo-benchmark/discovery-2026-10-01.6/discovery/data/checks-v2.json) are shared by
the figures, static tables, and [public saved-operand reader](https://github.com/djova/bar-halo-benchmark/blob/discovery-2026-10-01.6/discovery/scripts/discovery/replay_checks_v2.py).
The reader checks arithmetic. It does not certify the underlying force law,
sampling coverage, omitted tails, or numerical convergence.

## Warm population

![Recorded warm population](https://raw.githubusercontent.com/djova/bar-halo-benchmark/discovery-2026-10-01.6/discovery/figures/warm-cohort-v2.png)

DISC-CHECK-WARM-02. The cohort mass and signed heating contribution are different quantities. Bars on the latter are same-sample SE; the all-state numerical gate fails.

The stellar experiment uses a prescribed spherical Hernquist potential with
reference units \(G=M_h=a_h=1\). Positive gas components of mass 0.1,
scales 0.2 and 1.3, and cutoff 8 exchange a fraction
\(0.003\sin^2(\pi t/80)\cos(\omega t)\), at \(\omega=5,8\).
The endpoint is **80 Hernquist time units**. The stellar distribution has
guiding-radius density \(p(R_c)=R_c e^{-R_c}\), angular momentum
\(L=R_c v_c\), and conditional stationary radial-action density
\(e^{-J_r/J_*}/(2\pi J_*)\), where \(J_*=(0.1v_c)^2/\kappa\).
Spherical energy is insensitive to the orientation integral; this experiment
does not measure stellar thickness or vertical survival.

All 4096 original importance-sampled states and weights are retained, including
911 target-density underflows. The cohort \(R_c<0.25\) has exact target mass

\[
M_c=1-(1+0.25)e^{-0.25}=0.026499021160743902.
\]

This is a **guiding-angular-momentum selection**, not a present spatial cut,
halo binding-energy tag, or mass inferred from the sampled count. The figure
contrasts this mass with the cohort's contribution to the whole-population
signed finite-pulse-minus-numerical-zero response.

For paired per-path response \(Y_i\) and indicator \(B_i\), the recorded ratio
and its empirical same-sample delta-method standard error are

\[
u=\frac{\overline{YB}}{\overline Y},\qquad
\widehat{\mathrm{SE}}(u)=\frac{\operatorname{sd}[Y_i(B_i-u)/\overline Y]}{\sqrt N}.
\]

The inner numerator and denominator are correlated. Their covariance is
retained; treating them as independent would be wrong. Signed paired responses
permit a ratio outside \([0,1]\). The error bar is neither a calibrated confidence
interval nor a missing-tail or discretization allowance. The saved point ratios
are 95.558% ± 2.471 percentage points at frequency 5 and 99.8834% ± 0.0682
percentage points at frequency 8.

The inverse-composition allowance is \(10^{-9}\). The original coarse/fine
maxima, \(1.2553\times10^{-9}\) and \(2.1271\times10^{-9}\), both fail.
A tighter 20-state diagnostic passes only those selected states. The attempted
all-state extension stops at its resource limit after a complete first coarse
map; full fine maps and inverse compositions remain absent. Its scientific
qualification remains false. The tiny old/new coarse mean changes establish
arithmetic insensitivity of the **completed maps**, not qualification of the
missing work. There is no finite halo-to-star heating ratio or old-disk survival
bound in these records.

Saved fields are in `warm_population.original_fine_dilution`,
`original_inverse_failures`, `selected_replay`, `extended`, and `arithmetic`.
The portable operand descriptions distinguish whole-mass contributions from
conditional cohort means. The two downloadable arrays contain recorded values,
not reconstructed trajectories.

## Spatial field

![Recorded spatial field](https://raw.githubusercontent.com/djova/bar-halo-benchmark/discovery-2026-10-01.6/discovery/figures/echo-cross-v2.png)

DISC-CHECK-ECHO-02. Recorded signed imaginary potential/radial and real tangential components at time28, divided by fixed per-channel scales Q (not Toomre Q). Dashed lines mark the saved leading approximation; the radial scale spans dates28/32/36, so its time28 line need not equal1. Fine agreement with that approximation does not repair the failed coarse/fine gates.

The spatial echo model evolves an isochrone cohort with \(G=M=1,b=0.5\)
in an external field. Two positive-source pulses, degree/order \((2,2)\) and
\((4,4)\), retain common positive monopoles in every shape-sign case.
The absolute cohort mass is 0.952162896372471; no case mass is renormalized.
For the four sign cases the mixed complex coefficient is

\[
C_\mathrm{mixed}=(C_{++}-C_{+-}-C_{-+}+C_{--})/4.
\]

The readout is only the equatorial complex degree-2/order-2 potential and
radial/tangential force coefficient in a log-radius Gaussian annulus at radius
one, width 0.1. The real field is \(2\Re(C_m e^{im\phi})\); radial force is
positive outward. Other angular sectors, collective gravity and stars are absent.

The exact physical zero immediately after the second pulse at **isochrone
time 16** is a prerequisite. The subsequent nonzero comparison is at **time 28**.
Global-peak-scaled zero allowances and local-scale field differences are separate
tests. The fixed local component scales are

\[
(Q_\Phi,Q_R,Q_\phi)=(2.2724275174458845,1.319333933003653,4.582642287413650)
\times10^{-9}.
\]

Here \(Q\) denotes three field scales, not Toomre stability or the primitive
kernel in the canonical paper. Potential uses \(GM_0/L_0\); forces use
\(GM_0/L_0^2\). The dominant signed components in the plot are
\(\Im C_\Phi,\Im C_R,\Re C_\phi\), divided by their own scales. The leading radial line need not lie at one: its
fixed scale is selected over leading dates 28, 32, and 36 rather than at time
28 alone. Full complex
values and all four operands remain downloadable.

At time 28 the finer grid happens to lie within 4% of the saved leading
prediction. The original coarse-to-fine differences nevertheless reach
29.09%, 63.83%, and 29.39% of the corresponding local scales: all three
prospective 5% refinement gates fail. The two cross grids isolate the effects
of raising angular-momentum quadrature from 4 to 8 nodes and radial-phase
quadrature from 16 to 32. With coarse operator \(C\), cross operators \(X_L,X_\eta\),
and fine operator \(F\), the differences are

\[
F-C=(X_L-C)+(X_\eta-C)+(F-X_L-X_\eta+C).
\]

This is an algebraic decomposition of **numerical operators**, not three
physical forces. Angular-momentum quadrature dominates; the radial interaction
term remains material. Nothing refines beyond the existing 8/32 grid. The
remaining physical controls were not run, and there is no qualified late spatial
echo, visible disk response, or observational comparison. The earlier radial
memory experiment is a separate model.

Data keys: `echo_late.rows` (six closed rows with case operands and grids),
`original_failed_screen`, `cross_diagnosis`, and `local_scale_Q`.

## Twin forecast

![Recorded twin forecast](https://raw.githubusercontent.com/djova/bar-halo-benchmark/discovery-2026-10-01.6/discovery/figures/twins-forecast-v2.png)

DISC-CHECK-FORECAST-01. A sealed new weak-history forecast, not a driven measurement or an explanation of the earlier stronger-bar response. Bars are numerical proxies, not confidence.

This is a prospectively sealed **unforced-coefficient, second-order forecast**,
not an independently measured driven outcome. The populations have common mass
one in the reference isochrone and preserve the original matched moments.
The new history has amplitude \(\epsilon=10^{-4}\), a quintic ramp over 10 time
units, endpoint **40 isochrone time units**, no sweep, and reference pattern speed
set by \((J_r,J_z,J_s)=(0.08,0.05,0.30)\). This history does not explain or validate
the earlier amplitude-0.03, endpoint-300 response.

The observable is accumulated physical angular-momentum transfer
\(\Delta L_{z,+}-\Delta L_{z,-}\), in reference action units, per common mass
one. It is not instantaneous torque, \(J_s=L_z/2\), a percentage, or the
noisy-minus-smooth contrast in the canonical paper.

All seven grids, all three populations, the complete interior energy/circularity
domain and the real-field one-half are retained. The numerical proxy adds the
final anomaly-order change, action-grid change, and residual spectral-tail
proxy. It is compared with 5% of the absolute forecast. The full-norm tail proxy
is also reported. Quadrature-based norm estimates and refinement factors are
**not rigorous discretization bounds**. Family \(p=4\) remains tail-unqualified;
\(p=6,8\) pass this provisional numerical proxy with ratios approximately
0.198% and 0.024%. Weak-model applicability still requires the independent
forced and half-amplitude tests. No outcome was fitted to obtain this forecast.

Data keys: `twin_forecast.history`, `stages`, `qualifications`, and `limitations`.
The separately downloadable NumPy operator contains the exact eight scientific
functions, with original source and function-AST hashes. The portable NumPy
rerun regenerates all seven unforced grids in 123.85 CPU seconds on the recorded
host. It compares the forecasts, absolute spectral contributions, cancellation
ratios and signed in-plane sums at relative tolerance 2e-11, absolute tolerance
zero; it also compares both tail proxies for the declared paired/unpaired
checks specified in the operator README. This is not an exact comparison of
every NPZ array or validation against independently forced evolution. The saved
arithmetic reader launches no evolution; running the operator is a separate
explicit action.

## Evidence access and reuse

The [pinned public checkpoint](https://github.com/djova/bar-halo-benchmark/tree/discovery-2026-10-01.6/discovery)
includes compact values, two stellar operand arrays, their checksums, source,
and a saved-operand reader. This is an inspection/replay package; it does not
regenerate complete live galaxies or the spatial pulse trajectories. New code,
derived records and text use the benchmark's MIT terms. Dependency and external
catalogue/paper terms remain separate. Operational/privacy checks concern
delivery, not astrophysical validity. This work has not been externally reviewed.
