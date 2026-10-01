# Reuse and dependency notices

New numerical source, original summaries, manifest and derived compact records
in `discovery/` use the repository's MIT license, copyright 2026 djova. The
licensing follows the existing public benchmark and publication terms. Cite the
pinned scientific release and relevant primary work when reusing the research;
MIT permission is not a claim of scientific priority or independent review.

The three mandatory controls use NumPy, SciPy and Matplotlib. They are ordinary
Python dependencies installed by the user; their implementations and license
files are not vendored here. Exact tested direct versions are in
`requirements.lock.txt`. Preserve the licenses distributed with those packages.

The optional halo sources import AGAMA. No AGAMA or GSL source/binary is copied
into this directory. The separate `transfer/build_linux.py` in the outer
repository fetches pinned sources and applies the existing coordinate patch.
AGAMA's LICENSE states that its own original source has permissive BSD or MIT
terms, and that the GSL-linked library is available under GNU GPL terms. Its
third-party TorusMapper and DOP853 components retain their own notices.
GSL 2.8 retains its upstream GPL license. Preserve all notices and check the
applicable redistribution obligations before sharing a rebuilt library. This
package's MIT file does not replace those terms.

Primary literature is linked and summarized, not redistributed or relicensed.
No observational catalogue is included in this new campaign bundle. The compact
JSON records are outputs of the specified project calculations, with archived
provenance hashes; they are not independent observational data.
