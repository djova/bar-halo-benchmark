"""Independent finite readback of unforced identities; no orbit data are read.

The Bernstein boxes use direct affine power substitution, not the original
de Casteljau subdivision implementation. The DF series comes from factorial
evaluation of the Beta coefficients, not their original recurrence.
"""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from math import comb, factorial
from pathlib import Path
import hashlib
import json
import time


def beta_integer_half(n, q):
    """B(n,q+1/2), evaluated exactly for positive integer n and q."""
    return F(4**n * factorial(n-1) * factorial(2*q) * factorial(n+q),
             factorial(q) * factorial(2*(n+q)))


def shape_coefficient(n):
    return F(5 * (n+1) * (n+4)**2 * (n+3) * 4**(n+3) *
             factorial(n+2) * factorial(n+3),
             256 * 2**n * factorial(2*n+6))


def affine_power_coefficients(power, left_e, left_t, step):
    out = {}
    for (k, ell), value in power.items():
        for i in range(k+1):
            epart = value * comb(k, i) * left_e**(k-i) * step**i
            for j in range(ell+1):
                key = (i, j)
                out[key] = out.get(key, F(0)) + epart * comb(ell, j) * left_t**(ell-j) * step**j
    return out


def to_bernstein(power):
    return [[sum((v * F(comb(i, k), comb(12, k)) *
                  F(comb(j, ell), comb(3, ell))
                  for (k, ell), v in power.items() if k <= i and ell <= j), F(0))
             for j in range(4)] for i in range(13)]


def independent_bound(p):
    a = F(16*p, (2*p+5)*(2*p+7))
    bcoef = F(8, 2*p+7)
    num = {(p-4, 1): -a, (p-3, 1): a+bcoef, (p-2, 1): -bcoef,
           (p-4, 3): F(1, 2), (p-3, 3): F(-3, 2),
           (p-2, 3): F(3, 2), (p-1, 3): F(-1, 2)}
    den = {(k, 0): shape_coefficient(k) for k in range(13)}
    maximum = F(0)
    minimum_denominator = None
    winner = None
    for ie in range(16):
        d = to_bernstein(affine_power_coefficients(den, F(ie, 16), F(0), F(1, 16)))
        for it in range(16):
            h = to_bernstein(affine_power_coefficients(num, F(ie, 16), F(it, 16), F(1, 16)))
            for i in range(13):
                for j in range(4):
                    assert d[i][j] > 0
                    minimum_denominator = d[i][j] if minimum_denominator is None else min(minimum_denominator, d[i][j])
                    ratio = abs(h[i][j])/d[i][j]
                    if ratio > maximum:
                        maximum, winner = ratio, [ie, it, i, j]
    return maximum, minimum_denominator, winner


def decimal_potential_readback():
    rows = []
    with localcontext() as context:
        context.prec = 70
        b = Decimal('.5')
        for token in ('1e-8', '.001', '.1', '1', '30', '1e8'):
            r = Decimal(token)
            z = (b*b+r*r).sqrt()
            psi = 1/(b+z)
            # Independently differentiate r^2 Psi'(r), omitting common 4pi.
            density_derivative = 3*psi**2/z - 2*r*r*psi**3/z**2 - r*r*psi**2/z**3
            density_potential = b*(2-b*psi)*psi**4/(1-b*psi)**3
            radius_identity = 1/psi**2 - 2*b/psi
            vc2 = r*r*psi**2/z
            ec = psi-vc2/2
            lc2 = r*r*vc2
            lmax2 = (1-ec)**2/(2*ec)
            rows.append(dict(radius=token,
                density_relative_difference=str(density_derivative/density_potential-1),
                radius_relative_difference=str(radius_identity/(r*r)-1),
                circular_L2_relative_difference=str(lc2/lmax2-1)))
    return rows


def main():
    started_cpu = time.process_time()
    base = Path(__file__).resolve().parents[2]
    folder = base/'results/discovery-20261001/twins/exact-moments-preflight-02'
    record = json.loads((folder/'result.json').read_text())
    results = []
    for published in record['populations']:
        p = published['p']
        a = F(16*p, (2*p+5)*(2*p+7))
        bcoef = F(8, 2*p+7)
        first = -a*beta_integer_half(p, 2)+F(8, 5)*beta_integer_half(p+1, 3)
        second = bcoef*beta_integer_half(p+1, 2)-F(8, 5)*beta_integer_half(p+1, 3)
        assert first == second == 0
        bound, min_den, winner = independent_bound(p)
        expected = F(published['polynomial_ratio_upper_numerator'], published['polynomial_ratio_upper_denominator'])
        assert bound == expected
        results.append(dict(p=p, both_streaming_coefficients_exactly_zero=True,
            independently_rebuilt_bound_numerator=bound.numerator,
            independently_rebuilt_bound_denominator=bound.denominator,
            equals_published_bound=True, minimum_denominator_coefficient=str(min_den),
            maximizing_box_and_coefficient=winner))
    series = [shape_coefficient(n) for n in range(97)]
    ratios = [series[n+1]/series[n] for n in range(96)]
    assert series[0] == 1
    assert all(ratios[n] == F((n+2)*(n+5)**2, (n+1)*(n+4)*(2*n+7)) for n in range(96))
    assert all(ratio <= F(3, 4) for ratio in ratios[6:])
    decimal_rows = decimal_potential_readback()
    assert all(abs(Decimal(r[key])) < Decimal('1e-48') for r in decimal_rows
               for key in ('density_relative_difference', 'radius_relative_difference', 'circular_L2_relative_difference'))
    summary = dict(scope='Independent unforced algebra and source-record challenge; no particle sampling or integration',
        populations=results, factorial_series_matches_recurrence_through_n96=True,
        checked_ratio_tail_bound_after_n6=True, decimal_potential_and_circular_domain_checks=decimal_rows,
        archived_source_hash_matches=hashlib.sha256((folder/'source.py').read_bytes()).hexdigest()==record['source_sha256'],
        archived_protocol_hash_matches=hashlib.sha256((folder/'protocol.md').read_bytes()).hexdigest()==record['protocol_sha256'],
        cpu_seconds=time.process_time()-started_cpu,
        limitations=['Not a proof assistant or floating-point interval audit',
                    'No sampling implementation for exact Fplus/Fminus has been executed',
                    'No collective stability, bar response or observational outcome evaluated'])
    output = Path(__file__).with_suffix('.json')
    if output.exists():
        raise FileExistsError(output)
    output.write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
