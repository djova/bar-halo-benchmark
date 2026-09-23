# When is a cheap population approximation safe?

Campaign opened 23 September 2026, following the completed population-response
campaign. Its original outputs, thresholds and failed or marginal qualifications
remain unchanged. This is a local computational-methods investigation, not a
new claim about a live halo, observed bar, physical SIDM operator, or total halo
torque. Reference-halo weighting means the isochrone DF in the tested action slice.

## Deliverable and stopping point

Release a focused interactive research note, a review-ready Markdown manuscript,
and a runnable package that explain which population information is needed for
finite-time response. Finish the existing marginal forecast's joint error
assessment, measure estimator efficiency, and evaluate one frozen approximation
diagnostic at one new dynamical condition. Prepare substantive external-review
questions; do not contact researchers without explicit user authorization.

A useful negative outcome is acceptable: an allowance may be too conservative,
or a purportedly safe approximation may fail independent evolution. Neither is
permission to change the criterion or select a different dynamical condition.
No further 3D precision campaign is a dependency.

## Existing evidence first

1. Retain all 24 historical operational forecast decisions. Expand their
   discrepancy intervals by explicitly reported numerical-refinement changes,
   including the paired kernel timestep change. These changes are practical
   diagnostics, not proven error bounds. A failed expanded assessment does not
   erase the original operational pass. Do not refine until the answer passes.
2. Compute paired exponential-minus-halo sampling, timestep, window and
   independent discretization differences. Close point estimates alone do not
   establish sub-0.1% accuracy. Preserve covariance rather than adding separate
   population standard errors in quadrature.
3. Use all eight independent batches at each old sweep for raw-versus-remainder
   variance, paired consistency, and uncertainty. Benchmark actual integration
   and postprocessing costs separately on identical samples. Report projected
   CPU-to-precision only with its fixed-allocation, independent-sample scaling
   assumptions. Include concentrated populations as a stress test; do not assert
   universal variance reduction or infer speedup from variance alone.

## One prospective condition, selected before its population outcomes

The new condition is **s = 0.5, eta = 0.1**, twice the previous moving sweep rate
but below the constant-coefficient locking threshold. Retain the prescribed bar,
T = 10 and 20, fast-action slice, absolute central density and initial log slope.
Compute this condition's own kernel. The old s = 0 or 0.25 kernel is not its
prediction. This is not a new calibration to forced outcomes.

The positive family is halo, slope-matched exponential, and
exp(g*x - x*x/(2*sigma*sigma)) with sigma = 8, 32, 128, 512. Every member has the
same central density and slope. The fourfold width sequence deliberately spans
strong to weak imposed curvature; all members and both times must be reported.
Use the same smooth physical windows, plateau/cutoff 24/40 and 48/64, without
unit-mass renormalization. Numerical domain and auxiliary initial-action support
are separate from the physical window.

## Frozen diagnostic, before any new-condition outcome

For compact weights on a common interval, R[w] = -integral w' Q. The boundary
term vanishes because both weights vanish at the endpoints; the code must check
this. For a candidate approximation v to the halo weight h,

    |R[v] - R[h]| <= integral |v' - h'| |Q|.

This is an elementary triangle inequality, not a new theorem. It becomes an
operational diagnostic only after assessing the estimated kernel and numerical
representation. Do not label its plug-in value a rigorous ensemble bound.

Use eight independent, fresh kernel batches. Preserve each batch's full vector
of population contractions, fine/coarse timestep kernels, and fine/coarse action
mesh contractions. Use a nominal 97.5% simultaneous Bonferroni Student-t envelope
over the finite Q cells at both times and the paired fine-minus-coarse kernels.
Correlations between cells do not invalidate the union bound, but Student-t
coverage for these Monte Carlo batch means is an approximation, not a finite-
sample theorem. Report that assumption and the conservatism of this construction.

The gradient-mismatch allowance is the integral against |mean Q| plus this
sampling envelope, plus the absolute paired timestep-change envelope. Add twice
the measured change on coarsening the kernel representation; also report that
change separately. This numerical addition is a practical refinement allowance,
not a certified truncation bound. Compute it for both physical windows and report
their difference; do not conceal a boundary-sensitive answer with renormalization.

Preserve covariance in scalar contractions. Reserve a further nominal 2.5%
family error for the scalar response and paired timestep intervals of all six
profiles, both times and both windows. Combine simultaneous intervals with the
gradient-mismatch allowance conservatively. Qualify the sign only if the
approximate response interval, expanded by that allowance, excludes zero.
Qualify 5% magnitude accuracy only if the full absolute allowance (including
approximate-response statistical/numerical uncertainty) is below 5% of the
conservative lower absolute halo-response estimate. There is **no absolute floor
that can be mistaken for 5% accuracy**. Near zero, report absolute error and an
unqualified percentage. A shared-window qualification additionally requires the
matched-window response change to fit the same accuracy budget.

Freeze the diagnostic source and complete new-condition numerical forecasts
before independently evolving the new populations. The existing-condition
analysis is developmental evidence; only the new-condition assessment is
prospective. New-condition forecasts must report every family member, including
unqualified ones, with no outcome-dependent threshold or family changes.

## Independent evolution and falsification

Use the established noisy forward distribution solver and independent positive
collisionless characteristics, with action/angle mesh, timestep, domain, physical
window and unforced controls. A complete matrix and its finite cost cap must be
committed before it starts. Use the same positive absolute populations. Test the
predicted error allowances against *paired* independent population contrasts,
including measured numerical errors; also test response magnitudes and signs.
A false qualification is a failure of this diagnostic as implemented, not a
reason to exclude that comparison. Unqualified but accurate cases measure
conservatism. Distinguish them from false qualifications and inconclusive tests.

The criterion need not pass every profile or every time. If it is too conservative
to be useful, publish that result. Any signed derivative correction is exploratory
and cannot replace the frozen primary test or extend this bounded campaign.

## Resource and release guardrails

At most three nice=10 single-thread scientific workers, respecting the sauna job.
24 scientific core-hours total. Initial allocation: 3 hours existing-data analysis,
cost and controls; 4 hours new kernel; 6 hours independent evolution; 3 hours clean
reproduction; 8 hours reserve. Reallocation must be recorded and preserve the cap.
Production stops 2026-09-24 03:35:36 UTC. Final review/publication deadline is
2026-09-24 11:35:36 UTC, leaving eight hours for evidence review and release.
Use finite recorded process queues, no host timers. Stop an infeasible stage using
measured cost and precision, not a promise of future convergence.

The main publication should lead with the useful distinction between a bad
curvature approximation and a successful inexpensive one. Show three figures:
population comparison; kernel-weighted explanation and diagnostic; measured
variance/cost performance. Keep provenance and historical failures accessible
without making them the main scientific argument. Publish and verify both sites,
mobile rendering, the public runnable release, and zero relevant Ansible drift.
