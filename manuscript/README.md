# Galaxy Bar: MNRAS-format manuscript

Export 2026-09-24.3 of scientific article 2026-09-24.2. Unreviewed; not
submitted to or accepted by MNRAS. No numerical evidence was changed.

[Download the PDF](galaxy-bar-mnras.pdf) · [Interactive article](https://djova.ca/galaxy-bar/paper.html)

This directory contains the complete generated LaTeX, BibTeX database and four
figures. Retrieve the official MNRAS 3.2 template from [CTAN](https://ctan.org/pkg/mnras),
place `mnras.cls` and `mnras.bst` here, then run:

```sh
tectonic galaxy-bar-mnras.tex
# Or, with a TeX Live installation:
latexmk -pdf galaxy-bar-mnras.tex
```

Verified with Tectonic 0.17.0. For identical PDF timestamps set
`SOURCE_DATE_EPOCH=1790208000` and `FORCE_SOURCE_DATE=1` for the build.
The upstream template archive SHA-256 is
`9d453e272a47648b4418b76577c82c331c0a1499a2a620676d3997f5104adf82`.
Template files retain the RAS LPPL licence. Original project text/code and
derived figures retain the benchmark MIT licence; cited papers retain their terms.

The source-to-LaTeX generator is in
[publication/scripts/manuscript](../publication/scripts/manuscript); it combines
the canonical article with the existing result records. Its template-fetch helper
verifies the complete upstream archive before extraction. See
[build and bibliography notes](../publication/research/publication/mnras/README.md).

The manifest identifies input and output hashes. Input paths resolve relative
to the `publication/` directory. The generated manuscript can be compiled directly
without regenerating the article, running any simulation or accessing private files.

The substantive rewrite is documented in the [editorial repair](../publication/web/diagnostics/communication/EDITORIAL_REPAIR_2026-09-24.md).
It repairs the argument and explanations; it does not change measurements or frozen criteria.
The four figures include a new view of previously released population gradients and kernels.
The seven bibliography entries comprise six research references and the project publication.
Earlier exports remain available under their immutable tags.

To regenerate the gradient figure from released data, run from `publication/`:

```sh
python3 scripts/publication/gradient_figure.py --source web/data/population-response/publication.json --out /tmp/galaxy-gradient-figure
```

This uses NumPy and Matplotlib; it does not evolve any orbits.
