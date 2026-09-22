# Reproduce the completed failed confirmation in the public package

22 September 2026, after the original 20-case matrix and frozen analysis are
terminal, and before any full independent-environment rerun. This is a software
reproduction of the **same** seed 8302 IDs and numerical settings. It adds no
new scientific sample, physical parameter, integrator refinement or qualification
attempt. The original failed confirmation and its stopping decision are fixed.

The earlier PUBLIC_CONFIRMATION_REPRODUCTION.md restricted package development
to smoke checks while the scientific matrix was running, including “Do not launch
another complete confirmation on this host.” This document explicitly supersedes
that restriction for **one exact-sample reproduction**, now that the reference is
complete and its cost is measured. It does not reopen the prohibition against
repeating or enlarging the independent scientific sample to obtain qualification.

Use a new copy of the published standalone source, the previously independently
built patched AGAMA/GSL dependency, and the existing separately pinned Python
environment. No original trajectory array is an input to the run. State clearly
that this reuses an independent build and environment; it is not another fresh
dependency build or a new statistical replication. Source and dependency hashes,
all 20 cases, stable IDs, settings and finite limits must be recorded.

Use three nice=10 single-core workers, a 7200-second wall limit per case, an
aggregate 14 CPU-hour limit, and the unchanged absolute production stop of
23 September 18:46:24 UTC. The public driver's optional stop argument only
shortens its portable default deadline. No host timer or service is created.
Do not automatically repeat or resume a failed or stopped reproduction.

The closed original matrix cost 12.939978 CPU hours. Ledger11 includes it
once, alongside every earlier reported calculation and retained interruption
bounds. Those costs plus the new 14-hour ceiling and a 0.1-hour package/readback
reserve fit below the campaign's 48 scientific core-hour ceiling. The final
eight-hour interpretation and publication reserve is unchanged.

## Comparison fixed before the rerun

Require identical sample coverage, numerical allowance, original forecast hash,
scientific analyzer hash, local/numerical decisions and final qualification
(`false`). For all three aggregate candidate estimators, both interventions'
raw/reduced/discrepancy estimators, and every candidate/refinement/unforced chunk,
require absolute differences below **1e-9** in means, standard errors, interval
bounds and half-widths. This is the same scalar reproducibility tolerance used
in the earlier clean numerical matrix; it does not replace the scientific
1.8126730139721574e-7 allowance. Require exact point/interval decision flags.

Require the complete expected 20-case source-record set and the ten declared
paired chunk/control records with their exact IDs and sizes. Compare all original
and rebuilt raw arrays after both runs terminate and verify their own checksums.
Initial action–angle states, IDs, saved times and event labels must agree exactly.
Report maximum differences in all other arrays, including Cartesian states;
do not claim bitwise identity unless it is measured. Keep rare-path rank changes
descriptive; they are not a reason to alter the primary mean or exclude paths.

The reference checker must reject a missing control, a changed decision or
forecast, a nonfinite interval, and a scalar discrepancy beyond the fixed
tolerance. Verify these software controls without presenting their artificial
inputs as scientific data. Full execution, numerical qualification, scalar
reproducibility and individual-array equality remain separate outcomes.

Publish the original failed scientific result now. Publish the independent
reproduction comparison only when it has actually completed; until then the
public instructions must say that the full clean rerun is pending. Agreement
would verify that another installation can reproduce the failure, not supply
another datum about a bar or validate the outstanding physical forecast.
