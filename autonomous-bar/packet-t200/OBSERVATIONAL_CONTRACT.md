# Observations for the autonomous-bar comparison

Frozen preliminary design, 2 October 2026. Public-source access and column
semantics have been checked before new campaign outcomes. This is a contract
for observational confrontation; no synthetic halo-twin result is an
observational validation. In particular, these data do not measure dark-matter
mean velocities, higher odd moments, or the proposed hidden axis.

The primary comparison is the **author-listed 25 Milky Way analogue bars** in
Garma-Oehmichen et al. The 97-object parent catalogue supplies selection
context and a fixed sensitivity comparison. Exact membership is frozen from
the asterisks in the author LaTeX table. Additional data-quality failures
remain reported members with missing measurements; they are not replaced by
galaxies whose bars agree better with the calculation.

## Accessible evidence and exact subset

The [original paper](https://arxiv.org/pdf/2210.11424),
§§4, 6.3–6.4, describes the mass/morphology selection, geometry restrictions,
and subsequent MW comparison. Its nominal MW cuts are deprojected
$R_{\rm bar}<6$ kpc and $190<V_c<290$ km/s, with stricter geometry.
Selection uses photometric geometry, while the final table contains weighted
geometry. The author’s starred list is therefore the selection authority;
applying nominal thresholds to different weighted columns would change it.

The parent selection is SBb–SBc morphology and
$10.3<\log_{10}(M_\star/M_\odot)<11.3$, using NSA masses with $h=0.71$
and a Chabrier IMF. It requires photometric $20^\circ<i<70^\circ$,
$10^\circ<|\mathrm{PA}_{\rm bar}-\mathrm{PA}_{\rm disc}|<80^\circ$,
and accepted TW linearity. The intermediate 55-object quality subset
tightens these to $30^\circ<i<60^\circ$ and
$20^\circ<|\mathrm{PA}_{\rm bar}-\mathrm{PA}_{\rm disc}|<70^\circ$.
The 25 stars add the length/speed cuts above. Geometry and TW quality are
part of the observation selection, and must accompany a model comparison.

The [CSV](https://raw.githubusercontent.com/lgarma/MWA_pattern_speed/main/Tables/Appendix_Table.csv)
and [LaTeX table](https://raw.githubusercontent.com/lgarma/MWA_pattern_speed/main/Tables/Appendix_table.tex)
are downloaded as [manga-appendix-table.csv](literature/manga-appendix-table.csv)
and [manga-appendix-table.tex](literature/manga-appendix-table.tex).
The CSV Git blob is `a370de57901b99f35f1b09c3617d069577fb476f`;
its SHA-256 is
`612686522c19548bda2491c30a81c3451ceb6f0c247a6391adc7a77d58971410`.
The LaTeX SHA-256 is
`ca0ca88aa44737158c8491056509d3e3e6f8fb9ca185277f7946a3d0c62b9e7e`.
These snapshots, not the changing `main` branch, define this campaign.

```text
7495-12704   8088-3701    8312-12702   8320-6101    8324-12702
8444-12703   8450-9102    8486-6101    8552-9101    8597-12703
8656-6103    8715-12701   8940-12702   8978-9101    8983-12701
8983-3703    8984-12704   9028-12704   9029-12704   9046-12702
9502-12703   9867-12704   10213-12705 11017-12704  11963-9102
```

Public [MaNGA DR17 SAS access](https://www.sdss4.org/dr17/manga/manga-data/data-access/)
also permits stellar kinematic maps. One preselected member, 7495-12704,
was downloaded to confirm actual access:
[DR17 MAPS](observational-source/manga-7495-12704-MAPS-HYB10-MILESHC-MASTARSSP.fits.gz).
The HTTP response was 200 and 10,826,752 bytes; its SHA-256 is
`a683643dd1578eecfe490c1aa8a65bc7dd460bf76bcda24f2853b078a3784fd6`.
Its URL is
`https://data.sdss.org/sas/dr17/manga/spectro/analysis/v3_1_1/3.1.0/HYB10-MILESHC-MASTARSSP/7495/12704/manga-7495-12704-MAPS-HYB10-MILESHC-MASTARSSP.fits.gz`.
No FITS arrays were imported or processed during source verification.

The separately metered
[context-ingest-01 check](../../results/autonomous-bar-20261002/context-ingest-01/catalogue_checks.json)
confirms 97 unique CSV/LaTeX IDs, the exact 25 stars, finite values, ordered
intervals and central values consistent with the LaTeX precision in all
checked columns. Its
[completion record](../../results/autonomous-bar-20261002/context-ingest-01/TERMINAL.json)
reports unchanged frozen inputs and 0.078974 measured CPU seconds plus the
runner's explicit five-second closing allowance. The
[frozen 25 rows](../../results/autonomous-bar-20261002/context-ingest-01/manga_25_frozen.json)
and
[97-row membership export](../../results/autonomous-bar-20261002/context-ingest-01/manga_97_membership.csv)
retain the original columns; they do not provide new measured observables.

## Checked catalogue meanings

The [repository README](https://github.com/lgarma/MWA_pattern_speed/blob/main/README.md)
is useful but contains descriptions that must be checked against the table.
For 7977-9102, the CSV gives $\Omega=41.1242$, upper endpoint 46.3656,
and lower endpoint 35.6004. The LaTeX row is $41.1^{+5.2}_{-5.5}$.
For 7495-12704, `bar_med=3.8876` matches the table’s physical
deprojected radius of 3.9 kpc; `bar_dep=5.1204` matches its separate
column labelled arcseconds. Therefore:

| CSV field | Campaign interpretation |
| --- | --- |
| `Gal` | Plate–IFU observation ID; resolve any repeated observation to the underlying MaNGA galaxy ID before population statistics. |
| `nsa_mstar` | Logarithmic NSA stellar mass, not a mass in solar units. |
| `pa_w`, `pa_w_sigma`, `bar_pa`, `bar_pa_e` | Disc/bar position angles and symmetric uncertainty widths, in degrees. |
| `inc_w`, `inc_w_ep`, `inc_w_em` | Weighted inclination and upper/lower interval endpoints, in degrees. |
| `vc_flat`, `vc_flat_err` | Fitted flat-disc circular speed and uncertainty width, km/s. This is not the complete fitted rotation curve. |
| `bar_med`, `bar_upp`, `bar_low` | Physical deprojected bar-radius median and upper/lower endpoints, kpc. These are the length fields used for comparison. |
| `om_med`, `om_upp`, `om_low` | Pattern-speed median and upper/lower endpoints, km/s/kpc. |
| `cr_med`, `cr_upp`, `cr_low` | Corotation-radius median and upper/lower endpoints, kpc. |
| `R_med`, `R_upp`, `R_low` | Dimensionless rotation-rate median and upper/lower endpoints. |
| `rat_vel_sigma` | Actual CSV spelling of the Pipe3D (v/\sigma) quantity. README instead spells it `rad_vel_sigma`; do not silently invent that column. |
| `bar_dep`, `bar_dep_e` | Quarantined legacy fields. Their README description conflicts with the LaTeX column label; never substitute them for the physical `bar_med`. |

Raw endpoints remain in exported data. Error widths, when required for a
plot, are `upper−median` and `median−lower`. A malformed interval is a
failed record requiring diagnosis, not a value to sort or repair silently.
The catalogue provides marginal summaries, not downloadable joint posterior
samples or a full speed–length–corotation covariance. Independent random
draws from invented error curves would not restore that covariance.

## Joint measurement vector

The comparison vector for each recorded model epoch and selected galaxy is

\[
 y=(\Omega_{\rm bar},R_{\rm bar},R_{\rm CR},\mathcal R,
        A_{2,\max}^{\rm light},\sigma_{\rm los,bar},
        \sigma_{\rm los,outer},(v/\sigma)_{R_e}).
\]

Intrinsic $\sigma_R,\sigma_z$ and stellar thickness are also required model
diagnostics, but are not direct entries of this public observational table.
Each observable has a separate availability flag. The joint comparison
retains the complete row and reports which dimensions are unavailable.

**Pattern speed.** The simulation truth uses a coherent inner stellar
$m=2$ phase, $\phi_b=\tfrac12\arg\sum m_j e^{2i\phi_j}$, unwrapped
on saved epochs, with $\Omega_b=d\phi_b/dt$. The chosen radial aperture
and cadence are sealed before confirmation and tested for spiral/nested-bar
contamination. Phase is undefined for a sufficiently weak or incoherent mode;
its speed is missing. The observational comparator uses stellar-light
Tremaine–Weinberg integrals on projected, blurred, coverage-limited stellar
maps. The initial campaign should export both truth and the mock estimator;
catalogue agreement is claimed only for the latter. Shared geometry affects
speed and length together.

**Bar radius.** This is a semi-major-axis radius, never full end-to-end length.
Use a projected light image with a common stellar mass-to-light assumption
and measure isophotal ellipticity/PA, then apply the observational
deprojection. Specifically the paper identifies $R_\epsilon$ at the local
ellipticity maximum and $R_{\rm PA}$ when PA departs by about five degrees;
an earlier sharp ellipticity fall supplies the upper endpoint instead.
Its equations 5–6 set $\mu=\log R_\epsilon$ and
$s=\log\sqrt{R_{\rm PA}/R_\epsilon}$ for the lognormal radius model.
This parametrization places $R_\epsilon$ at the lognormal median even though
the accompanying prose calls it the mean. Apply the same declared rule
to the mock before propagating deprojection uncertainty. Keep the unprojected
mass-based Fourier radius as an independent
latent diagnostic. Its measurement is useful, but substituting it for the
catalogue length would mix definitions. Report the spread from declared
ellipse and phase-coherence alternatives beside any fast/slow classification.
Do not lengthen a bar with connected spiral arms to obtain a preferred ratio.

**Corotation.** Simulation truth solves
$\Omega_c(R)=\Omega_b$ using the midplane radial force of the
azimuthally averaged total potential, $\Omega_c^2=R^{-1}\partial_R\Phi_0$.
Retain all crossings and flag cases lacking an unambiguous crossing beyond
the bar. A spherical $GM(<r)/r$ curve is a different approximation for a
flattened disc. The catalogue's corotation relies on a fitted gas rotation
curve and can require radial extrapolation. Its published `cr_med` should be
retained; recomputing $V_{c,\rm flat}/\Omega_b$ is a separate sensitivity
diagnostic, not a replacement observation. A collisionless simulation has no
synthetic H-alpha tracer, so a gas-estimator match cannot be asserted.

**Rotation rate.** $\mathcal R=R_{\rm CR}/R_{\rm bar}$ is dimensionless.
Use the actual shared estimator and preserve covariance where it is known.
Medians need not obey the ratio of the two marginal medians. Report speed,
bar radius and corotation together: changing $\mathcal R$ can reflect bar
growth without increasing $\Omega_b$. Use the conventional fast interval
$1\le\mathcal R\le1.4$, but retain measurements below 1 and their
uncertainties. These are not removed to enforce a theory prior.

**Amplitude.** Freeze annuli and use

\[
 A_2(R)=\frac{|\sum_{j\in R} w_j e^{2i\phi_j}|}
                   {\sum_{j\in R}w_j}.
\]

Report both mass weighting and light weighting, the complex phase, and the
maximum only within a prospectively defined coherent bar region. This is not
an all-disc cumulative harmonic or the tangential-force measure $Q_b$.
The author CSV supplies no numeric $A_2$. Derive it from public
[Legacy Survey imaging](https://www.legacysurvey.org/dr9/description/)
only after choosing the same band, masks, centre, geometry, radial bins,
point-spread treatment and uncertainty propagation for mock and real images.
An image gallery or visual strong/weak category is not a numeric $A_2$.
No A2 measurements have yet been made for this campaign.

**Dispersion and thickness.** Model truth is the central velocity variance
in sealed radial/vertical bins, subtracting the appropriate local mean:
$\sigma_k^2=\langle(v_k-\langle v_k\rangle)^2\rangle$,
for $k=R,\phi,z$. Store their radial profiles and cross moments as well
as summaries. Define vertical thickness as
$z_{\rm rms}(R)=\sqrt{\langle(z-\langle z\rangle)^2\rangle}$,
with the disc midplane, aperture and tilt recorded. A scale-height parameter
depends on its density law and cannot be renamed $z_{\rm rms}$.

For a possible map extension, freeze projected apertures at
$0.5<R/R_{\rm bar}<1$ and $1.5<R/R_{\rm bar}<2$, keep the full
azimuthal selection, and report coverage before interpretation. A partially
covered outer aperture is missing, not a smaller aperture selected after
viewing the result. The light-weighted mean of within-bin
$\sigma_{\rm los}^2$ is distinguished from a stacked spectrum that includes
ordered velocity variation. Blur luminosity and its first/second raw LOS
velocity moments together before recovering central variance, so unresolved
rotation contributes properly to the mock measurement.

[SDSS's DR17 guidance](https://www.sdss4.org/dr17/manga/manga-data/working-with-manga-data/)
requires DAP masks, repeated-bin/covariance treatment and stellar instrumental
correction using `STELLAR_SIGMA` and `STELLAR_SIGMACORR`. Negative corrected
variance is an unresolved/censored measurement; never replace it with an
observed zero. Apply the documented correction channel and quality bits
after reading the pinned FITS data model. MaNGA LOS dispersion is not
$\sigma_z$, and the existing Pipe3D $v/\sigma$ is not a direct radial
or vertical dispersion. Moderate-inclination photometry in this subset does
not identify intrinsic thickness without a dynamical/photometric model.
Keep thickness and $\sigma_z$ as predictions with observational value
`unavailable`; they cannot contribute a claimed measured residual.

## Inputs, predictions and selection

The present positive-mass rotor has spherical support and an algebraic tail.
Its Plummer scale $a$ is a structural input, not a measured bar semi-major
axis. Its fixed principal PA and nonzero tail contrast do not generally
define a finite ellipse/PA bar endpoint. A chosen enclosed-mass radius would
be a different imposed descriptor. Consequently the restricted rotor
cannot supply the catalogue's bar length, light amplitude, TW stellar
kinematics, dispersion or thickness predictions, or a claimed observed-style
fast/slow ratio computed by substituting $a$ for $R_{\rm bar}$. Its
$\Omega(t)$ and angular-momentum exchange are useful model outputs; the joint
galaxy-bar vector becomes available only with a suitable live stellar model
and its observation operator.

| Quantity | Role in the experiment |
| --- | --- |
| Common initial halo density/potential, local means and even moments | Matched causal controls, independently qualified under the actual force law. |
| Common initial stellar DF, mass profile, Q/dispersion and thickness | Matched baryonic inputs. A resulting bar cannot be credited to the halo when these differ. |
| Initial rotation curve and chosen physical mass/length units | Inputs or scale calibration. Matching these is not a prediction. |
| Rotor density, inertia and prescribed size | Restricted-model inputs. Its geometric length is not a spontaneous live-disc prediction. |
| Composite live-disc $\Omega_b(t),R_b(t),R_{\rm CR}(t),A_2(t)$, stellar dispersion and thickness | Joint dynamical predictions, subject to observation-operator qualification. |
| Observational inclination, distance, PA, PSF, footprint, masks and fitted geometry | Observation-operator inputs with joint uncertainty. |
| Real halo odd DF, hidden axis, bar age, encounter history, gas torque | Unmeasured/modelled latent quantities; not inferred uniquely from a catalogue match. |

Exact spherical matching is stated at preparation start. A common imposed
shape/pattern history may produce different wakes and kinematics before
autonomous release. Those release states must be measured and retained;
they are not exact matched controls merely because their preparation was
common. A fixed analytic halo background also supplies no evolving
collective halo field, even when the particles torque an autonomous rotor.

One common physical similarity scaling must be selected from the declared
mass/length/rotation-curve context before comparing bar outcomes. Its units
obey $\Omega_{\rm phys}=(v_{\rm unit}/l_{\rm unit})\Omega_{\rm sim}$.
Separately fitting speed, radius and corotation to observations would erase
the prediction. Generic tracks at a Milky Way scale constitute context,
not individual-galaxy fits, because the observed present-day profile is not
necessarily the initial profile of the experiment.

Use the author's exact 25 in the main contextual display and all 97 in the
parent display. Model mocks use a sealed grid of allowed viewing geometries,
including the less favourable parent geometry to expose estimator failure.
Carry selection, IFU coverage, bar detectability, TW line-fit quality and
missing spectra/images into the display. A bar-conditioned catalogue cannot
validate a bar fraction. Do not claim isolated systems, gas-poor systems or
known bar ages without additional public evidence. In particular, this
collisionless experiment's omission of gas is a material adequacy limit for
late-type MW analogues.

The primary statistical product should be joint tracks/points and
observable-by-observable residuals with numerical, geometry and measurement
allowances. A formal covariance-weighted multivariate likelihood is deferred
until its covariance is measured or an explicit sensitivity model is frozen.
Marginal overlaps are not joint confidence. Independently sampled model
galaxies, orientations or histories are needed before a model track can
predict a distribution of real galaxy bars.

## Completion and failure reporting

The accessible catalogue allows a real speed/length/corotation confrontation
even if the image or map extension fails. It does not supply a complete
amplitude–intrinsic-thickness comparison. Any final claim must identify the
dimensions actually measured, list missing source coverage, and retain every
qualification failure. Agreement supports conditional model compatibility.
Disagreement may arise from DF response, gas, formation history, scale choice,
numerics or the observation operator and must be localized before attribution.
Neither outcome establishes that engineered twins are a population of real
halos.
