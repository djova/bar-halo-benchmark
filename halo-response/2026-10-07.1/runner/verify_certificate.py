#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Independently regenerate the full-support Bernstein positivity check.

Only the Python standard library is used. The clean certificate records exact
binary coefficient constants; no optimizer, numerical grid or campaign code
is imported. Execute only after the publisher supplies certificate.json.
"""
import argparse
import ast
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import time

POWERS=(5,6,7,8,10,12)
SCHEMA='bare-plummer-positivity-certificate-v1'


def rational(value):
    if (not isinstance(value,dict) or set(value)!= {'numerator','denominator'}
            or type(value['numerator']) is not int or type(value['denominator']) is not int
            or value['denominator']<=0):
        raise ValueError('Exact integer numerator and positive denominator required')
    return Fraction(value['numerator'],value['denominator'])


def encoded(value):
    return dict(numerator=value.numerator,denominator=value.denominator)


def add(a,b):
    result=dict(a)
    for key,value in b.items():
        result[key]=result.get(key,Fraction(0))+value
    return {key:value for key,value in result.items() if value}


def scale(poly,value):
    return {key:c*value for key,c in poly.items() if c*value}


def multiply(a,b):
    result={}
    for (i,j),x in a.items():
        for (k,l),y in b.items():
            key=i+k,j+l;result[key]=result.get(key,Fraction(0))+x*y
    return {key:value for key,value in result.items() if value}


def power(poly,n):
    result={(0,0):Fraction(1)}
    for unused in range(n):
        result=multiply(result,poly)
    return result


def operands(p,q):
    one={(0,0):Fraction(1)};u2={(2,0):Fraction(1)};t2={(0,2):Fraction(1)}
    plus=add(one,u2);minus=add(one,scale(u2,-1))
    e2=scale(multiply(u2,power(plus,2)),Fraction(1,4))
    denominator=add(one,scale(e2,-q))
    ap=Fraction(16*p,(2*p+5)*(2*p+7));bp=Fraction(4,p+1)
    bracket=add({(0,0):-ap},scale(e2,bp))
    bracket=add(bracket,scale(multiply(t2,multiply(power(minus,2),plus)),Fraction(1,2)))
    prefactor=multiply({(p-5,1):Fraction(1,2**(p-4))},multiply(minus,power(plus,p-4)))
    return multiply(prefactor,bracket),denominator


def bernstein(poly,nu,nt):
    """Exact power-to-tensor-Bernstein degree elevation on the unit square."""
    return tuple(tuple(sum((c*Fraction(math.comb(i,a),math.comb(nu,a))
        *Fraction(math.comb(j,b),math.comb(nt,b)) for (a,b),c in poly.items() if a<=i and b<=j),Fraction(0))
        for j in range(nt+1)) for i in range(nu+1))


def split1(values):
    """Positive de Casteljau subdivision at exact one-half."""
    work=list(values);left=[work[0]];right=[work[-1]]
    while len(work)>1:
        work=[(a+b)/2 for a,b in zip(work[:-1],work[1:])]
        left.append(work[0]);right.append(work[-1])
    return tuple(left),tuple(reversed(right))


def split2(matrix,axis):
    if axis==0:
        columns=[split1(tuple(row[j] for row in matrix)) for j in range(len(matrix[0]))]
        return tuple(tuple(tuple(columns[j][side][i] for j in range(len(columns)))
            for i in range(len(matrix))) for side in (0,1))
    rows=[split1(row) for row in matrix]
    return tuple(tuple(row[side] for row in rows) for side in (0,1))


def runner_vectors(path):
    names={'POWERS','A_COEFFICIENTS','NINE_TENTHS_COEFFICIENTS'};values={}
    for node in ast.parse(path.read_text(),filename=path.name).body:
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            name=node.targets[0].id
            if name in names:
                if name in values:raise ValueError('Duplicate runner coefficient declaration')
                values[name]=ast.literal_eval(node.value)
    if set(values)!=names or tuple(values['POWERS'])!=POWERS:
        raise ValueError('Exact public runner coefficient definitions required')
    vectors={name:tuple(Fraction(x) for x in values[key]) for name,key in
        (('A_full_plus','A_COEFFICIENTS'),('A_nine_tenths_plus','NINE_TENTHS_COEFFICIENTS'))}
    if any(len(row)!=6 for row in vectors.values()):raise ValueError('Six actual runner constants required')
    return vectors


def verify(payload,runner,check):
    if payload.get('schema')!=SCHEMA or tuple(payload.get('powers',()))!=POWERS:
        raise ValueError('Clean exact six-power certificate schema required')
    reference=payload['reference']
    if (rational(reference['q'])!=Fraction(14,33) or reference.get('bar_mass')!='1/10'
            or any(reference.get(key)!=1 for key in ('G','total_mass','radius'))):
        raise ValueError('Exact declared Plummer physical reference required')
    region=payload['region'];du,dt=region['depth_u'],region['depth_t'];q=Fraction(14,33);alpha=Fraction(35,99)
    if (region['degree_u']!=31 or region['degree_t']!=3 or rational(region['alpha'])!=alpha
            or any(type(d) is not int or not 0<=d<=4 for d in (du,dt))):
        raise ValueError('Bounded exact degree31-by3 dyadic certificate required')
    certificates=payload['certificates'];vectors=runner_vectors(runner)
    if set(certificates)!=set(vectors):raise ValueError('Separate full-A and actual .9 certificates required')
    combined={name:{} for name in vectors};denominator=None
    for index,p in enumerate(POWERS):
        h,d=operands(p,q)
        if denominator is not None and d!=denominator:raise ValueError('Common denominator mismatch')
        denominator=d
        for name,vector in vectors.items():combined[name]=add(combined[name],scale(h,vector[index]))
    for name,vector in vectors.items():
        cert=certificates[name]
        if (set(cert['coefficients'])!=set(map(str,POWERS))
                or tuple(rational(cert['coefficients'][str(p)]) for p in POWERS)!=vector
                or cert.get('feasible') is not True):
            raise ValueError('Certificate does not bind the actual binary runner vector: '+name)
    if payload['derived_populations']!=dict(F0=dict(zero=True),A_full_minus=dict(base='A_full_plus',scale=encoded(Fraction(-1))),
            A_half_plus=dict(base='A_full_plus',scale=encoded(Fraction(1,2)))):
        raise ValueError('Only exact zero/sign/halving certificate consequences allowed')
    dmatrix=tuple(row[0] for row in bernstein(denominator,31,0))
    boxes=[({name:bernstein(h,31,3) for name,h in combined.items()},dmatrix)]
    for unused in range(du):
        children=[]
        for hs,ds in boxes:
            hsplit={name:split2(h,0) for name,h in hs.items()};dsplit=split1(ds)
            children.extend(({name:h[side] for name,h in hsplit.items()},dsplit[side]) for side in (0,1))
        boxes=children;check()
    maxima={name:Fraction(0) for name in vectors};minimum=None;sites=0
    for hs,ds in boxes:
        if any(d<=0 for d in ds):raise ArithmeticError('Positive full-patch denominator failed')
        value=min(ds);minimum=value if minimum is None else min(minimum,value)
        tboxes=[hs]
        for unused in range(dt):
            children=[]
            for own in tboxes:
                split={name:split2(h,1) for name,h in own.items()}
                children.extend({name:h[side] for name,h in split.items()} for side in (0,1))
            tboxes=children
        for own in tboxes:
            for i in range(32):
                for j in range(4):
                    sites+=1
                    for name,h in own.items():maxima[name]=max(maxima[name],abs(h[i][j])/(alpha*ds[i]))
            check()
    if minimum!=rational(region['minimum_denominator']):raise ValueError('Recorded exact denominator minimum mismatch')
    for name,maximum in maxima.items():
        cert=certificates[name]
        if (maximum>1 or maximum!=rational(cert['maximum_constraint_ratio'])
                or 1-maximum!=rational(cert['minimum_normalized_slack'])):
            raise ArithmeticError('Regenerated full-support inequalities differ or fail: '+name)
    return dict(verified=True,maximum_constraint_ratios={name:encoded(v) for name,v in maxima.items()},
        minimum_denominator=encoded(minimum),raw_coefficient_sites_per_vector=sites,patches=2**(du+dt),
        guarantee='F0/2 <= F <= 3F0/2 on full bound support; exact coefficient arithmetic, not machine DF evaluation or stability')


def main():
    parser=argparse.ArgumentParser(description=__doc__,allow_abbrev=False)
    parser.add_argument('--certificate',default=str(Path(__file__).resolve().with_name('certificate.json')))
    parser.add_argument('--output');parser.add_argument('--cpu-seconds',type=int,default=60)
    parser.add_argument('--wall-seconds',type=int,default=120)
    args=parser.parse_args()
    if not 1<=args.cpu_seconds<=300 or not 1<=args.wall_seconds<=600:parser.error('Bounded verification time required')
    home=Path(__file__).resolve().parent;started=time.process_time();wall=time.monotonic()
    def check():
        if time.process_time()-started>args.cpu_seconds or time.monotonic()-wall>args.wall_seconds:
            raise TimeoutError('Certificate verification incomplete; declared time exhausted')
    def interrupted(unused_signal,unused_frame):raise InterruptedError('Certificate verification interrupted')
    for name in ('SIGINT','SIGTERM','SIGXCPU'):
        if hasattr(signal,name):signal.signal(getattr(signal,name),interrupted)
    try:
        import resource
        for key,amount in ((resource.RLIMIT_CPU,args.cpu_seconds),(resource.RLIMIT_AS,512*1024**2)):
            soft,hard=resource.getrlimit(key);limit=min([amount]+[v for v in (soft,hard) if v!=resource.RLIM_INFINITY])
            resource.setrlimit(key,(limit,hard))
    except (ImportError,AttributeError,OSError,ValueError):pass
    result=dict(verified=False)
    try:
        source=Path(args.certificate)
        if source.stat().st_size>1024**2:raise ValueError('Small clean certificate required')
        def unique(pairs):
            values={}
            for key,value in pairs:
                if key in values:raise ValueError('Duplicate certificate key')
                values[key]=value
            return values
        raw=source.read_bytes();payload=json.loads(raw,object_pairs_hook=unique)
        pins=payload['source_sha256'];required={'run.py','README.md','requirements.txt','MATCHING_AND_POSITIVITY.md','verify_certificate.py'}
        if set(pins)!=required:raise ValueError('Exact public source/theorem bindings required')
        def hashes():return {name:hashlib.sha256((home/name).read_bytes()).hexdigest() for name in required}
        if hashes()!=pins:raise ValueError('Public source/theorem digest mismatch')
        result.update(verify(payload,home/'run.py',check));check()
        if hashes()!=pins or source.read_bytes()!=raw:raise RuntimeError('Certificate/source changed during verification')
        result['certificate_sha256']=hashlib.sha256(raw).hexdigest()
    except (Exception,KeyboardInterrupt) as error:
        result=dict(verified=False,error=type(error).__name__+': '+str(error))
    result['process_CPU_seconds']=time.process_time()-started
    text=json.dumps(result,indent=2,allow_nan=False)
    if args.output:
        with Path(args.output).open('x',encoding='utf-8') as output:output.write(text+'\n')
    print(text,flush=True)
    return 0 if result['verified'] else 1


if __name__=='__main__':raise SystemExit(main())
