---
name: astrophysics-interactive-research
description: Turn astrophysics results into an intuitive, interactive research publication with explicit inference, recorded counterfactuals, observational comparisons, and inspectable evidence. Use for research stories, scientific explorers, or substantial communication reviews of astronomy results.
---

# Interactive astrophysics research

Help the reader understand the dynamics and evaluate the calculation. This is our
editorial workflow, not a named researcher's style or advice. Its source readings
illustrate particular explanatory decisions; they do not certify the resulting
writing. For a paper or substantial prose revision, read
[writing craft and worked repairs](references/writing-craft.md). For scientific
explorers, use [the research and visual examples](references/principles.md).

## Establish the physical argument before drafting

Write a private paragraph outline in which each paragraph answers the question
created by the previous one. Begin with the physical system and what happens to
it. Explain why the quantity of interest depends on the mechanism under study,
what existing work leaves uncertain, and why this particular calculation resolves
part of that uncertainty. Do not substitute a claim registry for this outline.

For a dynamical paper, develop one causal chain explicitly: what changes an
orbit, how those changes accumulate or cancel across a population, and which
measurement distinguishes the proposed explanations. An algebraic rearrangement
can explain a numerical sensitivity without identifying a new physical mechanism;
say which level of explanation the evidence supports.

Derive the model the reader actually needs. Give the physical variables before
rescaling them, explain the approximation that removes degrees of freedom, and
state initial conditions and forcing history. After an equation, use it: extract
a sign, scale, limiting case or reason for the next calculation. A list of symbol
definitions alone is not an explanation.

## Start with the inference

For traceability, keep a small claim ledger: question → measured contrast
→ proposed mechanism → surviving alternatives → usable domain → evidence link.
Choose the main page's few claims by scientific consequence, including decisive
failures. A parameter catalogue or chronological work log belongs deeper.

Keep these distinctions visible wherever they change the conclusion:

- **State versus dynamics.** Similar density profiles or final shapes can conceal
  different distribution functions, orbital populations, torques and histories.
  Show the evolving quantity that discriminates between explanations.
- **Physical versus numerical interventions.** Changing softening, time step or
  particle number tests the calculation; changing the equilibrium or responsive
  components tests a physical model. Record any changed realization or confound.
- **Conservation versus prediction stability.** Both matter; passing one does not
  establish the other. Preserve individual paired signs and seed scatter rather
  than hiding cancellation behind an average.
- **Objects versus populations.** A trajectory cannot predict a bar fraction.
  Population spread is not uncertainty on one object. A null or unavailable
  estimator is an informative result, never a zero.
- **Reality versus the observation operator.** Connect latent mass and motion to
  projected light, selection, instrumental effects and the estimator actually
  used in the catalogue. Compare like definitions, apertures and normalizations.
- **Model adequacy versus parameter precision.** Tight error bars conditional on
  a restrictive model need not be accurate. State omitted physics and test which
  assumptions could mimic the claimed signal.

Use analytical limits, independent estimators, controlled numerical experiments
and observations as complementary tests. Do not transplant numerical thresholds
from another problem just because it uses the same solver or particles.

## Design interactions that answer questions

Each interaction should let a reader change a declared assumption, follow a conserved
quantity, switch reference frames, expose a degeneracy, or inspect a measurement.
Before building it, state what the reader will learn from using it.

Useful patterns, chosen for the available evidence:

- Synchronize actual paired runs to one physical clock; preserve the same spatial
  and measurement scales. Discrete controls select recorded experiments. Sliders
  for computed geometry or analytic demonstrations must say what is recomputed.
- Let readers switch between a density pattern and fixed particle trajectories,
  or between inertial and qualified rotating coordinates. Do not imply that visible
  elongation proves orbital trapping or identifies a resonance.
- Put signed differences beside paired histories; show where a physical control
  affects several observables even if the final morphology is similar.
- Expose the observation operator interactively: project, blur, restrict coverage,
  measure, then compare with independent simulation truth. Preserve failed cases.
- Connect a picture to its estimator: highlight the sampled aperture or annulus,
  explain the harmonic convention, and link the exact measurement to its source.

Never invent intermediate simulation states. Interpolated chart lines are guides,
not new measurements; show saved timestamps and coverage gaps. Use one clock only
for genuinely shared units and origins. A dimensionless reduced model needs its own
clock. Avoid decorative particle motion, arbitrary 3D camera flight, and animation
that suggests a causal process absent from the data.

## Make a research publication, with depth on demand

The opening should deliver a physical question, a compelling real-data view and a
bounded finding. Explain the essential caveat beside that finding, not behind a
methodology link. Then provide named routes to the full explorer, inference checks,
observational definitions, methods, data and reproducibility.

Organize the argument around the assumption being tested. State why that assumption
is convenient, what it preserves, and what measurable consequence would expose its
failure. Explain the transport or inference mechanism before presenting its formal
estimator. Give a successful approximation as much interpretive attention as a
counterexample: readers need to know what information they can safely discard.
End with a usable consequence under stated conditions, rather than a list of checks
or a promise of broader significance.

Choose headings that name the scientific content; do not impose questions on every
section. Captions should explain what changes, what stays fixed, and what the
comparison permits us to infer. Define symbols with physical meaning and units.
Use connected paragraphs, not a sequence of compressed declarations. Keep
technical precision; replace internal workflow terms with the actual mathematical
operation or physical comparison. State each restriction where it affects an
inference, then refer back instead of repeatedly reciting all nonclaims.
Preserve collaborators' credit and link exact primary sources. Observations about
a coauthored paper's communication are not evidence of one author's private intent.

Do not require an interaction to discover the headline result. Give an initial
state that already carries information, then invite exploration. Support deep links
to selected runs, time and diagnostics. Give researchers the exact data and conventions
without making general readers traverse every audit first.

## Review the finished experience

Follow a first-time reader's route and a skeptical researcher's route. Check that
each headline follows from its linked measurement and that the controls really
isolate what the copy says. Test missing data, rapid selection changes and weak
signals, not only the attractive frame. Inspect rendered desktop and phone views,
keyboard operation, touch targets, contrast, reduced motion and actual image pixels.
Provide text equivalents for essential plotted conclusions. Keep navigation usable
without JavaScript; fail visibly when data cannot load. Verify both publication
and provenance within the user's authorized scope.

Review prose independently of software checks. Read a rendered manuscript without
the website's navigation, registry, controls or development history. A print
export must be a complete argument, not a webpage pasted into a journal template.
Use a fresh reader to identify missing premises, unexplained notation and broken
paragraph transitions; request faults, not a readiness endorsement. Passing data,
layout or browser checks cannot establish writing quality. Report concrete
revisions and remaining doubts; do not predict that a named expert will approve.

For gas, assembly or multi-scale problems, also identify the controlling reservoirs,
transport processes and competing timescales. Present-day structure can retain a
history of mergers, accretion and relaxation; do not imply a unique origin from a
single snapshot. Read principles 5–6 for examples beyond stellar dynamics.
