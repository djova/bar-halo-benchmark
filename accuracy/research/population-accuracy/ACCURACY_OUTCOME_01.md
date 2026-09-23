# A useful, conservative population-approximation diagnostic

Completed 23 September 2026. The prospective condition was s=0.5, η=0.1,
T=10 and 20, with one fixed fast-action slice, a prescribed bar, and constant
additive action diffusion. These are local response measurements, not total
halo torques or physical SIDM constraints.

## Frozen question and independent result

The diagnostic, positive six-profile family, common windows, error allocation
and numerical forecasts were committed before independent evolution. The
twenty candidate comparisons exclude four halo self-references. All are
correlated through the same dynamical kernel; they are not twenty independent
physical validations.

| Frozen claim or comparison | Independent assessment |
|---|---|
| Eight 5% qualifications: exponential and Gaussian 512 at both endpoints/windows | All eight supported; zero contradicted, zero inconclusive |
| Fifteen qualified signs | All fifteen supported; five other signs were not qualified |
| Twenty population-error allowances | All contain the independently measured paired population error plus its numerical proxy |
| Twelve candidates not qualified for 5% | Eight independently lie outside 5%; four Gaussian 128 cases meet 5% |
| Eight shared-window 5% qualifications | All eight supported against both independently evolved halo windows |
| Four halo self-references | All supported; counted separately |

The four Gaussian 128 cases measure conservatism, not failure of the exact
inequality. An allowance based on absolute contributions can be larger than
the signed error after cancellation. No profiles were dropped, thresholds
relaxed, or numerical ladder extended to obtain these outcomes.

For these four cases, the plug-in absolute-gradient term already exceeds the
frozen 5% target before the explicit kernel uncertainty is added. In the
primary window it is 0.00052005 at T = 10, versus signed error magnitude 0.00009479;
at T = 20 it is 0.00347405 versus 0.00216566. The statement concerns the recorded
mean kernel, whose own uncertainty remains relevant. It identifies loss of
signed cancellation as a source of conservatism, without claiming that the
true kernel or exact future precision is known.

## What the independent calculation measured

Primary physical window: plateau 24, cutoff 40. Values are noise-minus-smooth
accumulated bar transfer in displayed ∫wK_B dx units, at fixed central density.

| Population | T=10 | T=20 |
|---|---:|---:|
| Reference halo in the tested action slice | −0.00884000790 | −0.0661331971 |
| Exponential | −0.00884491869 | −0.0662460699 |
| Gaussian 8 | −0.0396109614 | −0.570685682 |
| Gaussian 32 | −0.0103050984 | −0.0991428226 |
| Gaussian 128 | −0.00893389220 | −0.0682987261 |
| Gaussian 512 | −0.00885047045 | −0.0663743443 |

The independent halo's summed numerical-refinement proxies are 2.3430×10⁻⁶
and 7.6954×10⁻⁵ at these endpoints. Its paired population contrasts have their
own, usually smaller proxies: common discretization shifts must not be
incorrectly treated as independent errors. The complete record retains each
mesh, timestep, numerical-domain and physical-window change.

The intrinsic exponential–halo point discrepancy is 0.0556% at T = 10 and 0.1707%
at T = 20. Gaussian 128 gives 1.062% and 3.274%; Gaussian 512 gives 0.1184% and 0.3646%.
These ratios explain the independently resolved 5% comparisons but are not
certified percentage bounds. The wider physical window gives the same
qualification outcomes. In particular, the very close old s = 0.25 exponential
comparison must not be generalized to sub-0.1% agreement at every dynamics.

The diagnostic qualifies a forecast of the halo response made with the
approximate population. Its total error includes population mismatch and
uncertainty in that approximate response. This differs from the intrinsic
population error measured by independently evolving both populations. The
publication shows both quantities and does not substitute one for the other.

## Numerical and support review

All 14 independently evolved cases completed before analysis, using 8323.741927
worker CPU-seconds. Original frozen source/input hashes and every raw-array
checksum were checked. The unforced noisy control passes its mean, variance
and zero-bar-impulse checks. Mass, positivity and first-moment checks pass in
the forward solver; its boundary mass remains negligible. The characteristic
cases pass path budgets, canonical analytical/assembly controls and the
auxiliary-support bound, including the larger bound needed for negative
fourth-order substeps. No control is inferred from conservation alone.

The central response combines the fine noisy distribution solution with the
finer positive characteristic calculation. Summed absolute refinement changes
are practical error proxies, not mathematically proven truncation bounds.
The independent comparison does not use its outcome to refit the kernel.

The new kernel used 5104.531353 worker CPU-seconds. Kernel construction is real
work; the approximately 0.8-second family contraction is cheap only once that
kernel exists. When the exact reference DF is known, its own contraction is
also cheap. The diagnostic is useful as an audit or compact-representation
test, not as a way to evade knowing the reference gradient.

## Inference and stopping decision

Within this declared family and one new condition, the allowance identifies
safe broad approximations and declines the inaccurate narrow ones, at the
cost of some conservative rejections. This is evidence of practical usefulness
in the specified regime. It does not calibrate a universal Gaussian width,
curvature threshold, simultaneous coverage law or general live-halo correction.
All new-condition population responses are negative. The supported sign
qualifications therefore do not test both physical orderings prospectively;
the earlier opposite-sign counterexample belongs to the separate s=0.25 case.

The exact triangle inequality is elementary. Its sampled implementation uses
approximate Student-t batch coverage and numerical proxies. Successful tests
do not remove those assumptions. Prospective population predictions validate
a reusable computation within externally prescribed dynamics, not a new law
of dark matter. Three-dimensional transfer remains unvalidated.

Scientific production for this test is closed. The complete public-source
reproduction has also passed: eight kernel cases, fourteen independent cases,
162 saved arrays matching exactly, all forecast/qualification outcomes and an
identical regenerated figure. The figure was inspected after completion. No
additional parameter search or Cartesian precision campaign is required to
assess this frozen test. Reproducing the released seeds is software/reproducibility
evidence, not another independent scientific sample. External-review questions
are prepared; no researchers have been contacted.
