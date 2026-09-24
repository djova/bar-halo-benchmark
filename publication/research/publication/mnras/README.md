# MNRAS-format print companion

PDF export **2026-09-24.3** of the canonical scientific article **2026-09-24.2**.
This is an unreviewed manuscript, not a journal submission or acceptance.
The existing project attribution and AI-assistance disclosure are retained;
no scientific author list or institutional affiliation has been invented.

The official MNRAS 3.2 class and `mnras.bst` provide the two-column journal
layout, equations and author-year bibliography. Four principal figures (including a new view of released gradient/kernel data),
the original six population rows, all 24 accuracy records and all 24 matched
estimator records are included. Longer numerical tables are appendices.
No simulations or physical inference were added.

## Build the document

In the project checkout, run `scripts/manuscript/fetch_template.py` to retrieve
and checksum the unchanged official template, then:

```sh
python3 scripts/manuscript/build.py --pandoc /path/to/pandoc --tectonic /path/to/tectonic
```

The verified tools are Pandoc 3.11 and Tectonic 0.17.0. Tectonic downloads its
TeX dependencies on first use. Neither tool is required for reading the PDF.
The builder uses the canonical ARTICLE.md and published JSON records, not a
separately maintained manuscript narrative. A fixed source date pins PDF metadata.
The generated `.tex`, `.bib` and four figures can also be compiled with
`latexmk -pdf galaxy-bar-mnras.tex` after placing the MNRAS class and style beside
them. The public source release includes that ready-to-compile document.

## Bibliography

Journal metadata were checked against primary pages on 24 September 2026:

- Hamilton et al. 2023, ApJ, 954, 12; DOI 10.3847/1538-4357/acd69b.
  https://www.princeton.edu/~vnd/Hamilton_2023_ApJ.pdf
- Chiba 2023, MNRAS, 525, 3576–3596; DOI 10.1093/mnras/stad2324.
  https://academic.oup.com/mnras/article/525/3/3576/7235089
- Ogilvie & Lubow 2006, MNRAS, 370, 784–798;
  DOI 10.1111/j.1365-2966.2006.10506.x.
  https://academic.oup.com/mnras/article/370/2/784/968223
- Elbers et al. 2021, MNRAS, 507, 2614–2631; DOI 10.1093/mnras/stab2260.
  https://academic.oup.com/mnras/article/507/2/2614/6343051
- Dattathri et al. 2026, The Open Journal of Astrophysics, 9;
  DOI 10.33232/001c.169864; inspected arXiv:2511.11804v2.
  https://arxiv.org/abs/2511.11804v2
- Vasiliev 2019, MNRAS, 482, 1525–1544; DOI 10.1093/mnras/sty2672.
  https://arxiv.org/abs/1802.08239
- The project's pinned canonical publication is cited separately, for seven entries total.

The template and bibliography style are maintained by the Royal Astronomical
Society and licensed under LPPL 1.3 or later. The complete original package is
retrieved from https://ctan.org/pkg/mnras. Original project text/code and derived
tables retain the benchmark's MIT terms; this does not relicense cited papers.

This export substantially rewrites the scientific argument and derives the local
model before discussing its results. The estimator explanation includes its
phase-average argument. Historical audits remain outside the main PDF narrative.
The preceding exports 2026-09-24.1 and 2026-09-24.2 remain unchanged. The editorial
repair record and corrected communication skill are linked from the article.

The gradient figure can be regenerated from the released numerical cells:

```sh
python3 scripts/publication/gradient_figure.py --source web/data/population-response/publication.json --out /tmp/galaxy-gradient-figure
```

This command needs NumPy and Matplotlib. It checks the cumulative sums and
records the source checksum; it does not rerun the physical calculation.
Article generation uses Python dependencies pinned in `requirements.txt`; the
website uses the lockfile in `web/`. The supplied source-to-LaTeX builder should
be run from this clean publication checkout after fetching the template.
