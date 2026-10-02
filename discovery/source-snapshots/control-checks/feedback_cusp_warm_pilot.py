"""PREPARATION ONLY: bounded finite warm radial-energy pilot; review before run."""
import os
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
import argparse
import hashlib
import json
from pathlib import Path
import resource
import signal
import time
CPU_START=time.process_time()
resource.setrlimit(resource.RLIMIT_CPU,(560,580))
OWNED=None
RUN_SOURCES={}
RUN_INPUTS={}
def stop(*_):raise TimeoutError('Frozen soft CPU limit reached; preserve partial pilot.')
signal.signal(signal.SIGXCPU,stop)
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import feedback_cusp_radial as scalar
import feedback_cusp_warm_radial as radial

ROOT=Path(__file__).resolve().parents[2]
PROTOCOL=ROOT/'research/discovery-20261001/FEEDBACK_CUSP_WARM_PILOT_PROTOCOL.md'
KNOWN='afa914ffca0106d66ea7f589d1fc46ee8a23e7e9790341cdbddeb47ce4992f86'
READBACK='144fe36181030465b098bc700ebf7d59344a144b25e76f821343377de7bd6dc7'
N=512;CUTOFFS=[None,.25,.5,1.,2.];FIXED=np.array([0,17,63,127,255,511])


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,v):
    Path(p).write_text(json.dumps(v,indent=2,allow_nan=False,
        default=lambda x:x.item() if isinstance(x,np.generic) else (_ for _ in ()).throw(TypeError(type(x).__name__)))+'\n')
def stat(x):return dict(mean=float(x.mean()),standard_error=float(x.std(ddof=1)/np.sqrt(len(x))))
def mass(c):return 1. if c is None else float(radial.cdf(c))
def select(z,c):return np.ones(N) if c is None else (z['Rc']<c)
def cohort(x,z,c):return stat(x*select(z,c)/mass(c))


def integrity():
    sources={path:sha(path)==digest and sha(OWNED/'inputs'/Path(path).name)==digest for path,digest in RUN_SOURCES.items()}
    inputs={path:sha(path)==digest for path,digest in RUN_INPUTS.items()}
    input_snapshots={name:sha(OWNED/'inputs'/name)==digest for name,digest in
        [('known-result.json',KNOWN),('known-array-readback.json',READBACK)]}
    return dict(sources=sources,inputs=inputs,input_snapshots=input_snapshots,
        gate=all(sources.values()) and all(inputs.values()) and all(input_snapshots.values()))


def controls(known):
    record=json.loads((known/'result.json').read_text());assert record['status']=='COMPLETE' and record['gate']
    receipt=known.parent/'cusp-gate-readback-02/result.json';assert sha(receipt)==READBACK
    anchor=json.loads(receipt.read_text());assert anchor['gate'] and anchor['radial_saved_scientific_gate']
    for i,row in enumerate(anchor['radial_blocks']):
        assert i==row['index'] and sha(known/f'initial-{i}.npz')==row['initial_sha256']
    Rc=[];r=[];d=[];J=[];om=[];g=[]
    for i,b in enumerate(record['blocks']):
        z=np.load(known/f'initial-{i}.npz');Rc.extend([b['Rc']]*len(FIXED))
        for target,key in [(r,'radius'),(d,'delta'),(J,'Jr'),(om,'Omega'),(g,'g')]:target.extend(z[key][FIXED])
    model=radial.Population(Rc);r=np.array(r);d=np.array(d);J=np.array(J);om=np.array(om);g=np.array(g)
    j1,o1,g1,_=model.target(d);q=[]
    for i in range(8):q.extend(np.load(known/f'initial-{i}.npz')['q'][FIXED])
    q=np.array(q)
    checks=dict(J_relative=float(np.max(abs(j1-J)/np.maximum(abs(J),1e-12))),
        Omega_relative=float(np.max(abs(o1-om)/np.maximum(abs(om),1e-12))),
        weighted_g_absolute=float(np.max(abs(g1-g)/q)),energy_difference=float(np.max(abs(model.difference(r)-
            np.concatenate([np.load(known/f'initial-{i}.npz')['delta'][FIXED]-.5*np.load(known/f'initial-{i}.npz')['pr'][FIXED]**2 for i in range(8)])))))
    checks['gate']=checks['J_relative']<1e-7 and checks['Omega_relative']<1e-7 and checks['weighted_g_absolute']<1e-7 and checks['energy_difference']<1e-12
    circles=np.array([1e-4,.01,.0595201846464861,.14243078492835742,.25,.5,1.,2.,6.,7.9,8.1,10.,100.])
    test=radial.Population(circles);radii=circles[:,None]*np.array([.2,.5,.9,1.1,2.,4.])
    direct=scalar.fields(radii)[0]+.5*test.L[:,None]**2/radii**2-test.Ec[:,None]
    stable=test.difference(radii);error=abs(stable-direct)/np.maximum(abs(direct),1e-14)
    near=circles[:,None]*(1+np.array([-1e-5,1e-5]));ratio=test.difference(near)/(.5*test.kappa[:,None]**2*(near-circles[:,None])**2)
    field=radial.force(radii)[0];fieldref=scalar.fields(radii)[1]
    checks['full_support_effective_potential']=dict(Rc=circles.tolist(),radius=radii.tolist(),direct=direct.tolist(),
        rationalized=stable.tolist(),relative_errors=error.tolist(),local_quadratic_ratios=ratio.tolist(),
        static_force_maximum_absolute_error=float(abs(field-fieldref).max()))
    checks['gate']=bool(checks['gate'] and error.max()<1e-9 and abs(ratio-1).max()<1e-4 and abs(field-fieldref).max()<1e-12)
    rr=np.array([1e-6,.001,.01,.0595201846464861,.14243078492835742,.25,.5,1.,2.,6.,7.9,8.,8.1,10.,100.])
    def raw_basis(x):
        values=[]
        for s in (.2,1.3):
            norm=8**3/(64+s*s)**1.5
            values.append(np.where(x<8,-(1/np.sqrt(x*x+s*s)-s*s/(64+s*s)**1.5)/norm,-1/x))
        return .1*(values[0]-values[1])
    psi0=.1*(-(1/.2-.2**2/(64+.2**2)**1.5)/(8**3/(64+.2**2)**1.5)
        +(1/1.3-1.3**2/(64+1.3**2)**1.5)/(8**3/(64+1.3**2)**1.5))
    h=1e-5*np.maximum(rr,.01);_,psi,grad=radial.force(rr)
    numerical=(radial.force(rr+h)[1]-radial.force(rr-h)[1])/(2*h)
    inside=rr<8;relative=abs(numerical[inside]-grad[inside])/np.maximum(abs(grad[inside]),1e-20)
    checks['gas_basis']=dict(radius=rr.tolist(),centered=psi.tolist(),center_constant=psi0,raw=raw_basis(rr).tolist(),
        derivative=numerical.tolist(),force=grad.tolist(),maximum_centering_error=float(abs(psi+psi0-raw_basis(rr)).max()),
        maximum_interior_derivative_relative_error=float(relative.max()),
        exterior_force_error=float(abs(grad[rr>8]).max()))
    checks['gate']=bool(checks['gate'] and abs(psi+psi0-raw_basis(rr)).max()<1e-12 and relative.max()<1e-5
        and np.all(grad[rr>8]==0))
    return checks


def sample(centers):
    rng=np.random.default_rng(201063);z=radial.sample_guiding(rng,N,centers);model=radial.Population(z['Rc'])
    z.update(radial.sample_radial(model,rng));J,om,g,slope=model.target(z['delta'])
    z.update(Jr=J,Omega=om,g=g,slope=slope,L=model.L,Js=model.Js,energy_circular=model.Ec)
    z['physical_weight']=z['guide_weight']*g/z['radial_q']
    generating=[]
    for key,original in [('guide_recovered_u','guide_u'),('radial_recovered_u','radial_u'),('radial_recovered_v','radial_v')]:
        x=z[key];error=float(np.max(abs(x-z[original])))
        for cutoff in (.1,.25,.5,.75,.9):
            se=float(np.sqrt(cutoff*(1-cutoff)/N));value=float(np.mean(x<cutoff))
            generating.append(dict(variable=key,cutoff=cutoff,mean=value,standard_error=se,recovery_error=error,
                gate=bool(abs(value-cutoff)<5*se and error<1e-12)))
    moments=[]
    for name,x,truth in [('mass',z['physical_weight'],1.),('guiding_first',z['physical_weight']*z['Rc'],2.),
        ('guiding_second',z['physical_weight']*z['Rc']**2,6.),('action_first',z['physical_weight']*J/model.Js,1.),
        ('action_second',z['physical_weight']*(J/model.Js)**2,2.)]:
        value=stat(x);moments.append(dict(moment=name,measured=value,target=truth,gate=abs(value['mean']-truth)<5*value['standard_error']))
    cohorts=[]
    for c in CUTOFFS:
        guide=stat(z['guide_weight']*select(z,c)/mass(c));physical=cohort(z['physical_weight'],z,c)
        cohorts.append(dict(Rc_upper=c,physical_mass=mass(c),guide_normalization=guide,phase_normalization=physical,
            gate=abs(guide['mean']-1)<5*guide['standard_error'] and abs(physical['mean']-1)<5*physical['standard_error']))
    initial_profile=[dict(radius=R,enclosed_phase_mass=stat(z['physical_weight']*(z['radius']<R))) for R in (.03,.1,.25,.5,1.,2.,8.)]
    return model,z,dict(generating_CDF=generating,moments=moments,cohorts=cohorts,actual_initial_profile=initial_profile,
        guide_weight_maximum=float(z['guide_weight'].max()),target_underflow_count=int(np.sum(g==0)),
        gate=all(x['gate'] for x in generating+moments+cohorts))


def response(model,z,maps,count,action_count):
    R=[];support=[];positive=[];signed=[]
    for forward,inverse in [(0,1),(2,3),(4,5)]:
        rem=model.curvature(z['delta'],maps['delta_final'][forward],count,action_count)
        capture=maps['delta_final'][inverse]>=model.D;sup=np.zeros(N)
        if np.any(capture):sup[capture]=model.subset(np.flatnonzero(capture)).primitive(z['delta'][capture],count,action_count)
        R.append(rem);support.append(sup);positive.append(z['guide_weight']*(rem+sup)/z['radial_q'])
        signed.append(z['physical_weight']*maps['deltaE'][forward])
    return dict(R=np.array(R),support=np.array(support),positive=np.array(positive),ordinary_signed=np.array(signed))


def reference(model,z,ids,cartesian=False):
    m=model.subset(ids);r=z['radius'][ids];p=z['pr'][ids];n=len(ids);direction=radial.DIRECTION[:,None]
    if cartesian:
        normal=np.array([np.sin(.03)*np.cos(.7),np.sin(.03)*np.sin(.7),np.cos(.03)])
        e1=np.cross(normal,[1.,0.,0.]);e1/=np.linalg.norm(e1);e2=np.cross(normal,e1)
        xv=np.column_stack((r[:,None]*e1,p[:,None]*e1+m.L[:,None]/r[:,None]*e2))
        state=np.zeros((6,n,7));state[:,:,:6]=xv
    else:
        state=np.zeros((6,n,3));state[:,:,0]=r;state[:,:,1]=p
    def rhs(s,values):
        a,da=radial.pulse(np.where(radial.DIRECTION>0,s,80-s),radial.FREQUENCY);zz=values.reshape(state.shape)
        if cartesian:
            radius=np.linalg.norm(zz[:,:,:3],axis=-1)
            if np.any(radius<=0):raise RuntimeError('Selected Cartesian central singularity.')
            f,psi,fp=radial.force(radius)
            acceleration=-(f+a[:,None]*fp)[:,:,None]*zz[:,:,:3]/radius[:,:,None]
            return np.concatenate((direction[:,:,None]*zz[:,:,3:6],direction[:,:,None]*acceleration,
                (direction*da[:,None]*psi)[:,:,None]),axis=-1).ravel()
        radius=zz[:,:,0]
        if np.any(radius<=0):raise RuntimeError('Selected radial integration crossed r=0.')
        f,psi,fp=radial.force(radius)
        return np.stack((direction*zz[:,:,1],direction*(m.L[None,:]**2/radius**3-f-a[:,None]*fp),
            direction*da[:,None]*psi),axis=-1).ravel()
    started=time.process_time();absolute=np.tile([1e-12]*6+[1e-14] if cartesian else [1e-12,1e-12,1e-14],6*n)
    sol=solve_ivp(rhs,(0.,80.),state.ravel(),method='DOP853',rtol=2e-10,atol=absolute,max_step=.08)
    if not sol.success:raise RuntimeError(sol.message)
    end=sol.y[:,-1].reshape(state.shape)
    if cartesian:
        radius=np.linalg.norm(end[:,:,:3],axis=-1);pr=np.sum(end[:,:,:3]*end[:,:,3:6],axis=-1)/radius
        kinetic=.5*np.sum(end[:,:,3:6]**2,axis=-1)
        energy=scalar.fields(radius)[0]+kinetic
        Lerr=np.cross(end[:,:,:3],end[:,:,3:6])-np.cross(state[:,:,:3],state[:,:,3:6])
        return dict(radius=radius,pr=pr,deltaE=energy-(m.Ec+z['delta'][ids])[None,:],work=end[:,:,6],
            L_vector_error=Lerr,cpu_seconds=np.array(time.process_time()-started),nfev=np.array(sol.nfev))
    energy=m.difference(end[:,:,0].T).T+.5*end[:,:,1]**2
    return dict(radius=end[:,:,0],pr=end[:,:,1],deltaE=energy-z['delta'][ids][None,:],work=end[:,:,2],
        cpu_seconds=np.array(time.process_time()-started),nfev=np.array(sol.nfev))


def run(args):
    global OWNED,RUN_SOURCES,RUN_INPUTS
    started=CPU_START;args.out.mkdir(parents=True,exist_ok=False);OWNED=args.out.resolve()
    paths=[Path(__file__),Path(radial.__file__),Path(scalar.__file__),PROTOCOL,
        ROOT/'research/discovery-20261001/FEEDBACK_CUSP_WARM_POPULATION_EQUIVALENCE.md',
        ROOT/'research/discovery-20261001/FEEDBACK_CUSP_WARM_VARIANCE_PROOF.md']
    hashes={str(p.relative_to(ROOT)):sha(p) for p in paths}
    RUN_SOURCES={str(p):sha(p) for p in paths}
    snapshots=args.out/'inputs';snapshots.mkdir()
    for path in paths:(snapshots/path.name).write_bytes(path.read_bytes())
    assert sha(args.known/'result.json')==KNOWN
    readback_path=args.known.parent/'cusp-gate-readback-02/result.json';assert sha(readback_path)==READBACK
    anchors=json.loads(readback_path.read_text())['radial_blocks']
    input_hashes={str(args.known/f'initial-{i}.npz'):row['initial_sha256'] for i,row in enumerate(anchors)}
    for path,digest in input_hashes.items():assert sha(path)==digest
    RUN_INPUTS={str(args.known/'result.json'):KNOWN,str(readback_path):READBACK,**input_hashes}
    (snapshots/'known-result.json').write_bytes((args.known/'result.json').read_bytes())
    (snapshots/'known-array-readback.json').write_bytes(readback_path.read_bytes())
    write(snapshots/'input-hashes.json',RUN_INPUTS)
    result=dict(status='RUNNING',scope='Finite radial-energy pilot in same intended warm population; no observed disk-survival claim',
        n=N,seed=201063,selection_seed=201064,source_sha256=hashes,input_sha256=dict(known_map=KNOWN,known_array_readback=READBACK),
        known_initial_sha256=input_hashes,
        original_inclination_scale=.03,orientation_treatment='Normalized original tilt/orientation variables analytically integrated for spherical energy',
        phases='NEW IID full-support Cartesian-free radial proposal; no old sample reuse',completed=[])
    def checkpoint():write(args.out/'partial.json',result)
    def finish(status,gate):
        verified=integrity();assert verified['gate'],'Launched sources/snapshots/known inputs changed.'
        result.update(status=status,gate=bool(gate),closure_integrity=verified,cpu_seconds=time.process_time()-started)
        write(args.out/'result.json',result)
    result['controls']=controls(args.known);checkpoint()
    if not result['controls']['gate']:
        finish('CONTROL_FAILED',False);return
    centers=[brentq(lambda r:float(np.sqrt(scalar.fields(np.array([r]))[2][0]+3*scalar.fields(np.array([r]))[1][0]/r))-f,1e-6,1.) for f in (5.,8.)]
    model,z,result['sampling']=sample(centers);result['proposal_centers']=centers
    np.savez_compressed(args.out/'initial.npz',**z)
    low=np.argsort(z['L'])[:4];pool=np.setdiff1d(np.arange(N),low);rng=np.random.default_rng(201064)
    ids=np.r_[low,rng.choice(pool,4,replace=False)];result['selected_before_forced_outcomes']=dict(ids=ids.tolist(),
        L=z['L'][ids].tolist(),Rc=z['Rc'][ids].tolist(),r=z['radius'][ids].tolist(),delta=z['delta'][ids].tolist())
    checkpoint()
    if not result['sampling']['gate']:
        finish('SAMPLING_FAILED',False);return
    maps=[];replies=[]
    for tag,dt in [('coarse',.00125),('fine',.000625)]:
        begin=time.process_time();m=radial.kdk(model,z['radius'],z['pr'],dt);map_cpu=time.process_time()-begin
        np.savez_compressed(args.out/f'{tag}-maps.npz',**m)
        if any(np.any(~np.isfinite(v)) for v in m.values()) or np.any(m['radius']<=0):
            raise RuntimeError('Nonfinite/nonpositive physical map retained; no excluded paths.')
        rr={str(count):response(model,z,m,count,128) for count in (32,64)}
        np.savez_compressed(args.out/f'{tag}-response.npz',**{k+'_'+c:v for c,x in rr.items() for k,v in x.items()})
        replay=radial.kdk(model,m['radius'],m['pr'],dt,-radial.DIRECTION)
        error=np.maximum(abs(replay['radius']-z['radius'])/(1+z['radius']),abs(replay['pr']-z['pr'])/(1+abs(z['pr'])))
        np.savez_compressed(args.out/f'{tag}-inverse-replay.npz',**replay,scaled_error=error)
        rows=[]
        for c in CUTOFFS:
            for j,freq in [(1,5.),(2,8.)]:
                full=cohort(rr['64']['positive'][j],z,c);zero=cohort(rr['64']['positive'][0],z,c)
                paired=cohort(rr['64']['positive'][j]-rr['64']['positive'][0],z,c)
                U=z['physical_weight']*(abs(m['energy_minus_work'][2*j])+abs(m['energy_minus_work'][0]))
                budget=cohort(U,z,c);quadrature=cohort(rr['64']['positive'][j]-rr['32']['positive'][j],z,c)
                rows.append(dict(Rc_upper=c,physical_mass=mass(c),frequency=freq,actual_forward=full,zero=zero,
                    paired=paired,ordinary_signed=cohort(rr['64']['ordinary_signed'][j],z,c),absolute_energy_work=budget,
                    curvature_difference=quadrature,precision_gate=paired['mean']>0 and paired['standard_error']<=.3*paired['mean'],
                    work_gate=paired['mean']>0 and budget['mean']<=.05*paired['mean'],
                    curvature_gate=paired['mean']>0 and abs(quadrature['mean'])<=.01*paired['mean']))
        result['completed'].append(dict(name=tag,dt=dt,map_cpu_seconds=map_cpu,block_cpu_seconds=time.process_time()-begin,
            rows=rows,capture_counts=[int(np.sum(m['delta_final'][i]>=model.D)) for i in (1,3,5)],
            inverse_scaled_error_maximum=float(error.max()),inverse_gate=bool(error.max()<1e-9)))
        maps.append(m);replies.append(rr['64']);checkpoint()
        if tag=='coarse':
            forecast=time.process_time()-started+2*result['completed'][0]['block_cpu_seconds']+120
            result['timing_gate']=dict(projected_cpu_seconds=forecast,cutoff=500,proceed=forecast<500);checkpoint()
            if forecast>=500:
                finish('COST_PARTIAL',False);return
    refined=response(model,z,maps[1],64,256);np.savez_compressed(args.out/'fine-action256-response.npz',**refined)
    result['paired_refinement']=[]
    for c in CUTOFFS:
        for j,freq in [(1,5.),(2,8.)]:
            pairfine=replies[1]['positive'][j]-replies[1]['positive'][0]
            paircoarse=replies[0]['positive'][j]-replies[0]['positive'][0]
            change=cohort(pairfine-paircoarse,z,c)
            action=cohort((refined['positive'][j]-refined['positive'][0])-pairfine,z,c)
            mean=cohort(pairfine,z,c)['mean'];result['paired_refinement'].append(dict(Rc_upper=c,frequency=freq,
                fine_minus_coarse=change,action256_minus128=action,
                timestep_gate=mean>0 and abs(change['mean'])<=.05*mean,action_gate=mean>0 and abs(action['mean'])<=.01*mean))
    checkpoint();ref=reference(model,z,ids);np.savez_compressed(args.out/'selected-radial-reference.npz',**ref)
    cart=reference(model,z,ids,True);np.savez_compressed(args.out/'selected-cartesian-reference.npz',**cart)
    refrows=[]
    for j,freq in [(1,5.),(2,8.)]:
        weight=z['physical_weight'][ids]/N
        discrepancy=stat(weight*((maps[1]['deltaE'][2*j,ids]-ref['deltaE'][2*j])-
            (maps[1]['deltaE'][0,ids]-ref['deltaE'][0])))
        total_partial=float(np.sum(weight*(abs(maps[1]['deltaE'][2*j,ids]-ref['deltaE'][2*j])+abs(maps[1]['deltaE'][0,ids]-ref['deltaE'][0]))))
        signal=stat(replies[1]['positive'][j]-replies[1]['positive'][0])['mean']
        refrows.append(dict(frequency=freq,selected_original_weight_partial_mean=total_partial,
            selected_individual_error_stat=discrepancy,full_paired_signal=signal,
            necessary_gate=signal>0 and total_partial<.01*signal))
    result['reference']=dict(rows=refrows,scope='Selected paths only; no omitted-state physical error bound and no DOP estimator',
        radial_cartesian_scaled_r_error=float(np.max(abs(ref['radius']-cart['radius'])/(1+ref['radius']))),
        radial_cartesian_scaled_pr_error=float(np.max(abs(ref['pr']-cart['pr'])/(1+abs(ref['pr'])))),
        Cartesian_all_L_scaled_error=float(np.max(abs(cart['L_vector_error'])/(1+model.L[ids])[None,:,None])))
    required=[r for r in result['completed'][1]['rows'] if r['Rc_upper'] is None or r['Rc_upper']==.25]
    refinements=[r for r in result['paired_refinement'] if r['Rc_upper'] is None or r['Rc_upper']==.25]
    result['gate']=bool(all(r['precision_gate'] and r['work_gate'] and r['curvature_gate'] for r in required)
        and all(r['timestep_gate'] and r['action_gate'] for r in refinements)
        and all(x['inverse_gate'] for x in result['completed']) and all(r['necessary_gate'] for r in refrows)
        and result['reference']['radial_cartesian_scaled_r_error']<1e-7
        and result['reference']['radial_cartesian_scaled_pr_error']<1e-7
        and result['reference']['Cartesian_all_L_scaled_error']<1e-9)
    result.update(status='COMPLETE',cpu_seconds=time.process_time()-started,
        limitations=['Known-map controls do not certify physical accuracy.',
            'Exact physical variance proof is not a numerical tail or practical precision certificate.',
            'Same intended analytic target; older AGAMA numerical realization is approximate.',
            'No velocity-dispersion, vertical survival, self-consistent core or observed disk claim.'])
    finish('COMPLETE',result['gate']);print((args.out/'result.json').read_text())


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--known',type=Path,required=True);parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    try:run(args)
    except BaseException as error:
        if OWNED is not None and OWNED==args.out.resolve() and (OWNED/'partial.json').exists():
            receipt=json.loads((args.out/'partial.json').read_text())
            receipt.update(status='FAILED',gate=False,error=dict(type=type(error).__name__,message=str(error)),
                cpu_seconds=time.process_time())
            try:receipt['closure_integrity']=integrity()
            except Exception as verification_error:
                receipt['closure_integrity']=dict(gate=False,error=str(verification_error))
            write(args.out/'result.json',receipt)
        raise
