"""Analytical local velocity marginals of the frozen unforced populations.

These are equation evaluations, not simulation snapshots or torque predictions.
The integral over the other two velocities is checked by separate quadrature.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import argparse,hashlib,json,time
import numpy as np
from numpy.polynomial.legendre import leggauss
import twins_exact_moments as m


def marginal(v, r, pop):
    psi=1/(.5+np.sqrt(.25+r*r))
    upper=np.maximum(psi-.5*v*v,0)
    # f0=a0 e^(5/2) sum s_n e^n; integrate e from0 to upper.
    base=2*np.pi*m.A0*upper**3.5*np.polynomial.polynomial.polyval(
        upper,m.SERIES/(np.arange(len(m.SERIES))+3.5))
    p=pop['p']; a=4*p/((p+2.5)*(p+3.5)); b=4/(p+3.5)
    odd=2*np.pi*r*v*(-a*upper**p/p+b*upper**(p+1)/(p+1)
        +r*r*(v*v*upper**(p+1)/(p+1)+upper**(p+2)/((p+1)*(p+2))))
    density=m.rho(psi)
    return base/density,pop['alpha']*odd/density


def numerical(v,r,pop,order):
    psi=1/(.5+np.sqrt(.25+r*r));upper=max(psi-.5*v*v,0)
    q,w=leggauss(order);e=upper*(q+1)/2;w=w*upper/2
    p=pop['p'];g0=-4*p/((p+2.5)*(p+3.5))*e**(p-1)+4/(p+3.5)*e**p
    odd=r*v*(g0+r*r*(v*v+upper-e)*e**p)
    return 2*np.pi*np.array([m.f0(e)@w,pop['alpha']*(odd@w)])/m.rho(psi)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--frozen',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=False);cpu=time.process_time()
    frozen=json.loads(args.frozen.read_text());assert m.sha(m.__file__)==frozen['source_sha256']
    for path in [Path(__file__),Path(m.__file__),args.frozen]:
        (args.out/path.name).write_bytes(path.read_bytes())
    r=1.;psi=1/(.5+np.sqrt(.25+r*r));escape=np.sqrt(2*psi)
    velocities=np.linspace(-escape,escape,257);rows=[];checks=[]
    for pop in frozen['populations']:
        base,odd=marginal(velocities,r,pop)
        curve=dict(p=pop['p'],alpha=pop['alpha'],velocity=velocities.tolist(),
            reference_pdf=base.tolist(),plus_pdf=(base+odd).tolist(),minus_pdf=(base-odd).tolist())
        rows.append(curve)
        nodes,weights=leggauss(256);v=nodes*escape;weights*=escape
        bb,oo=marginal(v,r,pop)
        quad_error=max(float(np.max(abs(numerical(x,r,pop,64)-np.array(marginal(x,r,pop)))))
            for x in np.linspace(-.99*escape,.99*escape,17))
        checks.append(dict(p=pop['p'],plus_mass=float(weights@(bb+oo)),
            minus_mass=float(weights@(bb-oo)),plus_mean=float(weights@(v*(bb+oo))),
            minus_mean=float(weights@(v*(bb-oo))),reference_second=float(weights@(v*v*bb)),
            second_difference=float(weights@(2*v*v*oo)),third_difference=float(weights@(2*v**3*oo)),
            minimum_marginal_ratio=float(np.min((bb-abs(oo))/bb)),
            quadrature_max_absolute_error=quad_error))
    assert all(abs(x['plus_mass']-1)<1e-10 and abs(x['minus_mass']-1)<1e-10
        and abs(x['plus_mean'])<1e-12 and abs(x['minus_mean'])<1e-12
        and abs(x['second_difference'])<1e-12 and x['minimum_marginal_ratio']>=.5
        and x['quadrature_max_absolute_error']<1e-8 for x in checks)
    result=dict(schema_version=1,status='unforced_analytic_view_verified',
        observable='Local marginal probability density of azimuthal velocity, not torque',
        radius=r,inclination='equatorial position, R=r',units='Reference velocity; density per reference velocity',
        model='Exact stationary unsoftened isochrone, G=M=1, b=0.5',
        interpretation='Density, mean and all even moments match; higher odd velocity structure differs.',
        limits=['Equation evaluations, not measured dark-matter velocities or simulation frames.',
            'A local marginal is not a torque predictor or a complete distribution function.'],
        figure=dict(default_p=8,rows=rows),checks=checks,
        source_sha256={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in
            [Path(__file__),Path(m.__file__),args.frozen]},cpu_seconds=time.process_time()-cpu)
    (args.out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    (args.out/'COMPLETE').write_text('Unforced analytic view only.\n')
    print(json.dumps(checks,indent=2))

if __name__=='__main__':main()
