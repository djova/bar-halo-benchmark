# All-forward elastic laws: prospective full-moment screen

Frozen 1 October 2026 after terminal readback of the previous delta=.05 stage,
before any all-forward A/B operator or evolution outcomes. The previous
campaign has used 4544.37 scientific CPU seconds; inertia uses .604 seconds.
This separate stage retains the combined7200-second ceiling and one nice10,
single-thread scientific worker. No live halo is authorized from its results.

## Operator and scientific target

Law A has c=cos(theta)=0 with probability1/4 and2/3 with probability3/4;
Law B always has c=1/3. Azimuth is uniform and events are exact equal-mass
elastic rotations. Both kernels are positive and reversible. No backward
events or zero-angle null collisions are used.

With sigma_V/m=kappa=.02, angular weights are2/3 and8/9, so the actual
relative-speed-dependent rates satisfy Gamma_B(g)=3 Gamma_A(g)/4 at every g.
Both conditional generators have drift `-Gamma_A*u/4` and raw second tensor
`Gamma_A*g^2*I/12`, derived in [SCATTER_NEXT_SCREEN.md](SCATTER_NEXT_SCREEN.md).
Fourth angular decay differs by53/32. This matches conditional increments
of the linear action J=v_x only. Higher nonlinear energy increments and
three-dimensional halo actions are not matched. This is a controlled gas
operator comparison, not a realistic SIDM differential cross-section.

The old conservative DSMC/force engine is unchanged. A wrapper replaces only
its angular-law sampler and weight. Outputs record engine, wrapper and this
protocol's hashes, plus the inherited protocol hash for provenance. Both laws
use the same exact unordered-pair rate correction. Initial-state pairing is
not common-random-number trajectory pairing.

## Frozen operator and ordinary controls

Operator: seed260510,262144 independent events at fixed u=(1,2,-.5), random
Maxwell centers. Require sampled drift/raw tensor, viscosity and P4 means
within5 analytic sampling standard errors, with1e-12 roundoff allowance.
Require pair kinetic energy and momentum conservation <1e-12 absolute.
Require the derived rate-weighted tensors of both laws to agree with the
same analytic tensor to1e-12. The analytic formula supplies arbitrary-u
matching; the chosen non-axis-aligned u checks sampler implementation.

Ordinary controls: four fresh seeds260511--260514. Equilibrium N8192,T20;
stress N32768,T30 with initial component variances(1.6,.7,.7). Both laws use
cells32,dt=.01,kappa=.02. Apply the original margins unchanged: event rate
within5% of the Maxwell reference; means/component second/speed-second and
speed-fourth moments within5 analytic sampling SE; maximum candidate
probability <.1; energy/momentum residuals <1e-10. Entire normalized stress
B-minus-A pointwise nominal95% four-seed intervals must fit +/- .05 initial
stress. These are pointwise intervals, not simultaneous confidence bands.
If either operator or full-control gate fails, no qualified forcing comparison
is advanced. A physical failed gate is not tuned away.

## Frozen response endpoints

Use N8192,cells32,dt=.01,T40,kappa=.02,omega0=.5, the identical prescribed
moving cosine for both laws. Primary endpoint is the final external impulse
contrast **B minus A, in either direction**. Sixteen independent matched
initial-state seeds supply a nominal95% Student-t interval. An interval
excluding zero selects a refinement; an interval including zero is unresolved,
not proof of no effect. No post-hoc positive-sign requirement is imposed.

- Original/calibration waveform epsilon=.25,sweep=.025,
  fresh seeds260521--260536. This waveform was selected after earlier laws'
  outcomes and is not called a wholly held-out physical regime.
- Second waveform epsilon=.16,sweep=.04,
  fresh seeds260541--260556. Other angular laws have already been tested here,
  but these A/B laws and seeds have no previous outcomes. The A/B comparison
  is prospective and parameters are not fitted to it.

There are two exploratory primary condition endpoints, not a discovery
significance claim. Report the mean, interval and paired-seed output
correlation for each. Instantaneous separatrix-population contrast remains a
secondary snapshot; it cannot rescue an unresolved primary. Report q and
Ncoll but do not treat post-evolution gas distributions as automatically
identical merely because conditional tensors initially match.

For each condition with a resolved primary and passed controls, refine dt/2
and cells64 independently for all16 original seeds, if remaining CPU budget
permits. Preserve the same signed endpoint and report contrast-change
intervals. A signal on all three discretizations is a resolved sign in those
finite experiments, not certified continuum magnitude. If refinements cannot
finish within the cap, label numerical qualification incomplete. No adaptive
sample-size extension, threshold change or parameter optimization follows.

The expected baseline-stage cost is several hundred CPU seconds. A queue
refuses a new job when <60 CPU seconds remain, records capacity interruptions,
and does not duplicate existing outputs. The final canonical findings must
retain every original and new failed/unresolved gate.
