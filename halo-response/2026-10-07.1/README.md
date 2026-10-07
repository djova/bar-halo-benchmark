# Hidden halo structure and complete-cycle work

Release `halo-response/2026-10-07.1` is an exploratory follow-up, not externally reviewed. Read the [interactive article](https://djova.ca/galaxy-bar/halo-response) or inspect the records below. This README and [release validation](RELEASE_VALIDATION.md) give the current validation status. The frozen runner's older “draft” and “pending” paragraphs are historical, as explained below.

A stationary halo can match a passive reference's entire initial velocity-reversal-even distribution and have zero current at every position, yet return energy during a prescribed rotating quadrupolar cycle. The selected hidden population has bare fixed-background work coefficient **W₂ = −4.367733872611715 × 10⁻⁶**, with nominal pointwise 95% Student t₇ interval **[−4.650549542380627, −4.084918202842803] × 10⁻⁶**, across eight independent whole orbital libraries. Population controls, probes, time nodes and numerical refinements within a library are paired; they are not additional independent observations. The sampling interval is neither simultaneous coverage nor a numerical error bound.

The construction changes the odd part of the initial distribution while preserving its full even part. A separate exact polynomial identity makes the initial current vanish; oddness alone would not suffice. The exact full-support certificate proves **F₀/2 ≤ F ≤ 3F₀/2**, including weak-binding and radial/circular limits. The two full hidden signs are related by a proper rotation and have the same unforced spectra. Positivity, stationarity and matching do not establish stability or a natural formation route. Different occupation-level volumes and Casimirs can coexist with the same initial energy and ordinary kinematics.

An independently integrated finite-orbit check at **ε = 0.005** supports the negative sign after its raw mechanical allowance, but fails its magnitude-agreement check. Its matched tangent control makes the estimate correlated. A separate fresh eight-library adaptive confirmation passes its own magnitude and timestep checks. It does not make the earlier magnitude failure pass. The principal eight-library estimate and fresh eight-library adaptive check remain separate; no sixteen-library estimate is formed.

The separate linear collective calculation gives each population its own induced gravitational field. At the fixed anchor, F₀ has **W₂ = +1.9460900012728735 × 10⁻⁵**; the selected A+ population has:

| Channel | Actual A+ anchor coefficient | Empirical allowance |
|---|---:|---:|
| Complete-cycle work W₂ | −6.058545271387929 × 10⁻⁶ | 3.6228416429609525 × 10⁻⁸ |
| Accumulated halo impulse J₂ | −6.225750982534571 × 10⁻⁵ | 2.983031655453644 × 10⁻⁷ |

Six recorded resolutions change action quadrature, Fourier support, radial basis or timestep one axis at a time. Their absolute shifts and recorded raw physical residuals add without cancellation; the larger of the two Fourier shifts contributes. These are deterministic empirical proxies, not confidence intervals or rigorous continuum bounds. The combined finest corner has not been tested. All 27 available population rows are retained: five settings contain five populations each, while Fourier64 contains only F₀ and A+. Missing finer-population results are not filled by reweighting. This finite-horizon linear assessment establishes neither global stability nor a nonlinear live halo.

Use **G = M = a = 1**, halo mass 0.9, baryonic mass **Mᵦ = 0.1**, physical source inertia **Iᵦ = 0.1**, **Ω = 0.12**, total cycle **T = 120**, rise/fall **12**, and shape coefficient **0.8**. Time is measured in √(a³/GM), total energy in GM²/a and angular impulse in M√(GMa). W₂ and J₂ multiply ε²; they are not fractional changes in bar energy or spin. The physical source inertia is stated for comparison; its rotation is prescribed here and it is not evolved as a rotor. Complete external work includes both switching and rotation: **Wcycle = Wshape + Ω Jcycle**. Negative halo work means energy returned to the external driver, not autonomous acceleration. No physical-unit or catalogue conversion is supplied.

[Nelson & Tremaine (1995)](https://arxiv.org/pdf/astro-ph/9408068v1) already discussed energy emission by nonstreaming anisotropic haloes coupled to warps. [Chiba & Kataria (2024)](https://arxiv.org/html/2311.07640v2) varied odd distribution structure while retaining the even distribution. The bounded contribution here combines full initial even matching, pointwise zero current, full-support positivity and negative total finite-cycle work. No first-discovery or priority claim is made. This package demonstrates no live stellar disc, observed-catalogue match, SIDM effect or collisionless formation history.

Read and check the public evidence using the [data schema and interpretation limits](results/DATA_SCHEMA.md):

- [Principal figure packet](results/figures.json), [initial hidden-structure figure](results/hidden-orbital-structure.png), [principal cycle and correlated finite-orbit figure](results/cycle-confirmation.png), and [complete principal evidence](results/evidence.json).
- [Actual coefficient vectors](results/coefficients.json), [coefficient certificate](results/certificate.json), and [principal export manifest](results/export-manifest.json). The manifest binds its eleven public payloads; full release checking is documented in the adjacent release validation.
- Numeric CSVs: [principal estimates](results/principal-estimates.csv), [paired libraries](results/paired-libraries.csv), [paired covariance](results/paired-covariance.csv), [binding profiles](results/binding-profiles.csv), and [finite-orbit estimates](results/finite-estimates.csv).
- Separate collective evidence: [records and limits](results/collective-assessment.json), [all 27 numeric population rows](results/collective-assessment.csv), and [six-resolution work/impulse figure](results/collective-assessment.png).

Rerun the **bare** calculation with the six frozen companions: [runner](runner/run.py), [instructions](runner/README.md), [pinned requirements](runner/requirements.txt), [matching and positivity theorem](runner/MATCHING_AND_POSITIVITY.md), [exact certificate](runner/certificate.json), and [certificate verifier](runner/verify_certificate.py). From this release directory, using Python 3.11 or later:

```sh
cd runner
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python verify_certificate.py --output positivity-verification.json
.venv/bin/python run.py --check-formulas --output formulas.json
.venv/bin/python run.py --preset quick --output quick.json
.venv/bin/python run.py --preset reference --output reference.json
```

Each output must be new. Quick is a coarse calculation, not a sign or continuum gate. Reference uses GL128/GL128 actions and radial Fourier modes −64…64; “reference” names a reproducible setting, not a rigorous error bound. The completed reference run consumed **96.783767 CPU seconds** and agreed with the campaign's same-setting bare calculation at about **10⁻¹⁹** in the compared scalars. Exact public proof verification consumed **1.122999 CPU seconds**. These are observed costs, not portable wall-time promises. The runner reproduces the bare deterministic action calculation, not the eight-library sampling interval or the finite-orbit histories. Its extraction from the campaign's method is reproducibility evidence, not a new independent physical experiment.

The original runner README and theorem contain hash-bound pre-validation status paragraphs. They remain unchanged because the certificate binds those source bytes. Their “draft/pending” wording describes the historical validation stage; this README and the release-validation companion supersede that status, without changing the method or its limitations.

The package supplies collective records, component budgets and a static figure, **not a portable collective evolution solver**. An independent collective rerun remains a reproduction gap. Autonomous physical-source qualification and unforced stability require separate evidence; no nonlinear live-halo or autonomous-source history is released here. Report reproduction failures or scientific corrections through the [public benchmark issue tracker](https://github.com/djova/bar-halo-benchmark/issues), identifying the release, command, package versions and sanitized error.
