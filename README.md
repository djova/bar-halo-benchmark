# Bar–halo response benchmark

A runnable controlled experiment in how imposed action noise changes bar torque.
At the same positive initial population, noise strength and elapsed time, the
reduced model resolves increased transfer at a stationary resonance and decreased
transfer at sweep s=.25. This is a finite local tracer population, not a full-halo
or dark-matter result. The independently frozen3D prediction remains numerically
unqualified; the package preserves that unresolved outcome.

**Regenerate the central matched figure:**

```sh
python3.11 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python reproduce_matched.py --out reproduced-matched
```

Python3.11 is the tested interpreter. The final command runs offline, generates
all initial conditions from seeds, and takes about45minutes on one CPU. It checks
both distribution estimates and all independent trajectory batches against the
reference. A clean isolated28-case rerun passes. No private files or credentials
are needed. Details and the full-precision receipt appear below.

[Interactive result, recorded paths and limitations](https://djova.ca/galaxy-bar/noise-sweep).

## Verify the finite-lag and collision-generator limits

The separate known-limit command also needs no private repository, particle
files, AGAMA, compiled gravity engine or API credential. In the same environment:

```sh
.venv/bin/python reproduce.py --out reproduced
```

The final command generates `result.json`, `finite-lag-controls.png` and
`maxwell-generators.png`. It refuses to overwrite an existing output directory.
This initial release verifies known limits, not a new astrophysical result:

* The exact Brownian and Ornstein–Uhlenbeck transition laws demonstrate why
  pooled finite-lag variance per time cannot generally identify a diffusion
  coefficient. Constant diffusion with restoring drift fails a flatness screen.
* Geometric Brownian motion demonstrates state-dependent Markov diffusion and
  the variance introduced by pooling different starting times.
* The Maxwell test reproduces an existing Galaxy Bar result: exact elastic
  jumps and their Gaussian second-order truncation agree on the first two jump
  coefficients but not the initial fourth velocity moment. This is a generator
  derivative, not a time-evolved halo or a physical SIDM response.

`FINITE_LAG_CONTROLS.md` freezes the controls, sample counts, seeds, lags and
acceptance criteria. `reference-maxwell.json` supplies the earlier full-precision
summary for a direct reproduction check. All outputs retain batch values, input
parameters, software versions, source hashes and analytical predictions. Seeds
are fixed for reproducibility; a repeat with those seeds is not independent
statistical replication. Reported uncertainty across control batches uses four
independent batches, not overlapping time increments as independent samples.

The moving-resonance release below includes provisional measurements and their
explicit qualification limits. A genuinely new-condition3D prediction remains
outstanding; no full-halo or dark-matter conclusion follows from these tests.

## Reproduce the provisional resonance response

`python reproduce_resonance.py --out reproduced-resonance` regenerates two central
contrasts from positive initial populations and32independent paired stochastic
runs. It requires only the same pinned NumPy/Matplotlib environment and normally
takes a few minutes on one CPU. It writes actual saved histories, full summaries
and `response.png`. No initial conditions or private arrays are required.

The s=0.4 collisionless reference missed its separately archived strict quadrature
tolerance. The command reproduces that reported estimate; it does not turn the
failed refinement into a success. The full map, population-width check and new
3D transfer have their own protocols. These finite Gaussian tracer populations
are not full halo DFs, and the imposed white action noise is not physical SIDM.

## Reproduce the matched stationary and moving comparison

`python reproduce_matched.py --out reproduced-matched` regenerates both signs
with the same positive initial population, noise strength and duration. It
recomputes the distribution estimates, the eight stationary positive-weight
trajectory batches, and all4,194,304initial particles in the new moving sample.
Allow roughly45minutes on one CPU. It writes full outputs and
`matched-response.png`, and checks every batch against the archived values.

The exact scientific sources and protocols are in `matched/`. The command uses
no private inputs and runs offline after installing the pinned dependencies.
A fresh isolated environment reproduced all28cases in44.7CPUminutes. Every
batch, distribution contrast and interval agrees within2.8e-17, below the frozen
1e-9 tolerance; all local gates pass. The full receipt is in
`matched/clean-reproduction.json`. This verifies this command and its seeded
inputs; it is not another independent physical sample. Separate numerical-refinement matrices are
documented but not all rerun by this command. This reduced-model sign comparison
does not qualify the3D prediction or a full-halo response.

## Frozen prospective 3D forecasts

The records in `forecasts/2026-09-22/` were committed before inspecting any
held-out Cartesian outcome. Case B predicts a noise-induced mean bar-Lz contrast
of-9.06336507e-6, with a fixed +/-20% operational approximation band. Its local,
refinement and independent reduced-trajectory checks pass. Case A narrowly fails
its independent-sampling prerequisite and remains unqualified; its3Dseed is
unused. The first3D test is statistically unresolved and fails its numerical
qualification. Its mean proximity to the forecast does not establish predictive
success. The exact conditions, failed checks and rules remain unchanged.

## Reproduce the initial 3D qualification test

The optional [transfer package](transfer/README.md) regenerates the original
eight-case Cartesian experiment from seeds, with a pinned, separately built
AGAMA/GSL dependency. It includes the full initial analysis as a reference,
including the failed timestep qualification. The clean build, independent
coordinate test, short unforced smoke and complete eight-case clean rerun pass.
All declared scalar differences are below1.66e-13 and every decision agrees;
individual state arrays retain small differences documented in the receipt.
This is a numerical and physical-model benchmark, not a live-halo or SIDM result.

The same [transfer package](transfer/README.md#reproduce-the-fixed-independent-cadence-confirmation)
now includes the fixed twenty-case independent cadence confirmation. Its short
unforced execution and known-value analysis controls pass; a full clean rerun of
that larger matrix is not claimed.

The separate six-case timestep/cadence rerun also reproduces all decisions in
2.636CPUhours. Its small timestep shifts pass; its cadence intervals still fail.
See the transfer README and full clean numerical receipt. Reproducing the result
does not turn that numerical qualification into a pass.
