# Inspection snapshots of the executed control methods

[Provenance](provenance.json) identifies the archived source/figure hashes and
any documentation-only link adaptation. Python sources are byte-identical
inspection snapshots of their executed versions. They retain historical
relative archive dependencies and process limits. They are not standalone
execution commands and should not be imported merely to read the publication.

- `twins_single_position_completion.py`: unique-position live unforced matrix.
- `export_control_checks_v1.py`: extraction of terminal saved records, with no
  evolution. It requires the retained campaign archive.
- `twins_phase_control.py`: same-sample analytic orbital-phase control.
- `feedback_cusp_warm_pilot.py`: finite warm-target radial pilot.
- `feedback_cusp_warm_radial.py` and `feedback_cusp_radial.py`: canonical radial
  target, action/period and effective-potential calculations.
- `feedback_cusp_warm_reference.py`: tighter exact-path radial/Cartesian reference.
- `feedback_cusp_warm_readback.py`: original comprehensive saved-operand diagnosis.
- `echo_finite_preflight.py`: original finite spatial exact-zero preflight.
- `echo_finite_diagnostic_completion.py`: frozen nine-direction continuation.
- `echo_finite_energy_pair.py`: later frozen two-row energy-only continuation.

The [portable saved-arithmetic reader](../../scripts/discovery/replay_checks_v1.py)
is separately adapted to the supplied compact public operands. It requires only
NumPy and performs no physical evolution. The [control narrative](../../CHECKS.md)
links every named protocol and distinguishes numerical checks from physical
inferences. Existing public echo helpers remain in the broader source package,
but the exact finite spatial archive needed by these inspection snapshots is not
redistributed as a complete rerun bundle.
