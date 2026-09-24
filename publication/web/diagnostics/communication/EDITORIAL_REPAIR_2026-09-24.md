# Editorial correction: restoring the physical argument

24 September 2026. Applies to article release 2026-09-24.2 and MNRAS export 2026-09-24.3. This is an account of our editorial decisions, not a representation of any researcher's style or approval.

## What went wrong

The previous writing pass improved terminology while leaving the wrong structure intact. The draft had accumulated accurate statements in response to successive checks, but its paragraphs did not develop a continuous scientific argument. Internal model codes, claim boxes, historical qualifications and reproduction counts interrupted the explanation. Some important methods were missing while less important audit details were repeated.

The skill contributed to that failure. It listed desirable qualities—physical intuition, controlled comparisons, bounded inference—without requiring the work that produces them: tracing paragraph dependencies, deriving the model in the reader's notation, explaining a figure and editing abstract noun groups back into operations. Screening a large bibliography did not establish that this work had been done. Neither numerical consistency checks nor successful PDF rendering justified our confidence in the prose.

We also gave the source readings too much personal authority. The skill is our workflow. It does not reproduce a named author's voice, imply that he wrote particular coauthored passages, or predict his judgment of the result. The current skill states that distinction directly.

## The new close reading

The focused comparison examines connected introductions and methods/discussion sequences, rather than collecting abstract-level themes. Its main first/sole-author examples are:

- [van den Bosch & Dattathri, 2511.14912v3](https://arxiv.org/abs/2511.14912v3), introduction, section2 and sections6.1–6.2: physical exchange precedes the torque equation; the later discussion tests the explanation through evolving phase-space structure.
- [van den Bosch & Ogiya, 1801.05427v1](https://arxiv.org/abs/1801.05427v1), introduction, sections2.1–2.2 and3: idealizations are justified by the processes they isolate, and one evolution is explained before numerical comparisons are expanded.
- [van den Bosch, Lange & Zentner, 1908.07547v1](https://arxiv.org/abs/1908.07547v1), introduction and connected methods/validation passages: the information lost by existing approaches motivates the added method.
- [van den Bosch, 1611.02657v1](https://arxiv.org/abs/1611.02657v1), introduction and sections2.1–2.2: definitions are introduced because they change the physical interpretation of catalogue histories.

A further recent coauthored comparison, [Chiang, van den Bosch & Keim, 2608.26249v1](https://arxiv.org/abs/2608.26249v1), introduction and opening methods, shows how a convenient orbital approximation is motivated and its error isolated. Coauthorship does not establish paragraph authorship. These are selected close readings, not a claim to have critically read every publication. The earlier broad discovery ledgers remain available as historical records, not quality scores.

## What changed in the paper

The argument now proceeds from orbital torque to resonance motion and scattering, then to the population approximation being tested. The methods derive the reduced equations from the local Hamiltonian, define the resonance width and libration scales, and identify the three terms in the action budget. They state the full-amplitude initial forcing, the isotropic isochrone DF tabulated with AGAMA, and the independent distribution and characteristic calculations. This distinguishes the physical positive population from the spectral algorithm, which monitors rather than guarantees positivity.

A new figure uses the existing recorded gradients and primitive kernel to show why the Gaussian changes signed cancellation. Its cumulative endpoints reproduce the corresponding recorded estimates to the documented kernel-grid tolerance. No new orbits, fitted curves or intermediate simulation frames were generated.

The error criterion is explained as a decision about replacing a population. Its conservative rejections follow from taking absolute values, rather than being presented only as status labels. The finite-displacement estimator is motivated by cancellation noise and its zero-integral control is explained through area preservation and the zero angular mean of the torque. The physical weighted impulse is not assumed to vanish.

The PDF now omits web controls, internal claim callouts and the unrelated model registry from the main narrative. It retains the common scientific text, numbered figures, bibliography and complete numerical appendices. The website keeps stable claim identifiers and supporting histories available after the argument. Old release files and scientific evidence remain unchanged.

## Revised skill and review limits

The [skill snapshot](skill-editorial-2026-09-24/SKILL.md) and [worked writing repairs](skill-editorial-2026-09-24/references/writing-craft.md) replace generic advice with examples from our own poor draft. Separate readings checked the paragraph sequence and checked the model definitions against the source. These are internal editorial checks, not external scientific review or evidence that a particular expert will approve the writing.

The numerical contribution and its restrictions are unchanged: one prescribed resonance, one reference fast-action slice, imposed additive diffusion and finite times. Three-dimensional transfer remains unresolved. Rewriting the explanation does not establish broader physical validity.
