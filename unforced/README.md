# The bar-free operator and its boundaries

This supplements the standalone resonance benchmark with a complete readback of
44 existing controls: 16 original distribution cases, four recorded domain
replacements, and eight stochastic batches at each of three conditions. These
checks do not qualify the forced response or the unresolved three-dimensional
prediction. No new physical sample is added.

From the repository root, with the pinned benchmark dependencies installed:

```sh
python unforced/plot.py --result unforced/reference.json --out unforced-figures
```

This reconstructs both figures from the full-precision recorded moments. It is
arithmetic/figure reproduction, not a fresh simulation of all 44 controls.
`reference.json` retains every batch, original gate and raw-array checksum.
`PROTOCOL.md` states the analytic expectations and sampling scope; `OUTCOME.md`
explains the three original boundary failures and recorded replacements.

The exact historical solver is `resonance.py`, SHA256
`bc1359a145b4ecaeb8dcf026a7c62bfdbbbb28ccbff4b3de6c8524117b6d6db5`.
Its width is hardcoded to 8; it predates the `--sigma` option. Its declared slope
is -0.016531804196572842. Do not silently use a current solver with different
settings. For example, this generates one of the actual bar-free conditions:

```sh
python unforced/resonance.py --out one-bar-free-control --s 0.4 --eta 0.1 --no-bar
```

That command performs a finite simulation and refuses to overwrite its output.
It is not the complete control matrix or a new independent physical sample.
A trajectory batch at the same condition is generated with:

```sh
python unforced/resonance.py --out one-bar-free-batch --s 0.4 --eta 0.1 --no-bar --method trajectories --seed 8201 --n 32768
```

The full design uses distribution sweeps 0,0.1,0.4,1.2 and noise strengths
0,0.01,0.1,1 at the solver defaults, plus four eta=1 domain replacements with
`--J 128 --nj 4096`. The stochastic conditions are (0,0.1), (0.4,0.1), (1.2,1),
each at seeds8201–8208, N32768. Endpoints follow the original T=min(8pi,8/s),
with T=8pi at s=0. Same-seed rows share random prefixes and must not be pooled as
independent conditions. All commands retain the original maximum step0.025.

`review.py` provides the exact full readback used here. It requires the complete
raw collection with the recorded directory names, completion markers and terminal
ledger dictionaries. Use `--root`, `--solver-source unforced/resonance.py`, and
`--out` to select those inputs and a fresh output folder. Those execution records
are not replaced by a claim that the reference JSON regenerates raw trajectories.
The existing `reproduce_matched.py` remains the one-command, independently checked
reproduction of a central forced-response result without private files.
