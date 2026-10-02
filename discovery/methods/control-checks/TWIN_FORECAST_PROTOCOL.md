# Frozen scientific forecast protocol

Scientific excerpt of the prospective protocol sealed before independent forced
outcomes. Its full archive SHA-256 is 926b131a63dabb1790cd6ab05aefa40052b87627bc46693d47c6dbbba8ec2652.
The fixed history is amplitude 0.0001, quintic ramp10, endpoint40, no sweep,
and pattern speed from actions (0.08,0.05,0.30). Populations p=4,6,8 remain
frozen. This excerpt omits private execution coordination, not scientific
conditions or error criteria.

## Correct quantity and measure

For the positive m=2 sector, including its conjugate, calculate

\[
\Delta L_{z,+}^{(2)}-\Delta L_{z,-}^{(2)}
=-2(2\pi)^3\sum_{n_r,k}\int dJ_r\,dL\,
2\alpha_p L\{2h_p I_k+L[2kLe^p-h_{p,e}(n_r\Omega_r+k\Omega_L)]M_k\}
|R_{n_rk}|^2|\mathcal I_{n_rk}|^2.
\]

Here Iminus=Iplus=2/5, I0=4/15, Mminus=-4/15, Mplus=4/15, M0=0.
The potential coefficient R contains -rb^3/2. Its real-field one-half must not
be removed. Positive response denotes more angular momentum transferred to
Fplus than Fminus. This is accumulated physical Lz, not Js=Lz/2, instantaneous
torque, a percentage or a per-window renormalized mean.

The complete energy/circularity domain is e in (0,1), ell in (0,1), with
L=ell Lmax(e) and Jacobian dJr dL=Lmax/Omega_r de dell. Keep all interior
quadrature nodes, including low-energy radial orbits. Use the independently
derived anomaly phases, exact radial Jacobian and all integer radial modes
within each declared symmetric range. No resonance-only list or asymptotic
LBK delta function is permitted.

For numerical stability, evaluate u-b as L^2/(A+zeta)+2a zeta sin^2(eta/2),
where A=1-e and zeta=A sqrt(1-ell^2). This is the algebraic identity obtained
from (A-zeta)(A+zeta)=L^2/a. It avoids cancellation in the positive radial
radius; it changes neither the Hamiltonian nor the radial phase convention.

## Frozen numerical matrix

Record seven complete coefficient/contraction cases:

| ID | Energy x circularity nodes | Anomaly nodes | Radial modes |
| --- | --- | ---: | --- |
| a | 32 x 24 | 512 | -64..64 |
| b | 32 x 24 | 1024 | -64..64 |
| c | 32 x 24 | 1024 | -128..128 |
| d | 64 x 48 | 512 | -128..128 |
| e | 64 x 48 | 1024 | -128..128 |
| f | 96 x 72 | 512 | -128..128 |
| g | 96 x 72 | 1024 | -128..128 |

Save complete complex coefficients, continuous value/derivative norms, weights,
Jacobian, signed mode contributions for all p, detunings, Hessian/libration
proxies and reference-DF mass weights. Keep signed and absolute contractions
separate. The reference F0 mass integral is a normalization diagnostic, not
an operation that rescales any population.

## Tail allowances and limitations

For an exact radial function, its derivative norm Q is sum n^2|R_n|^2.
Thus omitted power above N is at most Q/(N+1)^2 and its |n|-weighted power
at most Q/(N+1). The twin-gradient absolute envelope has a constant term plus
a term linear in |n|. Combine these with the exact history bound
|I|<=epsilon(T-ramp/2). Where (N+1)Omega_r exceeds
abs(k Omega_L-2Omega_p), sharpen it with
|I|<=2epsilon/[(N+1)Omega_r-abs(k Omega_L-2Omega_p)].

Report both the full-derivative-norm tail proxy and a residual-norm proxy that
subtracts the retained spectral derivative norm. For paired anomaly orders,
the residual adds twice the sum of the absolute direct-norm change and the
absolute retained-spectral-norm change. Negative roundoff residuals are set
to zero before adding that proxy; the unmodified norms and differences are
saved. These measured quadratures and factors do not make rigorous error
bounds or establish coverage. Loose tails remain unresolved; no difficult
cell or high-harmonic family is deleted.

The final numerical allowance sums the final anomaly-order response change,
the 64x48-to-96x72 action-grid response change, and the final residual tail
proxy. A family is provisionally qualified to 5% numerically only when this
allowance is at most 0.05 times its absolute forecast. A numerical sign is
qualified only when the allowance is smaller than the forecast magnitude.
This qualification does not establish weak-model applicability.

Report libration-phase proxies and, separately, their absolute mode-weighted
contribution fractions and reference-DF mass. Near means
abs(detuning)<=2pi/T. Report phase thresholds0.3,0.5,1.0. A large unweighted
maximum alone is not an integrated error estimate; a small contribution
fraction is also not a proof of nonlinear validity. Independent forced
evolution with the frozen forecast, fixed half-amplitude comparison and
numerical controls is required for that next inference.

