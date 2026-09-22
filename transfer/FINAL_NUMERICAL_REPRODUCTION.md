# Standalone reproduction of the last numerical matrix

22 September 2026, before that matrix is terminal. Package the exact fourth-order
kernel, nested Brownian source, runner and analysis, plus the original frozen
forecast and both numerical protocols. This is a reproduction of unchanged
conditions, not another refinement, new physical model or larger particle sample.

Use a fresh copied standalone source tree and the previously independently built
pinned AGAMA/GSL dependency. State that this reuses that clean dependency build;
it is not a third rebuild. First run the short seed8192 unforced noisy and smooth
smokes. Then regenerate all six original16384-particle cases with seed8302:
candidate dt.01/refinement4, halfstep.005/refinement4, halfcadence.01/refinement8,
each with noise and without it. No original arrays may be inputs to these runs.

Compare against the original terminal analysis only after both matrices finish.
Require identical local and numerical qualification decisions, and differences
below1e-9 for all three candidate means/standard errors/interval bounds and every
reported raw, reduced and discrepancy refinement mean/error/interval bound.
Also compare individual recorded arrays and report their maximum differences;
do not demand bitwise equality from a separately compiled simulation dependency.
The scientific numerical margin remains1.8126730139721574e-7 and is never relaxed
by this reproduction tolerance. A faithfully reproduced failure remains a failure.

Each case retains the7200s wall limit. At most two nice10single-core workers;
with the original matrix's one worker this uses at most three of the four allowed
scientific slots. Allocate up to3.5corehours to this clean reproduction. Ledger04
puts completed map/population/positive-reference/matched sampling work below
2.5corehours, so move3unused map hours to controls/package. Revised ceilings:
controls5,coefficients5,map5,transfer10,diagnosis7,total32unchanged. Expect about
2.6corehours; record actual completed CPU. Existing interruption loss bounds and
the full-population extension's held status remain unchanged.

The optional command may be released as runnable source before its full reference
comparison exists, but must explicitly say the clean full rerun is not yet verified.
Do not overwrite old sources, rerun the original matrix, pool this deterministic
reproduction as independent data, or count agreement as additional physical evidence.
The final fixed-population decision remains a separate resource/power decision,
conditional on the original numerical qualification. Scientific stop/deadline
are unchanged. No timers or services are created.
