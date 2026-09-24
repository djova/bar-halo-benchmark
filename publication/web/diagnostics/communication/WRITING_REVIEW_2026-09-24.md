# How the literature review changed the paper

24 September 2026. Editorial revision of the canonical interactive article and
its MNRAS-format PDF. The numerical records, figures, frozen criteria and retained
failures are unchanged. This review concerns communication; it is not external
scientific review, a priority determination or an endorsement by any cited author.

## Coverage and attribution

We screened **230 arXiv records**, spanning first submissions in 1994–2026, found
through an author search for Frank van den Bosch. We inspected titles and selected
abstract passages across that discovery set, then returned to body passages and
captions in **12 papers**, nine first submitted in 2024–2026. We also visually
inspected three recent figure pages. The [reading ledger](writing-review-2026-09-24.json)
lists every record and distinguishes these depths, with versions and PDF checksums
for the focused material. The earlier 77-paper decade review remains separate.

The search is not a certified complete bibliography. It includes coauthored work,
proceedings, white papers and a physics-benchmark paper. Screening a record is not
reading its whole paper. We gave first-author work particular weight when drawing
conclusions about explanatory choices, and treated the other papers as evidence
of collaborative practice. Authorship order does not reveal who wrote a passage.

The strongest recurring pattern is an argument built around a useful approximation:
why it is made, which information it discards, how that loss changes an observable,
and what a researcher can do about it. This is our synthesis of the inspected
papers, rather than a claim about an author's private intentions. We adapt these
general practices without copying distinctive prose or claiming endorsement.

## What we learned and applied

**Lead with the cost of an approximation.** The recent triaxial-orbit paper separates
the convenience of spherical reconstruction from errors in individual orbits and
population summaries. Our introduction now identifies the analogous question:
which properties of a simplified initial population must survive to preserve
finite-time transfer? “Population bias” is explicitly distinguished from statistical
estimator bias. [Chiang, van den Bosch & Keim, sections 1–3 and figure 4](https://arxiv.org/abs/2608.26249v1).

**Explain the physical balance before the formal estimator.** First-author work
on core dynamics introduces gain/loss and DF structure before the torque formula.
Our article now separates the orbital response from the amount of material at each
starting action before interpreting the kernel integral. The worked cancellation
shows why the Gaussian and halo give opposite early signs. Its terms remain
gradient-coordinate contributions, not literal orbital cohorts.
[van den Bosch & Dattathri, sections 1–2, 4 and figure 12](https://arxiv.org/abs/2511.14912v3).

**Hold the visible structure fixed to expose hidden dynamical information.** The
anisotropic-subhalo and core-dynamics papers illustrate why matching density does
not fully specify a dynamical system. We name exactly what is matched here:
central weight, initial slope, forcing, noise and duration. We distinguish the
physical population from an importance-sampling proposal, and a physical taper
from a numerical boundary. The new scientific citation to the core study states
that its collective mechanisms are absent from our model.
[Chiang et al., methods and figure 3](https://arxiv.org/abs/2411.03192v2);
[Dattathri et al., introduction and discussion](https://arxiv.org/abs/2511.11804v2).

**Explain the successful approximation too.** The Gaussian counterexample is
informative, but the exponential agreement better motivates a usable criterion.
The paper now gives both comparable interpretive weight. Its mathematical
explanation distinguishes a slope at one point from a gradient across the
kernel's region of sensitivity. The very close exponential means remain point
comparisons, not certified sub-0.1% accuracy claims. The general lesson comes
from testing the information retained by a model, as in the BASILISK studies;
the Gaussian/exponential numerical finding is our own recorded result.
[Mitra & van den Bosch, sections 5–8](https://arxiv.org/abs/2510.08421v1).

**Separate verification from adequacy.** The BASILISK validation hierarchy and
the numerical-disruption papers distinguish recovery under assumed rules from
tests of those rules. Our revised text keeps exact kernel identities, measured
qualifications, error proxies and unvalidated extensions separate. The practical
conclusion says when to accept an approximation and when to retain an unqualified
answer; it does not turn eight correlated comparisons into eight physical regimes.
[van den Bosch et al., section 7](https://arxiv.org/abs/1908.07547v1);
[van den Bosch & Ogiya, section 4](https://arxiv.org/abs/1801.05427v1);
[Chiang et al., sections 3–4 and 7](https://arxiv.org/abs/2510.26901v2).

**Make the figure do inferential work.** Recent intervention and model-comparison
figures align the quantity being changed with the consequence being explained.
Our three principal captions now start with the result, then state the observable,
matched settings, units, uncertainty and limits. The efficiency caption separates
measured batch estimates from extrapolated precision curves. No third-party image
is reproduced. [Dattathri et al., section 3.3.2 and figure 5](https://arxiv.org/abs/2606.27480v1).

## Durable skill and publication changes

The reusable [skill snapshot](skill-2026-09-24/SKILL.md) now routes article revisions to
a [writing-craft reference](skill-2026-09-24/references/writing-craft.md), which contains the source
examples and practical paragraph, equation and caption guidance. It complements
the existing interactive-design principles rather than replacing them.

The canonical article now follows question → controlled comparison → response
mechanism → approximation decision → estimator cost → domain → practical
conclusion. The PDF is generated from the same narrative. Both retain complete
results, scholarly predecessors, honest review status and routes to the methods.
Lengthy tables remain expandable on the web and in PDF appendices.

The editorial check is to read the abstract, first result and conclusion alone,
then read the methods alone: both must state the same scope and answer. No new
simulation, new confidence claim, correspondence or submission is part of this
revision. Whether specialists find the contribution original or useful remains
an external scientific question.
