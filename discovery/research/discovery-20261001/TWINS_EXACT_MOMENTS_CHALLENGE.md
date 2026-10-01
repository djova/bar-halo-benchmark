# Independent challenge of the exact-moment halo construction

2026-10-01. Scope: derivation, frozen preflight protocol, archived preflight-02
source and result, and the sampling functions in the earlier orbit libraries.
No forced outcomes, orbit histories or response arrays were opened. No active
scientific script was changed, and no particle/orbit integration was run.

**Finding:** I found no algebraic failure in the all-position streaming
cancellation or global positivity certificate. The equilibrium inference is
valid at the stated unsoftened spherical-model level. Actual exact-population
sampling and live stability remain unverified.

## Attempts to falsify the algebra

I independently derived the velocity-direction integrals. Their coefficients
are \(C_0=8\sqrt2\pi/3\), \(C_1=64\sqrt2\pi/15\), so the ratio \(8/5\)
is correct. Expressing the two remaining powers of \(\Psi\) separately gives

\[
-A_p\mathrm B(p,5/2)+\frac85\mathrm B(p+1,7/2)=0,
\]

\[
B_p\mathrm B(p+1,5/2)-\frac{16b}{5}\mathrm B(p+1,7/2)=0.
\]

Both coefficients evaluate to exactly zero with rational factorial expressions
for each fixed \(p=4,6,8\). This verifies a cancellation at every position,
rather than merely a global spin integral. Radial and polar means vanish by
their separate velocity parity. Full velocity reversal also establishes the
equality of all raw moments of even total degree; because the local means
vanish, their centered counterparts agree as well.

I rebuilt the Eddington-series coefficients directly from factorial Beta
expressions, rather than importing the original recurrence. Coefficients
through \(n=96\) agree exactly with that recurrence. The claimed \(3/4\) tail
ratio holds from \(n=6\); the associated cubic is positive there and has positive
derivative thereafter. Independently differentiating the potential and checking
circular-orbit energy/angular momentum at six radii from \(10^{-8}\) to
\(10^8\), with 70-digit Decimal arithmetic, supports the density formula,
\(r^2(\Psi)\) identity and \(L_{\max}=(1-e)/\sqrt{2e}\). These decimal checks
are finite arithmetic checks, not a replacement for the analytic identities.

## Attempt to falsify the global bound

I reconstructed every polynomial on each of the 256 boxes by direct affine
power substitution and then converted it to the common Bernstein basis. This
does not reuse the original de Casteljau subdivision functions. The denominator
coefficients are positive, with minimum 1. The independent exact maxima are:

- \(p=4:\quad 67/390\).
- \(p=6:\quad 1132034480781204/433439973399677645\).
- \(p=8:\quad 356211155200921020/870472444109974950221\).

All three match the archived rational operands exactly. The ratio-of-positive-
Bernstein-sums argument is applicable here. The 13-term denominator is a lower
bound because all omitted exact DF coefficients are positive. Transforming back
to \(|\delta F|/F_0\) and applying the formal
\(\alpha_p=4/(5\pi^3\mathcal B_p)\) yields the advertised \(1/2\) bound.
The numerical decimal normalization is not itself an interval-arithmetic
certificate; the derivation already correctly distinguishes it from the exact
expression. Rounding near the saturated \(p=4\) escape limit is not evidence
against the positive population construction.

## Equilibrium and sampling boundaries

\(e,L^2,L_z\) are integrals in the specified spherical potential. The DF is
therefore stationary, and its unchanged density sources the same potential.
This supports stationary self-consistency; it says nothing about collective
stability, a live stellar disk, a softened evolution force, formation history,
or forced torque. Spherical density does not make the full handed DF
rotationally invariant.

For a proposal DF \(F_q\) with mass \(M_q\), full phase-space importance
sampling uses weights \((M_q/N)F_\pm/F_q\). If the sampled action library folds
\(L_z\) to \(|L_z|\) and evaluates both time-reversed partners, each partner
instead carries \(M_q/(2N)\) times its respective ratio, followed by the
normalized angle quadrature. The Jacobian from the spherical actions to
\((J_r,L,L_z)\) has unit magnitude; no extra factor of \(L\) should be added
to those canonical-action weights. A sampler using energy and angular momentum
directly would require its own corresponding measure.

The correction \(F_0/F_q\), not only the odd multiplier
\(1\pm\alpha\delta F/F_0\), is necessary to recover the exact reference.
Preserve one absolute mass normalization instead of separately forcing the
two empirical populations to unit mass. The derivation identifies this
requirement correctly. This review did not execute or qualify a new sampler.

## Reproducible readback and small wording recommendations

[Independent readback source](../../scripts/discovery/twins_proof_challenge.py) and
[its operands/results](TWINS_EXACT_MOMENTS_CHALLENGE.json) record the exact
matches, decimal tests and source/protocol hash agreement. The finite readback
used 1.874 CPU seconds inside its measured body, at nice=10; it produced no new
physical sample. It is not a proof-assistant audit or a floating-point error
analysis.

Two quadrature orders in the archived local-moment check are refinements of
one implementation. Describe them as “two quadrature orders,” rather than
implying independent numerical implementations. Likewise, “all even moments”
means all even-total-degree local velocity moments; it is not equality of every
observable or of the complete velocity distribution. Neither point changes the
construction's mathematical result.

## Portable package adapter

The linked script retains the original independent rational and Decimal
algorithms, reads the supplied frozen operands and takes an explicit `--out`.
It checks the archived source/protocol hashes without importing the AGAMA
preflight. Its [released execution](../../reproductions/twins-proof-01/result.json)
passed the three exact bounds and all algebra checks. Optional `--mpmath`
uses mpmath 1.3.0 at 80 digits for an additional alpha evaluation; mpmath is
not required by the rational proof or the response-analysis replay. This
packaging execution is a software/arithmetic check of fixed operands, not
new sampling, orbit evolution, outside review or a stability result.
