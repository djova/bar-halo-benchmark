# Echo discovery screen, 1 October 2026

Canonical scope: early numerical validation of the proposed dark-halo memory experiment. The first gate replicates known collisionless echo physics; only subsequent three-dimensional gravitational observables can support the proposed halo extension. Initial allocation: at most two CPU-hours, one worker at nice 10, all BLAS/OpenMP pools limited to one thread. No live galaxy conclusion is possible from a prescribed tracer potential.

## Primary sources and novelty boundary

- Chiba, Ding, Hamilton, Kunz & Tremaine, *Galactic echoes* (2025), [arXiv version 2](https://arxiv.org/html/2506.16512v2), [published paper](https://doi.org/10.1093/mnras/staf1463). Equations 17–25 derive the two-impulse echo; Appendix B treats constant frequency shear and action-independent kicks. Their experiment concerns stellar vertical motion and already establishes the basic galactic echo mechanism. The halo and its gravitational readout remain the proposed extension.
- Gould, O'Neil & Malmberg (1967), *Plasma Wave Echo*, [Physical Review Letters 19, 219](https://doi.org/10.1103/PhysRevLett.19.219), is the foundational plasma calculation cited by Chiba et al.
- O'Neil & Gould (1968), *Temporal and spatial plasma wave echoes*, [Physics of Fluids 11, 134](https://doi.org/10.1063/1.1691746), primary analytical development; [Caltech archival record](https://authors.library.caltech.edu/records/qddf6-xjm06).
- Malmberg, Wharton, Gould & O'Neil (1968), *Plasma wave echo experiment*, [Physical Review Letters 20, 95](https://doi.org/10.1103/PhysRevLett.20.95), is the original laboratory demonstration referenced by Chiba et al.

Bibliographic details were checked against the primary archival records and publisher page. The initially entered DOI for O'Neil & Gould was incorrect; it was corrected to `10.1063/1.1691746` after reading the Caltech record, before interpreting results.

## Gate 1: exact one-angle numerical control

Use canonical cylinder coordinates `(theta,p)` with p on the whole real line, not a physical nonnegative halo action. The Hamiltonian is `H0=Omega0*p+s*p^2/2`; Gaussian p and uniform theta are an equilibrium. An impulsive potential `a_i cos(n_i theta)` gives the exact canonical kick `p += a_i n_i sin(n_i theta)`. Free evolution is exact. Product Gauss–Hermite and uniform-angle quadrature removes particle shot noise.

Record complex `C_m=<exp(-i m theta)>` and `C_AB-C_A-C_B+C_0`, with `m=n2-n1`. Test n1=1 and n2=2,3, several separations and a factor-four amplitude range. Check against an independently evaluated perturbative DF integral and the closed-form mixed response. Refocusing is at `te=n2*tau/(n2-n1)`; an integrated density mode can have a zero there and two surrounding lobes. Do not identify the largest lobe with the exact refocusing time.

At the second pulse, erase theta–p correlations by replacing the angle distribution with a new independent uniform distribution while preserving the p marginal. Apply this intervention to all four matched cases. Since m<n2, the second-only response of this projected distribution has zero m mode by discrete rotational symmetry. Confirm that with explicit product quadrature at selected times.

Acceptance: the exact map approaches the second-order analytic complex waveform as amplitudes shrink; quadrature refinement changes the result far less than the echo; delay changes move the refocusing window as predicted; projected memory removal suppresses it. These validate the implementation and prior mechanism only.

## Gate 2: three-dimensional physical impulses

Use the spherical isochrone with G=M=1 and b=0.5, an isotropic equilibrium tracer population, and gravitational impulses defined as spatial potentials rather than angle-space harmonics. Integrate the post-impulse background exactly in action/angle coordinates and cross-check selected trajectories independently in Cartesian coordinates.

The physical quadrupole is a finite radial-envelope real spherical harmonic; the Cartesian gradient supplies a velocity impulse. A smooth global tidal potential is a separate control. Measure complex density quadrupoles, radial breathing, and potential/force multipoles readable by a hypothetical stellar disk. Four paired cases and a memory-erased control are mandatory.

There is no universal scalar echo time in a 3D halo. For pulse Fourier vectors k1 and k2, a difference-mode phase is `[(k2-k1)t-k2*tau] dot Omega(J)`. A refocusing time requires the action-dependent part to cancel. The spherical Hamiltonian depends on Jr and total L, giving two dispersive frequencies and one degenerate plane-orientation frequency. Collinear radial harmonics can refocus; different angular/radial vectors generally leave residual dephasing. Identify possible channels before interpreting the measured curves.

Reject the astrophysical interpretation if a feature depends on a numerical defect, lacks pulse-product scaling or separation dependence, survives memory erasure, is only a persistent orbital-plane distortion, or has no measurable gravitational multipole. A null screen excludes only the selected potential, DF, pulse family, strengths and time window. Self-gravity and a live stellar response are subsequent gates, not inferred from a tracer calculation.

## Reproduction and receipts

Scripts live under `scripts/discovery/echo*`; raw traces, configurations, source hashes, timings and figures under `results/discovery-20261001/echoes/`. Preserve failed runs. Summarize completed gates and unmet conditions in `ECHO_LEARNINGS.md`.
