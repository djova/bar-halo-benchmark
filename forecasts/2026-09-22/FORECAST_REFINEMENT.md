# One bounded forecast quadrature refinement

22 September 2026, before any3D held-out outcome. Case A's noisy mean is stable,
but its512x8192 to1024x16384 collisionless quadrature shift is0.00027344 action
units, 3.31% of its contrast magnitude. This misses the frozen requirement that
numerical changes be under2% of the contrast (10% of the20% adequacy half-width).
The existing forecast therefore remains numerically unqualified. Do not change
that threshold or pretend the missing qualification is a physical failure.

Use the PLAN's one bounded failed-prerequisite refinement for each case that
misses this same forecast test: one2048x32768 positive collisionless quadrature,
unchanged domain, population, Hamiltonian, timestep and endpoint. Case B uses
this remedy only if its initial forecast misses the threshold. No further ladder.
The final magnitude and qualification must be frozen before any3D outcome.

Process initial-angle blocks sequentially to limit temporary arrays and improve
cache use. The reported quantity is the same positive quadrature, with the same
Yoshida characteristic step. This endpoint-only implementation omits intermediate
histograms; it must first reproduce case A's512x8192 endpoint to1e-10 and pass
its unchanged moment/analytic checks. Report speed and conservation equivalence
before adopting it. New final-only results must not become fabricated history
frames. Preserve the original arrays, failed refinements and every source hash.

Allocate at most2additional scientific core-hours from the unused map allocation:
map ceiling12->10 and forecast/preparation ceiling2->4, total32unchanged. Cases
have3600s wall limits, nice10 and one core, within the combined4worker cap.
