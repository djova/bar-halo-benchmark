# Primary-source comparison for the population campaign

Read22September2026. This is a targeted comparison, not a systematic novelty survey.

- [Hamilton et al., Galactic bar resonances with diffusion](https://arxiv.org/html/2208.03855v2): stationary prescribed resonance, diffusion and torque saturation. The present kernel will concern finite duration and specified positive populations, not automatically its steady reservoir limit.
- [Chiba, Dynamical friction and feedback](https://arxiv.org/html/2305.00022v2): moving resonances and trapped/untrapped feedback; the discussion explicitly expects diffusion to reduce feedback while restoring friction-producing gradients. It also compares collisionless reduced and full3D calculations. A new sign illustration alone is not a new mechanism.
- [Ogilvie & Lubow2006](https://doi.org/10.1111/j.1365-2966.2006.10506.x), [arXiv](https://arxiv.org/abs/astro-ph/0605138): migrating non-coorbital corotation in a viscous gaseous disc. Torque depends on drift and diffusion; in the relevant steady regime the trapped vortensity anomaly gives a contribution inversely related to viscosity, while circulating material contributes differently. The analogy motivates a more careful priority statement, but vortensity, viscous gas dynamics and its asymptotic/steady assumptions are not the halo DF and prescribed action diffusion used here.
- [AGAMA upstream](https://github.com/GalacticDynamics-Oxford/Agama): read-only API check returns masterf302756b8af2b763db58e278e30478517dc8eea3, dated25August2026, the same revision used by the coordinate benchmark. Current open issue/PR titles show no coordinate repair. The later bounded open/closed-title and coordinate-history check is archived in upstream-history-01; it is not proof that no related discussion exists. A fresh four-case regression now reproduces the unchanged-library failure and verifies the separately patched library against80-digit coordinates. The minimal artifact and both receipts are public in the standalone benchmark; no maintainer acceptance is claimed.

Scientific claim sought: a measured dependence on full phase-space weighting and
an independently verified way to predict it. Neither the adjoint construction nor
the existence of competing scattering effects is claimed as new.
