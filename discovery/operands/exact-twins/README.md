# Compact exact-twin saved-response operands

The [manifest](manifest.json) describes eight 512-family NPZ subsets and records
every original input hash and array selection. Each subset contains e, L,
folded positive Lz, common absolute masses, stored sampling density Fq, and the
prograde/full-velocity-reversed impulses for reference and second-frequency
histories. Libraries zero and one additionally carry the four selected
phase/timestep refinements. No phase samples, initial coordinates or movie
arrays are included.

The extraction evaluated Fq once with the archived pinned AGAMA density on
saved actions, without orbit evolution. Public analysis consumes those fixed
numeric density operands; it does not independently regenerate AGAMA sampling
or verify the unsupplied complete trajectory archives. The original hashes
identify those archives rather than matching the smaller released subsets.

For ratio r=F0/Fq and odd weight h=alpha deltaF/Fq, partner weights are
m(r+h)/2 and m(r-h)/2. The minus population swaps them. The reference
uses mr, and the contrast is sum m h (Ipro-Iretro). No population or
library is separately rescaled to unit mass. The frozen positive F0 series
has 96 terms; [frozen-populations.json](frozen-populations.json) supplies
alpha and exact rational positivity operands selected without forced outputs.

## Unforced velocity view

The [velocity export](../../data/twins-velocity.json) supplies the full recorded
257-node azimuthal-velocity marginals at an equatorial position of radius one,
with reference, plus and minus curves for p=4, 6 and 8. Velocity uses the
isochrone reference unit; probability density is per reference velocity. The
escape speed sets the symmetric endpoints. These are equation evaluations,
rather than observed velocities or evolved simulation snapshots.

The [original module](../../source-snapshots/exact-twins/twins_velocity_view.py)
accepts `--frozen` and a fresh `--out` directory. Its inputs are the
[frozen populations](frozen-populations.json), the original exact-moment module,
and the fixed unsoftened isochrone G=M=1, b=0.5. It integrates the same 96-term
positive reference series over the other two velocity components. A separate
64-node quadrature at 17 velocities checks that marginal; 256-node velocity
quadrature checks normalization, first, second and third moments. The recorded
output selections are `/figure/rows` and `/checks` in the scientific export;
their original result and source hashes are retained there.

The original module imports the AGAMA-dependent preflight transitively and is
an inspection source with archived layout assumptions. The public saved-response
replay does not regenerate its velocity quadrature. Hidden third moments describe
the unforced populations; a local marginal alone does not predict their torque.
