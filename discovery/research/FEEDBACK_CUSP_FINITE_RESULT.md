# Cuspy feedback: finite central response and retained controls

The specified positive gas redistribution deposits a small finite amount
of energy in a stationary central tag of a Hernquist halo. This result
concerns the halo only. Its coeval warm stellar calculation remains a
weak forecast, so no finite-amplitude stellar/halo cost, core formation
or observational survival bound follows.

## Physical definition

Use G=M_h=a_h=1. The static potential is a Hernquist halo plus two
positive finite-support spherical gas components with total mass.1,
scales.2 and1.3, and common cutoff8. Their fractions are1/2+a(t)
and1/2−a(t). The literal pulse is
a(t)=.003 sin²(pi t/80) cos(omega t) on0<t<80; it vanishes outside.
Frequencies5 and8 use the same spatial redistribution and amplitude.
The finite gas-flow kinetic proxy is larger at8; it is not measured
feedback work.

The halo DF is the separately verified piecewise actual-potential
Eddington table/asymptotic approximation. It is stationary and passive
under the declared approximation; it is not an exact analytic DF.
The smooth binding-energy tag is

g(E)=f(E)[(Ec−E)/(Ec−Phi0)]²/Z for Phi0<E<Ec, and zero otherwise,

with Ec=Phi(2)=−.3798604458002073,
Phi0=−1.2900604555052089 and
Z=.029142109885998378. This tag is not the instantaneous mass enclosed
inside radius2. Energy means below are per normalized tagged mass in
units G M_h/a_h. To express energy per original halo mass, multiply byZ.

## Why the forward estimator is positive

Let F(E)=−integral_E^Ec g(e)de, with F=0 beyond Ec. A cyclic canonical
map M preserves the full phase-volume integral of F. The forward
specific energy is exactly the integral of

R(E,E_M)=−[F(E_M)−F(E)−g(E)(E_M−E)],

plus the inverse-support contribution

−F(E) indicator(E_M_inverse>=Ec).

Concavity of F makes both terms nonnegative. The known inward DF seam
contributes a distributional curvature atom and remains included. This
identity estimates the forward response; it does not average forward
and inverse means. Sampling uses a positive-floor compact proposal
q=.5 delta^(−5/2)W/U+.5/V, delta=E−Phi0, W the tag above.
The inverse map is the actual reversed KDK clock/step sequence.

The normalization128/256 controls give U=2.03257071074436,
V=15.74470986846265 and theZ above, with relative refinements below
1.75e-9. Canonical velocity translations have independently known mean
energy k²/2 by isotropy. They test this proposal/estimator separately:

| Translation k | Known mean | Remainder mean | Empirical IID SE | Inverse Ec captures |
|---:|---:|---:|---:|---:|
|0|0|0|0|0|
|.05|.00125|.001251132|.000011884|1078|
|.2|.02|.020040938|.000192748|4165|
|.8|.32|.323674185|.003243024|18024|

Atk=.8 the inverse-support term contributes.01990497. Omitting it would
change the physical target. These controls validate saved estimator
arithmetic and the specified known maps; they do not validate gas-pulse
trajectory accuracy.

## Finite gas-pulse result

A new8192-state Cartesian IID sample, seed201054, is independent of the
earlier512-state pilot. The pilot failed its precision target and remains
separate. No resampling, clipping or sample-mass renormalization occurs.
The sampled normalized tag mass is1.006602+/- .009767.

| Per tagged mass | Literal frequency5 | Literal frequency8 |
|---|---:|---:|
| Actual forward energy |(1.293895+/- .134428)e-5|(3.843247+/- .439032)e-6|
| Same-state regular weak forecast |(1.646727+/- .188780)e-5|(5.323896+/- .705213)e-6|
| Paired actual minus weak |−(3.528328+/-2.016505)e-6|−(1.480649+/- .742921)e-6|
| Finer-minus-coarser mean / fine mean |+.002168%|−.063388%|
| Largest five states' sample heating share |15.09%|15.53%|

Fine/coarse steps are.000625/.00125. Both frozen15%-SE precision
criteria pass. The zero-map positive energy is
(9.5585+/-4.5311)e-14. Actual forward and matched zero contrasts
remain separate; ordinary signed means, including negative paths,
are retained in the arithmetic package.

The coarse frequency8 weighted energy/work screen fails at8.40%
of the sampled signal. Its fine counterpart passes at2.10%; frequency5
passes at.622%. Energy/work agreement is necessary accounting,
not a bound on orbital phase error. All-state L-vector, inverse replay
and remainder-quadrature screens pass. One frequency5 forward path
crosses Ec; no inverse capture is sampled, and every support term
remains present. Twelve reference states were selected before forcing
from initial energy/radius/L and random rules. Their original-weight
partial endpoint errors pass the frozen checks, but they do not bound
omitted states. Adaptive maps are not used as exactly volume-preserving
population estimators.

The gains are about15.0 and4.45 parts per million of tag binding
energy. The deepest binding-energy cohort supplies essentially none
of the heating. A total tag energy therefore does not imply uniform
heating of the innermost cusp. Actual-minus-weak differences are only
1.75 and1.99 empirical SE: no ensemble nonlinear correction is resolved.
Empirical errors do not certify unseen rare-tail coverage or dynamics
at arbitrarily small radius.

## Inspectable arithmetic

`data/feedback-cusp.json` supplies figure rows, exact normalization,
coarse and fine gates, known-map controls, support terms, source/input
checksums and limitations. `operands/feedback-cusp-v1/` retains every
IID state's arithmetic operands at both steps. The standalone replay
recomputes means, errors, paired differences, weighted work ledgers and
known-map estimates. It does not resample, integrate forces, invert the
DF or evolve self-gravity. See `FEEDBACK_CUSP_REPLAY.md` for axes and
the precise retained-data scope.

Feedback heating and resonant coupling have established antecedents:
[Pontzen and Governato](https://arxiv.org/abs/1106.0499),
[Ogiya and Mori](https://arxiv.org/abs/1206.5412), and
[El-Badry et al.](https://arxiv.org/abs/1512.01235).
The possible contribution is a restricted quantitative selectivity
measurement or cost bound, not discovery of feedback-driven heating.
