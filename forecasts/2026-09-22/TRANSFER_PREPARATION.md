# Unforced preparation for new-condition 3D forecasts

22 September 2026. Reserve two transfer conditions independent of the first map:
A: Jr=.05,Jz=.05,Js0=.25; B: Jr=.08,Jz=.05,Js0=.25.
For both use bar amplitude .0002, s=.25, eta=.1, T=20 in each condition's own
local libration units, and the positive Gaussian sigma8 with local log slope
from that condition's unforced isochrone DF. Thus A changes sweep history and
bar amplitude from the map, B additionally changes the fast radial action.
These are conditional tracer-population predictions, not full-halo torques.

Measure a,b,phase and slope with no forced trajectory. Repeat the central bar
Fourier coefficient at16³,32³,64³ angles; evaluate nearby coefficients and DF
on Js0+u*j, j=-64..64 in steps2, using32³ angles. Report coefficient/DF slope
variation across the actual swept region and 99.7% initial population interval.
The wider coefficient table supports a separately declared varying-coefficient
resonance diagnostic without extrapolating typical sampled actions. It does not
qualify a constant-coefficient approximation throughout that whole table.
Archive the largest bar harmonics and their frequency detunings to identify
possible non-resonant corrections without fitting a forced outcome.
Require mapping/frequency <1e-10 and central32³-to64³ coupling change<.1%.
Failing preparation prevents a claimed qualified transfer. No action/phase
seeds8301/8302 or forced new-condition outcome may be generated here.

After this unforced preparation, freeze reduced forecasts (positive collisionless
quadrature and noisy DF) and a magnitude adequacy band before any 3D run. The
band is a declared approximation target, not a probabilistic confidence interval.
Sampling intervals and numerical changes must be reported separately. Choose
sample size using reduced-model variance and measured runtime, never the 3D mean.
KDK portable kernel is retained: the exact-background alternative passed short
accuracy checks but was 2.85 times slower at the required comparison settings.
Its archival result remains available as an independent numerical reference.

One single-core nice10 preparation, wall cap300s, only after a worker slot is free.
