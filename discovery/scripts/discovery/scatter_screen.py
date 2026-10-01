"""Conservative viscosity-matched Boltzmann reference experiment.

Particles have one periodic position and three velocity components. Uniform
random disjoint pairs inside spatial cells receive exact equal-mass elastic
collisions. This is a controlled gas resonance, not an SIDM halo simulation.
"""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import time
import numpy as np
from scipy.special import eval_legendre

ROOT=Path(__file__).resolve().parents[2]


def elastic(v1, v2, rng, delta):
    center=(v1+v2)/2
    relative=v1-v2
    speed=np.linalg.norm(relative,axis=1)
    unit=relative/np.maximum(speed[:,None],1e-300)
    if delta==0:
        direction=rng.normal(size=relative.shape)
        direction/=np.linalg.norm(direction,axis=1)[:,None]
    else:
        random=rng.normal(size=relative.shape)
        tangent=random-np.sum(random*unit,axis=1)[:,None]*unit
        tangent/=np.linalg.norm(tangent,axis=1)[:,None]
        direction=np.cos(delta)*unit+np.sin(delta)*tangent
    offset=speed[:,None]*direction/2
    return center+offset,center-offset


def angular_weight(delta):
    return 2/3 if delta==0 else np.sin(delta)**2


def collision_step(x,v,rng,dt,kappa,delta,cells,ledger):
    if kappa==0:
        return
    n=len(x)
    bins=np.floor((x%(2*np.pi))*cells/(2*np.pi)).astype(int)
    counts=np.bincount(bins,minlength=cells)
    order=np.lexsort((rng.random(n),bins))
    # Pair within each cell from its own offset, retaining uniform pairing.
    starts=np.cumsum(np.r_[0,counts[:-1]])
    positions=np.arange(n)
    offsets=positions-np.repeat(starts,counts)
    candidates=positions[(offsets%2==0)&(offsets+1<np.repeat(counts,counts))]
    i,j=order[candidates],order[candidates+1]
    speed=np.linalg.norm(v[i]-v[j],axis=1)
    m=counts[bins[i]]
    # Candidate probability of any unordered pair is 1/(m-1) for
    # even m, 1/m for odd m. Undo that selection probability exactly.
    inverse_pair_probability=m-1+(m%2)
    probability=kappa*speed*dt*inverse_pair_probability*cells/n/angular_weight(delta)
    if len(probability):
        ledger['max_probability']=max(ledger['max_probability'],float(np.max(probability)))
    if np.any(probability>.1):
        raise ValueError('Collision probability exceeds preregistered .1; refine dt')
    ledger['expected_events']+=float(np.sum(probability))
    keep=rng.random(len(i))<probability
    i,j=i[keep],j[keep]
    if len(i):
        before_i,before_j=v[i].copy(),v[j].copy()
        v[i],v[j]=elastic(before_i,before_j,rng,delta)
        kick=v[i,0]-before_i[:,0]
        exchanged=np.sum((v[i]-v[j])*(before_i-before_j),axis=1)<0
        nearest_outgoing=np.where(exchanged[:,None],v[j],v[i])
        invariant_kick=nearest_outgoing[:,0]-before_i[:,0]
        ledger['events']+=len(i)
        ledger['kick_x_squared']+=float(np.sum(kick*kick))
        ledger['exchange_invariant_kick_x_squared']+=float(np.sum(invariant_kick*invariant_kick))
        ledger['collision_energy_change']+=float(.5*np.sum(v[i]*v[i]+v[j]*v[j]-before_i*before_i-before_j*before_j))
        ledger['collision_momentum_change']+=np.sum(v[i]+v[j]-before_i-before_j,axis=0)


def moments(v):
    speed2=np.sum(v*v,axis=1)
    return dict(mean=v.mean(axis=0).tolist(),second=(v*v).mean(axis=0).tolist(),
                speed_second=float(speed2.mean()),speed_fourth=float(np.mean(speed2*speed2)),
                stress=float(np.mean(v[:,0]**2-.5*(v[:,1]**2+v[:,2]**2))))


def operator(out):
    out.mkdir(parents=True,exist_ok=False)
    cpu,started=time.process_time(),time.monotonic()
    rng=np.random.default_rng(260100)
    n=262144
    a=rng.normal(size=(n,3));b=rng.normal(size=(n,3))
    rows=[]
    for delta in (0.,.2,.1,.05):
        av,bv=elastic(a,b,rng,delta)
        u=a-b;up=av-bv
        cosine=np.sum(u*up,axis=1)/np.sum(u*u,axis=1)
        weight=angular_weight(delta)
        rows.append(dict(delta=delta,pair_energy_max=float(np.max(abs(np.sum(av*av+bv*bv-a*a-b*b,axis=1)))),
            pair_momentum_max=float(np.max(abs(av+bv-a-b))),
            mean_sin_squared=float(np.mean(1-cosine*cosine)),expected_sin_squared=weight,
            angular_l2_eigenvalue_over_kappa=float((1-(0 if delta==0 else eval_legendre(2,np.cos(delta))))/weight),
            angular_l4_eigenvalue_over_kappa=float((1-(0 if delta==0 else eval_legendre(4,np.cos(delta))))/weight),
            small_angle_l4_limit=5.,kick_x_rms=float(np.sqrt(np.mean((av[:,0]-a[:,0])**2)))))
    gates=dict(pair_energy=max(r['pair_energy_max'] for r in rows)<1e-12,
        pair_momentum=max(r['pair_momentum_max'] for r in rows)<1e-12,
        angular_weight=max(abs(r['mean_sin_squared']-r['expected_sin_squared']) for r in rows)<.003,
        matched_l2=max(abs(r['angular_l2_eigenvalue_over_kappa']-1.5) for r in rows)<1e-10,
        small_angle_l4=abs(rows[-1]['angular_l4_eigenvalue_over_kappa']/5-1)<.003)
    result=dict(rows=rows,gates=gates,all_pass=all(gates.values()),seed=260100,n=n,
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-started,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        protocol_sha256=hashlib.sha256((ROOT/'research/discovery-20261001/SCATTER_PROTOCOL.md').read_bytes()).hexdigest())
    (out/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


def run(a):
    out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    started,cpu=time.monotonic(),time.process_time()
    begin=datetime.now(timezone.utc).isoformat()
    init_rng=np.random.default_rng(a.seed)
    rng=np.random.default_rng(np.random.SeedSequence([a.seed,109]))
    x=init_rng.uniform(0,2*np.pi,a.n)
    v=init_rng.normal(size=(a.n,3))
    if a.role=='stress':
        v*=np.sqrt(np.array([1.6,.7,.7]))
    initial_x,initial_v=x.copy(),v.copy()
    initial_moments=moments(v)
    eps=a.epsilon if a.role=='resonance' else 0.
    ledger=dict(events=0,expected_events=0.,max_probability=0.,kick_x_squared=0.,exchange_invariant_kick_x_squared=0.,
                collision_energy_change=0.,collision_momentum_change=np.zeros(3))
    work,impulse=0.,0.
    steps=int(round(a.duration/a.dt))
    dt=a.duration/steps
    rows=[]
    def potential(time):
        phase=a.omega0*time+.5*a.sweep*time*time
        angle=x-phase
        force=-eps*np.sin(angle)
        return -eps*np.cos(angle),force,(a.omega0+a.sweep*time)*force
    phi,force,power=potential(0)
    energy0=float(np.mean(.5*np.sum(v*v,axis=1)+phi));momentum0=v.mean(axis=0)
    energy_max,momentum_max=0.,0.
    cadence=max(1,int(round(.5/dt)))
    for step in range(steps):
        t=step*dt
        v[:,0]+=.5*dt*force
        x=(x+dt*v[:,0])%(2*np.pi)
        phi,force1,power1=potential(t+dt)
        v[:,0]+=.5*dt*force1
        work+=.5*dt*float(np.mean(power+power1))
        impulse+=.5*dt*float(np.mean(force+force1))
        collision_step(x,v,rng,dt,a.kappa,a.delta,a.cells,ledger)
        force,power=force1,power1
        if (step+1)%cadence==0 or step+1==steps:
            m=moments(v)
            energy=float(np.mean(.5*np.sum(v*v,axis=1)+phi))
            eerr=energy-energy0-work-ledger['collision_energy_change']/a.n
            perr=v.mean(axis=0)-momentum0-np.array([impulse,0.,0.])-ledger['collision_momentum_change']/a.n
            energy_max=max(energy_max,abs(eerr));momentum_max=max(momentum_max,float(np.max(abs(perr))))
            psi=x-(a.omega0*(t+dt)+.5*a.sweep*(t+dt)**2)
            relative=v[:,0]-(a.omega0+a.sweep*(t+dt))
            inside=(.5*relative*relative-eps*np.cos(psi)<eps) if eps else np.zeros(a.n,dtype=bool)
            rows.append(dict(time=t+dt,impulse=impulse,work=work,energy=energy,energy_error=eerr,
                momentum_error=perr.tolist(),instantaneous_libration_fraction=float(np.mean(inside)),**m))
    ledger['collision_momentum_change']=ledger['collision_momentum_change'].tolist()
    phase=a.omega0*a.duration+.5*a.sweep*a.duration*a.duration
    raw=out/'states.npz'
    np.savez_compressed(raw,initial_x=initial_x,initial_v=initial_v,final_x=x,final_v=v)
    result=dict(config=vars(a),pid=os.getpid(),state='complete',started_utc=begin,
        ended_utc=datetime.now(timezone.utc).isoformat(),initial=initial_moments,history=rows,
        ledger=ledger,max_energy_work_residual=energy_max,max_momentum_impulse_residual=momentum_max,
        event_rate=2*ledger['events']/(a.n*a.duration),
        maxwell_rate_reference=a.kappa*4/np.sqrt(np.pi)/angular_weight(a.delta),
        q_kick_over_resonance_halfwidth=float(np.sqrt(ledger['kick_x_squared']/max(ledger['events'],1))/(2*np.sqrt(eps))) if eps else None,
        q_exchange_invariant_over_resonance_halfwidth=float(np.sqrt(ledger['exchange_invariant_kick_x_squared']/max(ledger['events'],1))/(2*np.sqrt(eps))) if eps else None,
        ncoll_per_libration=float(2*ledger['events']/(a.n*a.duration)*2*np.pi/np.sqrt(eps)) if eps else None,
        cpu_seconds=time.process_time()-cpu,wall_seconds=time.monotonic()-started,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),raw_sha256=hashlib.sha256(raw.read_bytes()).hexdigest(),
        protocol_sha256=hashlib.sha256((ROOT/'research/discovery-20261001/SCATTER_PROTOCOL.md').read_bytes()).hexdigest(),
        scope='1D periodic moving cosine gas, 3D conservative equal-mass elastic collisions; finite cells and timesteps; no halo self-gravity or observational SIDM prediction.')
    (out/'result.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:result[k] for k in ('config','event_rate','max_energy_work_residual','max_momentum_impulse_residual','cpu_seconds')},indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True)
    p.add_argument('--operator',action='store_true')
    p.add_argument('--role',choices=('equilibrium','stress','resonance'),default='resonance')
    p.add_argument('--seed',type=int,default=260101)
    p.add_argument('--n',type=int,default=8192)
    p.add_argument('--cells',type=int,default=32)
    p.add_argument('--dt',type=float,default=.01)
    p.add_argument('--duration',type=float,default=40.)
    p.add_argument('--kappa',type=float,default=.02)
    p.add_argument('--delta',type=float,default=0.)
    p.add_argument('--epsilon',type=float,default=.25)
    p.add_argument('--omega0',type=float,default=.5)
    p.add_argument('--sweep',type=float,default=.025)
    args=p.parse_args()
    if args.operator:
        operator(Path(args.out))
    else:
        run(args)
