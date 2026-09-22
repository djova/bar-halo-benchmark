# Bar–halo response benchmark

A standalone numerical benchmark. No private repository, particle files, AGAMA,
compiled gravity engine or API credential is required. Python 3.11 is the tested
interpreter. Install dependencies once, then the reproduction is offline:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
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
