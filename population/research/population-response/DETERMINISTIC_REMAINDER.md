# Independent deterministic cumulative reference

The independent stochastic validation is already frozen and running. Its sample
and rules do not change in response to this calculation. The deterministic
reference uses the earlier fourth-order Yoshida characteristic flow and the
newly verified cumulative identity, with the same positive physical weights.
No raw Fourier or characteristic failure is retrospectively passed.

First run one moving s0.25 case: initial half-domain160,10240midpoint action
nodes,256midpoint phases, dt0.025, phase chunks of8, saved T10 and T20. Evaluate
the three populations in both declared windows at the same absolute density.
Both raw and remainder impulses are retained. This is a cost/bookkeeping pilot;
its outcome does not by itself qualify the physical contrast.

The negative Yoshida substeps require the rigorous bound
|B|<=T*(2*|Y1|+|Y0|)=88.09657536at T20. Therefore the largest cutoff64 needs
initial coverage beyond152.09657536; the chosen160covers it. Auxiliary points
outside the physical window have zero starting density and add no physical mass.
They are required to evaluate the zero-integral control. The cumulative density
is constant beyond its declared compact support, so no halo-DF extrapolation is
performed at those auxiliary actions.

The short known compact-polynomial identity passes to1.7e-16 with this integrator;
its moment error and the existing fixed-point/free-flow identities pass their
unchanged1e-10limits. Full paths must retain budget error<1e-8, positive physical
weights and the guaranteed impulse/support bounds. These checks do not replace
action/phase quadrature or timestep refinement.

Allow600CPU seconds and300wall seconds for the first case on the one available
nice10 single-thread worker. If it is feasible, freeze a follow-up comparison
with doubled action/phase grids, half timestep and larger auxiliary domain at
the same spacing, for both prescribed sweeps. Each comparison must retain the
original absolute2e-4 target for all physical profiles and both times. For a
noisy-minus-smooth contrast, account for the already measured noisy-grid changes
separately. Never use raw-minus-remainder quadrature differences as independent
sampling intervals.
