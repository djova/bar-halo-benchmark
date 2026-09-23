# Reviewable AGAMA isochrone-coordinate repair

AGAMA is developed by Eugene Vasiliev and contributors:
<https://github.com/GalacticDynamics-Oxford/Agama>.
Retain the upstream source, license and build prerequisites. This directory
contains a proposed source patch and a small Python regression, not an AGAMA
binary or a statement of maintainer acceptance.

The read-only upstream check on 23 September 2026 still finds master at
`f302756b8af2b763db58e278e30478517dc8eea3`, the same revision used by the
existing benchmark. The complete first pages of coordinate-file commit history
and open/closed issue titles contain no later coordinate repair. This bounded
screen does not prove that no related discussion exists. The fresh execution
receipt is required separately; the timestamp of a repository check is not a
new numerical test.

[The bounded upstream history receipt](minimal-reference/upstream-history.json)
records that check.

The fresh four-case execution now reproduces the failure in the unchanged
current revision. Its largest coordinate error is1.895 and largest angle error
is2.233radians. The proposed full patch passes all four checks; the largest
coordinate error is5.56e-16 and angle error4.45e-16. These are deliberately
selected numerical probes, not an error distribution in a galaxy. Both receipts
are preserved in [minimal-reference/original.json](minimal-reference/original.json)
and [minimal-reference/patched.json](minimal-reference/patched.json).
The runs use Python3.11.14, NumPy1.26.4 and mpmath1.3.0. The separate patched
library was built using GCC13.3.0, C++11, -O2, and GSL2.8. Reversing the proposed
patch passes `git apply --reverse --check`; no other source difference is present
in that isolated checkout. This is fresh execution of previously built libraries,
not a claim of a new dependency build during this campaign.

Install the pinned optional dependencies with
`python -m pip install -r optional-agama/requirements.txt`. The existing
[Linux build helper](../transfer/build_linux.py) supplies a separately pinned
GSL/AGAMA build recipe for the patched library. No full transfer simulation is
needed to run this regression.

Build an unchanged checkout and a separate copy with `stable-angles.patch`:

```sh
git apply --check /path/to/stable-angles.patch
git apply /path/to/stable-angles.patch
```

Run the same script separately against each built library, in an environment
with NumPy and mpmath installed:

```sh
python optional-agama/minimal_regression.py --library /path/to/Agama --out original-result
python optional-agama/minimal_regression.py --library /path/to/patched-Agama --out patched-result
```

The four exact inputs have actions `(0.03, 0.02, 0.5)`, vertical and azimuthal
angles `(0.93, 1.37)`, and radial phases at or close to pericentre/apocentre.
The isochrone potential has G=M=1 and scale radius 0.5. All actions are
nondegenerate. The script checks recovered actions, wrapped angle differences,
Cartesian round trips and an independently evaluated 80-digit analytical
coordinate map. The threshold for each is 1e-10 in the stated model units.
An unchanged-library failure is saved rather than hidden behind an exit code.

The patch changes three algebraic operations in `src/actions_isochrone.cpp`:

1. Evaluate the inverse map's half-angle tangent directly, avoiding cancellation
   between two large terms near a radial turning point.
2. Keep the signed radial mean anomaly when recovering the other angles,
   rather than reconstructing it from a wrapped value and a branch subtraction.
3. Evaluate the forward map's half-angle tangent directly, avoiding the loss of
   the branch when rounded cosine equals minus one near apocentre.

The Hamiltonian, actions and physical parameters are unchanged. The existing
larger benchmark also samples 4096 uniform phases and denser turning-phase probes;
this four-case version isolates the regression for review. These deliberately
difficult inputs do not establish its occurrence rate in a galaxy, effects on
a particular physical simulation, or accuracy for all degenerate/limiting actions.
No maintainer has been contacted as part of this campaign.
