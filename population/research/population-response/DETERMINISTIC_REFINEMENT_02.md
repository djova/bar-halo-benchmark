# One further moving characteristic grid comparison

The first independent remainder matrix is complete. At both times the halo and
exponential pass all declared numerical/window comparisons. The moving Gaussian
atT20fails: doubled action/angle resolution changes the collisionless impulse
by0.0005488918408267374, above the unchanged2e-4 target. Its timestep change is
3.16e-9 and physical-window change is7.95e-10. This localizes the observed failure
to quadrature, not the modeled population, noise, background or integration step.
It does not make the original coarse result qualified.

The measured fine calculation costs310.65CPU seconds. Freeze ONE further doubled
action/angle grid: moving s.25,J160,nj40960,nphi1024,dt.025,phase chunk8. Retain
all six absolute profiles andT10/T20. The projected cost is1243CPU seconds;
allow2400CPU seconds and1800wall seconds, one nice10single-thread worker. This
fits the open third slot while the independent validation uses two workers.

Compare the new grid against the previous fine grid at the same2e-4 absolute
target. Preserve the first failed base/fine comparison, and report both changes.
All previous timestep, boundary and physical-window checks remain visible. A
fine-grid difference below the target is an observed convergence check, not a
rigorous bound or a statistical replication. If this single further comparison
fails, retain that limitation; no additional quadrature ladder is preauthorized
by this supplement. The decisive halo-population test is not conditional on
turning the selected-Gaussian failure into a pass.
