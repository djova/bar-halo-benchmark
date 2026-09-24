# Writing an astrophysical argument

Use this reference when constructing or substantially revising a research narrative.
These are our editorial decisions, informed by close reading of selected published
papers. They do not represent a named author's style, advice or approval. The examples
below repair our own earlier Galaxy Bar prose; they illustrate choices, not sentences
to reuse or a mandatory outline for every paper.

## Find the missing reasoning before polishing language

A draft can contain accurate equations, qualified claims and complete references yet
fail to explain the science. First diagnose its argument. For each paragraph, write
privately: what does the reader know on entering; what question is answered; what
new fact or reasoning becomes available; why does the next paragraph follow? If the
only connection is that both paragraphs concern the same topic, reorder or supply
the missing premise. Delete a paragraph that neither advances nor qualifies the
argument; retain its evidence in supporting material when needed.

A dynamical example might develop orbit–perturber interaction → accumulated transfer
→ population weighting → approximation → discriminating test. An observational
paper might instead develop latent property → observable → selection/degeneracy →
inference → independent test. Choose the dependency that the science requires.
Do not impose question headings, a fixed paragraph length or one rhetorical pattern.

**Earlier draft:** an opening sentence about slow orbital phases led straight to
population approximations, followed by unrelated literature summaries and a model
registry. The reader never learned why resonance, sweep and noise belonged together.

**Repair:** establish the physical interaction before introducing the approximation:

> Away from a resonance, an orbit samples different phases of the bar and successive
> torque contributions largely cancel. Near a resonance, the relative phase changes
> slowly, allowing the torque to accumulate. The total transfer therefore depends on
> both an orbit's response and the abundance of orbits with similar initial actions.

The next paragraph can explain what changes when the resonance moves, then what a
specified noise process could change. Cite established mechanisms and distinguish
them from mechanisms demonstrated by the new calculation. A plausible verbal story
is not evidence that the experiment isolated that story.

## Introduce the problem that makes a method necessary

Organize prior work around what is known, how it is known and which unresolved step
motivates this calculation. A paragraph listing several related papers is not yet a
literature argument. Put estimator predecessors beside the estimation problem when
that is where their relevance becomes clear. Use a broader astrophysical analogy
only if it contributes a concrete premise or interpretation; do not add it merely
because it shares a keyword or author.

Explain what an idealization buys. Which interaction is removed, which comparison
becomes possible, and which inference is lost? The answer should justify the setup,
not apologize vaguely for its simplicity.

**Earlier draft:** “The results in this article concern RES-POS,” followed by a
registry of five current and historical model families.

**Repair:**

> We prescribe the bar and the action diffusion, so changing the initial orbital
> population cannot change either force law. This isolates how the initial
> distribution affects the measured transfer. It also excludes collective changes in
> the halo and any feedback of its torque on the bar's pattern speed.

Keep model IDs and the complete registry in the evidence interface. The scientific
setup should be understandable without knowing the project's development history.

## Give equations work to do

Check the reader's prerequisites before introducing notation. Define the physical
object, approximation and relevant scale; then state the equation. Use it immediately
to obtain a sign, limiting case, timescale or reason for another calculation. A list
of symbols after an equation is necessary in many cases but insufficient as an
explanation. Do not repeatedly restate the displayed algebra in words.

For reduced dynamics, explain the physical variables and removed degrees of freedom
before nondimensionalization. Define an angle's physical meaning without equating a
canonical angle to geometric azimuth. Explain the reference width or time behind a
scale, and distinguish a moving coordinate's change from physical momentum transfer.
Use rounded meaningful values in prose; retain full numerical calibration in a
parameter table, derivation or downloadable record.

**Earlier draft:** “The implemented frequency gradient is negative,” immediately
before dimensionless equations and long decimal calibration values.

**Repair:** identify which orbital frequency is differentiated with respect to which
action in the analytical model. Show how its sign enters the phase equation. Then
use the noiseless, stationary limit to identify libration or circulation if that
helps explain the experiment. The code's implementation is not the physical reason
for a sign. Do not invent an interpretation when the derivation is unavailable.

## Develop results through figures, rather than repeat their labels

Give a principal figure one scientific job. Introduce the comparison, direct attention
to a feature that matters, quantify it, and explain the next inference it permits.
A single representative case can orient the reader before a parameter grid. If a
feature challenges the proposed explanation, show the diagnostic that resolves or
preserves that ambiguity. Do not substitute a decorative orbit or density view for
evidence of the relevant mechanism.

The caption must identify the observable, units, changing and fixed conditions,
encoding and uncertainty. Let the prose develop the inference instead of copying
those details in full. An interactive default should carry the same argument as the
static figure; controls investigate additional recorded cases. Neither form should
require interaction to discover the principal finding.

**Earlier draft:** the population result repeated early and late signs in prose, a
claim box and a caption, then deferred explanation to another section.

**Repair:** connect the response to the plotted population gradients and their
kernel-weighted contributions. In the recorded example, the sums
−0.011058 + 0.012565 ≈ +0.001508 and −0.004835 + 0.000934 = −0.003901 show how a
changed balance reverses the net sign. Explain what each contribution represents;
these gradient-integral terms are not literal cohorts of particles. Distinguish
an algebraic account of population sensitivity from evidence for an orbital mechanism.

## Translate internal labels back into operations

Dense noun groups often hide the reasoning that generated them. Ask what was changed,
compared, integrated or estimated, and make that operation the sentence. Preserve a
technical term when it names a necessary concept; do not replace precision with
vagueness or make every sentence artificially short.

- **Before:** “Eight advance 5% qualifications are supported.” **After:** “At the
  second sweep rate, all eight approximations accepted by the error criterion meet
  the specified 5 per cent target in the independent calculation.” State nearby
  that these comparisons share dynamics; they are not eight physical regimes.
- **Before:** “The full allowance combines population mismatch and the approximate
  response's sampling/numerical allowance.” **After:** “We add the estimated error
  from replacing the population to the uncertainty in the kernel calculation.”
  Define the separate mathematical terms and how each is evaluated.
- **Before:** “The transferable product is the recorded kernel, the explicit
  approximation-error calculation and the runnable benchmark.” **After:** conclude
  with what the calculation teaches: matching the gradient at the initial resonance
  can fail because the response samples a finite action interval. Explain which
  approximation succeeds in the tested regime, then link the reusable calculation.

Use the same edit on “combined-proxy assessment,” “operational pass,” and similar
workflow terms. They may remain exact labels in a table or protocol; main prose
should let an outside reader understand their operands and consequence.

## Place uncertainty at the inference it limits

State scope when setting up the model. Put sampling and numerical uncertainty beside
the quantitative result they affect. Discuss untested physical extensions after the
main result has been explained. Refer back instead of repeating every exclusion in
each paragraph. This reduces repetition without strengthening the claim.

Do not hide a decisive limitation in an appendix. Conversely, an earlier campaign's
failed criterion need not interrupt a different current derivation. Preserve that
history in a clearly linked record. Separate numerical sensitivity, sampling error
and model inadequacy; their different meanings should survive any concise wording.
Explain a conservative rejection: losing signed cancellation can make an error bound
unhelpful even when an approximation happens to be accurate.

## Review narrative and publication apparatus separately

Read the abstract, figures and conclusion for a consistent physical claim. Then read
the entire argument in order, without navigation, claim IDs, protocol history or
software receipts. Locate missing premises, redundant conclusions, unexplained
normalizations and paragraphs that report our process instead of the science.
Keep those apparatus elements accessible on the website or in appendices, and make
the PDF a complete argument with its own figure references and captions.

Ask a fresh reader for specific points at which the reasoning fails or requires
unstated knowledge, not a verdict that the paper is impressive or ready. Revise the
argument before the sentence-level pass. Finally, read the sentences in sequence:
subjects and references should remain clear, new terms should follow their premises,
and paragraph endings should make the next step intelligible. Formatting, numerical
verification and mutation-test success do not establish writing quality. Report the
repairs and unresolved questions without predicting a named expert's reaction.

## Source examples and limits of attribution

These particular passages informed the practices above. They are not a comprehensive
bibliography or a count-based measure of editorial quality. Coauthorship does not
identify who wrote a paragraph; even first authorship does not establish that.

- [van den Bosch & Dattathri, 2511.14912v3](https://arxiv.org/abs/2511.14912v3),
  introduction, §2 and §§6.1–6.2: develops resonant gain/loss and a DF gradient before
  the torque equation; later uses matched evolution and DF structure to assess an
  explanation. Its collective SIDM dynamics are not the external-noise model above.
- [van den Bosch & Ogiya, 1801.05427v1](https://arxiv.org/abs/1801.05427v1),
  introduction, §§2.1–2.2 and §3: justifies idealizations, traces stripping through
  readjustment to further stripping, then orients the reader with one case before
  comparisons. Its numerical thresholds must not be imported into another problem.
- [van den Bosch, Lange & Zentner, 1908.07547v1](https://arxiv.org/abs/1908.07547v1),
  introduction, §§2, 5 and 7: motivates an inference method through the information
  and limitations of existing probes; validation tiers specify which assumptions
  are relaxed. Tiers support an inference rather than becoming its main message.
- [van den Bosch, 1611.02657v1](https://arxiv.org/abs/1611.02657v1), introduction
  and §§2.1–2.2: explains how catalogue construction changes the apparent evolution
  being measured. Use this to motivate definitions that affect an inference, not
  to burden an introduction with every internal classification.
