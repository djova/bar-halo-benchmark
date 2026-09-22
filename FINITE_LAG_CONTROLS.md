# Finite-lag diagnostic controls — frozen before new control output

22 September 2026. Reproduce the earlier statistic on exact Markov controls,
using the same saved cadence 0.05, endpoint 40, start windows [0,10), [10,20),
[20,32), lags 1, 2 and 4, and population-centered variance (ddof=0).
The range across the nine estimates divided by their mean is compared with 20%.
Each of four independent seeds 8101–8104 has 4,096 independent paths. Overlapping
increments are pooled as in the original; they are not assigned independent SEs.

1. Brownian motion, dJ=sqrt(2)dW, J(0)=0. Exact transition; true D=1, predicted
   pooled estimate 1 for every lag/window. This should pass the flatness screen.
2. Stationary restoring drift, dJ=-0.25Jdt+sqrt(2)dW. Initial N(0,4); exact
   transitions. True D=1, pooled prediction (1-exp(-0.25lag))/(0.25lag).
   Across lags 1,2,4 the exact relative spread is about 32.9%, so flatness must
   fail even though diffusion is constant. Conditional moments separately obey
   E[dJ|J]=(exp(-gamma lag)-1)J and Var[dJ|J]=D/gamma(1-exp(-2gamma lag)).
3. State-dependent Markov control, dJ=0.1Jdt+0.3JdW, J(0)=1. Exact geometric
   Brownian transitions; D(J)=0.045J². This is a mathematical control, not a halo.
   For each starting t, E[dJ]=exp(mu t)(exp(mu lag)-1), and
   E[dJ²]=exp((2mu+sigma²)t)[exp((2mu+sigma²)lag)-2exp(mu lag)+1].
   Average the raw second and mean over the actual starts, then center globally:
   E[dJ²]-E[dJ]². This includes between-start mean differences. Verify the exact
   moment formula against direct transition draws; long-time tail uncertainty is
   reported, not hidden by treating overlap as independent information.

Acceptance: all exact algebraic identities agree to 1e-12; Brownian and OU mean
estimates over four batches within 5% of the exact finite-lag curves and their
screen outcomes agree. For geometric Brownian, use 1,048,576 short conditional transition draws with seed 8105 for the
state J=1 and lag 2; use those
draws for a five-SE analytical check and publish pooled finite-path deviations
without demanding small relative error on a long-tailed sample. Fit OU drift and
innovation variance using only the first window; predict later finite-lag moments
with the exact OU semigroup. This verifies an inference method on a known model,
not its adequacy for the particle-cloud data.

Produce an isolated runnable package with the equations, all batch values,
expected values, checks and a central figure. Preserve old screen fields and
measurements as historical values. Future interpretation must say **flat pooled
finite-lag variance-rate screen**, not general rejection of constant diffusion.
Short-time ballistic behavior of softened gravitational paths rules out blindly
extrapolating the particle diagnostic to lag zero.
