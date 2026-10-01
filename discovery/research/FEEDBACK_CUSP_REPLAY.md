# Saved cuspy-feedback arithmetic

The standalone `replay_feedback_cusp_v1.py` uses NumPy and the retained
package `operands/feedback-cusp-v1/`. It verifies every retained NPZ
checksum and reproduces the saved-array known-map and finite-pulse
statistics. All state indices are retained, including inaccurate or
negative signed paths. No trajectory, physical DF or sample is changed.

The package's copy of `feedback-cusp.json` is identical to
`data/feedback-cusp.json`. Its `retained_files.path` fields are relative
to the arithmetic package. `public_path` fields are relative to the
discovery publication root. Figure rows compare actual finite central
halo energy with same-state weak forecasts; error bars are empirical
IID standard errors, not a stellar/halo cost or a population error bound.

## Array meanings and axes

`initial.npz` has8192 IID states. `xv` has columns x,y,z,vx,vy,vz.
`delta` is initial E−Phi0; `q` is the normalized proposal density;
`g` is the normalized stationary target density; `slope` is−dg/dE.
`component` marks the proposal-mixture component and `selected_ids`
are the twelve preselected reference indices. Initial state weights
are g/q and are never self-normalized.

Each `pulse-dt*.npz` retains both directions in map order
forward0,forward5,forward8,inverse0,inverse5,inverse8. Its
`delta_initial`, `delta_final`, `deltaE`, `work` and
`energy_minus_work` have axes map,state. Work integrates a centered
gas-potential basis; centering removes a physically irrelevant
constant while preserving the exact cyclic work. `L_vector_error`
has axes map,state,(Lx,Ly,Lz). `virtual_first_work` has axes
state,(frequency5,frequency8) and is evaluated on unforced paths.

`R32_i` and `R64_i` are finite forward curvature integrals, including
the declared seam atom, before division byq; i=0,1,2 denotes
zero,5,8. `support_i` is−F(E) for inverse Ec exits and zero otherwise.
`positive_estimates`=(R64+support)/q has axes (zero,5,8),state.
`paired_zero_contrast` retains each pulse minus that same state's zero
estimate. `weak_forecast` is.5(−g')D1²/q. The full weak seam contribution
has a separately recorded upper bound in the JSON. The
`inverse_composition_scaled_norm` array is the norm of the saved
Cartesian inverse composition error divided by1+the initial norm.

`known-map.npz` retains all32768 IID states' delta,q,g, mixture labels,
forward/inverse energies, R32/R64, seam atoms and support terms for
translations0,.05,.2,.8. No physical pulse is involved. The
independent target mean is k²/2. Cartesian positions for these known
maps are omitted because the arithmetic uses the saved energy operands.

`selected-reference.npz` has axes map,selected-state with the same six
map order and the initial indices above. Its adaptive signed endpoints
and work are checks on selected paths. They cannot be interpreted as a
population mean, an omitted-path error bound or an exactly canonical
map. Full population map endpoints and trajectory histories are not
part of this compact arithmetic package.

## What replay establishes

Replay recomputes known translation estimates, forward pulse means,
empirical standard errors, raw signed responses, pulse-zero contrasts,
same-state weak forecasts, covariance-aware finite-minus-weak and
fine-minus-coarse differences, weighted energy/work accounting,
sampled inverse-support counts and inverse replay norms. It checks
the figure operands against those recomputed values. The coarse8
accounting failure remains visible beside the fine passing values.

Replay does not establish initial equilibrium, physical DF exactness,
force accuracy, sampling-tail coverage, coeval stellar heating, or
self-consistent core formation. Those require separate evidence.
