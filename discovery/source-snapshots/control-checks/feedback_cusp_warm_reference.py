"""Prepared fixed-path tighter DOP reference; no population or target change."""
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
START=time.process_time()
resource.setrlimit(resource.RLIMIT_CPU,(45,48))
def stop(*_):raise TimeoutError('Frozen45CPU reference limit reached.')
signal.signal(signal.SIGXCPU,stop)
import numpy as np
from scipy.integrate import solve_ivp
import feedback_cusp_radial as scalar
import feedback_cusp_warm_radial as radial

ROOT=Path(__file__).resolve().parents[2]
PROTOCOL=ROOT/'research/discovery-20261001/FEEDBACK_CUSP_WARM_REFERENCE_PROTOCOL.md'
PILOT='e1a0e06d6f1937e3aab2b05281fed0810c2d04970e42820f3f448548fc5c7685'
READBACK='c72d6b75ce17a595779bd46b362e88367abdd540d29ed5c3110f766bc1de95fc'
OWNED=None
VERIFY=None


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):Path(p).write_text(json.dumps(x,indent=2,allow_nan=False)+'\n')


def reference(model,z,ids,cartesian):
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
    start=time.process_time();absolute=np.tile([1e-14]*6+[1e-16] if cartesian else [1e-14,1e-14,1e-16],6*n)
    sol=solve_ivp(rhs,(0.,80.),state.ravel(),method='DOP853',rtol=2e-12,atol=absolute,max_step=.04)
    if not sol.success:raise RuntimeError(sol.message)
    end=sol.y[:,-1].reshape(state.shape)
    if cartesian:
        radius=np.linalg.norm(end[:,:,:3],axis=-1);pr=np.sum(end[:,:,:3]*end[:,:,3:6],axis=-1)/radius
        energy=scalar.fields(radius)[0]+.5*np.sum(end[:,:,3:6]**2,axis=-1)
        return dict(radius=radius,pr=pr,deltaE=energy-(m.Ec+z['delta'][ids])[None,:],work=end[:,:,6],
            L_vector_error=np.cross(end[:,:,:3],end[:,:,3:6])-np.cross(state[:,:,:3],state[:,:,3:6]),
            cpu_seconds=np.array(time.process_time()-start),nfev=np.array(sol.nfev))
    energy=m.difference(end[:,:,0].T).T+.5*end[:,:,1]**2
    return dict(radius=end[:,:,0],pr=end[:,:,1],deltaE=energy-z['delta'][ids][None,:],work=end[:,:,2],
        cpu_seconds=np.array(time.process_time()-start),nfev=np.array(sol.nfev))


def run(args):
    global OWNED,VERIFY
    args.out.mkdir(parents=True,exist_ok=False);OWNED=args.out.resolve()
    assert sha(args.input/'result.json')==PILOT and sha(args.readback/'result.json')==READBACK
    old=json.loads((args.input/'result.json').read_text());readback=json.loads((args.readback/'result.json').read_text())
    assert old['status']=='COMPLETE' and old['gate'] is False and old['closure_integrity']['gate']
    assert readback['arithmetic_gate'] and readback['original_scientific_gate'] is False
    anchors={args.input/name:digest for name,digest in readback['input_sha256'].items()}
    anchors[args.readback/'result.json']=READBACK
    sources=[Path(__file__),Path(radial.__file__),Path(scalar.__file__),PROTOCOL]
    snapshots=args.out/'inputs';snapshots.mkdir()
    for p in sources:(snapshots/p.name).write_bytes(p.read_bytes())
    sourcehash={str(p):sha(p) for p in sources}
    for p,digest in anchors.items():assert sha(p)==digest
    for relative,digest in old['source_sha256'].items():
        assert sha(ROOT/relative)==digest and sha(args.input/'inputs'/Path(relative).name)==digest
    def integrity():
        checks={str(p):sha(p)==digest for p,digest in anchors.items()}
        checks.update({str(p):sha(p)==sourcehash[str(p)] and sha(snapshots/p.name)==sourcehash[str(p)] for p in sources})
        return dict(checks=checks,gate=all(checks.values()))
    VERIFY=integrity
    result=dict(status='RUNNING',source_sha256=sourcehash,input_sha256={str(p):s for p,s in anchors.items()},
        scope='Same eight preselected pilot paths; new reference control only, no old gate relabeling.',
        original_scientific_gate=False,rtol=2e-12,position_momentum_atol=1e-14,work_atol=1e-16,max_step=.04)
    def checkpoint():write(args.out/'partial.json',result)
    def finish(status,gate):
        result.update(status=status,gate=gate,cpu_seconds=time.process_time()-START,closure_integrity=integrity())
        assert result['closure_integrity']['gate']
        write(args.out/'result.json',result)
    z=np.load(args.input/'initial.npz');model=radial.Population(z['Rc'])
    ids=np.array(old['selected_before_forced_outcomes']['ids']);assert ids.tolist()==[67,0,118,483,461,238,130,456]
    result['ids']=ids.tolist();result['Rc']=z['Rc'][ids].tolist();result['L']=z['L'][ids].tolist()
    result['original_physical_weight']=z['physical_weight'][ids].tolist();checkpoint()
    ref=reference(model,z,ids,False);np.savez_compressed(args.out/'radial-reference.npz',**ref)
    forecast=time.process_time()-START+2*float(ref['cpu_seconds'])+4
    result['radial_cpu_seconds']=float(ref['cpu_seconds']);result['projection']=dict(cpu_seconds=forecast,cutoff=43,proceed=forecast<43)
    checkpoint()
    if forecast>=43:finish('COST_PARTIAL',False);return
    cart=reference(model,z,ids,True);np.savez_compressed(args.out/'cartesian-reference.npz',**cart)
    oldref=np.load(args.input/'selected-radial-reference.npz');oldcart=np.load(args.input/'selected-cartesian-reference.npz')
    rerror=abs(ref['radius']-cart['radius'])/(1+ref['radius'])
    perror=abs(ref['pr']-cart['pr'])/(1+abs(ref['pr']))
    energy=ref['deltaE']-cart['deltaE'];Lerror=abs(cart['L_vector_error'])/(1+model.L[ids])[None,:,None]
    radialbudget=ref['deltaE']-ref['work'];cartbudget=cart['deltaE']-cart['work']
    result.update(Cartesian_cpu_seconds=float(cart['cpu_seconds']),
        maximum_scaled_radius_error=float(rerror.max()),maximum_scaled_momentum_error=float(perror.max()),
        maximum_energy_disagreement=float(abs(energy).max()),maximum_all_L_scaled_error=float(Lerror.max()),
        maximum_radial_energy_work_error=float(abs(radialbudget).max()),maximum_Cartesian_energy_work_error=float(abs(cartbudget).max()),
        per_path=[dict(id=int(i),scaled_radius_error=rerror[:,k].tolist(),scaled_momentum_error=perror[:,k].tolist(),
            radial_old_to_new_scaled_radius=(abs(oldref['radius'][:,k]-ref['radius'][:,k])/(1+ref['radius'][:,k])).tolist(),
            Cartesian_old_to_new_scaled_radius=(abs(oldcart['radius'][:,k]-cart['radius'][:,k])/(1+cart['radius'][:,k])).tolist(),
            radial_old_to_new_scaled_momentum=(abs(oldref['pr'][:,k]-ref['pr'][:,k])/(1+abs(ref['pr'][:,k]))).tolist(),
            Cartesian_old_to_new_scaled_momentum=(abs(oldcart['pr'][:,k]-cart['pr'][:,k])/(1+abs(cart['pr'][:,k]))).tolist(),
            energy_disagreement=energy[:,k].tolist(),radial_energy_minus_work=radialbudget[:,k].tolist(),
            Cartesian_energy_minus_work=cartbudget[:,k].tolist()) for k,i in enumerate(ids)])
    gate=bool(rerror.max()<1e-7 and perror.max()<1e-7 and Lerror.max()<1e-9
        and abs(radialbudget).max()<1e-10 and abs(cartbudget).max()<1e-10)
    finish('COMPLETE',gate)
    print(json.dumps({key:result[key] for key in ['status','gate','cpu_seconds','maximum_scaled_radius_error','maximum_scaled_momentum_error']}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--readback',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    try:run(args)
    except Exception as error:
        if OWNED is not None and (OWNED/'partial.json').exists():
            result=json.loads((OWNED/'partial.json').read_text());result.update(status='FAILED',gate=False,
                error=dict(type=type(error).__name__,message=str(error)),cpu_seconds=time.process_time()-START)
            if VERIFY is not None:
                try:result['closure_integrity']=VERIFY()
                except Exception as verification:result['closure_integrity']=dict(gate=False,error=str(verification))
            write(OWNED/'result.json',result)
        raise
