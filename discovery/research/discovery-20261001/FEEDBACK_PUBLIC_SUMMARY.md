# A controlled selective-heating example, with a spatial qualification

A prescribed gas fluctuation can give much less energy to mildly warm
coeval stars than to a stationary central halo tracer in this fixed,
initially cored spherical model. The contrast survives direct orbit
evolution, amplitude and timestep controls. It does not demonstrate a
dark-matter core or an acceptable old stellar disk.

The pulse oscillates at frequency 8, above the maximum circular radial
frequency 5.7548. Circular stars barely absorb it, while eccentric halo
orbits and warm stars still couple through higher radial harmonics.
This is a restricted frequency window outside the earlier ten-function
response bound, whose maximum nominal frequency was 5.

The resolved central forward energy is (2.393 ± 0.235)×10⁻⁶ per unit tagged
halo mass. The whole stellar population gains (8.089 ± 1.697)×10⁻⁹ per unit
stellar mass, giving point cost 0.00338. Errors are one family standard
error; radial phase particles are quadrature nodes. A frozen empirical
bootstrap upper-star/lower-central ratio 0.00598 passes the 0.02 sample
usefulness criterion, without certifying unseen continuum tails.

That whole-disk normalization substantially dilutes inner heating. Stars
with guiding radius below 0.25 constitute about 3.5% of the population and
gain (2.153 ± 0.485)×10⁻⁷ per unit cohort mass, giving cost 0.08996. The same
cohort's earlier frequency-5 waveform cost is 2.31294: the frequency-8
reduction is still about 26-fold in this inner group. Neither ratio is an
observational co-spatial stellar-heating bound. The measured inner radial
variance change is about 2.07×10⁻⁷; it is a separate moment diagnostic.

Halving the timestep changes central energy 0.0052%. Halving the amplitude
changes the quadratically rescaled stellar energy -0.098%, but the halo
changes +7.16%, which is retained as finite-amplitude response. An
independent local action derivative accurately predicts the direct warm
response. A positive passive ensemble expression agrees only after
population integration, explaining a preserved finite-sample discrepancy
between the two weak estimators.

The limitations are physically important. The halo tracer is cored and
does not generate the imposed field; the stellar guiding distribution has
a central density hole. Spherical forcing protects angular momenta and
vertical actions. The pulse adds only a few parts per million of the tag's
binding energy, and the tag excludes less-bound orbits that pass through
the center. A finite positive-density gas construction supplies a finite
continuity-flow kinetic budget, but no hydrodynamic feedback engine or
core-energy budget. A cuspy halo with centrally populated stars is the
next independent test.

Feedback heating and resonant coupling are established prior work:
[Pontzen and Governato](https://arxiv.org/abs/1106.0499),
[Ogiya and Mori](https://arxiv.org/abs/1206.5412) and
[Hashim et al.](https://arxiv.org/abs/2209.08631). The present contribution
is a bounded quantitative example and its adversarial controls. The
[scientific export](../../data/feedback.json) retains unrounded outputs,
normalizations, control results and hashes identifying the archived findings.
This release publishes outputs and this summary; it does not regenerate the
feedback orbit ensembles, response matrices or bootstrap. The cuspy extension
is still in progress and has no result here.
