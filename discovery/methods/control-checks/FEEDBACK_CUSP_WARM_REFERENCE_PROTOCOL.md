# Frozen proposal: tighter reference on the exact eight warm pilot paths

Prepared2026-10-01 after the failed warm pilot. No trajectories are authorized
by this document. Root source review is required before launching this at-most
50CPU-second block; existing branch allocation remains5CPU hours.

## Question and retained failure

The512-state warm pilot has scientific gate=false. It failed both30% sampling
precision and the independent radial/Cartesian DOP endpoint tolerance1e-7.
The latter is a disagreement between two DOP references, not a KDK-vs-DOP
test. KDK errors separately shrink approximately4x on step-halving. Paths118
and483 dominate reference discrepancy; both were selected beforehand among
four smallestL states and retain zero/tiny physical weights. No path is removed,
and the old failed qualification will never be relabeled.

This block tests whether tighter independent references resolve that specific
discrepancy. It does not sample a population, estimate its heat, qualify unseen
tails, transfer a canonical positive estimator to DOP, or repair sampling.

## Exact inputs and unchanged physics

Anchor pilot result SHA
`e1a0e06d6f1937e3aab2b05281fed0810c2d04970e42820f3f448548fc5c7685`
and saved arithmetic readback SHA
`c72d6b75ce17a595779bd46b362e88367abdd540d29ed5c3110f766bc1de95fc`.
Verify every NPZ/result hash in that readback, plus working and archived
pilot source/helper/protocol/population/variance hashes before adoption.
Use the exact initial states and IDs[67,0,118,483,461,238,130,456]. No RNG,
sampler, action mapper or population change. Retain original Rc,L,r,p and
physical weights, including zero caused by exponential target underflow.

Same actual Hernquist+positive finite gas operator,0/5/8 forward/inverse
physical pulses, amplitude.003,T80. Load the same helper; no force smoothing
or cutoff change. Cartesian orientation remains the exact reference device
inclination.03,azimuth.7 used in the original pilot, not a replacement for
the integrated physical tilt law.

## Independent calculations and frozen gates

Repeat both radial and Cartesian DOP853 for all six maps and eight states,
with rtol2e-12, position/momentum atol1e-14, work atol1e-16,maxstep.04.
The original reference used2e-10/1e-12/1e-14/maxstep.08. Preserve complete
endpoint, energy/work and all Cartesian L-vector operands, old-to-new
individual differences and same-state radial-vs-Cartesian differences.

The new reference block passes only if maximum scaled radius and momentum
disagreements are both<1e-7, maximum scaled all-vector angular-momentum
error<1e-9, and maximum individual absolute energy−work defects in each
formulation<1e-10. Radius scales1+r; momentum scales1+|p|; L scale1+L.
No tolerance adaptation, pruning, zero-weight bypass or alternate target
after outcomes. These are new reference gates; passing them will not pass
the old pilot or establish population accuracy.

## Cost and preservation

One nice10 child with OMP/OPENBLAS/MKL/NUMEXPR threads1. CPU limits45/48
set before NumPy/SciPy; external80+5 wall timeout. After the complete radial
reference, project elapsedCPU+2*radialCPU+4. Stop COST_PARTIAL if>=43CPU.
The old pilot used68.760727CPU including wrapper; this repeats only its
selected reference calculation at tighter settings. No KDK or population
evolution. Reserve50CPU; stop/report at this gate, with no larger draw.

Refuse existing output directories. Snapshot source/helper/scalar/protocol
before calculations; verify hashes and all input operands again at closure.
Save partial receipt before first integration and retain failures. Wrapper
exit and scientific gate are separate receipts. No public deployment.
