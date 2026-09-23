# From moving stars to a testable inference

Six short modules lead from the original galaxy views to the current methods result. Each uses the project's actual evidence. The [research article](paper.html) gives the complete argument; the [evidence guide](guide.html) is a directory, not a prerequisite.

## 1. Stars and patterns {#learn-1}

**Prerequisite:** positions, velocities and the idea of an orbit.

A bar is a density pattern. Its stars need not remain together like points painted on a solid rod. In the [galaxy view](index.html#experiment), choose **Follow stars**, then switch between the inertial view and a qualified pattern frame. You are following recorded particle identities, not an artist's animation. A coherent orientation is evidence for a bar; visible elongation alone does not prove resonant trapping.

The galaxy clock is in **Gyr** (billions of years). Density brightness is logarithmic and normalized per frame; a brighter frame is not necessarily a stronger bar. The measured cosine amplitude is a separate quantity.

**Worked example — the factor of two.** If Σ(φ) ∝ 1 + a cos(2φ), the normalized complex coefficient is C₂ = ∫Σ exp(2iφ)dφ / ∫Σdφ. The constant and oscillating fourth-harmonic terms integrate to zero, leaving C₂ = a/2. Thus A₂ = 2|C₂| = |a| for this profile. General positive distributions can have higher harmonics and A₂ above one; A₂ is not a fraction of stars.

**Try:** Does a local A₂ of 1.2 mean 120% of the stars are in the bar?

<details><summary>Reason it through</summary><p>No. It is a cosine-amplitude convention. Its aperture, radial coherence and higher harmonics matter. The observed S⁴G comparison uses a related amplitude convention but not an identical measurement pipeline.</p></details>

[Expert definitions and observational selection](methodology.html) · [Next: orbital populations](#learn-2)

## 2. Orbital populations {#learn-2}

**Prerequisite:** module 1; a probability distribution describes how much material occupies a range of states.

Two galaxies can have similar density profiles but different orbital motions. A distribution function specifies population in phase space, including motion. A selected Gaussian tracer population is a physical modeling choice unless its sampling weights correct it back to the intended DF.

In the local experiment, the **kernel tells us what the dynamics do** at each starting action; the **weight tells us how much material is there**. Reweighting a fixed external response is legitimate because the particles do not change its prescribed field. That separation cannot simply be assumed in a live halo.

**Worked example.** An exponential wE = exp(gx) and Gaussian wσ = exp(gx − x²/(2σ²)) both have w(0) = 1 and w′(0) = g. Their logarithmic slopes are g and g − x/σ². A moving resonance encounters the mismatch away from zero. Same initial slope does not mean same sampled gradient.

[Explore the recorded populations](population-response.html#population-explorer) · [Expert model and normalization](paper.html#model) · [Next: transfer](#learn-3)

## 3. Angular-momentum exchange {#learn-3}

**Prerequisite:** a force can change momentum; module 2.

Torque is the rate of angular-momentum change. Integrating torque over time gives a transfer. In a live isolated galaxy, stars and halo can exchange it. In an imposed-field calculation the source is prescribed, so the test particles' transfer is not a self-consistent history of the bar.

The reduced experiment records the bar impulse B = −∫sinψ dt, separately from the imposed noise and the moving coordinate. The reported response is **Bnoise − Bsmooth**, averaged with a specified population weight.

**Worked example — contrast versus total.** If the smooth bar transfers +10 units to a population and the noisy bar transfers +8, the contrast is −2. Both transfers remain positive; the negative contrast means suppression, not transfer back to the bar. These numbers are an arithmetic illustration, not a simulated result.

[Follow the same recorded orbit and torque](response-coupling.html) · [Expert observable](paper.html#model) · [Next: resonances](#learn-4)

## 4. Resonances and a moving pattern {#learn-4}

**Prerequisite:** periodic motion and module 3.

Weak repeated pushes can accumulate if their phases remain correlated with an orbit. Near a resonance, a particular combination of orbital and bar angles changes slowly. Some trajectories librate around a phase; others circulate. As the imposed bar slows, the resonant action moves. Trapping, crossing and population gradients can then influence transfer.

The local slow-angle equations are dψ = −j dt and dj = (−sinψ − s)dt + √(2D)dW. The term −s shifts the coordinate origin; it is not a physical bar torque. At constant coefficients, a phase-locked solution requires |s| ≤ 1 because |sinψ| ≤ 1. That condition does not say what fraction of a particular population becomes trapped.

**Worked example.** At s = 1.2 no constant phase solves sinψ = −s; at s = 0.25 such phases exist. Neither calculation alone determines the sign of the noise-induced total transfer.

[Recorded resonance trajectories](noise-sweep.html#paths) · [Expert local model](paper.html#model) · [Next: noise and inference](#learn-5)

## 5. Noise and numerical inference {#learn-5}

**Prerequisite:** averages and variance; modules 3–4.

Particle graininess, a chosen stochastic operator and physical collisions are different sources of fluctuations. Changing numerical softening or particle count tests the calculation. Imposing additive Brownian action noise defines a model; it does not calibrate an SIDM cross-section. Conservation checks, convergence checks and a test of model adequacy answer different questions.

**Worked example — a non-flat screen with constant diffusion.** For a stationary Ornstein–Uhlenbeck process dJ = −γJdt + √(2D)dW, constant D coexists with restoring drift. Its increment variance gives:

```text
Var[J(t+τ) − J(t)] / (2τ) = D (1 − exp(−γτ)) / (γτ).
```

At γ = 0.25 and lags 1, 2, 4, this is about 0.8848D, 0.7869D and 0.6321D. It is not flat, despite constant diffusion. Pooled state-dependent drift adds another ambiguity. Short softened gravitational trajectories can instead be ballistic; taking lag to zero is not automatically a diffusion measurement.

**Try:** Are two endpoint times, two windows and two antithetic partners eight independent experiments?

<details><summary>Reason it through</summary><p>No. They share dynamics and random histories. The independent sampling units in the kernel uncertainty are the eight separately seeded batches. Retaining pairing helps estimate contrasts but does not create independence.</p></details>

[Retained correction and synthetic controls](response.html) · [Expert uncertainty](paper.html#accuracy) · [Next: the contribution](#learn-6)

## 6. When does an approximation preserve the answer? {#learn-6}

**Prerequisite:** gradients, signed sums and modules 2–5.

The primitive kernel Qₚ weights the initial population gradient: R[w] = −∫w′Qₚ dx when the boundary term vanishes. An absolute mismatch integral can qualify an approximation. It can also decline an accurate one because taking absolute values destroys useful cancellation.

**Worked example — reconstruct the sign.** The original early Gaussian gives approximately −0.011058 + 0.012565 = +0.001508. The halo gives −0.004835 + 0.000934 = −0.003901. Rounding explains the final displayed digit. These are **gradient-coordinate contributions**, not two literal orbital cohorts. Matching central density and slope did not preserve their balance.

[Inspect Gaussian 128's conservative rejection](paper.html?population=gaussian128&time=10&window=40#interactive-decision). Its independent intrinsic error is within 5%, but its absolute allowance declines to certify it. That is an informative limitation of the rule, not evidence that the recorded response was wrong.

**What has been learned?** Population approximations can change a finite-time answer; some inexpensive approximations work closely here; the kernel can expose the mismatch and assess its error with stated numerical assumptions. The eight supported qualifications share one new dynamical condition. No full-halo or SIDM prediction follows.

[Read the complete article](paper.html) · [Check the evidence yourself](reproduce.html)

## Keep symbols and clocks separate {#notation}

| Model | Symbol or clock | Meaning |
|---|---|---|
| Original galaxy | t in Gyr; positions in kpc | Physical simulation time and distance |
| Original galaxy | Toomre Q | Disc stability parameter; realized baseline minimum ≈ 1.31, target 1.5 |
| Prescribed Cartesian field | Model time and model action | Analytical-potential units; no automatic Gyr conversion |
| Reduced resonance | T, x, j, ψ, s, η | Dimensionless time, initial action, moving slow action, resonant angle, sweep and noise |
| Reduced resonance | Qₚ (Q in earlier records) | Primitive response kernel, unrelated to Toomre Q |
| Reduced resonance | R[w] | Noise-minus-smooth accumulated bar transfer with specified weight |
| All models | An unavailable estimate | Missing or unqualified, never silently zero |

The original particles were sampled from an approximately self-consistent equilibrium model. The softened evolution force differs from the construction potential, so initial adjustment is a documented limitation. A successful local resonance test does not remove that galaxy-model limitation.
