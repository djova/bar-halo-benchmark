"""Check saved paired records; this command does not evolve orbits or certify errors."""
import argparse
import csv
import json
import math
from pathlib import Path
import statistics

OMEGA0 = 0.5946035575013605
T_QUANTILES = {4: 3.182446305284263, 8: 2.3646242515927844}
PAIRS = (("plus", "minus"), ("plus", "F0"), ("minus", "F0"))
POSTRELEASE_COLUMNS = ("postrelease_bar_impulse", "autonomous_energy_residual",
                       "actual_rotor_K_exchange", "postrelease_rotor_bar_residual")
NUMERIC_COLUMNS = ("nominal_time", "omega", "theta", "rotor_L", "total_bar_impulse",
                   "shape_work", "pattern_work", "postrelease_bar_impulse",
                   "autonomous_energy_residual", "actual_rotor_K_exchange",
                   "postrelease_rotor_bar_residual", "actual_time")


def records(path, expected_seeds, fields, variants):
    groups = {}
    with Path(path).open(newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["variant", "seed", "field", "population", *NUMERIC_COLUMNS]:
            raise ValueError("Exact published scalar columns required")
        for row in reader:
            if set(row) != set(reader.fieldnames) or any(v is None for v in row.values()):
                raise ValueError("Missing or extra CSV cell")
            key = (row["variant"], int(row["seed"]), row["field"], row["population"])
            if key[0] not in variants or key[1] not in expected_seeds or key[2] not in fields or key[3] not in ("F0", "plus", "minus"):
                raise ValueError("Unexpected library/treatment coordinate")
            time = float(row["nominal_time"])
            if time in groups.setdefault(key, {}):
                raise ValueError("Duplicate saved node")
            values = {k: (None if v == "" else float(v)) for k, v in row.items()
                      if k not in ("variant", "seed", "field", "population")}
            if any(v is not None and not math.isfinite(v) for v in values.values()):
                raise ValueError("Nonfinite supplied numeric operand")
            groups[key][time] = values
    expected = {(v, s, f, p) for v in variants for s in expected_seeds for f in fields for p in ("F0", "plus", "minus")}
    if set(groups) != expected or any(set(g) != set(range(0, 201, 2)) for g in groups.values()):
        raise ValueError("Missing complete paired library, population, or saved node")
    for history in groups.values():
        for t, row in history.items():
            for k in POSTRELEASE_COLUMNS:
                if (t < 20) != (row[k] is None):
                    raise ValueError("Incorrect pre-release missing-value semantics")
            if any(row[k] is None for k in NUMERIC_COLUMNS if k not in POSTRELEASE_COLUMNS):
                raise ValueError("Missing applicable recorded operand")
            if not math.isclose(row["actual_time"], t, rel_tol=0, abs_tol=1e-8):
                raise ValueError("Actual integration clock differs from the recorded node")
    return groups


def quantity(history, observable):
    if observable == "endpoint":
        return history[200.0]["omega"] / OMEGA0
    if observable != "late_window":
        raise ValueError("Unknown predeclared observable")
    # Trapezoid of the eleven recorded 180--200 nodes, not continuous-time integration.
    return math.fsum(history[t]["omega"] + history[t + 2]["omega"]
                     for t in range(180, 200, 2)) / (20 * OMEGA0)


def interval(values):
    n = len(values)
    mean = statistics.mean(values)
    half = T_QUANTILES[n] * statistics.stdev(values) / math.sqrt(n)
    return mean, [mean - half, mean + half]


def nearly_equal(a, b):
    return math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-12)


def evaluate(directory):
    directory = Path(directory)
    published = json.loads((directory / "results.json").read_text())
    b = records(directory / "baseline-recorded-operands.csv", range(7510101, 7510109), ("fixed_halo", "responsive"), ("baseline",))
    g = records(directory / "growth-recorded-operands.csv", range(7510101, 7510105), ("responsive",), ("baseline", "refined"))
    for key, history in g.items():
        if key[0] == "baseline" and history != b[key]:
            raise ValueError("Growth comparator must use identical first-four baseline records")
    verified = []
    for scope, supplied in (("baseline", published["baseline_contrasts"]), ("growth", published["growth_contrasts"])):
        roles = ("fixed_halo", "responsive", "responsive_minus_fixed") if scope == "baseline" else ("responsive",)
        estimators = ("baseline_eight",) if scope == "baseline" else ("baseline_same_four", "refined_same_four", "refined_minus_baseline_same_four")
        expected = {(o, f, p, e) for o in ("endpoint", "late_window") for f in roles for p in PAIRS for e in estimators}
        coordinates = [(r["observable"], r["field_role"], tuple(r["populations"]),
                        r.get("estimator", "baseline_eight")) for r in supplied]
        if len(coordinates) != len(expected) or set(coordinates) != expected:
            raise ValueError("Exactly all eighteen distinct declared comparisons required")
        for row in supplied:
            seeds = range(7510101, 7510109 if scope == "baseline" else 7510105)
            values = []
            for seed in seeds:
                def contrast(dataset, variant, field):
                    left, right = row["populations"]
                    return quantity(dataset[(variant, seed, field, left)], row["observable"]) - quantity(dataset[(variant, seed, field, right)], row["observable"])
                if scope == "baseline":
                    role = row["field_role"]
                    value = (contrast(b, "baseline", "responsive") - contrast(b, "baseline", "fixed_halo")) if role == "responsive_minus_fixed" else contrast(b, "baseline", role)
                else:
                    estimator = row["estimator"]
                    c, a = contrast(g, "refined", "responsive"), contrast(g, "baseline", "responsive")
                    value = {"refined_same_four": c, "baseline_same_four": a, "refined_minus_baseline_same_four": c - a}[estimator]
                values.append(value)
            mean, band = interval(values)
            stored_band = row["nominal_pointwise_t7_interval" if scope == "baseline" else "nominal_pointwise_t3_interval"]
            if len(stored_band) != 2 or not nearly_equal(mean, row["signed_mean_C"]) or not all(nearly_equal(a, v) for a, v in zip(band, stored_band)):
                raise ValueError("Published aggregate does not reconstruct from its paired operands")
            folded = ([0., max(map(abs, band))] if band[0] <= 0 <= band[1]
                      else [min(map(abs, band)), max(map(abs, band))])
            stored_folded = row["zero_aware_folded_interval"]
            absolute_key = "absolute_of_signed_ensemble_mean" if scope == "baseline" else "absolute_of_signed_mean"
            if (len(stored_folded) != 2 or not nearly_equal(abs(mean), row[absolute_key]) or
                    not all(nearly_equal(a, v) for a, v in zip(folded, stored_folded))):
                raise ValueError("Absolute display must fold the signed ensemble interval through zero")
            count_key = "independent_whole_libraries" if scope == "baseline" else "whole_paired_libraries"
            if (row[count_key] != len(values) or row["calibrated_coverage"] is not False or
                    row["mean_absolute_draws_not_used"] is not True):
                raise ValueError("Preserve whole-library sampling and nominal uncertainty scope")
            verified.append({"scope": scope, "observable": row["observable"], "field": row["field_role"], "populations": row["populations"], "estimator": row.get("estimator", "baseline_eight"), "individual_signed_C": values, "mean": mean, "nominal_interval": band})
    primary = next(r for r in verified if r["scope"] == "baseline" and r["observable"] == "endpoint" and r["field"] == "responsive" and r["populations"] == ["plus", "minus"])
    shift = next(r for r in verified if r["scope"] == "growth" and r["observable"] == "endpoint" and r["estimator"] == "refined_minus_baseline_same_four" and r["populations"] == ["plus", "minus"])
    allowance = max(map(abs, shift["nominal_interval"]))
    threshold = min(.02, .20 * abs(primary["mean"]))
    decompositions = []
    for seed in range(7510101, 7510105):
        for population in ("F0", "plus", "minus"):
            a, c = g[("baseline", seed, "responsive", population)], g[("refined", seed, "responsive", population)]
            release_shift = c[20]["total_bar_impulse"] - a[20]["total_bar_impulse"]
            free_shift = c[200]["postrelease_bar_impulse"] - a[200]["postrelease_bar_impulse"]
            total_shift = c[200]["total_bar_impulse"] - a[200]["total_bar_impulse"]
            if not nearly_equal(release_shift + free_shift, total_shift):
                raise ValueError("Release plus autonomous impulse decomposition does not close")
            decompositions.append({"seed": seed, "population": population, "release_impulse_shift": release_shift, "postrelease_impulse_shift": free_shift, "total_impulse_shift": total_shift})
    return {"status": "saved-record arithmetic agrees", "reconstructed_contrasts": verified,
            "growth_impulse_decomposition": decompositions,
            "necessary_policy_checks": {"baseline_interval_contains_zero": primary["nominal_interval"][0] <= 0 <= primary["nominal_interval"][1], "single_growth_arm_proxy": allowance, "magnitude_share_ceiling": threshold, "single_growth_arm_exceeds_ceiling": allowance > threshold},
            "does_not_verify": ["forces or trajectories", "full numerical convergence", "true-error bounds or calibrated confidence coverage", "physical stability", "observations"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(evaluate(args.directory), indent=2, allow_nan=False))
