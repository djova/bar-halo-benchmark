# Data, measures and uncertainty

Two different physical models occur in this release. Their clocks and
normalizations must not be combined.

## Assembly endpoints and sign construction

`runner/inputs/inputs.json` defines four complete endpoints: synchronous and
phase-advanced satellite histories at each of two timesteps, 0.00125 and
0.000625. All endpoints have model time 40. The two timestep pairs reuse the
same original particle clouds; they are not independent physical realizations.
Both satellites are present initially. The phase advance is not a later
injection of a tidally evolved satellite.

Units are G = host mass = host Plummer scale = 1. The time unit is
(b_host cubed / G M_host) to the one-half power; velocity unit is
(G M_host / b_host) to the one-half power. The host has 8,192 particles and
mass 1. Each satellite has 2,048 particles, mass 0.025 and Plummer scale 0.1.
The tree uses P1 softening with epsilon 0.0025 and opening parameter 0.0625.
These construction parameters are inputs, not observed-galaxy predictions.

Each NPZ has exactly four arrays, with no missing values:

| Array | Axes and content | Units |
|---|---|---|
| `xv` | 12,288 particles × [x,y,z,vx,vy,vz] | Model length and velocity |
| `mass` | 12,288 positive physical masses | Host mass |
| `cohort` | 0 = host, 1 and 2 = satellites | Integer label |
| `particle_id` | Stable original identifiers 0 through 12,287 | Integer identifier |

The original whole-system barycentric inertial frame is retained, without a
new recentering, axis rotation, or velocity subtraction. Particle IDs 0–8191
are hosts. No radial, bound-state, or high-contribution selection is applied.
The exact file sizes, dtypes, shapes and hashes are in the input manifest.

For each host particle, h determines probabilities (1+h)/2 and (1-h)/2 for
retaining or reversing its velocity. Mass enters each constraint once.
The 203 fitted rows comprise six global momentum/angular-momentum rows,
162 spatially weighted current rows, and 35 quadrupole-density derivative rows.
`feature_labels` specifies component, radius, polynomial and radial/STF order.
Seven radial profiles and five real symmetric trace-free angular components
define the added rows. Observer profiles are diagnostics in assembly units;
they do not impose a new equilibrium potential.

Held-out rows include intermediate radial windows with additional spatial
harmonics, logarithmic windows, and quadrupole observers rescaled to 0.8 and
1.25. A normalized current residual divides the discrepancy by the sum of the
absolute original particle contributions to that feature. It is **not** a
fraction of a possibly tiny signed mean, a work error, or a confidence bound.

All 16 seeds, 76101601 through 76101616, are retained for both rounding methods.
The same particle identifiers and seeds are used across the states. Seeds are
algorithmic realizations of a fixed state, not new assembly histories.
Balanced rounding has dependent covariance; independent Bernoulli variance
does not describe its full sampling error. Final fractional-particle landing
records and raw constraint errors are retained. Maxima over seeds and features
are descriptive and correlated.

The construction preserves positions, masses, initial raw even velocity
moments and kinetic energy. Central velocity covariance also depends on mean
currents and is not automatically matched. Large reversed fractions or changes
in cubic moments do not measure physically formed hidden memory.

## Assembly summary

`evidence/assembly-T40-two-pair-summary.json` records ordinary initial
differences, host angular momentum, occupation diagnostics and qualifications.
Raw angular momentum is about the original inertial origin. `COM_orbital` is
the host centre-of-mass contribution; `internal` subtracts it. `delta_*`
subtract each arm's own initial value. Contrasts are lagged minus synchronous.
Angular momentum has units M_host times square root of G M_host b_host.
Late-clock vectors retain x, y, z ordering. No quiet-control drift is subtracted
to conceal adjustment. Persistent satellite forces are part of the histories.

## Collective response summary

`evidence/simultaneous-family-summary.json` refers to a separate anchored
spherical equilibrium with G = total background mass = b = 1, including a
positive baryonic monopole of mass 0.1. The imposed quadrupole has pattern speed
0.12, a complete cycle of length 120, and rise/fall durations 12. This clock is
not an age in Gyr or the assembly clock above.

F0 and A label the frozen reference and engineered hidden distributions.
Work and canonical-energy entries are quadratic coefficients in perturbation
amplitude, with energy unit G M_total squared / b. They are not fractional
bar-speed changes. Scalar histories sum both signed azimuthal sectors before
extrema are taken; all seven radial channels remain included.

`work_direct` is cumulative work by the imposed external perturbation,
evaluated directly along the simultaneous own-field response. The stationary
convolution uses the corresponding finite orbit/phase rule. Their difference,
raw canonical-energy-minus-work budget and independently formed field-energy
checks are retained. The field discrepancy norm has square-root-energy units;
it is not a bound on work. Each summary states the actual extremum and time.
`comparisons` gives differences at common clocks, not sampling confidence
intervals. The empirical 1e-6 work scale is a scoped numerical decision rule,
not a rigorous universal bound. Refinement agreement does not establish coverage
or remove shared projection errors.

## Access and provenance

JSON uses explicit Boolean qualifications and labelled arrays/maps. An absent
measurement means unperformed or not included, never zero. Nonfinite values are
not silently replaced. Public projections retain numerical values and record
the hash of the selected original record; operational paths are omitted.
`manifest.json` lists every distributed file with size and SHA256. Original
source/definition hashes, input hashes and per-array port comparisons are in
the runner's extraction and equivalence records.
