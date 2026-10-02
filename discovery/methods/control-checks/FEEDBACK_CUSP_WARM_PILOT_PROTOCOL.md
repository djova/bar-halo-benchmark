# Frozen proposal: finite coeval warm radial-energy pilot

Preparation2026-10-01. SOURCE PREPARATION ONLY is authorized. Root must
review these sources/inputs/physical support before a trajectory launch.
This document requests a bounded600-child-CPU-second pilot within the
existing5-hour branch allocation; it is not launch approval.

## Physical target and fixed sample

Use exactly the analytic Hernquist+positive finite gas model and literal
pulses of the8192-state halo stage: G=M_h=a_h=1, gas mass.1,
scales.2/1.3, cutoff8, static fractions.5; a=.003sin²(pi t/80)cos(omega t)
for0<t<80, omega5 or8; zero case unchanged. Inclination.03 remains the
original normalized Rayleigh pushforward, analytically integrated together
with the two orientation angles for spherical energy. The exact measure is
p_Rc dRc g_L dr dp_r, p_Rc=Rc exp(−Rc), L=Rc vc,
Js=(.1vc)²/kappa, g_L=exp(−Jr/Js)/(2piJs). See the independent
population-equivalence derivation. This is the same intended analytic
population, not the exact discrete old AGAMA realization.

512 NEW IID proposal states, seed201063. q_Rc=.5p_Rc plus.25 truncated
Gaussian with mean the unforced kappa5 radius and std.03, plus.25 truncated
Gaussian at the kappa8 radius and std.015. Both have exact lower0 normal-CDF
normalization. At eachL use the previously tested50/50 radial mixture:
full-support parabolic tail withR=1+Rc and uniform allowedp, plus truncated
lognormal radius stdlog.2 and truncated Gaussian momentum std.1vc.
Retain exact p_Rc/q_Rc and q_L, every component label and generating uniform.
No clipping, resampling, highL/lowL exclusion or sample normalization.

Compute whole stars and guiding cohortsRc<.25,.5,1,2, with their exact
absolute masses1−(1+c)exp(−c). Whole andRc<.25 are principal qualification
gates; all other values are descriptive. Saved initial radial enclosed
fractions at.03,.1,.25,.5,1,2,8 record actual spatial weighting. No density
matching to the stationary central halo tag is claimed.

## Adoption controls before sampling/forcing

Anchor the saved known-map result SHA
`afa914ffca0106d66ea7f589d1fc46ee8a23e7e9790341cdbddeb47ce4992f86`.
Also anchor the independent saved-array readback SHA
`144fe36181030465b098bc700ebf7d59344a144b25e76f821343377de7bd6dc7`
and verify its eight individual initial-array SHA256 values before adoption.
At fixed indices0,17,63,127,255,511 from each of its eight blocks, compare
variableL Jr/Omega/g/difference with the frozen scalar operands. Require
relative Jr/Omega errors<1e-7, absolute g/q difference<1e-7 and energy
difference<1e-12. Preserve every operand and failure.

The new full-support implementation must also includeRc>8. For circles
1e-4,.01,kappa8 radius,kappa5 radius,.25,.5,1,2,6,7.9,8.1,10,100,
check Veff−Ec against independent direct potential subtraction at
r/Rc=.2,.5,.9,1.1,2,4. Require relative error<1e-9 with floor1e-14.
At signed relative radius offsets1e-5 check the local quadratic limit
within1e-4. Static force must match the actual analytic derivative to
1e-12 absolute. The density edge8 has a second-derivative jump; no two-sided
circle-frequency limit is asserted exactly there. No finite neighborhood
of that edge is removed from the continuous target or proposal.

Independently compare the centered gas basis plus its center constant to
the direct physical unit-mass potential difference at1e-6,.001,.01,
kappa8/kappa5 radii,.25,.5,1,2,6,7.9,8,8.1,10,100. Require absolute
centering error<1e-12, interior finite-difference derivative relative
error<1e-5, and exactly zero exterior perturbing force. Retain the edge
derivative diagnostic; its C1 potential is not silently smoothed.

Before forcing, recover guide/radius/momentum generating CDFs with<1e-12
error and frozen5-SE uniform thresholds. Compare phase-weighted mass,
guiding moments2/6, action moments1/2 and every cohort mass with known
physical values using5 empirical SE. Those checks do not certify rare
unsampled tails. Target underflows remain counted and retained.

## Canonical dynamics and saved operands

EachL is fixed. Potential half-kicks and exact free/centrifugal drift
form a radial canonical KDK map. Use all six0/5/8 forward/inverse maps
atdt=.00125/.000625 with one clock reversed for inverses. The helper
handles both gas-circle branches and all crossing orbits. Direct Jr/Omega
integrals use128 points, split at8, with64 root bisections and sin²
turning-point substitution. No interpolation table or epicycle interval.
Negative energy/radicand/bracket failures stop, never clip or resample.

For each map save r,p,initial/final E−Ec,DeltaE, centered external work
and DeltaE−work. The actual forward estimator is the positive primitive
remainder plus inverse E>=0 capture, divided by q_L and multiplied by
p_Rc/q_Rc. Retain32/64 curvature and support arrays, ordinary signed
forward responses and exact matched zero. Actual unsubtract and paired
zero contrast are both reported; a negative contrast is not clipped.
After every full matrix, reverse every numerical map from its endpoint
and retain all-family inverse replay. Require scaled r/p error<1e-9.

For each map/cohort, empirical precision<=30% of the positive paired mean
is required only for the principal two cohorts at both carriers. Compare
all-family fine−coarse paired means within5%. Require mean absolute
target-weighted energy−external-work contributions, including matched
zero defects, within5% of the paired signal. These are sampled necessary
conditions, not omitted-orbit physical error bounds. Require curvature
32/64 and all-family action128/256 paired-mean changes within1%.
Fine/coarse covariance and raw operands remain; no threshold is renamed
after its outcome.

## Independent selected references

Before forcing select four smallestL states plus four distinct random IDs
with seed201064. Record their initial Rc/L/r/E. Evolve all six maps with
both radial and Cartesian DOP853, rtol2e-10, position/momentum atol1e-12,
work atol1e-14,maxstep.08. For Cartesian reference only choose a fixed
orientation with inclination.03 and azimuth.7, with allL components
nonzero; spherical rotational invariance makes its energy identical.
This orientation is a reference device, not a sampled replacement for
the analytically integrated physical tilt law.

Require radial/Cartesian scaled endpoint agreement<1e-7 and all-vectorL
scaled error<1e-9. Original-weight selected partial absolute endpoint-energy
discrepancies, including the zero map, must be<1% of the full paired signal.
These selected partial sums do not estimate or bound omitted paths. No
positive estimator or canonical identity is transferred to DOP maps.

## Finite resources, preservation and interpretive limits

One nice10 child, all four numerical thread variables1. Process limits
560/580 CPU seconds, external700-second wall timeout. After the complete
coarse matrix/remainder/replay, forecast twice that measured block cost
plus120 seconds reserve and elapsed CPU. Stop partial above500 CPU seconds;
the forecast is a gate, not a guarantee. No substitute compiler, target,
proposal, interpolation table or seed after failure. Soft CPU failures
save the partial receipt; hard/time failures preserve prior arrays/logs and
the supervising ledger. Freeze source/helper/protocol hashes before launch
and verify at closure. No automatic larger population or new amplitude.

Set process CPU limits and SIGXCPU handling before NumPy/SciPy imports.
The failure handler may write only a newly created, explicitly owned output
directory, never a pre-existing --out/partial.json. At child start snapshot
the exact launched source, variableL helper, scalar helper, physical protocol,
population-equivalence derivation and variance derivation. Preserve the known
result/readback JSON and all eight initial-NPZ hashes. Verify working sources,
snapshots and those known input anchors on every normal closure, including
CONTROL_FAILED, SAMPLING_FAILED and COST_PARTIAL; record integrity on failure.
The supervisor separately records process exit and saved scientific status/gate.
A normal process exit for a failed scientific gate is not a scientific pass.

The new analytic variance proof bounds the exact physical-flow estimator
using the action-energy comparison and compact physical forcing support.
It does not certify this fixed-step implementation's lowL tails or practical
precision. Passing finite known-map controls does not establish physical
pulse accuracy. All numerical DF/action approximations remain qualified.
The purpose is a bounded finite radial-energy comparison, not radial/vertical
velocity-dispersion survival, a self-consistent core, hydrodynamic affordability
or observational old-disk heating. Root review remains required before launch.
