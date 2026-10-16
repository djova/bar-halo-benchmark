"""Exact AST-selected frozen scientific functions; same-code port, not independent validation."""


RADII = (.25, .5, 1., 2., 4., 8.)


SEEDS = tuple(range(76101601, 76101617))


COMPONENTS = ('x', 'y', 'z')


POLYNOMIALS = ('1', 'x', 'y', 'z', 'x2-y2', 'xy', 'xz', 'yz', '2z2-x2-y2',
    'x(x2-3y2)', 'y(3x2-y2)', 'z(x2-y2)', 'xyz',
    'x(4z2-x2-y2)', 'y(4z2-x2-y2)', 'z(2z2-3x2-3y2)')


THIRDS = ((0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 1), (0, 1, 2),
          (0, 2, 2), (1, 1, 1), (1, 1, 2), (1, 2, 2), (2, 2, 2))


SOLVER = dict(maxiter=400, maxfun=12000, maxls=30, maxcor=10, ftol=1e-14, gtol=1e-10)


def read_state(state, np):
    values = {}
    with np.load(state['arrays'], allow_pickle=False) as saved:
        for name, header in state['header'].items():
            if set(header) != {'npz', 'shape', 'dtype'}:
                raise RuntimeError('Exact stored-array reference required')
            value = saved[header['npz']]
            if list(value.shape) != header['shape'] or str(value.dtype) != header['dtype'] or not np.isfinite(value).all():
                raise RuntimeError('Original array/header mismatch or nonfinite state')
            values[name] = value
    if (values['xv'].shape != (12288, 6)
            or not np.array_equal(values['particle_id'], np.arange(12288))
            or not np.array_equal(values['cohort'], np.repeat([0, 1, 2], [8192, 2048, 2048]))
            or not np.array_equal(values['mass'], np.r_[np.full(8192, 1./8192), np.full(4096, .025/2048)])):
        raise RuntimeError('Full original positive constant-mass cohorts and IDs required')
    return values


def polynomials(x, degree, np):
    a, b, c = x.T
    values = [np.ones(len(x)), a, b, c, a*a-b*b, a*b, a*c, b*c, 2*c*c-a*a-b*b]
    if degree == 3:
        values += [a*(a*a-3*b*b), b*(3*a*a-b*b), c*(a*a-b*b), a*b*c,
            a*(4*c*c-a*a-b*b), b*(4*c*c-a*a-b*b), c*(2*c*c-3*a*a-3*b*b)]
    return np.asarray(values)


def feature_sets(x, v, np, check):
    radius = np.linalg.norm(x, axis=1)
    def spatial(radii, degree, logarithmic=False):
        rows, labels = [], []
        for r in radii:
            check()
            if logarithmic:
                direction = np.divide(x, radius[:, None], out=np.zeros_like(x), where=radius[:, None] > 0)
                basis = polynomials(direction, degree, np)
                basis[1:, radius == 0] = 0.
                log = np.full(len(x), -np.inf)
                np.log(radius/r, out=log, where=radius > 0)
                window = np.exp(-.5*(log/.35)**2)
            else:
                basis = polynomials(x/r, degree, np)
                window = np.exp(-.5*(radius/r)**2)
            for name, b in zip(POLYNOMIALS, basis, strict=False):
                for j, axis in enumerate(COMPONENTS):
                    rows.append(window*b*v[:, j]); labels.append(f'R={r:.17g}|{name}|v{axis}')
        return np.asarray(rows), labels
    train, labels = spatial(RADII, 2)
    train = np.concatenate((v.T, np.cross(x, v).T, train), axis=0)
    labels = ['global_P'+a for a in COMPONENTS]+['global_L'+a for a in COMPONENTS]+labels
    mid = tuple((a*b)**.5 for a, b in zip(RADII[:-1], RADII[1:], strict=True))
    held_a, names_a = spatial(mid, 3)
    held_b, names_b = spatial(RADII, 2, True)
    third, names_t = [], []
    for r in RADII:
        check(); window = np.exp(-.5*(radius/r)**2)
        for i, j, k in THIRDS:
            third.append(window*v[:, i]*v[:, j]*v[:, k])
            names_t.append(f'R={r:.17g}|v{COMPONENTS[i]}v{COMPONENTS[j]}v{COMPONENTS[k]}')
    groups = dict(training=(train, labels), heldout_midpoint_solid_l0_l3=(held_a, names_a),
        heldout_original_logwindow_unit_direction_l0_l2=(held_b, names_b),
        velocity_third_signal=(np.asarray(third), names_t))
    for (a, names), count in zip(groups.values(), (168, 240, 162, 60), strict=True):
        if a.shape != (count, len(x)) or len(names) != count or not np.isfinite(a).all():
            raise RuntimeError('Full fixed feature set changed or is nonfinite')
    return groups


def dual(z, features, mass, np):
    q = features.T @ z
    # logcosh(q)-q = log(1+exp(-2q))-log(2), stable for the original h=+1 target.
    value = float(mass @ (np.logaddexp(0., -2*q)-np.log(2.)))
    gradient = features @ (mass*(np.tanh(q)-1.))
    if not np.isfinite(value) or not np.isfinite(gradient).all():
        raise ArithmeticError('Nonfinite entropy dual; no clipping or repair')
    return value, gradient


def solve(a, mass, np, minimize, check):
    check(); rms = np.sqrt((a*a) @ mass/mass.sum())
    scale = np.where(rms > 0, rms, 1.)  # Exactly zero rows retained with original zero residual.
    b = a/scale[:, None]
    gram = (b*mass) @ b.T
    eigenvalues, vectors = np.linalg.eigh(gram)
    ridge = float(np.sqrt(np.finfo(float).eps)*max(1., float(eigenvalues[-1])))
    if not np.isfinite(eigenvalues).all() or eigenvalues[0]+ridge <= 0:
        raise ArithmeticError('Full-rank numerical preconditioner unavailable; no rank truncation')
    transform = (vectors*(eigenvalues+ridge)**-.5) @ vectors.T
    features = transform @ b
    check()
    def objective(z):
        check(); return dual(z, features, mass, np)
    def callback(z):
        check()
    result = minimize(objective, np.zeros(len(a)), jac=True, method='L-BFGS-B',
        callback=callback, options=dict(SOLVER))
    check(); q = features.T @ result.x; h = np.tanh(q)
    original_lambda = (transform.T @ result.x)/scale
    target = a @ mass; absolute_moment = abs(a) @ mass
    boundary_rows = (absolute_moment > 0) & (abs(target) == absolute_moment)
    saturated = abs(h) == 1.
    status = ('inconclusive_boundary' if boundary_rows.any() else
        'inconclusive_solver' if not result.success else
        'inconclusive_numerical_saturation' if saturated.any() else 'finite_solver_candidate_only')
    probabilities = .5*(1+h); reverse = .5*(1-h)
    lp = np.log(2*probabilities, out=np.zeros_like(h), where=probabilities > 0)
    lm = np.log(2*reverse, out=np.zeros_like(h), where=reverse > 0)
    summary = dict(status=status, optimizer_success=bool(result.success), optimizer_status=int(result.status),
        message=str(result.message), iterations=int(result.nit), function_evaluations=int(result.nfev),
        gradient_evaluations=int(result.njev), objective=float(result.fun),
        transformed_gradient_max_absolute=float(abs(result.jac).max()),
        entropy_relative_to_even=float(mass @ (probabilities*lp+reverse*lm)),
        original_entropy_relative_to_even=float(mass.sum()*np.log(2.)),
        expected_reversed_mass=float(mass @ reverse), host_mass=float(mass.sum()),
        minimum_h=float(h.min()), maximum_h=float(h.max()),
        numerically_saturated_count=int(saturated.sum()), minimum_one_minus_h_squared=float((1-h*h).min()),
        floating_point_support_boundary_row_indices=np.flatnonzero(boundary_rows).tolist(),
        boundary_search_complete=False, original_rows_dropped=0,
        preconditioning=dict(method='row_RMS_then_full_rank_ridge_inverse_sqrt',
            ridge=ridge, ridge_formula='sqrt(float64_epsilon)*max(1,largest_eigenvalue_of_RMS_Gram)',
            smallest_Gram_eigenvalue=float(eigenvalues[0]), largest_Gram_eigenvalue=float(eigenvalues[-1]),
            Gram_evaluation='RMS-scaled dual Hessian at h=0; not the final solution Hessian',
            objective_regularization=False, zero_RMS_rows=int((rms == 0).sum()),
            explanation='lambda=diag(1/RMS) T.T z; T=(Gram+ridge I)^(-1/2), no eigenvalue clipping or row deletion'),
        solver_options=dict(SOLVER), physical_feasibility_qualified=False)
    arrays = dict(h=h, original_dual_lambda=original_lambda, transformed_dual_z=result.x,
        row_RMS=rms, RMS_Gram_eigenvalues=eigenvalues,
        original_support_function_gap=absolute_moment-abs(target))
    return h, summary, arrays


def fixtures(np, minimize, check):
    a = np.array([[1., -1.]]); mass = np.array([2., 1.])
    h, report, _ = solve(a, mass, np, minimize, check)
    expected = np.array([1./3, -1./3])
    interior_error = float(abs(h-expected).max())
    if not report['optimizer_success'] or interior_error > 1e-8:
        raise RuntimeError('Unequal-mass analytic interior-current fixture failed')
    _, boundary, _ = solve(np.array([[1., 2.]]), mass, np, minimize, check)
    if boundary['status'] != 'inconclusive_boundary':
        raise RuntimeError('Boundary target must remain inconclusive, even if optimizer terminates successfully')
    a = np.array([[1., -2., .5], [.3, .7, -.4]])
    w = np.array([.2, .3, .5]); z = np.array([.17, -.31]); step = 1e-6
    _, analytic = dual(z, a, w, np); finite = []
    for j in range(2):
        shift = np.zeros(2); shift[j] = step
        finite.append((dual(z+shift, a, w, np)[0]-dual(z-shift, a, w, np)[0])/(2*step))
    error = float(abs(analytic-np.asarray(finite)).max())
    if error > 2e-8:
        raise RuntimeError('Independent finite-difference entropy-gradient fixture failed')
    return dict(passed=True, implementation_only=True, interior_expected_h=expected.tolist(),
        interior_max_absolute_error=interior_error, boundary_status=boundary['status'],
        boundary_optimizer_success=boundary['optimizer_success'], gradient_max_absolute_error=error,
        gradient_central_difference_step=step, unequal_mass_fixture=True)


def normalized(value, scale, np):
    return np.divide(value, scale, out=np.zeros_like(value, dtype=float), where=scale > 0)


def moments(a, mass, h, signs, np):
    target = a @ mass; fractional = a @ (mass*h)
    scale = abs(a) @ mass  # Positive absolute moment, never a cancellation-prone original signed target.
    rounded = (a @ (signs*mass).T).T
    variance = (a*a) @ (mass*mass*(1-h*h))
    residual = fractional-target; rounding_residual = rounded-target
    values = dict(original=target, fractional=fractional, fractional_residual=residual,
        absolute_moment_scale=scale, normalized_available=scale > 0,
        fractional_normalized_residual=normalized(residual, scale, np),
        rounded=rounded, rounded_residual=rounding_residual,
        rounded_normalized_residual=normalized(rounding_residual, scale, np),
        rounded_minus_fractional=rounded-fractional,
        analytical_rounding_variance_about_fractional=variance,
        analytical_rounding_SD_normalized=normalized(np.sqrt(variance), scale, np),
        sixteen_seed_mean_residual=rounding_residual.mean(axis=0),
        sixteen_seed_sample_SD=rounding_residual.std(axis=0, ddof=1))
    values['sixteen_seed_mean_normalized_residual'] = normalized(values['sixteen_seed_mean_residual'], scale, np)
    values['sixteen_seed_sample_SD_normalized'] = normalized(values['sixteen_seed_sample_SD'], scale, np)
    summary = dict(rows=len(a), normalization='sum_i w_i abs(a_ki); zero-scale rows unavailable, raw zeros retained',
        max_absolute_fractional_normalized_residual=float(abs(values['fractional_normalized_residual']).max()),
        max_absolute_single_seed_normalized_residual=float(abs(values['rounded_normalized_residual']).max()),
        max_analytical_rounding_SD_normalized=float(values['analytical_rounding_SD_normalized'].max()),
        max_sixteen_seed_sample_SD_normalized=float(values['sixteen_seed_sample_SD_normalized'].max()),
        max_absolute_sixteen_seed_mean_normalized_residual=float(abs(values['sixteen_seed_mean_normalized_residual']).max()),
        zero_scale_rows=int((scale == 0).sum()), numerical_pass_assigned=False)
    return values, summary
