# Anonymous research access

**Current authority:** [canonical article](paper.html) ([Markdown](paper.md)), release **2026-09-23.2**, not externally reviewed. This page describes discovery, not instructions to execute jobs. Reading requires no login, privileged browser, private network or private repository.

Start with [manifest.json](manifest.json), then [claims.json](claims.json), [models.json](models.json), [campaigns.json](campaigns.json), [datasets.json](datasets.json) and the small [results summary](results/summary.json). RFC6901 pointers identify exact source rows. Result files expose units, model and numerical provenance via their dataset entries. Use the same article, uncertainties and limitations as human readers.

## What a cold-start reader should establish

1. Contribution: finite-time population bias plus a reusable diagnostic and estimator in model RES-POS.
2. Nonclaims: no full-halo torque, no calibrated SIDM, no qualified 3D transfer, no universal uncertainty guarantee or runtime speedup.
3. Eight 5% qualifications share **one** new condition, two approximate populations, two times and two windows.
4. Recalculate the late Gaussian/halo magnitude ratio from [the six principal values](results/populations.json); it is about 4.7353.
5. Find Gaussian 128, T = 10, cutoff 40 in [all 24 accuracy rows](results/accuracy.json): the allowance rejects it although its independent error meets 5%.
6. Explain the difference between conditional and between-batch cost-times-variance estimates in [the cost table](results/cost.json).
7. Distinguish prescribed-field test-particle validation from collective live-halo validation using the model registry.

[Inspect/check/rerun map](reproduce.html) supplies separate dependencies and measured costs. [verify_publication.py](verify_publication.py) checks published arithmetic and files; it never evolves an orbit. A project reproduction receipt is not evidence that you reran the experiment. No global all_pass field combines physics, software and deployment.

## Stable references and reuse

Claim IDs, equations, figures, limitations and result IDs are stable within this release. Each principal figure records its default state, scientific parameters, source, full values and analysis hashes in [figures.json](figures.json). A release snapshot lives under [releases/2026-09-23.2/](releases/2026-09-23.2/manifest.json). [llms.txt](llms.txt) is an optional discovery aid, not a guarantee that any service will index this work. [Licenses and contact](reproduce.html#licenses) distinguish benchmark code, scientific records, article and third-party data.
