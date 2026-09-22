# Matched stationary control for the qualified new-condition family

22 September 2026, before any caseB3Doutcome is available. The old map changes
exposure across sweep rows and uses a different slope from the weak-bar transfer.
Add one finite stationary control: same caseBunforced coefficients, Gaussian
sigma8, ell=-0.004749321154862916, eta=.1 versus0, T20; only s changes from.25to0.
This remains a finite selected population, with no halo-distribution generality.
The already frozen moving forecast and every failed map gate remain unchanged.

Use noisy DF128x2048 and256x4096 on+/-64,dt.025, finehalfstep.0125 and unforced
control. Positive collisionless quadratures256x4096,512x8192,coarsehalfstep and
coarsedouble-domain at fixed action spacing. Require local positivity, mass,
physical moment/unforced checks; all selected changes<5e-5absolute AND<2%of
|contrast| before a resolved numerical interpretation. Otherwise retain failure.
No automatic refinement ladder or change to the existing moving forecast.

Independent paths:8new batches8401..8408,32768independent antithetic pairs each,
using the same drift-kick-drift stochastic algorithm, separately implemented
with paired Brownian leaves. The coarse step sums two fine increments; the
halfstep uses them separately, with the same endpoint random action change. The centered Gaussian q(j) of
width8samples a positive target p(j)=q(j)exp(ell*j-ell^2*sigma^2/2).
For s0the exact reflection(j,psi,W)->(-j,-psi,-W) reverses bar impulse.
Each pair represents two positive weights w+=exp(ell*j-c) andw-=exp(-ell*j-c),
c=ell^2*sigma^2/2. Its weighted bar contrast is Q*sinh(ell*j)*exp(-c).
This is importance sampling of the stated positive Gaussian, not a signed
physical population, fitted correction or changed noise operator. The independent
sample count is32768pairs, not65536orbits. Report normalization estimates without
renormalizing weights, full batch values and Student-t95%interval across8batches.

Verify reflection numerically on256explicit mirrored paths before using it.
Keep separate bar/noise budgets. Repeat these same8batches at halfdt for a paired
stochastic timestep estimate. The independent interval must contain the DF
contrast (unchanged pointwise95%agreement rule); otherwise retain a failed check.
Interpret signs only after separate numerical and sampling qualification.

Ceiling0.75scientific corehours from unused map allocation; finitecasewalllimits,
no more than4combined scientific workers. Start only after transfer workers leave
slots free. This matches a missing scientific control; it does not change either
held-out3Dcondition, select an observed sign or authorize further3Dproduction.
