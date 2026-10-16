"""Exact AST-selected frozen scientific functions; same-code port, not independent validation."""
import math
import time


REBASE_EVERY = 128


ROW_CONSERVATION_TOL = 1e-10


QR_TOL = 1e-10


RANK_DIAGONAL_TOL = 256*2.220446049250313e-16


STF_NAMES = ('(xx-yy)/sqrt2', 'sqrt2xy', 'sqrt2xz', 'sqrt2yz', '(2zz-xx-yy)/sqrt6')


def observers(x, scale, body, np):
    """phi_s(x)=phi_1(x/s); all35 real STF channels, radial-major ordering."""
    y = x/scale; basis = body.tensor_basis(np)
    f, fs, _, _ = body.profiles(y, np, jets=True)  # Default profiles returns TWO fs.
    sx = np.einsum('bij,aj->abi', basis, y)
    quad = np.einsum('ai,abi->ab', y, sx)
    value = f[:, :, None]*quad[:, None, :]
    gradient = (2*f[:, :, None, None]*sx[:, None, :, :]
        +2*fs[:, :, None, None]*quad[:, None, :, None]*y[:, None, None, :])/scale
    return value.reshape(len(x), 35), gradient.reshape(len(x), 35, 3)


def observer_rows(x, v, scale, body, np):
    _, gradient = observers(x, scale, body, np)
    rows = np.einsum('aqi,ai->qa', gradient, v)
    labels = [f'scale={scale:.17g}|CB{n}|{b}|grad_phi_dot_v' for n in range(7) for b in STF_NAMES]
    if rows.shape != (35, len(x)) or not np.isfinite(rows).all():
        raise RuntimeError('Invalid complete derivative observer family')
    return rows, labels


def flight_coordinates(a, mass, np):
    rms = np.sqrt((a*a) @ mass/mass.sum()); scale = np.where(rms > 0, rms, 1.)
    b = a/scale[:, None]; gram = (b*mass) @ b.T
    try: eig, vec = np.linalg.eigh(gram)
    except np.linalg.LinAlgError as exc: raise FlightFailure('Flight preconditioner eigensolve failed') from exc
    ridge = float(np.sqrt(np.finfo(float).eps)*max(1., float(eig[-1])))
    if not np.isfinite(eig).all() or eig[0]+ridge <= 0:
        raise FlightFailure('Full-rank flight coordinate transform failed')
    transform = (vec*(eig+ridge)**-.5) @ vec.T
    return (transform @ b)*mass, dict(rows=len(a), rows_dropped=0, ridge=ridge,
        min_RMS_Gram_eigenvalue=float(eig[0]), max_RMS_Gram_eigenvalue=float(eig[-1]),
        definition='A_i=m_i*T*diag(1/RMS)*a_i; invertible coordinates only; no target penalty')


class FlightFailure(RuntimeError):
    pass


def limits(p, u, np):
    plus = np.full(len(p), np.inf); minus = plus.copy()
    positive, negative = u > 0, u < 0
    plus[positive] = (1-p[positive])/u[positive]; minus[positive] = p[positive]/u[positive]
    plus[negative] = p[negative]/(-u[negative]); minus[negative] = (1-p[negative])/(-u[negative])
    ap, am = float(plus.min()), float(minus.min())
    if not (ap > 0 and am > 0 and np.isfinite(ap+am)):
        raise FlightFailure('Degenerate/nonfinite cube-flight step; no clipping/retry')
    return ap, am, plus, minus


def endpoint(p, u, alpha, ratios, forward, np):
    q = p+alpha*u if forward else p-alpha*u
    hits = ratios == alpha  # Only mathematical hitting coordinate(s) are frozen.
    q[hits] = (u[hits] > 0).astype(float) if forward else (u[hits] < 0).astype(float)
    if not hits.any() or not np.isfinite(q).all() or np.any((q < 0) | (q > 1)):
        raise FlightFailure('Flight left the probability cube; no global clipping/repair')
    return q, int(hits.sum())


def flight(a, mass, h, A, seed, np, la, check):
    """Full-support unbiased flight, then independent landing of <=row_count probabilities."""
    started = time.process_time(); r, n = a.shape; p0 = .5*(1+h); p = p0.copy()
    if n <= r or not np.isfinite(p).all() or np.any((p < 0) | (p > 1)):
        raise FlightFailure('Invalid finite full-particle probability state')
    order = np.random.Generator(np.random.PCG64(np.random.SeedSequence([seed, 1]))).permutation(n)
    order = order[(p[order] > 0) & (p[order] < 1)]
    coin = np.random.Generator(np.random.PCG64(np.random.SeedSequence([seed, 2])))
    landing_uniform = np.random.Generator(np.random.PCG64(seed)).random(n)
    cost = {k: 0. for k in ('QR', 'update', 'arithmetic', 'conservation')}
    counts = {k: 0 for k in cost}; worst = dict(null=0., orthogonality=0., reconstruction=0., conservation=0.)
    min_diag = 1.; checks = []; steps = 0; ties = 0; scale = abs(a) @ mass
    def conservation():
        mark = time.process_time(); residual = a @ (2*mass*(p-p0))
        norm = np.divide(residual, scale, out=np.zeros_like(residual), where=scale > 0)
        maximum = float(abs(norm).max()); worst['conservation'] = max(worst['conservation'], maximum)
        checks.append((steps, maximum)); cost['conservation'] += time.process_time()-mark; counts['conservation'] += 1
        if maximum > ROW_CONSERVATION_TOL:
            raise FlightFailure(f'Original-row flight conservation failed at step {steps}: max={maximum:.17g}; no correction')
        return residual
    def rebase(matrix):
        nonlocal min_diag
        check(); mark = time.process_time()
        try: q, rr = la.qr(matrix, mode='full', check_finite=False)
        except np.linalg.LinAlgError as exc: raise FlightFailure('Full active QR failed') from exc
        diag = abs(np.diag(rr[:r])); ratio = float(diag.min()/max(float(diag.max()), np.finfo(float).tiny))
        min_diag = min(min_diag, ratio)
        reconstruction = float(abs(q @ rr-matrix).max()/max(float(abs(matrix).max()), np.finfo(float).tiny))
        orth = float(abs(q.T @ q-np.eye(len(matrix))).max())
        worst['reconstruction'] = max(worst['reconstruction'], reconstruction); worst['orthogonality'] = max(worst['orthogonality'], orth)
        cost['QR'] += time.process_time()-mark; counts['QR'] += 1
        if (not np.isfinite([ratio, reconstruction, orth]).all()
                or ratio < RANK_DIAGONAL_TOL or reconstruction > QR_TOL or orth > QR_TOL):
            raise FlightFailure(f'Active QR failed: diagonal ratio={ratio:.17g}, backward={reconstruction:.17g}, orthogonality={orth:.17g}; no repair')
        return q, rr
    conservation()
    if len(order) > r:
        active = order[:r+1].copy(); cursor = r+1; matrix = A[:, active].T.copy()
        q, rr = rebase(matrix)
        while True:
            if steps % 16 == 0: check()
            mark = time.process_time(); u = q[:, -1].copy()
            if u[int(np.argmax(abs(u)))] < 0: u = -u
            null = float(abs(matrix.T @ u).max()/max(float(abs(matrix).sum(axis=0).max()), np.finfo(float).tiny))
            worst['null'] = max(worst['null'], null)
            if null > QR_TOL or abs(float(u @ u)-1.) > QR_TOL:
                raise FlightFailure(f'Updated full-Q null direction failed: relative residual={null:.17g}; no adaptive rebase')
            ap, am, positive, negative = limits(p[active], u, np)
            forward = bool(coin.random() < am/(ap+am))
            new, nhit = endpoint(p[active], u, ap if forward else am,
                positive if forward else negative, forward, np)
            p[active] = new; steps += 1; ties += nhit-1
            hit_rows = np.flatnonzero((new == 0) | (new == 1))
            cost['arithmetic'] += time.process_time()-mark; counts['arithmetic'] += 1
            finished = False
            for row in hit_rows:
                if cursor == len(order): finished = True; break
                mark = time.process_time(); incoming = int(order[cursor]); cursor += 1
                difference = A[:, incoming]-matrix[row]
                unit = np.zeros(r+1); unit[row] = 1.
                try: q, rr = la.qr_update(q, rr, unit, difference, check_finite=False)
                except np.linalg.LinAlgError as exc: raise FlightFailure('Rank-one active QR update failed') from exc
                matrix[row] = A[:, incoming]; active[row] = incoming
                cost['update'] += time.process_time()-mark; counts['update'] += 1
            if finished: break
            if steps % REBASE_EVERY == 0:
                conservation(); q, rr = rebase(matrix)
    final_flight_residual = conservation()
    terminal = np.flatnonzero((p > 0) & (p < 1))
    if len(terminal) > r or np.any((p < 0) | (p > 1)):
        raise FlightFailure('Flight did not terminate with <=all retained rows fractional')
    signs = np.where(landing_uniform < p, 1, -1).astype(np.int8)
    terminal_leverage = 2*(abs(a[:, terminal]) @ mass[terminal])
    terminal_leverage = np.divide(terminal_leverage, scale, out=np.zeros_like(scale), where=scale > 0)
    # Only the FINAL independent landing, conditional on this dependent flight.
    landing_variance = 4*(a[:, terminal]**2) @ (mass[terminal]**2*p[terminal]*(1-p[terminal]))
    elapsed = time.process_time()-started
    cost['other'] = elapsed-sum(cost.values()); counts['other'] = 1
    if not math.isfinite(elapsed) or elapsed <= 0 or any(not math.isfinite(v) or v < 0 for v in cost.values()):
        raise FlightFailure('Invalid measured component time; no negative/clipped timing credit')
    report = dict(seed=seed, complete=True, flight_steps=steps, fractional_start_count=len(order),
        terminal_fractional_count=len(terminal), exact_tie_extra_hits=ties, minimum_QR_diagonal_ratio=min_diag,
        QR_diagonal_ratio_is_condition_number=False, maximum_checks=worst,
        conservation_checks=[dict(step=s, max_absolute_normalized_residual=v) for s, v in checks],
        CPU_seconds=elapsed, component_CPU_seconds=cost, operation_counts=counts,
        marginals_preserved_in_conditional_expectation=True, final_constraints_exact=False,
        full_sampling_covariance='dependent; independent-Bernoulli variance does not apply')
    arrays = dict(terminal_particle_id=terminal, terminal_probability=p[terminal],
        flight_final_original_row_residual=final_flight_residual,
        terminal_original_row_worst_case_normalized_bound=terminal_leverage,
        conditional_terminal_landing_variance=landing_variance)
    return signs, report, arrays


def fixtures(body, old, np, la, minimize, check):
    result = old.fixtures(np, minimize, check)
    x = np.array([[0., 0., 0.], [.2, -.3, .4], [1.1, .5, -.7], [5., -2., 3.]])
    errors = []
    for scale in (1., .8, 1.25):
        _, gradient = observers(x, scale, body, np); step = 1e-6
        for axis in range(3):
            delta = np.zeros_like(x); delta[:, axis] = step
            fd = (observers(x+delta, scale, body, np)[0]-observers(x-delta, scale, body, np)[0])/(2*step)
            errors.append(float((abs(fd-gradient[:, :, axis])/(1+abs(gradient[:, :, axis]))).max()))
    if max(errors) > 2e-7: raise RuntimeError('Observer finite-difference gradient fixture failed')
    matrix = np.array([[1., .2, -.3], [.4, 1.2, .5], [-.7, .1, 1.], [.3, -.8, .9]])
    q, rr = la.qr(matrix, mode='full'); revised = matrix.copy(); revised[1] = [.7, -.2, 1.3]
    unit = np.array([0., 1., 0., 0.]); qu, ru = la.qr_update(q, rr, unit, revised[1]-matrix[1])
    qf, rf = la.qr(revised, mode='full')
    qr_error = float(abs(qu @ ru-revised).max())
    null_error = float(abs(np.outer(qu[:, -1], qu[:, -1])-np.outer(qf[:, -1], qf[:, -1])).max())
    if max(qr_error, null_error) > 1e-11: raise RuntimeError('Rank-one row update versus fresh full QR fixture failed')
    a = np.array([[1., -1., 2., -2., .5], [.3, .7, -1., .2, -.4]])
    mass = np.array([.2, .3, .1, .25, .15]); h = np.array([.2, -.1, .35, -.4, .05])
    A = a*mass; active = np.array([0, 1, 2]); q, rr = la.qr(A[:, active].T, mode='full')
    p = .5*(1+h[active]); u = q[:, -1]; ap, am, rp, rm = limits(p, u, np)
    pp, _ = endpoint(p, u, ap, rp, True, np); pm, _ = endpoint(p, u, am, rm, False, np)
    expectation_error = float(abs((am*pp+ap*pm)/(ap+am)-p).max())
    constraint_error = max(float(abs(A[:, active] @ (pp-p)).max()), float(abs(A[:, active] @ (pm-p)).max()))
    if max(expectation_error, constraint_error) > 1e-12:
        raise RuntimeError('Unequal-mass martingale/constraint identity failed')
    _, fr, _ = flight(a, mass, h, A, old.SEEDS[0], np, la, check)
    if fr['terminal_fractional_count'] > 2: raise RuntimeError('Complete tiny flight fixture failed')
    return dict(passed=True, implementation_only=True, original_dual_fixture=result,
        observer_gradient_max_scaled_error=max(errors), QR_reconstruction_error=qr_error,
        QR_null_projector_error=null_error, martingale_error=expectation_error,
        unequal_mass_constraint_error=constraint_error, tiny_flight=fr)


def preserve(raw, signs, np, check):
    xv, mass = raw['xv'], raw['mass']; speed = np.sum(xv[:, 3:]**2, axis=1)
    K = float(.5*(mass @ speed)); second = xv[:8192, 3:, None]*xv[:8192, None, 3:]
    for sign in signs:
        check(); changed = xv.copy(); changed[:8192, 3:] *= sign[:, None]
        if (not np.all(sign*sign == 1) or not np.array_equal(changed[:, :3], xv[:, :3])
                or not np.array_equal(changed[8192:], xv[8192:])
                or not np.array_equal(np.sum(changed[:, 3:]**2, axis=1), speed)
                or not np.array_equal(changed[:8192, 3:, None]*changed[:8192, None, 3:], second)):
            raise RuntimeError('Original full-mass single-sign/even/satellite identity failed')
    return dict(initial_K=K, exact_positions_masses_satellites_speed_and_raw_second=True,
        all_even_measures_preserved_by_single_sign=True, central_covariance_claimed_exact=False)


def measure(groups, mass, h, signs, old, np, check, independent):
    arrays, report = {}, {}
    for name, (a, labels) in groups.items():
        check()
        if independent:
            values, summary = old.moments(a, mass, h, signs, np)
        else:
            target = a @ mass; fractional = a @ (mass*h); scale = abs(a) @ mass
            rounded = (a @ (mass*signs).T).T; residual = rounded-target
            norm = old.normalized(residual, scale, np)
            values = dict(original=target, fractional=fractional, fractional_residual=fractional-target,
                absolute_moment_scale=scale, normalized_available=scale > 0,
                fractional_normalized_residual=old.normalized(fractional-target, scale, np),
                rounded=rounded, rounded_residual=residual, rounded_normalized_residual=norm,
                rounded_minus_fractional=rounded-fractional,
                sixteen_seed_mean_residual=residual.mean(axis=0), sixteen_seed_sample_SD=residual.std(axis=0, ddof=1))
            values['sixteen_seed_mean_normalized_residual'] = old.normalized(values['sixteen_seed_mean_residual'], scale, np)
            values['sixteen_seed_sample_SD_normalized'] = old.normalized(values['sixteen_seed_sample_SD'], scale, np)
            summary = dict(rows=len(a), max_absolute_fractional_normalized_residual=float(abs(values['fractional_normalized_residual']).max()),
                max_absolute_single_seed_normalized_residual=float(abs(norm).max()),
                max_absolute_sixteen_seed_mean_normalized_residual=float(abs(values['sixteen_seed_mean_normalized_residual']).max()),
                max_sixteen_seed_sample_SD_normalized=float(values['sixteen_seed_sample_SD_normalized'].max()),
                full_sampling_covariance='dependent; complete16 raw moment samples retained', numerical_pass_assigned=False)
        arrays.update({name+'__'+k: v for k, v in values.items()}); report[name] = summary
    return arrays, report


def prepare(states, body, old, np, minimize, check):
    prepared = []; costs = []; labels = None
    for state in states:
        check(); started = time.process_time(); raw = old.read_state(state, np)
        x, v, mass = raw['xv'][:8192, :3], raw['xv'][:8192, 3:], raw['mass'][:8192]
        groups = old.feature_sets(x, v, np, check)
        derivative, names = observer_rows(x, v, 1., body, np)
        original, old_names = groups['training']
        groups['training'] = (np.concatenate((original, derivative)), old_names+names)
        for scale in (.8, 1.25):
            groups[f'heldout_observer_scale_{scale}'] = observer_rows(x, v, scale, body, np)
        a = groups['training'][0]
        if a.shape != (203, 8192): raise RuntimeError('All168+35 original constraints required')
        h, solved, solution_arrays = old.solve(a, mass, np, minimize, check)
        A, precondition = flight_coordinates(a, mass, np)
        signs = np.asarray([np.where(np.random.Generator(np.random.PCG64(seed)).random(8192) < .5*(1+h), 1, -1)
            for seed in old.SEEDS], dtype=np.int8)
        mark = time.process_time(); identity = preserve(raw, signs, np, check)
        arrays, report = measure(groups, mass, h, signs, old, np, check, True)
        diagnostic_cost = time.process_time()-mark
        current_labels = {k: names for k, (_, names) in groups.items()}
        if labels is not None and labels != current_labels: raise RuntimeError('Fixed observer labels changed')
        labels = current_labels
        prepared.append(dict(state=state, raw=raw, mass=mass, groups=groups, h=h, A=A,
            solved=solved, solution_arrays=solution_arrays, precondition=precondition,
            independent_signs=signs, independent_arrays=arrays, independent_report=report,
            identity=identity, balanced_signs=np.empty_like(signs), flights=[], flight_arrays=[]))
        costs.append(dict(label=state['label'], total_CPU=time.process_time()-started,
            complete_independent_diagnostics_CPU=diagnostic_cost))
    return prepared, costs, labels
