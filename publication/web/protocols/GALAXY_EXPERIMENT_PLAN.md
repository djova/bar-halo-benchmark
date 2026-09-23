# Six-hour bar-formation experiment — public scientific extract

The original protocol and dated amendments are preserved below. One private
hosting instruction was omitted; host labels were generalized. Scientific
parameters, thresholds and outcomes are unchanged. This is a publication copy,
not a newly frozen protocol.

Started 2026-09-20 14:35:55 UTC. Deadline 20:35:55 UTC.

## Question and scope

Can an initially axisymmetric, self-consistent collisionless stellar disc and live halo develop a persistent bar, with quantitative properties comparable to published observations, on the local workstation within six hours?

This is an isolated, gas-free dynamical experiment, not a cosmological galaxy formation calculation or a CDM-versus-SIDM inference. The starting point is the public AGAMA bulge/disc/halo distribution-function example and the public falcON force solver, with exact source revisions recorded. Parameter choices and departures from published runs will be explicit.

## Planned model, chosen before viewing simulation outcomes

Use the AGAMA example's equilibrium construction with an exponential stellar disc, vertical sech-squared distribution, and a live NFW-like halo. Target disc scale radius 2.5 kpc, scale height 0.3 kpc, circular speed 240 km/s at 8 kpc; stellar fraction of squared circular speed 0.6, zero bulge, minimum target Toomre Q=1.5, halo scale radius 20 kpc, Gaussian outer cutoff 200 kpc. These are an exploratory bar-susceptible model, NOT an exact reproduction of the recent SIDM paper (which uses different parameters/cutoff and much higher resolution). Use the documented energy-based halo mass refinement to improve central sampling, and report masses. No imposed oval, bar potential, or phase alignment.

Benchmark particle count before fixing production resolution. Aim at a baseline, matched smaller/larger softening, smaller timestep, and a higher-particle-count run; use additional seeds and a hotter-disc comparison if time permits. Gravity uses falcON's P1 kernel, initially epsilon=0.1 kpc, theta=0.6. Fixed-step kick-drift-kick integration with timestep selected from accuracy diagnostics. Initial conditions and parameters are saved, and all runs have finite end times and wall-clock limits.

## Evidence and validation rules

- Download CDS S4G (J/A+A/587/A160) and MaNGA (J/MNRAS/521/1775) tables and ReadMe files; verify advertised row counts and record source URLs and SHA256.
- Verify forces against analytic two-particle P1 and direct sums; verify the integrator with orbital energy conservation; compare tree force tolerances.
- Track actual energy (T + 0.5 sum m phi), total and component angular momenta, centre of mass, disc thickness, radial profiles, local Fourier amplitudes AND phases, and global m=2 amplitude.
- Bar detection requires sustained m=2 growth and an extended nearly constant radial phase, supported by projected density maps; a spiral's m=2 peak alone is insufficient.
- Initial target conservation tolerances: max relative total-energy drift <0.5%; angular-momentum-vector drift <0.5% of initial disc Lz. Report failures rather than hiding them. Bar properties should be stable to about 10% across numerical controls before a quantitative convergence claim, allowing stochastic onset differences and comparing matched evolutionary stages explicitly.
- Compare the S4G definition of local Fourier amplitude with ours, including the factor-of-two convention. Never compare a global particle amplitude directly to a local image amplitude.
- Primary observational comparison: S4G bar amplitude and size, all finite measurements and a preselected stellar-mass interval within +/-0.3 dex of the model disc mass. Report the population spread and sample size, not a goodness-of-fit claim from one galaxy.
- Secondary comparison: MaNGA bar pattern speeds and corotation/bar-length ratio, with observational uncertainties and sample mismatch stated. Pattern speed requires coherent phase tracking; corotation requires a measured circular-velocity curve. Withhold quantities that cannot be measured reliably.
- No tuning model parameters or choosing output times to match the catalogue. Report trajectories and final outputs, not only the best-looking frame.
- Conservation alone does not establish convergence. A visual bar plus observational overlap is a demonstration with external benchmarking, not proof of the galaxy's history or dark-matter microphysics.

## Deliverables

Reproducible scripts, pinned dependencies and source provenance, raw observational tables, numerical checks, initial conditions and snapshots, plots/movie, and a concise report distinguishing pass/fail/unresolved findings. Leave host services and global packages unchanged.

## Recorded implementation decisions, before final outcomes

- Default theta=0.6 failed the initial desired force-accuracy bound in an independent 2,000-particle direct-sum test (99th-percentile relative force error ~4.8%). Production baseline uses theta=0.4 (~1.8%), with theta=0.25 as the tighter control (~0.52%); theta=0.2 provides the validation reference (~0.30%). These are approximation errors, not exact-force claims.
- Selected 120,000 particles (40,000 disc + 80,000 mass-refined halo), and 480,000 for the higher-resolution run. Baseline fixed timestep 0.2 Myr; the timestep control uses 0.1 Myr. All initially target 3 Gyr.
- The realized disc mass is ~6.16e10 solar masses and sampled minimum Q is ~1.31. The DF's target Q=1.5 is not the realized minimum. The initial smooth-to-particle radial-force mismatch reaches ~10% in the innermost radial bin, and must be treated as an initial-equilibrium limitation.
- At 2026-09-20 14:55 UTC, after the user requested intuitive interactive orbit visualizations, all runs were gracefully checkpointed. Fixed-identity star/halo trajectories and the inner-disc complex bar amplitude are now recorded every 1 Myr. Tracking starts between ~0.10 and 0.45 Gyr depending on the run; earlier individual paths will not be invented. Full stellar snapshots remain at 25 Myr and full halo snapshots at 100 Myr.
- A Ryzen-specific build (`-O3 -march=znver4 -fno-math-errno -fno-trapping-math`, without fast-math) benchmarked ~1.14x faster. Maximum baseline/native relative force difference was 6.2e-7; the independent direct-force and orbit tests also passed. All six runs resumed with this build; the restart ledger, old/new configurations, binary hashes, source pins and build instructions record this change. Independent simulations use separate CPU cores; rewriting the multipole algorithm would consume the validation budget.
- Added a causal control at 15:09 UTC using the same sampled phase-space coordinates in the fixed axisymmetric initial potential. This isolates the importance of gravitational response: it is not a competing live-halo model or part of the numerical convergence comparison. In this external field, energy uses the full external potential and axial angular momentum is the relevant conserved component.
- Midpoint review (16:20–16:30 UTC): base, soft050, soft200 and frozen completed 3 Gyr. All pass conservation, but final local-amplitude changes of +19.1% / −40.3% fail the approximately 10% softening-stability target. A saved independent seed43 realization was started with baseline eps=0.1 kpc, dt=0.2 Myr, theta=0.4, unchanged physical DF parameters and 3 Gyr target; its sampled Qmin is about 1.26. No original run is extended or replaced. Added direct-force checks on full evolved models and tilt-corrected thickness/phase-sampling audits. Face-on and measured edge-on exports show the subsequent weakening/thickening rather than selecting only peak-bar frames.

## Additional numerical follow-up fixed at 16:44 UTC

The completed 50/100/200 pc runs failed the preselected 10% final-amplitude stability target. With 3h50m remaining and two force-solver cores free (while preserving an unrelated ~2-core job), add `soft050_dt` (50 pc, 0.1 Myr) and `soft025_dt` (25 pc, 0.1 Myr), both using the exact baseline IC, theta .4, 120k particles and a 3 Gyr target. These are explicitly post-interim numerical diagnostics, not part of the original preselected six-run campaign. The pair isolates 25-vs-50 pc sensitivity at a common smaller timestep, while existing soft050 versus soft050_dt checks timestep sensitivity at 50 pc. This does not establish a continuum extrapolation or remove stochastic sensitivity. No physical DF parameter, measurement threshold or observed sample changes. Each gets a 9900-second wall cap, ending before 19:30 UTC; preserve partial outputs if either stops early. No extensions beyond the cap.
