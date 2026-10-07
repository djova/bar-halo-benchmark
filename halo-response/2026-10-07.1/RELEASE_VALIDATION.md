# Validation and limits of release 2026-10-07.1

This release is an exploratory follow-up to the earlier bar–halo benchmark.
The immutable `runner/README.md` was frozen before its numerical checks and
therefore describes those checks as pending. This file records their subsequent
completion; the historical source is retained rather than silently rewritten.
Neither a successful software check nor publication of this package is an
additional physical sample.

## What can be run independently

`runner/run.py` generates the actions, orbital Fourier coefficients and finite
forcing history for the **bare** response. It needs the pinned NumPy/SciPy
dependencies, not the private campaign archive. Its formula fixture, quick
calculation and reference calculation completed in the campaign. Measured
whole-process CPU times were 0.361, 2.609 and 96.784 seconds respectively on the
campaign host. These are reported execution measurements, not portable runtime
promises. The portable implementation was also compared with the campaign's
bare formula on matched inputs; their scalar differences were approximately
1e-19. That establishes agreement between implementations of the same response
formula, not an independent physical theory or new orbit sample.

The separate exact-positivity packaging and command-line checks completed in
1.505 and 1.123 measured CPU seconds. `runner/verify_certificate.py` checks
the supplied rational certificate for the represented coefficients. Positivity
does not establish response convergence or collective stability.

The quick preset is deliberately coarse. The reference preset is a specified
quadrature, not a certified continuum answer. Refinement must vary action order,
orbital/Fourier resolution and forcing conditions separately. The eight-library
sampling intervals in `results/principal-estimates.csv` belong to the published
trajectory ensemble. They are not sampling intervals for this deterministic
portable quadrature calculation.

## Evidence supplied without a complete collective runner

`results/` contains the selected bare-response records, paired covariance,
finite-amplitude comparison, the represented population coefficients and
certificate, and three static scientific figures. It also contains the
own-field linear collective assessment and its 27 actual population/setting
rows. `results/DATA_SCHEMA.md` defines the quantities and their scope.

The collective values have six recorded settings: the anchor and five
single-axis changes. Their
reported allowances are empirical numerical proxies, not confidence intervals,
rigorous error bounds, a combined finest-resolution corner, or proof of global
stability. A portable collective solver is **not included** in this release;
those results are available for inspection, while the inputs and executable
collective workflow needed for full experiment reproduction are not supplied
by this package. This
distinction is a reproduction gap, not something a checksum can remove.

The independently integrated finite-amplitude comparison supports the active
sign under its supplied uncertainty allowance but fails its original magnitude
qualification. It shares control data with other comparisons and must not be
counted as eight additional independent libraries. A separate fresh
eight-library adaptive confirmation passed its own magnitude and timestep
checks. That does not repair the earlier magnitude failure. These ensembles
retain their distinct estimators and protocols; they are not pooled into
sixteen independent samples.

## Physical meaning

Negative complete-cycle external work means that the specified halo returns
net energy to the external driver while the initial and final external
potentials agree. The reported coefficients multiply the squared weak forcing
amplitude. They do not measure autonomous pattern-speed growth, a live stellar
bar, a full observed galaxy population, or a dark-matter interaction law.

The exact construction preserves density, pointwise zero mean streaming and
the complete velocity-reversal-even distribution. It permits an odd hidden
orbital component; zero mean streaming is not time-reversal invariance. The
positive and negative twins are related by a proper rotation and have the
same unforced spectrum. The calculation does not evade the earlier
collisionless formation restriction from the smooth reference distribution.

The result is not externally reviewed. Prior work already establishes
distribution-function sensitivity and examples of active nonstreaming media;
the narrower question here is whether the stronger matching constraints retain
a resolved complete-cycle response. Specialist priority and applicability
remain matters for independent criticism.

## Inspecting versus reproducing

Reading the JSON, CSV, figures or source launches no calculation. The commands
in `runner/README.md` execute a bounded bare-response experiment. The
certificate command checks an exact mathematical witness; it does not evolve
orbits. `CHECKSUMS.sha256` identifies the release files, not the truth of their
scientific interpretation. Public issue reports can identify a filename,
population, frequency and observable at
https://github.com/djova/bar-halo-benchmark/issues.

The benchmark's existing MIT license applies to this new original code and
data package. No third-party observational catalogue is redistributed here.
