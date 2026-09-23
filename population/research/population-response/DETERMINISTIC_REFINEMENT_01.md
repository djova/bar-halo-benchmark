# Independent deterministic remainder refinement 01

The single moving pilot completed in79.647947CPU seconds with all local checks.
This measured cost permits a bounded refinement matrix alongside the two-worker
independent stochastic validation. Reuse its moving base exactly; do not repeat
or relabel the failed earlier raw-characteristic quadrature.

Keep the same Hamiltonian, eta0.1 noisy counterpart, s0/.25, positive absolute
weights, windows24/40 and48/64, T10/T20 and density spacing1/8192. The collisionless
integrator is the existing fourth-order Yoshida composition, independent of the
stochastic Strang path implementation. The cumulative identity changes only the
quadrature estimator. Its full conservative auxiliary support exceeds152.10.

At each sweep compare base J160,nj10240,nphi256,dt.025 against:
- doubled action and angle resolution: J160,nj20480,nphi512;
- half timestep: J160,nj10240,nphi256,dt.0125;
- larger auxiliary domain at the same action spacing: J192,nj12288,nphi256,dt.025.

All six profiles and both times remain prescribed. Each comparison must change
the integrated bar impulse by less than2e-4. Retain raw and remainder estimates;
their finite-grid difference is a quadrature diagnostic, not sampling uncertainty.
Combine a qualified reference with the already recorded noisy distribution
calculations, whose independent mesh, step and window changes remain required.
Do not call agreement of collisionless estimators a noisy physical validation.

Run seven new cases plus the retained moving base, one nice10 single-thread
worker, at most7200CPU seconds and900wall seconds per case. This occupies the
third scientific slot. No source in either running matrix changes. A failed
refinement remains a failure; any further experiment requires a new documented
reason, cost estimate and unchanged scientific interpretation.
