# Prospective s=0.5 kernel, fixed before execution

Apply the diagnostic in PLAN.md and scripts/population_accuracy/diagnostic.py to
one new moving-resonance condition, s=0.5 and eta=0.1. Retain T10/T20 and all
populations/windows in the plan. No independently evolved outcome at this
condition has been inspected to choose the diagnostic or population family.

Use the unchanged positive-step cumulative_paths.py integrator. Eight fresh
batches use seeds96101 through96108. Each uses the *existing* allocation from
research/population-response/validation-allocation-01.json: 1,572,864 independent
initial points in all176 strata spanning[-88,88]. This inherited allocation was
chosen on earlier conditions; it is not optimized using the new outcomes.
Antithetic Brownian partners are correlated. Coarse dt0.0125 and fine dt0.00625
share Brownian leaves. Save both T10 and T20 and exact triangular kernel cell
averages on[-64,64], spacing1/256, plus original raw and remainder controls.

The auxiliary support includes the full cutoff64 plus the maximum bar impulse20.
Its extra sample points do not add physical halo mass. All original local budget,
force-bound and kernel-assembly checks must pass. Do not remove batches, replace
seeds, or enlarge the sample in response to an inconvenient qualification.

Use two nice10 single-thread workers, a four-core-hour aggregate ceiling and a
1800second per-case wall limit, with the campaign's production UTC stop. Prior
measured per-case CPU is about620–686seconds, so eight cases should fit this
allocation with substantial reserve. These are estimates, not runtime promises.

After all eight cases complete, save every frozen diagnostic forecast and commit
it before the independent new-population evolution starts. The latter receives
its own complete registered numerical matrix. If this kernel cannot meet its
guards, publish an incomplete prospective test rather than use partial batches.
