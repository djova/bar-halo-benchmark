# Equal-time density-null diagnostic: record and method

The [complete scientific record](../diagnostics/ward-density-kick.json) contains both actual grids and both populations, including all nonzero raw matrices and residuals. The completed diagnostic passed its original physical-seed and two-grid known-null screens. This is an equal-time projection check without evolution, not an independent collective-response confirmation, a forced-work error bound, a causal accuracy test, or a stability result. It does not repair the isolated dipole failure.

The JSON is an explicitly sanitized projection of the closed result: private source-path inventory is omitted, while every scientific grid value, refinement operand, flag and actual resource value is retained. The result and origin hashes are recorded in its `public_projection`.

## Consumed historical protocol

The protocol below is preserved as authored before execution. Its prospective wording describes that historical source state; the completed record linked above supplies the current status. It is a method record, not a command for a new portable runner.

# Equal-time quadrupole density-null diagnostic

This is one prospective, owner-metered diagnostic of the anchored quadrupole
projection. It has not been executed. It does not evolve a halo or amend any
previous method failure, result, or scientific criterion.

For a canonical generator \(G=\tau_g V(\boldsymbol{x})\), the perturbation is
\(f_1=\{G,F\}=\tau_g\nabla V\cdot\partial_{\boldsymbol v}F\). The velocity
integral is zero for the supported, vanishing-at-escape distribution. Thus an
instantaneous potential kick has zero density perturbation. This identity does
not require an isotropic DF or the specially imposed zero-current condition.
It tests the projection at one time, rather than stability or causal response.

With the existing source conventions, the angle-Fourier generator is
\(G_{nkm}=C_{mk}(\mu)\sum_a b_{ma}R_{nka}\). There is no extra factor of
\(i\) in this generator; \(f_{1,nkm}=i\kappa_{nkm}G_{nkm}\). The raw matrix
reported for all seven input/output radial columns and both \(m=\pm2\) is

\[
 S_{ba,m}=\frac{i}{I_{b2}}\sum_{E,L,n,k} W\,R_{nkb}R_{nka}
 \int_{-1}^{1}C_{mk}^2(\mu)\kappa_{nkm}(\mu)\,d\mu .
\]

Here \(I_{b2}<0\), \(W=(2\pi)^3L_c^2\eta\,de\,d\eta/\Omega_r\),
\(\nu=n\Omega_r+k\Omega_L\), and \(k=-2,0,2\). For
\(F=C[f_0(e)+L\mu h(e,L^2)]\), the full derivative is

\[
 \kappa=C[-\nu f_{0,e}+mh+L\mu(2kLh_{L^2}-\nu h_e)].
\]

The nodal term \(m h=mF_{L_z}/C\) is retained even though the unperturbed
nodal frequency is zero. GL3 evaluates this inclination polynomial exactly
in exact arithmetic. Its direct contraction is also compared with the existing
analytic \(C A_k[-\nu f_{0,e}+mh+(mk/6)L(2kLh_{L^2}-\nu h_e)]\), where
\(A_k=(3/4,1/2,3/4)\). Neither expression is adjusted to produce a zero.

The physical quadrupole basis \(B\) has \(b_{\pm2,0}=3M_b/(7\sqrt{30})\),
all other input coefficients zero, \(M_b=0.1\), and \(\tau_g=1\) in model
time. This is the normalization of \(B\) alone; no finite-cycle shape or
envelope history is applied.
Its projected density is \(c_{bm}=\tau_g b_{m0}S_{b0,m}\). The caller reports
\(-U=-\tfrac12\sum I_{b2}|c_{bm}|^2\), the raw complex source torque
\(\sum I_{b2}c_{bm}^{*}(-im b_{mb})\), and the raw reality residual.
The matrix is a generator-to-density map; the columns are not orbital counts.
Arbitrary unit columns do not share the physical source's normalization.

Two fresh full-support libraries are required: GL32×32/N32 and GL64×64/N64,
both CB0–6, signed radial harmonics and complete \(k\), orbit order 64 with
maximum 2048 and tolerance \(3\times10^{-8}\). The same frozen manifest's F0
and A_full_plus are used. No action tail is removed, no stored orbit library is
reused, and no mass, coefficient, target, or reality symmetry is renormalized.
The retained Fourier tail proxies and action measure are recorded. Their
positive-measure weighting is not a bound on the forced work or Ward residual.

The physical seed alone has these frozen, inclusive operational screens:
each grid/population requires \(\max|c|\le10^{-6}\) and \(-U\le10^{-10}\);
the two-grid physical coefficient difference must also be at most \(10^{-6}\).
The coefficient scale is approximately 0.05% of the roughly 0.002 response
amplitude supplied by ROOT. The energy screen is a separate known-null
allowance. Neither is a new error allowance on the finite-cycle claim. All raw
matrix columns are reported without a column-wide pass assertion. Failure
remains a validation gap; passage is a finite-quadrature known-null check,
not a continuum bound, angular-closure proof, or global stability result.

The no-argument command is the canonical `.venv/bin/python -B
scripts/halo_response/ward_density_kick.py`, stage
`l2-equal-time-density-ward`. ROOT selects the unique owner and freezes/adopts
the launch after review. Exact prospective caps are 240 CPU seconds, 600 wall
seconds, 4096 MiB RAM and 64 MiB output; one-job obligation including the
existing 27-second meter grace is 267 CPU seconds. These are a bounded attempt,
not a guaranteed completion price. ROOT supplied the paid joint setup costs:
111.06204232 CPU seconds for GL128×128/N64 orbital construction and
1.807992137 for its operator. This diagnostic constructs smaller libraries and
no evolution; differing orbital orders and process overhead still require
metering. No retry, larger grid, or altered screen is admitted by this note.

Only one small JSON result is written, atomically after completed grids and
at closure; an exception preserves the completed prefix as incomplete. No
orbit archive, generator archive, or time series is written. The fine radial
array is 4096×129×3×7 doubles (roughly 89 MB); its frequency array is roughly
13 MB. Fresh orbital construction retains temporary row arrays before stacking,
and contractions use 64-action chunks. The 4 GiB limit includes these temporary
arrays, imports, and source snapshots; it is enforced, not asserted measured.

The narrow closure is the caller/note; its 19 fixed source/method/meter/contract
pins; the pinned `FINALIST_POPULATIONS.json`; all sources declared by that
manifest (already in those 19); and each exact proof payload as a closed
reference with its START/TERMINAL as source snapshots. The caller enforces that
exact union, hashes, sizes and roles. It uses the existing held-volume Guard,
with repeated UUID/directory checks and original owner resource gates. No old
trajectory, unrelated archive, numerical output, ledger, or publication is an
input. Root must supply the proof paths from the already frozen manifest;
this source authoring does not read its proof outcomes or generate a new proof.


## Exact contraction-source excerpt

This is the unmodified `grid` function from `ward_density_kick.py`, SHA-256 `a7f7fa8a03bd852a8edbc15cd31ffa6665b277776ca86a8ddfab9a3dc5a11883`. The consumed protocol SHA-256 is `aae35a566adb01646aecb5effacbbbf9bddf48e0d541b37f6ec182566a837733`. The excerpt requires its original helper objects and constants and is not a standalone executable or a newly tested public runner. No private runtime wrapper or infrastructure paths are included.

```python
def grid(cfg, guard, maps, core, robust, primitive, negative_norm, np, brentq):
    library = robust.build_library(cfg, guard, np, brentq, primitive, core.radial_values, core.K_VALUES)
    started = time.process_time()
    norms = np.asarray([negative_norm(n, 2) for n in range(7)])
    require(np.all(norms < 0), 'Physical negative CB norms required')
    mu, muw = core.rule(3, np)
    angular = core.angular_coefficients(mu, np)
    ak = np.asarray((.75, .5, .75))[None, None, :]
    k = library['inplane_k'][None, None, :]
    matrix = np.zeros((2, 2, 7, 7), dtype=complex)
    angular_difference = 0.
    # Direct complete GL3 inclination contraction; the closed-form expression
    # is separately compared, never used to force the Ward matrix to zero.
    for left in range(0, cfg.ne*cfg.neta, 64):
        guard.check()
        if guard.stop[0]:
            raise InterruptedError('Stopped raw Ward construction; no correction or automatic retry')
        right = min(left+64, cfg.ne*cfg.neta)
        e = library['e'][left:right, None, None]
        L = library['L'][left:right, None, None]
        nu = library['nu'][left:right]
        r = library['radial'][left:right].reshape(-1, 7)
        weight = library['weight'][left:right, None, None]
        ge = .5*e**2.5*(7-11*(140/33)*MB*e*e)
        for pi, coefficients in enumerate(maps.values()):
            h, he, hs = (np.zeros_like(e) for unused in range(3))
            for power, coefficient in coefficients.items():
                ap, bp = 4*power/((power+2.5)*(power+3.5)), 4/(power+1)
                h += coefficient*(-ap*e**(power-1)+bp*e**(power+1)+L*L*e**power)
                he += coefficient*(-ap*(power-1)*e**(power-2)+4*e**power+power*L*L*e**(power-1))
                hs += coefficient*e**power
            for mi, m in enumerate(M_VALUES):
                contraction = np.zeros_like(nu)
                for qi in range(3):
                    contraction += core.DF_C*muw[qi]*angular[qi, m+2, :][None, None, :]**2* (
                        -nu*ge+m*h+L*mu[qi]*(2*k*L*hs-nu*he))
                analytic = core.DF_C*ak*(-nu*ge+m*h+(m*k/6)*L*(2*k*L*hs-nu*he))
                angular_difference = max(angular_difference, float(np.max(np.abs(contraction-analytic))))
                weighted = (weight*contraction).ravel()
                matrix[pi, mi] += 1j*(r.T@(weighted[:, None]*r))/norms[:, None]
    b = 3*MB/(7*math.sqrt(30))
    density = TAU_G*b*matrix[:, :, :, 0]
    source = np.zeros((2, 7), dtype=complex); source[:, 0] = b
    torque = np.sum(norms[None, None, :]*density.conjugate()*(-1j*np.asarray(M_VALUES)[None, :, None]*source), axis=(1, 2))
    energy = -.5*np.sum(norms[None, None, :]*np.abs(density)**2, axis=(1, 2))
    require(all(np.all(np.isfinite(value)) for value in (matrix, density, torque, energy)),
            'All raw equal-time operands must be finite')
    maximum = np.max(np.abs(density), axis=(1, 2))
    mass = float(np.sum(library['weight']*2*core.DF_C*library['e']**3.5*(1-(140/33)*MB*library['e']**2)))
    weights = library['weight']
    tail = dict(value=np.sum(weights[:, None, None]*library['value_tail_proxy'], axis=0).tolist(),
        derivative=np.sum(weights[:, None, None]*library['derivative_tail_proxy'], axis=0).tolist(),
        weighting='Positive canonical action measure only; no DF/response-work bound')
    output = dict(config=asdict(cfg), full_action_node_count=cfg.ne*cfg.neta,
        radial_n=library['radial_n'].tolist(), inplane_k=library['inplane_k'].tolist(),
        m=list(M_VALUES), norms=norms.tolist(), source_b=b, generator_tau=TAU_G,
        raw_matrix_real=matrix.real.tolist(), raw_matrix_imag=matrix.imag.tolist(),
        physical_density_real=density.real.tolist(), physical_density_imag=density.imag.tolist(),
        physical_density_max_abs=maximum.tolist(), physical_minus_U=energy.tolist(),
        initial_source_torque_real=torque.real.tolist(), initial_source_torque_imag=torque.imag.tolist(),
        reality_max_abs=float(np.max(np.abs(density[:, 0]-density[:, 1].conjugate()))),
        physical_seed_screens=[bool(maximum[i] <= SCREENS['physical_coefficient_max']
            and energy[i] <= SCREENS['physical_minus_U']) for i in range(2)],
        direct_GL3_vs_analytic_kappa_max_abs=angular_difference,
        action_domain=dict(e=[0., 1.], eta=[0., 1.], endpoint_rule='GL interior nodes; no tail cuts'),
        physical_mass_totals=[mass, mass], canonical_measure_sum=float(np.sum(weights)),
        all_nodes_retained=True, normalization_changed=False, time_evolution=False,
        orbit_order_max=int(np.max(library['order'])),
        orbit_quadrature_error_max=library['quadrature_errors'].max(axis=0).tolist(),
        phase_panel_errors_max=library['phase_panel_errors'].max(axis=0).tolist(),
        pole_reconstruction_error_max=float(np.max(library['pole_reconstruction_error'])),
        weighted_fourier_tail_proxies=tail,
        orbit_construction_CPU_seconds=library['construction_CPU_seconds'],
        contraction_and_diagnostics_CPU_seconds=time.process_time()-started)
    return output, density.copy()
```
