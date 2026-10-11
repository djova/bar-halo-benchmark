"""Fresh portable central l2 cycle; no numerical imports at module load.

The three scientific modules are preserved byte-for-byte. Execution requires
an externally chosen resource allowance; no saved orbit/history input exists.
"""
import argparse
from dataclasses import asdict
import json
import math
from pathlib import Path
import sys
import time

PACKAGE = Path(__file__).resolve().parent
if str(PACKAGE) not in sys.path:
    sys.path.insert(0, str(PACKAGE))
from portable_io import PortableIO, verify_package


PRESETS = {"gl8-preview": "configs/gl8-preview.json",
           "gl64-provisional": "configs/gl64-provisional.json"}
ORBIT_FIELDS = ("ne", "neta", "nmax", "radial_modes", "orbit_tolerance",
                "initial_solver_rtol", "minimum_solver_rtol", "maximum_refinements",
                "phase_step", "phase_panels", "phase_probe_order")
CYCLE_FIELDS = ("duration", "rise", "fall", "dt", "shape", "omega")
COEFFICIENTS = {"5": 3.795853269534006, "6": -135.59804126193885,
                "7": 678.294264313138, "8": -800.1997907110583,
                "10": 259.1199993421909, "12": -136.73855372860442}
PHYSICAL = dict(G=1.0, total_mass=1.0, radius=1.0, halo_mass=0.9, bar_mass=0.1)


def validate_definition(definition):
    if (definition.get("schema") != "portable-frozen-active-halo-population-v1"
            or definition.get("coefficients") != COEFFICIENTS
            or definition.get("reference_Q") != "14/33"
            or definition.get("physical") != PHYSICAL):
        raise ValueError("Exactly frozen physical population and source units required")


def validate_config(config):
    # The preserved module imports only the standard library; no backend work.
    from scientific.independent_orbits import OrbitConfig
    if set(config) != set(ORBIT_FIELDS+CYCLE_FIELDS):
        raise ValueError("Explicit complete orbital and physical cycle configuration required")
    orbital = OrbitConfig(**{key: config[key] for key in ORBIT_FIELDS})
    orbital.validate()
    if any(not math.isfinite(config[key]) for key in CYCLE_FIELDS):
        raise ValueError("Finite physical cycle controls required")
    if (min(config["dt"], config["duration"], config["rise"], config["fall"]) <= 0
            or config["rise"]+config["fall"] > config["duration"]
            or not 0 <= config["shape"] < 1
            or abs(config["duration"]/config["dt"]-round(config["duration"]/config["dt"])) > 1e-8):
        raise ValueError("Complete positive physical cycle and disclosed positive source amplitude required")
    return orbital


def preview(config, label, closure):
    """Integer sizes only: this does not create GL nodes or import a backend."""
    validate_config(config)
    actions = config["ne"]*config["neta"]
    harmonics = (2*config["radial_modes"]+1)*3
    basis = config["nmax"]+1
    times = round(config["duration"]/config["dt"])+1
    return dict(schema="portable-independent-cycle-preview-v1",
        configuration=config, configuration_label=label,
        target_status="Provisional reproduction target; qualification pending" if label == "gl64-provisional"
                      else "Configuration preview; no numerical execution",
        checksum_manifest_sha256=closure["package_sha256"],
        fresh_action_nodes=actions, signed_nk_harmonics_per_action=harmonics,
        driven_m=[-2, 2], populations=["F0", "A"], self_gravity=[0, 1],
        basis_count=basis, physical_time_count=times,
        principal_array_bytes=dict(radial_coefficients=8*actions*harmonics*basis,
            frequency_lattice=8*actions*harmonics,
            four_saved_complex_kernels=4*16*times*basis*basis,
            eight_saved_complex_wakes=8*16*times*basis,
            one_endpoint_complex_action_time_block=16*times*min(2048, actions*harmonics)),
        cost_scaling=dict(fresh_orbits=actions,
            kernel_terms=4*times*actions*harmonics*basis*basis,
            endpoint_orbit_potential_terms=8*times*actions*harmonics*basis,
            Volterra_history_terms=8*times*(times-1)//2*basis*basis),
        memory_scope="Array component counts, not peak RSS; orbit rows, solver temporaries and two endpoint blocks add memory",
        runtime_scope="No guaranteed CPU estimate; price the GL8 preview then the selected full configuration independently",
        scientific_qualification=False)


def run_cycle(config, io, definition, configuration_label="custom"):
    """Generate fresh inputs/orbits/kernel/fields/work using an injected I/O.

    A local metered wrapper may pass its own check/write/stop object. No host
    I/O class is imported by this package, and scientific globals are untouched.
    """
    verify_package(PACKAGE)
    validate_definition(definition)
    cfg = validate_config(config)
    io.check()
    started = time.process_time()
    stage = "inputs"
    io.write("inputs.json", dict(schema="portable-independent-cycle-inputs-v1",
        configuration=config, configuration_label=configuration_label,
        population=definition, fresh_orbit_construction=True,
        source_history="Symmetric quintic amplitude, exp(-2 i Omega t), physical signed pair",
        physical_time_unit="sqrt(a^3/(G Mtotal))=1",
        saved_scientific_payloads_consumed=False))
    progress = dict(schema="portable-independent-cycle-progress-v1", complete=False,
                    stage=stage, completed_signed_cells=[], scientific_qualification=False)
    io.write("progress.json", progress)
    # All numerical imports follow explicit input/source closure and I/O checks.
    import numpy as np
    import scipy
    from scipy.integrate import solve_ivp
    from scipy.optimize import brentq
    from scipy.special import eval_gegenbauer
    from scientific import independent_orbits as orbital, causal_response as response
    from scientific.volterra import solve, pulse
    backend = orbital.Backend(np, solve_ivp, brentq, eval_gegenbauer)
    coefficients = {int(key): value for key, value in definition["coefficients"].items()}
    try:
        stage = "fresh_orbit_library"
        progress.update(stage=stage)
        io.write("progress.json", progress)
        library = orbital.build_library(cfg, backend, io)
        angular = orbital.angular_moments(backend)
        io.write("orbit-library.npz", {key: value for key, value in library.items()
                                      if isinstance(value, np.ndarray)}, True, np)
        metric = response.spatial_metric(cfg.nmax, np, eval_gegenbauer, 128)
        norms = np.diag(metric)
        t = np.linspace(0, config["duration"], round(config["duration"]/config["dt"])+1)
        scalar = 3*definition["physical"]["bar_mass"]/(7*math.sqrt(30))
        positive, derivative, shape_derivative = pulse(t, config["duration"],
            config["rise"], config["fall"], config["shape"], config["omega"], np)
        saved = dict(time=t, spatial_metric=metric)
        rows = []
        populations = (("F0", {}), ("A", coefficients))
        for name, selected in populations:
            registers = []
            for m in (-2, 2):
                stage = f"kernel_{name}_m{m}"
                progress.update(stage=stage)
                io.write("progress.json", progress)
                kappa = orbital.contracted_derivative(library, selected, m, backend, angular)
                kernel = response.retarded_kernel(library, kappa, t, norms, np, io)
                b = np.zeros((len(t), cfg.nmax+1), complex)
                db, ds = b.copy(), b.copy()
                conjugate = lambda value: value.conj() if m == -2 else value
                b[:, 0] = scalar*conjugate(positive)
                db[:, 0] = scalar*conjugate(derivative)
                ds[:, 0] = scalar*conjugate(shape_derivative)
                saved[f"{name}_m{m}_kernel"] = kernel
                saved[f"{name}_m{m}_source"] = b
                saved[f"{name}_m{m}_source_derivative"] = db
                saved[f"{name}_m{m}_source_shape_derivative"] = ds
                registers.append(dict(m=m, raw_equal_time_kernel_real=kernel[0].real.tolist(),
                    raw_equal_time_kernel_imag=kernel[0].imag.tolist(),
                    kernel_initial_slope_proxy_real=((kernel[1]-kernel[0])/config["dt"]).real.tolist(),
                    kernel_initial_slope_proxy_imag=((kernel[1]-kernel[0])/config["dt"]).imag.tolist()))
                for own in (0, 1):
                    stage = f"cycle_{name}_m{m}_self{own}"
                    progress.update(stage=stage)
                    io.write("progress.json", progress)
                    c = solve(kernel, b, config["dt"], np, io, self_gravity=own)
                    history = response.work_history(c, b, db, ds, metric, t, np, m)
                    Q, J = response.endpoint_budget(library, kappa, b+own*c, t, norms, np, io, m)
                    field = .5*float(np.real(c[-1].conj()@metric@c[-1]))
                    row = dict(population=name, m=m, self_gravity=own,
                        W2=float(history["work"][-1]), J2=float(history["impulse"][-1]),
                        shape_W2=float(history["shape_work"][-1]),
                        rotational_W2=config["omega"]*float(history["impulse"][-1]),
                        orbit_Q2=Q, canonical_J2=J, self_U2=field,
                        raw_energy_budget_residual=Q+own*field-float(history["work"][-1]),
                        raw_impulse_budget_residual=J-float(history["impulse"][-1]))
                    rows.append(row)
                    saved[f"{name}_m{m}_self{own}_wake"] = c
                    for key, value in history.items():
                        saved[f"{name}_m{m}_self{own}_{key}"] = value
                    io.write("checkpoint.npz", saved, True, np)
                    progress.update(completed_signed_cells=list(rows),
                                    process_CPU_seconds=time.process_time()-started)
                    io.write("progress.json", progress)
                    print(json.dumps(dict(stage=stage, **row), allow_nan=False), flush=True)
                saved[f"{name}_raw_kernel_diagnostics"] = np.asarray(json.dumps(registers))
        totals = []
        for name, unused in populations:
            for own in (0, 1):
                selected_rows = [row for row in rows if row["population"] == name
                                 and row["self_gravity"] == own]
                values = {key: sum(row[key] for row in selected_rows) for key in
                    ("W2", "J2", "shape_W2", "rotational_W2", "orbit_Q2", "canonical_J2",
                     "self_U2", "raw_energy_budget_residual", "raw_impulse_budget_residual")}
                reality = float(np.max(np.abs(saved[f"{name}_m-2_self{own}_wake"]
                                              -saved[f"{name}_m2_self{own}_wake"].conj())))
                totals.append(dict(population=name, self_gravity=own,
                                   conjugate_wake_error=reality, **values))
        stage = "complete_outputs"
        io.check()
        io.write("history.npz", saved, True, np)
        result = dict(schema="portable-independent-cycle-result-v1", complete=True,
            config=config, orbit_config=asdict(cfg), configuration_label=configuration_label,
            numerical_versions=dict(python=sys.version.split()[0], numpy=np.__version__, scipy=scipy.__version__),
            results=totals, signed_cells=rows, physical_source_scalar=scalar,
            physical_halo_mass=orbital.physical_mass(library, backend),
            orbit_construction_CPU_seconds=library["construction_CPU_seconds"],
            total_child_CPU_seconds=time.process_time()-started,
            maximum_orbit_refinement_proxy=np.max(library["quadrature_errors"], axis=0).tolist(),
            signed_n=list(range(-cfg.radial_modes, cfg.radial_modes+1)), inplane_k=[-2, 0, 2],
            driven_m=[-2, 2], fresh_orbits=True, raw_Ward_registers_preserved=True,
            no_empirical_mass_normalization=True, no_kernel_repair=True,
            saved_scientific_payloads_consumed=False,
            independence="Reproduction of the same frozen independent method, not a third independent construction",
            reproduction_equivalence_verified=False, scientific_qualification=False,
            target_provisional=True,
            qualification="Complete numerical cycle only; independent refinements, portable equivalence and final target selection remain pending")
        io.write("result.json", result)
        progress.update(complete=True, stage=stage, completed_signed_cells=list(rows))
        io.write("progress.json", progress)
        return result
    except BaseException as error:
        # A stop or output failure may prevent this write; prior progress remains.
        try:
            io.write("failure.json", dict(complete=False, stage=stage,
                error_type=type(error).__name__, error=str(error), completed_signed_cells=list(progress["completed_signed_cells"]),
                scientific_qualification=False))
        except BaseException:
            pass
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--preset", choices=tuple(PRESETS), default="gl8-preview")
    parser.add_argument("--output")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--expected-manifest-sha256")
    for name in ORBIT_FIELDS+CYCLE_FIELDS:
        parser.add_argument("--"+name.replace("_", "-"), type=int if name in
            ("ne", "neta", "nmax", "radial_modes", "maximum_refinements", "phase_panels", "phase_probe_order") else float)
    parser.add_argument("--ramp", type=float, help="Compatibility shorthand setting both rise and fall")
    args = parser.parse_args(argv)
    if args.ramp is not None and (args.rise is not None or args.fall is not None):
        raise ValueError("Use either symmetric --ramp or explicit --rise/--fall")
    closure = verify_package(PACKAGE, args.expected_manifest_sha256)
    config = json.loads((PACKAGE/PRESETS[args.preset]).read_text())["config"]
    changed = False
    for name in ORBIT_FIELDS+CYCLE_FIELDS:
        value = getattr(args, name)
        if value is not None:
            config[name] = value
            changed = True
    if args.ramp is not None:
        config.update(rise=args.ramp, fall=args.ramp)
        changed = True
    label = args.preset+("-overrides" if changed else "")
    definition = json.loads((PACKAGE/"inputs/population.json").read_text())
    validate_definition(definition)
    validate_config(config)
    if args.preview:
        print(json.dumps(preview(config, label, closure), indent=2, allow_nan=False))
        return
    if not args.output:
        raise ValueError("Execution requires an explicit fresh --output directory")
    io = PortableIO(PACKAGE, args.output, config, label, args.expected_manifest_sha256)
    try:
        result = run_cycle(config, io, definition, label)
        io.terminal(True, "complete_outputs")
        print(json.dumps(dict(complete=True, signed_cells=len(result["signed_cells"]),
            total_child_CPU_seconds=result["total_child_CPU_seconds"], scientific_qualification=False)), flush=True)
    except BaseException as error:
        try:
            io.terminal(False, "failed", error)
        except BaseException:
            pass
        raise


if __name__ == "__main__":
    main()
