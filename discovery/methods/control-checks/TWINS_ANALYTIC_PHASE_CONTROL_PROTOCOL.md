# Same-sample analytic phase control — frozen protocol 01

1 October 2026. Prepared for source review; **not a launch authorization**.
This is a finite diagnostic control, not a driven-bar or live-halo experiment.
The original single-position completion and all its five-percent flags remain
unchanged. No increase in the 12-CPU-hour twin allocation is requested.

## Question and interpretation

Do the exact finite samples used by the live quiet screen show comparable
shell-moment excursions when evolved in their stationary, unsoftened analytic
construction potential? The continuous F0 and F± distributions are stationary
in that potential, but a finite list of particles need not have stationary
moments in fixed radial shells. Moving shell membership, phases and cylindrical
velocity components can change those moments.

Similar analytic and live excursions support phase/cohort sampling as a
contributor. They do not erase a live flag or establish its false-positive rate.
A live-minus-analytic residual includes softening, tree force, discreteness,
construction mismatch and collective response; it does not uniquely identify
instability. The analytic Hamiltonian is deliberately different from the live
softened Hamiltonian. This control establishes neither stability of the live
halo nor its response to a bar. It provides no SIDM or observational test.

## Immutable inputs and permitted preparation

Source: `scripts/discovery/twins_phase_control.py`. The only permitted initial
operation is its `--prepare` mode. That mode reads and copies files, extracts
the original pure profile arithmetic by AST, and prospectively chooses a small
Cartesian validation subset. It imports no NumPy, SciPy or AGAMA and does not
map or integrate an orbit. `PREPARED` is distinct from `COMPLETE`.

The parent is `results/discovery-20261001/twins/single-position-completion-01`.
Use both exact saved samples with 16,384 single physical positions each:

| Input | SHA-256 |
|---|---|
| `sample-50511.npz` | `4d46b37f8d88d829e5a4a8a14e75ac5f19633b093cb6434345e27618b80a88b4` |
| `sample-50512.npz` | `6dc37b3314056da29e5ff63984985aba67818a2b91b604c1349fef79ae30d723` |
| Original executed completion source | `6bdbc827f17c98f785558debec26047a69238f4fd9b2fc2f57a36ab21fe4e5f6` |
| Original pinned `agama.so` | `f6c04e4941aff3538d3bb08f6446d731b788d85406af94092cf856fbd139d000` |
| Original launch configuration | `f1c26a918ea9bffb3feb17341e0dd93b71d464a4fa71209dbd46c411732c7aee` |

Preserve masses, folded Cartesian states, archived actions, uniforms, thresholds,
stored F0/F+/F− sign choices, fixed radial boundaries, initial family counts and
tracked IDs. No resampling, mass renormalization, recentering, streaming removal,
velocity correction, phase randomization or population change is permitted.
Weakly bound, radial, turning and near-circular paths remain included.

Preparation copies the six completed coarse diagnostic records and their
receipts, validates their time-15 closure and hashes, and freezes their initial
profiles. It copies the exact-moment derivation, population certificate, original
source/native license, resource review and assessment. `FROZEN.json` lists the
copied inputs and the hashes of source, protocol, configuration and AST-method
receipt. `PREPARED-MODULES.json` hashes selected Python interpreter, NumPy/SciPy
native and Python implementation files before scientific imports. This is a
selected module audit, not a claim of a complete dynamic dependency closure.

The original nine-case live matrix must have `COMPLETE`, terminal receipt and
`status=complete` before `--run`. Its numerical qualification may be false:
that does not make this diagnostic question meaningless. Its final result and
receipt are copied into a separately frozen live-closure snapshot **before**
scientific imports. Neither that closure nor this control alters the parent.

## Hamiltonian, angles and exact reversal

Use the original pinned analytic isochrone with G=M0=1 and b=0.5:

\[
\Phi_0(r)=-\frac{1}{0.5+\sqrt{0.25+r^2}}.
\]

Recover canonical angles from the exact folded Cartesian states using the
pinned ActionFinder. Conjugate angles are not geometric azimuths. Check recovered
actions against the archived actions, and use the **archived** actions thereafter.
For the positive-Lz folded population,

\[
L=J_z+L_z,\quad I=J_r+\tfrac12(L+\sqrt{L^2+2}),\quad
\Omega_r=I^{-3},\quad
\Omega_z=\Omega_\phi=\tfrac12(1+L/\sqrt{L^2+2})I^{-3}.
\]

Check these frequencies independently against ActionFinder and ActionMapper.
At each original epoch t=0,0.5,...,15, evaluate the mapper at
theta(t)=theta(0)+Omega*t. The complete reversed branch is x−(t)=x+(−t),
v−(t)=−v+(−t). This reverses every velocity component, not just vphi.
Choose the branch for each population using its stored sign. The initial
profile record uses the exact original Cartesian states; the independently
mapped time-zero state is recorded and checked separately.

## Mapping, profile and independent Cartesian screens

All quantities are checked over the entire sample, with no excluded outliers.
Save recovered actions, angles, frequencies and Cartesian round-trip differences
before evaluating the screens. Record every failed particle ID. Nonfinite
mapping states and failed invariant states are retained as explicit operands;
stop rather than changing or dropping a path.

The prospective maxima are:

| Screen | Normalization | Allowance |
|---|---|---:|
| Recovered action error | sqrt(0.5)+absolute archived component | 1e-10 |
| Frequency error, both APIs | absolute analytic component, floor 1e-30 | 1e-10 |
| Cartesian round-trip position | 0.5+absolute original component | 1e-10 |
| Cartesian round-trip velocity | sqrt(2)+absolute original component | 1e-10 |
| Mapped time-zero pure-profile scalar | 1+absolute original scalar | 1e-8 |
| Every mapped particle energy | 1+absolute initial energy | 1e-10 |
| Every mapped vector angular momentum | sqrt(0.5)+initial vector norm | 1e-10 |
| Selected DOP853/mapper Cartesian components | Same position/velocity scales | 1e-8 |
| Selected DOP853 energy | Same energy scale | 1e-9 |
| Selected DOP853 vector angular momentum | Same vector scale | 1e-9 |

These are new control-specific screens, not rigorous continuum error bounds or
replacements for the old live criteria. Structural/count/coverage differences
in the initial profile comparison fail exactly, even when floating scalar
differences are small.

Extract `tied_quantile` and the original `diagnostic` body up to its live
`budgets(...)` call from the frozen executed source. Its AST prefix must remain
identical. Remove only the live budget field from the return. Preserve the
original fixed shells, weighted quantiles, spherical-harmonic conventions,
cylindrical components, shell-mass normalization, coverage threshold of 256,
shrinking-center diagnostic and inertial origin. The diagnostic center is not
used to recenter the calculation. Exact saved initial states must reproduce
all six original initial pure profiles exactly.

Use analytic single-particle E=v²/2+Phi0 and vector L=x cross v for this control.
There is no one-half self-energy factor. The finite sample's total linear
momentum is not an invariant in an external field. Do not import the live
self-energy or linear-momentum gates.

Prospectively choose Cartesian IDs from initial data alone: the first of each
16-ID original radial-rank validation stratum (eight targets), plus the weakest
binding action, largest initial radius, smallest circularity, smallest initial
absolute radial-velocity fraction and smallest radial-action fraction. First
index breaks all ties; deduplicate while retaining all selection reasons.
Freeze the final IDs and both velocity senses in the launch configuration
before any mapping. No validation ID is chosen from an evolved outcome.

Integrate these selected paths independently in Cartesian coordinates with
DOP853, rtol=2e-11, atol=2e-12, maximum step 0.1 and all 31 original output
epochs. Its force is the analytic derivative

\[
\mathbf a=-\mathbf x\big/
\left[\sqrt{0.25+r^2}(0.5+\sqrt{0.25+r^2})^2\right].
\]

Save its states, mapped counterparts, errors and evaluation counts before
checking their allowances. This independently checks selected mapping paths;
it does not certify every Cartesian path or self-consistent gravitational force.

## Finite resource and prospective profiling rule

Use the original project Python 3.11.14, NumPy 1.26.4, SciPy 1.17.1, the copied
original AGAMA native module, one OMP/BLAS/AGAMA thread and nice=10. No tree
solver or force-opening calculation is needed. Resource limits:

- CPU soft 90 seconds, hard 100 seconds.
- Internal finite wall alarm 170 seconds.
- External timeout 175 seconds, then kill after 5 seconds.
- No new job, cap increase or fallback integrator after closure without review.

There is no measured cost for this exact command yet. Complete both saved-sample
initial mapping checks, then measure the first seed's time-zero and time-0.5
profiles, including all three populations and their actual compact writes. If
Cprefix is that two-epoch CPU cost, the fixed projection is

\[
C_{\rm projected}=C_{\rm already\ used}
  +1.25(60/2)C_{\rm prefix}+10\ {
m CPU\ seconds}.
\]

The second seed setup is already included in CPU used and is listed separately
in the receipt, never double counted. The 60 remaining seed/epoch records
include both seeds' remaining epochs. The ten-second reserve covers the selected
Cartesian checks and closure arithmetic. Proceed only if this projection is
strictly below 90 seconds. Retain an over-budget prefix with finite failed
receipt. The hard cap bounds a poor projection; it does not authorize adaptive
changes or a reduced particle/epoch count.

## Outputs, comparisons and completion meaning

Commit only whole synchronized seed/epoch records for all three populations.
Atomically persist compact selected-star states, full scalar profiles and hashes
after each epoch. Maintain a finite status record. Report the original live
flags unchanged alongside descriptive analytic flags using the same old 5%
threshold. The analytic flags do not acquire a newly calibrated statistical
interpretation.

For each original coarse history, give same-sample live-minus-analytic quantile,
mass and diagonal-second-moment residuals divided by the common **initial**
quantity. Keep shell coverage visible. Do not divide by independently changing
mass conventions or renormalize the samples. All comparisons share a finite
model-time clock; they are not independent ensembles.

`COMPLETE` means that both seeds, all three populations, all 31 epochs, the
frozen selected Cartesian screens and unchanged-hash checks finished. It does
not mean the live halos were stable or their original flags passed. A failed
screen, cost gate, signal or exception writes `FAILED` and a finite terminal
receipt while preserving the last whole synchronized record. An external hard
kill with no terminal receipt remains incomplete and must not be promoted to a
scientific outcome. Raw operands and the untouched original records are retained.

## Reviewed commands

Preparation only, before source review:

```sh
.venv/bin/python scripts/discovery/twins_phase_control.py --prepare \
  --out results/discovery-20261001/twins/analytic-phase-control-01
```

After explicit parent source review and original live terminal closure only:

```sh
nice -n 10 timeout --signal=TERM --kill-after=5 175 \
  .venv/bin/python scripts/discovery/twins_phase_control.py --run \
  --out results/discovery-20261001/twins/analytic-phase-control-01
```

Before launch, persist stdout/stderr to the private output's launch log. Parent
records approval and any private process receipt. This protocol does not itself
authorize launch, a driven experiment, publication, tagging or deployment.
