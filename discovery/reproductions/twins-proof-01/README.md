# Portable unforced algebra challenge

The [result](result.json) reproduces the three exact rational Bernstein bounds,
zero streaming coefficients, factorial DF recurrence and Decimal potential
checks using frozen unforced operands. The optional alpha comparison used
mpmath 1.3.0 at 80 digits and agreed with each frozen float within 1.3e-16
relative. The rational proof adapter itself requires no external dependency.

This is a software/arithmetic repetition of the independent internal challenge,
not outside review, proof-assistant certification, floating-point interval
analysis, sampling, bar evolution or collective-stability validation.
