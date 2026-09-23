# Inspect, check, or rerun

These are different activities. Reading starts no computation and needs no credentials. Checking published records is not rerunning trajectories. A reproduction receipt reports what its author checked; it does not mean a reader independently performed it.

## Per-study reproducibility map {#map}

| Study | Published outputs | Analysis reproducible | Complete experiment reproducible |
|---|---|---|---|
| Original 10 / expanded 25 galaxies | Yes: [run index](data/index.json), movies, diagnostics, [catalogue provenance](data/manifest.json) | Selected exported diagnostics and [scientific source](diagnostics/response/source-index.html); coverage varies | **No complete public package for every original galaxy**; some IC/raw archives remain private |
| Prescribed-field Cartesian response | [Recorded paths and budgets](response.html); limitations retained | Named reduced/synthetic checks in [earlier benchmark scope](https://github.com/djova/bar-halo-benchmark/blob/cdb30b5b2f350d2f3de6831995b83f281fe2974e/EARLIER_BENCHMARKS.md) | No blanket claim for every Cartesian/cloud run |
| Matched noisy-resonance benchmark | [Original study](noise-sweep.html) | Yes, named public recipes | [reproduce_matched.py](https://github.com/djova/bar-halo-benchmark/blob/cdb30b5b2f350d2f3de6831995b83f281fe2974e/reproduce_matched.py) for that matched setup |
| Population response and heldout weights | [Population study](population-response.html) | Yes | [reproduce_population.py](https://github.com/djova/bar-halo-benchmark/blob/cdb30b5b2f350d2f3de6831995b83f281fe2974e/reproduce_population.py) and [reproduce_heldout.py](https://github.com/djova/bar-halo-benchmark/blob/cdb30b5b2f350d2f3de6831995b83f281fe2974e/reproduce_heldout.py) |
| Prospective accuracy / matched estimator cost | [Complete article](paper.html), [tables](results/accuracy.json), [arrays](datasets.json) | Yes, retained covariance and exact reference outputs | [reproduce_accuracy.py](https://github.com/djova/bar-halo-benchmark/blob/cdb30b5b2f350d2f3de6831995b83f281fe2974e/reproduce_accuracy.py), cost and retrospective commands |

## Inspection: seconds, no installation {#inspection}

[Article](paper.html) · [Markdown](paper.md) · [claims](claims.json) · [models](models.json) · [datasets and units](datasets.json) · [release manifest](manifest.json). All central tables are in the initial HTML. Controls select recorded endpoints and clarify the calculation.

## Verification: cheap arithmetic, no orbit evolution {#verification}

Download [verify_publication.py](verify_publication.py) and run it with Python3.11, standard library only:

```sh
python3 verify_publication.py --origin https://djova.ca/galaxy-bar/
```

It anonymously fetches the manifest, claims and small result tables, checks hashes and content types, recomputes the late population ratio and prospective counts, identifies a conservative rejection, and reports the broad/narrow estimator ratios. It also checks source-row consistency where supplied. Expected runtime is seconds to a few minutes of network access; no solver is invoked. Network failure is reported, not converted to a scientific failure.

## Reproduction: deliberately run the experiment {#reproduction}

The [public benchmark](https://github.com/djova/bar-halo-benchmark) is separate from the private working repository. Use the pinned numerical version `cdb30b5b2f350d2f3de6831995b83f281fe2974e` and its [exact instructions](https://github.com/djova/bar-halo-benchmark/blob/cdb30b5b2f350d2f3de6831995b83f281fe2974e/accuracy/README.md). Reproduction requires Python3.11, pinned scientific dependencies and available CPU/memory. This command is never run merely by reading the page.

```sh
git clone https://github.com/djova/bar-halo-benchmark.git
cd bar-halo-benchmark
git checkout cdb30b5b2f350d2f3de6831995b83f281fe2974e
python3.11 -m venv .venv
.venv/bin/pip install -r accuracy/requirements.lock.txt
.venv/bin/python reproduce_accuracy.py --out ./accuracy-rerun --workers 2
```

The recorded fresh-source accuracy rerun used **3.60 summed core-hours**; elapsed time and platform equality can differ. The default launcher has finite case/wall limits and4+6 aggregate core-hour ceilings for its two stages. The original cost benchmark used about 347 worker CPU-seconds. The retrospective audit reuses saved arrays. Check each recipe before executing; these costs do not describe the original galaxy simulations.

## Versions, authorship and reuse {#licenses}

Numerical source: `cdb30b5b2f350d2f3de6831995b83f281fe2974e`. Tested accuracy rerun: `66143ebdb7441e17f4b44c23d15c2b35eb66841a`. Publication release: **2026-09-23.2**. Checksums identify the article's exact scientific inputs; publication changes do not silently revise their protocols.

The public benchmark's [MIT code license](https://github.com/djova/bar-halo-benchmark/blob/cdb30b5b2f350d2f3de6831995b83f281fe2974e/LICENSE) is preserved. Original article text, new learning modules and derived result tables included in this clean public release use the same MIT license. Cite the release and underlying papers when reusing the research. This does not license every legacy or third-party item: no new license is asserted over third-party catalogue tables, papers, logos or quotations. Consult the [CDS catalogue](https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/587/A160) and original authors for their terms and attribution.

Project initiated and maintained by [djova](https://github.com/djova). Scientific authorship beyond this project role is not asserted. Analysis, software and exposition were developed with AI assistance; the maintainer is the human contact through the public issue tracker.

[Archived protocols and corrections](archive.html) preserve scientific history. [Release snapshots](releases/2026-09-23.2/manifest.json) and a public Git tag preserve this publication's central evidence. The current manifest is a discovery pointer; cite the versioned files or pinned public commit for a fixed reference.
