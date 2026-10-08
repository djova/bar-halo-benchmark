# Equations and provenance of the portable collective port

The physical model is G=M=a=1, total Plummer potential, fixed spherical bar
monopole Mb=.1, and stationary halo density
3/(4pi)*(1+r²)^(-5/2)-15Mb/(8pi)*(1+r²)^(-7/2). The published family is
F/C=e^(7/2)*(1-q*e²)+Lz*h(e,L²), q=14/33,
C=24sqrt2/(7pi³). Its actual six-power vectors and represented attenuation
are read from the exact adjacent bare runner; they are not fitted or replaced.

Actions are (Jr,L,Lz), with binding e=-H0, node frequency zero and
nu=n*Omega_r+k*Omega_L. The full DF contraction is

    kappa/C=-nu*g0_e+m*h+L*mu*(2*k*L*h_L2-nu*h_e), mu=Lz/L.

The L derivative holds Lz fixed. The m*h nodal derivative remains despite the
zero nodal frequency. The exact orientation integrals for l2 in unnormalized
dmu are A_k=(3/4,1/2,3/4), B_mk=A_k*m*k/6, k=-2,0,+2. Each DF's own
contracted kappa uses both terms; self-consistent outcomes are not linearly
reweighted from an F0 or endpoint solution.

For this affine-Lz family in the unforced central reference, constant plus
rank-one inclination weighting and equatorial parity close each l response
block. This is not generic axisymmetric-DF angular decoupling. With zero
initial generator and prescribed quadrupole forcing, only m=-2,+2 evolve;
the explicit zero m0/±1 coefficients are not stability evidence. The proper
rotation Ry(pi) reverses Lz and exchanges m/-m, so the full A± unforced spectra
are identical.
Drive-handedness comparisons retain their separate prescribed-field meaning.

The orbital measure is (2pi)^3*Lc²*eta/Omega_r de deta dmu, full0<e<1 and
0<eta=L/Lc<1. Gaussian nodes cover the whole compactified action domain.
The existing analytic angular pole and adjacent GL8/16/32 phase panels are
used. Every signed radial n=-N..N and in-plane k remains, with no resonance
approximation. The adaptive orbit criterion compares frequencies/Jr, all CB
Fourier coefficients normalized by their value norms, Parseval derivative
norms and phase. An unresolved node aborts; tail proxies are not response bounds.

CB radial phi_n2=-r²*(1+r²)^(-5/2)*C_n^3((r²-1)/(r²+1)). The derivative
uses dC_n^3/dchi=6*C_(n-1)^4. Harmonic angular norm is4pi. The negative
physical density-potential norm is generated from lambda=l+1=3 by the frozen
log-gamma prefactor and exact n recurrence, and checked independently against
unbounded physical-r Poisson density integration. Its sign is never replaced
by an absolute value. All nCB0..nmax fields are retained; only nCB0 of the
external physical bar is nonzero, with b_m=3Mb/(7sqrt30)*shape(t)*exp(-im*theta).

The generator obeys the existing implicit midpoint equations. Drift is
(1-i*dt*nu/2)/(1+i*dt*nu/2), force is dt/(1+i*dt*nu/2), and
projection is i*sum(weight*kappa*R*g)/I_n2. Each population and forced m has
its own small Schur solve for the midpoint field. Both conjugate m and signed
n/k partners, complex CS reality, and canonical one-half factors are retained.
The port allocates a successor generator and commits only after a finite
fresh projection; it does not change the midpoint equations.

For each DF, Q=-.5 sum(weight*kappa*nu*|g|²), J=-.5
sum(weight*kappa*m*|g|²), U=.5 sum(I_n2*|c|²), and U_included=sg*U.
External interaction V=sum(I_n2*Re(c*conj(b))). Shape work accumulates
dt*sum(I_n2*Re(conj(c_mid)*b_shape_rate)), and angular impulse accumulates
dt*sum(I_n2*Re(conj(c_mid)*(-i*m*b_mid))). Thus physical work is Wshape+Omega*Jbar.
The physical residual is Delta(Q+U_included)+V-Wshape-Omega*Jbar; the angular
residual is DeltaJ-Jbar. Actual initial Q/J/U and coefficients are retained.
For a driven record with nonzero V, Q+U alone is not the physical energy.

The exact midpoint discrete flux is separately accumulated as
sum I*Re(conj(c_mid)*Delta b+conj(Delta c)*[(b_before+b_after)/2-b_mid]).
It tests discrete algebra and never replaces physical work. The F0 l2 energy
bound gap is only a continuum benchmark for that positive-F_e reference; it
does not qualify mixed DFs or a finite discretization. Zero-drive/zero-seed
control uses the actual constructed operator and requires exact zero registers.

`run.py` records its own local source/document hashes, exact bare dependency
hash, NumPy/SciPy/Python versions, coefficients, all explicit controls and the
qualified-source ancestor hashes. Ancestors are attribution, not runtime
imports or a claim of independent implementation. This source-only preparation
has not executed formulas, arrays, histories or reference comparisons. A root
metered quick fixture and same-config collective reference comparison remain
necessary before any numerical-method adoption; scientific continuum/stability
claims additionally require the established independent physical/refinement
controls. Original bare source and releases are immutable.
