# Fresh execution of the public known-limit controls

The sources in this clean package were run with Python 3.11.14, NumPy 1.26.4,
SciPy 1.17.1 and Matplotlib 3.11.2. Each of three sequential numerical children
used one numerical thread and nice=10 with a finite 180-second wall limit.
The unchanged known-limit gates all passed.

The [receipt](receipt.json) records **59.426331 child CPU-seconds** in total:
0.774840 seconds for harmonic inertia, 0.493671 seconds for the elastic operator,
and 58.157820 seconds for the constant-shear echo. Wall time was approximately
59.5 seconds. These costs include numerical-child import/setup time; the
parent's bookkeeping and manual inspection are not included.

The selected q=2,4,8 first/second harmonic frequencies equal the published export
operands exactly on this execution. The operator's fourth angular-decay ratio
is exactly 53/32. The four gate fields are harmonic reference, conservative
operator, fourth angular ratio and constant-shear echo. Individual source hashes
are retained in the receipt; scientific outputs are stored in the three named
subdirectories. Process IDs are omitted from the clean harmonic/operator JSON
copies; numerical values are unchanged and the manifest records both generated
and released hashes. The known-echo PNG and PDF reproduce that control's visual
comparison, not the halo readout.

This is a fresh run from the public-source directory using equations and seeds,
not a receipt copied from the original physical campaign. It is not a fresh
physical sample or independent validation of live galaxies, halo echo amplitudes,
collision-law ensemble significance, selective heating, halo twins or
observations. A dependency build or every optional full-response command was
not executed here.
