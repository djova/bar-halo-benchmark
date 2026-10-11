"""Fresh cached-kernel strength solves; no scientific imports at module load.

This extension leaves the twelve-file portable cycle capsule immutable.
An explicitly bound input manifest and external execution allowance are required.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import resource
import sys
import tempfile
import time
from types import SimpleNamespace
import zipfile

PACKAGE=Path(__file__).resolve().parent
CAPSULE_MANIFEST_SHA256='61c963c8d0c6b929701c5f5b18491741713b15fb69380583b0ab4a247fef2a00'
PORTABLE_IO_SHA256='f296c46e9be669718d41797b2789876d39d2bacb7fcc697476499c25052bdb53'
CALCULATION_SOURCE_SHA256='70932b2368900e59a259434a41a3c1aa94fb3e1287a056ebd6dfd07af798ec73'
SCIENTIFIC_SHA256={
 'scientific/independent_orbits.py':'bfa312a372fb046133a15ce7f08f636dbd8510c9377d18ec948d5a8de88e130b',
 'scientific/causal_response.py':'1df0ee3707926eb756bfe5c8a827461f0ad1a8a44f1bfe7ba44d00bf83808996',
 'scientific/volterra.py':'0b05fce93f8fdf615f5b298addce01bb6950a24d97c5435f7f0cf86de2e54fb1'}
LAMBDAS=(0.,.25,.5,.75,1.)
CONFIRMATION_LAMBDAS=(.5,.75)
LAYOUTS={'gl32_coarse':(32,.05,2401),'gl32_fine':(32,.025,4801),'gl64_fine':(64,.025,4801)}
HISTORY_FIELDS=('power','shape_power','torque','work','shape_work','impulse')
ENDPOINT_FIELDS=('W2','J2','shape_W2','rotational_W2','orbit_Q2','canonical_J2',
 'self_U2','raw_energy_budget_residual','raw_impulse_budget_residual')
FALSE_FLAGS=('continuum_response_qualified','whole_waveform_qualified','stationary_power_qualified',
 'continuous_band_qualified','stability_qualified','autonomous_growth_qualified','natural_formation_qualified')
MAX_HISTORY=64*1024**2
MAX_LIBRARY=128*1024**2
MAX_INPUT_TOTAL=256*1024**2
MAX_JSON=1024**2
MAX_RESULT=8*1024**2
MEMORY_MIB=4096
OUTPUT_MIB=256


def require(ok,message):
 if not ok:raise ValueError(message)


def digest_file(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024**2),b''):h.update(block)
 return h.hexdigest()


def read_json(path):
 require(path.stat().st_size<=MAX_JSON,'Bounded JSON input required')
 def reject(value):raise ValueError('Nonfinite JSON input rejected')
 return json.loads(path.read_text(),parse_constant=reject)


def capsule_closure(directory):
 directory=Path(directory).resolve(strict=True)
 module=directory/'portable_io.py'
 require(module.resolve()==module and digest_file(module)==PORTABLE_IO_SHA256,'Frozen portable I/O source required')
 spec=importlib.util.spec_from_file_location('cached_strength_portable_io',module)
 io_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(io_module)
 closure=io_module.verify_package(directory,CAPSULE_MANIFEST_SHA256)
 require(closure['scientific_SHA256']==SCIENTIFIC_SHA256,'Exact portable scientific source required')
 return directory,closure


def fixed_config(capsule,label):
 ne,dt,count=LAYOUTS[label]
 config=read_json(capsule/'configs/gl64-provisional.json')['config']
 config.update(ne=ne,neta=ne,dt=dt)
 return config


def history_inputs(count):
 shapes={'time':((count,),'<f8'),'spatial_metric':((7,7),'<f8')}
 for pop in ('F0','A'):
  for m in (-2,2):
   shapes[f'{pop}_m{m}_kernel']=((count,7,7),'<c16')
   shapes[f'{pop}_m{m}_self0_wake']=((count,7),'<c16')
 return shapes


def library_inputs(ne):
 count=ne*ne
 return {'e':((count,),'<f8'),'eta':((count,),'<f8'),'L':((count,),'<f8'),
  'weight':((count,),'<f8'),'nu':((count,129,3),'<f8'),'radial':((count,129,3,7),'<f8'),
  'radial_n':((129,),'<i8'),'inplane_k':((3,),'<i8')}


def bound_inputs(manifest_path,capsule,selected):
 manifest_path=Path(manifest_path).resolve(strict=True);cache=manifest_path.parent
 manifest=read_json(manifest_path)
 require(manifest.get('binding_status')=='bound','UNBOUND_INPUT_MANIFEST: actual input hashes/configuration required')
 require(manifest['schema']=='portable-cached-strength-inputs-v1'
  and manifest['runner_sha256']==digest_file(PACKAGE/'run_strength.py')
  and manifest['readme_sha256']==digest_file(PACKAGE/'README.md')
  and manifest['capsule_manifest_sha256']==CAPSULE_MANIFEST_SHA256
  and manifest['scientific_SHA256']==SCIENTIFIC_SHA256,
  'Exact executable/source/input namespace required')
 require(manifest['cache_provenance']==dict(generator='frozen portable independent-cycle equations',
  fresh_orbit_and_kernel_generation=True,shared_numerical_method=True,independent_physics_confirmation=False),
  'Explicit cached-source provenance and shared-method scope required')
 held={};layouts={};libraries={};total=0
 def descriptor(desc,cap):
  nonlocal total
  require(set(desc)=={'path','bytes','sha256'} and isinstance(desc['path'],str)
   and Path(desc['path']).name==desc['path'] and desc['path'] not in ('','.','..')
   and type(desc['bytes']) is int and 0<desc['bytes']<=cap
   and isinstance(desc['sha256'],str) and len(desc['sha256'])==64
   and all(c in '0123456789abcdef' for c in desc['sha256']), 'Actual bounded relative file descriptor required')
  p=cache/desc['path'];require(p.resolve(strict=True)==p and p.is_file(),'Regular cached input required')
  if p not in held:
   f=p.open('rb');st=os.fstat(f.fileno())
   try:require(st.st_size==desc['bytes'] and digest_file(p)==desc['sha256'],'Cached input checksum differs')
   except BaseException:f.close();raise
   held[p]=(f,(st.st_dev,st.st_ino,st.st_size,st.st_mtime_ns),desc);total+=st.st_size
  else:require(held[p][2]==desc,'A shared cached file must have one exact descriptor')
  return p
 try:
  for label in selected:
   ne,dt,count=LAYOUTS[label];row=manifest['layouts'][label]
   require(set(row)=={'configuration','history'} and row['configuration']==fixed_config(capsule,label),
    'Exactly frozen layout/source controls required')
   path=descriptor(row['history'],MAX_HISTORY)
   npy_headers(path,history_inputs(count),MAX_HISTORY,max_members=160)
   layouts[label]=dict(label=label,ne=ne,dt=dt,count=count,history_path=path)
   if ne not in libraries:
    p=descriptor(manifest['libraries'][str(ne)],MAX_LIBRARY)
    npy_headers(p,library_inputs(ne),192*1024**2,max_members=160);libraries[ne]=p
  require(total<=MAX_INPUT_TOTAL,'Selected input aggregate exceeds256MiB')
  require(all(p!=manifest_path for p in held),'Manifest cannot be a numeric cached input')
  return manifest_path,manifest,held,layouts,libraries
 except BaseException:
  for f,_,_ in held.values():f.close()
  raise


class CachedIO:
 """One fresh output and bounded progress; no host owner or process lookup."""
 def __init__(self,output,capsule,manifest_path,manifest,held,cpu_cap,wall_cap,started):
  target=Path(output).absolute();parent=target.parent.resolve(strict=True);self.path=parent/target.name
  require(not self.path.exists() and not self.path.is_symlink(),'Fresh output directory required')
  require(self.path not in held and self.path!=manifest_path and capsule not in self.path.parents
   and PACKAGE not in self.path.parents and manifest_path.parent not in self.path.parents,
   'Output must be separate from all immutable source/input directories')
  self.path.mkdir();st=self.path.stat();self.identity=(st.st_dev,st.st_ino)
  self.capsule=capsule;self.manifest_path=manifest_path;self.manifest=manifest;self.held=held
  self.manifest_sha=digest_file(manifest_path);self.source_sha={n:digest_file(PACKAGE/n) for n in ('run_strength.py','README.md')}
  self.cpu_cap=cpu_cap;self.wall_cap=wall_cap;self.started_CPU,self.started_wall=started;self.stop=[False];self.last_check=0.
 def check(self,final=False):
  st=self.path.stat();require(self.path.resolve()==self.path and (st.st_dev,st.st_ino)==self.identity,'Output identity changed')
  if self.stop[0] or (self.path/'STOP').exists():self.stop[0]=True;raise InterruptedError('Cached-strength stop requested')
  require(time.process_time()-self.started_CPU<self.cpu_cap and time.monotonic()-self.started_wall<self.wall_cap,
   'Declared external CPU/wall allowance exhausted')
  for p,(f,identity,desc) in self.held.items():
   s=p.stat();fs=os.fstat(f.fileno())
   require((s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns)==identity
    and (fs.st_dev,fs.st_ino,fs.st_size,fs.st_mtime_ns)==identity,'Cached input identity changed')
  now=time.monotonic()
  if final or now-self.last_check>=10:
   capsule_closure(self.capsule)
   require(digest_file(self.manifest_path)==self.manifest_sha and all(digest_file(PACKAGE/n)==h for n,h in self.source_sha.items()),
    'Cached manifest or extension source changed')
   if final:require(all(digest_file(p)==desc['sha256'] for p,(_,_,desc) in self.held.items()),'Final cached input checksum changed')
   self.last_check=now
 def write(self,name,value,arrays=False,np=None,immutable=False):
  require(isinstance(name,str) and Path(name).name==name and name not in ('','.','..','STOP'),'One regular output name required')
  self.check()
  if arrays:
   require(np is not None and len(value)<=160 and sum(v.nbytes for v in value.values())+1024*len(value)<=MAX_HISTORY,
    'Complete or partial numeric archive exceeds64MiB')
  else:require(len(json.dumps(value,allow_nan=False).encode())<=MAX_RESULT,'Bounded complete report required')
  fd,tmp=tempfile.mkstemp(prefix='.'+name+'-',dir=self.path)
  try:
   with os.fdopen(fd,'wb' if arrays else 'w') as f:
    if arrays:np.savez(f,**value)
    else:json.dump(value,f,indent=2,allow_nan=False);f.write('\n')
    f.flush();os.fsync(f.fileno())
   require(Path(tmp).stat().st_size<=(MAX_HISTORY if arrays else MAX_RESULT),'Actual output file exceeds its declared bound')
   self.check();require(sum(p.stat().st_size for p in self.path.iterdir() if p.is_file())<=OUTPUT_MIB*1024**2,
    'Output including atomic temporary exceeds256MiB')
   if immutable:os.link(tmp,self.path/name);os.unlink(tmp)
   else:os.replace(tmp,self.path/name)
  finally:
   if os.path.exists(tmp):os.unlink(tmp)
 def write_once(self,name,value):
  require(not (self.path/name).exists(),'Forecast must precede GL64 and may be published only once')
  self.write(name,value,immutable=True)


def npy_headers(path,expected,total_cap,max_members=128):
    """Inspect every bounded nonobject header before NumPy allocation."""
    found={};total=0
    with zipfile.ZipFile(path) as z:
        entries=z.infolist()
        require(len(entries)==len({e.filename for e in entries}) and len(entries)<=max_members,'Distinct bounded NPY members required')
        for entry in entries:
            require(entry.filename.endswith('.npy') and Path(entry.filename).name==entry.filename
                and not entry.flag_bits&1,'Contained unencrypted NPY member required')
            with z.open(entry) as f:
                require(f.read(6)==b'\x93NUMPY','NPY magic required');version=f.read(2)
                require(version in (b'\x01\x00',b'\x02\x00',b'\x03\x00'),'NPY version1/2/3 required')
                width=2 if version==b'\x01\x00' else 4
                raw=f.read(width);require(len(raw)==width,'Complete header length required')
                size=int.from_bytes(raw,'little');require(0<size<=65536,'Bounded literal header required')
                raw=f.read(size);require(len(raw)==size,'Complete header required')
                h=ast.literal_eval(raw.decode('utf8' if version==b'\x03\x00' else 'latin1').strip())
            require(set(h)=={'descr','fortran_order','shape'} and isinstance(h['descr'],str)
                and h['fortran_order'] is False and isinstance(h['shape'],tuple)
                and all(type(v) is int and 0<=v<=2000000 for v in h['shape']),'Plain fixed numeric header required')
            descr=h['descr'];code=descr[1:2]
            require(descr[:1] in ('<','>','|','=') and code in ('f','c','i','u','b','U')
                and descr[2:].isdigit(),'No object/structured dtype allowed')
            item=int(descr[2:])*(4 if code=='U' else 1)
            require(0<item<=32768,'Bounded scalar dtype required')
            payload=math.prod(h['shape'])*item
            require(entry.file_size==8+width+size+payload,'Exact decompressed member size required')
            total+=entry.file_size;found[entry.filename[:-4]]=h
        require(total<=total_cap,'Decompressed archive exceeds declared bound')
    for name,(shape,descr) in expected.items():
        require(name in found and found[name]['shape']==shape and found[name]['descr']==descr,'Exact consumed array shape/type required: '+name)
    return found

def arrays_load(path,names,np):
    with np.load(path,allow_pickle=False) as archive:out={n:archive[n].copy() for n in names}
    require(all(np.all(np.isfinite(v)) for v in out.values()),'Every consumed numeric array must be finite')
    return out

def drives(t,np,volterra):
    p,dp,sp=volterra.pulse(t,120.,12.,12.,.8,.12,np);scale=3*.1/(7*math.sqrt(30));out={}
    for m in (-2,2):
        out[m]=[]
        for value in (p,dp,sp):
            a=np.zeros((len(t),7),complex);a[:,0]=scale*(value.conj() if m==-2 else value);out[m].append(a)
    return out

def new_own_cell(lam,m,K,library,t,G,drive,coefficients,np,response,orbital,volterra,angular,g=None):
    """Pure reusable calculation: the unchanged full own solver and original budget."""
    backend=SimpleNamespace(np=np);b,db,ds=drive
    kappa0=orbital.contracted_derivative(library,{},m,backend,angular)
    kappa1=orbital.contracted_derivative(library,coefficients,m,backend,angular)
    kappa=(1-lam)*kappa0+lam*kappa1
    c=volterra.solve(K,b,float(t[1]-t[0]),np,g,self_gravity=1)
    h=response.work_history(c,b,db,ds,G,t,np,m)
    Q,J=response.endpoint_budget(library,kappa,b+c,t,np.diag(G),np,g,m)
    U=.5*float(np.real(c[-1].conj()@G@c[-1]))
    row=dict(W2=float(h['work'][-1]),J2=float(h['impulse'][-1]),shape_W2=float(h['shape_work'][-1]),
        rotational_W2=.12*float(h['impulse'][-1]),orbit_Q2=Q,canonical_J2=J,self_U2=U,
        raw_energy_budget_residual=Q+U-float(h['work'][-1]),raw_impulse_budget_residual=J-float(h['impulse'][-1]))
    return c,h,row

def cell_key(li,m,own):return f'lambda{li}_m{m}_self{own}'

def forecasts(rows):
    out=[]
    for lam in CONFIRMATION_LAMBDAS:
        for channel,budget,target in (('W2','raw_energy_budget_residual',1e-6),('J2','raw_impulse_budget_residual',1e-5)):
            get=lambda tag:next(r for r in rows if r['rule']==tag and r['lambda_value']==lam and r['self_gravity']==1)
            a,b=get('gl32_fine'),get('gl32_coarse');proxy=abs(a[channel]-b[channel])+abs(a[budget])
            out.append(dict(lambda_value=lam,channel=channel,center=a[channel],time_shift=abs(a[channel]-b[channel]),
                finest_budget=abs(a[budget]),time_only_proxy=proxy,range=[a[channel]-proxy,a[channel]+proxy],
                forecast_sign=1 if a[channel]>proxy else -1 if a[channel]<-proxy else 0,
                original_absolute_target=target,action_uncertainty_bounded=False,accuracy_qualified=False))
    return out

def fresh_bare_cell(lam,m,data,library,t,G,drive,coefficients,np,response,orbital,angular,io):
 c=(1-lam)*data[f'F0_m{m}_self0_wake']+lam*data[f'A_m{m}_self0_wake']
 k0=orbital.contracted_derivative(library,{},m,SimpleNamespace(np=np),angular)
 k1=orbital.contracted_derivative(library,coefficients,m,SimpleNamespace(np=np),angular)
 kappa=(1-lam)*k0+lam*k1;b,db,ds=drive
 h=response.work_history(c,b,db,ds,G,t,np,m)
 Q,J=response.endpoint_budget(library,kappa,b,t,np.diag(G),np,io,m)
 U=.5*float(np.real(c[-1].conj()@G@c[-1]))
 return c,h,dict(W2=float(h['work'][-1]),J2=float(h['impulse'][-1]),shape_W2=float(h['shape_work'][-1]),
  rotational_W2=.12*float(h['impulse'][-1]),orbit_Q2=Q,canonical_J2=J,self_U2=U,
  raw_energy_budget_residual=Q-float(h['work'][-1]),raw_impulse_budget_residual=J-float(h['impulse'][-1]))


def paired_totals(rows):
 keys=sorted({(r['layout'],r['lambda_value'],r['self_gravity']) for r in rows})
 out=[]
 for label,lam,own in keys:
  selected=[r for r in rows if (r['layout'],r['lambda_value'],r['self_gravity'])==(label,lam,own)]
  require(len(selected)==2 and {r['m'] for r in selected}=={-2,2},'Both raw signed sectors required')
  out.append(dict(rule=label,lambda_value=lam,self_gravity=own,**{n:math.fsum(r[n] for r in selected) for n in ENDPOINT_FIELDS}))
 return out


def public_manifest_template(capsule,selected):
 return dict(schema='portable-cached-strength-inputs-v1',binding_status='unbound',
  runner_sha256=digest_file(PACKAGE/'run_strength.py'),readme_sha256=digest_file(PACKAGE/'README.md'),
  capsule_manifest_sha256=CAPSULE_MANIFEST_SHA256,scientific_SHA256=SCIENTIFIC_SHA256,
  cache_provenance=dict(generator='frozen portable independent-cycle equations',fresh_orbit_and_kernel_generation=True,
   shared_numerical_method=True,independent_physics_confirmation=False),
  layouts={n:dict(configuration=fixed_config(capsule,n),history=dict(path=n+'-history.npz',bytes=None,sha256=None)) for n in selected},
  libraries={str(ne):dict(path=f'gl{ne}-orbit-library.npz',bytes=None,sha256=None) for ne in sorted({LAYOUTS[n][0] for n in selected})})


def execution_limits(cpu,wall):
 require(cpu is not None and wall is not None and math.isfinite(cpu) and math.isfinite(wall)
  and 0<cpu<=86400 and 0<wall<=172800,'Explicit externally admitted positive CPU and wall allowances required')
 for kind,target in ((resource.RLIMIT_CPU,math.ceil(time.process_time()+cpu)),(resource.RLIMIT_AS,MEMORY_MIB*1024**2)):
  _,hard=resource.getrlimit(kind);bound=target if hard==resource.RLIM_INFINITY else min(target,hard)
  resource.setrlimit(kind,(bound,bound))
 for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
  os.environ[key]='1'


def main(argv=None):
 started=(time.process_time(),time.monotonic())
 require(sys.flags.dont_write_bytecode,'Use python -B; the immutable capsule must not receive bytecode files')
 parser=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
 parser.add_argument('--capsule',required=True)
 parser.add_argument('--input-manifest');parser.add_argument('--output');parser.add_argument('--inspect',action='store_true')
 parser.add_argument('--lambda',dest='strengths',type=float,action='append',choices=LAMBDAS)
 parser.add_argument('--layout',action='append',choices=tuple(LAYOUTS));parser.add_argument('--full',action='store_true')
 parser.add_argument('--cpu-seconds',type=float);parser.add_argument('--wall-seconds',type=float)
 args=parser.parse_args(argv)
 require(not args.full or (args.strengths is None and args.layout is None),'Full fixed map cannot be mixed with subset selectors')
 strengths=LAMBDAS if args.full else tuple(v for v in LAMBDAS if v in (args.strengths or CONFIRMATION_LAMBDAS))
 selected=tuple(LAYOUTS) if args.full or args.layout is None else tuple(n for n in LAYOUTS if n in args.layout)
 full_map=strengths==LAMBDAS and selected==tuple(LAYOUTS)
 capsule,closure=capsule_closure(args.capsule)
 if args.inspect:
  print(json.dumps(public_manifest_template(capsule,selected),indent=2,allow_nan=False));return
 require(args.input_manifest and args.output,'Execution refuses an unbound or absent input manifest and requires fresh output')
 execution_limits(args.cpu_seconds,args.wall_seconds)
 manifest_path,manifest,held,rules,library_paths=bound_inputs(args.input_manifest,capsule,selected)
 io=None;report=None
 try:
  io=CachedIO(args.output,capsule,manifest_path,manifest,held,args.cpu_seconds,args.wall_seconds,started)
  planned=len(selected)*len(strengths)*4
  report=dict(schema='portable-cached-strength-result-v1',complete=False,stage='headers_and_sources_verified',
   input_manifest_sha256=digest_file(manifest_path),capsule_manifest_sha256=CAPSULE_MANIFEST_SHA256,
   calculation_source_sha256=CALCULATION_SOURCE_SHA256,scientific_SHA256=SCIENTIFIC_SHA256,
   cached_numeric_inputs=True,fresh_orbit_or_kernel_generation=False,
   selected_lambda_values=list(strengths),selected_layouts=list(selected),full_five_strength_three_layout_map=full_map,
   fixed_cycle=dict(T=120.,rise=12.,fall=12.,shape=.8,pattern_speed=.12,harmonic_frequency=.24,N=64,CB=list(range(7))),
   planned_signed_cells=planned,planned_fresh_own_cells=planned//2,completed_signed_cells=0,completed_fresh_own_cells=0,
   current=None,signed_cells=[],totals=[],products=[],raw_metric_diagnostics=[],raw_kernel_diagnostics=[],
   baseline_own_histories_or_endpoint_tables_replayed=False,all_selected_orbital_budgets_fresh=True,
   bare_wakes_only_exact_affine=True,own_histories_interpolated=False,raw_Gram_or_Ward_repaired=False,
   original_expanded_precision_failures_preserved=True,shared_numerical_method=True,independent_physics_confirmation=False,
   forecasts_status='not available without both GL32 layouts and both fixed confirmation strengths',**{n:False for n in FALSE_FLAGS})
  def checkpoint():
   io.check();report['process_CPU_seconds']=time.process_time()-started[0];io.write('result.json',report)
  checkpoint()
  require(not any(n in sys.modules for n in ('scientific','scientific.independent_orbits','scientific.causal_response','scientific.volterra')),
   'Scientific namespace must be fresh before importing frozen capsule')
  sys.path.insert(0,str(capsule))
  import numpy as np
  from scientific import causal_response as response,independent_orbits as orbital,volterra
  for module,leaf in ((response,'causal_response'),(orbital,'independent_orbits'),(volterra,'volterra')):
   require(Path(module.__file__).resolve()==capsule/'scientific'/(leaf+'.py'),'Actual imported frozen module required')
  definition=read_json(capsule/'inputs/population.json');coefficients={int(k):v for k,v in definition['coefficients'].items()}
  require(set(coefficients)=={5,6,7,8,10,12},'Exactly frozen population required')
  angular=orbital.angular_moments(SimpleNamespace(np=np));libraries={}
  for ne,path in library_paths.items():
   lib=arrays_load(path,library_inputs(ne),np)
   require(np.array_equal(lib['radial_n'],np.arange(-64,65)) and np.array_equal(lib['inplane_k'],[-2,0,2])
    and np.all((lib['e']>0)&(lib['e']<1)) and np.all((lib['eta']>0)&(lib['eta']<1))
    and np.all(lib['L']>0) and np.all(lib['weight']>0),'Full signed/static physical library support required')
   libraries[ne]=lib
  frozen=None
  for label in selected:
   rule=rules[label];data=arrays_load(rule['history_path'],history_inputs(rule['count']),np)
   t=data['time'];G=data['spatial_metric'];drive=drives(t,np,volterra)
   require(np.array_equal(t,np.linspace(0.,120.,rule['count'])) and np.all(np.diag(G)<0),'Actual full raw clock and negative Gram required')
   report['raw_metric_diagnostics'].append(dict(layout=label,diagonal=np.diag(G).tolist(),
    maximum_raw_Hermitian_defect=float(np.max(np.abs(G-G.T))),maximum_raw_offdiagonal=float(np.max(np.abs(G-np.diag(np.diag(G))))),
    full_Gram_used_in_work=True,diagonal_Gram_used_in_saved_kernel=True,repair_applied=False))
   out={'time':t,'spatial_metric':G,'lambda_values':np.asarray(strengths),'m_values':np.asarray((-2,2),dtype=np.int64)}
   for pop in ('F0','A'):
    for m in (-2,2):out[f'{pop}_m{m}_kernel']=data[f'{pop}_m{m}_kernel']
   cells=0
   for lam in strengths:
    li=LAMBDAS.index(lam)
    for m in (-2,2):
     K=(1-lam)*data[f'F0_m{m}_kernel']+lam*data[f'A_m{m}_kernel']
     report['raw_kernel_diagnostics'].append(dict(layout=label,lambda_value=lam,m=m,
      equal_time_real=K[0].real.tolist(),equal_time_imag=K[0].imag.tolist(),
      initial_slope_proxy_real=((K[1]-K[0])/(t[1]-t[0])).real.tolist(),initial_slope_proxy_imag=((K[1]-K[0])/(t[1]-t[0])).imag.tolist(),
      target_equal_time_value_imposed=False))
     for own in (0,1):
      report['current']=dict(layout=label,lambda_value=lam,m=m,self_gravity=own);checkpoint();before=time.process_time()
      if own:c,h,row=new_own_cell(lam,m,K,libraries[rule['ne']],t,G,drive[m],coefficients,np,response,orbital,volterra,angular,io)
      else:c,h,row=fresh_bare_cell(lam,m,data,libraries[rule['ne']],t,G,drive[m],coefficients,np,response,orbital,angular,io)
      require(np.all(np.isfinite(c)) and all(np.all(np.isfinite(v)) for v in h.values())
       and all(math.isfinite(float(v)) for v in row.values()),'Every full raw cell must be finite')
      key=cell_key(li,m,own);out[key+'_wake']=c;out.update({key+'_'+n:v for n,v in h.items()})
      report['signed_cells'].append(dict(layout=label,lambda_value=lam,m=m,self_gravity=own,
       calculation_kind='fresh_own_field_and_full_endpoint_budget' if own else 'exact_affine_bare_wake_and_fresh_full_endpoint_budget',
       CPU_seconds=time.process_time()-before,**row));cells+=1;report['completed_signed_cells']+=1
      report['completed_fresh_own_cells']+=own
      leaf=label+'-history.npz';io.write(leaf,out,arrays=True,np=np);p=io.path/leaf
      report['products']=[q for q in report['products'] if q['layout']!=label]+[dict(layout=label,path=leaf,
       bytes=p.stat().st_size,sha256=digest_file(p),completed_signed_cells=cells,complete=cells==len(strengths)*4)]
      report['current']=None;checkpoint()
   if label=='gl32_fine' and 'gl32_coarse' in selected and all(v in strengths for v in CONFIRMATION_LAMBDAS):
    frozen=forecasts(paired_totals(report['signed_cells']))
    record=dict(schema='portable-cached-strength-forecast-v1',complete=True,rows=frozen,
     confirmation_lambdas=list(CONFIRMATION_LAMBDAS),GL64_selected_own_fields_computed=False,
     completed_fresh_own_cells=report['completed_fresh_own_cells'],posthoc_parameter_selection=False)
    io.write_once('frozen-forecasts.json',record);p=io.path/'frozen-forecasts.json'
    report['frozen_forecast_product']=dict(path=p.name,bytes=p.stat().st_size,sha256=digest_file(p))
    report['forecasts_status']='fixed GL32-only forecasts saved before any selected GL64 own solve'
   del out,data;checkpoint()
  require(report['completed_signed_cells']==planned and report['completed_fresh_own_cells']==planned//2,
   'All selected full cells required; no qualified prefix')
  report['totals']=paired_totals(report['signed_cells'])
  if frozen is not None and 'gl64_fine' in selected:
   report['forecast_comparisons']=[]
   for row in frozen:
    value=next(v[row['channel']] for v in report['totals'] if v['rule']=='gl64_fine' and v['lambda_value']==row['lambda_value'] and v['self_gravity']==1)
    report['forecast_comparisons'].append(dict(**row,actual_GL64=value,
     inside_time_only_forecast_range=row['range'][0]<=value<=row['range'][1],same_nonzero_forecast_sign=row['forecast_sign']!=0 and value*row['forecast_sign']>0))
  io.check(final=True);report.update(complete=True,stage='complete_selected_calculation',current=None)
  checkpoint();io.write('TERMINAL.json',dict(schema='portable-cached-strength-terminal-v1',complete=True,status='complete',
   inputs_unchanged=True,process_CPU_seconds=time.process_time()-started[0],wall_seconds=time.monotonic()-started[1],scientific_qualification=False))
  print(json.dumps(dict(complete=True,signed_cells=planned,fresh_own_cells=planned//2,full_map=full_map,scientific_qualification=False)))
 except BaseException as error:
  if io is not None and report is not None:
   report.update(complete=False,stage='failed',failure=dict(type=type(error).__name__,message='Calculation failed; previous complete cells are retained'))
   try:io.write('result.json',report);io.write('TERMINAL.json',dict(schema='portable-cached-strength-terminal-v1',complete=False,status='failed',scientific_qualification=False))
   except BaseException:pass
  raise
 finally:
  for f,_,_ in held.values():f.close()


if __name__=='__main__':main()
